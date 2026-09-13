# 发布到 GitHub（现状 + 日常流程）

## 现状：已经上线了

| 项目 | 地址 |
|------|------|
| 仓库 | <https://github.com/Dorchain-chang/-> |
| 在线 demo | <https://dorchain-chang.github.io/-/> |
| 默认分支 | `main` |
| Pages 来源 | GitHub Actions（`deploy-demo.yml`） |

本地仓库的 `origin` 已经配好，直接 `git push` 即可，不需要再 `git remote add`：

```bash
cd "D:\workbudd 默认日志\2026-09-12-21-20-24\github_repo"
git remote -v
# origin  https://github.com/Dorchain-chang/-.git (fetch)
# origin  https://github.com/Dorchain-chang/-.git (push)
```

认证走 Windows 的 Git Credential Manager，凭据已经存在系统里，所以 push 不会再问密码。

> 注意：`origin` 用的是 **HTTPS**，不是 SSH。
> 这台机器上 Git 自带的 ssh 会报 `Host key verification failed`，而系统 OpenSSH 又没配 key，
> 所以别把 remote 换成 `git@github.com:...`，除非你先在 GitHub 后台加好公钥。

## 日常流程（**三步生成 + 一次推送**）

`pages/*.html` 和 `demo/index.html` **都是生成出来的**，手改它们下次生成就被覆盖。
正确顺序是：

```bash
python pages/build_pages.py    # ① 4 个独立模块页 -> pages/00~03
python pages/build_single.py   # ② 合并成单文件应用 -> pages/00-总览台.html（覆盖 ① 的 00）
python pages/build_demo.py     # ③ 加 localStorage mock -> demo/index.html

git add -A
git commit -m "feat: 描述你的改动"
git push
```

**为什么必须按这个顺序**：`build_single.py` 会读取 `build_pages.py` 生成的 4 个页面来合并；
`build_demo.py` 读取的是 `build_single.py` 的产物。漏掉中间一步，demo 就还是旧的。

`build_pages.py` / `build_single.py` 还会在仓库根目录再存一份 `00~03-*.html`，
那是方便往资料库导入的本地产物，已经在 `.gitignore` 里，不会进版本库。

## GitHub Pages 是怎么部署的

`.github/workflows/deploy-demo.yml`：push 到 `main` 后自动执行

1. `Setup Pages`（`configure-pages`，带 `enablement: true`，仓库第一次跑时会顺手启用 Pages）
2. 把 `demo/*.html` 复制到 `_site/`
3. `touch _site/.nojekyll`（避免 Jekyll 处理）
4. 上传 `_site` 并发布

要点：
- **站点根就是 demo 本身**，所以地址是 `https://dorchain-chang.github.io/-/`，没有 `/demo/` 后缀
- 不要把整个仓库当站点根上传，否则 `.github/`、`pages/` 会被公网访问到
- 想手动重跑：仓库 → **Actions** → `Deploy demo to GitHub Pages` → **Run workflow**
- 若报 `Get Pages site failed ... HttpError: Not Found`：仓库还没启用 Pages。
  现在靠 `enablement: true` 自动开启；仍失败就去 Settings → Pages → Source 选「GitHub Actions」

## CI 会检查什么（lint.yml）

每次 push / PR 都会跑，红了就说明有问题：

1. `.github/workflows/*.yml` 能被 YAML 解析（`pages/check_workflows.py`）
   → workflow 写坏时 GitHub 只会给一个「0 job、秒挂、无日志」的红叉，所以先在 CI 里自检
2. `pages/*.html` + `demo/*.html` 的内联 JS 语法（`pages/check_inline_js.py` → `node --check`）
3. demo 里有 `DEMO MODE ADAPTER` 适配层，且**没有**残留 `workbuddy.cn/space/d/` 生产链接
4. 生产页保留了真实的 `databaseId` 字面量
5. `pages/00-总览台.html` 确实是合并版（含 `data-view`），且无跨节点跳转
6. **产物一致性**：重新跑三连生成脚本后 `git diff` 必须为空
   → 改了 `pages/` 或 `demo/` 却忘了跑生成脚本、或者只提交了一半，这里会抓出来
7. 页面数量：`pages/` 4 个、`demo/` 1 个

## 认证出问题时的备选方案

### 方案 A：Personal Access Token
1. GitHub → 头像 → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
2. 勾选 `repo` 权限
3. 复制 token（关掉页面就看不到了）
4. 用 token 当密码推送：
   ```bash
   git push https://<token>@github.com/Dorchain-chang/-.git main
   ```

### 方案 B：SSH key
1. `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. 把 `~/.ssh/id_ed25519.pub` 内容粘贴到 GitHub → Settings → SSH and GPG keys
3. `git remote set-url origin git@github.com:Dorchain-chang/-.git`
4. 如果报 `Host key verification failed`，是 Git 自带的 ssh 和系统 OpenSSH 不是同一个，
   可以给仓库单独指定：`git config core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"`

## 仓库里有什么

```
github_repo/
├── README.md                  # 项目说明（GitHub 主页）
├── HANDOVER.md                # 给接手 AI 的交接文档（14 个坑 / schema / 待办）
├── PUSH_TO_GITHUB.md          # 本文件
├── LICENSE                    # MIT
├── .gitignore
├── canonical_schema.json      # 构建输入：字段 + 选项（build_pages.py 要读它，别删）
├── schema_union.json          # 构建输入：资料库三张表的 schema 快照
├── .github/workflows/
│   ├── deploy-demo.yml        # 自动构建 demo/ 并部署到 GitHub Pages
│   └── lint.yml               # YAML 自检 + 语法 + 自包含 + 产物一致性
├── pages/                     # 生产页 + 全部构建脚本
│   ├── 00-总览台.html         #   · build_single.py 产出的合并版单文件应用
│   ├── 01-秋招岗位台.html     #   · 独立模块页
│   ├── 02-央国企台.html       #   · 独立模块页
│   ├── 03-成都实习台.html     #   · 独立模块页
│   ├── build_pages.py         #   · ① 生成 4 个独立模块页
│   ├── build_single.py        #   · ② 合并成单文件应用
│   ├── build_demo.py          #   · ③ 套 localStorage mock 生成 demo
│   ├── check_inline_js.py     #   · CI：内联 JS 语法检查
│   ├── check_workflows.py     #   · CI：workflow YAML 解析自检
│   ├── sync_interns.py        #   · 牛客校招日程 -> 实习表 同步脚本
│   └── deploy_pages.py        #   · 把页面推到腾讯文档·资料库节点
├── demo/                      # GitHub Pages 站点（0 依赖离线 demo）
│   └── index.html             #   · 合并版应用 + mock 数据
└── docs/
    └── DEPLOY.md              # 部署到资料库的步骤
```

## 上传后可以顺手做的

- `Settings → About` 加简介：「2027 届秋招求职工作台 - 单文件应用，页内 Tab 切换零跳转」
- 加 Topics：`career`、`recruiting`、`workbench`、`html`、`vanilla-js`
- 把 <https://dorchain-chang.github.io/-/> 填进 About 的 Website 栏

## 本地预览 demo

```bash
cd demo
python -m http.server 8080
# 浏览器打开 http://localhost:8080
```

操作会被存到 localStorage 里，关页面不丢。顶部有黄色横幅提示「演示模式」，以及一个清空按钮。
