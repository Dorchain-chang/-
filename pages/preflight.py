#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键预检：构建 → 静态守卫 → 官方 lint → 浏览器冒烟。

用法:
    python pages/preflight.py            # 全量（含浏览器冒烟）
    python pages/preflight.py --no-browser

退出码 0 表示全部通过。任何一步失败立刻中止并打印原因。
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
PY = sys.executable

LIB = Path(r"D:/workbuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library/page")
MANAGED_NODE = Path(r"C:/Users/窦畅/.workbuddy/binaries/node/versions/22.22.2-3/node.exe")
NODE_MODULES = Path(r"C:/Users/窦畅/.workbuddy/binaries/node/workspace/node_modules")
# check_workflows.py 需要 pyyaml，装在隔离 venv 里，避免污染系统 Python
VENV_PY = Path(r"C:/Users/窦畅/.workbuddy/binaries/python/envs/default/Scripts/python.exe")

PAGES = ["00-总览台", "01-秋招岗位台", "02-央国企台", "03-成都实习台"]
PER_PAGE_SCHEMA = {
    "00-总览台": "canonical_overview.json",
    "01-秋招岗位台": "canonical_autumn.json",
    "02-央国企台": "canonical_soe.json",
    "03-成都实习台": "canonical_intern.json",
}

results = []


def run(label, cmd, cwd=None, stdin_file=None, env=None, allow_fail=False):
    print(f"\n=== {label} ===")
    e = dict(os.environ)
    if env:
        e.update(env)
    data = None
    if stdin_file:
        data = open(stdin_file, "rb").read()
    r = subprocess.run(cmd, cwd=cwd or ROOT, input=data, capture_output=True, env=e)
    out = (r.stdout or b"").decode("utf-8", "replace").strip()
    err = (r.stderr or b"").decode("utf-8", "replace").strip()
    if out:
        print(out[:1200])
    if err and "SyntaxWarning" not in err:
        print("[stderr]", err[:600])
    ok = r.returncode == 0
    results.append((label, ok))
    if not ok and not allow_fail:
        print(f"!!! 失败：{label}")
        summary()
        sys.exit(1)
    return ok, out


def summary():
    print("\n================ 预检汇总 ================")
    for label, ok in results:
        print(("  PASS  " if ok else "  FAIL  ") + label)
    failed = [l for l, ok in results if not ok]
    print("==========================================")
    print("全部通过 " if not failed else f"存在失败项 {len(failed)} 个")


def main():
    no_browser = "--no-browser" in sys.argv

    run("1) 生成四个独立页 + 合并单文件 + demo",
        [PY, "pages/build_pages.py"])
    run("2) 生成合并版单文件", [PY, "pages/build_single.py"])
    run("3) 生成 demo（离线 mock 版）", [PY, "pages/build_demo.py"])
    run("4) 转义陷阱守卫（Python 模板串吃掉 JS 转义 / 裸控制字符）",
        [PY, "pages/check_escapes.py"])
    run("5) workflow YAML 自检",
        [str(VENV_PY) if VENV_PY.exists() else PY, "pages/check_workflows.py"])
    run("6) 内联 JS 语法", [PY, "pages/check_inline_js.py"])

    if LIB.exists():
        for page in PAGES:
            schema = HERE / PER_PAGE_SCHEMA[page]
            r = subprocess.run([PY, str(LIB / "lint_schema.py"), "--stdin", "--html", str(HERE / f"{page}.html")],
                               input=schema.read_bytes(), capture_output=True)
            ok = b"MINDX_LINT_OK" in r.stdout and r.returncode == 0
            print(f"  {page}: {'OK' if ok else r.stdout.decode('utf-8', 'replace').strip()[:200]}")
            results.append((f"7) schema lint · {page}", ok))
        for page in PAGES:
            r = subprocess.run([PY, str(LIB / "lint_database_sdk_usage.py"),
                                "--html", str(HERE / f"{page}.html"),
                                "--schema-file", str(ROOT / "canonical_schema.json")], capture_output=True)
            ok = b"MINDX_DBSDK_LINT_OK" in r.stdout
            print(f"  {page}: {'OK' if ok else r.stdout.decode('utf-8', 'replace').strip()[:200]}")
            results.append((f"8) SDK lint · {page}", ok))
    else:
        print("!! 未找到官方 lint 脚本目录，跳过 7/8")

    if not no_browser:
        if MANAGED_NODE.exists():
            run("9) 浏览器冒烟（mock SDK，620 岗位 / 实时订阅 / 交互）",
                [str(MANAGED_NODE), "pages/smoke_browser.js"],
                env={"NODE_PATH": str(NODE_MODULES)})
        else:
            print("!! 未找到托管 node，跳过浏览器冒烟")

    summary()
    failed = [l for l, ok in results if not ok]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
