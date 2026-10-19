# -*- coding: utf-8 -*-
"""
datum_xlsx.py — builder workbook DATUM berbasis token v2.0.0
(kelas builder/render DHS-RB-05, 2026-10-05; kartu t_28d93e3c).

PROVENANS: pola chrome diambil dari garis builder terbukti
build_contoh_datum_xlsx.py (pita klasifikasi dua blok TANPA merged cell, eyebrow
thin-space, blok identitas pasangan label-mono, kunci glif rich-text Mono 9) dan
kontrak STD-SAJI-001 (BLD_saji_check.py, G-SAJI-1..8). Palet/wajah dibaca dari
tokens.json (colour.interior + type.faces) lewat datumbind.tokens_path(); warna
ARGB dibangun dari heks token, tidak ada heks literal di modul ini.
Lint 23 cek W milik datumbuku.py (DHS-RB-03) — modul ini BUKAN lint, hanya
builder yang mencegah cacat sejak situs-panggil (N1 nama lembar, tanpa merge di
zona hitung DATUM-20, kolom angka MONO rata kanan).

Pemakaian:
    from datum_xlsx import DatumWorkbook
    W = DatumWorkbook(title="...", doc_no="00X-...", rev="A")
    W.cover(kicker="...", judul="...", deck="...", identity=[(l,v,l,v), ...])
    ws = W.sheet("RANKING TIER")          # nama dicek N1 (spasi/hubung, bukan '_')
    W.header(ws, ["Peringkat", "Skor", "Catatan"])
    W.row(ws, [1, 97.5, "keterangan"], numeric_cols={1})
    W.save("out.xlsx")
"""
import json, os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

import datumcheck as DC
from datumbind import tokens_path

_TOK = json.load(open(tokens_path(), encoding="utf-8"))
_COL = _TOK["colour"]["interior"]
_WRAP = _TOK["colour"]["wrapper"]
_FACES = _TOK["type"]["faces"]

def argb(tok_hex):
    return "FF" + tok_hex.lstrip("#").upper()

INK = argb(_COL["ink900"]); SLATE = argb(_COL["ink700"]); GRAY = argb(_COL["ink400"])
HAIR = argb(_COL["ink200"]); AMBER = argb(_COL["signal"]); CRIMSON = argb(_COL["alert"])
MAROON = argb(_WRAP["seal"]); VERDI = argb(_COL["verd"]); WHITE = "FFFFFFFF"
LINK = argb(_COL["link"])

F_COND = _FACES["condensed"]; F_SANS = _FACES["workbook_ui"]; F_MONO = _FACES["mono"]
THIN_SP = "\u2009"


def track(tokens):
    """Sambung huruf dalam token dgn thin space; antar token spasi tipis (pola REF B10)."""
    return (THIN_SP + " " + THIN_SP).join(THIN_SP.join(list(t)) for t in tokens)


def font(name, size, bold=False, color=INK):
    return Font(name=name, size=size, bold=bold, color=color)


class DatumWorkbook:
    def __init__(self, title, doc_no, rev, author="", classification="TERBATAS"):
        DC.name_guard(doc_no)
        self.title, self.doc_no, self.rev = title, doc_no, rev
        self.classification = classification
        self.wb = Workbook()
        p = self.wb.properties
        p.title = title
        p.creator = author or "Divisi Engineering PT Gemilang Satria Perkasa"
        p.description = f"{doc_no} Rev {rev}"

    def cover(self, kicker, judul, deck="", identity=()):
        cov = self.wb.active
        cov.title = "COVER"
        cov.sheet_view.showGridLines = False
        cov.sheet_properties.tabColor = MAROON[2:]
        for col, w in {"A": 2.2, "B": 3.0, "C": 20.0, "D": 16.0, "E": 14.0,
                       "F": 10.0, "G": 10.0, "H": 10.0, "I": 10.0, "J": 10.0}.items():
            cov.column_dimensions[col].width = w
        fill = PatternFill("solid", fgColor=MAROON)
        cov["B1"] = "KLASIFIKASI \u00b7 " + self.classification
        cov["B1"].font = font(F_COND, 7.5, True, WHITE)
        cov["G1"] = "REV %s \u00b7 PENGGUNAAN INTERNAL GSP" % self.rev
        cov["G1"].font = font(F_COND, 7.5, True, WHITE)
        cov["G1"].alignment = Alignment(horizontal="right", vertical="center")
        for coord in ("B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1", "J1"):
            cov[coord].fill = fill                     # dua blok fill, tanpa merge
        cov.row_dimensions[1].height = 18
        cov["B10"] = track([kicker]) if kicker else ""
        cov["B10"].font = font(F_COND, 8, True, AMBER)
        cov["B11"] = judul
        cov["B11"].font = font(F_COND, 19, True, INK)
        cov.row_dimensions[11].height = 30
        if deck:
            cov["B12"] = deck
            cov["B12"].font = font(F_SANS, 10.5, True, SLATE)
        r = 14
        for l1, v1, l2, v2 in identity:
            cov[f"B{r}"] = l1; cov[f"B{r}"].font = font(F_COND, 7, True, GRAY)
            cov[f"D{r}"] = v1; cov[f"D{r}"].font = font(F_MONO, 8.5, True, INK)
            cov[f"F{r}"] = l2; cov[f"F{r}"].font = font(F_COND, 7, True, GRAY)
            cov[f"H{r}"] = v2; cov[f"H{r}"].font = font(F_MONO, 8.5, True, INK)
            cov.row_dimensions[r].height = 24
            r += 2
        return cov

    def sheet(self, name, tab_color=None):
        """Nama lembar dicek GUARD-N1 saat dibuat (situs-panggil)."""
        DC.name_guard(name)
        ws = self.wb.create_sheet(name)
        ws.sheet_view.showGridLines = False
        if tab_color:
            ws.sheet_properties.tabColor = tab_color
        return ws

    def header(self, ws, labels, row=3, widths=None):
        """Baris kepala: condensed 7.5 kapital kelabu, hair bawah, tanpa fill."""
        for ci, lab in enumerate(labels, start=2):     # mulai kolom B (A margin)
            c = ws.cell(row=row, column=ci, value=str(lab).upper())
            c.font = font(F_COND, 7.5, True, GRAY)
            c.alignment = Alignment(horizontal="left")
        if widths:
            for ci, w in enumerate(widths, start=2):
                ws.column_dimensions[get_column_letter(ci)].width = w
        # koordinat string: ws.cell() akan membuat sel fantom dan menggeser max_row
        ws.freeze_panes = f"{get_column_letter(2)}{row + 1}"   # bendera panel beku
        return row

    def row(self, ws, values, row=None, numeric_cols=(), marks=None):
        """Baris data: teks Sans, kolom angka MONO rata kanan (G-SAJI pola DOCX
        num-col). `marks` = {idx: glif provenans} dicetak MONO amber."""
        row = row or (ws.max_row + 1)
        for ci, v in enumerate(values, start=2):
            c = ws.cell(row=row, column=ci, value=v)
            idx = ci - 2
            if idx in numeric_cols and isinstance(v, (int, float)):
                c.font = font(F_MONO, 9, False, INK)
                c.alignment = Alignment(horizontal="right")
            else:
                c.font = font(F_SANS, 9, False, SLATE)
        if marks:
            for idx, glif in marks.items():
                c = ws.cell(row=row, column=len(values) + 2)
                c.value = glif
                c.font = font(F_MONO, 9, False, AMBER)
        return row

    def source_line(self, ws, text, row=None):
        row = row or (ws.max_row + 1)
        c = ws.cell(row=row, column=2, value="SUMBER " + text)
        c.font = font(F_MONO, 7, False, GRAY)
        return row

    def save(self, path):
        DC.name_guard(os.path.basename(path))
        self.wb.save(path)
        return path


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
