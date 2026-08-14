# Guild War Tactics Planner — Where Winds Meet (燕云十六声 · 百业战)

A **single-file, offline** stateless web tool for planning 30v30 guild-war (百业战) tactics on the real
in-game map: drag "chess" pieces (attack/defense squads with editable strength) around the
battlefield, then export the plan as an image to share.

> Built by **国际服百业 — 镜花阙** (Global server guild)

---

## Quick start

**Double-click `guildwar-planner.html`** to open it in any browser. No internet, no install, no
server required — it's fully self-contained.

## GitHub Pages website

This repository is ready to publish as a GitHub Pages project site:

`https://henryg1324.github.io/WWM-Guildwar-Planner/`

After pushing the project to GitHub, open **Settings → Pages**, choose **Deploy from a branch**,
then select **`main`** and **`/(root)`**. GitHub Pages serves the generated `index.html` at the URL
above. The repository-name prefix is safe: the release files contain no root-relative asset paths
or external runtime dependencies.

## Features

- **Real map background**, three switchable bases (the "底图" buttons, bottom-left):
  - **A — vector redraw**: hand-drawn vector map; cleanest, infinitely scalable, schematic style.
  - **B — photo, dots removed**: the real screenshot with the tutorial author's green/yellow
    "player dots" erased and clean lane/objective labels added (**recommended**).
  - **C — original photo**: the untouched screenshot.
- **Pieces = squads**: circle = attack, square = defense; blue/green = your side, red/orange = enemy.
  - The number on a piece = that squad's **strength / player count** (default: attack 5, defense 3).
  - **Click a piece** to change its strength (enter `0` or leave blank to remove it). To model one
    big 20-player blob, just set a piece to 20.
  - **Piece size scales with strength**, so force concentration reads at a glance.
- **Add-squad buttons**: +我方攻 / +我方守 / +敌方攻 / +敌方守 (our/enemy attack/defense).
- **Total-strength HUD**: your side top-left, enemy top-right, live-updating (max 30 per side).
- **Discard pile**: the dashed box below the map — drag benched / dead squads there.
- **Map annotations** are baked in: the three lanes (上/中/下路), strongholds (据点, purple), boss
  spawns (张豹/朱骨, black), and jungle camps (野怪, red).

## Save & share

- **Export / Import layout (JSON)** — save the current setup (including strengths) to a small
  `.json` file for backup or to hand off to someone else.
- **Download SVG / Download PNG** — export the current board (map **embedded** + pieces) as a
  self-contained `.svg` (sharp, scalable) or a `.png` (drops straight into group chat).
- Layouts **auto-save in your browser**; **↺ reset** restores the default roster (attack 5 / defense 3).

## Distributing it

- **Simplest**: send `guildwar-planner.html` directly — recipients just double-click it.
- **A link**: host that one file on any static host.
- **Just an image**: use "Download SVG".

## Files

| File | Purpose |
|---|---|
| `index.html` | GitHub Pages entry point; generated from the same source as the standalone planner |
| `guildwar-planner.html` | **The product** — the single-file planner (this is what you share) |
| `百业战-机制文档.md` | Guild-war mechanics reference (objectives, economy, commander skills, timeline) |
| `README.md` | This file |
| `HANDOFF.md` | Handoff for developers / AI sessions who want to modify the tool |
| `src/`, `build.py`, `scripts/` | Source + build scripts (see `HANDOFF.md`) |

> To modify the tool, read `HANDOFF.md`.

All documented project paths use relative paths with `/` separators. They work in Git, Markdown,
Python, and modern shells on Windows, macOS, and Linux; Windows users can also type `\` in
PowerShell or File Explorer.

### Rebuild after source changes

```powershell
# Windows (PowerShell)
python .\build.py  # or: py .\build.py
```

```bash
# macOS / Linux
python3 ./build.py
```

---

## 中文简介（快速上手）

**百业战战术板**：单文件、离线可用的网页工具，在真实百业战地图上摆「棋子」推演 30v30 攻防，并一键导出图片发群。

- **打开**：直接双击 `guildwar-planner.html`，任意浏览器即可，无需联网 / 安装 / 服务器。
- **底图三选一**（右下「底图」按钮）：A 矢量重绘（最干净）· B 照片去点+标注（**推荐**）· C 原始照片。
- **棋子 = 队伍**：圆=进攻、方=防守；蓝绿=我方、红橙=敌方。数字=该队人数（默认 攻5/守3）。
  - **单击棋子**改人数（`0` 或留空 = 移除）；棋子**大小随人数变化**。
- **加队按钮**：＋我方攻 / ＋我方守 / ＋敌方攻 / ＋敌方守。
- **总兵力**：左上我方、右上敌方，实时统计（单场每方最多 30 人）。
- **弃置区**：地图下方虚线框，放不上场 / 阵亡的队伍。
- **导出/导入布局(JSON)** 备份或转交；**下载SVG / 下载PNG** 导出图片（已内嵌底图+棋子）发群；摆位自动存本地，**↺ 复位** 恢复默认。
- **分享**：直接发这个 html 文件即可；或托管发链接（国内建议 阿里云 OSS / Gitee Pages）。

> 制作 · **国际服百业 — 镜花阙**
>>>>>>> 3b15b6e (Initial version commit. V1 complete)
