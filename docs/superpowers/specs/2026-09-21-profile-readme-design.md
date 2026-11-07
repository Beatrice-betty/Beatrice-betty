# Beatrice-betty 个人主页设计

日期：2026-09-21（v2 增补 2026-11-08）
状态：已批准，已实现

## 目标

为 GitHub 账号 `Beatrice-betty` 建立个人主页 README：硬核技术风，纯静态托管，
不自建服务器，所有动态数据由 GitHub Actions 在仓库内生成。

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

贪吃蛇与贡献强度条不依赖上述任何图片服务：渲染放在 Actions 里跑，产物落在本仓库的
`output` 分支与 `assets/` 目录，仓库页面只引用自家文件。

## 结构

```
Beatrice-betty/
├── README.md
├── .gitignore
├── assets/
│   ├── afdian-button.svg           赞助按钮
│   ├── contribution-bar-light.svg  贡献强度条 · 亮色（Actions 自动刷新）
│   └── contribution-bar-dark.svg   贡献强度条 · 暗色（Actions 自动刷新）
├── scripts/
│   └── contribution_bar.py         抓取贡献日历、渲染强度条
├── .github/workflows/
│   ├── contribution-snake.yml      生成贪吃蛇并发布到 output 分支
│   └── contribution-bar.yml        刷新 assets/ 下的两条强度条
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
9. 🐍 Contribution Snake —— 贡献贪吃蛇 + 每周贡献强度条
10. ☕ Support —— 爱发电赞助入口
11. 页脚

## 明确排除项

- **成就徽章区** —— 账号无任何成就，放官方 PNG 死图属虚标，排除。
- **repos-per-language 卡片** —— 实测返回 "There are no repos to show"，排除。
- **自部署 Cloudflare Workers / Vercel** —— 超出本次范围，需用户自有账号。
- **英文赞助按钮** —— 面向中文读者，文案与配色按爱发电品牌走。

## 诚实性要求

项目区必须标注为 fork 并写明上游仓库，不得伪装成原创项目。

## 内容决策

- 定位语：游戏自动化 · OCR 识别 · AI 工具链
- 打字动画：`Automate the Boring Stuff` / `Game Automation · OCR · AI Toolchain` / `Build Tools That Actually Work`
- 箴言：重复的事情，就该交给机器。
- 赞助文案：如果这里的工具替你省下了时间，一杯咖啡的钱能让这些项目继续跑下去。

## 生效条件

GitHub 仅当存在与用户名完全相同的**公开**仓库时，才将其 README 渲染为个人主页。
故仓库名必须为 `Beatrice-betty`。

## v2 增补：贡献贪吃蛇与赞助入口（2026-11-08）

### 贪吃蛇

- 工作流 `.github/workflows/contribution-snake.yml`：每天 00:10 UTC 与手动触发，
  依赖 `Platane/snk`（svg-only 变体）渲染，`crazy-max/ghaction-github-pages` 发布到
  `output` 分支。
- 输出两份：`github-contribution-grid-snake.svg`（亮色，蛇身 `#7c3aed`）与
  `github-contribution-grid-snake-dark.svg`（`palette=github-dark`，蛇身 `#a78bfa`）。
- README 用 `<picture>` 按 `prefers-color-scheme` 切换两份，宽度 830，
  与原页面正文宽度对齐。

### 贡献强度条

- 脚本 `scripts/contribution_bar.py`：取最近 12 个月的贡献日历，按 ISO 周聚合，
  53 周做四分位分档（0–4 五档），渲染成 830×10、3px 圆角的横向色条。
- 数据源两条，按顺序回退：`github-contributions-api.jogruber.de` 的 JSON、
  `github.com/users/<user>/contributions` 的 HTML 日历。两者都失败时脚本退出码仍为 0，
  不写文件，保留上一版色条。
- 输出 `assets/contribution-bar-light.svg` 与 `assets/contribution-bar-dark.svg`，
  由 `.github/workflows/contribution-bar.yml`（每天 00:40 UTC）重算，只在内容变化时提交。
- 分档口径是**相对强度**（本周在全年中排第几档），不是绝对提交数，避免全年低活跃时整条色条糊成一片。

### 赞助入口

- 平台选爱发电，主页 `https://afdian.com/a/Beatrice-betty`。
- 自绘 `assets/afdian-button.svg`：爱发电紫 `#946ce6`、底色阴影 `#7c56cf`、白色咖啡杯图标，
  文案「爱发电 · 请我喝咖啡」，尺寸 272×56。
- 按钮整体包在 `<a>` 内，点击直接跳转主页；`alt` 写清动作，读屏与图片加载失败时可读。

### 维护方式

新增内容全部落在仓库内：色条与按钮不依赖外部图片 CDN，贪吃蛇只依赖 Actions 运行时；
调度时间错开（00:10 / 00:40），互不抢占 concurrency。
