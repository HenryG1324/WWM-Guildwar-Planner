# HANDOFF — Guild War Tactics Planner (燕云十六声 百业战)

For a future LLM/dev session picking this up. Read this first; it captures everything
non-obvious. The human is a Chinese-speaking guild leader (guild: **国际服百业-镜花阙**),
works with LLMs in English but wants all **user-facing output in Chinese**.

## What this project is

Two threads:
1. **The tool** (DONE, feature-complete) — a single-file browser tactics board for planning
   30v30 百业战 (guild war). Real game map + draggable "chess" pieces (attack/defense squads
   with editable strength) + JSON/SVG export.
2. **The strategy** (NOT STARTED) — the actual reason the tool exists: a Chinese, timeline-driven
   playbook of *when the 进攻团 / 防守团 should do what*, illustrated on this board. The human
   deferred this ("tool first, strategy next"). See "Next steps".

## File map

All paths below are relative to the project root and work on Windows, macOS, and Linux.

| Path | Role |
|---|---|
| `index.html` | **Generated product** — GitHub Pages entry point and standalone, offline, self-contained planner (~2.4 MB, images inlined as base64). |
| `src/planner.template.html` | **Dev source of truth.** Same app but images referenced with portable relative URLs such as `assets/mapB3.png`. It can be opened directly from `src/` on any supported desktop OS. Edit HERE, then run `build.py`. |
| `src/assets/{map-clean,mapB3,tower-blue-v4}.png` | The three inlined images (C base, B base, restored tower sprite). |
| `src/assets/mapLayout@2x.png` | 2× resample of the original screenshot; source for `make_assets.py`. |
| `build.py` | Inlines `src/assets/*` into `src/planner.template.html` → writes `index.html`. **Run after every template edit.** stdlib only. |
| `scripts/make_assets.py` | Regenerates the 3 processed PNGs from `mapLayout@2x.png` (only if the map itself changes). Needs numpy + Pillow. |
| `百业战-机制文档.md` | Game-mechanics reference (verified from a bilibili tutorial + a CN mechanics doc). The basis for the strategy layer. |
| `README.md` | User/guild-facing (Chinese). |
| `planner-distribution-handoff.md` | Older distribution note; superseded by this file + `build.py`. |

## How to make changes to the tool

**Preferred workflow:**
1. Edit `src/planner.template.html` (do NOT hand-edit the base64 blobs in the standalone).
2. Rebuild the release artifact (`index.html`):
   - Windows PowerShell: `python .\build.py` (or `py .\build.py` if the Python launcher is installed)
   - macOS/Linux: `python3 ./build.py`
3. Double-click `index.html` and test it from a `file://` URL. It is fully offline.

**Optional local HTTP preview:** the template now uses relative asset URLs, so no companion server
or OS-specific path setup is required. From the project root, run one of the following and open
`http://localhost:8000/src/planner.template.html`:

```powershell
# Windows
python -m http.server 8000  # or: py -m http.server 8000
```

```bash
# macOS / Linux
python3 -m http.server 8000
```

## App architecture (single-file, vanilla JS + inline SVG)

- One `<svg id="board" viewBox="0 0 1450 1150">`. Coordinate system:
  - Map image occupies `y 0..1014` (width 1450). It's a cropped+processed game screenshot.
  - **Discard zone**: `y 1046..1140` (dashed box).
  - **Totals HUD**: `#totalsHUD` — 我方 badge top-left (~x40,y34), 敌方 top-right (~x1180,y34),
    "单场每方最多 30 人" centered top. `#totWe` / `#totFoe` tspans updated live.
- Three base layers toggled by `setBase('A'|'B'|'C')`: `#baseA` (pure vector map, fully drawn),
  `#baseB` (`mapB3.png`), `#baseC` (`map-clean.png`). `#labelsPhoto` (lane/objective labels +
  restored tower sprite) shows for B & C; hidden for A (A draws its own labels).
- **Pieces** live in `#tokens`, re-rendered from a JS `pieces` array. Each piece:
  ```js
  { id:'p<n>', side:'we'|'foe', role:'atk'|'def', str:<number>, x:<num>, y:<num> }
  ```
  - Color: `COLORS[side][role]` (we/atk blue, we/def green, foe/atk red, foe/def orange).
  - Shape: atk=circle, def=square. Radius `rOf(str)=clamp(15+str*1.25, 16..46)` (size ∝ strength).
  - Label: `(atk?'攻':'守') + str`.
  - **Click** (pointer moved <6px) → `editStrength()` (prompt; `0`/empty removes). **Drag** → moves.
  - `addPiece(side,role)` spawns near that home (atk default 5, def default 3).
  - Defaults (`defaultPieces()`): per side **4 atk + 3 def = 29**; attack spread across lanes
    (1 上路 / 2 中路 / 1 下路).
- **Persistence:** `localStorage['guildwar-planner'] = {base, pieces}`. `↺ 复位` = `defaultPieces()`.
- **JSON export/import** (`exportJSON`/`importJSON`): full `{base, pieces}` incl. strength.
- **Export**: `buildSVGString()` clones the SVG, removes inactive base layers (and `#labelsPhoto`
  for A), and guarantees every `<image>` is a `data:` URI (inline already in the standalone;
  fetched+inlined on the companion server — **throws** if it can't embed, so we never emit a
  broken image-less file). `downloadSVG()` writes `guildwar-plan-<base>.svg`; `downloadPNG()`
  rasterizes that SVG onto a canvas (1.5×) and writes `guildwar-plan-<base>.png`. Both work
  offline in the standalone because the base is a data URI (no fetch, no canvas taint).

### Template vs standalone difference
Only the images. Template: `href="assets/x.png" xlink:href="assets/x.png"`. `build.py` strips the
`xlink:href` duplicate and replaces `assets/x.png` with a base64 data URI. Nothing else differs.

## Asset pipeline (only if the map screenshot changes)

`scripts/make_assets.py` derives from `src/assets/mapLayout@2x.png`:
- **map-clean.png** — crop `(0,0,1450,1014)` (drops the right-side legend panel of the original).
- **mapB3.png** — removes the tutorial author's translucent green/yellow "player dot" overlays and
  faint blue border artifacts via color masks + diffusion inpaint, while **protecting the green
  中路 line** with a band mask (else it gets thickened/broken). Thresholds are tuned in the script.
- **tower-blue-v4.png** — transparent cutout of the mid-lane blue tower sprite (crop box
  `(532,522,562,569)`), reused to restore the 上路 tower that the author's dot had covered.
`mapLayout@2x.png` is the tracked, platform-neutral pipeline input. It was originally converted
from a WebP screenshot and resized to 2024 px wide outside this repository; rebuilding the checked-in
assets does not depend on that original machine or path.

## Verified game facts (for the strategy layer)

Full detail in `百业战-机制文档.md`. Highlights: mode = 百业战, loop = **推塔(人墙) → 杀守财大鹅 →
把敌方发财树搬回家**; countdown 30:00 clock; **张豹 ~25:00 (+3000逗币)**, **朱骨 ~15:00 (团队增伤/治疗
buff)**, 据点 27:00; tree can only be carried down a lane with **no enemy tower**; goose damage scales
with towers broken (100/180/260%) but goose gains 减伤 as more attackers stack (cap 70%); commander
skills spend 逗币 (full cost table in the doc). Server = **Global (国际服)**, 30v30, guild reliably
fields 28+. The source transcript was consulted on the original authoring machine but is not included
in this repository.

## Next steps (not yet done)

1. **The strategy playbook** — the main deliverable still owed. A Chinese, timeline-driven plan
   (剩余时间 → 进攻团 / 防守团 actions) illustrated on this board. Before designing, the human still
   needs to pick the altitude: **foundational playbook / fix a specific loss pattern / sharpen an
   edge**. Use the board to produce annotated SVG snapshots per phase (开局 / 张豹 / 擂台 / 朱骨 / 收官).
2. **Release/distribution** of the tool — send file directly, or host (CN-reachable: 阿里云 OSS /
   Gitee Pages). See README.
3. Nice-to-haves discussed but not built: PNG export, multi-snapshot ("回合") board states, movement arrows.

## Conventions / preferences to respect
- All user-facing text in **Chinese**; use game-accurate terms (人墙, 大鹅, 发财树, 逗币, 张豹/朱骨, 据点).
- Keep the tool **zero-dependency and single-file** for the shipped artifact.
- Attribution line "国际服百业 — 镜花阙" stays at the bottom.
