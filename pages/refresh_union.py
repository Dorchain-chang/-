#!/usr/bin/env python3
"""刷新 schema_union.json：把四张表的实时 schema 拼成一份并集快照（构建/交接用的契约文件）。

用法: printf '%s\\n' '<token>' | python pages/refresh_union.py
"""
import json
import subprocess
import sys

DB = r"D:/workbuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library/database"
PY = sys.executable

TABLES = [
    ("GgZ71tywhs4HEZytFSqXTP", "秋招岗位清单"),
    ("oBGkMFTv9Xv4Xn5gFOK18S", "投递跟踪"),
    ("tgH8096uENTaIj8RSY9qm5", "成都实习岗位"),
    ("EdCHnKtjZIXEw37tUmvhqL", "求职情报收件箱"),
]


def main():
    token = sys.stdin.readline().strip()
    if not token:
        print("NO TOKEN")
        return 1
    out, seen = [], set()
    for dbid, label in TABLES:
        r = subprocess.run([PY, DB + "/get_database_schema.py", "--database-id", dbid, "--token-stdin"],
                           input=(token + "\n").encode(), capture_output=True)
        d = json.loads(r.stdout.decode("utf-8", "replace").strip().splitlines()[0])
        props = d.get("properties") or d.get("data", {}).get("properties") or []
        print(f"  {label}: {len(props)} 字段")
        for p in props:
            name = p.get("name")
            if name and name not in seen:
                seen.add(name)
                out.append({k: v for k, v in p.items() if k in ("id", "name", "type", "config")})
    doc = {"id": "union", "title": "union", "properties": out}
    for path in ("schema_union.json", "pages/schema_union.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
    print("union 字段总数:", len(out))
    print([p["name"] for p in out])
    return 0


if __name__ == "__main__":
    sys.exit(main())
