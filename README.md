# 秋招求职台 (Qiuzhao Workbench)

> 一个为 2027 届校招求职定制的个人数字工作台，解决"打开一个超长页面、翻好久才能翻到不同模块"的效率问题。

## 这是什么

这是为求职季（秋招/实习）量身打造的**单文件工作台**，核心目标是**不让用户在同一个长页面里上下滚动找东西**。

工作台使用 [腾讯文档·资料库](https://docs.qq.com) 的「在线 page」+「数据表」能力部署，数据云端同步、多设备共享。

**在线 demo（不需要登录，数据只存在你自己的浏览器里）**：<https://dorchain-chang.github.io/-/>

## 单文件应用 + 页内 Tab 切换

整个工作台是**一个 HTML 文件**，用页内 Tab 在 4 个模块之间切换：不跳转、不滚动找模块，三张表的数据也只加载一次。

| 模块 | 用途 |
|------|------|
| **总览台** | 统一管理 / 今天要处理 / 投递跟踪 / 模块入口 |
| **秋招岗位** | 互联网/科技/制造业等非央国企岗位（按 城市/职业/批次 筛选） |
| **央国企** | 央企/银行/运营商/电网/烟草等，按公司名关键词自动识别 + 红色卡片 |
| **成都实习** | 实习岗位专区，BOSS 直聘手动收录 + 牛客每日同步 |

> 演进历史：最早是 4 个独立节点互相跳转，后来合并为单文件应用——跨节点跳转会让 SDK 重新初始化、数据重新拉取，体验反而更差。
> `pages/01~03` 仍保留各模块的**独立版**，方便单独引用或回退。

## 核心功能

- **「今天要处理」自动汇总**：逾期岗位（红）/ 3 天内截止（橙）/ 今天的面试节点（蓝），不切换 Tab 就能看到今天该做什么
- **分类清晰**：秋招/实习 一键 chip 切换；央国企/其他企业 自动分流到「央国企」和「秋招岗位」两个 Tab
- **直达 vs 搜索**：有网申链接 → 绿色按钮直达；没链接 → 灰色虚线按钮（自动跳牛客/必应搜索）
- **投一个存一个**：岗位看板点「标已投」会自动在投递跟踪表建一条记录（按公司去重）
- **每日自动同步**：每天 9:00 自动抓牛客校招日程（含 AI/算法/数据 等方向）的有效期内岗位，补齐到岗位清单表
- **公司情报 · 牛客直达**：任意一条岗位（含表外公司）都能一键查情报；有 `牛客ID` 时首出该公司的**主页 / 面经 / 真题 / 薪资 / 讨论** 5 条精准深链，没有则降级为全网检索
- **B 站反爬实测**：BOSS 直聘有反爬，无法自动抓取 → 改为「BOSS 上手动复制链接 + 一键收录」+ 牛客 daily sync 兜底

## 数据结构

工作台背后是 3 张数据表（都在腾讯文档·资料库里）：

| 表名 | 字段（类型） | 表 ID |
|------|------|-------|
| 秋招岗位清单 | 公司(text) / 批次(select: 27秋招·27暑期实习·27日常实习·其他) / 岗位方向(text) / 工作地点(text) / 优先级(select: P0·P1·P2) / 投递状态(select: 待投递·已投递·不投了) / 网申开始(date) / 截止日期(date) / 投递链接(url) / 来源(text) / 备注(text) / **牛客ID(text)** | `GgZ71tywhs4HEZytFSqXTP` |
| 简历投递跟踪 | 公司(text) / 岗位(text) / 当前阶段(select: 已投递·笔试·一面·二面·HR面·Offer·感谢信·已终止) / 投递日期(date) / 下次节点(date) / 节点说明(text) / 复盘笔记(text) / 相关链接(url) | `oBGkMFTv9Xv4Xn5gFOK18S` |
| 成都实习岗位 | 公司(text) / 岗位名称(text) / 薪资(text) / 工作地点(text) / 岗位要求(text) / 投递状态(select) / 投递链接(url) / 来源(text) / 备注(text) / 网申开始(date) / 截止日期(date) / **牛客ID(text)** | `tgH8096uENTaIj8RSY9qm5` |

> **`牛客ID`** 存牛客企业 `companyId`，有它时「公司情报」按钮会首出 5 条精准直达深链（`enterprise/{id}` 主页 / `interview` 面经 / `question/company` 真题 / `salary` 薪资 / `discussion` 讨论），比按公司名搜索准得多。同步脚本会自动回填；历史数据用 `python pages/backfill_nowcoder.py` 一次性补齐。

## 技术栈

- 单文件 HTML + 内联 CSS + 内联 JS（零外部依赖）
- 内联 SVG 图标（不用 emoji、不用图标库）
- 自适应 PC / 移动端，窄屏单列，按钮 ≥ 32px（移动端 ≥ 44px）
- Tencent 资料库的 SDK：`db.query / db.addRecord / db.updateRecord / db.deleteRecord`
- 沙箱内 `window.open` 被拦截的兜底方案：弹层 + 一键复制链接
- 自动同步：WorkBuddy「automation」能力，每天 9:00 + 9:30 各抓一次牛客

## 目录结构

```
.
├── README.md                      # 本文件
├── HANDOVER.md                    # 交接文档（坑 / schema / 待办）
├── PUSH_TO_GITHUB.md              # 发布与 CI 说明
├── canonical_schema.json          # 构建输入：字段 + 选项（build_pages.py 依赖，别删）
├── schema_union.json              # 构建输入：三张表的 schema 快照
├── pages/                         # 生产页 + 全部构建脚本
│   ├── 00-总览台.html             #   · build_single.py 产出的合并版单文件应用
│   ├── 01-秋招岗位台.html         #   · 独立版：非央国企岗位看板
│   ├── 02-央国企台.html           #   · 独立版：央国企专栏
│   ├── 03-成都实习台.html         #   · 独立版：成都实习专区
│   ├── build_pages.py             #   · ① 生成 4 个独立模块页
│   ├── build_single.py            #   · ② 合并成单文件应用
│   ├── build_demo.py              #   · ③ 套 localStorage mock 生成 demo/
│   ├── preflight.py               #   · 一键预检（构建 + 15 项 lint / 冒烟，见下）
│   ├── check_escapes.py           #   · P0 守卫：Python 模板串吃掉 JS 反斜杠转义 / 裸控制字符
│   ├── smoke_browser.js           #   · Playwright 冒烟：mock 三表跑初始化/筛选/情报/订阅
│   ├── perf_probe.js              #   · 性能探针：首屏耗时 / 重渲染 / JS 堆 / DOM 节点
│   ├── ab_cache.js                #   · A/B：分类缓存开关对重渲染耗时的影响
│   ├── audit_data.py              #   · 数据体检（只读）：记录数/体积/字段覆盖/重复公司
│   ├── sync_interns.py            #   · 牛客校招日程 → 实习表 同步脚本
│   ├── sync_autumn_all.py         #   · 牛客 tab=3 全量 → 秋招表（有效期过滤，单次≤60）
│   ├── sync_nowcoder_autumn.py    #   · 牛客 tab=3 → 秋招表（AI/算法方向筛选，单次≤30）
│   ├── backfill_nowcoder.py       #   · 按公司名回填「牛客ID」（企业档案深链用）
│   ├── refresh_union.py           #   · 刷新 schema_union.json（三表字段并集）
│   ├── check_dups.py              #   · 检查合并版重复 id / 函数重复定义
│   ├── verify_autumn.py           #   · 秋招表抽样校验
│   └── deploy_pages.py            #   · 推到腾讯文档·资料库节点（4 节点同推单文件）
├── demo/                          # GitHub Pages 站点，零依赖
│   └── index.html                 #   · 合并版应用 + mock 数据
├── docs/
│   ├── DEPLOY.md                  # 部署到腾讯文档·资料库的步骤
│   └── AUDIT-2026-09-14.md        # 上线前终检报告（保密/安全/内存/存储/稳定/牛客）
└── .github/workflows/
    ├── deploy-demo.yml            # push 后自动构建 demo/ 并部署到 GitHub Pages
    └── lint.yml                   # 语法 + 自包含 + 合并版标记 + 转义守卫 + 一致性 + 浏览器冒烟
```

## 改代码后必做

`pages/*.html` 和 `demo/index.html` **都是生成出来的**，手改它们下次生成就被覆盖。三步顺序不能乱：

```bash
python pages/build_pages.py    # ① 4 个独立模块页 -> pages/00~03
python pages/build_single.py   # ② 合并成单文件应用 -> pages/00-总览台.html（覆盖 ① 的 00）
python pages/build_demo.py     # ③ 套 mock -> demo/index.html
```

`build_single.py` 要读 `build_pages.py` 的产物，`build_demo.py` 要读 `build_single.py` 的产物，漏一步 demo 就还是旧的。
（`build_pages.py` / `build_single.py` 还会在仓库根目录顺手存一份，那是本地产物，已被 `.gitignore` 忽略。）

CI（`.github/workflows/lint.yml`）会重新跑这三步并检查 `git diff`，忘记生成/忘记提交会被判红。

## 一键预检（改完必跑）

```bash
python pages/preflight.py
```

单条命令串完 15 项检查，全绿才算改完：

| # | 检查 | 作用 |
|---|------|------|
| 1-3 | `build_pages` → `build_single` → `build_demo` | 重新生成三件产物，确保产物与源码同步 |
| 4 | `check_escapes.py` | **P0 守卫**：源码里会被 Python 解释的反斜杠转义、产物里的裸控制字符（曾导致整页白屏） |
| 5 | `check_workflows.py` | 校验 `.github/workflows/*.yml` 语法 |
| 6 | `check_inline_js.py` | 内联 JS 语法（`new Function` 编译） |
| 7-10 | `lint_schema.py` × 4 页 | 字段名 / 选项与 `canonical_schema.json` 一致 |
| 11-14 | `lint_database_sdk_usage.py` × 4 页 | DSDK001-013：SDK 调用契约（分页游标、返回结构、字段映射等） |
| 15 | `smoke_browser.js` | Playwright 真浏览器冒烟：mock 三表跑初始化 / 四视图 / 筛选 / 热力图 / 情报面板 / 外部变更订阅 |

单独跑某一项也可以，例如：

```bash
python pages/check_escapes.py     # 只跑转义守卫（不需要 token）
python pages/check_inline_js.py   # 只跑内联 JS 语法
python pages/check_dups.py        # 扫秋招表重复公司名（token 走 stdin）
python pages/audit_data.py        # 三表体检：记录数/体积/字段覆盖（token 走 stdin）
```

> `check_dups.py` / `audit_data.py` 需要资料库 token，用 `echo "<token>" | python …` 或管道传入；token 有效期 30 分钟。

> 关于 `check_escapes.py`：`build_pages.py` 里的 JS 是大段**普通三引号字符串**，`\u0000` 这类转义会被 Python 先吃成真实控制字符写进 HTML。历史上就是它把 `openLink` 的正则弄成 `Range out of order` 导致整页白屏（`node --check` 查不出）。**新的 JS 里写正则/转义前，先跑一遍这个脚本。**

## 本地预览

```bash
# 任何静态服务器都行
cd demo
python -m http.server 8080

# 然后打开
open http://localhost:8080
```

demo 顶部有黄色横幅提示「演示模式」，数据存在浏览器 localStorage，可以点「清空演示数据」恢复初始示例。

## 部署到腾讯文档·资料库

参见 `docs/DEPLOY.md`。简要步骤：

1. 创建 3 张数据表（字段见上文），把字段/选项写进 `canonical_schema.json`
2. 确认 `pages/build_pages.py` 里的 `JOBS_ID / APPS_ID / INTERN_ID` 是你的实际节点 ID
3. 跑上面三步生成产物
4. 用 `python pages/deploy_pages.py` 把页面推到资料库节点（或手动走「导入 HTML」）

## License

MIT

## 致谢

- 牛客网校招日程（匿名接口可用）
- 腾讯文档·资料库（个人云端数据表能力）
