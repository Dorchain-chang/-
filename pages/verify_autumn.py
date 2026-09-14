import json, subprocess, sys
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
print("TOTAL records:", len(out))


def txt(p, k):
    v = p.get(k)
    if isinstance(v, list):
        v = (v[0] or {}).get("text") if v else ""
    if isinstance(v, dict):
        v = v.get("text")
    return str(v or "").strip()


want = ["英雄游戏", "厦门海尼电子商务有限公司", "江苏曙光", "天翼安全", "广州地铁",
        "进迭时空", "雷赛智能", "四达时代", "珀莱雅", "千象资产", "中国农业银行上海市分行"]
props = [rec.get("properties") or rec for rec in out]
have = set(txt(p, "公司") for p in props)
print("present:", {w: (w in have) for w in want})
src = {}
for p in props:
    s = txt(p, "来源")
    src[s] = src.get(s, 0) + 1
print("by 来源:", src)
nk = sum(1 for p in props if txt(p, "牛客ID"))
print("with 牛客ID:", nk)
