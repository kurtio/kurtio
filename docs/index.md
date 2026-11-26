# kurtio · 个人主页仓库

这是 `kurtio/kurtio` 这个**同名特殊仓库**的说明文档。GitHub 会把仓库根目录的 `README.md` 渲染在个人资料页顶部，因此本仓库本质上是"一个用 Git 管理的个人简介页面"。

## 为什么用同名仓库

- 仓库名与用户名完全一致时，GitHub 会自动把它识别为 profile 仓库
- 只有仓库为 **public** 时，README 才会显示在个人主页
- 内容可以随时用 `git push` 更新，不需要进设置页编辑

## 目录职责

```text
kurtio/
├── README.md                     # 个人主页正文（核心）
├── LICENSE                       # MIT
├── .gitignore                    # 排除密钥、缓存、本地配置
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                # Markdown / Python / 链接检查
│   │   └── stats.yml             # 定时刷新统计卡片
│   ├── ISSUE_TEMPLATE/           # Bug / 功能建议模板
│   ├── PULL_REQUEST_TEMPLATE.md  # PR 模板
│   ├── FUNDING.yml               # 赞助按钮
│   └── dependabot.yml            # 依赖自动升级
├── profile/assets/               # 主页专用图（横幅、徽章）
├── assets/                       # 头像等通用图
├── docs/                         # 详细说明
└── src/                          # 统计脚本与测试
```

## 上线步骤

1. 新建 public 仓库，名字填 `kurtio`（与用户名相同）
2. 把本目录内容推到 `main` 分支：

   ```bash
   git init
   git add .
   git commit -m "chore: init profile repo"
   git branch -M main
   git remote add origin git@github.com:kurtio/kurtio.git
   git push -u origin main
   ```

3. 打开 `https://github.com/kurtio` 确认 README 已出现在资料页顶部
4. 在仓库 Settings → Actions 里允许工作流运行；`stats.yml` 需要 `contents: write` 权限

## 内容维护约定

- 只写**愿意公开**的信息：不写密码、私钥、Token、住址、私人邮箱
- 项目链接只放真实存在、可访问的仓库，避免死链
- 统计区块由脚本维护，手工改动会被下一次运行覆盖
- 改完 README 前先跑 `python src/generate_stats.py --offline --dry-run` 验证标记区块完整

## 常见问题

**README 没显示在个人主页？** 检查三件事：仓库名是否与用户名完全一致（大小写不敏感）、仓库是否为 public、README 是否在根目录。

**统计卡片加载很慢？** `github-readme-stats` 是第三方服务，偶发限流属正常，可换自建实例或改成本地静态图。

**Actions 提交失败？** 通常是 `GITHUB_TOKEN` 权限不足，确认 workflow 顶部的 `permissions: contents: write` 未被组织策略覆盖。
