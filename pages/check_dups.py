import json, subprocess, sys
from collections import Counter

DB_DIR = r"D:/workbuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library/database"
PY = sys.executable
DB_ID = "GgZ71tywhs4HEZytFSqXTP"
token = sys.stdin.readline().strip()
out, cur = [], None
while True:
    args = [PY, DB_DIR + "/query_database_record.py", "--database-id", DB_ID, "--page-size", "100", "--token-stdin"]
    if cur:
        args += ["--start-cursor", cur]
    r = subprocess.run(args, input=(token + "\n").encode(), capture_output=True)
    d = json.loads(r.stdout.decode("utf-8", "replace").strip().splitlines()[0])
    if "error" in d:
        print("ERR", d)
        break
    out += d.get("results") or []
    cur = d.get("next_cursor")
    if not cur or not d.get("has_more"):
        break


def txt(p, k):
    v = p.get(k)
    if isinstance(v, list):
        v = (v[0] or {}).get("text") if v else ""
    if isinstance(v, dict):
        v = v.get("text")
    return str(v or "").strip()


props = [rec.get("properties") or rec for rec in out]
c = Counter(txt(p, "公司") for p in props)
dup = {k: v for k, v in c.items() if v > 1}
print("TOTAL:", len(out), "unique companies:", len(c), "dups:", len(dup))
if dup:
    print("DUP NAMES:", list(dup.items())[:20])
