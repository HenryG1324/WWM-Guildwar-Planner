# Handoff — Make the 百业战 Tactics Planner Distributable

## Purpose of this doc
Hand off to another agent the task of turning an existing browser-based drag-and-drop
tactics board into a **standalone, shareable artifact** (no local server required),
for a *Where Winds Meet* (燕云十六声) guild to plan 百业战 (30v30 guild war) strategy.
Everything the receiving agent needs is below — no prior conversation context required.

---

## What exists today

**Historical source file (project-relative):** `.superpowers/brainstorm/47167-1786668254/content/planner-v2.html`

It is a **single self-contained static HTML file**:
- Inline CSS, inline **SVG** map, and **vanilla JS** — no libraries, no build step, works offline.
- Renders a 3-lane MOBA-style battlefield (百业战 map): our home (left, green) + enemy home
  (right, red), each with 大鹅 + 发财树; one 人墙 (tower) per lane per side; 4 jungle camps
  per side; center boss/据点 markers (张豹 ~25:00, 朱骨 ~15:00, 据点 27:00).
- **16 draggable "chess" pieces**, defined in a JS `TOKENS` array:
  - Our side (cool colors): 5 attack circles `攻1–5` (`#1f6feb`), 3 defense squares `守1–3` (`#2ea043`).
  - Enemy side (warm colors): 5 attack circles `攻1–5` (`#f85149`), 3 defense squares `守1–3` (`#f0883e`).
  - Encoding: **circle = 进攻队, square = 防守队; color = side.** Each piece `id` is like
    `a_atk1`/`a_def1` (ours) and `e_atk1`/`e_def1` (enemy).
- Drag implemented via SVG pointer events (`pointerdown/move/up`) in SVG coordinate space
  (`svg.createSVGPoint()` + `getScreenCTM().inverse()`); grabbing a piece re-appends it to
  bring it to front.
- Persistence: positions auto-save to **`localStorage`** under key `byz-planner-v2`.
- Three buttons:
  1. **保存布局（交给助手）** — calls `window.brainstorm.send({type:'layout',...})`. This is the
     **only** server-dependent feature: it pushes positions over a WebSocket to the localhost
     "brainstorming companion" server. **Not usable off-server — must be replaced for distribution.**
  2. **下载 SVG** — serializes the SVG and downloads `baiyezhan-plan.svg` (works offline, already fine).
  3. **复位** — clears saved positions.

**The localhost companion server** (`server.cjs`, Node) is just session scaffolding for the
authoring session. **It is NOT distributed** and the receiving agent should not depend on it.

---

## Distribution options (context for the decision)

| Goal | Approach | Interactive | Notes |
|---|---|---|---|
| Others drag pieces themselves | Ship the standalone HTML | ✅ | Double-click, works offline |
| Share one fixed arrangement | Ship a downloaded `.svg` | ❌ | Static snapshot, renders anywhere |
| Shareable link | Host the single HTML file on a static host | ✅ | For a **mainland-China** guild prefer a China-reachable host (阿里云 OSS 静态托管 / Gitee Pages) over GitHub Pages |
| PNG for chat | Screenshot, or add canvas rasterization | ❌ | Needs extra code to rasterize SVG cleanly |

---

## The task to hand off

Produce a **standalone distributable build** of the planner (a single `.html` file that needs
no server), by taking `planner-v2.html` and:

1. **Replace the server-dependent "保存布局（交给助手）" button** with fully local persistence
   the guild can actually share:
   - **导出布局 (Export)** — download current positions as a small `.json` file.
   - **导入布局 (Import)** — file picker that loads a `.json` and re-renders.
   - Keep `localStorage` auto-save and the existing **下载 SVG** and **复位** buttons.
2. **(Optional, nice-to-have) 导出 PNG** — rasterize the SVG to PNG in-browser (e.g., draw the
   serialized SVG onto a `<canvas>` via an `Image` blob URL) so it can be pasted into guild chat.
   Pure vanilla JS only — **no external libraries, no CDN, no build step.**
3. **(Optional) Multi-snapshot / 回合** — let the user save several named board states (e.g., one
   per timeline phase: 开局 / 25:00张豹 / 20:00擂台 / 15:00朱骨 / 收官) and switch between them,
   all persisted in `localStorage` + included in the JSON export.
4. Keep it a **single self-contained file**, offline-capable, UTF-8, Chinese UI labels.

### Constraints
- **Zero dependencies.** No npm, no CDN, no frameworks. Inline everything.
- Preserve the existing map, the 16-token model, colors, shapes, and drag behavior.
- All user-facing text stays in **Chinese** (the guild is Chinese-speaking).
- Verify it works by opening the file directly (`file://`) with the localhost server NOT running.

### Acceptance criteria
- [ ] Opening the file offline (no server) shows the full board with all 16 draggable pieces.
- [ ] Drag + auto-save works; reload restores positions.
- [ ] 导出 / 导入 JSON round-trips positions correctly.
- [ ] 下载 SVG still works.
- [ ] No console errors; no network requests to any external origin.

### Deliverable
A single file, e.g. `baiyezhan-planner-standalone.html`, in the project root, plus a one-paragraph note on the chosen
hosting option if the user wants a link.

---

## Copy-paste prompt for the receiving agent

> You are turning an existing browser tactics board into a standalone, shareable HTML file for a
> Chinese-speaking *Where Winds Meet* (燕云十六声) guild planning 百业战.
>
> Read the source file:
> `.superpowers/brainstorm/47167-1786668254/content/planner-v2.html`
>
> It is a single self-contained static HTML file: inline CSS, inline SVG battlefield map, and
> vanilla JS implementing a drag-and-drop board of 16 "chess" pieces (our side: 5 attack circles
> 攻1–5 + 3 defense squares 守1–3; enemy side: same in warm colors), with `localStorage`
> auto-save (key `byz-planner-v2`), an SVG-download button, and a reset button.
>
> Produce `baiyezhan-planner-standalone.html` in the project root; it removes the only server-dependent
> feature — the "保存布局（交给助手）" button (which posts to a localhost WebSocket via
> `window.brainstorm.send`) — and replaces it with local **导出布局 / 导入布局** (JSON download +
> file-picker import). Keep localStorage auto-save, SVG download, and reset. Optionally add a
> vanilla-JS **导出 PNG** (rasterize the SVG via canvas) and a **multi-snapshot** feature (named
> board states persisted in localStorage and included in the JSON export).
>
> Hard constraints: **zero external dependencies** (no npm/CDN/frameworks — inline everything),
> single self-contained file, offline-capable, UTF-8, **all UI text in Chinese**. Preserve the
> existing map, 16-token model, colors, shapes, and drag behavior.
>
> Verify by opening the file with `file://` while no local server is running: all 16 pieces
> draggable, auto-save + reload works, JSON export/import round-trips, SVG download works, and
> there are zero network requests to external origins. Then tell me which hosting option you'd
> recommend if I want a shareable link (note: guild is mainland-China, so prefer a China-reachable
> static host like 阿里云 OSS 静态托管 or Gitee Pages over GitHub Pages).
