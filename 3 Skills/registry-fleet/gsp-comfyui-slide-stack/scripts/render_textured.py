# -*- coding: utf-8 -*-
"""Render GLB multi-sudut DENGAN tekstur (sampling UV per-face) -> PNG untuk penilaian."""
import sys, numpy as np, trimesh
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image

glb, out = sys.argv[1], sys.argv[2]
views = eval(sys.argv[3]) if len(sys.argv) > 3 else [(15,-70),(25,110),(60,30),(0,0)]
m = trimesh.load(glb, force="mesh")
V, F = m.vertices, m.faces
# warna per-face dari tekstur UV
fc = None
try:
    vis = m.visual
    uv = getattr(vis, "uv", None)
    mat = getattr(vis, "material", None)
    img = getattr(mat, "image", None) or getattr(mat, "baseColorTexture", None)
    if uv is not None and img is not None:
        img = img.convert("RGB")
        W, H = img.size
        px = np.asarray(img)
        fu = uv[F].mean(axis=1)
        xs = np.clip((fu[:,0] * (W-1)).astype(int), 0, W-1)
        ys = np.clip(((1-fu[:,1]) * (H-1)).astype(int), 0, H-1)
        fc = px[ys, xs] / 255.0
        print("tekstur OK:", len(fc), "face colors")
except Exception as e:
    print("tekstur gagal:", e)
if fc is None:
    fc = np.full((len(F),3), 0.62)

n = len(views)
fig = plt.figure(figsize=(6*n, 6), dpi=110)
for i,(elev,azim) in enumerate(views,1):
    ax = fig.add_subplot(1,n,i,projection="3d")
    pc = Poly3DCollection(V[F], facecolors=fc, edgecolors="none")
    ax.add_collection3d(pc)
    c = V.mean(0); r = (V.max(0)-V.min(0)).max()*0.62
    ax.set_xlim(c[0]-r,c[0]+r); ax.set_ylim(c[1]-r,c[1]+r); ax.set_zlim(c[2]-r,c[2]+r)
    ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
    ax.set_title(f"elev{elev} azim{azim}")
plt.tight_layout(); plt.savefig(out, bbox_inches="tight", facecolor="white")
print("verts:", len(V), "faces:", len(F), "->", out)
