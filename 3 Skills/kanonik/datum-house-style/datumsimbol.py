#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""datumsimbol.py — PUSTAKA SIMBOL GSP (registry datum-house-style v2.1.0, ENH-F).

Empat dialek baseline DATUM dalam geometri vektor SVG milimeter, token-driven:
  iec: 16 simbol listrik/daya (IEC 60617:2026 DB)      SIM-01..SIM-16
  isa: 12 simbol instrumentasi (ANSI/ISA-5.1-2024)     SIM-17..SIM-28
  sec: 7 legenda rumah keamanan GSP (tanpa standar)    SIM-29..SIM-35
  mil: 6 penanda MIL-STD-2525E (BASELINE-ONLY ber-flag) SIM-36..SIM-41

Normatif (makna, edisi, larangan-pakai, mark verifikasi) TIDAK diduplikasi di sini:
satu rumahnya katalog
  docs/2026-10-04-datum-manual/library/katalog-simbol.md (SIM-nn)
modul ini hanya memegang id, nama pendek, dan geometri. Palet dan wajah dibaca
runtime dari tokens.json (nol hex literal); lantai garis 0,18 mm dan huruf 5,5 pt
mengikuti LIMITS DATUM.

Perbaikan register 000 RevA yang ditutup modul ini:
  E-11  ID simbol ditulis dengan tanda hubung (isa:shared-field), bukan garis bawah
  E-18  lembar simbol dipagasi pada tinggi blok 247 mm, label tidak terpotong
  SM-03 lembar selalu mencetak kepala 'bukan simbol standar' untuk dialek house
  SM-04 satu lembar satu dialek (lint 35: lebih dari satu dialek per gambar cacat)

Panggilan kanonis:
  uv run --python 3.11 --no-project python datumsimbol.py --list
  uv run --python 3.11 --no-project python datumsimbol.py --dialect iec --sheet out.svg
  uv run --python 3.11 --no-project python datumsimbol.py --symbol iec:breaker --out s.svg
Exit: 0 OK | 2 salah pakai.
Provenans: ENH-F misi konsolidasi DATUM terpadu 08-10; geometri mengikuti deskripsi
katalog SIM-nn dan references/09 (bentuk konvensional, bukan salinan berkas berbayar;
SM-12: simbol standar berbayar dibeli, tidak disalin).
"""
import argparse
import json
import textwrap
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TOKENS_CANDIDATES = [
    os.environ.get("DATUM_TOKENS", ""),
    os.path.join(HERE, "tokens.json"),
    r"C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/datum-house-style/tokens.json",
]
TOKENS_PATH = next(p for p in TOKENS_CANDIDATES if p and os.path.isfile(p))
_TOK = json.load(open(TOKENS_PATH, encoding="utf-8"))
_C = _TOK["colour"]["interior"]
INK900 = _C["ink900"]; INK700 = _C["ink700"]; INK400 = _C["ink400"]
INK200 = _C["ink200"]; SIGNAL = _C["signal"]; ALERT = _C["alert"]
PAPER = _C["paper"]
GRID = _TOK["grid_mm"]
HAIR = 0.20          # mm, lantai fotokopi 0,18 + satu langkah (DT-11)
STROKE_W = 0.35      # mm, garis bentuk simbol
CELL = 24.0          # mm petak simbol
LABEL_PT = 6.0       # pt >= lantai 5,5 (DATUM-28)
BLOCK_H_MAX = float(GRID.get("text_column", 128)) * 1.93  # ~247 mm blok teks A4


# ------------------------------------------------------------------ geometri
def _g(x1, y1, x2, y2, col=INK900, w=STROKE_W, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
            'stroke-width="%s"%s/>' % (x1, y1, x2, y2, col, w, d))


def _r(x, y, wd, ht, col=INK900, w=STROKE_W, fill="none"):
    return ('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" stroke="%s" '
            'stroke-width="%s"/>' % (x, y, wd, ht, fill, col, w))


def _c(cx, cy, rad, col=INK900, w=STROKE_W, fill="none"):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" '
            'stroke-width="%s"/>' % (cx, cy, rad, fill, col, w))


def _p(pts, col=INK900, w=STROKE_W, fill="none"):
    s = " ".join("%s,%s" % (a, b) for a, b in pts)
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
        s, fill, col, w)


def _path(d, col=INK900, w=STROKE_W, fill="none"):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (d, fill, col, w)


def _lead(s):
    """Kaki sambungan standar di tengah tepi sel (s=arah: t/b/l/r)."""
    m = CELL / 2.0
    return {"t": _g(m, 0, m, 4, INK900, HAIR * 2),
            "b": _g(m, CELL - 4, m, CELL, INK900, HAIR * 2),
            "l": _g(0, m, 4, m, INK900, HAIR * 2),
            "r": _g(CELL - 4, m, CELL, m, INK900, HAIR * 2)}[s]


# ---- dialek iec --------------------------------------------------------------
def _iec_switch(cx, cy, cross="", coil=False, tick=False):
    """Keluarga sakelar: kontak berbilah terbuka; pembeda hanya tanda pada kontak.
    x = pemutus daya; tick = pemisah (ujung kontak bertanda tegak lurus, IEC);
    kotak = kontaktor; polos = sakelar umum."""
    parts = [_g(cx - 5, cy + 4, cx + 5, cy - 4, INK900, STROKE_W)]  # bilah terbuka
    parts.append(_c(cx - 5, cy + 4, 0.9, INK900, HAIR, PAPER))
    parts.append(_c(cx + 5, cy - 4, 0.9, INK900, HAIR, PAPER))
    if cross:  # x pemutus daya: klaim kemampuan putus arus gangguan
        parts.append(_g(cx - 2.2, cy - 2.2, cx + 2.2, cy + 2.2, INK900, HAIR * 1.5))
        parts.append(_g(cx - 2.2, cy + 2.2, cx + 2.2, cy - 2.2, INK900, HAIR * 1.5))
    if tick:   # pemisah: tanda pendek tegak lurus di ujung kontak tetap
        parts.append(_g(cx + 5, cy - 6.2, cx + 5, cy - 2.2, INK900, HAIR * 1.5))
    if coil:   # kontaktor: kotak kumparan penahan
        parts.append(_r(cx + 3, cy + 2, 4, 4, INK900, HAIR * 1.5))
    return parts


IEC = {
    "iec:breaker":    lambda: _lead("t") + _lead("b") + "".join(_iec_switch(12, 12, cross="x")),
    "iec:disconnector": lambda: _lead("t") + _lead("b") + "".join(_iec_switch(12, 12, tick=True)),
    "iec:contactor":  lambda: _lead("t") + _lead("b") + "".join(_iec_switch(12, 12, coil=True)),
    "iec:switch":     lambda: _lead("t") + _lead("b") + "".join(_iec_switch(12, 12)),
    "iec:changeover": lambda: (_lead("t") + _g(12, 4, 12, 12, INK900, STROKE_W)
                               + _g(12, 12, 7, 17, INK900, STROKE_W)
                               + _c(7, 17, 0.9, INK900, HAIR, PAPER)
                               + _c(17, 17, 0.9, INK900, HAIR, PAPER)
                               + _g(17, 17, 17, 20, INK900, HAIR * 2)),
    "iec:fuse":       lambda: (_lead("t") + _lead("b")
                               + _r(9, 7, 6, 10, INK900, STROKE_W)
                               + _g(12, 7, 12, 17, INK900, STROKE_W)),
    "iec:generator":  lambda: (_lead("l") + _lead("r")
                               + _c(12, 12, 6, INK900, STROKE_W)
                               + _path("M9.5 14.5 A3.5 3.5 0 0 1 9.5 9.5 M14.5 9.5 A3.5 3.5 0 0 1 14.5 14.5",
                                       INK900, HAIR * 1.5)),
    "iec:motor":      lambda: (_lead("l") + _lead("r")
                               + _c(12, 12, 6, INK900, STROKE_W)
                               + '<text x="12" y="14" font-family="IBM Plex Mono" font-size="5" fill="%s" text-anchor="middle">M</text>' % INK900),
    "iec:transformer": lambda: (_lead("l") + _lead("r")
                                + _c(9.5, 12, 3.4, INK900, STROKE_W)
                                + _c(14.5, 12, 3.4, INK900, STROKE_W)),
    "iec:ct":         lambda: (_lead("l") + _lead("r")
                               + _c(12, 12, 4.5, INK900, STROKE_W)
                               + _path("M8.5 12 A3.5 3.5 0 0 1 15.5 12", INK900, HAIR * 1.5)
                               + _g(12, 6.5, 12, 8, INK900, HAIR * 1.5)),
    "iec:arrester":   lambda: (_lead("t") + _lead("b")
                               + _r(9, 8, 6, 8, INK900, STROKE_W)
                               + _g(12, 8, 12, 13, INK900, STROKE_W)
                               + _p([(10.6, 13), (13.4, 13), (12, 15.4)], SIGNAL, HAIR * 1.5, fill=SIGNAL)),
    "iec:earth":      lambda: (_lead("t")
                               + _g(12, 8, 12, 13, INK900, STROKE_W)
                               + _g(6, 13, 18, 13, INK900, STROKE_W)
                               + _g(8.5, 15.5, 15.5, 15.5, INK900, STROKE_W)
                               + _g(11, 18, 13, 18, INK900, STROKE_W)),
    "iec:battery":    lambda: (_lead("l") + _lead("r")
                               + _g(10, 7, 10, 17, INK900, STROKE_W * 1.6)
                               + _g(12.5, 9, 12.5, 15, INK900, STROKE_W)
                               + _g(15, 7, 15, 17, INK900, STROKE_W * 1.6)
                               + _g(17.5, 9, 17.5, 15, INK900, STROKE_W)),
    "iec:lamp":       lambda: (_lead("l") + _lead("r")
                               + _c(12, 12, 5, INK900, STROKE_W)
                               + _g(8.5, 8.5, 15.5, 15.5, INK900, HAIR * 1.5)
                               + _g(8.5, 15.5, 15.5, 8.5, INK900, HAIR * 1.5)),
    "iec:busbar":     lambda: _g(4, 12, 20, 12, INK900, STROKE_W * 3),
    "iec:enclosure":  lambda: (_r(6, 8, 12, 8, INK900, STROKE_W)
                               + '<text x="12" y="13.2" font-family="IBM Plex Sans Condensed" font-size="4.5" fill="%s" text-anchor="middle">UPS</text>' % INK700),
}

# ---- dialek isa --------------------------------------------------------------
def _isa_bubble(shape="circle", lines=0, inner=""):
    m = 12
    parts = []
    if shape == "circle":
        parts.append(_c(m, m, 6, INK900, STROKE_W))
    elif shape == "hex":
        pts = [(m + 6 * (1 if a in (0, 3) else 0.5), m + (0 if a in (1, 2) else 5.2 * (-1 if a < 2 else 1)))
               for a in range(4)]
        pts = [(m - 3, m - 5.2), (m + 3, m - 5.2), (m + 6, m), (m + 3, m + 5.2),
               (m - 3, m + 5.2), (m - 6, m)]
        parts.append(_p(pts, INK900, STROKE_W))
    elif shape == "sq-circle":
        parts.append(_r(m - 6, m - 6, 12, 12, INK900, STROKE_W))
        parts.append(_c(m, m, 6, INK900, STROKE_W))
    if lines == 1:
        parts.append(_g(m - 6, m + 2.5, m + 6, m + 2.5, INK900, HAIR * 1.5))
    if lines == 2:
        parts.append(_g(m - 6, m + 1.5, m + 6, m + 1.5, INK900, HAIR * 1.5))
        parts.append(_g(m - 6, m + 3.5, m + 6, m + 3.5, INK900, HAIR * 1.5))
    if lines == "dash":
        parts.append(_g(m - 6, m + 2.5, m + 6, m + 2.5, INK900, HAIR * 1.5, "1.2,1"))
    if inner:
        parts.append(inner)
    return "".join(parts)


def _valve(actuator=""):
    m = 12
    body = (_p([(m - 5, m - 4.5), (m - 5, m + 4.5), (m, m)], INK900, STROKE_W)
            + _p([(m + 5, m - 4.5), (m + 5, m + 4.5), (m, m)], INK900, STROKE_W))
    stem = _g(m, m - 3, m, m - 6.5, INK900, STROKE_W)
    if actuator == "diaphragm":
        cap = _path("M%s %s A5 5 0 0 1 %s %s" % (m - 5, m - 6.5, m + 5, m - 6.5), INK900, STROKE_W)
        return body + stem + cap
    if actuator == "motor":
        return body + stem + _c(m, m - 9, 2.6, INK900, HAIR * 1.5) + \
            '<text x="%s" y="%s" font-family="IBM Plex Mono" font-size="3.6" fill="%s" text-anchor="middle">M</text>' % (m, m - 8, INK900)
    if actuator == "solenoid":
        return body + stem + _r(m - 3, m - 11.5, 6, 3, INK900, HAIR * 1.5)
    return body + stem


ISA = {
    "isa:field":          lambda: _isa_bubble("circle", 0),
    "isa:primary":        lambda: _isa_bubble("circle", 1),
    "isa:auxiliary":      lambda: _isa_bubble("circle", 2),
    "isa:inaccessible":   lambda: _isa_bubble("circle", "dash"),
    "isa:shared":         lambda: _isa_bubble("sq-circle", 0),
    "isa:shared-field":   lambda: _isa_bubble("sq-circle", 1),
    "isa:computer":       lambda: _isa_bubble("hex", 0),
    "isa:plc":            lambda: _isa_bubble("circle", 0,
                                              _r(9, 9, 6, 6, INK900, HAIR * 1.5)),
    "isa:valve":          lambda: _valve(""),
    "isa:valve-diaphragm": lambda: _valve("diaphragm"),
    "isa:valve-motor":    lambda: _valve("motor"),
    "isa:valve-solenoid": lambda: _valve("solenoid"),
}

# ---- dialek sec (legenda rumah; SM-03 wajib kepala bukan-standar) -----------
def _cone():
    return _p([(12, 12), (20, 6), (20, 18)], SIGNAL, HAIR * 1.5, fill=SIGNAL) + \
        '<text x="13.4" y="8.4" font-family="IBM Plex Mono" font-size="3.4" fill="%s">FOV</text>' % INK900


SEC = {
    "sec:camera":  lambda: _c(12, 12, 2.6, INK900, STROKE_W, PAPER) + _cone(),
    "sec:ptz":     lambda: (_c(12, 12, 2.6, INK900, STROKE_W, PAPER) + _cone()
                            + _g(9.4, 12, 14.6, 12, INK900, HAIR * 1.5)
                            + _g(12, 9.4, 12, 14.6, INK900, HAIR * 1.5)),
    "sec:pir":     lambda: (_path("M8 16 A6 6 0 0 1 16 16", INK900, STROKE_W)
                            + _path("M9.6 16 A3.2 3.2 0 0 1 14.4 16", INK900, HAIR * 1.5)
                            + _c(12, 16, 1.1, INK900, HAIR, PAPER)),
    "sec:fence":   lambda: (_g(6, 16, 18, 8, INK900, STROKE_W)
                            + _g(8, 17, 10, 15, INK900, HAIR * 1.5)
                            + _g(12, 13, 14, 11, INK900, HAIR * 1.5)
                            + _g(16, 9, 18, 7, INK900, HAIR * 1.5)),
    "sec:reader":  lambda: (_r(8, 9, 8, 6, INK900, STROKE_W)
                            + _g(12, 15, 12, 18, INK900, HAIR * 1.5)
                            + _g(9, 18, 15, 18, INK900, HAIR * 1.5)),
    "sec:barrier": lambda: (_r(6, 10, 2.4, 8, INK900, HAIR * 1.5)
                            + _g(8.4, 11, 19, 8.4, ALERT, STROKE_W * 1.4)
                            + _g(11, 10.2, 12.2, 8.6, ALERT, HAIR * 1.5)
                            + _g(14, 9.4, 15.2, 7.9, ALERT, HAIR * 1.5)),
    "sec:mast":    lambda: (_g(12, 19, 12, 6, INK900, STROKE_W)
                            + _g(10, 19, 14, 19, INK900, HAIR * 1.5)
                            + _g(12, 6, 16, 6, INK900, HAIR * 1.5)
                            + _c(16.6, 6.6, 1.1, INK900, HAIR, PAPER)),
}

# ---- dialek mil --------------------------------------------------------------
def _mil_frame(kind):
    m = 12
    if kind == "rect":      # kawan darat
        return _r(5, 8, 14, 8, INK900, STROKE_W)
    if kind == "diamond":   # lawan darat
        return _p([(m, 5.5), (18.5, 12), (m, 18.5), (5.5, 12)], INK900, STROKE_W)
    if kind == "square":    # netral darat
        return _r(6.5, 6.5, 11, 11, INK900, STROKE_W)
    if kind == "quatrefoil":  # tak dikenal: empat lingkaran bersatu (E-19: bukan terpisah)
        return (_c(10.4, 10.4, 3.2, INK900, STROKE_W) + _c(13.6, 10.4, 3.2, INK900, STROKE_W)
                + _c(10.4, 13.6, 3.2, INK900, STROKE_W) + _c(13.6, 13.6, 3.2, INK900, STROKE_W))
    if kind == "dome":      # kawan udara
        return _path("M6 18 A6 6 0 0 1 18 18", INK900, STROKE_W)
    if kind == "arch":      # lawan udara: pointed arch, dua busur bertemu di puncak
        return _path("M6 18 L6 12.5 A8.5 8.5 0 0 1 12 6 A8.5 8.5 0 0 1 18 12.5 L18 18",
                     INK900, STROKE_W)
    raise ValueError(kind)


MIL = {
    "mil:friend":      lambda: _mil_frame("rect"),
    "mil:hostile":     lambda: _mil_frame("diamond"),
    "mil:neutral":     lambda: _mil_frame("square"),
    "mil:unknown":     lambda: _mil_frame("quatrefoil"),
    "mil:friend-air":  lambda: _mil_frame("dome"),
    "mil:hostile-air": lambda: _mil_frame("arch"),
}

DIALECTS = {"iec": IEC, "isa": ISA, "sec": SEC, "mil": MIL}

HOUSE_NOTE = ("Legenda rumah GSP: BUKAN simbol standar. Wajib tercetak pada lembar "
              "yang sama dengan gambarnya (SM-03, cek 34).")
MIL_NOTE = ("MIL-STD-2525E BASELINE-ONLY ber-flag: cocokkan ke dokumen NATO sebelum "
            "terbit konstruksi (SM-11, putusan R-10).")
ISA_NOTE = ("Bentuk sama dengan fungsi; garis sama dengan lokasi (ISA-5.1-2024, "
            "putusan R-08). Simbol berbayar tidak disalin (SM-12).")
IEC_NOTE = ("Geometri mengikuti IEC 60617:2026 DB. Sebelum terbit konstruksi, cocokkan "
            "setiap simbol ke entri basis data (SM-11).")
NOTES = {"iec": IEC_NOTE, "isa": ISA_NOTE, "sec": HOUSE_NOTE, "mil": MIL_NOTE}


def symbol_svg(sid):
    prefix = sid.split(":")[0]
    lib = DIALECTS.get(prefix)
    if not lib or sid not in lib:
        raise KeyError(sid)
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%smm" height="%smm" '
            'viewBox="0 0 %s %s">%s</svg>' % (CELL, CELL, CELL, CELL, lib[sid]()))


def _label(text, x, y, size=LABEL_PT, color=INK700, anchor="start", bold=False):
    fam = "IBM Plex Sans Condensed"
    w = ' font-weight="600"' if bold else ""
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" '
            'text-anchor="%s"%s>%s</text>' % (x, y, fam, size, color, anchor, w, text))


def sheet_svg(dialect, cols=3):
    """Lembar satu dialek: kepala + petak dengan label DI BAWAH (tidak pernah
    menabrak kolom tetangga), dipagasi pada blok teks 247 mm (E-18 ditutup)."""
    lib = DIALECTS[dialect]
    ids = sorted(lib)
    W = 166.0
    col_w = (W - 8.0) / cols
    cell_h = CELL + 10.0         # petak 24 + dua baris label di bawahnya
    head_h = 18.0
    page_h = 247.0
    per_page = max(1, int((page_h - head_h - 12) // cell_h))
    chunks = [ids[i:i + per_page * cols] for i in range(0, len(ids), per_page * cols)]
    pages = []
    for pi, chunk in enumerate(chunks):
        parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="%smm" height="%smm" '
                 'viewBox="0 0 %s %s">' % (W, page_h, W, page_h)]
        parts.append('<rect x="0" y="0" width="%s" height="%s" fill="%s"/>' % (W, page_h, PAPER))
        parts.append(_label("PUSTAKA SIMBOL %s LEMBAR %d/%d" % (dialect.upper(), pi + 1, len(chunks)),
                            4, 6, LABEL_PT + 1.0, INK900, bold=True))
        parts.append(_g(4, 8, W - 4, 8, INK200, HAIR))
        # pemotongan berbasis kata, 56 karakter/baris (cadang: font pengganti
        # lebih lebar dari Condensed; uji render 08-10 menangkap potong kata)
        for li, ln in enumerate(textwrap.wrap(NOTES[dialect], 56)[:2]):
            parts.append(_label(ln, 4, 12 + li * 3.6, LABEL_PT - 0.5, INK400))
        for j, sid in enumerate(chunk):
            r, cidx = divmod(j, cols)
            ox = 4 + cidx * col_w
            oy = head_h + r * cell_h
            cx = ox + (col_w - CELL) / 2.0
            parts.append('<g transform="translate(%s,%s)">' % (round(ox, 2), round(oy, 2)))
            parts.append(_r(round((col_w - CELL) / 2.0, 2), 0, CELL, CELL, INK200, HAIR))
            parts.append('<g transform="translate(%s,0)">%s</g>'
                         % (round((col_w - CELL) / 2.0, 2), lib[sid]()))
            lx = round(col_w / 2.0, 2)
            parts.append(_label(sid, lx, CELL + 4, LABEL_PT, INK900, anchor="middle", bold=True))
            parts.append(_label("geometri konvensional", lx, CELL + 7.6, LABEL_PT - 1,
                                INK400, anchor="middle"))
            parts.append('</g>')
        parts.append(_label("SUMBER katalog-simbol.md SIM-nn · datumsimbol.py v1.0",
                            4, page_h - 4, LABEL_PT - 1, INK400))
        parts.append('</svg>')
        pages.append("".join(parts))
    return pages


def main():
    ap = argparse.ArgumentParser(description="Pustaka simbol DATUM (ENH-F)")
    ap.add_argument("--list", action="store_true", help="daftar id simbol semua dialek")
    ap.add_argument("--dialect", choices=sorted(DIALECTS), help="satu dialek untuk lembar")
    ap.add_argument("--sheet", metavar="OUT.svg", help="tulis lembar simbol (multi-halaman: OUT-1.svg ...)")
    ap.add_argument("--symbol", help="satu id penuh, mis. iec:breaker")
    ap.add_argument("--out", metavar="OUT.svg", help="tujuan satu simbol")
    a = ap.parse_args()
    if a.list:
        n = 0
        for d in sorted(DIALECTS):
            for sid in sorted(DIALECTS[d]):
                print(sid); n += 1
        print("TOTAL %d simbol · %s dialek" % (n, len(DIALECTS)))
        return 0
    if a.sheet:
        if not a.dialect:
            print("SALAH PAKAI: --sheet butuh --dialect (satu lembar satu dialek, SM-04)", file=sys.stderr)
            return 2
        pages = sheet_svg(a.dialect)
        base, ext = os.path.splitext(a.sheet)
        for i, svg in enumerate(pages, 1):
            path = a.sheet if len(pages) == 1 else "%s-%d%s" % (base, i, ext)
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            print("LEMBAR %s" % path)
        print("TOTAL %d halaman lembar (blok maks 247 mm, E-18 ditutup)" % len(pages))
        return 0
    if a.symbol:
        try:
            svg = symbol_svg(a.symbol)
        except KeyError:
            print("SIMBOL TIDAK DIKENAL: %s (lihat --list)" % a.symbol, file=sys.stderr)
            return 2
        if a.out:
            open(a.out, "w", encoding="utf-8").write(svg)
            print("TULIS %s" % a.out)
        else:
            print(svg)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
