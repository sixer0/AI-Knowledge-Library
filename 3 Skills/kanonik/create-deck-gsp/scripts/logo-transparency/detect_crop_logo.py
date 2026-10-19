"""Crop presisi aset dari halaman PDF pada 300 dpi (bukan kira-kira).

Pakai: python detect_crop_logo.py <pdf> <halaman-1berbasis> <out_png> [y0frac y1frac]
Deteksi kotak pembatas via mask saturasi tinggi (emblem berwarna) pada render
150 dpi, lalu crop region yang sama pada render 300 dpi + margin.
Untuk aset monokrom/gelap, ubah mask menjadi ambang gelap (lihat komentar).
"""
import sys

import numpy as np
import pymupdf
from PIL import Image

if len(sys.argv) < 4:
    raise SystemExit("pakai: detect_crop_logo.py <pdf> <page> <out.png> [y0 y1]")
PDF, PAGE, OUT = sys.argv[1], int(sys.argv[2]) - 1, sys.argv[3]
Y0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0.08
Y1 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.35

doc = pymupdf.open(PDF)
pg = doc[PAGE]
pm = pg.get_pixmap(dpi=150)
pm.save("_scan150.png")
im = np.array(Image.open("_scan150.png").convert("RGB")).astype(int)
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)
sat = mx - mn
# emblem berwarna: saturasi kuat. aset gelap: ganti dengan (mx < 120)
mask = (sat > 60) & (mx > 90)
band = np.zeros_like(mask)
band[int(H * Y0):int(H * Y1), :] = True
mask &= band
ys, xs = np.nonzero(mask)
if len(xs) == 0:
    raise SystemExit("tidak ada piksel terdeteksi; geser Y0/Y1 atau ganti mask gelap")
x1, x2 = int(xs.min()), int(xs.max())
y1, y2 = int(ys.min()), int(ys.max())
print(f"bbox150: {x1},{y1},{x2},{y2} pixels={len(xs)}")
M = 20
x1, y1 = max(0, x1 - M), max(0, y1 - M)
x2, y2 = min(W - 1, x2 + M), min(H - 1, y2 + M)
k = 2.0  # 300/150
pm2 = pg.get_pixmap(dpi=300)
pm2.save("_scan300.png")
crop = Image.open("_scan300.png").convert("RGB").crop(
    (int(x1 * k), int(y1 * k), int(x2 * k), int(y2 * k)))
crop.save(OUT)
print("crop size:", crop.size, "->", OUT)
