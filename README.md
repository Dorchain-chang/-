# 秋招求职台 (Qiuzhao Workbench)

> 一个为 2027 届校招求职定制的个人数字工作台，解决"打开一个超长页面、翻好久才能翻到不同模块"的效率问题。

## 这是什么

这是为求职季（秋招/实习）量身打造的**多页面工作台**，核心目标是**不让用户在同一个长页面里上下滚动找东西**。

工作台使用 [腾讯文档·资料库](https://docs.qq.com) 的「在线 page」+「数据表」能力部署，数据云端同步、多设备共享。

**在线 demo（不需要登录，数据只存在你自己的浏览器里）**：<https://dou-chang.github.io/qiuzhao-workbench/>

## 4 个独立页面

按功能拆分为 4 个独立节点，避免滚动：

| 页面 | 用途 | 进入方式 |
|------|------|----------|
| **总览台** | 统一管理 / 今天要处理 / 投递跟踪 / 4 模块入口 | 一打开就能看到全局 |
| **秋招岗位** | 互联网/科技/制造业等非央国企岗位（按 城市/职业/批次 筛选） | 想看具体岗位就进这个 |
| **央国企** | 央企/银行/运营商/电网/烟草等，按公司名关键词自动识别+红色卡片 | 只看央国企进这个 |
| **成都实习** | 实习岗位专区，BOSS 直聘手动收录+牛客每日同步 | 实习和秋招分开管理 |

## 核心功能

- **「今天要处理」自动汇总**：逾期岗位（红）/ 3 天内截止（橙）/ 今天的面试节点（蓝），不打开任何子页就能看到今天该做什么
- **分类清晰**：秋招/实习 一键 chip 切换；央国企/其他企业 自动分流到两个独立页面
- **直达 vs 搜索**：有网申链接 → 绿色按钮直达；没链接 → 灰色虚线按钮（自动跳牛客/必应搜索）
- **投一个存一个**：岗位看板点「标已投」会自动在投递跟踪表建一条记录（按公司去重）
- **每日自动同步**：每天 9:00 自动抓牛客校招日程（含 AI/算法/数据 等方向）的有效期内岗位，补齐到岗位清单表
- **B 站反爬实测**：BOSS 直聘有反爬，无法自动抓取 → 改为「BOSS 上手动复制链接 + 一键收录」+ 牛客 daily sync 兜底

## 数据结构

工作台背后是 3 张数据表（都在腾讯文档·资料库里）：

| 表名 | 字段（类型） | 表 ID |
|------|------|-------|
| 秋招岗位清单 | 公司(text) / 批次(select: 27秋招·27暑期实习·27日常实习·其他) / 岗位方向(text) / 工作地点(text) / 优先级(select: P0·P1·P2) / 投递状态(select: 待投递·已投递·不投了) / 网申开始(date) / 截止日期(date) / 投递链接(url) / 来源(text) / 备注(text) | `GgZ71tywhs4HEZytFSqXTP` |
| 简历投递跟踪 | 公司(text) / 岗位(text) / 当前阶段(select: 已投递·笔试·一面·二面·HR面·Offer·感谢信) / 投递日期(date) / 下次节点(date) / 节点说明(text) / 复盘笔记(text) / 相关链接(url) | `oBGkMFTv9Xv4Xn5gFOK18S` |
| 成都实习岗位 | 公司(text) / 岗位名称(text) / 薪资(text) / 工作地点(text) / 岗位要求(text) / 投递状态(select) / 投递链接(url) / 来源(text) / 备注(text) | `tgH8096uENTaIj8RSY9qm5` |

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
├── pages/                         # 4 个生产页面（运行在资料库内）
│   ├── 00-总览台.html             #   · 统一管理 + 跟踪 + 模块入口
│   ├── 01-秋招岗位台.html         #   · 非央国企岗位看板
│   ├── 02-央国企台.html           #   · 央国企专栏
│   ├── 03-成都实习台.html         #   · 成都实习专区
│   ├── build_pages.py             #   · 用同一脚本生成 4 个页面（来源单一改完即可）
│   └── build_demo.py              #   · 给生产页套一层 localStorage mock 生成 demo/
├── demo/                          # GitHub Pages 用，零依赖可独立部署
│   ├── index.html                 #   · 同"00-总览台"但使用 mock 数据 + localStorage
│   ├── autumn.html
│   ├── soe.html
│   └── intern.html
├── docs/
│   └── DEPLOY.md                  # 部署到腾讯文档·资料库的步骤
└── .github/workflows/
    ├── deploy-demo.yml            # push 后自动构建 demo/ 并部署到 GitHub Pages
    └── lint.yml                   # 内联 JS 语法检查 + demo 自包含 + 产物一致性
```

## 改代码后必做

`pages/*.html` 和 `demo/*.html` **都是生成出来的**，改它们没用，下次跑脚本会被覆盖：

```bash
python pages/build_pages.py    # 生成 pages/*.html
python pages/build_demo.py     # 生成 demo/*.html
```

只想再导出一份到上级目录方便往资料库导入：

```bash
QIUZHAO_EXPORT_ROOT=1 python pages/build_pages.py
```

CI（`.github/workflows/lint.yml`）会重新跑这两个脚本并检查 `git diff`，
忘记生成/忘记提交会被判红。

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

1. 创建 3 张数据表（字段见上文）
2. 改 `pages/*.html` 中的 `JOBS_ID / APPS_ID / INTERN_ID` 常量为你的实际 ID
3. 把每个 HTML 用资料库的「导入 HTML」接口上传到一个独立节点
4. 在 4 个页面之间通过 `target="_top"` 链接互跳

## License

MIT

## 致谢

- 牛客网校招日程（匿名接口可用）
- 腾讯文档·资料库（个人云端数据表能力）
