"""QA dua-latar untuk aset RGBA: tempel di putih + gelap, cek sisa kotak/fringe/lubang."""
import sys
import numpy as np
from PIL import Image

SRC = sys.argv[1]
im = Image.open(SRC).convert("RGBA")
w, h = im.size
for name, col in (("qa_white.png", (255, 255, 255, 255)), ("qa_dark.png", (34, 30, 26, 255))):
    base = Image.new("RGBA", (w + 40, h + 40), col)
    base.alpha_composite(im, (20, 20))
    base.convert("RGB").save(name)

a = np.array(im)[..., 3]
full = int((a == 255).sum()); zero = int((a == 0).sum()); soft = int(((a > 0) & (a < 255)).sum())
print(f"alpha: fully-opaque={full} fully-transparent={zero} feather={soft} total={a.size}")
# tepi frame terluar isi harus menempel transparansi (tanda bbox sudah pas)
ys, xs = np.nonzero(a > 8)
top_ok = a[ys.min(), xs.min():xs.max()+1].min() <= 8
print("bbox rapat ke isi:", bool(top_ok))
print("saved qa_white.png qa_dark.png")
