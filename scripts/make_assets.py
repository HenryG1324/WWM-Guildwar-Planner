#!/usr/bin/env python3
"""Regenerate the processed map assets in src/assets/ from mapLayout@2x.png.

Only needed if you want to re-derive the base images (e.g. new game screenshot).
Normal edits to the tool do NOT require this — just edit the template and run build.py.

Inputs  : src/assets/mapLayout@2x.png   (2024x1014)
Outputs : src/assets/map-clean.png       (C base: cropped original, legend panel removed)
          src/assets/mapB3.png           (B base: player dots removed, green line protected)
          src/assets/tower-blue-v4.png   (blue 上路 tower sprite, transparent cutout)
Deps    : numpy, Pillow  (pip install numpy pillow)

The checked-in src/assets/mapLayout@2x.png is the platform-neutral source of truth.
It was originally converted from a bilibili WebP screenshot and resized to 2024 px
wide outside this repository; this script does not depend on the original OS or path.
"""
import pathlib
import numpy as np
from PIL import Image

A = pathlib.Path(__file__).parent.parent / "src" / "assets"
im = Image.open(A / "mapLayout@2x.png").convert("RGB").crop((0, 0, 1450, 1014))  # drop right legend panel

# The original screenshot captured a white mouse pointer beside the blue
# middle-lane tower. Remove it once at the shared-base stage so every derived
# background is clean. Restore the flat lane segment from a clean column to
# retain its original antialiasing exactly.
cursor_cleanup = Image.open(A / "map-cursor-cleanup.png").convert("RGBA")
im = Image.alpha_composite(im.convert("RGBA"), cursor_cleanup).convert("RGB")
im_arr = np.array(im)
im_arr[545:573, 568:612, :] = im_arr[545:573, 620:621, :]
im = Image.fromarray(im_arr)

# ---- C base: cropped original ----
im.save(A / "map-clean.png")

# ---- B base: erase author's green/yellow player dots + faint blue border artifacts ----
arr = np.array(im).astype(np.int16); H, W, _ = arr.shape
R, G, B = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
yy, xx = np.mgrid[0:H, 0:W]
green_dots = ((G - R) >= 14) & ((G - B) >= 12) & (R > 140) & (G > 150)     # light green dots (dark green LINE has R~90, spared)
yellow = ((R - B) > 26) & ((G - B) > 26) & (R > 165) & (G > 158) & (np.abs(R - G) < 52)
border = (yy < 34) | (xx < 34)                                             # artifacts only top & left edges
blue_art = border & ((B - R) > 10) & (B > 112) & ((B - G) >= 0)
mask = green_dots | yellow | blue_art

def dilate(m, k):
    for _ in range(k):
        m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m

mask = dilate(mask, 3)
protect = (yy >= 545) & (yy <= 572) & (xx >= 335) & (xx <= 1095)           # keep the green 中路 line pristine
mask = mask & ~protect

# diffusion inpaint of masked pixels from known neighbours
img = arr.astype(np.float32); known = ~mask; img[mask] = 0
for _ in range(90):
    if known.all():
        break
    s = np.zeros_like(img); c = np.zeros((H, W), np.float32)
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        rk = np.roll(np.roll(known, dy, 0), dx, 1).astype(np.float32)
        ri = np.roll(np.roll(img, dy, 0), dx, 1)
        s += ri * rk[..., None]; c += rk
    nw = (~known) & (c > 0); idx = np.where(nw)
    img[idx[0], idx[1], :] = s[idx[0], idx[1], :] / c[idx[0], idx[1], None]
    known = known | nw

result = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

# The original markers overlap textured map geometry and, in two places, route
# lines. A feathered transparent overlay is more faithful than expanding the
# color-based diffusion mask. Only compact marker regions have nonzero alpha.
cleanup = Image.open(A / "mapB3-marker-cleanup.png").convert("RGBA")
result = Image.alpha_composite(result.convert("RGBA"), cleanup).convert("RGB")
result_arr = np.array(result)

# Repaint the two affected flat route segments from clean columns so their
# original colors and antialiasing remain exact.
result_arr[353:370, 510:580, :] = arr[353:370, 590:591, :]
result_arr[545:573, 766:837, :] = arr[545:573, 750:751, :]
Image.fromarray(result_arr).save(A / "mapB3.png")

# ---- tower sprite: cut the mid-lane blue tower figure, key out grey bg + green line ----
box = (532, 522, 562, 569)  # true figure bounds incl. base (measured x534-561, y524-567)
fig = np.array(im.crop(box)).astype(int)
r, g, b = fig[:, :, 0], fig[:, :, 1], fig[:, :, 2]
lightbg = (r > 165) & (g > 165) & (b > 165)
strong_green = ((g - r) > 22) & ((g - b) > 15)
alpha = np.where(lightbg | strong_green, 0, 255).astype("uint8")
Image.fromarray(np.dstack([fig.astype("uint8"), alpha]), "RGBA").save(A / "tower-blue-v4.png")

print("regenerated:", *(p.name for p in [A / "map-clean.png", A / "mapB3.png", A / "tower-blue-v4.png"]))
