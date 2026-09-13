# HANDOVER.md —— 给接手这个项目的 AI

> 如果你是一个新 AI 第一次读到这个仓库，先读这一份，再读 `README.md`，然后再开始动代码。
> 这份文档不是给你看项目漂亮的地方，而是**让你知道哪里会咬人**。

---

## 0. 你现在的身份和上下文

- **项目主人**：窦畅，西南交大 2027 届本科生，求职 AI 大模型/算法实习方向
- **这是他的个人数字工作台**，不是商业项目
- **核心目标**：把"打开一个超长页面、翻好久才能找到不同模块"的问题拆掉
- **目标用户只有他一个人**，不要过度设计"通用化"

## 1. 项目一句话

> 一个为 2027 届秋招求职定制的个人工作台：**单文件 HTML 应用（页内 Tab 切 4 个模块）+ 3 张数据表 + GitHub Pages demo**，已部署到腾讯文档·资料库。

**当前是单文件架构**：`pages/00-总览台.html` 由 `build_single.py` 把 4 个模块合并成一个文件，页内 Tab 切换（不跳转、数据只加载一次）。
`pages/01~03` 是最初的独立版，保留但不再是主线。

---

## 2. 文件结构（不要乱动）

```
github_repo/
├── README.md                      # 项目对外说明（GitHub 主页用）
├── PUSH_TO_GITHUB.md              # 发布流程 + CI 说明（已推送成功，看这份）
├── HANDOVER.md                    # ← 你正在读这个
├── LICENSE                        # MIT
├── .gitignore
├── canonical_schema.json          # 【构建输入】字段名 + 选项，build_pages.py 要读，别删
├── schema_union.json              # 【构建输入】三张表的 schema 快照
│
├── pages/                         # 【生产版 + 全部构建脚本】
│   ├── 00-总览台.html             # · build_single.py 产出的合并版单文件应用
│   ├── 01-秋招岗位台.html         # · 独立版：非央国企岗位看板
│   ├── 02-央国企台.html           # · 独立版：央国企专栏
│   ├── 03-成都实习台.html         # · 独立版：成都实习专区
│   ├── build_pages.py             # · ① 生成 4 个独立模块页
│   ├── build_single.py            # · ② 合并成单文件应用（覆盖上面的 00）
│   ├── build_demo.py              # · ③ 加 demo 适配层（SDK 缺失 → localStorage mock）
│   ├── sync_interns.py            # · 牛客校招日程 → 实习表 同步脚本
│   └── deploy_pages.py            # · 推到腾讯文档·资料库节点
│
├── demo/                          # 【静态 demo】GitHub Pages 用
│   └── index.html                 # · 合并版应用 + mock 数据（只有这一个文件）
│
├── docs/
│   └── DEPLOY.md                  # · 部署到腾讯文档·资料库的步骤
│
└── .github/workflows/
    ├── deploy-demo.yml            # · push 后自动部署 demo/ 到 GitHub Pages
    └── lint.yml                   # · 语法 + 自包含 + 合并版标记 + 产物一致性
```

> **生成顺序不能乱**：`build_single.py` 读 `build_pages.py` 的产物，`build_demo.py` 读 `build_single.py` 的产物。
> 三步都跑完再提交，否则 CI 的「产物一致性」检查会红（见坑 11）。

---

## 3. 三个数据表（schema 锁死，不要随便改字段名）

> ⚠️ 下面这份是 **2026-09 校订过的真实 schema**（旧版文档把字段名/选项写错了，已修正）。
> 权威来源：仓库根目录的 `canonical_schema.json`（`build_pages.py` 直接读它，**已入库**）+ `schema_union.json`。

### 表 A：秋招岗位清单
- **表 ID（资料库）**：`GgZ71tywhs4HEZytFSqXTP`
- **字段**：
  | 字段名 | 类型 | 选项 / 说明 |
  |--------|------|------|
  | 公司 | text | 公司全称（`isSOE()` 靠这个字段做央国企识别） |
  | 批次 | select | `27秋招` / `27暑期实习` / `27日常实习` / `其他` |
  | 岗位方向 | text | 算法 / 后端 / 数据 等，可写多个用`、`分隔 |
  | 工作地点 | text | "北京、上海" 多地可 |
  | 优先级 | select | `P0` / `P1` / `P2` |
  | 投递状态 | select | `待投递` / `已投递` / `不投了` |
  | 网申开始 | date | |
  | 截止日期 | date | 「今天要处理」和「7 天内截止」全靠它 |
  | 投递链接 | url | 数组 `[{text,link}]`（见坑 1） |
  | 来源 | text | "牛客校招日程" / "手动添加" 等 |
  | 备注 | text | 自由 |

### 表 B：简历投递跟踪
- **表 ID**：`oBGkMFTv9Xv4Xn5gFOK18S`
- **字段**：
  | 字段名 | 类型 | 选项 / 说明 |
  |--------|------|------|
  | 公司 | text | 主索引（`syncTracking()` 按公司去重） |
  | 岗位 | text | |
  | 当前阶段 | select | `已投递` / `笔试` / `一面` / `二面` / `HR面` / `Offer` / `感谢信` |
  | 投递日期 | date | |
  | 下次节点 | date | 「今天要处理」的蓝色项来自这里 |
  | 节点说明 | text | 例：周三 14:00 一面 |
  | 复盘笔记 | text | 自由 |
  | 相关链接 | url | 数组 `[{text,link}]` |

### 表 C：成都实习岗位
- **表 ID**：`tgH8096uENTaIj8RSY9qm5`
- **字段**：
  | 字段名 | 类型 | 选项 / 说明 |
  |--------|------|------|
  | 公司 | text | |
  | 岗位名称 | text | |
  | 薪资 | text | 例：200-300元/天 |
  | 工作地点 | text | 默认"成都" |
  | 岗位要求 | text | 自由 |
  | 投递状态 | select | 同表 A：`待投递` / `已投递` / `不投了` |
  | 投递链接 | url | 数组 `[{text,link}]` |
  | 来源 | text | "BOSS直聘（手动添加）" / "牛客校招日程" |
  | 备注 | text | |

> **如果一定要改字段**，必须同时改：① 三张表实际字段 ② `canonical_schema.json` ③ `pages/build_pages.py` 里读写的字段名 ④ 跑三步生成（`build_pages.py` → `build_single.py` → `build_demo.py`）⑤ 提交后让 lint 工作流跑过

---

## 4. 已部署到腾讯文档·资料库的 4 个页面节点

| 页面 | 节点 ID（资料库） | 备注 |
|------|-------------------|------|
| 总入口（旧页改的） | `KLHGJ6uGsY1f2JumTog0Qu` | 4 模块导航 |
| 总览台 | `szZlSjyPnnpGwDW4OD4y0X` | |
| 秋招岗位台 | `G9pPkUVWIc6Fk43Mnn1csc` | |
| 央国企台 | `PQ5cLpifIyB1CaQB2OIMrm` | |
| 成都实习台 | `JgXPaIiaDMGt2xH3vBftAo` | |

访问入口（主人的）：`https://www.workbuddy.cn/space/d/{节点ID}`

---

## 5. 关键技术决策（**踩过的坑，别再踩**）

### 坑 1：URL 字段是数组，不是对象

**错误理解**（你以为）：
```js
j["投递链接"][0].text === "官网"  // ❌ undefined
```

**实际**：
```js
// 返回值形如：
j["投递链接"] = [{ text: "校招官网", link: "https://..." }, { text: "牛客", link: "..." }]
```

✅ **正确处理**：见 `pages/build_pages.py` 中的 `urlVal(v)` 函数，**同时兼容**：
- 数组 `[{text,link}]`
- 对象 `{text, link}` 
- 纯字符串 `"https://..."`

永远不要假设字段格式，先 `Array.isArray` 再 `.map`。

### 坑 2：记录主键是 `record_id`，**不是 `_id`**

文档写的是 `_id`，但 SDK 实际返回 `record_id`。

✅ 用 `r.record_id || r._id` 兼容（见 `recId(r)` 函数）。

### 坑 3：iframe 沙箱拦截 `window.open`

页面运行在腾讯文档的 iframe 里，`target="_blank"` 和 `window.open(url)` 都会被拦截为静默失败。

✅ **必须**用 `openLink(url)` 函数：
```js
function openLink(url) {
  try {
    const w = window.open(url, '_blank');
    if (w) return;
    // 兜底弹层：显示链接 + 一键复制按钮
    showLinkModal(url);
  } catch(e) {
    showLinkModal(url);
  }
}
```

### 坑 4：lint 强制 databaseId 字面量

资料库有个 lint：`databaseId:JOBS_ID` 这种变量形式会被拒（DSDK012 错误）。

✅ **不要**写：
```js
const JOBS_ID = 'GgZ71tywhs4HEZytFSqXTP';
db.query({ databaseId: JOBS_ID, ... })  // ❌
```

✅ **要**写：
```js
db.query({ databaseId: 'GgZ71tywhs4HEZytFSqXTP', ... })  // ✅
```

所有 `databaseId` 必须是字符串字面量。

### 坑 5：BOSS 直聘有反爬，无法自动抓取

不要尝试用 Playwright/Selenium 抓 BOSS 直聘，会被 ban。

✅ 当前方案：**用户手动复制链接 → 一键收录** + 牛客 daily sync 兜底。

### 坑 6：腾讯文档·智能表不是资料库

主人最初提到的是「腾讯文档·智能表」，但那是只读 + 限制多。
**资料库（workbuddy.cn/space）的 SDK 是另一套**，见 `db.query` / `db.addRecord` 等。

不要混用。

### 坑 7：demo 的 mock db 会把三张表串成一张（**修过两次，注意别再回退**）

`pages/build_demo.py` 里旧版 `fakeDb()` 用 `forEach` 循环给**同一个 `db` 对象**反复赋值 `db.query=...`，
闭包只留住最后一次循环的 `name`，结果 **jobs / apps / interns 三张表全都返回 interns 的数据**
（线上表现：岗位列表空、实习列表重复三遍）。

✅ 现在改成按 `opts.databaseId` 分派：`map` + `nameOf(opts)`，
`query / addRecord / updateRecord / deleteRecord / getSchema` 全部走 `nameOf(opts)`；
`getSchema` 直接返回真实的 select 字段（不再只靠 `__DEMO_OPTS__` 注入兜底）。

⚠️ **这个坑修过两次**：第一次修了仓库里的 `pages/build_demo.py`，后来工作区的旧版脚本又被拷回仓库，bug 复活。
改 mock 时**工作区和仓库两边都要改**。

### 坑 8：日期字段的形态不止一种

`dOnly()` 只认 `'YYYY-MM-DD'` 字符串时，遇到 `{date:'YYYY-MM-DD'}` 会截出 `{"date":"2` 这种垃圾。

✅ 现在 `dOnly()` 同时兼容：字符串 / `{date:...}` / `{text:...}` / `Date`。
demo 的种子数据就是 `{date:...}`，所以这个坑不修 demo 里所有日期都是错的。

同一个坑还有第二张脸：**文本字段也是对象**。资料库的文本 / 单选 / 来源字段返回 `{text:'字节跳动'}`，
直接 `String(v)` 拼进 innerHTML 或 textContent 就会渲染成 `[object Object]`（线上 demo 就出现过：
投递记录卡片的公司、岗位、阶段全变成 `[object Object]`）。

✅ 共享 JS 里新增 `plain(v)`：兼容 字符串 / `{text|value|name|date|link}` / 数组取首项。
`setFieldText()`、今日待办标题、搜索关键词拼接、删除确认框文案都已改走 `plain()`。
以后新增渲染逻辑，字段值一律先过 `plain(...)`，不要再直接拼接。

### 坑 9：demo 页面不能保留生产环境的导航链接

demo 是纯静态站，如果页面里还有指向 `https://www.workbuddy.cn/space/d/...` 的链接，
访客点一下就跳到主人的私有资料库（而且大概率没权限，看到 404）。

✅ 合并成单文件之后，模块切换用的是**页内 Tab**（`data-view` + 事件委托），页面里一个生产链接都没有。
`build_demo.py` 还会把真实的 `databaseId` 替换成 `JOBS_ID_FAKE` 等假 ID。
CI 里有 `grep workbuddy.cn/space/d/ demo/*.html` 的回归校验，改回跨节点跳转会被抓出来。

### 坑 10：GitHub Pages 不要把整个仓库当站点根

旧版 `deploy-demo.yml` 直接 `upload-pages-artifact` 传 `.`，会把 `.github/`、`pages/`、`docs/` 全部发到公网。

✅ 现在先 `cp demo/*.html _site/` 再传 `_site`，站点根就是 demo 本身。
仓库名是 `-`，所以演示地址是 <https://dorchain-chang.github.io/-/>（没有 `/demo/` 后缀）。

### 坑 11：仓库的 `pages/` 曾和工作区脚本分叉，导致 CI 必红

合并成单文件应用那几轮提交**只更新了 `demo/`**，没同步脚本，于是出现三处不一致：

| 症状 | 后果 |
|------|------|
| 仓库 `pages/build_demo.py` 是旧版（只支持 4 个页） | 跑它会生成 3 个多余文件 + 覆盖掉 `demo/index.html` |
| 仓库里没有 `build_single.py` | 仓库**无法自我复现** `demo/index.html` |
| 仓库里没有 `canonical_schema.json` | `build_pages.py` 静默降级成空 schema，CI 生成的页面和提交的**必然不一致** |

✅ 现在 5 个脚本（`build_pages` / `build_single` / `build_demo` / `sync_interns` / `deploy_pages`）
和两个输入文件（`canonical_schema.json` / `schema_union.json`）都在仓库里，
跑完整三连后 `git diff` 为空，CI 绿。

### 坑 12：不要手改生成产物

`pages/*.html` 和 `demo/index.html` 都是脚本生成的。

- 手改 → 下次生成被覆盖，白改
- 只提交产物不提交脚本改动 → CI 的「产物一致性」检查判红
- 想改页面行为，去改 `pages/build_pages.py`（模块内容）或 `pages/build_single.py`（合并/页内 Tab 骨架）

改完必须跑：`build_pages.py` → `build_single.py` → `build_demo.py`，再一起提交。

### 坑 13：不要把多行脚本写进 workflow 的 `run: |` 块标量

`.github/workflows/lint.yml` 里曾经直接塞了一段内联 python：

```yaml
        run: |
          python3 -c '
import re,sys          # ← 顶格，YAML 认为块标量在这里结束了
          '
```

顶格的行会被 YAML 当成块外内容 → **整个 workflow 解析失败**。GitHub 的表现极其隐晦：
运行记录里 workflow 名字直接显示成 `.github/workflows/lint.yml`，`conclusion=failure`，
`jobs` 数量为 0，耗时不到 1 秒，**连日志都没有**。

✅ 现在多行脚本一律放 `pages/*.py`（如 `pages/check_inline_js.py`），workflow 只写一行调用；
并且加了 `pages/check_workflows.py` 在 CI 最前面做 YAML 解析自检，同类问题不会再悄悄溜进去。

### 坑 14：仓库没启用 Pages 时 `configure-pages` 会直接失败

首次部署报错：`Get Pages site failed ... HttpError: Not Found`（`GET /repos/{owner}/{repo}/pages` 404）。
原因是仓库设置里还没启用 Pages，而不是 workflow 写错。

✅ `deploy-demo.yml` 的 Setup Pages 步骤已加 `enablement: true`，让 action 自动把 Pages 打开
（`build_type=workflow`，配合 `permissions: pages: write`）。若仍失败，去
Settings → Pages → Source 手动选「GitHub Actions」。

---

## 6. 已完成的功能

- [x] 单文件应用（`build_single.py` 把 4 个模块合并成一个文件，页内 Tab 切换零跳转）
- [x] 今天要处理（自动汇总逾期/3 天内截止/今天的面试）
- [x] AI/计算机相关筛选 + 北京/成都/天津筛选（见 `mineMatch(j)`）
- [x] 央国企识别（70+ 关键词，见 `isSOE(j)`）
- [x] 直达 vs 搜索按钮区分（绿色实色 vs 灰色虚线）
- [x] 投一个存一个（点"标已投"自动在投递跟踪表建档，按公司去重）
- [x] 牛客 daily sync（每天 9:00 + 9:30 自动抓取，见 `automation_update`）
- [x] BOSS 直聘手动收录
- [x] GitHub repo 准备（README / LICENSE / CI / .gitignore / HANDOVER）
- [x] **已 push 到 <https://github.com/Dorchain-chang/->，Pages 演示已上线 <https://dorchain-chang.github.io/-/>**
- [x] GitHub Pages demo（`demo/` 用 localStorage mock，可独立部署）
- [x] Pages 部署改为构建 `_site` 后上传（不再把整个仓库发到公网）
- [x] mock 三表串数据 bug 修复（`query/addRecord/updateRecord/deleteRecord/getSchema` 全部按 `databaseId` 分派，见坑 7）
- [x] `dOnly()` 兼容对象与 `Date` 形态日期（见坑 8；这次修在 `build_pages.py` 的共享 JS 里，4 个页面 + demo 一起生效）
- [x] 演示横幅改为普通文档流（原来 `position:fixed` 会盖住 sticky 导航）
- [x] demo 种子数据改为相对今天的日期，随时打开都有逾期/临期/正常三类样本
- [x] 补齐仓库缺失的 `build_single.py` / `sync_interns.py` / `deploy_pages.py` / `canonical_schema.json` / `schema_union.json`
- [x] CI 全绿：workflow YAML 自检（坑 13）+ 内联 JS 语法 / demo 自包含 / 合并版标记 / 产物一致性 / 页面数
- [x] GitHub Pages 已在仓库里启用（`build_type=workflow`），<https://dorchain-chang.github.io/-/> 部署成功
- [x] 字段值对象拍平成 `plain()`，修掉页面上的 `[object Object]`（见坑 8）
- [x] HANDOVER / README / PUSH_TO_GITHUB 与实际架构、真实仓库地址对齐

---

## 7. 待办（按优先级排序）

1. **`deploy_pages.py` 的节点映射要和单文件架构对齐**：现在 4 个节点各推各自的 `0X-*.html`，
   只有总览台节点拿到合并版；如果想让 4 个节点都是合并版（页内 Tab 到处能切），把 `PAGES` 指向同一个文件
2. **资料库清理**：4 个旧占位版页面（无 ID 记录）需主人在腾讯文档 UI 手动删（无 delete API）
3. **简历投递追踪统计图表**：现在只有漏斗图，可以再加阶段分布饼图
4. **BOSS 直聘 cookie 自动化**（需要主人提供 cookie，**反爬风险**）
5. **响应式优化**：iPad 横向 / iPhone SE 小屏（目前只有 `max-width:768px` 一档）
6. **导出为 PDF 简历投递报告**（周报用）

> 改完页面记得跑三步生成：`build_pages.py` → `build_single.py` → `build_demo.py`，
> 再 `git add -A && git commit && git push`。
> 直接手改 `pages/*.html` 或 `demo/index.html` 会被下次生成覆盖，而且 CI 的产物一致性检查会判红（见坑 12）。

---

## 8. 给你的开局 prompt 模板

如果你是新 AI 第一次和主人对话，**直接复用下面这段**：

```text
我是窦畅（西南交大 2027 届 / AI 大模型求职方向）的助手。我有一个单文件个人工作台「秋招求职台」，
页内 Tab 切 4 个模块，已在腾讯文档·资料库部署，GitHub 仓库和 Pages demo 都已上线。

请你先：
1. 读 HANDOVER.md（项目背景 + 14 个坑 + schema + 待办）
2. 读 README.md（对外说明 + 数据表 + 技术栈）
3. 用 `ls github_repo/pages` 和 `ls github_repo/demo` 看一下当前结构
4. 然后告诉我：你现在理解了什么、有没有疑问、你想先做哪一项

注意：
- 这是单人项目，不要"过度工程化" / 不要加没必要的抽象
- 资料库 SDK 的 `databaseId` 必须是字符串字面量（不能传变量，会被 lint 拒）
- iframe 沙箱里 `window.open` 会被拦截，必须用 openLink() + 兜底弹层
- URL 字段是数组 `[{text,link}]` 不是对象，先 Array.isArray
- 不要尝试爬 BOSS 直聘，会被 ban

最后告诉我：你需要我先决定什么 / 提供什么，我们才能继续。
```

---

## 9. 紧急联系方式

如果遇到主人已经做过但你不知道的事，先 **读 README + HANDOVER**，**再问主人**。
不要随便改 schema、不要随便删文件、不要随便 push。

主人最讨厌的：
1. 编造数字
2. 抢功（在面试材料里）
3. 没说就动资料库/远程仓库