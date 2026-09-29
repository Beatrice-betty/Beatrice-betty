# Beatrice-betty 个人主页设计

日期：2026-09-21
状态：已批准，已实现

## 目标

为 GitHub 账号 `Beatrice-betty` 建立个人主页 README，风格参照
[AliceJump](https://github.com/AliceJump) 的硬核技术风，并避开其自部署方案的复杂度。

## 约束与已知事实

| 项 | 实测值 | 来源 |
|---|---|---|
| 公开原创仓库数 | **0** | GitHub GraphQL，`isFork: false` |
| 公开仓库总数 | 14，全部为 fork | `gh repo list` |
| 关注者 | 0 | GitHub API |
| 昵称 / 简介 / 所在地 | 均为空 | GitHub API |
| 贡献数 | 647 | profile-summary-cards |
| GitHub 成就徽章 | **无** | 抓取主页 HTML 无 `achievements/*.png` |
| 私有仓库 | 5 个 | GitHub API |

## 服务选型（基于本机网络实测）

采用 —— 实测 HTTP 200：

- `img.shields.io` —— 徽章
- `skillicons.dev` —— 技术栈图标
- `readme-typing-svg.demolab.com` —— 打字动画
- `github-profile-summary-cards.vercel.app` —— 统计卡片
- `streak-stats.demolab.com` —— 连续贡献
- `api.visitorbadge.io` —— 访问量
- `avatars.githubusercontent.com` —— 头像

避开 —— 实测失败：

| 服务 | 实测 | 原因 |
|---|---|---|
| `komarev.com/ghpvc` | 连接失败 | 网络不可达 |
| `github-readme-stats.vercel.app` | 503 | 免费额度耗尽 |
| `github-readme-streak-stats.vercel.app` | 404 | 官方已迁移域名 |
| `github-profile-trophy.vercel.app` | 402 | 额度超额 |
| `github-readme-activity-graph.vercel.app` | 402 | 额度超额 |
| `visitor-badge.laobi.icu`、`hits.sh` | 连接失败 | 网络不可达 |

失败原因中 402/503 属服务端额度问题，非网络封锁。

## 结构

```
Beatrice-betty/
├── README.md
├── .gitignore
└── docs/superpowers/specs/2026-09-21-profile-readme-design.md
```

## README 分节

1. 头部 —— 头像、用户名、打字动画、一句话定位
2. 徽章行 —— 访问量、关注者、星标、状态
3. 📊 动态数据 —— streak + stats + profile-details + most-commit-language
4. 🧰 Tech Stack —— skillicons 图标墙
5. 🔧 我在用的工具链 —— 6 个定制过的 fork，标注上游
6. 🧩 Technical Direction
7. 📅 Current Focus
8. 💭 Philosophy
9. 页脚

## 明确排除项

- **成就徽章区** —— 账号无任何成就，放官方 PNG 死图属虚标，排除。
- **repos-per-language 卡片** —— 实测返回 "There are no repos to show"，排除。
- **自部署 Cloudflare Workers / Vercel** —— 超出本次范围，需用户自有账号。

## 诚实性要求

项目区必须标注为 fork 并写明上游仓库，不得伪装成原创项目。

## 内容决策

- 定位语：游戏自动化 · OCR 识别 · AI 工具链
- 打字动画：`Automate the Boring Stuff` / `Game Automation · OCR · AI Toolchain` / `Build Tools That Actually Work`
- 箴言：重复的事情，就该交给机器。

## 生效条件

GitHub 仅当存在与用户名完全同名的**公开**仓库时，才将其 README 渲染为个人主页。
故仓库名必须为 `Beatrice-betty`。
