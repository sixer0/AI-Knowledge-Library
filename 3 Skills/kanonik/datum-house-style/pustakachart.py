# -*- coding: utf-8 -*-
"""pustakachart.py — PUSTAKA CHART GSP (registry datum-house-style v2.1.0, ENH-A).

Render deterministik galeri chart katalog VCTL-1007 (99 entri VC, keluarga
bar/column/threshold/komposisi/sebaran/hubungan/geospasial/aliran/kinerja)
dalam palet dan tipografi DATUM. Dipromosikan dari
docs/2026-10-07-vctl-chart-catalog/scripts/render_chart_examples.py rev0
tanpa mengubah resep gambar; nama modul mengikuti DT-12 (tanpa garis bawah).

Aturan mengikat (warisan CONTRACT VCTL D-03 + gerbang G-REND-1 + ENH-E):
- Palet & ground DIBACA RUNTIME dari tokens.json; nol hex hardcoded; navy+gold
  haram (retired di tokens).
- Kanvas HANYA 128 mm atau 166 mm (grid_mm DATUM), PNG 300 dpi.
- Data dari pustakachart_data.py (sintetis, seed beku 42); tiap berkas berlabel
  'CONTOH DATA SINTETIS' pada footer gambar + caption manifest.
- Deterministik: tanpa timestamp PNG (metadata dibuang), rcParams beku, seed
  tunggal. Dua run berurutan WAJIB byte-identik (gerbang promosi 08-10).
- Teks terkecil diukur per figur (pt dan px @300 dpi) dan dilaporkan di
  manifest; lantai 5,5 pt (DATUM-28) ditagih pemakai lewat --check-min-pt.
- Blok warisan datum_chart_buku.py bersifat OPSIONAL: dilewati dengan catatan
  manifest bila toolkit misi tidak ada di disk.

Panggilan kanonis:
  C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 --no-project \
    --with matplotlib --with numpy python pustakachart.py --out <dir> [--check-min-pt]
Exit: 0 bersih | 1 teks terkecil di bawah lantai (saat --check-min-pt) | 2 salah pakai.
"""
import argparse
import datetime as _dt
import glob
import hashlib
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.text
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle, Polygon, FancyArrow

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pustakachart_data as D  # noqa: E402

# ---------------- TOKENS RUNTIME (nol hex literal) ----------------
TOKENS_CANDIDATES = [
    os.environ.get("DATUM_TOKENS", ""),
    r"C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/datum-house-style/tokens.json",
    r"C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp/datum-house-style/tokens.json",
]
TOKENS_PATH = next(p for p in TOKENS_CANDIDATES if p and os.path.isfile(p))
_TOK = json.load(open(TOKENS_PATH, encoding="utf-8"))
_C = _TOK["colour"]["interior"]
_G = _TOK["grid_mm"]
_F = _TOK["type"]["faces"]

PAPER = _C["paper"]; INK900 = _C["ink900"]; INK700 = _C["ink700"]
INK400 = _C["ink400"]; INK200 = _C["ink200"]; INK100 = _C["ink100"]
SIGNAL = _C["signal"]; ALERT = _C["alert"]; VERD = _C["verd"]
W128 = float(_G["text_column"])   # 128 mm (satuan mm; canvas() yang mengonversi)
W166 = float(_G["full_span"])     # 166 mm
DPI = 300
SEED = D.SEED
CAPTION_LABEL = "CONTOH DATA SINTETIS"

# ---------------- FONT (fallback-safe, dicatat) ----------------
def init_fonts():
    dirs = ["C:/Windows/Fonts",
            os.path.expandvars(r"%LOCALAPPDATA%/Microsoft/Windows/Fonts")]
    added = []
    for d in dirs:
        for p in glob.glob(os.path.join(d, "IBM_Plex*.ttf")) + \
                 glob.glob(os.path.join(d, "IBMPlex*.ttf")):
            try:
                fm.fontManager.addfont(p); added.append(os.path.basename(p))
            except Exception:
                pass
    avail = {f.name for f in fm.fontManager.ttflist}

    def pick(*chain):
        for x in chain:
            if x in avail:
                return x
        return "DejaVu Sans"

    struct = pick(_F["condensed"], "IBM Plex Sans Condensed",
                  "Segoe UI Semibold", "Segoe UI")
    read = pick(_F["serif"], "Georgia")
    mono = pick(_F["mono"], "Consolas")
    sans = pick(_F["workbook_ui"], "Segoe UI")
    # rantai fallback (mpl>=3.6): nama terpilih + padanan Windows + DejaVu
    chains = ([struct, "Segoe UI Semibold", "Segoe UI", "DejaVu Sans"],
              [read, "Georgia", "DejaVu Serif"],
              [mono, "Consolas", "DejaVu Sans Mono"],
              [sans, "Segoe UI", "DejaVu Sans"])
    return chains[0], chains[1], chains[2], chains[3], sorted(set(added)), chains

STRUCT, READ, MONO, SANS, FONTS_ADDED, FONT_CHAINS = init_fonts()
GLIF = "DejaVu Sans"  # putusan R-14: ■□ di luar cakupan IBM Plex; DejaVu ada di semua host

plt.rcParams.update({
    "font.family": SANS, "font.size": 7.0,
    "axes.edgecolor": INK400, "axes.labelcolor": INK700,
    "text.color": INK700, "xtick.color": INK400, "ytick.color": INK400,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.6, "figure.facecolor": PAPER, "axes.facecolor": PAPER,
    "savefig.facecolor": PAPER, "savefig.pad_inches": 0.03,
    "svg.fonttype": "none",
})
RAMP = LinearSegmentedColormap.from_list("datum_seq", [PAPER, INK200, INK400, INK900])
CAT_SERIES = [INK900, SIGNAL, VERD, INK400, ALERT]  # maks 5 warna/figur (E-16)

# ---------------- KERANGKA FIGUR ----------------
def canvas(width_mm, height_mm):
    assert min(abs(width_mm - w) for w in (W128, W166)) < 0.06, \
        "lebar %s mm bukan 128/166" % width_mm
    fig = plt.figure(figsize=(width_mm / 25.4, height_mm / 25.4))
    return fig

def _is_number(s):
    t = s.replace(",", "").replace("%", "").replace(" ", "")
    try:
        float(t)
        return True
    except ValueError:
        return False

def style_ax(ax, grid_axis=None):
    if grid_axis:
        ax.grid(axis=grid_axis, color=INK200, lw=0.4, zorder=0)
    for t in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
        t.set_fontsize(6.5)
        if _is_number(t.get_text()):      # peran data DATUM: angka pakai mono
            t.set_fontfamily(MONO)
    ax.tick_params(length=0)

def finish(fig, out_png, title, footer_extra=""):
    """Judul di LUAR plot (tanpa judul-dalam-plot); footer label sintetis.
    Footer ditaruh di bawah tepi kanvas (y negatif) agar bbox_inches='tight'
    memperluas kanvas dan tidak tabrakan dengan xlabel."""
    fig.text(0.01, 0.985, title, fontsize=8.0, color=INK900, fontweight="bold",
             fontfamily=STRUCT, va="top")
    fig.text(0.01, -0.075, "%s - seed %d | pustakachart_data.py (VCTL-1007 C2)%s"
             % (CAPTION_LABEL, SEED, (" | " + footer_extra) if footer_extra else ""),
             fontsize=6.0, color=INK400, fontfamily=MONO, va="bottom")
    fig.canvas.draw()
    min_pt = measure_min_pt(fig)
    fig.savefig(out_png, dpi=DPI, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)
    return min_pt

def measure_min_pt(fig):
    """Ukuran teks TERKECIL yang benar-benar tampil (point)."""
    sizes = []
    for t in fig.findobj(matplotlib.text.Text):
        try:
            if t.get_text().strip() and t.get_visible():
                sizes.append(t.get_fontsize())
        except Exception:
            pass
    return min(sizes) if sizes else 0.0

def mono_label(ax, x, y, s, **kw):
    kw.setdefault("fontsize", 6.5); kw.setdefault("color", INK700)
    kw.setdefault("fontfamily", MONO)
    return ax.text(x, y, s, **kw)

# =================================================================
# PENGGAMBAR PER ENTRI - masing-masing mengembalikan min_pt setelah
# menyimpan PNG ke jalur out_png.
# =================================================================
fn_ax = [None]; fn_grid = [None]

def _save(fig, fn, out_png, title, w_mm, extra=""):
    if fn_ax[0] is not None:
        style_ax(fn_ax[0], grid_axis=fn_grid[0])
    return finish(fig, out_png, title, extra)

# registry diisi lewat dekorator sederhana
REGISTRY = []

def entry(id_, nama, kelas, lebar_mm, tinggi_mm, resep, caption, fn):
    REGISTRY.append(dict(id=id_, nama=nama, kelas=kelas, lebar_mm=lebar_mm,
                         tinggi_mm=tinggi_mm, resep=resep, caption=caption, fn=fn))

# ---------- K1 ----------
def v01_bar_ranking(out, title):
    fig = canvas(W128, 62); ax = fig.add_subplot(111)
    o = np.argsort(D.HARGA)[::-1]
    cats = [D.PERANGKAT[i] for i in o]; vals = [D.HARGA[i] for i in o]
    cols = [SIGNAL if v == max(vals) else INK900 for v in vals]
    bars = ax.barh(range(len(vals)), vals, height=0.6, color=cols, zorder=3)
    ax.set_yticks(range(len(vals))); ax.set_yticklabels(cats, fontfamily=STRUCT)
    ax.invert_yaxis()
    for b, v in zip(bars, vals):
        mono_label(ax, v + 6, b.get_y() + b.get_height() / 2, "%.1f" % v, va="center")
    ax.set_xlim(0, max(vals) * 1.2); ax.set_xlabel("Nilai penawaran (juta Rp)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "x"
    return _save(fig, None, out, title, 128)

def v02_column_time(out, title):
    fig = canvas(W128, 52); ax = fig.add_subplot(111)
    ax.bar(D.TAHUN, D.VOLUME_PROYEK, color=INK900, width=0.55, zorder=3)
    ax.set_ylabel("Volume proyek (unit)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v03_grouped_bar(out, title):
    fig = canvas(W166, 62); ax = fig.add_subplot(111)
    ys = np.arange(len(D.PERANGKAT)); w = 0.36
    ax.barh(ys - w / 2, D.HARGA, height=w, color=INK900, zorder=3)
    ax.barh(ys + w / 2, D.HARGA_B, height=w, color=INK400, zorder=3)
    ax.set_yticks(ys); ax.set_yticklabels(D.PERANGKAT, fontfamily=STRUCT)
    ax.invert_yaxis()
    ax.text(max(max(D.HARGA), max(D.HARGA_B)) * 1.02, -0.75,
            "\u25a0 Alfa   \u25a1 Bravo", fontsize=6.5, color=INK700, fontfamily=GLIF)
    ax.set_xlim(0, max(max(D.HARGA), max(D.HARGA_B)) * 1.15)
    ax.set_xlabel("Nilai penawaran (juta Rp)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "x"
    return _save(fig, None, out, title, 166)

def v04_grouped_column(out, title):
    fig = canvas(W166, 58); ax = fig.add_subplot(111)
    xs = np.arange(len(D.PERANGKAT)); w = 0.36
    ax.bar(xs - w / 2, D.HARGA, width=w, color=INK900, zorder=3)
    ax.bar(xs + w / 2, D.HARGA_B, width=w, color=INK400, zorder=3)
    ax.set_xticks(xs); ax.set_xticklabels(D.PERANGKAT, fontfamily=STRUCT, fontsize=6.2)
    ax.text(4.4, max(max(D.HARGA), max(D.HARGA_B)) * 1.02,
            "\u25a0 Alfa   \u25a1 Bravo", fontsize=6.5, color=INK700, fontfamily=GLIF)
    ax.set_ylabel("Nilai penawaran (juta Rp)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 166)

def v05_lollipop(out, title):
    fig = canvas(W128, 58); ax = fig.add_subplot(111)
    o = np.argsort(D.HARGA)[::-1]
    cats = [D.PERANGKAT[i] for i in o]; vals = [D.HARGA[i] for i in o]
    ax.hlines(range(len(vals)), 0, vals, color=INK200, lw=1.2, zorder=2)
    ax.plot(vals, range(len(vals)), "o", ms=6, color=INK900, zorder=3)
    ax.plot(vals[0], 0, "o", ms=6, color=SIGNAL, zorder=4)
    ax.set_yticks(range(len(vals))); ax.set_yticklabels(cats, fontfamily=STRUCT)
    ax.invert_yaxis(); ax.set_xlim(0, max(vals) * 1.15)
    ax.set_xlabel("Nilai penawaran (juta Rp)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "x"
    return _save(fig, None, out, title, 128)

def v06_dotplot(out, title):
    fig = canvas(W128, 60); ax = fig.add_subplot(111)
    for gi, (m, s) in enumerate([(30, 4), (34, 5), (33, 3)]):
        vals = D.MTBF[gi]
        lo, hi, mu = vals.min(), vals.max(), vals.mean()
        ax.plot([gi, gi], [lo, hi], color=INK400, lw=0.7, zorder=1)
        rng = np.random.default_rng(SEED + gi)
        for v in vals:
            ax.plot(gi + rng.uniform(-0.06, 0.06), v, "o", ms=2.6,
                    color=CAT_SERIES[gi], zorder=2)
        ax.plot(gi, mu, "_", ms=12, mew=1.4, color=SIGNAL, zorder=3)
        mono_label(ax, gi + 0.12, hi, "maks %.0f" % hi, va="bottom")
    ax.set_xticks(range(3)); ax.set_xticklabels(D.SITE, fontfamily=STRUCT)
    ax.set_ylabel("MTBF (jam)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v07_dumbbell(out, title):
    fig = canvas(W166, 62); ax = fig.add_subplot(111)
    ys = np.arange(len(D.AUDIT_OBJEK))
    ax.hlines(ys, D.AUDIT_H1, D.AUDIT_H2, color=INK200, lw=1.6, zorder=1)
    ax.plot(D.AUDIT_H1, ys, "o", ms=5.5, color=INK400, zorder=2)
    ax.plot(D.AUDIT_H2, ys, "o", ms=5.5, color=INK900, zorder=3)
    ax.set_yticks(ys); ax.set_yticklabels(D.AUDIT_OBJEK, fontfamily=STRUCT)
    ax.invert_yaxis(); ax.set_xlim(50, 95)
    ax.text(50, -0.9, "\u25cf H1-2026   \u25cf H2-2026", fontsize=6.5,
            color=INK700, fontfamily=STRUCT)
    ax.set_xlabel("Skor audit kepatuhan (0-100)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "x"
    return _save(fig, None, out, title, 166)

def v09_range(out, title):
    fig = canvas(W128, 58); ax = fig.add_subplot(111)
    rng = np.random.default_rng(SEED + 9)
    groups = [("Panel L1", 42, 58), ("Panel L2", 28, 41), ("Panel L3", 12, 24)]
    for gi, (nm, lo, hi) in enumerate(groups):
        samp = rng.uniform(lo, hi, 24)
        ax.plot([gi, gi], [samp.min(), samp.max()], color=INK400, lw=0.8, zorder=1)
        ax.plot(gi, samp.mean(), "s", ms=6, color=SIGNAL, zorder=3)
        for v in samp:
            ax.plot(gi, v, "o", ms=2.4, color=INK900, zorder=2)
        mono_label(ax, gi + 0.14, samp.max(), "%.0f-%.0f A" % (samp.min(), samp.max()),
                   va="bottom")
    ax.set_xticks(range(3)); ax.set_xticklabels([g[0] for g in groups], fontfamily=STRUCT)
    ax.set_ylabel("Arus fasa (A)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v11_slope(out, title):
    fig = canvas(W166, 62); ax = fig.add_subplot(111)
    for h1, h2, nm in zip(D.AUDIT_H1, D.AUDIT_H2, D.AUDIT_OBJEK):
        col = VERD if h2 > h1 else ALERT
        ax.plot([0, 1], [h1, h2], color=col, lw=1.2, zorder=2)
        mono_label(ax, 1.04, h2, nm, va="center", fontsize=6.2)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["H1-2026", "H2-2026"], fontfamily=STRUCT)
    ax.set_xlim(-0.1, 1.5); ax.set_ylim(50, 95)
    ax.set_ylabel("Skor audit (0-100)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 166)

def v12_matrix(out, title):
    fig = canvas(W166, 70); ax = fig.add_subplot(111)
    sym = [" ", ".", ":", "o", "O", "#"]
    for i in range(6):
        for j in range(8):
            k = int(D.SKOR_M[i, j] * (len(sym) - 1.001))
            ax.text(j, i, sym[k] * 3, ha="center", va="center",
                    fontsize=7.5, color=INK900, fontfamily=MONO)
    ax.set_xticks(range(8)); ax.set_xticklabels(D.FAKTOR, fontfamily=STRUCT)
    ax.set_yticks(range(6)); ax.set_yticklabels(D.NAMA_SITE6, fontfamily=STRUCT)
    ax.set_xlim(-0.5, 7.5); ax.set_ylim(5.5, -0.5)
    for s in ax.spines.values():
        s.set_visible(True); s.set_color(INK200)
    ax.grid(True, color=INK200, lw=0.4)
    ax.set_xlabel("Faktor uji F1..F8", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166, "simbol gradasi bobot teks, bukan warna")

def v13_small_multiples(out, title):
    fig = plt.figure(figsize=(W166 / 25.4, 74 / 25.4))
    axes = []
    for idx, (site, ser) in enumerate(D.SM_MULT.items()):
        ax = fig.add_subplot(2, 3, idx + 1)
        ax.plot(range(1, 13), ser, color=INK900, lw=1.0)
        ax.plot(12, ser[-1], "o", ms=3, color=SIGNAL)
        ax.set_title(site, fontsize=6.8, color=INK900, fontfamily=STRUCT)
        ax.set_ylim(0, 7)
        for t in ax.get_xticklabels() + ax.get_yticklabels():
            t.set_fontsize(5.8); t.set_fontfamily(MONO)
        ax.tick_params(length=0)
        axes.append(ax)
    fig.text(0.01, -0.075, "%s - seed %d | pustakachart_data.py (VCTL-1007 C2)"
             % (CAPTION_LABEL, SEED), fontsize=6.0, color=INK400,
             fontfamily=MONO, va="bottom")
    fig.text(0.01, 0.985, title, fontsize=8.0, color=INK900, fontweight="bold",
             fontfamily=STRUCT, va="top")
    fig.tight_layout(rect=(0.01, 0.05, 1, 0.94))
    fig.canvas.draw()
    mp = measure_min_pt(fig)
    fig.savefig(out, dpi=DPI, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)
    return mp

def v15_table(out, title):
    fig = canvas(W128, 46); ax = fig.add_subplot(111); ax.axis("off")
    tbl = ax.table(cellText=D.TABLE_ROWS, colLabels=D.TABLE_HEAD,
                   cellLoc="center", loc="upper center")
    tbl.auto_set_font_size(False); tbl.set_fontsize(6.8)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor(INK200); cell.set_linewidth(0.5)
        cell.set_facecolor(PAPER)
        if r == 0:
            cell.set_text_props(color=INK400, fontweight="bold", fontfamily=STRUCT)
        elif c == 1:
            v = D.TABLE_ROWS[r - 1][1]
            col = ALERT if v < 95 else (SIGNAL if v < 98 else INK900)
            cell.set_text_props(color=col, fontfamily=MONO)
        elif c == 3:
            st = D.TABLE_ROWS[r - 1][3]
            col = ALERT if st != "Selesai" else VERD
            cell.set_text_props(color=col, fontfamily=MONO)
        else:
            cell.set_text_props(color=INK700, fontfamily=MONO if c == 2 else STRUCT)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128,
                 "pratinjau; produksi lewat datum_docx/datum_xlsx")

def v16_pareto(out, title):
    fig = canvas(W166, 62); ax = fig.add_subplot(111)
    cum = np.cumsum(D.KEJADIAN) / sum(D.KEJADIAN) * 100
    ax.bar(range(5), D.KEJADIAN, color=INK900, width=0.6, zorder=3)
    ax2 = ax.twinx()
    ax2.plot(range(5), cum, color=SIGNAL, lw=1.4, marker="o", ms=3.5)
    ax2.axhline(80, color=INK400, lw=0.7, ls=(0, (3, 3)))
    ax2.set_ylim(0, 105); ax2.set_ylabel("Kumulatif (%)", fontsize=6.8)
    ax2.tick_params(colors=INK400, labelsize=6.5, length=0)
    ax2.spines["top"].set_visible(False)
    ax.set_xticks(range(5))
    ax.set_xticklabels(D.PENYEBAB, fontfamily=STRUCT, fontsize=6.2)
    ax.set_ylabel("Frekuensi kejadian", fontsize=6.8)
    ax.grid(axis="y", color=INK200, lw=0.4, zorder=0)
    for t in ax.get_xticklabels():
        t.set_fontfamily(STRUCT)
    fig.canvas.draw()
    mp = measure_min_pt(fig)
    fig.text(0.01, -0.075, "%s - seed %d | pustakachart_data.py (VCTL-1007 C2)"
             % (CAPTION_LABEL, SEED), fontsize=6.0, color=INK400,
             fontfamily=MONO, va="bottom")
    fig.text(0.01, 0.985, title, fontsize=8.0, color=INK900, fontweight="bold",
             fontfamily=STRUCT, va="top")
    fig.savefig(out, dpi=DPI, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)
    return mp

# ---------- K2 ----------
def _stack_rows(labels, parts, total100, width_mm, height_mm, out, title):
    fig = canvas(width_mm, height_mm); ax = fig.add_subplot(111)
    ys = np.arange(len(labels))
    for ri, row in enumerate(parts):
        vals = [v / sum(row) * 100 for v in row] if total100 else row
        left = 0.0
        for si, v in enumerate(vals):
            ax.barh(ys[ri], v, left=left, height=0.55,
                    color=CAT_SERIES[si % 5], zorder=3)
            if v > 9:
                ax.text(left + v / 2, ys[ri], "%d%%" % round(v), ha="center",
                        va="center", fontsize=6.0, fontfamily=MONO,
                        color=PAPER if CAT_SERIES[si % 5] in (INK900, SIGNAL, VERD, ALERT) else INK700)
            left += v
    ax.set_yticks(ys); ax.set_yticklabels(labels, fontfamily=STRUCT)
    ax.invert_yaxis(); ax.set_xlim(0, max(np.sum(np.array(r) for r in parts)) if not total100 else 100)
    ax.set_xlabel("Komposisi (%)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "x"
    return _save(fig, None, out, title, width_mm)

def v19_stacked_bar(out, title):
    labels = ["Proyek VSS", "Proyek Fiber", "Proyek Daya"]
    parts = [[52, 28, 14, 6], [40, 35, 17, 8], [61, 22, 11, 6]]
    return _stack_rows(labels, parts, True, W166, 50, out, title)

def v20_stacked_column(out, title):
    fig = canvas(W128, 58); ax = fig.add_subplot(111)
    comps = np.array([[18, 12, 8, 4], [22, 14, 9, 5], [19, 15, 10, 6],
                      [24, 13, 8, 4], [21, 16, 9, 5], [23, 14, 10, 6]])
    bottoms = np.zeros(6)
    for si in range(4):
        ax.bar(D.BULAN[:6], comps[:, si], bottom=bottoms, width=0.6,
               color=CAT_SERIES[si], zorder=3)
        bottoms += comps[:, si]
    ax.set_ylabel("Beban daya (kW)", fontsize=6.8)
    ax.set_xticks(range(6)); ax.set_xticklabels(D.BULAN[:6], fontfamily=STRUCT)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v21_diverging_bar(out, title):
    fig = canvas(W166, 58); ax = fig.add_subplot(111)
    ys = np.arange(len(D.SURVEI_ASP))
    ax.barh(ys, D.SETUJU, height=0.55, color=VERD, zorder=3)
    ax.barh(ys, D.TIDAK_SETUJU, height=0.55, color=ALERT, zorder=3)
    ax.axvline(0, color=INK900, lw=0.8)
    ax.set_yticks(ys); ax.set_yticklabels(D.SURVEI_ASP, fontfamily=STRUCT)
    ax.invert_yaxis(); ax.set_xlim(-60, 75)
    ax.text(0, -0.95, "\u25a0 setuju    \u25a0 tidak setuju", fontsize=6.5,
            color=INK700, fontfamily=GLIF)
    ax.set_xlabel("Selisih respons responden (%)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "x"
    return _save(fig, None, out, title, 166)

def v22_diverging_column(out, title):
    fig = canvas(W128, 58); ax = fig.add_subplot(111)
    xs = np.arange(len(D.SURVEI_ASP))
    ax.bar(xs, D.SETUJU, width=0.55, color=VERD, zorder=3)
    ax.bar(xs, D.TIDAK_SETUJU, width=0.55, color=ALERT, zorder=3)
    ax.axhline(0, color=INK900, lw=0.8)
    ax.set_xticks(xs); ax.set_xticklabels(D.SURVEI_ASP, fontfamily=STRUCT, fontsize=6.0)
    ax.set_ylabel("Selisih respons (%)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v23_pyramid(out, title):
    fig = canvas(W166, 58); ax = fig.add_subplot(111)
    ys = np.arange(len(D.JENJANG))
    ax.barh(ys, [-v for v in D.FRONT_END], height=0.6, color=INK900, zorder=3)
    ax.barh(ys, D.BACK_END, height=0.6, color=INK400, zorder=3)
    ax.set_yticks(ys); ax.set_yticklabels(D.JENJANG, fontfamily=STRUCT)
    ax.invert_yaxis()
    ax.text(-46, -0.95, "\u25a0 Tim lapangan", fontsize=6.5, color=INK700, fontfamily=GLIF)
    ax.text(12, -0.95, "\u25a0 Tim kantor", fontsize=6.5, color=INK700, fontfamily=GLIF)
    ax.set_xlim(-50, 50); ax.set_xlabel("Jumlah personel per jenjang", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "x"
    return _save(fig, None, out, title, 166)

def v24_waffle(out, title):
    fig = canvas(W128, 78); ax = fig.add_subplot(111)
    seq = []
    for (nm, n), col in zip(D.WAFFLE_PARTS, [VERD, SIGNAL, INK200]):
        seq += [(nm, col)] * n
    for k, (nm, col) in enumerate(seq):
        r, c = divmod(k, 10)
        ax.add_patch(Rectangle((c * 1.06, -r * 1.06), 0.9, 0.9, facecolor=col,
                               edgecolor=PAPER, lw=0.4))
    ax.set_xlim(-0.3, 10.6); ax.set_ylim(-10.6, 0.6); ax.set_aspect("equal")
    ax.axis("off")
    xoff = 0
    for (nm, n), col in zip(D.WAFFLE_PARTS, [VERD, SIGNAL, INK200]):
        ax.text(xoff, 0.95, "\u25a0 %s %d%%" % (nm, n), fontsize=6.5, color=col,
                fontfamily=GLIF)
        xoff += 3.6
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128, "1 kotak = 1 persen")

def v25_square_area(out, title):
    fig = canvas(W128, 60); ax = fig.add_subplot(111)
    xoff = 0
    for (nm, n) in D.KAMERA_SITE:
        cells = int(round(n / 20))          # 1 kotak = 20 kamera
        side = int(np.ceil(np.sqrt(cells)))
        for k in range(cells):
            r, c = divmod(k, side)
            ax.add_patch(Rectangle((xoff + c * 1.05, -r * 1.05), 0.9, 0.9,
                                   facecolor=INK900, edgecolor=PAPER, lw=0.3))
        ax.text(xoff, -side * 1.05 - 0.7, "%s\n%d titik" % (nm, n), fontsize=6.2,
                color=INK700, fontfamily=STRUCT, va="top")
        xoff += side * 1.05 + 2.2
    ax.set_xlim(-0.5, xoff); ax.set_ylim(-math_floor(), 1.5); ax.set_aspect("equal")
    ax.axis("off")
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128, "1 kotak = 20 kamera")

def math_floor():
    import math as m
    return m.ceil(np.sqrt(max(n for _, n in D.KAMERA_SITE) / 20)) * 1.05 + 2.5

def v26_icon_circles(out, title):
    fig = canvas(W128, 56); ax = fig.add_subplot(111)
    xoff = 0
    for (nm, n) in D.KAMERA_SITE:
        rad = np.sqrt(n / np.pi) / 6.0      # luas proporsional jumlah
        circ = plt.Circle((xoff + rad, rad + 0.6), rad, facecolor=INK900,
                          edgecolor=PAPER, lw=0.5)
        ax.add_patch(circ)
        ax.text(xoff + rad, -0.35, "%s\n%d" % (nm, n), fontsize=6.2, color=INK700,
                fontfamily=STRUCT, ha="center", va="top")
        xoff += 2 * rad + 1.6
    ax.set_xlim(-0.4, xoff); ax.set_ylim(-2.2, 5.2); ax.set_aspect("equal"); ax.axis("off")
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128, "glif netral: lingkaran luas proporsional")

def v31_marimekko(out, title):
    fig = canvas(W166, 66); ax = fig.add_subplot(111)
    xoff = 0.0
    for cat, (lebar, bagian) in D.MARIMEKKO.items():
        ybot = 0.0
        for bi, (bnm, bpct) in enumerate(bagian):
            h = bpct
            ax.add_patch(Rectangle((xoff, ybot), lebar * 0.94, h,
                                   facecolor=CAT_SERIES[bi], edgecolor=PAPER, lw=0.6))
            ax.text(xoff + lebar * 0.47, ybot + h / 2, "%s %d%%" % (bnm, bpct),
                    ha="center", va="center", fontsize=6.0, fontfamily=MONO,
                    color=PAPER if bi == 0 else INK700)
            ybot += h
        ax.text(xoff + lebar * 0.47, -7, cat, ha="center", va="top", fontsize=6.2,
                color=INK700, fontfamily=STRUCT)
        xoff += lebar
    ax.set_xlim(0, xoff); ax.set_ylim(-16, 104); ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("Porsi menang tender (%)", fontsize=6.8)
    ax.set_xticks([])
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166, "lebar kolom = porsi tender")

def _squarify(items, x, y, w, h, outp):
    """slice-dice pada sisi terpanjang - deterministik, luas = nilai."""
    if not items:
        return
    total = sum(v for _, v in items)
    nm, v = items[0]
    frac = v / total
    if w >= h:
        ww = w * frac
        outp.append((x, y, ww, h, nm, v))
        _squarify(items[1:], x + ww, y, w - ww, h, outp)
    else:
        hh = h * frac
        outp.append((x, y, w, hh, nm, v))
        _squarify(items[1:], x, y + hh, w, h - hh, outp)

def v32_treemap(out, title):
    fig = canvas(W166, 70); ax = fig.add_subplot(111)
    flat = []
    for div, subs in D.TREEMAP:
        for nm, v in subs:
            flat.append(("%s / %s" % (div, nm), v))
    flat.sort(key=lambda t: -t[1])
    rects = []
    _squarify(flat, 0, 0, 100, 100, rects)
    shades = [INK900, INK700, INK400, INK200]
    # FIX3-D4 (kartu t_86670cef): label hanya dicetak bila MUAT di kotak —
    # lebar teks diukur riil lewat renderer (bukan ambang luas kotak buta),
    # sehingga '...d Patch' terklip dan 'UPS 10kVA' mepet tepi tidak terjadi.
    # Kotak yang tidak muat memakai kode divisi + nilai (VS/Fi/Da); identitas
    # penuh tetap terbaca lewat keterangan footer + caption manual. Data/seed
    # beku 42 tidak berubah.
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_aspect("equal"); ax.axis("off")
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    inv = ax.transData.inverted()

    def _fits(s, x, y, w, h, fs, fam):
        t = ax.text(x, y, s, fontsize=fs, fontfamily=fam)
        bb = t.get_window_extent(renderer=rend)
        (x0, y0), (x1, y1) = inv.transform(bb)
        t.remove()
        return (x1 - x0) <= w - 2.0 and (y1 - y0) <= h - 1.5

    omitted = []
    for i, (x, y, w, h, nm, v) in enumerate(rects):
        col = shades[i % 4]
        ax.add_patch(Rectangle((x, y), w, h, facecolor=col, edgecolor=PAPER, lw=1.0))
        ink = PAPER if col in (INK900, INK700) else INK700
        div, sub = nm.split(" / ")
        if _fits(sub, x + 1.5, y + h - 2, w, h, 6.2, STRUCT) and \
           _fits("%.1f" % v, x + 1.5, y + 2, w, h, 6.2, MONO):
            ax.text(x + 1.5, y + h - 2, sub, fontsize=6.2, fontfamily=STRUCT,
                    va="top", color=ink)
            ax.text(x + 1.5, y + 2, "%.1f" % v, fontsize=6.2, fontfamily=MONO,
                    color=ink)
        elif _fits("%s %.1f" % (div.split()[1][:2], v), x + 1.5, y + h / 2 - 2,
                   w, h, 6.2, MONO):
            ax.text(x + 1.5, y + h / 2 - 2, "%s %.1f" % (div.split()[1][:2], v),
                    fontsize=6.2, fontfamily=MONO, color=ink)
            omitted.append(nm)
        else:
            omitted.append(nm)
    extra = ("kotak kecil tanpa label muat: %s" % ", ".join(sorted(omitted))
             if omitted else "")
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166, "slice-dice deterministik, luas = biaya"
                 + ((" | " + extra) if extra else ""))

def v36_dendro(out, title):
    fig = canvas(W166, 58); ax = fig.add_subplot(111)
    xs = {i: float(i) for i in range(6)}
    pos = {}
    for i, nm in enumerate(D.DENDRO_LEAF):
        pos[i] = (xs[i], 0.0)
    nid = 6
    for (a, b, dist) in D.DENDRO_TREE:
        xa, ya = pos[a]; xb, yb = pos[b]
        ynew = max(ya, yb) + dist * 0.35
        ax.plot([xa, xa], [ya, ynew], color=INK700, lw=0.9)
        ax.plot([xb, xb], [yb, ynew], color=INK700, lw=0.9)
        ax.plot([xa, xb], [ynew, ynew], color=INK700, lw=0.9)
        pos[nid] = ((xa + xb) / 2, ynew); nid += 1
    for i, nm in enumerate(D.DENDRO_LEAF):
        ax.text(i, -0.25, nm, ha="center", va="top", fontsize=6.5,
                color=INK700, fontfamily=STRUCT)
    ax.set_ylim(-1.2, max(p[1] for p in pos.values()) + 0.6)
    ax.set_xlim(-0.6, 5.6); ax.set_yticks([]); ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("Daun = gardu; tinggi cabang = jarak profil beban", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166)

def v37_funnel(out, title):
    fig = canvas(W128, 62); ax = fig.add_subplot(111)
    n0 = D.FUNNEL[0][1]
    y = 0
    for i, (nm, v) in enumerate(D.FUNNEL):
        w_top = v / n0
        w_bot = (D.FUNNEL[i + 1][1] / n0) if i + 1 < len(D.FUNNEL) else v / n0 * 0.85
        col = SIGNAL if i == len(D.FUNNEL) - 1 else INK900
        ax.add_patch(Polygon([(-w_top / 2, -y), (w_top / 2, -y),
                              (w_bot / 2, -y - 0.9), (-w_bot / 2, -y - 0.9)],
                             closed=True, facecolor=col, edgecolor=PAPER, lw=0.8))
        ax.text(0, -y - 0.45, "%s  %d" % (nm, v), ha="center", va="center",
                fontsize=6.4, fontfamily=MONO, color=PAPER)
        y += 1.0
    ax.set_xlim(-0.6, 0.6); ax.set_ylim(-y - 0.2, 0.4); ax.axis("off")
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128, "trapesium bertumpuk, lebar = sisa dokumen")

def v40_org(out, title):
    fig = canvas(W166, 66); ax = fig.add_subplot(111)
    root_nm, lvl1 = D.ORG["root"]
    def box(x, y, txt, col=INK900, tcol=PAPER):
        ax.add_patch(Rectangle((x - 0.075, y - 0.045), 0.15, 0.09, facecolor=col,
                               edgecolor=INK400, lw=0.6))
        ax.text(x, y, txt, ha="center", va="center", fontsize=6.2,
                fontfamily=STRUCT, color=tcol)
    box(0.5, 0.86, root_nm)
    n1 = len(lvl1)
    xs1 = [0.5 + (i - (n1 - 1) / 2) * 0.3 for i in range(n1)]
    for (nm1, kids), x1 in zip(lvl1, xs1):
        ax.plot([0.5, 0.5, x1, x1], [0.815, 0.74, 0.74, 0.665], color=INK400, lw=0.8)
        box(x1, 0.62, nm1, col=INK700)
        nk = len(kids)
        xsk = [x1 + (j - (nk - 1) / 2) * 0.11 for j in range(nk)]
        for kid, xk in zip(kids, xsk):
            ax.plot([x1, x1, xk, xk], [0.575, 0.50, 0.50, 0.425], color=INK400, lw=0.8)
            box(xk, 0.38, kid, col=INK100, tcol=INK900)
    ax.set_xlim(0, 1); ax.set_ylim(0.28, 0.95); ax.axis("off")
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166)

# ---------- K3 ----------
def v41_line(out, title):
    fig = canvas(W128, 56); ax = fig.add_subplot(111)
    m = np.arange(1, 13)
    ax.plot(m, D.BITRATE_A, color=INK900, lw=1.4)
    ax.plot(m, D.BITRATE_B, color=INK400, lw=1.2, ls=(0, (4, 3)))
    ax.text(12.2, D.BITRATE_A[-1], "Site A", color=INK900, fontsize=6.5,
            va="center", fontfamily=STRUCT)
    ax.text(12.2, D.BITRATE_B[-1], "Site B", color=INK400, fontsize=6.5,
            va="center", fontfamily=STRUCT)
    ax.set_xlim(1, 14.8); ax.set_xlabel("Bulan 2026", fontsize=6.8)
    ax.set_ylabel("Bitrate rerata (Mbps)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v42_area(out, title):
    fig = canvas(W128, 54); ax = fig.add_subplot(111)
    ax.fill_between(D.BULAN, D.BEBAN_KW, color=INK200, zorder=2)
    ax.plot(D.BULAN, D.BEBAN_KW, color=INK900, lw=1.2, zorder=3)
    ax.set_ylabel("Beban puncak (kW)", fontsize=6.8)
    ax.set_ylim(0, max(D.BEBAN_KW) * 1.15)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v43_stacked_area(out, title):
    fig = canvas(W166, 60); ax = fig.add_subplot(111)
    m = np.arange(1, 13)
    data = [D.BITRATE_A, D.BITRATE_B, D.BITRATE_C]
    ax.stackplot(m, data, colors=[INK900, SIGNAL, INK400], zorder=2)
    ax.text(12.3, D.BITRATE_A[-1] / 2, "Site A", fontsize=6.2, color=PAPER,
            fontfamily=STRUCT, va="center")
    ax.set_xlim(1, 12); ax.set_xlabel("Bulan 2026", fontsize=6.8)
    ax.set_ylabel("Total bitrate agregat (Mbps)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166)

def v45_bump(out, title):
    fig = canvas(W166, 62); ax = fig.add_subplot(111)
    xs = np.arange(4)
    for i, (nm, ranks) in enumerate(D.BUMP_SERI.items()):
        col = CAT_SERIES[i]
        ax.plot(xs, ranks, color=col, lw=1.5, marker="o", ms=4)
        ax.text(-0.08, ranks[0], nm, ha="right", va="center", fontsize=6.2,
                color=col, fontfamily=STRUCT)
        ax.text(3.08, ranks[-1], nm, ha="left", va="center", fontsize=6.2,
                color=col, fontfamily=STRUCT)
    ax.set_xticks(xs); ax.set_xticklabels(D.BUMP_KV, fontfamily=STRUCT)
    ax.set_ylim(5.6, 0.4); ax.set_xlim(-0.9, 4.0)
    ax.set_ylabel("Peringkat vendor (1 = terbaik)", fontsize=6.8)
    ax.set_yticks([1, 2, 3, 4, 5])
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166)

def _smooth(y, k=3):
    ker = np.ones(k) / k
    pad = np.r_[[y[0]] * (k - 1), y, [y[-1]] * (k - 1)]
    return np.convolve(pad, ker, mode="same")[k - 1: k - 1 + len(y)]

def v47_spline(out, title):
    fig = canvas(W128, 56); ax = fig.add_subplot(111)
    m = np.arange(1, 13)
    sm = _smooth(D.BITRATE_A, 3)
    ax.plot(m, sm, color=INK900, lw=1.4)
    ax.plot(m, D.BITRATE_A, color=INK200, lw=0.8, ls=(0, (2, 2)))
    ax.text(12.15, sm[-1], "Site A (halus)", color=INK900, fontsize=6.2,
            va="center", fontfamily=STRUCT)
    ax.text(12.15, D.BITRATE_A[-1] - 0.35, "titik asli", color=INK400, fontsize=6.2,
            va="center", fontfamily=STRUCT)
    ax.set_xlim(1, 15.2); ax.set_xlabel("Bulan 2026", fontsize=6.8)
    ax.set_ylabel("Bitrate (Mbps)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128, "penghalusan moving-average, bukan interpolasi spline")

def v48_step(out, title):
    fig = canvas(W128, 54); ax = fig.add_subplot(111)
    tariff = [1444, 1444, 1544, 1544, 1650, 1650, 1650, 1755, 1755, 1848, 1848, 1932]
    ax.step(np.arange(1, 13), tariff, where="post", color=INK900, lw=1.4)
    ax.set_xticks(np.arange(1, 13)); ax.set_xticklabels(D.BULAN, fontsize=5.8)
    ax.set_ylabel("Tarif tenaga listrik (Rp/kWh)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v49_calendar(out, title):
    fig = canvas(W166, 44); ax = fig.add_subplot(111)
    start = _dt.date(2026, 1, 5)             # Senin pertama grid beku
    rng = np.random.default_rng(SEED + 49)
    counts = rng.poisson(3.2, 7 * 53)
    for wk in range(53):
        for wd in range(7):
            d = start + _dt.timedelta(days=wk * 7 + wd)
            if d.year != 2026:
                continue
            v = counts[wd * 53 + wk]
            ax.add_patch(Rectangle((wk, -wd), 0.88, -0.88, facecolor=RAMP(min(1, v / 9.0)),
                                   edgecolor=PAPER, lw=0.3))
    ax.set_xlim(-0.5, 53); ax.set_ylim(6.8, -0.8)
    ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
    ax.set_yticklabels(["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"],
                       fontfamily=STRUCT, fontsize=6.0)
    ax.set_xticks([0, 9, 18, 26, 35, 44, 52])
    ax.set_xticklabels(["Jan", "Mar", "Mei", "Jul", "Sep", "Nov", "Des"],
                       fontfamily=STRUCT, fontsize=6.0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166, "jumlah tiket harian 2026")

def v50_fan(out, title):
    fig = canvas(W166, 60); ax = fig.add_subplot(111)
    t = D.FAN_TAHUN
    ax.fill_between(t, D.FAN_LO2, D.FAN_HI2, color=INK100, zorder=1)
    ax.fill_between(t, D.FAN_LO1, D.FAN_HI1, color=INK200, zorder=2)
    ax.plot(t, D.FAN_MED, color=INK900, lw=1.5, zorder=3)
    ax.plot(t[:3], D.FAN_MED[:3], color=SIGNAL, lw=1.5, zorder=4)
    ax.text(2031.1, D.FAN_MED[-1], "median", fontsize=6.2, color=INK900,
            va="center", fontfamily=STRUCT)
    ax.text(2031.1, D.FAN_HI1[-1], "p10-p90", fontsize=6.2, color=INK700,
            va="center", fontfamily=STRUCT)
    ax.text(2031.1, D.FAN_HI2[-1], "p5-p95", fontsize=6.2, color=INK400,
            va="center", fontfamily=STRUCT)
    ax.set_xlim(2026, 2033.6)
    ax.set_ylabel("Titik kamera terpasang (proyeksi)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 166)

def v51_spark(out, title):
    fig = plt.figure(figsize=(W128 / 25.4, 44 / 25.4))
    rows = list(D.SPARK.items())
    for i, (nm, ser) in enumerate(rows):
        ax = fig.add_axes([0.30, 0.86 - i * 0.175, 0.42, 0.11])
        ax.plot(range(len(ser)), ser, color=INK900, lw=0.9)
        ax.plot(len(ser) - 1, ser[-1], "o", ms=2.6, color=SIGNAL)
        ax.axis("off")
        fig.text(0.02, 0.885 - i * 0.175, "%s: %.1f" % (nm, ser[-1]), fontsize=6.2,
                 color=INK700, fontfamily=MONO, va="center")
    fig.text(0.01, -0.075, "%s - seed %d | sparkline dalam sel tabel DATUM"
             % (CAPTION_LABEL, SEED), fontsize=6.0, color=INK400,
             fontfamily=MONO, va="bottom")
    fig.text(0.01, 0.975, title, fontsize=8.0, color=INK900, fontweight="bold",
             fontfamily=STRUCT, va="top")
    fig.canvas.draw()
    mp = measure_min_pt(fig)
    fig.savefig(out, dpi=DPI, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)
    return mp

# ---------- K4 ----------
def v52_hist(out, title):
    fig = canvas(W128, 54); ax = fig.add_subplot(111)
    ax.hist(D.LATENSI, bins=24, color=INK900, edgecolor=PAPER, lw=0.4, zorder=3)
    ax.set_xlabel("Lebar bin tetap 24 bin; aturan bin di caption", fontsize=6.6)
    ax.set_ylabel("Frekuensi (kbps)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def _kde(sample, grid, bw=None):
    s = np.asarray(sample, dtype=float)
    if bw is None:
        bw = 1.06 * s.std() * len(s) ** -0.2
    return np.exp(-0.5 * ((grid[:, None] - s[None, :]) / bw) ** 2).sum(axis=1) / \
        (len(s) * bw * np.sqrt(2 * np.pi))

def v53_density(out, title):
    fig = canvas(W128, 54); ax = fig.add_subplot(111)
    g = np.linspace(D.LATENSI.min(), np.percentile(D.LATENSI, 99), 200)
    dens = _kde(D.LATENSI, g)
    ax.fill_between(g, dens, color=INK200, zorder=2)
    ax.plot(g, dens, color=INK900, lw=1.2, zorder=3)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("Throughput (kbps)", fontsize=6.8)
    ax.set_ylabel("Kerapatan (KDE Silverman)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128)

def v54_box(out, title):
    fig = canvas(W128, 56); ax = fig.add_subplot(111)
    bp = ax.boxplot(D.MTBF, patch_artist=True, widths=0.5,
                    flierprops=dict(marker=".", ms=3, mec=INK400),
                    medianprops=dict(color=SIGNAL, lw=1.6),
                    whiskerprops=dict(color=INK700), capprops=dict(color=INK700))
    for b in bp["boxes"]:
        b.set(facecolor=INK100, edgecolor=INK700, lw=0.8)
    ax.set_xticklabels(D.SITE, fontfamily=STRUCT)
    ax.set_ylabel("MTBF (jam); n=80/grup", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v55_violin(out, title):
    fig = canvas(W128, 56); ax = fig.add_subplot(111)
    vp = ax.violinplot(D.MTBF, widths=0.7, showextrema=False)
    for body in vp["bodies"]:
        body.set(facecolor=INK100, edgecolor=INK700, linewidth=0.8)
    for i, data in enumerate(D.MTBF):
        q1, med, q3 = np.percentile(data, [25, 50, 75])
        ax.plot([i + 1, i + 1], [q1, q3], color=INK700, lw=6, solid_capstyle="butt", zorder=3)
        ax.plot(i + 1, med, "_", color=SIGNAL, ms=12, mew=1.6, zorder=4)
    ax.set_xticks([1, 2, 3]); ax.set_xticklabels(D.SITE, fontfamily=STRUCT)
    ax.set_ylabel("MTBF (jam)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v56_strip(out, title):
    fig = canvas(W128, 54); ax = fig.add_subplot(111)
    for gi, data in enumerate(D.MTBF):
        ax.plot(np.full(len(data), gi + 1), data, "o", ms=2.8,
                color=CAT_SERIES[gi], alpha=0.85, zorder=3)
        ax.plot(gi + 1, data.mean(), "_", color=SIGNAL, ms=14, mew=1.5, zorder=4)
    ax.set_xticks([1, 2, 3]); ax.set_xticklabels(D.SITE, fontfamily=STRUCT)
    ax.set_ylabel("MTBF (jam)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v57_jitter(out, title):
    fig = canvas(W128, 54); ax = fig.add_subplot(111)
    for gi, data in enumerate(D.MTBF):
        rng = np.random.default_rng(SEED + 57 + gi)
        xs = gi + 1 + rng.uniform(-0.14, 0.14, len(data))
        ax.plot(xs, data, "o", ms=2.8, color=CAT_SERIES[gi], alpha=0.8, zorder=3)
    ax.set_xticks([1, 2, 3]); ax.set_xticklabels(D.SITE, fontfamily=STRUCT)
    ax.set_ylabel("MTBF (jam); jitter horizontal seeded", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v59_ridge(out, title):
    fig = canvas(W166, 66); ax = fig.add_subplot(111)
    g = np.linspace(20, 50, 160)
    for i, data in enumerate(D.MTBF):
        dens = _kde(data, g)
        dens = dens / dens.max() * 0.8
        base = len(D.MTBF) - 1 - i
        ax.fill_between(g, dens + base, base, color=INK100, zorder=2 + i)
        ax.plot(g, dens + base, color=INK900, lw=1.0, zorder=12 + i)
        ax.text(19.2, base + 0.32, D.SITE[i], fontsize=6.4, color=INK700,
                fontfamily=STRUCT, ha="right")
    ax.set_yticks([]); ax.set_xlim(19, 50)
    ax.set_xlabel("MTBF (jam) - deret vertikal Site A atas ke Site C bawah", fontsize=6.8)
    for s in ("left",):
        ax.spines[s].set_visible(False)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166)

def v60_barcode(out, title):
    fig = canvas(W128, 40); ax = fig.add_subplot(111)
    for i, v in enumerate(D.PING_MS):
        ax.plot([v, v], [0, 1], color=INK900, lw=0.5, alpha=0.6,
                solid_capstyle="butt", zorder=3)
    ax.axvline(np.median(D.PING_MS), color=SIGNAL, lw=1.2, zorder=4)
    ax.text(np.median(D.PING_MS) + 1, 1.04, "median %.0f ms" % np.median(D.PING_MS),
            fontsize=6.4, color=SIGNAL, fontfamily=MONO)
    ax.set_ylim(0, 1); ax.set_yticks([])
    ax.set_xlim(D.PING_MS.min(), D.PING_MS.max())
    ax.set_xlabel("RTT ping (ms) - 400 sampel", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128)

def v61_heat1d(out, title):
    fig = canvas(W166, 34); ax = fig.add_subplot(111)
    vals = np.round(np.linspace(0, 1, 60), 3)
    ax.imshow(vals.reshape(1, -1), cmap=RAMP, aspect="auto", vmin=0, vmax=1)
    ax.set_xticks([0, 15, 30, 45, 59])
    ax.set_xticklabels(["0 jam", "6 jam", "12 jam", "18 jam", "24 jam"],
                       fontfamily=STRUCT, fontsize=6.2)
    ax.set_yticks([])
    ax.set_xlabel("Intensitas gangguan sepanjang hari (ramp sekuensial satu hue)",
                  fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166)

def v63_ecdf(out, title):
    fig = canvas(W128, 54); ax = fig.add_subplot(111)
    xs = np.sort(D.PING_MS)
    ys = np.arange(1, len(xs) + 1) / len(xs)
    ax.step(xs, ys, color=INK900, lw=1.3, where="post", zorder=3)
    for p in (50, 95):
        v = np.percentile(D.PING_MS, p)
        ax.plot(v, p / 100, "o", ms=4, color=SIGNAL, zorder=4)
        ax.text(v + 1.5, p / 100 - 0.06, "p%d = %.0f ms" % (p, v), fontsize=6.4,
                color=SIGNAL, fontfamily=MONO)
    ax.set_xlabel("RTT ping (ms)", fontsize=6.8); ax.set_ylabel("Proporsi sampel")
    ax.set_ylim(0, 1.02)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v65_errorbar(out, title):
    fig = canvas(W128, 56); ax = fig.add_subplot(111)
    xs = np.arange(4)
    ax.bar(xs, D.ERR_MEAN, width=0.55, yerr=D.ERR_SD, capsize=3,
           color=INK900, zorder=3,
           error_kw=dict(ecolor=INK400, lw=0.9))
    ax.set_xticks(xs); ax.set_xticklabels(D.ERR_LABEL, fontfamily=STRUCT, fontsize=6.2)
    ax.set_ylabel("Latensi rerata +/- SD (ms)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

# ---------- K5 ----------
def v66_scatter(out, title):
    fig = canvas(W128, 66); ax = fig.add_subplot(111)
    ax.scatter(D.SCAT_X, D.SCAT_Y, s=16, color=INK900, zorder=3)
    for idx, nm in D.SCAT_ANNOT.items():
        ax.annotate(nm, (D.SCAT_X[idx], D.SCAT_Y[idx]), xytext=(5, 4),
                    textcoords="offset points", fontsize=6.2, color=SIGNAL,
                    fontfamily=STRUCT)
    ax.set_xlabel("Harga paket (juta Rp)", fontsize=6.8)
    ax.set_ylabel("Throughput uji (Mbps)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "both"
    return _save(fig, None, out, title, 128)

def v67_bubble(out, title):
    fig = canvas(W128, 66); ax = fig.add_subplot(111)
    ax.scatter(D.SCAT_X, D.SCAT_Y, s=D.SCAT_SIZE * 28, facecolor=INK100,
               edgecolor=INK900, linewidth=0.8, zorder=3)
    for idx, nm in D.SCAT_ANNOT.items():
        ax.annotate(nm, (D.SCAT_X[idx], D.SCAT_Y[idx]), xytext=(6, 5),
                    textcoords="offset points", fontsize=6.2, color=SIGNAL,
                    fontfamily=STRUCT)
    ax.set_xlabel("Harga paket (juta Rp)", fontsize=6.8)
    ax.set_ylabel("Throughput uji (Mbps)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "both"
    return _save(fig, None, out, title, 128, "luas gelembung = garansi (tahun)")

def v68_conn_scatter(out, title):
    fig = canvas(W128, 60); ax = fig.add_subplot(111)
    ax.plot(D.CS_X, D.CS_Y, color=INK900, lw=1.0, marker="o", ms=3.2, zorder=3)
    ax.annotate("08:00", (D.CS_X[0], D.CS_Y[0]), xytext=(-2, 6),
                textcoords="offset points", fontsize=6.2, color=VERD, fontfamily=STRUCT)
    ax.annotate("23:00", (D.CS_X[-1], D.CS_Y[-1]), xytext=(-6, -10),
                textcoords="offset points", fontsize=6.2, color=ALERT, fontfamily=STRUCT)
    ax.set_xlabel("Latensi rerata per jam (ms)", fontsize=6.8)
    ax.set_ylabel("Jitter per jam (ms)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "both"
    return _save(fig, None, out, title, 128)

def v69_cat_scatter(out, title):
    fig = canvas(W128, 58); ax = fig.add_subplot(111)
    for i, (nm, vals) in enumerate(D.CAT_SCAT.items()):
        rng = np.random.default_rng(SEED + 69 + i)
        ax.plot(i + 1 + rng.uniform(-0.12, 0.12, len(vals)), vals, "o", ms=3,
                color=CAT_SERIES[i], zorder=3)
        ax.plot(i + 1, vals.mean(), "_", color=SIGNAL, ms=14, mew=1.5, zorder=4)
    ax.set_xticks([1, 2, 3]); ax.set_xticklabels(list(D.CAT_SCAT.keys()), fontfamily=STRUCT)
    ax.set_ylabel("Durasi backup baterai UPS (jam)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128)

def v70_hexbin(out, title):
    fig = canvas(W128, 64); ax = fig.add_subplot(111)
    hb = ax.hexbin(D.SCAT_X, D.SCAT_Y, gridsize=9, cmap=RAMP, mincnt=1,
                   edgecolors=PAPER, linewidths=0.6)
    cb = fig.colorbar(hb, ax=ax, fraction=0.04, pad=0.02)
    cb.outline.set_edgecolor(INK400); cb.ax.tick_params(labelsize=6.0, colors=INK400)
    cb.set_label("jumlah titik", fontsize=6.4, color=INK700)
    ax.set_xlabel("Harga paket (juta Rp)", fontsize=6.8)
    ax.set_ylabel("Throughput uji (Mbps)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "both"
    return _save(fig, None, out, title, 128)

def v71_contour(out, title):
    fig = canvas(W128, 64); ax = fig.add_subplot(111)
    gx = np.linspace(0, 10, 60); gy = np.linspace(0, 6, 40)
    X, Y = np.meshgrid(gx, gy)
    Z = D.medan_sinyal(X, Y)
    cf = ax.contourf(X, Y, Z, levels=8, cmap=RAMP)
    cs = ax.contour(X, Y, Z, levels=8, colors=INK400, linewidths=0.4)
    ax.clabel(cs, fmt="%.0f", fontsize=5.8)
    ax.set_xlabel("X (meter relatif denah)", fontsize=6.8)
    ax.set_ylabel("Y (meter relatif denah)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128, "medan kekuatan sinyal sintetis")

def v72_quadrant(out, title):
    fig = canvas(W166, 70); ax = fig.add_subplot(111)
    mx = np.median(D.SCAT_X); my = np.median(D.SCAT_Y)
    ax.axvline(mx, color=INK400, lw=0.8, ls=(0, (4, 3)))
    ax.axhline(my, color=INK400, lw=0.8, ls=(0, (4, 3)))
    ax.scatter(D.SCAT_X, D.SCAT_Y, s=18, color=INK900, zorder=3)
    for idx, nm in D.SCAT_ANNOT.items():
        ax.annotate(nm, (D.SCAT_X[idx], D.SCAT_Y[idx]), xytext=(5, 4),
                    textcoords="offset points", fontsize=6.2, color=SIGNAL,
                    fontfamily=STRUCT)
    ax.text(0.02, 0.97, "murah & lambat", fontsize=6.2, color=INK400,
            fontfamily=STRUCT, transform=ax.transAxes, va="top")
    ax.text(0.98, 0.97, "mahal & cepat", fontsize=6.2, color=VERD,
            fontfamily=STRUCT, transform=ax.transAxes, va="top", ha="right")
    ax.text(0.98, 0.03, "mahal & lambat", fontsize=6.2, color=ALERT,
            fontfamily=STRUCT, transform=ax.transAxes, va="bottom", ha="right")
    ax.set_xlabel("Harga paket (juta Rp); garis = median", fontsize=6.8)
    ax.set_ylabel("Throughput uji (Mbps)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "both"
    return _save(fig, None, out, title, 166)

def v73_heatmap(out, title):
    fig = canvas(W166, 72); ax = fig.add_subplot(111)
    im = ax.imshow(D.SKOR_M, cmap=RAMP, aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(8)); ax.set_xticklabels(D.FAKTOR, fontfamily=STRUCT)
    ax.set_yticks(range(6)); ax.set_yticklabels(D.NAMA_SITE6, fontfamily=STRUCT)
    for i in range(6):
        for j in range(8):
            ax.text(j, i, "%.2f" % D.SKOR_M[i, j], ha="center", va="center",
                    fontsize=6.0, fontfamily=MONO,
                    color=PAPER if D.SKOR_M[i, j] > 0.55 else INK700)
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cb.outline.set_edgecolor(INK400); cb.ax.tick_params(labelsize=6.0, colors=INK400)
    cb.set_label("Skor ternormalisasi", fontsize=6.4, color=INK700)
    ax.set_xlabel("Faktor uji", fontsize=6.8); ax.set_ylabel("Site", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166)

# ---------- K6 ----------
def v79_network(out, title):
    fig = canvas(W166, 74); ax = fig.add_subplot(111)
    for a, b in D.NET_EDGES:
        xa, ya = D.NET_NODES[a]; xb, yb = D.NET_NODES[b]
        hot = (a, b) == D.NET_LINK_UTAMA
        ax.plot([xa, xb], [ya, yb], color=SIGNAL if hot else INK400,
                lw=1.6 if hot else 0.9, zorder=1)
    for nm, (x, y) in D.NET_NODES.items():
        core = nm.startswith("Core")
        ax.add_patch(Rectangle((x - 0.055, y - 0.035), 0.11, 0.07,
                               facecolor=INK900 if core else INK100,
                               edgecolor=INK400, lw=0.6, zorder=3))
        ax.text(x, y, nm, ha="center", va="center", fontsize=6.0, fontfamily=STRUCT,
                color=PAPER if core else INK900, zorder=4)
    ax.set_xlim(0, 1); ax.set_ylim(0.1, 0.92); ax.axis("off")
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166, "tautan trunk Core-DS-2 diwarnai aksen")

def v81_flow(out, title):
    fig = canvas(W166, 70); ax = fig.add_subplot(111)
    pos = {0: (0.5, 0.92), 1: (0.5, 0.76), 2: (0.5, 0.58), 3: (0.28, 0.40),
           4: (0.72, 0.40), 5: (0.5, 0.20)}
    kinds = [s[0] for s in D.FLOW["steps"]]
    for i, (_, txt) in enumerate(D.FLOW["steps"]):
        x, y = pos[i]
        if kinds[i] == "dia":
            ax.add_patch(Polygon([(x, y + 0.055), (x + 0.11, y), (x, y - 0.055),
                                  (x - 0.11, y)], closed=True, facecolor=INK100,
                                 edgecolor=INK700, lw=0.8, zorder=3))
        else:
            ax.add_patch(Rectangle((x - 0.10, y - 0.035), 0.20, 0.07,
                                   facecolor=INK900 if i in (0, 5) else INK100,
                                   edgecolor=INK400, lw=0.6, zorder=3))
        ax.text(x, y, txt, ha="center", va="center", fontsize=6.2, fontfamily=STRUCT,
                color=PAPER if i in (0, 5) else INK900, zorder=4)
    for e in D.FLOW["edges"]:
        a, b = e[0], e[1]
        lab = e[2] if len(e) > 2 else None
        xa, ya = pos[a]; xb, yb = pos[b]
        ax.add_patch(FancyArrow(xa, ya - 0.04, xb - xa, yb - ya + 0.05,
                                width=0.004, head_width=0.018, head_length=0.02,
                                color=INK700, length_includes_head=True, zorder=2))
        if lab:
            ax.text((xa + xb) / 2 + 0.02, (ya + yb) / 2, lab, fontsize=6.0,
                    color=SIGNAL, fontfamily=STRUCT)
    ax.set_xlim(0, 1); ax.set_ylim(0.1, 1.0); ax.axis("off")
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166)

# ---------- K7 ----------
def v84_tilemap(out, title):
    fig = canvas(W166, 76); ax = fig.add_subplot(111)
    for r in range(D.TILE_ROWS):
        for c in range(D.TILE_COLS):
            v = D.TILE_SCORE[r, c]
            ax.add_patch(Rectangle((c * 1.08, -r * 1.08), 1.0, 1.0,
                                   facecolor=RAMP(v / 100.0), edgecolor=PAPER, lw=1.2))
            lab = D.TILE_LABEL.get((r, c))
            if lab:
                ax.text(c * 1.08 + 0.5, -r * 1.08 - 0.5, lab, ha="center", va="center",
                        fontsize=6.0, fontfamily=STRUCT,
                        color=PAPER if v > 55 else INK900)
            ax.text(c * 1.08 + 0.92, -r * 1.08 - 0.9, "%d" % v, ha="right", va="bottom",
                    fontsize=5.8, fontfamily=MONO, color=PAPER if v > 55 else INK700)
    ax.set_xlim(-0.2, D.TILE_COLS * 1.08); ax.set_ylim(-D.TILE_ROWS * 1.08, 0.4)
    ax.set_aspect("equal"); ax.axis("off")
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166, "denah skematik gudang; angka = cakupan wifi %")

# ---------- K8 ----------
def v91_waterfall(out, title):
    fig = canvas(W166, 62); ax = fig.add_subplot(111)
    cum = 0.0
    for i, (nm, dv) in enumerate(D.WATERFALL):
        col = INK900 if i == 0 else (SIGNAL if dv > 0 else ALERT)
        if i == 0:
            ax.bar(i, dv, color=INK900, width=0.55, zorder=3)
            cum = dv
        else:
            ax.bar(i, dv, bottom=cum, color=col, width=0.55, zorder=3)
            cum += dv
    ax.bar(len(D.WATERFALL), cum, color=INK700, width=0.55, zorder=3)
    labels = [s[0] for s in D.WATERFALL] + ["TOTAL"]
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontfamily=STRUCT,
                                                          fontsize=6.0, rotation=15,
                                                          ha="right")
    ax.axhline(0, color=INK400, lw=0.6)
    ax.set_ylabel("Biaya RAB (juta Rp)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 166)

def v94_gantt(out, title):
    fig = canvas(W166, 62); ax = fig.add_subplot(111)
    for i, (nm, start, dur) in enumerate(D.GANTT):
        y = len(D.GANTT) - 1 - i
        ax.barh(y, dur, left=start, height=0.55, color=INK900, zorder=3)
        mono_label(ax, start + dur + 0.15, y, "M%d-%d" % (start, start + dur),
                   va="center", fontsize=5.8)
    ms, _ = D.GANTT_MILESTONE
    ax.plot(ms, len(D.GANTT) - 0.4, "D", ms=6, color=SIGNAL, zorder=4)
    ax.text(ms + 0.2, len(D.GANTT) - 0.4, D.GANTT_MILESTONE[1], fontsize=6.2,
            color=SIGNAL, fontfamily=STRUCT, va="center")
    ax.set_yticks(range(len(D.GANTT)))
    ax.set_yticklabels([g[0] for g in D.GANTT][::-1], fontfamily=STRUCT)
    ax.set_xlim(0, 16); ax.set_xticks(range(0, 16, 2))
    ax.set_xlabel("Minggu proyek", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "x"
    return _save(fig, None, out, title, 166)

def v95_bullet(out, title):
    fig = canvas(W128, 30); ax = fig.add_subplot(111)
    ax.barh([0], [D.BULLET["max"]], color=INK100, height=0.72, zorder=1)
    ax.barh([0], [D.BULLET["max"] * 0.6], color=INK200, height=0.72, zorder=2)
    ax.barh([0], [D.BULLET["max"] * 0.8], color=INK100, height=0.72, zorder=1)
    ax.barh([0], [D.BULLET["value"]], color=INK900, height=0.34, zorder=3)
    ax.plot([D.BULLET["target"]] * 2, [-0.30, 0.30], color=ALERT, lw=2.2, zorder=4)
    mono_label(ax, D.BULLET["value"] - 1.5, 0.42, "%.0f%%" % D.BULLET["value"],
               ha="right", fontsize=6.4)
    ax.set_yticks([]); ax.set_xlim(0, D.BULLET["max"])
    ax.set_xlabel("%s - target garis merah %.0f%%" % (D.BULLET["label"], D.BULLET["target"]),
                  fontsize=6.6)
    for s in ("left", "top"):
        ax.spines[s].set_visible(False)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128)

def v99_control(out, title):
    fig = canvas(W128, 58); ax = fig.add_subplot(111)
    xs = np.arange(1, 31)
    ucl = D.CTRL_CL + 3 * D.CTRL_SIGMA; lcl = D.CTRL_CL - 3 * D.CTRL_SIGMA
    ax.axhline(D.CTRL_CL, color=INK400, lw=0.8)
    ax.axhline(ucl, color=ALERT, lw=0.8, ls=(0, (4, 3)))
    ax.axhline(lcl, color=ALERT, lw=0.8, ls=(0, (4, 3)))
    breach = D.CTRL < lcl
    ax.plot(xs, D.CTRL, color=INK900, lw=1.1, zorder=3)
    ax.plot(xs[~breach], D.CTRL[~breach], "o", ms=3, color=INK900, zorder=4)
    ax.plot(xs[breach], D.CTRL[breach], "o", ms=5, color=ALERT, zorder=5)
    ax.text(30.4, D.CTRL_CL, " CL", fontsize=6.0, color=INK400, fontfamily=MONO, va="center")
    ax.text(30.4, ucl, " UCL", fontsize=6.0, color=ALERT, fontfamily=MONO, va="center")
    ax.text(30.4, lcl, " LCL", fontsize=6.0, color=ALERT, fontfamily=MONO, va="center")
    ax.set_xlim(1, 33); ax.set_ylim(lcl - 1.2, ucl + 1.2)
    ax.set_xlabel("Hari observasi ke-", fontsize=6.8)
    ax.set_ylabel("Ketersediaan harian (%)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128)

# =================================================================
# PASANGAN SALAH-BENAR (aturan presisi kunci)
# =================================================================
def ap01_salah(out, title):
    fig = canvas(W128, 52); ax = fig.add_subplot(111)
    ax.bar(D.AP_BAR_KAT, D.AP_BAR_VAL, color=INK900, width=0.55, zorder=3)
    ax.set_ylim(40, 48)                      # BASELINE TERPOTONG = cacat yang ditunjukkan
    ax.set_ylabel("Produksi energi (MWh)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128, "SALAH: sumbu Y tidak dimulai dari nol")

def ap01_benar(out, title):
    fig = canvas(W128, 52); ax = fig.add_subplot(111)
    ax.bar(D.AP_BAR_KAT, D.AP_BAR_VAL, color=INK900, width=0.55, zorder=3)
    ax.set_ylim(0, 50)
    for i, v in enumerate(D.AP_BAR_VAL):
        mono_label(ax, i, v + 0.8, "%.1f" % v, ha="center")
    ax.set_ylabel("Produksi energi (MWh)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 128, "BENAR: batang panjangnya jujur dari nol")

def ap02_salah(out, title):
    fig = canvas(W128, 66); ax = fig.add_subplot(111)
    vals = [p[1] for p in D.AP_PIE_PARTS]
    cols = [INK900, SIGNAL, VERD, INK400, ALERT, INK200, INK700, INK100]
    ax.pie(vals, colors=cols[:len(vals)], startangle=90, counterclock=False,
           wedgeprops=dict(edgecolor=PAPER, lw=0.6))
    ax.text(0, -1.35, "delapan iris sulit dibandingkan + warna habis", fontsize=6.2,
            color=ALERT, ha="center", fontfamily=STRUCT)
    ax.set_aspect("equal")
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 128,
                 "SALAH: pie overload >3 iris (diharamkan SV-GRA-02)")

def ap02_benar(out, title):
    fig = canvas(W166, 44); ax = fig.add_subplot(111)
    vals = [p[1] for p in D.AP_PIE_PARTS]
    names = [p[0] for p in D.AP_PIE_PARTS]
    o = np.argsort(vals)[::-1]
    left = 0.0
    for k, i in enumerate(o):
        v = vals[i]
        col = INK900 if k == 0 else (INK400 if k == 1 else INK200)
        ax.barh([0], [v], left=left, height=0.5, color=col, zorder=3)
        if v >= 8:
            ax.text(left + v / 2, 0, "%d%%" % v, ha="center", va="center",
                    fontsize=6.0, fontfamily=MONO,
                    color=PAPER if col == INK900 else INK700)
        left += v
    ax.set_yticks([0]); ax.set_yticklabels(["Komposisi kontrak"], fontfamily=STRUCT)
    ax.set_xlim(0, 100)
    txt = "   ".join("%s %d%%" % (names[i], vals[i]) for i in o)
    ax.text(0, 0.42, txt, fontsize=5.8, color=INK700, fontfamily=STRUCT, ha="left")
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166,
                 "BENAR: satu batang tersusun berperingkat, label langsung")

def ap03_salah(out, title):
    fig = canvas(W166, 58); ax = fig.add_subplot(111)
    ax.plot(D.AP_DUAL_X, D.AP_DUAL_A, color=INK900, lw=1.3)
    ax2 = ax.twinx()
    ax2.plot(D.AP_DUAL_X, D.AP_DUAL_B, color=SIGNAL, lw=1.3)
    ax2.spines["top"].set_visible(False)
    ax.set_ylim(9.5, 14.5); ax2.set_ylim(0, 100)   # sumbu manipulate agar tampak sejalan
    ax.set_ylabel("Indeks harga (skala dipersempit)", fontsize=6.4, color=INK900)
    ax2.set_ylabel("Unit terjual", fontsize=6.4, color=SIGNAL)
    ax2.tick_params(colors=INK400, labelsize=6.5, length=0)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166,
                 "SALAH: dual-axis disejajarkan paksa = korelasi palsu")

def ap03_benar(out, title):
    fig = canvas(W166, 62)
    a1 = fig.add_subplot(2, 1, 1)
    a1.plot(D.AP_DUAL_X, D.AP_DUAL_A, color=INK900, lw=1.3)
    a1.set_ylabel("Indeks harga", fontsize=6.4)
    a2 = fig.add_subplot(2, 1, 2, sharex=a1)
    a2.plot(D.AP_DUAL_X, D.AP_DUAL_B, color=SIGNAL, lw=1.3)
    a2.set_ylabel("Unit terjual", fontsize=6.4)
    a2.set_xlabel("Bulan 2026", fontsize=6.8)
    for ax_ in (a1, a2):
        style_ax(ax_, grid_axis="y")
    fig.tight_layout(rect=(0.01, 0.05, 1, 0.94))
    fig.text(0.01, 0.985, title, fontsize=8.0, color=INK900, fontweight="bold",
             fontfamily=STRUCT, va="top")
    fig.text(0.01, -0.075, "%s - seed %d | BENAR: dua panel kecil sejajar (small multiples)"
             % (CAPTION_LABEL, SEED), fontsize=6.0, color=INK400,
             fontfamily=MONO, va="bottom")
    fig.canvas.draw()
    mp = measure_min_pt(fig)
    fig.savefig(out, dpi=DPI, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)
    return mp

def ap04_salah(out, title):
    fig = canvas(W166, 60); ax = fig.add_subplot(111)
    m = np.arange(1, 13)
    for i, (nm, ser) in enumerate(D.AP_LEG_SERI.items()):
        ax.plot(m, ser, color=CAT_SERIES[i], lw=1.2)
    leg = ax.legend(loc="upper right", frameon=True, fontsize=6.2, title="Legenda jauh")
    leg.get_frame().set_edgecolor(INK200)
    ax.set_ylabel("Bitrate (Mbps)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 166,
                 "SALAH: kotak legenda jauh - mata bolak-balik, seri tertutup")

def ap04_benar(out, title):
    fig = canvas(W166, 60); ax = fig.add_subplot(111)
    m = np.arange(1, 13)
    for i, (nm, ser) in enumerate(D.AP_LEG_SERI.items()):
        ax.plot(m, ser, color=CAT_SERIES[i], lw=1.2)
        ax.text(12.25, ser[-1], nm, color=CAT_SERIES[i], fontsize=6.2,
                va="center", fontfamily=STRUCT)
    ax.set_xlim(1, 15.4)
    ax.set_ylabel("Bitrate (Mbps)", fontsize=6.8)
    fn_ax[0] = ax; fn_grid[0] = "y"
    return _save(fig, None, out, title, 166,
                 "BENAR: label langsung di ujung seri, tanpa kotak legenda")

def v3d_helper(fig_data, out, title, three_d, extra):
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    fig = canvas(W128, 62)
    if three_d:
        ax = fig.add_subplot(111, projection="3d")
        xs = np.arange(4); ys = np.arange(3)
        for j, y in enumerate(ys):
            ax.bar3d(xs, np.full(4, y), np.zeros(4), 0.6, 0.6,
                     np.array(D.AP_BAR_VAL) * (1 - 0.15 * j), color=INK400,
                     edgecolor=INK700)
        ax.set_zlabel("MWh", fontsize=6.2)
        ax.tick_params(labelsize=5.8)
    else:
        ax = fig.add_subplot(111)
        for j in range(3):
            ax.bar(np.arange(4) + j * 0.27 - 0.27,
                   np.array(D.AP_BAR_VAL) * (1 - 0.15 * j), width=0.26,
                   color=[INK900, INK400, INK200][j], zorder=3)
        ax.set_xticks(np.arange(4)); ax.set_xticklabels(D.AP_BAR_KAT, fontfamily=STRUCT)
        ax.text(3.6, max(D.AP_BAR_VAL) * 1.02, "\u25a0 Q1  \u25a0 Q2  \u25a1 Q3",
                fontsize=6.2, color=INK700, fontfamily=GLIF)
        ax.set_ylabel("Produksi (MWh)", fontsize=6.8)
    fig.text(0.01, 0.985, title, fontsize=8.0, color=INK900, fontweight="bold",
             fontfamily=STRUCT, va="top")
    fig.text(0.01, -0.075, "%s - seed %d | %s" % (CAPTION_LABEL, SEED, extra),
             fontsize=6.0, color=INK400, fontfamily=MONO, va="bottom")
    fig.tight_layout(rect=(0.01, 0.06, 1, 0.93))
    fig.canvas.draw()
    mp = measure_min_pt(fig)
    fig.savefig(out, dpi=DPI, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)
    return mp

def ap05_salah(out, title):
    return v3d_helper(None, out, title, True,
                      "SALAH: 3-D + kedalaman palsu memelintir perbandingan tinggi")

def ap05_benar(out, title):
    return v3d_helper(None, out, title, False,
                      "BENAR: grouped bar datar, selisih terbaca lurus")

def ap06_salah(out, title):
    fig = canvas(W166, 66); ax = fig.add_subplot(111)
    im = ax.imshow(D.SKOR_M, cmap="turbo", aspect="auto")   # RAINBOW = cacat yang ditunjukkan
    cb = fig.colorbar(im, ax=ax, fraction=0.03)
    cb.ax.tick_params(labelsize=6.0)
    ax.set_xlabel("rainbow turbo: urutan hue tidak monotonik persepsi", fontsize=6.4)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166,
                 "SALAH: colormap rainbow/turbo (dihambat SV-GRA-13)")

def ap06_benar(out, title):
    fig = canvas(W166, 66); ax = fig.add_subplot(111)
    im = ax.imshow(D.SKOR_M, cmap=RAMP, aspect="auto", vmin=0, vmax=1)
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cb.outline.set_edgecolor(INK400); cb.ax.tick_params(labelsize=6.0, colors=INK400)
    cb.set_label("Skor", fontsize=6.4, color=INK700)
    ax.set_xlabel("ramp sekuensial satu hue dari tokens (gelap = tinggi)", fontsize=6.4)
    fn_ax[0] = ax; fn_grid[0] = None
    return _save(fig, None, out, title, 166,
                 "BENAR: ramp sekuensial token, monotonik dan fotokopi-selamat")

# ---------- warisan: datum_chart_buku (famili threshold) ----------
def legacy_threshold(out, title):
    tk = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-10-06-prompt-manual-v2/toolkit"
    if not os.path.isdir(tk):
        raise ImportError("toolkit warisan tidak ada di disk: %s" % tk)
    sys.path.insert(0, tk)
    import datum_chart_buku as dcb
    captured = {}
    orig = matplotlib.figure.Figure.savefig
    def spy(self, fname, *a, **kw):
        captured["fig"] = self
        return orig(self, fname, *a, **kw)
    matplotlib.figure.Figure.savefig = spy
    try:
        dcb.chart_bar2rute(out, ["RT-01", "RT-02", "RT-03", "RT-04", "RT-05"],
                           [52.4, 58.1, 49.7, 61.3, 44.0],
                           [48.9, 55.2, 53.4, 50.1, 47.8],
                           nama_a="Rute utama", nama_b="Rute cadangan",
                           title=title, ylabel="Kebisingan dB(A)",
                           threshold=55.0, threshold_label="batas KAK 55,0",
                           width_mm=128.0)
    finally:
        matplotlib.figure.Figure.savefig = orig
    mp = measure_min_pt(captured["fig"]) if "fig" in captured else 5.5
    return mp

# =================================================================
# REGISTRASI ENTRI
# =================================================================
def build_registry():
    E = entry
    E("VC-01", "Bar chart", "K1", 128, 62, "r1_bar_ranking",
      "Peringkat nilai penawaran lima perangkat utama.", v01_bar_ranking)
    E("VC-02", "Column chart", "K1", 128, 52, "r3_column_time",
      "Volume proyek per tahun (deret waktu diskret).", v02_column_time)
    E("VC-03", "Grouped bar chart", "K1", 166, 62, "r1 varian grouped",
      "Bandingkan dua vendor pada perangkat yang sama.", v03_grouped_bar)
    E("VC-04", "Grouped column chart", "K1", 166, 58, "r3 varian grouped",
      "Kolom berkelompok dua rute penawaran.", v04_grouped_column)
    E("VC-05", "Lollipop chart", "K1", 128, 58, "r1 varian lollipop",
      "Titik nilai dengan tangkai - alternatif hemat tinta.", v05_lollipop)
    E("VC-06", "Dot plot", "K1", 128, 60, "dot variansi (setara datum_chart_buku)",
      "Sebaran ulangan MTBF per site dengan rentang dan rerata.", v06_dotplot)
    E("VC-07", "Dumbbell chart", "K1", 166, 62, "dot plot + konektor",
      "Geseran skor audit H1 ke H2 per objek.", v07_dumbbell)
    E("VC-09", "Range plot", "K1", 128, 58, "rentang min-maks per kategori",
      "Rentang arus operasional tiga panel.", v09_range)
    E("VC-11", "Slope chart", "K1", 166, 62, "r2 varian dua titik",
      "Naik-turun skor audit antar dua periode.", v11_slope)
    E("VC-12", "Matrix chart", "K1", 166, 70, "r9 varian simbol",
      "Matriks site x faktor uji dengan simbol bobot teks.", v12_matrix)
    E("VC-13", "Small multiples", "K1", 166, 74, "kisi facets token-driven",
      "Tren bitrate enam site pada skala bersama.", v13_small_multiples)
    E("VC-15", "Table chart", "K1", 128, 46, "jalur tabel DATUM (pratinjau PNG)",
      "Tabel status site dengan anotasi warna ambang.", v15_table)
    E("VC-16", "Pareto chart", "K1", 166, 62, "r8_pareto",
      "Hukum 80/20 penyebab gangguan jaringan.", v16_pareto)
    E("VC-19", "Stacked bar chart", "K2", 166, 50, "r10_share (100%)",
      "Komposisi anggaran tiga proyek dinormalisasi 100%.", v19_stacked_bar)
    E("VC-20", "Stacked column chart", "K2", 128, 58, "r10 varian absolut",
      "Beban daya empat komponen enam bulan.", v20_stacked_column)
    E("VC-21", "Diverging bar chart", "K2", 166, 58, "r1 baseline tengah",
      "Survei kepuasan: setuju vs tidak setuju per aspek.", v21_diverging_bar)
    E("VC-22", "Diverging column chart", "K2", 128, 58, "varian diverging vertikal",
      "Bentuk kolom dari selisih respons survei.", v22_diverging_column)
    E("VC-23", "Population pyramid", "K2", 166, 58, "diverging dua sisi",
      "Piramida jenjang personel tim lapangan vs kantor.", v23_pyramid)
    E("VC-24", "Waffle chart", "K2", 128, 78, "grid kotak tanpa glif",
      "Status pengujian 100 titik kamera (1 kotak 1 persen).", v24_waffle)
    E("VC-25", "Square area chart", "K2", 128, 60, "varian icon chart kotak",
      "Luas persegi menandai jumlah titik kamera per site.", v25_square_area)
    E("VC-26", "Icon chart", "K2", 128, 56, "putusan C2: lingkaran luas proporsional",
      "Padanan icon chart tanpa pustaka glif berlisensi.", v26_icon_circles)
    E("VC-31", "Marimekko chart", "K2", 166, 66, "putusan C2: mosaic matplotlib",
      "Segmen pasar: lebar porsi tender, tinggi rasio menang.", v31_marimekko)
    E("VC-32", "Treemap", "K2", 166, 70, "putusan C2: slice-dice deterministik",
      "Biaya subpaket dalam divisi proyek (luas = juta Rp).", v32_treemap)
    E("VC-36", "Dendrogram", "K2", 166, 58, "pohon dari merge beku",
      "Kemiripan profil beban antar gardu.", v36_dendro)
    E("VC-37", "Funnel chart", "K2", 128, 62, "putusan C2: trapesium bertumpuk",
      "Corong proses pengadaan dari dokumen masuk ke kontrak.", v37_funnel)
    E("VC-40", "Org chart", "K2", 166, 66, "pohon tiga tingkat (datum_diagram setara)",
      "Struktur project office tiga tingkat.", v40_org)
    E("VC-41", "Line chart", "K3", 128, 56, "r2_line_trend",
      "Tren bitrate dua site setahun, label langsung.", v41_line)
    E("VC-42", "Area chart", "K3", 128, 54, "fill-between token-driven",
      "Beban puncak bulanan sebagai volume terisi.", v42_area)
    E("VC-43", "Stacked area chart", "K3", 166, 60, "varian area bertumpuk",
      "Agregat bitrate tiga site (total + komposisi).", v43_stacked_area)
    E("VC-45", "Bump chart", "K3", 166, 62, "varian line peringkat terbalik",
      "Peringkat vendor bergeser antar kuartal.", v45_bump)
    E("VC-47", "Spline chart", "K3", 128, 56, "r2 varian penghalusan",
      "Garis halus di atas titik asli - interpolasi diumumkan.", v47_spline)
    E("VC-48", "Step line chart", "K3", 128, 54, "r2 varian drawstyle steps",
      "Tarif listrik berubah mendadak - tangga jujur.", v48_step)
    E("VC-49", "Calendar heatmap", "K3", 166, 44, "grid tanggal + ramp token",
      "Kepadatan tiket harian sepanjang 2026.", v49_calendar)
    E("VC-50", "Fan chart", "K3", 166, 60, "fill_between berlapis + median",
      "Proyeksi titik kamera dengan pita ketidakpastian.", v50_fan)
    E("VC-51", "Sparkline", "K3", 128, 44, "mini line dalam sel tabel",
      "Lima metrik ringkas ala sel laporan.", v51_spark)
    E("VC-52", "Histogram", "K4", 128, 54, "r6_histogram",
      "Distribusi throughput 500 sampel, bin tetap.", v52_hist)
    E("VC-53", "Density plot", "K4", 128, 54, "KDE Silverman + fill",
      "Kerapatan throughput tanpa batas bin.", v53_density)
    E("VC-54", "Box plot", "K4", 128, 56, "r7_boxplot",
      "Ringkasan kuartil MTBF tiga site.", v54_box)
    E("VC-55", "Violin plot", "K4", 128, 56, "varian r7 + kde",
      "Bentuk distribusi MTBF lengkap dengan kuartil.", v55_violin)
    E("VC-56", "Strip plot", "K4", 128, 54, "strip tanpa jitter",
      "Semua observasi MTBF per site apa adanya.", v56_strip)
    E("VC-57", "Jitter plot", "K4", 128, 54, "strip + jitter seeded",
      "Observasi digeser horizontal seeded agar tidak bertumpuk.", v57_jitter)
    E("VC-59", "Ridgeline plot", "K4", 166, 66, "ggridges-style matplotlib",
      "Distribusi MTBF tiga site ditumpuk vertikal.", v59_ridge)
    E("VC-60", "Barcode chart", "K4", 128, 40, "garis tipis kolektif",
      "Kepadatan RTT 400 sampel dengan median.", v60_barcode)
    E("VC-61", "One-dimensional heatmap", "K4", 166, 34, "pita colormap token",
      "Intensitas gangguan sepanjang satu hari.", v61_heat1d)
    E("VC-63", "ECDF chart", "K4", 128, 54, "langkah kumulatif",
      "Proporsi RTT di bawah nilai - p50/p95 terbaca.", v63_ecdf)
    E("VC-65", "Error bar chart", "K4", 128, 56, "r1 varian errorbar",
      "Latensi rerata per operator dengan simpangan baku.", v65_errorbar)
    E("VC-66", "Scatter plot", "K5", 128, 66, "scatter baru C2 (lubang prioritas)",
      "Harga vs throughput 24 paket, empat kit diberi nama.", v66_scatter)
    E("VC-67", "Bubble chart", "K5", 128, 66, "scatter varian bubble",
      "Dimensi ketiga garansi lewat luas gelembung.", v67_bubble)
    E("VC-68", "Connected scatter plot", "K5", 128, 60, "scatter varian konektor",
      "Trajektori latency-jitter sepanjang hari.", v68_conn_scatter)
    E("VC-69", "Categorical scatter plot", "K5", 128, 58, "scatter sumbu kategori",
      "Durasi backup UPS per merek dengan rerata aksen.", v69_cat_scatter)
    E("VC-70", "Hexagonal binning", "K5", 128, 64, "hexbin matplotlib + ramp token",
      "Kerapatan titik harga-throughput per heksagon.", v70_hexbin)
    E("VC-71", "Contour plot", "K5", 128, 64, "contour token",
      "Medan kekuatan sinyal area parkir.", v71_contour)
    E("VC-72", "Quadrant chart", "K5", 166, 70, "scatter + garis median",
      "Kuadran murah-cepat untuk seleksi paket.", v72_quadrant)
    E("VC-73", "Heatmap (matrix)", "K5", 166, 72, "r9_heatmap",
      "Matriks skor site x faktor uji dengan angka sel.", v73_heatmap)
    E("VC-79", "Network diagram", "K6", 166, 74, "topologi koordinat tetap",
      "Topologi distro core-distribution-access, trunk diaksen.", v79_network)
    E("VC-81", "Flowchart", "K6", 166, 70, "flow/swimlane registri DIA",
      "Alur triase tiket dengan cabang prioritas.", v81_flow)
    E("VC-84", "Tile map", "K7", 166, 76, "grid tile skematik + ramp token",
      "Denah skematik gudang: cakupan wifi per zona ubin.", v84_tilemap)
    E("VC-91", "Waterfall chart", "K8", 166, 62, "r5_waterfall",
      "Susunan RAB dari peralatan sampai total.", v91_waterfall)
    E("VC-94", "Gantt chart", "K8", 166, 62, "swimlane/sequence mingguan",
      "Jadwal proyek tujuh tugas plus milestone serah terima.", v94_gantt)
    E("VC-95", "Bullet chart", "K8", 128, 30, "r4_bullet",
      "SLA aktual vs target dalam sepenggal garis.", v95_bullet)
    E("VC-99", "Control chart", "K8", 128, 58, "line + CL/UCL/LCL",
      "Ketersediaan harian dengan pelanggaran LCL ditandai.", v99_control)
    # pasangan salah-benar
    E("AP-01S", "Baseline terpotong (SALAH)", "AP", 128, 52, "pasangan presisi",
      "Contoh keliru: kolom sumbu Y dipotong.", ap01_salah)
    E("AP-01B", "Baseline nol (BENAR)", "AP", 128, 52, "pasangan presisi",
      "Perbaikan: sumbu mulai nol, nilai dilabeli.", ap01_benar)
    E("AP-02S", "Pie overload (SALAH)", "AP", 128, 66, "pasangan presisi",
      "Contoh keliru: delapan iris pie.", ap02_salah)
    E("AP-02B", "Batang tersusun (BENAR)", "AP", 166, 44, "pasangan presisi",
      "Perbaikan: satu batang berperingkat.", ap02_benar)
    E("AP-03S", "Dual-axis menyesatkan (SALAH)", "AP", 166, 58, "pasangan presisi",
      "Contoh keliru: dua sumbu disejajarkan paksa.", ap03_salah)
    E("AP-03B", "Dua panel sejajar (BENAR)", "AP", 166, 62, "pasangan presisi",
      "Perbaikan: panel kecil berbagi sumbu-x.", ap03_benar)
    E("AP-04S", "Legenda jauh (SALAH)", "AP", 166, 60, "pasangan presisi",
      "Contoh keliru: kotak legenda di pojok.", ap04_salah)
    E("AP-04B", "Label langsung (BENAR)", "AP", 166, 60, "pasangan presisi",
      "Perbaikan: nama seri di ujung garis.", ap04_benar)
    E("AP-05S", "3-D/volume (SALAH)", "AP", 128, 62, "pasangan presisi",
      "Contoh keliru: perspektif 3-D memelintir tinggi.", ap05_salah)
    E("AP-05B", "Grouped datar (BENAR)", "AP", 128, 62, "pasangan presisi",
      "Perbaikan: grouped bar datar terbaca lurus.", ap05_benar)
    E("AP-06S", "Rainbow colormap (SALAH)", "AP", 166, 66, "pasangan presisi",
      "Contoh keliru: turbo/rainbow pada matriks skor.", ap06_salah)
    E("AP-06B", "Ramp sekuensial token (BENAR)", "AP", 166, 66, "pasangan presisi",
      "Perbaikan: ramp satu hue dari tokens.", ap06_benar)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="direktori tujuan (berisi render/)")
    ap.add_argument("--check-min-pt", action="store_true",
                    help="exit 1 bila ada figur dengan teks terkecil < 5,5 pt (DATUM-28)")
    args = ap.parse_args()
    out_dir = args.out
    png_dir = os.path.join(out_dir, "render")
    os.makedirs(png_dir, exist_ok=True)

    reg = []
    build_registry()
    manifest = []
    for item in REGISTRY:
        fn_ax[0] = None; fn_grid[0] = None
        fname = ("%s__%s.png" % (item["id"], item["nama"].lower()
                                 .replace(" ", "-").replace("/", "-")
                                 .replace("(", "").replace(")", "")))
        path = os.path.join(png_dir, fname)
        min_pt = item["fn"](path, "%s (%s)" % (item["nama"], item["id"]))
        blob = open(path, "rb").read()
        manifest.append(dict(
            id=item["id"], file="render/" + fname,
            sha256=hashlib.sha256(blob).hexdigest(),
            lebar_mm=item["lebar_mm"], tinggi_mm=item["tinggi_mm"],
            font_min_pt=round(float(min_pt), 2),
            font_min_px=round(float(min_pt) * DPI / 72.0, 1),
            resep=item["resep"], kelas=item["kelas"],
            caption="%s - %s | %s" % (item["nama"], item["caption"].rstrip("."),
                                      CAPTION_LABEL),
            data_seed=SEED))
        print("OK %-7s %-46s min_pt=%.1f min_px=%.1f" %
              (item["id"], fname, min_pt, min_pt * DPI / 72.0))

    # warisan (OPSIONAL sejak promosi registry 08-10)
    fn_ax[0] = None; fn_grid[0] = None
    warisan_catatan = ""
    try:
        leg_path = os.path.join(png_dir, "LEGACY-THRESHOLD__datum-chart-buku.png")
        mp = legacy_threshold(leg_path, "Kebisingan dua rute vs batas KAK (warisan)")
        blob = open(leg_path, "rb").read()
        manifest.append(dict(
            id="LEGACY-THRESHOLD", file="render/LEGACY-THRESHOLD__datum-chart-buku.png",
            sha256=hashlib.sha256(blob).hexdigest(), lebar_mm=128, tinggi_mm=74,
            font_min_pt=round(float(mp), 2), font_min_px=round(float(mp) * DPI / 72.0, 1),
            resep="datum_chart_buku.chart_bar2rute (engine warisan, tanpa modifikasi)",
            kelas="WARISAN",
            caption="Pembanding warisan famili threshold - engine datum_chart_buku.py "
                    "(padanan hidup datumchart.py yang hilang per GAP-09/TA-07). %s" % CAPTION_LABEL,
            data_seed=SEED))
        print("OK LEGACY   min_pt=%.1f" % mp)
    except ImportError as e:
        warisan_catatan = "Blok warisan DILEWATI (%s). " % e

    meta = dict(
        versi_engine="pustakachart v1.0 (promosi VCTL-1007 C2 rev0, ENH-A 08-10)",
        tokens_path=TOKENS_PATH,
        tokens_sha256=hashlib.sha256(open(TOKENS_PATH, "rb").read()).hexdigest(),
        python=sys.version.split()[0],
        matplotlib=matplotlib.__version__, numpy=np.__version__,
        dpi=DPI, seed=SEED,
        fonts=dict(structural=", ".join(FONT_CHAINS[0]), reading=", ".join(FONT_CHAINS[1]),
                   data=", ".join(FONT_CHAINS[2]), sans=", ".join(FONT_CHAINS[3]),
                   plex_added=FONTS_ADDED),
        catatan=(warisan_catatan + "datumchart.py tidak ada di disk (GAP-09/TA-07); pembanding warisan "
                "dipenuhi lewat datum_chart_buku.py tanpa modifikasi. VC-35 Sunburst "
                "TIDAK DIRENDER: putusan C2 - keluarga radial diharamkan vonis "
                "SV-GRA-02/pie fleet; kebutuhan ditutup VC-19/VC-32."),
        entries=manifest)
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2, sort_keys=False)

    lines = ["# Katalog gambar contoh chart (siap tempel manual)", "",
             "Engine: scripts/render_chart_examples.py | seed %d | %s %s / numpy %s | "
             "PNG %d dpi | tokens runtime: %s" %
             (SEED, "matplotlib", matplotlib.__version__, np.__version__, DPI,
              TOKENS_PATH), "",
             "| id | berkas | lebar_mm | font_min_px | caption |",
             "|---|---|---|---|---|"]
    for m in manifest:
        lines.append("| %s | %s | %s | %.1f | %s |" %
                     (m["id"], m["file"], m["lebar_mm"], m["font_min_px"], m["caption"]))
    lines += ["", "Catatan putusan C2: VC-35 Sunburst tidak dirender (keluarga radial "
              "diharamkan vonis SV-GRA-02; padanan sah VC-19 stacked share dan VC-32 "
              "treemap). Semua berkas berlabel %s." % CAPTION_LABEL]
    with open(os.path.join(out_dir, "katalog-gambar.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("TOTAL %d PNG | manifest.json | katalog-gambar.md" % len(manifest))
    if args.check_min_pt:
        buruk = [m for m in manifest if m["font_min_pt"] < 5.5]
        for m in buruk:
            print("MIN-PT FAIL %s min_pt=%.2f < 5,5 (DATUM-28)" % (m["id"], m["font_min_pt"]))
        if buruk:
            sys.exit(1)
        print("MIN-PT: semua figur >= 5,5 pt (DATUM-28 bersih)")

if __name__ == "__main__":
    main()
