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

> 一个为 2027 届秋招求职定制的个人工作台，包含 **4 个独立 HTML 页面 + 3 张数据表 + GitHub Pages demo**，已部署到腾讯文档·资料库。

---

## 2. 文件结构（不要乱动）

```
github_repo/
├── README.md                      # 项目对外说明（GitHub 主页用）
├── PUSH_TO_GITHUB.md              # 主人手动推 GitHub 的步骤
├── HANDOVER.md                    # ← 你正在读这个
├── LICENSE                        # MIT
├── .gitignore
│
├── pages/                         # 【生产版】运行在资料库内
│   ├── 00-总览台.html             # · 统一管理 + 今天要处理 + 投递跟踪 + 4 模块入口
│   ├── 01-秋招岗位台.html         # · 非央国企岗位看板
│   ├── 02-央国企台.html           # · 央国企专栏（红色卡片）
│   ├── 03-成都实习台.html         # · 成都实习专区（BOSS 直聘 + 牛客 daily）
│   ├── build_pages.py             # · 单一来源生成 4 个页面的脚本
│   └── build_demo.py              # · 给生产版加 demo 适配层（SDK 缺失 → localStorage mock）
│
├── demo/                          # 【静态 demo】GitHub Pages 用
│   ├── index.html                 # · 同"00-总览台"但用 mock 数据
│   ├── autumn.html
│   ├── soe.html
│   └── intern.html
│
├── docs/
│   └── DEPLOY.md                  # · 部署到腾讯文档·资料库的步骤
│
└── .github/workflows/
    ├── deploy-demo.yml            # · push 后自动部署 demo/ 到 GitHub Pages
    └── lint.yml                   # · 自动跑 schema + sdk lint
```

---

## 3. 三个数据表（schema 锁死，不要随便改字段名）

> ⚠️ 下面这份是 **2026-09 校订过的真实 schema**（旧版文档把字段名/选项写错了，已修正）。
> 权威来源：`pages/build_pages.py` 里实际读写的字段名 + 仓库外的 `schema_union.json`。

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

> **如果一定要改字段**，必须同时改：① 三张表实际字段 ② `pages/build_pages.py` 里读写的字段名 ③ 跑 `python pages/build_pages.py && python pages/build_demo.py` 重新生成 ④ 提交后让 lint 工作流跑过（CI 里有"生成产物与脚本一致"的校验，忘了重新生成会红）

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

### 坑 7：demo 的 mock db 曾把三张表串成一张（已修）

`pages/build_demo.py` 里旧版 `fakeDb()` 用 `forEach` 循环给同一个 `db` 对象反复赋值 `db.query=...`，
闭包变量 `name` 最终停在最后一个值，结果 **jobs / apps / interns 三张表全都返回 interns 的数据**。

✅ 现在改成按 `opts.databaseId` 分派（`databaseId -> 表名` 映射），见 `fakeDb()` 的 `nameOf()`。
**以后给 mock 加方法，一定要接收 `opts` 并用 `nameOf(opts)` 取表名，不要直接用循环变量。**

### 坑 8：日期字段的形态不止一种

`dOnly()` 只认 `'YYYY-MM-DD'` 字符串时，遇到 `{date:'YYYY-MM-DD'}` 会截出 `{"date":"2` 这种垃圾。

✅ 现在 `dOnly()` 同时兼容：`'YYYY-MM-DD'` / `{date:...}` / `{text:...}` / `Date`。
demo 的种子数据就是 `{date:...}`，所以这个坑不修 demo 里所有日期都是错的。

### 坑 9：demo 页面不能保留生产环境的导航链接（已修）

demo 是纯静态站，如果 nav 还指向 `https://www.workbuddy.cn/space/d/...`，
访客点一下就跳到主人的私有资料库（而且大概率没权限，看到 404）。

✅ `pages/build_demo.py` 的 `DEMO_LINK_MAP` 会把 4 个生产节点 URL 改写成
`index.html / autumn.html / soe.html / intern.html`。CI 里也加了回归校验。

### 坑 10：GitHub Pages 不要把整个仓库当站点根

旧版 `deploy-demo.yml` 直接 `upload-pages-artifact` 传 `.`，会把 `.github/`、`pages/`、`docs/` 全部发到公网。

✅ 现在先 `cp demo/*.html _site/` 再传 `_site`，站点根就是 demo 本身，
访问地址是 `https://<user>.github.io/qiuzhao-workbench/`（不再有 `/demo/` 后缀）。

---

## 6. 已完成的功能

- [x] 4 个独立页面部署到资料库
- [x] 今天要处理（自动汇总逾期/3 天内截止/今天的面试）
- [x] AI/计算机相关筛选 + 北京/成都/天津筛选（见 `mineMatch(j)`）
- [x] 央国企识别（70+ 关键词，见 `isSOE(j)`）
- [x] 直达 vs 搜索按钮区分（绿色实色 vs 灰色虚线）
- [x] 投一个存一个（点"标已投"自动在投递跟踪表建档，按公司去重）
- [x] 牛客 daily sync（每天 9:00 + 9:30 自动抓取，见 `automation_update`）
- [x] BOSS 直聘手动收录
- [x] GitHub repo 准备（3 commit 待 push）
- [x] GitHub repo 准备（README / LICENSE / CI / .gitignore）
- [x] GitHub Pages demo（`demo/` 用 localStorage mock，可独立部署）
- [x] demo 三表串数据 bug 修复 + demo 导航改站内相对链接（`pages/build_demo.py`）
- [x] `dOnly()` 兼容 `{date:...}` 形态日期
- [x] Pages 部署改为构建 `_site` 后上传（不再把整个仓库发到公网）
- [x] CI 增加"demo 自包含"和"生成产物与脚本一致"两项回归校验
- [x] HANDOVER / README 里的 schema 与真实字段对齐

---

## 7. 待办（按优先级排序）

1. **GitHub push**（需要主人的 SSH key 或 Personal Access Token，AI 无法代劳凭证）
2. **资料库清理**：4 个旧占位版页面（无 ID 记录）需主人在腾讯文档 UI 手动删（无 delete API）
3. **简历投递追踪统计图表**：现在只有漏斗图，可以再加阶段分布饼图
4. **BOSS 直聘 cookie 自动化**（需要主人提供 cookie，**反爬风险**）
5. **响应式优化**：iPad 横向 / iPhone SE 小屏（目前只有 `max-width:768px` 一档）
6. **导出为 PDF 简历投递报告**（周报用）

> 改完页面记得：`python pages/build_pages.py && python pages/build_demo.py`，
> 再 `git add -A && git commit && git push`。只改 `pages/*.html` 不改生成脚本，下次拉代码会被覆盖。

---

## 8. 给你的开局 prompt 模板

如果你是新 AI 第一次和主人对话，**直接复用下面这段**：

```text
我是窦畅（西南交大 2027 届 / AI 大模型求职方向）的助手。我有一个多页面个人工作台「秋招求职台」，
已在腾讯文档·资料库部署，GitHub repo 准备就绪。

请你先：
1. 读 HANDOVER.md（项目背景 + 5 个坑）
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