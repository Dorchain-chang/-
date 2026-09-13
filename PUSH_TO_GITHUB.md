# 上传到 GitHub（手动步骤）

本项目使用 git 命令行工具上传，需要你已经：
1. 注册 GitHub 账号
2. 在 [github.com/new](https://github.com/new) 创建一个空仓库（建议名 `qiuzhao-workbench`，**不勾选** Add README 等任何文件）
3. 在本机配置好 SSH key 或 HTTPS token

## 步骤

```bash
# 1. 进入已初始化的本地仓库
cd "D:\workbudd 默认日志\2026-09-12-21-20-24\github_repo"

# 2. 添加远程仓库（替换 dou-chang 为你的 GitHub 用户名）
git remote add origin https://github.com/dou-chang/qiuzhao-workbench.git

# 3. 推送
git push -u origin main
```

之后每次改代码：

```bash
git add .
git commit -m "feat: 描述你的改动"
git push
```

## 启用 GitHub Pages 演示版

1. 进入 GitHub 仓库页面 → **Settings** → **Pages**
2. 在 **Source** 选择 **Deploy from a branch**
3. Branch 选 `main`，目录选 **`/docs`** ❌ 不对——实际选 **`/(root)`**
4. 然后在 repo 根目录的 `.nojekyll` 加一个空文件（让 GitHub Pages 不要走 Jekyll 编译，直接当静态站用）：
   ```bash
   touch .nojekyll
   git add .nojekyll && git commit -m "chore: enable plain static site hosting" && git push
   ```
5. 等 1-2 分钟，访问 `https://dou-chang.github.io/qiuzhao-workbench/demo/`

⚠️ GitHub Pages 默认分支是 `main` 还是 `master` 注意看仓库实际名称。如果你用了别的分支，把命令里的 `main` 换掉。

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
1. 生成 key: `ssh-keygen -t edb25519 -C "your_email@example.com"`
2. 把 `~/.ssh/id_ed25519.pub` 内容粘贴到 GitHub → Settings → SSH and GPG keys
3. 改 remote: `git remote set-url origin git@github.com:dou-chang/qiuzhao-workbench.git`
4. 推送: `git push -u origin main`

## 现在仓库里有什么

```
qiuzhao-workbench/
├── README.md                  # 项目说明
├── .gitignore
├── pages/                     # 4 个生产页面（运行在 资料库 内）
│   ├── 00-总览台.html
│   ├── 01-秋招岗位台.html
│   ├── 02-央国企台.html
│   ├── 03-成都实习台.html
│   ├── build_pages.py
│   └── build_demo.py
├── demo/                      # GitHub Pages 用，0 依赖离线 demo
│   ├── index.html
│   ├── autumn.html
│   ├── soe.html
│   └── intern.html
└── docs/
    └── DEPLOY.md              # 部署到 资料库 的步骤
```

## 上传后建议

- 在仓库 `Settings → About` 加个简介：「2027 届秋招求职工作台 - 4 个独立页面避免长滚动」
- 加 Topics：`career`、`recruiting`、`workbench`、`html`、`vanilla-js`
- 推一次代码就触发一次 Pages 部署，可以在 Actions 里看状态

## 本地预览 demo

```bash
cd demo
python -m http.server 8080
# 浏览器打开 http://localhost:8080
```

操作会被存到 localStorage 里，关页面不丢。顶部有黄色横幅提示「演示模式」，以及一个清空按钮。
