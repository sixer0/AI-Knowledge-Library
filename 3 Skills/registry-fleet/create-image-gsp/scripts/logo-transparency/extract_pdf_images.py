"""Ekstraksi citra tertanam dari PDF (jalur cepat cek alpha bawaan).

Pakai: python extract_pdf_images.py <pdf> <outdir> [min_px=64] [max=25]
Berguna untuk tahap 0 rantai transparan: bila pix.alpha > 0, citra sudah
transparan asli dan crop tak diperlukan.
"""
import os
import sys

import pymupdf  # uv run --with pymupdf

if len(sys.argv) < 3:
    raise SystemExit("pakai: extract_pdf_images.py <pdf> <outdir> [min_px] [max]")
PDF, OUT = sys.argv[1], sys.argv[2]
MIN_PX = int(sys.argv[3]) if len(sys.argv) > 3 else 64
MAX_N = int(sys.argv[4]) if len(sys.argv) > 4 else 25

os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)
print("pages:", len(doc))
seen, n = set(), 0
for pno in range(len(doc)):
    for img in doc[pno].get_images(full=True):
        xref = img[0]
        if xref in seen:
            continue
        seen.add(xref)
        pix = pymupdf.Pixmap(doc, xref)
        w, h = pix.width, pix.height
        if w < MIN_PX or h < MIN_PX:
            continue
        tag = "ALPHA" if pix.alpha else "OPAQUE"
        if pix.n - pix.alpha >= 4:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        name = f"{OUT}/p{pno+1:03d}_x{xref}_w{w}_h{h}_{tag}.png"
        pix.save(name)
        n += 1
        print(name)
        if n >= MAX_N:
            raise SystemExit(f"stop {MAX_N}")
print("total:", n)
