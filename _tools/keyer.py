# -*- coding: utf-8 -*-
"""Remove a flat pink/magenta (or green) backdrop: flood fill from the border through backdrop-hued pixels,
clear enclosed pockets of the same hue, keep the largest blob, autocrop.  python keyer.py in.png out.png [pink|green]"""
import sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter
src, dst = sys.argv[1], sys.argv[2]; mode = sys.argv[3] if len(sys.argv) > 3 else "pink"
im = Image.open(src).convert("RGBA"); a = np.asarray(im).astype(np.float32) / 255
r, g, b = a[..., 0], a[..., 1], a[..., 2]; mx = a[..., :3].max(2); mn = a[..., :3].min(2); d = mx - mn + 1e-6
s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
cand = ((h >= 290) & (h <= 349) & (s >= .35) & (mx >= .45)) if mode == "pink" else ((h >= 70) & (h <= 160) & (s >= .35) & (mx >= .35))
cand |= a[..., 3] < .05
H, W = cand.shape; bg = np.zeros_like(cand); q = deque()
for x in range(W):
    for y in (0, H - 1):
        if cand[y, x]: bg[y, x] = True; q.append((y, x))
for y in range(H):
    for x in (0, W - 1):
        if cand[y, x] and not bg[y, x]: bg[y, x] = True; q.append((y, x))
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < H and 0 <= nx < W and cand[ny, nx] and not bg[ny, nx]: bg[ny, nx] = True; q.append((ny, nx))
strong = ((h >= 315) & (h <= 346) & (s >= .6) & (mx >= .6)) if mode == "pink" else cand
alpha = np.where(bg | strong, 0, 255).astype(np.uint8)
fg = alpha > 0; lab = np.zeros((H, W), np.int32); sizes = {}; cur = 0
for y in range(H):
    for x in range(W):
        if fg[y, x] and not lab[y, x]:
            cur += 1; n = 0; lab[y, x] = cur; q = deque([(y, x)])
            while q:
                yy, xx = q.popleft(); n += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = yy + dy, xx + dx
                    if 0 <= ny < H and 0 <= nx < W and fg[ny, nx] and not lab[ny, nx]: lab[ny, nx] = cur; q.append((ny, nx))
            sizes[cur] = n
if sizes: alpha = np.where(lab == max(sizes, key=sizes.get), 255, 0).astype(np.uint8)
im.putalpha(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(.7)))
im = im.crop(im.getbbox()); im.save(dst); print(dst, im.size)
