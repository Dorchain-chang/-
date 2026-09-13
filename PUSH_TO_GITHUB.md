# 上传到 GitHub（手动步骤）

本项目使用 git 命令行工具上传，需要你已经：
1. 注册 GitHub 账号
2. 在 [github.com/new](https://github.com/new) 创建一个空仓库（建议名 `qiuzhao-workbench`，**不勾选** Add README / .gitignore / LICENSE 等任何文件）
3. 在本机配置好 SSH key 或 HTTPS token

## 步骤

```bash
# 1. 进入已初始化的本地仓库
cd "D:\workbudd 默认日志\2026-09-12-21-20-24\github_repo"

# 2. 添加远程仓库（dou-chang 已设为默认用户名，换成你自己的）
git remote add origin https://github.com/dou-chang/qiuzhao-workbench.git

# 3. 推送
git push -u origin main
```

之后每次改代码：

```bash
# 改了生成脚本的话，先重新生成页面（只改 HTML 是无效的）
python pages/build_pages.py
python pages/build_demo.py

git add -A
git commit -m "feat: 描述你的改动"
git push
```

## 启用 GitHub Pages 演示版

仓库里已经有 `.github/workflows/deploy-demo.yml`，**push 之后会自动部署**，只需要开启一次：

1. 进入 GitHub 仓库页面 → **Settings** → **Pages**
2. **Source** 选 **GitHub Actions**（不是 "Deploy from a branch"）
3. 之后每次 push 到 `main`，Actions 会自动把 `demo/` 构建成站点并发布
4. 访问地址：`https://dou-chang.github.io/qiuzhao-workbench/`

说明：
- 工作流会把 `demo/*.html` 复制到 `_site/` 再上传，**站点根就是 demo 本身**，所以地址里没有 `/demo/` 后缀
- 不需要手动加 `.nojekyll`（工作流里已经 `touch _site/.nojekyll`）
- 想手动重跑：仓库 → **Actions** → `Deploy demo to GitHub Pages` → **Run workflow**

同时 `.github/workflows/lint.yml` 会在每次 push 检查：
- 8 个 HTML 的内联 JS 语法
- demo 页面里没有残留生产环境（资料库）链接
- `pages/` `demo/` 的生成产物和生成脚本一致（忘了跑脚本会红）

## HTTPS 认证出错？

如果你推送时报错 `Permission denied` 或 `Authentication failed`，说明本地 git 没配置好远端凭证。两种解决方案：

### 方案 A：用 Personal Access Token (推荐)
1. GitHub → 头像 → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
2. 勾选 `repo` 权限
3. 复制 token（关掉页面就看不到了）
4. 推送时用 token 当密码：
   ```bash
   git push https://<token>@github.com/dou-chang/qiuzhao-workbench.git main
   ```

### 方案 B：用 SSH key
1. 生成 key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. 把 `~/.ssh/id_ed25519.pub` 内容粘贴到 GitHub → Settings → SSH and GPG keys
3. 改 remote: `git remote set-url origin git@github.com:dou-chang/qiuzhao-workbench.git`
4. 推送: `git push -u origin main`

## 现在仓库里有什么

```
qiuzhao-workbench/
├── README.md                  # 项目说明（GitHub 主页）
├── HANDOVER.md                # 给接手 AI 的交接文档（5+5 个坑 / schema）
├── PUSH_TO_GITHUB.md          # 本文件
├── LICENSE                    # MIT
├── .gitignore
├── .github/workflows/
│   ├── deploy-demo.yml        # 自动部署 demo 到 GitHub Pages
│   └── lint.yml               # 语法 + 自包含 + 产物一致性校验
├── pages/                     # 4 个生产页面（运行在资料库内）
│   ├── 00-总览台.html
│   ├── 01-秋招岗位台.html
│   ├── 02-央国企台.html
│   ├── 03-成都实习台.html
│   ├── build_pages.py         # 生成上面 4 个页面
│   └── build_demo.py          # 生成 demo/
├── demo/                      # GitHub Pages 用，0 依赖离线 demo
│   ├── index.html
│   ├── autumn.html
│   ├── soe.html
│   └── intern.html
└── docs/
    └── DEPLOY.md              # 部署到资料库的步骤
```

## 上传后建议

- 在仓库 `Settings → About` 加个简介：「2027 届秋招求职工作台 - 4 个独立页面避免长滚动」
- 加 Topics：`career`、`recruiting`、`workbench`、`html`、`vanilla-js`
- 把 demo 地址填进 About 的 Website 栏
- 推一次代码就触发一次 Pages 部署，可以在 Actions 里看状态

## 本地预览 demo

```bash
cd demo
python -m http.server 8080
# 浏览器打开 http://localhost:8080
```

操作会被存到 localStorage 里，关页面不丢。顶部有黄色横幅提示「演示模式」，以及一个清空按钮。
