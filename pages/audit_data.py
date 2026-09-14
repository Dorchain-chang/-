#!/usr/bin/env python3
"""只读审计：统计三表记录数、字段缺失、重复公司、体积估算。不写任何数据。"""
import json, sys, subprocess, collections

DB = r"D:/workbuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library/database"
PY = sys.executable

TABLES = {
    "秋招岗位清单": "GgZ71tywhs4HEZytFSqXTP",
    "投递跟踪": "oBGkMFTv9Xv4Xn5gFOK18S",
    "成都实习岗位": "tgH8096uENTaIj8RSY9qm5",
}


def q(dbid, token, cursor=None):
    args = [PY, DB + "/query_database_record.py", "--database-id", dbid, "--page-size", "100", "--token-stdin"]
    if cursor:
        args += ["--start-cursor", cursor]
    r = subprocess.run(args, input=(token + "\n").encode(), capture_output=True)
    out = r.stdout.decode("utf-8", "replace").strip()
    try:
        return json.loads(out.splitlines()[0])
    except Exception:
        return {"error": out[:300]}


def main():
    token = sys.stdin.readline().strip()
    for name, dbid in TABLES.items():
        recs, cur, pages = [], None, 0
        while pages < 60:
            d = q(dbid, token, cur)
            if "error" in d:
                print(f"[{name}] QUERY FAIL {d['error']}"); break
            recs += d.get("results") or []
            cur = d.get("next_cursor") or d.get("nextCursor")
            pages += 1
            if not cur or not (d.get("has_more") or d.get("hasMore")):
                break
        if not recs:
            continue
        size = len(json.dumps(recs, ensure_ascii=False).encode())
        keys = collections.Counter()
        for r in recs:
            for k in r.keys():
                if k != "record_id":
                    keys[k] += 1
        comp = collections.Counter()
        for r in recs:
            c = r.get("公司")
            if isinstance(c, list):
                c = c[0].get("text") if c and isinstance(c[0], dict) else ""
            comp[str(c or "").strip()] += 1
        dups = {k: v for k, v in comp.items() if v > 1}
        empt = sum(1 for r in recs if not str(r.get("公司") or "").strip())
        print(f"\n=== {name} ({dbid}) ===")
        print(f"记录数: {len(recs)}   序列化体积: {size/1024:.1f} KB   平均: {size/max(len(recs),1):.0f} B/条")
        print(f"公司为空: {empt}   重复公司: {len(dups)} 组 -> {dict(list(dups.items())[:12])}")
        total = len(recs)
        for k, v in keys.most_common():
            print(f"   {k}: {v}/{total} ({v*100//total}%)")


if __name__ == "__main__":
    main()
