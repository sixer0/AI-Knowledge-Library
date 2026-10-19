# -*- coding: utf-8 -*-
"""Ekstraksi PDF brand-manual -> dossier mentah untuk design_master (SOP Imagegen 2.1 §13).

Peran: alat deterministik SAJA. Render halaman, hitung sha256, ukur luminansi +
dominan warna per halaman, kutip teks. Deskripsi desain (palet-nama, tipografi,
gaya panel, dsb) diisi AGENT lewat vision ke dossier.json, bukan oleh skrip ini.

Pakai:  python extract_pdf.py <file.pdf> <outdir> [--max-pages N] [--width 2200]
Output: <outdir>/manifest.json + <outdir>/pages/page_NN.png
"""
import argparse, hashlib, json, os, sys


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def measure(png):
    """Luminansi rata-rata + warna dominan (kuantil 8-bit) dari PNG halaman."""
    import numpy as np
    from PIL import Image
    im = Image.open(png).convert("RGB")
    a = np.asarray(im.resize((im.width // 4 or 1, im.height // 4 or 1)))
    lum = float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
    q = (a // 32 * 32).reshape(-1, 3)
    codes = q[:, 0].astype(int) * 65536 + q[:, 1].astype(int) * 256 + q[:, 2].astype(int)
    vals, counts = np.unique(codes, return_counts=True)
    top = []
    for v, c in sorted(zip(vals, counts), key=lambda t: -t[1])[:6]:
        r, g, b = (v >> 16) & 255, (v >> 8) & 255, v & 255
        top.append({"hex": "#%02X%02X%02X" % (r, g, b), "share_pct": round(100.0 * c / codes.size, 2)})
    return {"mean_luminance": round(lum, 1), "tone": "dark" if lum < 110 else ("light" if lum > 170 else "mid"),
            "dominant_colors": top}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("outdir")
    ap.add_argument("--max-pages", type=int, default=40)
    ap.add_argument("--width", type=int, default=2200)
    args = ap.parse_args()
    try:
        import pymupdf
    except ImportError:
        sys.exit("Butuh pymupdf: pip install pymupdf")
    pages_dir = os.path.join(args.outdir, "pages")
    os.makedirs(pages_dir, exist_ok=True)
    doc = pymupdf.open(args.pdf)
    man = {"file": os.path.abspath(args.pdf), "sha256": sha256(args.pdf),
           "pdf_pages": doc.page_count, "render_width": args.width, "pages": []}
    n = min(doc.page_count, args.max_pages)
    for i in range(n):
        page = doc[i]
        zoom = args.width / float(page.rect.width)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
        png = os.path.join(pages_dir, "page_%02d.png" % (i + 1))
        pix.save(png)
        text = page.get_text("text") or ""
        entry = {"page": i + 1, "png": png, "png_sha256": sha256(png),
                 "text_head": text[:400], "text_chars": len(text)}
        try:
            entry["measured"] = measure(png)
        except Exception as exc:  # pengukuran bukan gerbang keras
            entry["measured"] = {"error": str(exc)[:120]}
        man["pages"].append(entry)
        print("hal %d/%d -> %s (%s)" % (i + 1, n, png, entry.get("measured", {}).get("tone", "?")))
    out = os.path.join(args.outdir, "manifest.json")
    json.dump(man, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("MANIFEST:", out)


if __name__ == "__main__":
    main()
