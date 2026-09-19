#!/usr/bin/env python3
"""Deploy built pages to the library via the page edit transaction flow.

Token comes from stdin first line (never written to disk).
For each (node_id, local_html): create tx -> list artifacts -> PUT entry html -> commit.
"""
import json, sys, os, subprocess, urllib.request

SKILL_DIR = r"D:/workbuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library"
PAGE_DIR = os.path.join(SKILL_DIR, "page")
HERE = os.path.dirname(os.path.abspath(__file__))

SINGLE = "00-总览台.html"

# 单文件应用：同一个文件推到全部节点，任何旧链接打开都是完整四模块应用
PAGES = [
    ("szZlSjyPnnpGwDW4OD4y0X", SINGLE),
    ("G9pPkUVWIc6Fk43Mnn1csc", SINGLE),
    ("PQ5cLpifIyB1CaQB2OIMrm", SINGLE),
    ("JgXPaIiaDMGt2xH3vBftAo", SINGLE),
]

MSG = "v33 新 UI：左侧边栏「发现 / 我的 / 配置」三组导航；新增求职助理（对话式，本机检索做上下文）、定时任务（到期浮出今日提醒）、日程安排（投递节点+邮箱事项+任务聚合）、邮件解析工作台（粘贴原文→AI 抽取→确认写入）；个人知识库 / 投递记录 / 招聘邮箱 / AI 配置全部升级为一级页"


def run_page_script(name, args, token):
    cmd = [sys.executable, os.path.join(PAGE_DIR, name)] + args
    r = subprocess.run(cmd, input=(token + "\n").encode(), capture_output=True)
    out = r.stdout.decode("utf-8", "replace").strip()
    # stdout may be `<json>` optionally followed by KS_* status lines; parse first line
    first = out.splitlines()[0].strip() if out else ""
    try:
        return json.loads(first)
    except Exception:
        return {"error": (out or r.stderr.decode("utf-8", "replace"))[:300]}


def http_put(url, data):
    req = urllib.request.Request(url, data=data, method="PUT")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.status


def main():
    token = sys.stdin.readline().strip()
    if not token:
        print("NO TOKEN"); return
    ok, fail = 0, 0
    for node_id, fname in PAGES:
        local = os.path.join(HERE, fname)
        with open(local, encoding="utf-8") as f:
            html = f.read()
        print(f"== {fname} -> {node_id}")
        # 1. create transaction
        tx = run_page_script("create_page_transaction.py", ["--token-stdin", "--node-id", node_id], token)
        if "error" in tx or "data" not in tx:
            print("  TX FAIL:", json.dumps(tx, ensure_ascii=False)[:200]); fail += 1; continue
        txid = tx["data"]["transactionId"]; base = tx["data"]["baseVersion"]
        # 2. list artifacts (base version)
        la = run_page_script("list_page_artifacts.py", ["--token-stdin", "--node-id", node_id, "--version", str(base)], token)
        if "error" in la or "data" not in la:
            print("  LIST FAIL:", json.dumps(la, ensure_ascii=False)[:200]); fail += 1; continue
        entry = None
        for a in la["data"].get("artifacts", []):
            p = a.get("path", "")
            if p.lower().endswith(".html"):
                entry = p; break
        if not entry:
            print("  NO HTML ARTIFACT"); fail += 1; continue
        # 3. upload entry html
        up = run_page_script("get_page_upload_url.py", ["--token-stdin", "--transaction-id", txid, "--path", entry], token)
        if "error" in up or "data" not in up:
            print("  UPLOAD URL FAIL:", json.dumps(up, ensure_ascii=False)[:200]); fail += 1; continue
        status = http_put(up["data"]["uploadUrl"], html.encode("utf-8"))
        if status not in (200, 201):
            print(f"  PUT status={status}"); fail += 1; continue
        # 4. commit
        cm = run_page_script("commit_page_transaction.py", ["--token-stdin", "--transaction-id", txid, "--message", MSG], token)
        if "error" in cm:
            print("  COMMIT FAIL:", json.dumps(cm, ensure_ascii=False)[:200]); fail += 1; continue
        d = cm.get("data", {})
        print(f"  OK v{d.get('newVersion')} url={d.get('url', '')}")
        ok += 1
    print(f"DONE ok={ok} fail={fail}")


if __name__ == "__main__":
    main()
