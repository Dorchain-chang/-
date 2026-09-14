#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mail_bridge.py —— 邮件取信桥（数据源管线 · 方式 B / IMAP 直读）

把任意支持 IMAP 的邮箱（QQ / Gmail / 163 / Outlook / 企业邮箱）里的
校招通知（笔试 / 面试 / Offer / 感谢信）抓出来，解析成统一消息格式，
写入「求职情报收件箱」表（建议，永不直改投递跟踪，需人工确认）。

纯 Python 标准库（imaplib / email / urllib），零第三方依赖。

用法:
  python pages/mail_bridge.py --self-test               # 内置样例自测解析器（不需要邮箱）
  python pages/mail_bridge.py --dry-run                 # 连邮箱解析并打印，不写任何地方
  python pages/mail_bridge.py --out local               # 写本地队列 pages/mail_outbox_queue.json
  printf '%s\n' '<token>' | python pages/mail_bridge.py --out api --token-stdin
                                                        # 直接写入资料库收件箱表

配置: pages/mail_config.json（含授权码，已进 .gitignore，绝不提交）
模板: pages/mail_config.example.json
"""
from __future__ import annotations

import argparse
import email
import email.utils
import imaplib
import json
import re
import ssl
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from email.header import decode_header, make_header
from email.message import Message
from pathlib import Path

SELF = Path(__file__).resolve().parent
CONFIG_PATH = SELF / "mail_config.json"
SEEN_PATH = SELF / "mail_seen.json"
QUEUE_PATH = SELF / "mail_outbox_queue.json"

INBOX_DB_ID = "EdCHnKtjZIXEw37tUmvhqL"
API_BASE = "https://www.workbuddy.cn"
API_ADD = "/space/api/agent/v1/batch-add-records"

# IMAP 服务商预设（host, port, ssl）
PROVIDERS = {
    "qq": ("imap.qq.com", 993, True),
    "gmail": ("imap.gmail.com", 993, True),
    "163": ("imap.163.com", 993, True),
    "outlook": ("outlook.office365.com", 993, True),
}

# 分类关键词（按优先级，先命中先定类型）；排除词防「面经分享」误判
EXCLUDE_WORDS = ["面经", "经验分享", "攻略", "题库", "回忆版", "拒信统计", "求职交流"]
TYPE_RULES = [
    ("Offer", ["offer", "录用", "录用通知", "恭喜你", "入职邀请", "欢迎加入"]),
    ("笔试", ["笔试", "在线考试", "测评邀请", "性格测评", "行测", "考务"]),
    ("面试", ["面试", "复试", "一面", "二面", "三面", "终面", "hr面", "面试邀请", "视频面"]),
    ("感谢信", ["感谢信", "遗憾", "未能通过", "暂不推进", "很遗憾", "不匹配"]),
]
SNIPPET_LEN = 500

# 常见招聘域名 → 中文名（命中直接给高置信度）
DOMAIN_MAP = {
    "tencent": "腾讯", "bytedance": "字节跳动", "alibaba": "阿里", "taobao": "阿里",
    "meituan": "美团", "jd": "京东", "netease": "网易", "baidu": "百度",
    "xiaomi": "小米", "huawei": "华为", "didiglobal": "滴滴", "didi": "滴滴",
    "byd": "比亚迪", "bosch": "博世", "sap": "SAP", "microsoft": "微软",
    "google": "谷歌", "apple": "苹果", "nvidia": "英伟达", "intel": "英特尔",
    "oppo": "OPPO", "vivo": "vivo", "honor": "荣耀", "zte": "中兴",
    "shein": "希音", "pinduoduo": "拼多多", "kuaishou": "快手", "bilibili": "B站",
}


# ---------------------------------------------------------------- 解析层

def decode_mime(s: str | None) -> str:
    """RFC2047 解码主题/发件人（=?gbk?B?...?= 之类）。"""
    if not s:
        return ""
    try:
        return str(make_header(decode_header(s)))
    except Exception:
        return s or ""


def get_body_snippet(msg: Message) -> str:
    """取正文前 SNIPPET_LEN 字（text/plain 优先，html 剥标签）。"""
    text = ""
    if msg.is_multipart():
        parts = msg.walk()
        candidates = []
        for p in parts:
            if p.get_content_maintype() != "text" or p.get_filename():
                continue
            candidates.append((p.get_content_subtype(), p))
        candidates.sort(key=lambda x: 0 if x[0] == "plain" else 1)  # plain 优先
        for _, p in candidates:
            payload = p.get_payload(decode=True)
            if not payload:
                continue
            charset = p.get_content_charset() or "utf-8"
            for enc in (charset, "gb18030", "utf-8"):
                try:
                    text = payload.decode(enc, errors="strict")
                    break
                except (LookupError, UnicodeDecodeError):
                    continue
            if text.strip():
                break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            for enc in (charset, "gb18030", "utf-8"):
                try:
                    text = payload.decode(enc, errors="strict")
                    break
                except (LookupError, UnicodeDecodeError):
                    continue
    text = re.sub(r"<style[\s\S]*?</style>|<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:SNIPPET_LEN]


def extract_company(from_name: str, from_addr: str, subject: str) -> str:
    """公司归一化：显示名 > 域名映射 > 主题【X】前缀。"""
    name = re.sub(r"(招聘|校招|校园招聘|人才|HR|人力|资深|官方|official|noreply|no-reply|通知)",
                  "", from_name, flags=re.I).strip(" 【】·-—")
    if 1 < len(name) <= 20 and not re.fullmatch(r"[\d@.\s]+", name):
        return name
    domain = (from_addr.split("@")[-1].split(".")[0] if "@" in from_addr else "").lower()
    if domain in DOMAIN_MAP:
        return DOMAIN_MAP[domain]
    m = re.search(r"【([^】]{1,20})】", subject)
    if m:
        return m.group(1).strip()
    return ""


def classify(subject: str, snippet: str) -> tuple[str, str]:
    """→ (类型, 置信度)。排除词先行，防面经分享误判。"""
    text = (subject + " " + snippet).lower()
    if any(w in text for w in EXCLUDE_WORDS):
        return ("其他", "低")
    for typ, words in TYPE_RULES:
        if any(w in text for w in words):
            hits = sum(1 for w in words if w in text)
            return (typ, "高" if hits >= 2 else "中")
    return ("其他", "低")


def to_record(company: str, typ: str, conf: str, when_iso: str,
              snippet: str, sender: str, msg_id: str, recv_iso: str) -> dict:
    """统一消息格式 → 收件箱表 properties（状态恒为 待确认：解析只出建议）。"""
    return {
        "公司": {"text": company or "（未识别）"},
        "类型": {"select": typ},
        "事项时间": {"date": when_iso},
        "原文摘要": {"text": snippet},
        "发件人": {"text": sender[:120]},
        "来源": {"select": "邮件"},
        "状态": {"select": "待确认"},
        "置信度": {"select": conf},
        "消息ID": {"text": msg_id},
        "收件时间": {"date": recv_iso},
    }


def parse_message(raw: bytes, account: str) -> dict | None:
    """原始邮件 → 统一消息 dict；不含关键词/被排除词命中的返回 None。"""
    msg = email.message_from_bytes(raw)
    subject = decode_mime(msg.get("Subject", ""))
    from_name, from_addr = email.utils.parseaddr(decode_mime(msg.get("From", "")))
    msg_id = (msg.get("Message-ID") or msg.get("Message-Id") or "").strip()
    try:
        when = email.utils.parsedate_to_datetime(msg.get("Date"))
    except (TypeError, ValueError):
        when = datetime.now(timezone.utc)
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    recv_iso = when.astimezone(timezone(timedelta(hours=8))).isoformat(timespec="seconds")

    snippet = get_body_snippet(msg)
    text = subject + " " + snippet
    if any(w in text for w in EXCLUDE_WORDS):
        return None
    typ, conf0 = classify(subject, snippet)
    if typ == "其他" and conf0 == "低" and not any(
            w in text.lower() for _, ws in TYPE_RULES for w in ws):
        return None  # 与校招通知无关的普通邮件
    company = extract_company(from_name, from_addr, subject)
    domain = (from_addr.split("@")[-1].split(".")[0] if "@" in from_addr else "").lower()
    conf = conf0
    if conf == "高" and domain not in DOMAIN_MAP:
        conf = "中"  # 陌生域名的公司归一化不可靠，置信度封顶「中」
    return {
        "key": f"{account}|{msg_id or (subject + recv_iso)}",
        "record": to_record(company, typ, conf, recv_iso, snippet,
                            f"{from_name} <{from_addr}>", msg_id or "-", recv_iso),
    }


# ---------------------------------------------------------------- 取信层

def fetch_account(acc: dict, since_days: int, limit: int) -> list[dict]:
    host, port, use_ssl = PROVIDERS.get(acc.get("provider", ""), ("", 0, False))
    if not host:
        print(f"  [跳过] 未知 provider: {acc.get('provider')}")
        return []
    user, code = acc["user"], acc["auth_code"]
    print(f"  连接 {host}:{port} ({user}) ...")
    conn = imaplib.IMAP4_SSL(host, port, ssl_context=ssl.create_default_context()) if use_ssl \
        else imaplib.IMAP4(host, port)
    conn.login(user, code)
    conn.select("INBOX", readonly=True)
    # IMAP 搜索日期必须用英文月份缩写，中文 locale 下 strftime 会给出"9月"，这里手动拼
    en_mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    d = datetime.now() - timedelta(days=since_days)
    since = f'{d.day:02d}-{en_mon[d.month - 1]}-{d.year}'
    typ, data = conn.uid("SEARCH", None, f'(SINCE "{since}")')
    if typ != "OK":
        return []
    uids = data[0].split()[-limit:]
    out = []
    for uid in uids:
        typ, mdata = conn.uid("FETCH", uid, "(RFC822)")
        if typ != "OK" or not mdata or mdata[0] is None:
            continue
        try:
            parsed = parse_message(mdata[0][1], user)
        except Exception as e:  # 单封坏邮件不能拖垮整批
            print(f"  [警告] 解析 uid={uid.decode()} 失败: {e}")
            continue
        if parsed:
            out.append(parsed)
    conn.logout()
    print(f"  命中 {len(out)} 条通知")
    return out


# ---------------------------------------------------------------- 输出层

def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return default


def dedupe(items: list[dict]) -> list[dict]:
    seen = set(load_json(SEEN_PATH, []))
    fresh = [it for it in items if it["key"] not in seen]
    seen.update(it["key"] for it in fresh)
    SEEN_PATH.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=1),
                         encoding="utf-8")
    return fresh


def write_api(records: list[dict], token: str) -> bool:
    body = json.dumps({"databaseId": INBOX_DB_ID, "records": records},
                      ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(API_BASE + API_ADD, data=body, method="POST", headers={
        "Accept": "*/*", "Content-Type": "application/json",
        "X-Skill-Token": token, "User-Agent": "mail-bridge/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            ok = str(data.get("code", "0")) in ("0", "200")
            print(f"  写入收件箱表: {'成功 ' + str(len(records)) + ' 条' if ok else data}")
            return ok
    except Exception as e:
        print(f"  [错误] 写入失败: {e} → 已存本地队列兜底")
        return False


def write_queue(records: list[dict]) -> None:
    q = load_json(QUEUE_PATH, [])
    q.extend(records)
    QUEUE_PATH.write_text(json.dumps(q, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  已写入本地队列 {QUEUE_PATH.name}（共 {len(q)} 条待推）")


# ---------------------------------------------------------------- 入口

def self_test() -> int:
    """内置样例邮件自测解析器（无需真实邮箱）。"""
    samples = [
        ("腾讯校园招聘 <campus@tencent.com>", "【腾讯】面试邀请-技术岗",
         "您好，恭喜进入一面，请于 9 月 20 日 14:00 参加视频面试", "面试", "高"),
        ("字节跳动招聘 <noreply@bytedance.com>", "笔试通知",
         "请按时参加 9 月 18 日的在线考试，范围包括数据结构与算法", "笔试", "高"),
        ("牛客 <noreply@nowcoder.com>", "【面经分享】腾讯一面回忆版",
         "牛客网友分享的面试经验帖，欢迎围观题库", None, None),
        ("某公司HR <hr@unknown-corp.cn>", "感谢信",
         "很遗憾地通知您，本次未能通过，感谢投递", "感谢信", "中"),
        ("同学 <friend@qq.com>", "周末聚餐",
         "周六晚上一起吃饭吗？", None, None),
    ]
    fails = 0
    for frm, subj, body, want_typ, want_conf in samples:
        raw = (
            f"From: {frm}\r\nTo: me@qq.com\r\nSubject: =?utf-8?B?"
            f"{__import__('base64').b64encode(subj.encode()).decode()}?=\r\n"
            f"Date: Mon, 14 Sep 2026 10:00:00 +0800\r\n"
            f"Message-ID: <test-{hash(subj) & 0xffff}@local>\r\n"
            f"Content-Type: text/plain; charset=utf-8\r\n\r\n{body}\r\n"
        ).encode("utf-8")
        got = parse_message(raw, "test@qq.com")
        if want_typ is None:
            status = "OK(过滤)" if got is None else "FAIL"
            if got is not None:
                fails += 1
        else:
            ok = got and got["record"]["类型"]["select"] == want_typ \
                and got["record"]["置信度"]["select"] == want_conf
            status = "OK" if ok else (
                "FAIL got=%s/%s" % (got and got["record"]["类型"]["select"],
                                    got and got["record"]["置信度"]["select"]))
            if not ok:
                fails += 1
        print(f"  [{status}] {subj}")
    print("自测通过" if fails == 0 else f"自测失败 {fails} 例")
    return 1 if fails else 0


def main() -> int:
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--out", choices=["api", "local"], default="local")
    ap.add_argument("--token-stdin", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not CONFIG_PATH.exists():
        print(f"缺配置：复制 {CONFIG_PATH.name + '.example.json'} 为 {CONFIG_PATH.name} 并填授权码")
        return 1
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    items: list[dict] = []
    for acc in cfg.get("accounts", []):
        try:
            items.extend(fetch_account(acc, cfg.get("since_days", 3), cfg.get("max_per_account", 100)))
        except imaplib.IMAP4.error as e:
            print(f"  [错误] {acc.get('user')} 登录/读取失败（检查授权码/IMAP开关）: {e}")
        except Exception as e:
            print(f"  [错误] {acc.get('user')}: {e}")
    fresh = dedupe(items)
    records = [it["record"] for it in fresh]
    print(f"共解析 {len(items)} 条，去重后新增 {len(records)} 条")
    if args.dry_run:
        for r in records:
            print("  ·", r["公司"]["text"], "|", r["类型"]["select"], "|", r["置信度"]["select"],
                  "|", r["原文摘要"]["text"][:40])
        return 0
    if not records:
        return 0
    if args.out == "api":
        token = ""
        if args.token_stdin and not sys.stdin.isatty():
            raw_in = sys.stdin.read() or ""
            lines = raw_in.strip().splitlines()
            token = lines[0].strip() if lines else ""
        if not token:
            print("[错误] api 模式需要 --token-stdin 传入 token（30 分钟有效，过期重取）")
            return 1
        if not write_api(records, token):
            write_queue(records)
    else:
        write_queue(records)
    return 0


if __name__ == "__main__":
    sys.exit(main())
