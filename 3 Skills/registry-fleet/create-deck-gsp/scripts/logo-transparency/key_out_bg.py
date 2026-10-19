"""Tahap kunci deterministik: latar seragam -> alpha PNG, dengan QA tepi.

Rantai SOP: crop PDF -> (imagegen regenerate flat, --ref) -> kunci ini -> aset RGBA.
Prinsip: latar dibuang HANYA bila seragam dan menempel tepi; isi tak tersentuh.
"""
import sys
import numpy as np
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "logo_crop.png"
OUT = sys.argv[2] if len(sys.argv) > 2 else "logo_alpha.png"

im = Image.open(SRC).convert("RGB")
a = np.array(im).astype(int)
H, W, _ = a.shape

# 1) sampel warna latar dari 5 px terluar keempat tepi
edge_px = np.concatenate([
    a[:5, :, :].reshape(-1, 3), a[-5:, :, :].reshape(-1, 3),
    a[:, :5, :].reshape(-1, 3), a[:, -5:, :].reshape(-1, 3)])
bg = np.median(edge_px, axis=0)
dist = np.sqrt(((a - bg) ** 2).sum(axis=2))

# 2) ambang: Otsu pada jarak-ke-latar, dijepit [24, 128]
hist, _ = np.histogram(dist.ravel(), bins=256, range=(0, 256))
hist = hist.astype(float)
tot = hist.sum()
sum_all = (np.arange(256) * hist).sum()
sum_b, w_b, best, best_t = 0.0, 0.0, -1.0, 128.0
for t in range(256):
    w_b += hist[t]
    if w_b == 0 or w_b == tot:
        continue
    sum_b += t * hist[t]
    m_b = sum_b / w_b
    m_f = (sum_all - sum_b) / (tot - w_b)
    var = w_b * (tot - w_b) * (m_b - m_f) ** 2
    if var > best:
        best, best_t = var, float(t)
thr = float(np.clip(best_t, 24.0, 128.0))

# 3) flood-fill dari tepi (bagian yang terhubung tepi saja yang boleh transparan)
from collections import deque
bgmask = dist <= thr
visited = np.zeros_like(bgmask)
q = deque()
for x in range(W):
    for y in (0, H - 1):
        if bgmask[y, x] and not visited[y, x]:
            visited[y, x] = True; q.append((y, x))
for y in range(H):
    for x in (0, W - 1):
        if bgmask[y, x] and not visited[y, x]:
            visited[y, x] = True; q.append((y, x))
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < H and 0 <= nx < W and bgmask[ny, nx] and not visited[ny, nx]:
            visited[ny, nx] = True; q.append((ny, nx))
removed = visited  # True = akan transparan

# 4) halo anti-fringe: pixel transisi 1-2 px di batas dipudar linear
alpha = np.where(removed, 0, 255).astype(np.uint8)
dilate = removed.copy()
dilate[1:, :] |= removed[:-1, :]
dilate[:-1, :] |= removed[1:, :]
dilate[:, 1:] |= removed[:, :-1]
dilate[:, :-1] |= removed[:, 1:]
feather_band = dilate & (~removed)
soft = dist.copy()
soft = np.clip((soft - thr) / max(thr, 1.0), 0, 1)
alpha2 = np.where(removed, 0, np.where(feather_band,
                                       (soft * 255).astype(np.uint8), 255)).astype(np.uint8)

# 5) rakit RGBA + crop ke bbox isi
rgba = np.dstack([np.array(im), alpha2])
ys, xs = np.nonzero(alpha2 > 8)
bbox = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
out = Image.fromarray(rgba[bbox[1]:bbox[3], bbox[0]:bbox[2]], "RGBA")
out.save(OUT)

# 6) QA: checkerboard + latar gelap untuk melihat sisa kotak putih
def mount(bgcol, name):
    base = Image.new("RGBA", (W + 40, H + 40), bgcol)
    base.alpha_composite(out, (20, 20))
    base.convert("RGB").save(name)
mount((255, 255, 255, 255), "qa_white.png")
mount((34, 30, 26, 255), "qa_dark.png")

kept = int((alpha2 > 8).sum())
print(f"bg median RGB={bg.astype(int).tolist()} thr={thr:.1f}")
print(f"piksel dipertahankan: {kept} dari {H*W} ({100*kept/(H*W):.1f}%)")
print(f"bbox isi: {bbox} | out: {out.size} -> {OUT}")
