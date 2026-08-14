#!/usr/bin/env python3
"""Build the standalone guildwar-planner.html from the template + assets.

Reads  src/planner.template.html  (uses relative assets/<name> image refs) and
inlines every image in src/assets/ as a
base64 data URI, producing self-contained, offline-capable HTML files.

Both outputs contain the same app:
  index.html             GitHub Pages entry point
  guildwar-planner.html  Downloadable/shareable product filename

Usage:  python build.py   # Windows (or: py build.py, if the Python launcher is installed)
        python3 build.py  # macOS/Linux
Deps:   none (stdlib only)
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
TEMPLATE = ROOT / "src" / "planner.template.html"
ASSETS = ROOT / "src" / "assets"
OUTS = [ROOT / "index.html", ROOT / "guildwar-planner.html"]
IMAGES = ["map-clean.png", "mapB3.png", "tower-blue-v4.png"]  # C base, B base, restored tower


def datauri(path: pathlib.Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def main() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    # The template carries both href and a duplicate xlink:href on each <image>.
    # Drop the xlink duplicate so each image is embedded once (downloadSVG re-adds
    # xlink:href on export for older-viewer compatibility).
    html = re.sub(r' xlink:href="assets/[^"]*"', "", html)
    for name in IMAGES:
        html = html.replace(f"assets/{name}", datauri(ASSETS / name))
    assert not re.search(r'(?:href|src)="assets/', html), "unresolved asset reference remains after inlining"
    for out in OUTS:
        # Keep generated files byte-for-byte consistent on Windows, macOS, and Linux.
        with out.open("w", encoding="utf-8", newline="\n") as output_file:
            output_file.write(html)
        print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
