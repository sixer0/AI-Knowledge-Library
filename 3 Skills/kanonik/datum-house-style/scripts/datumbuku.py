#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
datumbuku.py — lint workbook DATUM: 23 cek W01..W23 atas berkas .xlsx.

PROVENANS (paket datum-house-style v2.0.0, DHS-RB-03 2026-10-05): dibangun dari
nol menurut Standar_Workbook_DATUM_001-GSP-STD-X-2026_RevA §11.1 (23 cek, Tabel
11.2) dan Lampiran A; preseden arsip legacy bukukerja.py dibaca read-only sebagai
contoh bentuk lembar DATUM, bukan sebagai sumber logika lint. Token warna/huruf
dibaca dari tokens.json paket (resolver di samping datumbind.py). Kalibrasi:
nol temuan pada workbook spesimen RAB_Spesimen_UPK-70_000-GSP-RAB-X-2026_RevA.xlsx.

Cara pakai:
    python datumbuku.py BERKAS.xlsx [--json] [--silent]

Kode keluar (Standar §11.1):
    0  bersih - tidak ada temuan yang menahan terbit
    1  ada temuan yang menahan terbit
    2  berkas tidak terbaca

W19 adalah peringatan (Standar §11.2 catatan Tabel 11.2) dan tidak menahan terbit.
Tiga batas lint (§11.3) melekat: pengecualian kolom urut No/Desimal/ID/Rev pada
W02/W04; W04 menilai warna dari teks rumus sehingga tidak bergantung nilai
tembolok; W03 mengizinkan 0, 1, 100, 1.000, 3.600, eksponen bulat dan digit ROUND.
"""

import argparse
import json
import os
import re
import sys
import zipfile

try:
    from openpyxl import load_workbook
    from openpyxl.utils import column_index_from_string, get_column_letter, range_boundaries
except ImportError:  # pragma: no cover
    sys.stderr.write("datumbuku butuh openpyxl: uv run --python 3.11 --with openpyxl python datumbuku.py BERKAS\n")
    raise SystemExit(2)

__all__ = ["lint", "CHECKS", "main"]

# ------------------------------------------------------------------ tabel cek
# (ID, yang ditandai, aturan) — urutan dan bunyi mengikuti Tabel 11.2 Standar 001.
CHECKS = [
    ("W01", "Wajah huruf di luar IBM Plex", "BK-21"),
    ("W02", "Konstanta di luar MASUKAN dan AHS", "BK-02"),
    ("W03", "Literal angka di dalam rumus", "BK-53"),
    ("W04", "Warna angka tidak sesuai asalnya", "BK-31"),
    ("W05", "Warna pada format angka", "BK-44"),
    ("W06", "Fungsi terlarang atau penutup galat", "BK-52"),
    ("W07", "Rujukan lembar tanpa tanda kutip", "BK-14"),
    ("W08", "Sel gabungan", "BK-38"),
    ("W09", "Lembar, baris atau kolom tersembunyi", "BK-38"),
    ("W10", "Tautan ke berkas luar", "BK-66"),
    ("W11", "Nama terdefinisi di luar pola Kelompok.Nama", "BK-13"),
    ("W12", "Bendera induk atau panel beku tidak sesuai", "BK-36"),
    ("W13", "Pengaturan cetak tidak lengkap", "BK-61"),
    ("W14", "Persen tanpa spasi", "BK-43"),
    ("W15", "Isian sel selain baris kepala", "BK-32"),
    ("W16", "Komentar sel", "BK-66"),
    ("W17", "Terbilang diketik tangan", "BK-57"),
    ("W18", "Uji KENDALI tanpa rujukan", "BK-92"),
    ("W19", "Masukan tanpa validasi data", "BK-65"),
    ("W20", "Properti berkas tidak lengkap", "BK-63"),
    ("W21", "Nama lembar di luar pola", "BK-12"),
    ("W22", "Tebal sintetis pada Plex", "BK-24"),
    ("W23", "Nilai tembolok rumus kosong", "BK-59"),
]
CHECK_IDS = [c[0] for c in CHECKS]
WARN_ONLY = {"W19"}

# ------------------------------------------------------------------- token
FORBIDDEN_FACES = ("Calibri", "Arial", "Times New Roman", "Aptos")
DOC_ID_RE = re.compile(r"\b\d{3}/GSP/[A-Z]+/[IVXL]+/\d{4}\b")
SEQ_HEADERS = {"no", "desimal", "id", "rev"}          # §11.3 pengecualian kolom urut
TERBILANG_SHEET = "HITUNG-TERBILANG"
CONST_LEAVES = {"MASUKAN", "AHS"}                     # BK-02
ALLOWED_LITERALS = {0.0, 1.0, 100.0, 1000.0, 3600.0}  # BK-53
FORBIDDEN_FUNCS = [
    "INDIRECT", "OFFSET", "TODAY", "NOW", "RAND", "RANDBETWEEN",
    "XLOOKUP", "XMATCH", "FILTER", "SORT", "SORTBY", "UNIQUE", "SEQUENCE",
    "LET", "LAMBDA", "IFERROR", "IFNA",
]


def _norm6(rgb):
    """Normalisasi warna openpyxl (ARGB/RGB/named) menjadi 6 heksat kecil."""
    if not rgb or not isinstance(rgb, str):
        return None
    s = rgb.lstrip("#").lower()
    if len(s) == 8:
        s = s[2:]
    return s if len(s) == 6 else None


def load_tokens():
    """tokens.json paket: cari di samping skrip lalu satu tingkat di atas
    (paket FLAT: scripts/datumbuku.py membaca ../tokens.json)."""
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(here, "tokens.json"),
                 os.path.join(os.path.dirname(here), "tokens.json")):
        if os.path.isfile(cand):
            with open(cand, encoding="utf-8") as fh:
                return json.load(fh)
    sys.stderr.write("tokens.json tidak ditemukan di samping datumbuku.py maupun induknya.\n")
    raise SystemExit(2)


class Tok:
    def __init__(self):
        t = load_tokens()
        interior = t["colour"]["interior"]
        self.signal = _norm6(interior["signal"])
        self.verd = _norm6(interior["verd"])
        self.ink900 = _norm6(interior["ink900"])
        self.alert = _norm6(interior["alert"])
        self.white = "ffffff"
        ui = t["type"]["faces"]["workbook_ui"]      # "IBM Plex Sans"
        mono = t["type"]["faces"]["mono"]           # "IBM Plex Mono"
        self.faces = {ui.lower(), mono.lower(),
                      (ui + " SemiBold").lower(), (mono + " SemiBold").lower()}


# ------------------------------------------------------------- util rumus
_STR_RE = re.compile(r'"(?:[^"]|"")*"')
_NUM_RE = re.compile(r"(?<![\w.$])(\d+(?:\.\d+)?)(?![\w.])")
_CELLREF_RE = re.compile(r"(?<![\w.$])(\$?[A-Z]{1,3}\$?\d+)")
_NAME_RE = re.compile(r"(?<![\w.$])([A-Za-z_][A-Za-z0-9_.]*)\s*\(!")  # placeholder
_PURE_LINK_RE = re.compile(r"^='?([^'!]+)'?!\$?[A-Z]{1,3}\$?\d{1,7}$")
_SHEETREF_RE = re.compile(r"(?:(?<=')([^']+)')|(?<![A-Za-z0-9_.'\"$])([A-Za-z0-9_\-]+)!")
_ROUND_RE = re.compile(r"\b(ROUND|ROUNDDOWN|ROUNDUP|TRUNC)\(", re.I)


def strip_strings(formula):
    return _STR_RE.sub('""', formula)


def round_digit_literals(formula):
    """Kumpulkan literal yang merupakan argumen digit ROUND/ROUNDDOWN/ROUNDUP/TRUNC."""
    allowed = set()
    f = strip_strings(formula)
    for m in _ROUND_RE.finditer(f):
        i = m.end()
        depth = 1
        args = [""]
        while i < len(f) and depth > 0:
            ch = f[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    break
            if ch == "," and depth == 1:
                args.append("")
                i += 1
                continue
            args[-1] += ch
            i += 1
        if len(args) >= 2:
            last = args[-1].strip()
            if re.fullmatch(r"\d+", last) and int(last) <= 15:
                allowed.add(float(last))
    return allowed


def power_literals(formula):
    """Literal di sekitar operator ^ : eksponen bulat dan basis pangkat (BK-53)."""
    allowed = set()
    f = strip_strings(formula)
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*\^\s*(\d+(?:\.\d+)?)", f):
        exp = float(m.group(2))
        if exp == int(exp):
            allowed.add(exp)
            allowed.add(float(m.group(1)))   # basis pangkat sepuluh dsb.
    return allowed


def classify_formula_color(formula, names_sheet, this_sheet):
    """Aturan warna BK-31 dihitung dari isi sel (Standar §5.1, diagram bukudatum).
    Mengembalikan 'alert' | 'verd' | 'ink900' | None (tak dinilai)."""
    f = formula.lstrip("=")
    if "[" in f:
        return "alert"
    m = _PURE_LINK_RE.match("=" + f)
    if m:
        return "verd" if m.group(1) != this_sheet else "ink900"
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", f):
        tgt = names_sheet.get(f)
        if tgt and tgt != this_sheet:
            return "verd"
        return "ink900"
    return "ink900"


# ------------------------------------------------------------------- lint
def lint(path, tok=None):
    """Kembalikan (results, exit_code). results: list dict per cek."""
    tok = tok or Tok()
    findings = {cid: [] for cid in CHECK_IDS}

    def add(cid, sheet, ref, msg):
        findings[cid].append({"sheet": sheet, "ref": ref, "msg": msg})

    try:
        z = zipfile.ZipFile(path)
        wb = load_workbook(path)
        wbd = load_workbook(path, data_only=True)
    except Exception as exc:
        sys.stderr.write("berkas tidak terbaca: %s (%s)\n" % (path, exc))
        return None, 2

    part_names = z.namelist()
    raw_parts = {}
    for n in part_names:
        if n.endswith(".xml") or n.endswith(".rels"):
            try:
                raw_parts[n] = z.read(n).decode("utf-8", "replace")
            except Exception:
                raw_parts[n] = ""

    sheetnames = wb.sheetnames
    names_sheet = {}   # defined name -> sheet tujuan
    names_dest = {}    # defined name -> (sheet, sel) untuk W19
    for nm, dn in wb.defined_names.items():
        try:
            sheet_t, cell_t = list(dn.destinations)[0]
            names_sheet[nm] = sheet_t
            names_dest[nm] = (sheet_t, cell_t)
        except Exception:
            names_sheet[nm] = ""
            names_dest[nm] = ("", "")

    # peta lembar -> part xml (untuk W23): elemen <sheet> dan <Relationship> diurai
    # per-elemen sehingga tahan terhadap urutan atribut (LibreOffice vs Excel).
    sheet_part = {}
    try:
        wbx = raw_parts.get("xl/workbook.xml", "")
        relsx = raw_parts.get("xl/_rels/workbook.xml.rels", "")
        rid_of = {}
        for el in re.finditer(r"<sheet\b[^>]*/?>", wbx):
            nm = re.search(r'name="([^"]+)"', el.group(0))
            rid = re.search(r'r:id="(rId\d+)"', el.group(0))
            if nm and rid:
                rid_of[nm.group(1)] = rid.group(1)
        target_of = {}
        for el in re.finditer(r"<Relationship\b[^>]*/?>", relsx):
            rid = re.search(r'Id="(rId\d+)"', el.group(0))
            tgt = re.search(r'Target="([^"]+)"', el.group(0))
            if rid and tgt:
                target_of[rid.group(1)] = tgt.group(1)
        for nm, rid in rid_of.items():
            tgt = target_of.get(rid, "")
            if tgt:
                p_ = "xl/" + tgt.lstrip("/") if not tgt.startswith("xl/") else tgt
                sheet_part[nm] = p_
    except Exception:
        pass

    # ---------- W01 wajah huruf ----------
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.value is not None and c.font and c.font.name:
                    fn = c.font.name.strip().lower()
                    if fn and fn not in tok.faces:
                        add("W01", ws.title, c.coordinate, "wajah %r" % c.font.name)
    blob = "".join(raw_parts.get(n, "") for n in raw_parts
                   if n.startswith("xl/") or n.startswith("docProps/"))
    for face in FORBIDDEN_FACES:
        if face in blob:
            add("W01", "-", "-", "wajah terlarang %r tercatat di XML berkas" % face)

    # ---------- W02 konstanta di luar MASUKAN/AHS ----------
    seq_cols = {}
    for ws in wb.worksheets:
        cols = set()
        for c in ws[6]:
            if isinstance(c.value, str) and c.value.strip().rstrip(".").lower() in SEQ_HEADERS:
                cols.add(c.column)
        seq_cols[ws.title] = cols
    for ws in wb.worksheets:
        if ws.title in CONST_LEAVES:
            continue
        for row in ws.iter_rows(min_row=7):
            for c in row:
                if isinstance(c.value, bool):
                    continue
                if isinstance(c.value, (int, float)) and c.column not in seq_cols.get(ws.title, set()):
                    add("W02", ws.title, c.coordinate, "konstanta %r di lembar non-masukan" % c.value)

    # ---------- W03/W06/W07/W10/W17/W23 per rumus ----------
    # Catatan: openpyxl mempertahankan tanda kutip lembar di string rumus, sehingga
    # W07 dinilai dari objek; W23 dinilai dari XML mentah karena elemen <v></v> kosong
    # (tembolok kosong) hanya terlihat di sana.
    for ws in wb.worksheets:
        wsd = wbd[ws.title]
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if not (isinstance(v, str) and v.startswith("=")):
                    continue
                ref, sheet = c.coordinate, ws.title
                body = strip_strings(v)
                # W03 literal
                if sheet != TERBILANG_SHEET:
                    ok = ALLOWED_LITERALS | round_digit_literals(v) | power_literals(v)
                    for m in _NUM_RE.finditer(body):
                        try:
                            val = float(m.group(1))
                        except ValueError:
                            continue
                        if val not in ok:
                            add("W03", sheet, ref, "literal %s dalam %s" % (m.group(1), v[:48]))
                # W06 fungsi terlarang
                fu = body.upper()
                for fn in FORBIDDEN_FUNCS:
                    if re.search(r"(?<![A-Z0-9_.])%s\s*\(" % fn, fu):
                        add("W06", sheet, ref, "fungsi terlarang %s" % fn)
                # W07 kutip rujukan lembar
                for m in _SHEETREF_RE.finditer(body):
                    quoted, bare = m.group(1), m.group(2)
                    nm = quoted or bare
                    if nm is None:
                        continue
                    if bare is not None and nm in sheetnames and re.search(r"[- ]", nm):
                        add("W07", sheet, ref, "rujukan %s! tanpa kutip" % nm)
                # W10 rujukan berkas luar
                if "[" in body:
                    add("W10", sheet, ref, "rujukan berkas luar dalam %s" % v[:48])
                # W17 terbilang diketik (cek di bawah untuk teks; rumus cukup ada)
        # W23 dari XML mentah: sel ber-rumus tanpa elemen <v>
        part = sheet_part.get(ws.title)
        if part and part in raw_parts:
            for m in re.finditer(r"<c\b[^>]*r=\"([A-Z]+\d+)\"[^>]*>(.*?)</c>", raw_parts[part], re.S):
                inner = m.group(2)
                if "<f" in inner and "<v" not in inner:
                    add("W23", ws.title, m.group(1), "rumus tanpa nilai tembolok")

    # ---------- W04 warna angka dari isi sel ----------
    # "Warna ANGKA menyatakan asal": hanya sel bernilai angka yang dinilai.
    # Nilai tembolok menentukan jenisnya; tanpa tembolok, klasifikasi dari rumus
    # dipakai (§11.3: berkas belum dihitung ulang dapat menghasilkan temuan yang
    # hilang setelah hitung ulang).
    for ws in wb.worksheets:
        wsd = wbd[ws.title]
        for row in ws.iter_rows(min_row=7):
            for c in row:
                v = c.value
                if v is None:
                    continue
                col = _norm6(c.font.color.rgb if (c.font and c.font.color and c.font.color.type == "rgb")
                             else (c.font.color.value if (c.font and c.font.color) else None))
                expected = None
                if isinstance(v, str) and v.startswith("="):
                    cv = wsd[c.coordinate].value
                    if cv is not None and not isinstance(cv, (int, float)):
                        continue                      # hasil rumus bukan angka: bukan wilayah W04
                    kind = classify_formula_color(v, names_sheet, ws.title)
                    expected = {"alert": tok.alert, "verd": tok.verd, "ink900": tok.ink900}[kind]
                    why = kind
                elif not isinstance(v, bool) and isinstance(v, (int, float)):
                    if c.column in seq_cols.get(ws.title, set()):
                        continue                      # §11.3 kolom urut dikecualikan
                    expected, why = tok.signal, "signal"
                else:
                    continue                          # teks tidak dinilai W04
                if col != expected:
                    add("W04", ws.title, c.coordinate,
                        "warna %s, seharusnya %s (%s)" % (col, expected, why))

    # ---------- W05 / W14 format angka ----------
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.value is None:
                    continue
                fmt = c.number_format or ""
                if re.search(r"\[(Red|Black|Blue|Green|White|Magenta|Yellow|Cyan|Color\s*\d+)\]", fmt, re.I):
                    add("W05", ws.title, c.coordinate, "warna pada format %r" % fmt)
                if "%" in fmt:
                    unesc = fmt.replace("\\", "")
                    if not re.search(r"\s%", unesc):
                        add("W14", ws.title, c.coordinate, "persen tanpa spasi: %r" % fmt)

    # ---------- W08 gabungan / W09 tersembunyi ----------
    for ws in wb.worksheets:
        for rng in ws.merged_cells.ranges:
            add("W08", ws.title, str(rng), "sel gabungan")
        if ws.sheet_state != "visible":
            add("W09", ws.title, "-", "lembar state=%s" % ws.sheet_state)
        for r, dim in ws.row_dimensions.items():
            if dim.hidden:
                add("W09", ws.title, "%d:" % r, "baris tersembunyi")
        for colL, dim in ws.column_dimensions.items():
            if dim.hidden:
                add("W09", ws.title, "%s:%s" % (colL, colL), "kolom tersembunyi")

    # ---------- W10 tautan berkas luar (struktur) ----------
    if any(n.startswith("xl/externalLinks") for n in part_names):
        add("W10", "-", "-", "berkas memuat bagian externalLinks")

    # ---------- W11 nama terdefinisi ----------
    NAME_PAT = re.compile(r"^[A-Z][A-Za-z0-9]*(\.[A-Z][A-Za-z0-9]*)+$")
    CELLISH = re.compile(r"^[A-Za-z]{1,3}[0-9]{1,7}$")
    for nm in wb.defined_names:
        bare = nm.split("!")[-1].lstrip("$")
        if not NAME_PAT.match(nm) or CELLISH.match(bare):
            add("W11", "-", nm, "nama terdefinisi di luar pola Kelompok.Nama")

    # ---------- W12 bendera induk + panel beku ----------
    def row6_is_header(ws):
        for c in ws[6]:
            if c.value is not None and c.fill and c.fill.fill_type == "solid":
                return True
        return False

    kend = wb["KENDALI"] if "KENDALI" in sheetnames else None
    flag_a4 = kend["A4"].value if kend else None
    if kend is None:
        add("W12", "-", "A4", "lembar KENDALI tidak ada")
    elif not (isinstance(flag_a4, str) and flag_a4.startswith("=") and "BENDERA INDUK" in flag_a4):
        add("W12", "KENDALI", "A4", "bendera induk tidak ditulis sebagai rumus di KENDALI!A4")
    for ws in wb.worksheets:
        want = "A7" if row6_is_header(ws) else "A6"
        if ws.freeze_panes != want:
            add("W12", ws.title, ws.freeze_panes or "-", "panel beku %s, seharusnya %s" % (ws.freeze_panes, want))
        if ws.title == "KENDALI":
            continue
        a4 = ws["A4"].value
        if not (isinstance(a4, str) and a4.startswith("=") and re.search(r"KENDALI.{0,4}\$?A\$?4", a4)):
            add("W12", ws.title, "A4", "A4 tidak menaut ke KENDALI!A4")

    # ---------- W13 pengaturan cetak ----------
    for ws in wb.worksheets:
        ps = ws.page_setup
        if ps.paperSize != 9:
            add("W13", ws.title, "page_setup", "kertas bukan A4 (paperSize=%r)" % ps.paperSize)
        if ps.fitToWidth != 1:
            add("W13", ws.title, "page_setup", "tidak muat satu halaman lebar (fitToWidth=%r)" % ps.fitToWidth)
        titles = ws.print_title_rows or ""
        if not re.fullmatch(r"\$1:\$6", titles):
            add("W13", ws.title, "print_title_rows", "judul cetak %r, seharusnya $1:$6" % titles)
        of = ws.oddFooter
        for side, txt in (("left", of.left.text), ("center", of.center.text), ("right", of.right.text)):
            if not txt:
                add("W13", ws.title, "footer." + side, "kaki halaman kosong")
        if ws.sheet_view.showGridLines:
            add("W13", ws.title, "sheet_view", "garis kisi masih tampil")

    # ---------- W15 isian sel ----------
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.value is None:
                    continue
                f = c.fill
                if f and f.fill_type == "solid":
                    bg = _norm6(f.start_color.rgb if f.start_color and f.start_color.type == "rgb" else None)
                    fg = _norm6(c.font.color.rgb if (c.font and c.font.color and c.font.color.type == "rgb") else None)
                    if not (bg == tok.ink900 and fg == tok.white):
                        add("W15", ws.title, c.coordinate, "isian %s huruf %s di luar gaya kepala" % (bg, fg))

    # ---------- W16 komentar ----------
    if any(n.startswith("xl/comments") or n.startswith("xl/threadedComments") for n in part_names):
        add("W16", "-", "-", "berkas memuat bagian komentar")
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.comment is not None:
                    add("W16", ws.title, c.coordinate, "komentar sel")

    # ---------- W17 terbilang diketik ----------
    for ws in wb.worksheets:
        for row in ws.iter_rows(min_row=7):
            for c in row:
                v = c.value
                if isinstance(v, str) and not v.startswith("=") and re.search(r"\brupiah\.?\s*$", v.strip()):
                    if ws.title != TERBILANG_SHEET:
                        add("W17", ws.title, c.coordinate, "terbilang diketik tangan")
    tb = wb[TERBILANG_SHEET] if TERBILANG_SHEET in sheetnames else None
    if tb is not None:
        f15 = tb["F15"].value
        if not (isinstance(f15, str) and f15.startswith("=")):
            add("W17", TERBILANG_SHEET, "F15", "terbilang bukan rumus")

    # ---------- W18 uji KENDALI tanpa rujukan ----------
    if kend is not None:
        tur_col = None
        for c in kend[6]:
            if isinstance(c.value, str) and "turunan" in c.value.lower():
                tur_col = c.column
        lap_col = None
        for c in kend[6]:
            if isinstance(c.value, str) and "dilaporkan" in c.value.lower():
                lap_col = c.column
        if tur_col:
            for r in range(7, kend.max_row + 1):
                idv = kend.cell(row=r, column=1).value
                if isinstance(idv, str) and re.fullmatch(r"K-\d{2}", idv):
                    tcell = kend.cell(row=r, column=tur_col)
                    tv = tcell.value
                    if not (isinstance(tv, str) and tv.startswith("=")):
                        add("W18", "KENDALI", tcell.coordinate, "turunan mandiri bukan rumus")
                        continue
                    body = strip_strings(tv)
                    has_ref = bool(_CELLREF_RE.search(body)) or any(
                        re.search(r"(?<![\w.])%s(?![\w.(])" % re.escape(nm), body) for nm in names_sheet)
                    if not has_ref:
                        add("W18", "KENDALI", tcell.coordinate, "turunan mandiri tidak merujuk sel mana pun")
                    if lap_col and tv == kend.cell(row=r, column=lap_col).value:
                        add("W18", "KENDALI", tcell.coordinate, "turunan mandiri sama dengan nilai dilaporkan")

    # ---------- W19 masukan tanpa validasi (peringatan) ----------
    for ws in wb.worksheets:
        covered = set()
        for dv in ws.data_validations.dataValidation:
            for rng in str(dv.sqref).split():
                try:
                    mn, mr, mx, mxr = range_boundaries(rng)
                except Exception:
                    continue
                for rr in range(mr, mxr + 1):
                    for cc in range(mn, mx + 1):     # batas inklusif
                        covered.add((rr, cc))
        for nm, (sheet_t, cellref) in names_dest.items():
            if sheet_t != ws.title or not cellref:
                continue
            m = re.fullmatch(r"\$?([A-Z]{1,3})\$?(\d+)", str(cellref))
            if not m:
                continue
            coord = "%s%s" % (m.group(1), m.group(2))
            cell = ws[coord]
            if isinstance(cell.value, (int, float)) and not isinstance(cell.value, bool) \
                    and (cell.row, cell.column) not in covered:
                add("W19", ws.title, coord, "masukan bernama %s tanpa validasi data" % nm)

    # ---------- W20 properti berkas ----------
    p = wb.properties
    if not (p.title or "").strip():
        add("W20", "-", "core.title", "judul kosong")
    subj = (p.subject or "").strip()
    if not DOC_ID_RE.search(subj):
        add("W20", "-", "core.subject", "subjek %r bukan nomor dokumen GSP" % subj)
    if not (p.keywords or "").strip():
        add("W20", "-", "core.keywords", "kata kunci kosong")
    custom = {}
    try:
        for d in wb.custom_doc_props.props:
            custom[str(d.name).strip().lower()] = str(getattr(d, "value", "") or getattr(d, "text", "") or "")
    except Exception:
        pass
    for req in ("klasifikasi", "revisi"):
        if not custom.get(req):
            add("W20", "-", "custom." + req, "properti kustom %s absen/kosong" % req.capitalize())

    # ---------- W21 nama lembar ----------
    SHEET_PAT = re.compile(r"^[A-Z][A-Z0-9]*(-[A-Z][A-Z0-9]*)*$")
    for nm in sheetnames:
        if len(nm) > 31 or not SHEET_PAT.match(nm):
            add("W21", nm, "-", "nama lembar di luar pola kapital-tandahubung")
        if nm.startswith("HITUNG-") and nm == "HITUNG-":
            add("W21", nm, "-", "HITUNG tanpa ranah")

    # ---------- W22 tebal pada Plex ----------
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.value is not None and c.font and c.font.b and c.font.name and "plex" in c.font.name.lower():
                    add("W22", ws.title, c.coordinate, "tanda tebal pada %s" % c.font.name)

    # ---------- rangkum ----------
    results = []
    blocking = 0
    warn = 0
    for cid, desc, bk in CHECKS:
        n = len(findings[cid])
        if cid in WARN_ONLY:
            warn += n
        else:
            blocking += n
        results.append({"id": cid, "desc": desc, "bk": bk, "count": n,
                        "warn_only": cid in WARN_ONLY,
                        "findings": findings[cid][:20]})
    exit_code = 1 if blocking else 0
    return {"file": path, "results": results, "blocking": blocking, "warnings": warn}, exit_code


def render_table(rep):
    lines = []
    lines.append("datumbuku — lint workbook DATUM (23 cek W01..W23, Standar 001 §11.1)")
    lines.append("berkas: %s" % rep["file"])
    lines.append("")
    lines.append("%-4s %-44s %-7s %6s  %s" % ("Cek", "Yang ditandai", "Aturan", "Temuan", "Status"))
    lines.append("-" * 88)
    for r in rep["results"]:
        st = "OK" if r["count"] == 0 else ("WARN" if r["warn_only"] else "FAIL")
        lines.append("%-4s %-44s %-7s %6d  %s" % (r["id"], r["desc"], r["bk"], r["count"], st))
    lines.append("-" * 88)
    lines.append("temuan menahan terbit: %d | peringatan: %d" % (rep["blocking"], rep["warnings"]))
    for r in rep["results"]:
        if r["count"]:
            lines.append("")
            lines.append("%s (%s) %d temuan%s:" % (r["id"], r["desc"], r["count"],
                         " — peringatan, tidak menahan" if r["warn_only"] else ""))
            for f in r["findings"]:
                lines.append("   %s!%s %s" % (f["sheet"], f["ref"], f["msg"]))
            if r["count"] > len(r["findings"]):
                lines.append("   ... %d lagi" % (r["count"] - len(r["findings"])))
    return "\n".join(lines)


def selftest(fixdir=None):
    """Selftest dua arah bawaan (gerbang eksekusi DHS-RB-03) atas fixture di
    samping skrip: scripts/fixtures_buku/.
      bersih            -> exit lint 0, nol temuan penahan DAN nol peringatan
      rusak__Wxx        -> exit lint 1 dengan cek Wxx memicu >=1 temuan
      peringatan__W19   -> exit lint 0 dengan W19 > 0 sebagai peringatan
      berkas rusak      -> exit 2
    Memakai fixture bersih.xlsx yang merupakan salinan byte workbook spesimen
    000/GSP/RAB/X/2026. Cetak CHECK per baris + satu VERDICT; mengembalikan
    kode keluar proses (0 lulus semua, 1 ada CHECK gagal)."""
    here = os.path.dirname(os.path.abspath(__file__))
    fixdir = fixdir or os.path.join(here, "fixtures_buku")
    lines = []
    failed = []

    def record(name, ok, detail):
        lines.append("CHECK %s: %s — %s" % (name, "PASS" if ok else "FAIL", detail))
        if not ok:
            failed.append(name)

    if not os.path.isdir(fixdir):
        print("CHECK fixtures: FAIL — direktori fixture tidak ada: %s" % fixdir)
        print("VERDICT: FAIL")
        return 1

    path = os.path.join(fixdir, "bersih.xlsx")
    if not os.path.isfile(path):
        record("bersih", False, "fixture bersih.xlsx absen")
    else:
        rep, code = lint(path)
        ok = code == 0 and rep and rep["blocking"] == 0 and rep["warnings"] == 0
        record("bersih", ok, "exit=%d penahan=%d peringatan=%d" % (
            code, rep["blocking"] if rep else -1, rep["warnings"] if rep else -1))

    for cid in CHECK_IDS:
        if cid in WARN_ONLY:
            continue
        fp = os.path.join(fixdir, "rusak__%s.xlsx" % cid)
        if not os.path.isfile(fp):
            record(cid, False, "fixture rusak__%s.xlsx absen" % cid)
            continue
        rep, code = lint(fp)
        hit = {r["id"]: r["count"] for r in rep["results"]} if rep else {}
        ok = code == 1 and hit.get(cid, 0) > 0
        others = sorted(k for k, v in hit.items() if v > 0 and k != cid)
        record(cid, ok, "exit=%d temuan=%d cek_lain=%s" % (code, hit.get(cid, 0), others or "-"))

    fp = os.path.join(fixdir, "peringatan__W19.xlsx")
    if not os.path.isfile(fp):
        record("W19-peringatan", False, "fixture peringatan__W19.xlsx absen")
    else:
        rep, code = lint(fp)
        hit = {r["id"]: r["count"] for r in rep["results"]} if rep else {}
        ok = code == 0 and hit.get("W19", 0) > 0 and rep["blocking"] == 0
        record("W19-peringatan", ok, "exit=%d W19=%d penahan=%d" % (
            code, hit.get("W19", 0), rep["blocking"] if rep else -1))

    import tempfile
    fd, junk = tempfile.mkstemp(suffix=".xlsx")
    with os.fdopen(fd, "wb") as fh:
        fh.write(b"bukan xlsx")
    try:
        rep, code = lint(junk)
        record("berkas-rusak", code == 2, "exit=%d" % code)
    finally:
        os.remove(junk)

    for ln in lines:
        print(ln)
    print("VERDICT:", "PASS" if not failed else "FAIL (%s)" % ", ".join(failed))
    return 0 if not failed else 1


def main(argv=None):
    ap = argparse.ArgumentParser(prog="datumbuku", description="lint workbook DATUM W01..W23")
    ap.add_argument("berkas", nargs="?", help=".xlsx yang diperiksa")
    ap.add_argument("--json", action="store_true", help="keluaran JSON mesin-baca")
    ap.add_argument("--silent", action="store_true", help="hanya tabel ringkas, tanpa daftar temuan")
    ap.add_argument("--selftest", action="store_true",
                    help="jalankan selftest dua arah atas scripts/fixtures_buku/")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.berkas:
        ap.error("berkas wajib diisi kecuali --selftest")
    rep, code = lint(args.berkas)
    if rep is None:
        return code
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    else:
        out = render_table(rep)
        if args.silent:
            out = "\n".join(l for l in out.splitlines() if not l.startswith("   "))
        print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
