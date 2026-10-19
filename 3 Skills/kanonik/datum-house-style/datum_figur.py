#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""datum_figur.py — baterai figur ENH-E: gerbang mutu gambar pada berkas PDF terbit.

Mengukur objek TERBIT (pymupdf), bukan klaim builder. Empat pemeriksaan per halaman:
  F1 overflow  : bingkai gambar badan keluar zona teks (x1 > lebar-15pt atau x0 < 20pt)
  F2 caption   : blok teks terdekat <= 40 pt di bawah bingkai, overlap horisontal; target 100%
  F3 overlap   : kata teks (level kata, bukan blok) menimpa bingkai gambar; nol toleransi
                 (area > 1 pt persegi per kata dihitung; preseden EOSADINT RevB 08-10)
  F4 void      : halaman berfigur dengan konten terbawah > 25% tinggi di atas pita kaki;
                 boleh dikecualikan per halaman lewat --allow-void 1,4,9

Sensor ditambal dari lesson repro 08-10: dedup gambar per (xref, halaman), skip ikon
rambut (lebar < 57 pt ~ 20 mm) dan latar full-page, pita kepala/kaki dibuang dari badan.

Panggilan:
  uv run --python 3.11 --with pymupdf python datum_figur.py BERKAS.pdf [--json]
      [--allow-void 46,57]
Exit: 0 bersih | 1 cacat | 2 berkas tak terbaca / salah pakai.
Provenans: ENH-E misi konsolidasi DATUM terpadu 08-10 (kartu user langsung);
fixture merah = EOSADINT-LAP-1007-RevB (3 halaman overlap), hijau = katalog VCTL
(caption 75/75) dan repro pasca-tambal ENH-C.
"""
import argparse
import json
import sys

try:
    import pymupdf
except ImportError:
    print("pymupdf tidak tersedia: jalankan lewat uv --with pymupdf", file=sys.stderr)
    sys.exit(2)

HEADER_Y1 = 70.0      # pt: blok dengan y1 < ini = kepala halaman
FOOTER_TOP = 60.0     # pt: blok dengan y0 > H-60 = kaki halaman
MIN_IMG_W = 57.0      # pt (~20 mm): di bawah ini = ikon/garis rambut, bukan figur
MIN_IMG_H = 23.0      # pt (~8 mm): garis rambut horizontal/vertikal chrome halaman
CAPTION_MAX_GAP = 40.0
WORD_AREA_MIN = 1.0   # pt^2: serpihan di bawah ini = sentuhan antialiasing
COVER_PAGES_DEFAULT = "1"  # DT-14: logo sampul bukan figur; caption/void tak ditagih,
                            # overflow tetap dihitung (kalibrasi VCTL 08-10)


def _body_images(page, seen, px_map=None):
    out = []
    for im in page.get_images(full=True):
        xref = im[0]
        if xref in seen:
            continue
        seen.add(xref)
        if px_map is not None:
            px_map.setdefault(xref, (im[2], im[3]))
        try:
            r = page.get_image_bbox(im)
        except Exception:
            continue
        if r.is_empty or r.width < MIN_IMG_W or r.height < MIN_IMG_H:
            continue
        if r.width > page.rect.width - 20 and r.height > page.rect.height - 20:
            continue  # latar full-page
        out.append((xref, r))
    return out


def _body_blocks(page):
    return [b for b in page.get_text("blocks")
            if b[6] != 1 and b[1] > HEADER_Y1 and b[3] < page.rect.y1 - FOOTER_TOP]


def battery(pdf_path, allow_void=(), cover_pages=(1,)):
    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        return None, "berkas tak terbaca: %s" % e
    allow = set(allow_void)
    res = {"pages": doc.page_count, "figures": 0,
           "overflow_pages": [], "caption_ok": 0, "caption_total": 0,
           "caption_missing_pages": [], "overlap": [], "void_pages": [],
           "lowres": []}
    seen_global = set()
    px_map = {}  # xref -> (px_w, px_h) untuk F5 (ENH-D E-08)
    for pno in range(doc.page_count):
        page = doc[pno]
        pr = page.rect
        imgs = _body_images(page, seen_global, px_map)
        if not imgs:
            continue
        res["figures"] += len(imgs)
        body = _body_blocks(page)
        words = [(pymupdf.Rect(w[:4]), w[4]) for w in page.get_text("words")]
        low = max([b[3] for b in body] or [0])
        is_cover = (pno + 1) in cover_pages  # DT-14: logo sampul bukan figur
        for xref, ib in imgs:
            if ib.x1 > pr.x1 - 15 or ib.x0 < 20:
                res["overflow_pages"].append(pno + 1)
            # F5 (ENH-D E-08): resolusi efektif px per inci cetak; lantai 150 dpi.
            px_w = px_map.get(xref, (None, None))[0]
            if px_w:
                eff_dpi = px_w / (ib.width / 72.0)
                if eff_dpi < 150.0:
                    res["lowres"].append({"page": pno + 1, "xref": xref,
                                          "eff_dpi": round(eff_dpi)})
            if not is_cover:
                below = [b for b in body
                         if 0 <= b[1] - ib.y1 <= CAPTION_MAX_GAP
                         and b[0] < ib.x1 and b[2] > ib.x0]
                res["caption_total"] += 1
                if below:
                    res["caption_ok"] += 1
                elif (pno + 1) not in res["caption_missing_pages"]:
                    res["caption_missing_pages"].append(pno + 1)
            bad = []
            for wr, txt in words:
                inter = wr.intersect(ib)
                if not inter.is_empty and inter.get_area() > WORD_AREA_MIN \
                        and wr.y0 < ib.y1 - 1:
                    bad.append(txt)
            if bad:
                res["overlap"].append({"page": pno + 1, "xref": xref,
                                       "words": len(bad),
                                       "sample": bad[:5]})
            low = max(low, ib.y1)
        if low and not is_cover and (pr.y1 - FOOTER_TOP) - low > 0.25 * pr.height:
            if (pno + 1) not in allow:
                res["void_pages"].append(pno + 1)
    doc.close()
    res["overflow_pages"] = sorted(set(res["overflow_pages"]))
    defects = (len(res["overflow_pages"])
               + (res["caption_total"] - res["caption_ok"])
               + len(res["overlap"]) + len(res["void_pages"])
               + len(res["lowres"]))
    res["defects"] = defects
    return res, None


def main():
    ap = argparse.ArgumentParser(description="Baterai figur ENH-E untuk PDF terbit")
    ap.add_argument("pdf")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--allow-void", default="",
                    help="daftar halaman berfigur yang void-nya dideklarasikan, mis. 46,57")
    ap.add_argument("--cover-pages", default=COVER_PAGES_DEFAULT,
                    help="halaman chrome tanpa kewajiban caption/void (default: 1)")
    a = ap.parse_args()
    allow = [int(x) for x in a.allow_void.split(",") if x.strip()]
    covers = tuple(int(x) for x in a.cover_pages.split(",") if x.strip())
    res, err = battery(a.pdf, allow, covers)
    if err:
        print("SALAH PAKAI:", err, file=sys.stderr)
        sys.exit(2)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print("halaman=%d figur=%d" % (res["pages"], res["figures"]))
        print("F1 overflow      : %s" % (res["overflow_pages"] or "bersih"))
        print("F2 caption       : %d/%d %s" % (res["caption_ok"], res["caption_total"],
              ("bersih" if res["caption_ok"] == res["caption_total"]
               else "HILANG di hlm %s" % res["caption_missing_pages"])))
        print("F3 overlap kata  : %s" % ("bersih" if not res["overlap"]
              else "; ".join("hlm %d xref %d (%d kata)" % (o["page"], o["xref"], o["words"])
                             for o in res["overlap"])))
        print("F4 void          : %s" % (res["void_pages"] or "bersih"))
        print("F5 lowres(E-08)  : %s" % (res["lowres"] or "bersih"))
        print("DEFECTS=%d -> %s" % (res["defects"], "PASS" if res["defects"] == 0 else "FAIL"))
    sys.exit(0 if res["defects"] == 0 else 1)


if __name__ == "__main__":
    main()
