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
│   ├── DEPLOY.md                  # · 部署到腾讯文档·资料库的步骤
│   └── screenshot.png             # · 占位（待补）
│
└── .github/workflows/
    ├── deploy-demo.yml            # · push 后自动部署 demo/ 到 GitHub Pages
    └── lint.yml                   # · 自动跑 schema + sdk lint
```

---

## 3. 三个数据表（schema 锁死，不要随便改字段名）

### 表 A：秋招岗位清单
- **表 ID（资料库）**：`GgZ71tywhs4HEZytFSqXTP`
- **字段**（按顺序）：
  | 字段名 | 类型 | 说明 |
  |--------|------|------|
  | 公司 | 文本 | 公司全称 |
  | 批次 | 文本 | "2027 届秋招" / "2027 届提前批" |
  | 岗位方向 | 文本 | 算法 / 后端 / 数据 / 产品 等 |
  | 工作地点 | 文本 | "北京 / 上海 / 成都" 多地可 |
  | 优先级 | 文本 | P0 / P1 / P2 |
  | 投递状态 | 文本 | 待投递 / 已投递 / 已笔试 / 已面试 / 已 Offer / 已拒绝 |
  | 网申起止日期 | 文本 | "2026-09-01 ~ 2026-12-31" |
  | 投递链接 | 文本 | **数组** `[{text,link}]`，**不是对象**！ |
  | 来源 | 文本 | "牛客" / "应届生" / "官网" |
  | 备注 | 文本 | 自由 |

### 表 B：简历投递跟踪
- **表 ID**：`oBGkMFTv9Xv4Xn5gFOK18S`
- **字段**：
  | 字段名 | 类型 | 说明 |
  |--------|------|------|
  | 公司 | 文本 | 主索引（按公司去重） |
  | 岗位 | 文本 | |
  | 当前阶段 | 文本 | 投递 / 笔试 / 一面 / 二面 / 三面 / HR / Offer / 拒 |
  | 投递日期 | 文本 | YYYY-MM-DD |
  | 下次节点 | 文本 | YYYY-MM-DD |
  | 节点说明 | 文本 | 例：周三 14:00 一面 |
  | 复盘笔记 | 文本 | 自由 |
  | 相关链接 | 文本 | 数组 `[{text,link}]` |

### 表 C：成都实习岗位
- **表 ID**：`tgH8096uENTaIj8RSY9qm5`
- **字段**：
  | 字段名 | 类型 | 说明 |
  |--------|------|------|
  | 公司 | 文本 | |
  | 岗位名称 | 文本 | |
  | 薪资 | 文本 | 例：200-300/天 |
  | 工作地点 | 文本 | 默认"成都" |
  | 岗位要求 | 文本 | 自由 |
  | 投递状态 | 文本 | |
  | 投递链接 | 文本 | 数组 `[{text,link}]` |
  | 来源 | 文本 | "BOSS" / "牛客" |
  | 备注 | 文本 | |

> **如果一定要改字段**，必须同时改：① 三张表实际字段 ② `pages/build_pages.py` 中的 schema_union ③ 跑 `python pages/build_pages.py` 重新生成 ④ 跑 lint 通过

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
- [x] GitHub Pages demo（`demo/` 用 localStorage mock，可独立部署）

---

## 7. 待办（按优先级排序）

1. **GitHub push**（主人手动，需要 SSH/token）
2. **资料库清理**：4 个旧占位版页面（无 ID 记录）需主人在腾讯文档 UI 手动删（无 delete API）
3. **简历投递追踪统计图表**：投递/各阶段分布（饼图）
4. **BOSS 直聘 cookie 自动化**（需要主人提供 cookie，**反爬风险**）
5. **响应式优化**：iPad 横向 / iPhone SE 小屏
6. **导出为 PDF 简历投递报告**（周报用）

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