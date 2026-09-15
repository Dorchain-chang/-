# 秋招求职台 (Qiuzhao Workbench)

> 一个为 2027 届校招求职定制的个人数字工作台：**把"看岗位"和"管投递"装进同一个页面。**
>
> 最后更新：2026-09-14

## 为什么做这个

灵感来自牛客网的校招日历——它是少数**不用登录就能看**全行业校招日程的地方，公司、批次、网申起止一目了然。但它有个致命的短板：**只能看，不能记**。

- 没法标记「这个我投过了」「这个 P0 优先，先投它」
- 没法记录自己的进度：笔试在哪天、一面过了没有、Offer 到手没有
- 岗位信息、网申链接、面经情报分散在牛客/官网/邮箱各处，每次都要重新找

对招聘方来说日历是展示工具，对求职者来说**投递记录和进度才是主数据**。于是有了这个工作台：以牛客校招日历做数据源（免登录 API + 每日自动同步），再补上它缺掉的另一半——**投递跟踪、阶段推进、节点提醒、公司情报直达**，全部集成进一个自己的页面。

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

## 架构与原理

整套系统是五层结构：**数据源 → 处理自动化 → 云端数据表 → 单文件应用 → 构建部署流水线**。

![整体架构](docs/img/architecture.svg)

设计上的三个关键决策：

1. **零外部依赖的单文件**：没有 `<script src>`、没有字体/图标 CDN——页面运行在资料库的 iframe 沙箱里，任何外部资源都是潜在的单点故障和隐私出口。JS 堆实测 10MB，首屏 222ms。
2. **解析只产生建议，永不直改状态**：邮件/短信解析出的"笔试/面试/Offer"先进**情报收件箱**，人工点确认才写投递跟踪表——识别错最多浪费一次点击，不会静默把 Offer 改成感谢信（自动校验 → 人工确认 → 落库的三级审核思路）。
3. **取信/解析/存储三层解耦**：换邮箱只动"取信层"（转发规则或 IMAP 桥），解析器和数据层零改动——这也是邮件管线能平滑接入任意邮箱的原因：

![邮件接入管线](docs/img/mail-pipeline.svg)

> 邮箱接入的两种方式（关键词自动转发 / 本地 IMAP 桥）与逐步配置教程见 [`docs/MAIL-SETUP.md`](docs/MAIL-SETUP.md)。

## 核心功能

- **「今天要处理」自动汇总**：逾期岗位（红）/ 3 天内截止（橙）/ 今天的面试节点（蓝），不切换 Tab 就能看到今天该做什么
- **分类清晰**：秋招/实习 一键 chip 切换；央国企/其他企业 自动分流到「央国企」和「秋招岗位」两个 Tab
- **直达 vs 搜索**：有网申链接 → 绿色按钮直达；没链接 → 灰色虚线按钮（自动跳牛客/必应搜索）
- **投一个存一个**：岗位看板点「标已投」会自动在投递跟踪表建一条记录（按公司去重）
- **每日自动同步**：每天 9:00 自动抓牛客校招日程（含 AI/算法/数据 等方向）的有效期内岗位，补齐到岗位清单表
- **公司情报 · 牛客直达**：任意一条岗位（含表外公司）都能一键查情报；有 `牛客ID` 时首出该公司的**主页 / 面经 / 真题 / 薪资 / 讨论** 5 条精准深链，没有则降级为全网检索
- **BOSS 反爬实测**：BOSS 直聘有反爬，无法自动抓取 → 改为「BOSS 上手动复制链接 + 一键收录」+ 牛客 daily sync 兜底
- **AI 能力（BYOK）**：简历解析 / 投递画像 / 简历↔JD 匹配打分（含批量）/ 今日 AI 推荐 / 面试复盘 / 邮件 AI 解析，全部按需触发、结果存本机、未配 Key 走 Mock 演示（详见 [AI 能力](#ai-能力已实现--用户自带-key)）

## 数据结构

工作台背后是 4 张数据表（都在腾讯文档·资料库里）：

| 表名 | 字段（类型） | 表 ID |
|------|------|-------|
| 秋招岗位清单 | 公司(text) / 批次(select: 27秋招·27暑期实习·27日常实习·其他) / 岗位方向(text) / 工作地点(text) / 优先级(select: P0·P1·P2) / 投递状态(select: 待投递·已投递·不投了) / 网申开始(date) / 截止日期(date) / 投递链接(url) / 来源(text) / 备注(text) / **牛客ID(text)** | `GgZ71tywhs4HEZytFSqXTP` |
| 简历投递跟踪 | 公司(text) / 岗位(text) / 当前阶段(select: 已投递·笔试·一面·二面·HR面·Offer·感谢信·已终止) / 投递日期(date) / 下次节点(date) / 节点说明(text) / 复盘笔记(text) / 相关链接(url) | `oBGkMFTv9Xv4Xn5gFOK18S` |
| 成都实习岗位 | 公司(text) / 岗位名称(text) / 薪资(text) / 工作地点(text) / 岗位要求(text) / 投递状态(select) / 投递链接(url) / 来源(text) / 备注(text) / 网申开始(date) / 截止日期(date) / **牛客ID(text)** | `tgH8096uENTaIj8RSY9qm5` |
| 求职情报收件箱 | 公司(text) / 类型(select: 笔试·面试·Offer·感谢信·其他) / 事项时间(date) / 原文摘要(text) / 发件人(text) / 来源(select: 邮件·短信·浏览器扩展) / 状态(select: 待确认·已确认·已忽略) / 置信度(select: 高·中·低) / 消息ID(text) / 收件时间(date) | `EdCHnKtjZIXEw37tUmvhqL` |

> **`牛客ID`** 存牛客企业 `companyId`，有它时「公司情报」按钮会首出 5 条精准直达深链（`enterprise/{id}` 主页 / `interview` 面经 / `question/company` 真题 / `salary` 薪资 / `discussion` 讨论），比按公司名搜索准得多。同步脚本会自动回填；历史数据用 `python pages/backfill_nowcoder.py` 一次性补齐。

## 技术栈

**前端（单文件应用）**
- 单文件 HTML + 内联 CSS + 内联 JS，**零外部依赖**（无 CDN / 字体 / 图标库，图标全部内联 SVG）
- 自适应 PC / 移动端：窄屏单列，按钮 ≥ 32px（移动端 ≥ 44px）
- 资料库 SDK 数据读写：`db.query / addRecord / updateRecord / deleteRecord` + `onUpdated` 实时订阅（去抖 + 回声抑制）
- 沙箱内 `window.open` 被拦截的兜底：弹层 + 一键复制链接

**数据与自动化（Python + WorkBuddy automation）**
- 牛客免登录 API（`school-schedule/list-card`）每日同步：校招日程 → 秋招/实习表，`companyId` 回填支撑企业档案深链
- 邮件管线：关键词自动转发（方式A）/ 纯标准库 IMAP 直读桥（方式B，`imaplib/email/urllib` 零依赖）
- WorkBuddy automation 定时任务驱动同步与解析，云端 4 表存储

**质量工程（保证敢改代码）**
- `preflight.py` 一键预检：构建 3 步 + 转义守卫 + schema/SDK lint（DSDK001-013）+ Playwright 真浏览器冒烟，共 15 项
- GitHub Actions CI：语法 / 自包含 / 合并版标记 / 产物一致性 / 浏览器冒烟
- 性能实测留痕：`perf_probe.js`（首屏 222ms / 重渲染 12.9ms / JS 堆 10MB）+ `ab_cache.js`（缓存 A/B）

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
│   ├── mail_bridge.py             #   · 邮件取信桥（IMAP 直读 → 收件箱表；--llm 可选 LLM 结构化）
│   ├── mail_config.example.json   #   · 邮箱配置模板（含可选 llm 段；真配置已进 .gitignore）
│   └── deploy_pages.py            #   · 推到腾讯文档·资料库节点（4 节点同推单文件）
├── demo/                          # GitHub Pages 站点，零依赖
│   └── index.html                 #   · 合并版应用 + mock 数据
├── docs/
│   ├── DEPLOY.md                  # 部署到腾讯文档·资料库的步骤
│   ├── AUDIT-2026-09-14.md        # 上线前终检报告（保密/安全/内存/存储/稳定/牛客）
│   ├── MAIL-SETUP.md              # 校招通知邮箱接入指南（转发收口 / IMAP 直读桥 + 面试话术）
│   └── AI-FEATURES.md             # AI 能力说明（BYOK / 按需触发 / 成本控制 / 抓 JD 书签 / 安全模型）
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

## AI 能力（已实现 · 用户自带 Key）

> 两条原则：**BYOK**（用户填自己的 API Key，存本机 `localStorage`，不上传服务器、不进资料库表）+ **按需触发**（无常驻后台、无定时任务，只有点按钮那一刻才调模型）。
>
> 完整说明、成本估算、配置步骤与安全模型见 **[`docs/AI-FEATURES.md`](docs/AI-FEATURES.md)**。

**七个能力**（全部已上线，未配 Key 时走 Mock 演示模式，页面永不白屏）

| 能力 | 入口 | 单次成本 |
|---|---|---|
| 简历档案解析（多份，每份自带求职意向） | 个人中心 → 简历档案 → AI 解析 | 2–4k |
| 投递画像（简历 + 投递数据 → 节奏/瓶颈/建议） | 个人中心 → 投递画像 | 2–3k |
| 单岗位匹配打分（简历 ↔ JD，分数+亮点+缺口+建议） | 岗位卡片 → 贴 JD 打分 | 1–2k |
| 批量匹配打分（当前列表，**一次上限 8 条，可中断**） | 岗位页筛选区 → 批量打分 | ≈2k×条数 |
| 今日 AI 推荐（本地排序 0 成本，**按需** AI 点评，当天缓存） | 今日提醒顶部 | ≈1k |
| 面试复盘（面经 → 总评/答好/答砸/准备清单/预测题，写入复盘笔记） | 投递跟踪卡片 → AI 复盘 | 2–3k |
| 邮件 AI 解析（环节/时间/形式/地点/准备/待办） | 收件箱卡片 → AI 解析 | ≈1k |

**JD 拿不到自动正文的解法**：牛客列表接口不含 JD，详情页前端渲染 + 反爬 → 采用**零安装书签**：在任意招聘页点一下书签，JD 自动进剪贴板，回岗位卡片粘贴即可打分（代码与添加步骤见 `docs/AI-FEATURES.md`）。

**成本控制**：批量上限 8 条 + 执行前告知预估消耗 + 随时中断；推荐默认本地规则排序（匹配分 50% + 截止紧迫度 30% + 意向吻合 20%）并当天缓存；要求稳定复现的任务温度锁 `0.2`。所有 AI 结果只存本机，唯一写云的是面试复盘落到「复盘笔记」字段与收件箱确认写入投递跟踪（均需人工确认）。

## License

MIT

## 致谢

- 牛客网校招日程（匿名接口可用）
- 腾讯文档·资料库（个人云端数据表能力）
