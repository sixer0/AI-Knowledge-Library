#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""datum_lint.py — instrumen lint berkas DATUM, 38 cek DATUM-01..DATUM-38.

Provenans : rebuild GAP-09 lapis-2a, kartu DHS-RB-02 (t_60780c73), 2026-10-05.
            BUKAN restorasi mesin Rev J (arsip absen di disk; vonis PUTUSAN-GAP-09).
Daftar cek: tabel M01 docs/2026-10-04-datum-manual/measurement/01-instrumen-penegakan.md
            §2.1 = salinan Tabel 8.1 spesifikasi 000 RevA (38 ID unik; tahap file 27,
            build 7, eye 4). Limit verbatim tabel tersebut.
Token gaya: dibaca dari tokens.json paket (samping berkas ini) — palet TIDAK di-hardcode.
Banner    : sejak Rev J hanya yang dijalankan skrip dilaporkan sebagai hasil; cek
            tahap build/eye tercetak NOT-RUN dengan pemilik tahapnya (jujur, bukan PASS).

Cakupan   : berkas .docx rilis (kelas "file"). XLSX milik datumbuku.py (DHS-RB-03);
            cek tahap build milik engine diagram/render; cek mata milik manusia.
Limit khusus: DATUM-36 limit "report" = selalu dilaporkan, tidak memblokir.

Gerbang eksekusi dua arah:
    uv run --python 3.11 --with python-docx python datum_lint.py <dokumen>.docx
    uv run --python 3.11 --with python-docx python datum_lint.py --selftest
Exit: 0 = bersih pada cek yang dijalankan; 1 = ada FAIL; 2 = salah pakai/berkas.
"""
import json
import os
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- daftar cek
# (id, cek verbatim Tabel 8.1, limit, tahap)
CHECKS = [
    ("DATUM-01", "KPI tile rows, dashboard stat strips", 0, "file"),
    ("DATUM-02", "Filled callout boxes with coloured bars", 0, "file"),
    ("DATUM-03", "Em dashes per 1.000 words; none in headings", 0, "file"),
    ("DATUM-04", "Question-form headings", 0, "file"),
    ("DATUM-05", "Office default faces in output", 0, "file"),
    ("DATUM-06", "Centred cover layouts", 0, "file"),
    ("DATUM-07", "Vertical rules in tables", 0, "file"),
    ("DATUM-08", "Filled table header rows in Word or PDF", 0, "eye"),
    ("DATUM-09", "Data table without a unit column", 0, "file"),
    ("DATUM-10", "Table or figure without SUMBER line", 0, "file"),
    ("DATUM-11", "Load-bearing number without provenance mark", 0, "file"),
    ("DATUM-12", "Decorative colour", 0, "eye"),
    ("DATUM-13", "Rasterised charts", 0, "eye"),
    ("DATUM-14", "Colour values visible on one page", 5, "file"),
    ("DATUM-15", "Body measure in characters", "66-80", "eye"),
    ("DATUM-16", "Value and unit without a space", 0, "file"),
    ("DATUM-17", "\u00b1 without a stated meaning", 0, "file"),
    ("DATUM-18", "Wrong classification for the recipient", 0, "file"),
    ("DATUM-19", "VAT other than 11 % for 2026 non-luxury", 0, "file"),
    ("DATUM-20", "Merged cells in a computation zone", 0, "file"),
    ("DATUM-21", "Rules below 0,18 mm or tints below 15 %", 0, "file"),
    ("DATUM-22", "External claim without Admiralty grade", 0, "file"),
    ("DATUM-23", "Rounded corners outside a terminator", 0, "file"),
    ("DATUM-24", "Connector without a label", 0, "build"),
    ("DATUM-25", "Colour values in one figure", 5, "file"),
    ("DATUM-26", "Accented subjects in one figure", 1, "build"),
    ("DATUM-27", "Diagram strokes below 0,18 mm", 0, "file"),
    ("DATUM-28", "Diagram type below 5,5 pt", 0, "file"),
    ("DATUM-29", "Figure without a SUMBER line", 0, "file"),
    ("DATUM-30", "Figure without number or caption", 0, "file"),
    ("DATUM-31", "Mermaid source in a deliverable", 0, "file"),
    ("DATUM-32", "Connector routed through an unrelated box", 0, "build"),
    ("DATUM-33", "Figure taller than the 247 mm text block", 0, "build"),
    ("DATUM-34", "House marks without the published legend", 0, "build"),
    ("DATUM-35", "More than one symbol dialect in a drawing", 0, "build"),
    ("DATUM-36", "Apparatus delegated to the page", "report", "file"),
    ("DATUM-37", "Composed sheet overflows the A4 page", 0, "build"),
    ("DATUM-38", "Underscore in file, folder or sheet name", 0, "file"),
]
STAGE_OWNER = {"build": "engine build (datum_diagram/datum_render)", "eye": "mata manusia (000 8.3)"}

CLEAN_DEFAULT = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/"
                     "2026-10-04-datum-manual/manual/DATUM Document Manual 002-GSP-STD-X-2026 RevA.docx")


def load_tokens():
    p = HERE / "tokens.json"
    if not p.exists():
        p = HERE.parent / "tokens.json"  # bila dijalankan dari scripts/
    return json.loads(p.read_text(encoding="utf-8"))


# ------------------------------------------------------------------- konteks
class Ctx:
    def __init__(self, path, tok):
        from docx import Document
        self.path = Path(path)
        self.tok = tok
        self.doc = Document(str(path))
        z = zipfile.ZipFile(path)
        self.xml = z.read("word/document.xml").decode("utf-8")
        self.names = [n for n in z.namelist() if n.startswith("word/") and n.endswith((".png", ".jpeg", ".jpg", ".gif", ".emf", ".wmf", ".bin", ".xlsx", ".docx", ".svg"))]
        rels_name = "word/_rels/document.xml.rels"
        self.rel_targets = []
        if rels_name in z.namelist():
            self.rel_targets = re.findall(r'Target="([^"]+)"', z.read(rels_name).decode("utf-8"))
        W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        self.W = W
        self.children = list(self.doc.element.body)
        self.paras = self.doc.paragraphs
        self.tables = self.doc.tables
        self.body_text = "\n".join([p.text for p in self.paras] +
                                   [c.text for t in self.tables for r in t.rows for c in r.cells])
        # segmen halaman dari jejak repaginate Word; tanpa jejak = 1 segmen
        self.segments = re.split(r"lastRenderedPageBreak", self.xml)
        # palet token (hex terlarang-tidak-dikenal utk cek tint/fill)
        pal = set()
        def walk(o):
            if isinstance(o, dict):
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
            elif isinstance(o, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", o):
                pal.add(o[1:].upper())
        walk(tok.get("colour", {}))
        self.palette = pal
        self.marks = "".join(tok.get("marks", {}).get(k, "") for k in
                             ("TERUKUR", "DITURUNKAN", "PEMASOK", "ASUMSI"))


def hexes_in(s):
    return re.findall(r'w:(?:val|color|fill)="([0-9A-Fa-f]{6})"', s)


def chromatic(h):
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    mx, mn = max(r, g, b), min(r, g, b)
    return mx > 0 and (mx - mn) / mx >= 0.15


def is_pure_number(s):
    return bool(re.fullmatch(r"-?\d{1,3}(?:\.\d{3})*(?:,\d+)?\s*\S{0,8}", s.strip())) and any(c.isdigit() for c in s)


def heading_paras(ctx):
    return [p for p in ctx.paras if p.style.name.startswith("Heading")
            or (p._p.find(ctx.W + "pPr") is not None
                and p._p.find(ctx.W + "pPr").find(ctx.W + "outlineLvl") is not None)]


def numeric_data_tables(ctx):
    """tabel konten: [(indeks, tabel)] dgn >=2 baris, >=3 kolom, >=50% sel angka."""
    out = []
    for i, t in enumerate(ctx.tables):
        if len(t.rows) < 2 or len(t.columns) < 3:
            continue
        cells = [c.text for r in t.rows[1:] for c in r.cells]
        if not cells:
            continue
        if sum(1 for c in cells if is_pure_number(c)) / len(cells) >= 0.5:
            out.append((i, t))
    return out


def _cover_limit(ctx):
    """indeks child body pertama yang memuat jejak patahan halaman = akhir sampul."""
    for i, ch in enumerate(ctx.children):
        try:
            x = ch.xml
        except Exception:
            x = ""
        if "lastRenderedPageBreak" in x:
            return i
    return len(ctx.children)


def figure_paras(ctx):
    """Paragraf berisi gambar yang merupakan FIGUR konten. Heuristik deterministik
    dari extent drawing: latar penuh/composed sheet (>=200mm lebar atau >=260mm tinggi),
    pita tipis (rasio aspek >20 atau sisi terkecil <6mm), dan seluruh gambar di area
    sampul (logo/branding, MAT-07) bukan figur."""
    WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
    EMU_MM = 36000
    cover_end = _cover_limit(ctx)
    out = []
    for i, ch in enumerate(ctx.children):
        if ch.tag != ctx.W + "p" or i < cover_end:
            continue
        is_fig = False
        for ext in ch.iter(WP + "extent"):
            try:
                w = int(ext.get("cx", 0)) / EMU_MM
                h = int(ext.get("cy", 0)) / EMU_MM
            except (TypeError, ValueError):
                continue
            if w >= 200 or h >= 260:      # composed sheet / latar halaman -> DATUM-36/37
                continue
            if min(w, h) < 6 or max(w, h) / max(min(w, h), 0.1) > 20:
                continue                   # pita/garis dekoratif
            is_fig = True
        if is_fig:
            out.append((i, ch))
    return out


def neighbor_text(ctx, idx, back=4, fwd=5):
    win = ctx.children[max(0, idx - back): idx + fwd]
    return " ".join("".join(n.text or "" for n in e.iter(ctx.W + "t")) for e in win)


# ------------------------------------------------------------------ para cek
def c01(ctx):
    v = []
    for i, t in enumerate(ctx.tables):
        if len(t.rows) <= 2 and len(t.columns) >= 3:
            # sel grid mentah (hindari duplikasi sel merge ala python-docx)
            cells = ["".join(n.text or "" for n in tc.iter(ctx.W + "t"))
                     for tc in t._tbl.iter(ctx.W + "tc")]
            if sum(1 for c in cells if is_pure_number(c)) / max(1, len(cells)) >= 0.5:
                v.append("tabel%d" % i)
    return v


def c02(ctx):
    v = []
    papers = {"FFFFFF", "AUTO"}
    for grp in ("wrapper", "interior", "brief"):
        g = ctx.tok.get("colour", {}).get(grp, {})
        for k in ("paper", "ground"):
            if isinstance(g.get(k), str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", g[k]):
                papers.add(g[k][1:].upper())
    for m in re.finditer(r"<w:pPr>(?:(?!</w:pPr>).)*?</w:pPr>", ctx.xml, re.S):
        b = m.group(0)
        shd = re.search(r'<w:shd [^>]*w:fill="([0-9A-Fa-f]{6})"', b)
        bar = re.search(r'<w:pBdr>.*?w:(left|right) [^>]*w:val="(?!nil|none)', b, re.S)
        if shd and bar and shd.group(1).upper() not in papers:
            v.append("paragraf terisi+pita @%d" % m.start())
    return v


def c03(ctx):
    words = re.findall(r"\S+", ctx.body_text)
    per1000 = ctx.body_text.count("\u2014") / max(1, len(words)) * 1000
    hd = [p.text[:60] for p in heading_paras(ctx) if "\u2014" in p.text]
    # Putusan user 08-10: ambang turun 3 -> 0, selaras A1 naturalisasi (nol mutlak).
    return [(per1000, "em-dash/1000 kata")] if per1000 > 0 else [] , hd


def c04(ctx):
    pat = re.compile(r"\?\s*$")
    lead = re.compile(r"^(What|How|Why|When|Who|Which|Is|Are|Do|Does|Bagaimana|Apa|Kenapa|Mengapa)\s+\w+\s+(is|are|the|a|an|to|should|can|does|do)\b", re.I)
    return [p.text[:60] for p in heading_paras(ctx) if pat.search(p.text.strip()) or lead.match(p.text.strip())]


def c05(ctx):
    tokf = set(ctx.tok["type"]["faces"].values())
    for r in ctx.tok["type"]["roles"].values():
        if isinstance(r.get("fallback"), str):
            tokf.add(r["fallback"])
    used = set(re.findall(r'<w:rFonts [^>]*w:(?:ascii|hAnsi)="([^"]+)"', ctx.xml))
    # gaya yang benar-benar dirujuk dokumen: hanya styleId terpakai yang dihitung
    import zipfile as _zf
    with _zf.ZipFile(ctx.path) as z:
        st = z.read("word/styles.xml").decode("utf-8")
    refs = set(re.findall(r'<w:pStyle w:val="([^"]+)"', ctx.xml)) | \
           set(re.findall(r'<w:rStyle w:val="([^"]+)"', ctx.xml))
    for m in re.finditer(r'<w:style [^>]*w:styleId="([^"]+)"[^>]*>(.*?)</w:style>', st, re.S):
        if m.group(1) in refs:
            used |= set(re.findall(r'<w:rFonts [^>]*w:ascii="([^"]+)"', m.group(2)))
    bad = sorted(u for u in used if u not in tokf)
    forbidden = {f.lower() for f in ctx.tok["colour"].get("forbidden_body_faces", [])}
    bad += sorted(u for u in used if u.lower() in forbidden and u not in bad)
    return bad


def c06(ctx):
    # sampul = segmen sebelum patahan halaman pertama
    seg0 = ctx.segments[0]
    v = []
    for m in re.finditer(r'<w:p [^>]*>.*?</w:p>|<w:p>.*?</w:p>', seg0, re.S):
        if '<w:jc w:val="center"' in m.group(0):
            txt = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", m.group(0)))[:50]
            v.append("centered di sampul: %r" % txt)
    return v


def c07(ctx):
    v = []
    for m in re.finditer(r"<w:tblBorders>(.*?)</w:tblBorders>", ctx.xml, re.S):
        iv = re.search(r"<w:insideV ([^>]*)/>", m.group(1))
        if iv and 'w:val="nil"' not in iv.group(1) and re.search(r'w:sz="[1-9]', iv.group(1)):
            v.append("insideV aktif")
    for m in re.finditer(r"<w:tcBorders>(.*?)</w:tcBorders>", ctx.xml, re.S):
        for side in ("left", "right"):
            sm = re.search(r"<w:%s ([^>]*)/>" % side, m.group(1))
            if sm and 'w:val="nil"' not in sm.group(1) and 'w:val="none"' not in sm.group(1) \
               and re.search(r'w:sz="[1-9]', sm.group(1)):
                v.append("garis vertikal sel")
                break
    return v


def c09(ctx):
    UNIT = r"(?:\b(?:mm|cm|km|kg|ton|kW|kVA|kWh|VA|dB|Hz|kHz|MHz|dpi|pt|px|pcs|unit|Rp|USD|hari|bulan|tahun)\b|\b[AVW]\b|%)"
    v = []
    for i, t in numeric_data_tables(ctx):
        allt = " ".join(c.text for r in t.rows for c in r.cells)
        if not re.search(UNIT, allt):
            v.append("tabel%d angka tanpa satuan" % i)
    return v


def c10(ctx):
    v = []
    for i, t in enumerate(ctx.tables):
        body_cells = [c.text for r in t.rows for c in r.cells]
        if not any(is_pure_number(c) for c in body_cells):
            continue  # tabel tata letak/admin (sampul, pengesahan) bukan objek data
        if re.search(r"SUMBER", " ".join(body_cells), re.I):
            continue
        idx = ctx.children.index(t._tbl)
        after = " ".join("".join(n.text or "" for n in e.iter(ctx.W + "t"))
                         for e in ctx.children[idx + 1: idx + 3])
        if not re.search(r"SUMBER", after, re.I):
            v.append("tabel%d tanpa SUMBER" % i)
    return v


def c11(ctx):
    # proksi deterministik: baris angka berdiri sendiri (statistik telanjang) wajib tanda provenans
    v = []
    for p in ctx.paras:
        s = p.text.strip()
        if not s or len(s.split()) > 5:
            continue
        if re.fullmatch(r"-?\d{1,3}(?:\.\d{3})*(?:,\d+)?\s*\S{0,10}", s) and any(ch.isdigit() for ch in s):
            if not any(mk in s for mk in ctx.marks) and not re.search(r"\[[A-F][1-6]\]", s):
                v.append(repr(s[:50]))
    return v


def c14(ctx):
    v = []
    for i, seg in enumerate(ctx.segments):
        hx = {h.upper() for h in hexes_in(seg) if chromatic(h.upper())}
        if len(hx) > 5:
            v.append("halaman %d: %d nilai warna %s" % (i + 1, len(hx), sorted(hx)[:7]))
    return v


def c16(ctx):
    UNITS = "mm|cm|km|kg|ton|kW|kVA|kWh|VA|dB|Hz|kHz|MHz|dpi|persen"
    pat = re.compile(r"\d(?:" + "%|" + UNITS + r"(?![A-Za-z0-9]))")
    hits = pat.findall(ctx.body_text)
    return ["%r" % h for h in hits[:20]] if hits else []


def _sentence_bounds(text, i):
    """Batas kalimat tempat indeks i (tidak menembus batas paragraf \\n)."""
    start = 0
    for m in re.finditer(r"[.!?][ \t]*\n|[.!?][ \t]+(?=[\"'(\[]?[A-Z])|\n", text[:i]):
        start = m.end()
    end = len(text)
    m = re.search(r"[.!?](?=[ \t]*\n|[ \t]+[\"'(\[]?[A-Z])|\n", text[i:])
    if m:
        end = i + m.end()
    return text[start:end]


# PUTUSAN-HEUR-1009 butir 1: penanda skema klasifikasi dibaca PEKA-KASUS. Marking sah
# = token kapital-penuh berbatas kata (\bRESTRICTED\b seluruh kapital) ATAU kemunculan
# apa pun yang berada dalam radius kata penanda kelas pada kalimat yang sama. Frasa
# prosa huruf kecil ("a restricted arithmetic of ratios") bukan marking dan tidak
# pernah menaikkan temuan. Mekanisme disahkan manager; JANGAN dibatasi ke posisi
# header/footer/cover saja (marking sah boleh muncul di badan dokumen).
CLASS_MARK = re.compile(r"\b(?:KLASIFIKASI|CLASSIFICATION|SECURITY|KEAMANAN)\b", re.I)


def classification_marks(text, schemes):
    """Unsur `schemes` yang terhitung MARKING klasifikasi (bukan kata prosa) pada `text`.

    Pemindaian kasus-abdi, lalu dua gerbang sesuai putusan: (a) token seluruh kapital
    -> marking; (b) kemunculan apa pun dalam radius kata penanda kelas pada kalimat
    yang sama -> marking. Selain itu = kata prosa, tidak dihitung."""
    found = []
    for scheme in schemes:
        for m in re.finditer(r"\b%s\b" % re.escape(scheme), text, re.I):
            token = text[m.start():m.end()]
            if token.isupper() or CLASS_MARK.search(_sentence_bounds(text, m.start())):
                found.append(scheme)
                break
    return found


# PUTUSAN-HEUR-1009 butir 2: DAFTAR TERTUTUP subjek deiksis dokumen di awal kalimat.
# Hanya kalimat itu yang keluar dari kelas klaim eksternal; subjek pihak ketiga
# ("This vendor's datasheet states 45 %") tetap dinilai penuh.
DOC_DEIXIS = re.compile(
    r"^\s*(?:This|These)\s+(?:standard|document|procedure|specification|policy|report|"
    r"manual|form|checklist)\b"
    r"|^\s*(?:Standar|Dokumen|Prosedur|Spesifikasi|Laporan|Formulir)\s+ini\b", re.I)


def _sentences(text):
    return [s for s in re.split(r"(?<=[.!?])(?:[ \t]*\n|[ \t]+)(?=[\"'(\[]?[A-Z])", text) if s.strip()]


def strip_document_deictic(text):
    """Sisa teks setelah kalimat bersubjek deiksis dokumen dibuang (predikat lain utuh)."""
    kept = [s for s in _sentences(text) if not DOC_DEIXIS.match(s)]
    return " ".join(kept) if kept else ""


def c17(ctx):
    v = []
    MEANING = re.compile(r"toleransi|tolerance|ketidakpastian|uncertainty|deviasi|rentang|range|artinya|menyatakan|maksimum|minimum", re.I)
    for m in re.finditer("\u00b1", ctx.body_text):
        w = ctx.body_text[max(0, m.start() - 120): m.start() + 140]
        if not MEANING.search(w):
            v.append(repr(w[100:160].replace("\n", " ")))
    return v


def c18(ctx):
    # klasifikasi dibaca dari teks area sampul (segmen sebelum patahan halaman pertama,
    # termasuk sel tabel sampul), bukan hanya paragraf lepas.
    TEXT = ["BIASA", "TERBATAS", "RAHASIA"]
    FOR = ["CONFIDENTIAL", "RESTRICTED", "TOP SECRET"]
    cover = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", ctx.segments[0])).upper()
    v = []
    if not any(k in cover for k in TEXT + FOR):
        v.append("tanpa penanda klasifikasi di area sampul")
    # PUTUSAN-HEUR-1009 butir 1: pencocokan peka-kasus, bukan body_text.upper().
    id_used = classification_marks(ctx.body_text, TEXT)
    fo_used = classification_marks(ctx.body_text, FOR)
    if id_used and fo_used:
        v.append("campur skema klasifikasi: %s + %s" % (id_used, fo_used))
    return v


def c19(ctx):
    v = []
    for m in re.finditer(r"(?:PPN|VAT|Pajak Pertambahan Nilai)[^.\n%]{0,25}?(\d{1,2})\s*(?:%|persen)", ctx.body_text):
        rate = int(m.group(1))
        seg = ctx.body_text[max(0, m.start() - 40): m.start() + 60]
        if rate == 11:
            continue
        if rate == 12 and re.search(r"DPP", seg):
            continue  # bentuk sah 12 % x DPP = efektif 11 %
        v.append("tarif %d %% dekat PPN: %r" % (rate, seg.replace("\n", " ")[:90]))
    return v


def c20(ctx):
    v = []
    for i, t in numeric_data_tables(ctx):
        x = t._tbl.xml
        if "<w:vMerge" in x or re.search(r'<w:gridSpan w:val="[2-9]', x):
            v.append("tabel%d zona hitung punya sel gabungan" % i)
    return v


def c21(ctx):
    v = []
    for m in re.finditer(r'<w:(?:top|bottom|left|right|insideH|insideV) ([^>]*)/>', ctx.xml):
        b = m.group(1)
        if 'w:val="nil"' in b or 'w:val="none"' in b:
            continue
        sz = re.search(r'w:sz="(\d+)"', b)
        if sz and int(sz.group(1)) < 4:  # < 0,176 mm < lantai fotokopi 0,18 mm
            v.append("garis sz=%s (<0,18 mm)" % sz.group(1))
    for m in re.finditer(r'<w:shd [^>]*w:fill="([0-9A-Fa-f]{6})"', ctx.xml):
        h = m.group(1).upper()
        if h not in ctx.palette and h not in ("FFFFFF", "AUTO"):
            v.append("isian %s di luar palet token" % h)
    return v


def c22(ctx):
    # klaim eksternal = rujukan bahan pihak luar yang memuat angka; paragraf yang
    # justru MEMBAHAS grade/Admiralty adalah teks normatif, bukan klaim.
    # PUTUSAN-HEUR-1009 butir 2: kalimat bersubjek deiksis dokumen (daftar tertutup
    # DOC_DEIXIS) dikeluarkan dari kelas ini; subjek pihak ketiga tetap dinilai.
    v = []
    # C22-PLURAL (putusan t_0a75080c Vonis 3, kartu t_65fb51b1): bentuk jamak ikut
    # tertangkap; -s opsional per token EN + reduplikasi ID pada 'brosur'.
    KW = re.compile(r"\b(?:datasheets?|vendors?|manufacturers?|brosur(?:-brosur)?)\b", re.I)
    for p in ctx.paras:
        text = strip_document_deictic(p.text)
        if KW.search(text) and re.search(r"\d", text) \
           and not re.search(r"\[[A-F][1-6]\]", text) \
           and not re.search(r"grade|admiralty", text, re.I):
            v.append(text[:110])
    return v


def c23(ctx):
    n = ctx.xml.count("roundRect")
    return ["roundRect di luar terminator"] if n else []


def _drawing_blocks(ctx):
    return re.findall(r"<w:drawing>.*?</w:drawing>|<w:pict>.*?</w:pict>", ctx.xml, re.S)


def c25(ctx):
    v = []
    for i, blk in enumerate(_drawing_blocks(ctx)):
        hx = {h.upper() for h in re.findall(r'(?:fillcolor|strokecolor|fill|stroke|color)="(?:#)?([0-9A-Fa-f]{6})', blk)}
        if len({h for h in hx if chromatic(h)}) > 5:
            v.append("figur %d: %d warna" % (i + 1, len(hx)))
    return v


def c27(ctx):
    v = []
    for blk in _drawing_blocks(ctx):
        for w, u in re.findall(r'o:weight="([\d.]+)(pt|mm)"', blk):
            mmv = float(w) * (0.3528 if u == "pt" else 1.0)
            if mmv < 0.18:
                v.append("stroke %.3f mm" % mmv)
        for w in re.findall(r'<a:ln[^>]*\bw="(\d+)"', blk):
            if int(w) < 6480:  # < 0,18 mm dalam EMU (635 EMU/mm)
                v.append("stroke %s EMU" % w)
    return v


def c28(ctx):
    v = []
    for blk in _drawing_blocks(ctx):
        for s in re.findall(r'w:sz="(\d+)"', blk):
            if int(s) < 11:
                v.append("teks %s pt" % (int(s) / 2))
        for s in re.findall(r"font-size:\s*([\d.]+)px", blk):
            if float(s) * 0.75 < 5.5:
                v.append("teks %s px" % s)
    return v


def c29(ctx):
    v = []
    for idx, ch in figure_paras(ctx):
        if not re.search(r"SUMBER", neighbor_text(ctx, idx), re.I):
            v.append("figur @paragraf-induk %d tanpa SUMBER" % idx)
    return v


def c30(ctx):
    v = []
    for idx, ch in figure_paras(ctx):
        near = neighbor_text(ctx, idx)
        if not re.search(r"(Gambar\s*\d|FIG[\s.\-]?\d|Gambar\s*[A-Z])", near):
            v.append("figur @%d tanpa nomor/caption" % idx)
    return v


def c31(ctx):
    n = len(re.findall(r"^\s*(graph (?:TD|LR|BT|RL)|flowchart (?:TD|LR)|sequenceDiagram)\b", ctx.body_text, re.M))
    return ["sumber Mermaid (%d blok)" % n] if n else []


def c36(ctx):
    n = len(figure_paras(ctx))
    return ("report", "%d figur ditanam di docx (apparatus ke page; verifikasi legenda/kunci lewat engine)" % n)


def c38(ctx):
    v = []
    if "_" in ctx.path.name:
        v.append("nama berkas: %s" % ctx.path.name)
    for n in ctx.names:
        leaf = n.rsplit("/", 1)[-1]
        stem = leaf.rsplit(".", 1)[0]
        if "_" in stem:
            v.append("nama internal: %s" % n)
    return v


EXEC = {"DATUM-01": c01, "DATUM-02": c02, "DATUM-03": c03, "DATUM-04": c04,
        "DATUM-05": c05, "DATUM-06": c06, "DATUM-07": c07, "DATUM-09": c09,
        "DATUM-10": c10, "DATUM-11": c11, "DATUM-14": c14, "DATUM-16": c16,
        "DATUM-17": c17, "DATUM-18": c18, "DATUM-19": c19, "DATUM-20": c20,
        "DATUM-21": c21, "DATUM-22": c22, "DATUM-23": c23, "DATUM-25": c25,
        "DATUM-27": c27, "DATUM-28": c28, "DATUM-29": c29, "DATUM-30": c30,
        "DATUM-31": c31, "DATUM-36": c36, "DATUM-38": c38}


# ------------------------------------------------------------------ runner
def run(path, tok, verbose=True):
    ctx = Ctx(path, tok)
    results = {}
    for cid, desc, limit, stage in CHECKS:
        if stage != "file":
            results[cid] = ("NOT-RUN", "tahap %s -> %s" % (stage, STAGE_OWNER[stage]))
            continue
        try:
            out = EXEC[cid](ctx)
        except Exception as e:  # cacat instrumen dilaporkan, bukan disembunyikan
            results[cid] = ("ERROR", "%s: %s" % (type(e).__name__, e))
            continue
        if cid == "DATUM-03":
            per1000, hd = out
            viol = [str(x) for x in per1000] + hd
            results[cid] = ("FAIL", "; ".join(map(str, viol))) if viol else ("PASS", "em-dash<=3/1000 kata, nol di heading")
            continue
        if cid == "DATUM-36":
            results[cid] = ("REPORT", out[1])
            continue
        if out:
            results[cid] = ("FAIL", "; ".join(str(x) for x in out[:6]))
        else:
            results[cid] = ("PASS", "limit %s" % limit)
    return results


def print_report(path, results):
    print("datum_lint 38 cek :: %s" % path)
    npass = nfail = nskip = nrep = nerr = 0
    for cid, desc, limit, stage in CHECKS:
        st, det = results[cid]
        npass += st == "PASS"; nfail += st in ("FAIL", "ERROR"); nerr += st == "ERROR"
        nskip += st == "NOT-RUN"; nrep += st == "REPORT"
        print("%-9s %-4s [%s] limit=%s | %s" % (cid, st, stage, limit, det[:110]))
    print("-" * 72)
    print("BANNER: dijalankan %d cek file (PASS %d, FAIL %d, REPORT %d); NOT-RUN %d (build/eye, pemilik di atas)."
          % (npass + nfail + nrep, npass, nfail, nrep, nskip))
    print("VERDICT:", "FAIL" if nfail else "PASS")
    return 1 if nfail else 0


# ------------------------------------------------------------------ selftest
def selftest(tok):
    """Dua arah: corpus basal rusak WAJIB exit!=0; artefak bersih WAJIB exit 0."""
    fx = HERE / "fixtures_lint" / "basal_rusak.docx"
    clean = Path(os.environ.get("DATUM_CLEAN", str(CLEAN_DEFAULT)))
    ok = True
    if not fx.exists():
        print("CHECK 1: FAIL - fixture basal_rusak.docx absen di", fx.parent)
        print("VERDICT: FAIL")
        return 1
    print("# arah RED (corpus basal rusak, harapan exit != 0)")
    r = run(fx, tok)
    rc_red = print_report(fx, r)
    fired = {cid for cid, (st, _) in r.items() if st in ("FAIL", "ERROR")}
    expect = {"DATUM-01", "DATUM-03", "DATUM-04", "DATUM-05", "DATUM-06", "DATUM-07",
              "DATUM-09", "DATUM-10", "DATUM-16", "DATUM-17", "DATUM-19", "DATUM-20",
              "DATUM-21", "DATUM-31", "DATUM-38"}
    miss = expect - fired
    print("CHECK 1: %s - RED exit=%d, temuan %d cek%s" %
          ("FAIL" if rc_red == 0 else "PASS", rc_red, len(fired),
           "" if not miss else ", TANPA expected: " + ",".join(sorted(miss))))
    ok &= rc_red != 0 and not miss
    print("# arah GREEN (artefak bersih pin VERIF-final-4, harapan exit 0)")
    if not clean.exists():
        print("CHECK 2: FAIL - artefak bersih absen:", clean)
        ok = False
    else:
        r2 = run(clean, tok)
        rc_green = print_report(clean, r2)
        print("CHECK 2: %s - GREEN exit=%d" % ("PASS" if rc_green == 0 else "FAIL", rc_green))
        ok &= rc_green == 0
    print("CHECK 3: %s - registry 38 ID unik DATUM-01..38" %
          ("PASS" if len({c[0] for c in CHECKS}) == 38 else "FAIL"))
    ok &= len({c[0] for c in CHECKS}) == 38
    ok &= _selftest_heur_1009()
    print("VERDICT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


class _MiniCtx:
    """Konteks sintetis seukuran kebutuhan cek teks murni (c18/c22).

    `cover` diisi penanda klasifikasi sampul sah agar cabang 'tanpa penanda klasifikasi
    di area sampul' tidak mencemari uji mekanisme butir 1."""
    def __init__(self, paras, cover="KLASIFIKASI RAHASIA - INTERNAL"):
        self.paras = [type("P", (), {"text": t})() for t in paras]
        self.body_text = "\n".join(paras)
        self.segments = ["<w:t>%s</w:t>" % cover]


def _selftest_heur_1009():
    """Baris fixture PUTUSAN-HEUR-1009: dua arah per tambalan (positif-palsu lepas,
    positif-sejati tetap jatuh). Tidak menyentuh ambang/limit cek lain."""
    res = []

    # --- DATUM-18 -------------------------------------------------------------
    # positif-palsu lepas: frasa prosa huruf kecil bukan marking skema asing.
    fp = EXEC["DATUM-18"](_MiniCtx([
        "KLASIFIKASI RAHASIA - INTERNAL",
        "That expression is a restricted arithmetic of ratios, percentages, "
        "and unit conversions parsed by its own parser."]))
    res.append(("H18-a positif-palsu lepas (prosa 'restricted' huruf kecil)", not fp, fp))
    # positif-sejati tetap jatuh: marking campur kapital asli RAHASIA + RESTRICTED.
    tp = EXEC["DATUM-18"](_MiniCtx([
        "KLASIFIKASI RAHASIA - INTERNAL",
        "Dokumen turunan ini memakai penanda RESTRICTED untuk lingkup luar."]))
    res.append(("H18-b positif-sejati jatuh (RAHASIA + RESTRICTED kapital)", bool(tp), tp))
    # radius penanda kelas: kemunculan apa pun dalam kalimat berpenanda kelas dihitung.
    rad = EXEC["DATUM-18"](_MiniCtx([
        "KLASIFIKASI RAHASIA - INTERNAL",
        "Klasifikasi dokumen ini restricted untuk mitra."]))
    res.append(("H18-c radius penanda kelas aktif (kalimat KLASIFIKASI)", bool(rad), rad))
    # kontrol cakupan: sampul tanpa penanda klasifikasi tetap terlapor (cabang lama utuh).
    cov = EXEC["DATUM-18"](_MiniCtx(["Isi prosa biasa tanpa penanda apa pun."], cover="KOSONG"))
    res.append(("H18-d sampul tanpa penanda tetap terlapor", any("sampul" in x for x in cov), cov))

    # --- DATUM-22 -------------------------------------------------------------
    # positif-palsu lepas: kalimat normatif sampul bersubjek deiksis dokumen.
    fp22 = EXEC["DATUM-22"](_MiniCtx([
        "This standard is DD-VENDOR, the Principal Deep-Dive Due Diligence Procedure "
        "for Potential Vendors of PT Gemilang Satria Perkasa, carried under provisional "
        "number DDV/GSP/STD/X/2026 pending assignment of the Master Register number."]))
    res.append(("H22-a positif-palsu lepas ('This standard is ...' deiksis)", not fp22, fp22))
    # kontrol wajib putusan: subjek pihak ketiga HARUS tetap FAIL.
    tp22 = EXEC["DATUM-22"](_MiniCtx(["This vendor's datasheet states 45 % coverage."]))
    res.append(("H22-b kontrol wajib jatuh (\"This vendor's datasheet states 45 %\")", bool(tp22), tp22))
    # padanan Indonesia pada daftar tertutup.
    idn = EXEC["DATUM-22"](_MiniCtx([
        "Standar ini mengatur vendor yang mengirim brosur 2026 dan datasheet 3 lembar."]))
    res.append(("H22-c deiksis Indonesia 'Standar ini' lepas", not idn, idn))
    # kalimat non-deiksis tentang pihak ketiga di paragraf yang sama tetap dinilai.
    mix = EXEC["DATUM-22"](_MiniCtx([
        "Standar ini berlaku internal. Vendor Alpha mengirim datasheet 2026 dengan 12 klaim."]))
    res.append(("H22-d kalimat pihak ketiga di paragraf sama tetap jatuh", bool(mix), mix))
    # C22-PLURAL (putusan t_0a75080c Vonis 3, kartu t_65fb51b1): kontrol merah baru
    # bentuk jamak wajib jatuh; tiga probe plural_probe.py plus K1/K2 dan preseden K3.
    pl1 = EXEC["DATUM-22"](_MiniCtx(["Vendors state 900 W output at 40 C."]))
    res.append(("H22-e kontrol wajib jatuh (plural 'Vendors state 900 W')", bool(pl1), pl1))
    pl2 = EXEC["DATUM-22"](_MiniCtx(["Datasheets from three suppliers quote 900 W at 40 C."]))
    res.append(("H22-f kontrol wajib jatuh (plural 'Datasheets from three suppliers')", bool(pl2), pl2))
    pl3 = EXEC["DATUM-22"](_MiniCtx(["Manufacturers advertise 900 W output at 40 C."]))
    res.append(("H22-g kontrol wajib jatuh (plural 'Manufacturers advertise 900 W')", bool(pl3), pl3))
    k1 = EXEC["DATUM-22"](_MiniCtx(["The vendor named in the annex states 900 W output at 40 C."]))
    res.append(("H22-h kontrol wajib jatuh (K1 'The vendor named in the annex')", bool(k1), k1))
    k2 = EXEC["DATUM-22"](_MiniCtx(["The manufacturer published 900 W at 40 C in its leaflet."]))
    res.append(("H22-i kontrol wajib jatuh (K2 'The manufacturer published')", bool(k2), k2))
    k3 = EXEC["DATUM-22"](_MiniCtx(["This vendor's datasheet states 45 % coverage."]))
    res.append(("H22-j kontrol wajib jatuh (K3 preseden H22-b)", bool(k3), k3))
    # dua arah perluasan: reduplikasi ID jatuh, dan deiksis jamak tetap lepas.
    plid = EXEC["DATUM-22"](_MiniCtx(["Brosur-brosur mitra menyebut 900 W keluaran pada 40 C."]))
    res.append(("H22-k kontrol wajib jatuh (reduplikasi ID 'brosur-brosur')", bool(plid), plid))
    fp22p = EXEC["DATUM-22"](_MiniCtx([
        "Standar ini mengatur vendor-vendor yang mengirim brosur-brosur 2026 dan "
        "datasheet-datasheet 3 lembar."]))
    res.append(("H22-l deiksis Indonesia subjek jamak tetap lepas", not fp22p, fp22p))

    for n, (name, passed, detail) in enumerate(res, start=4):
        print("CHECK %d: %s - %s%s" % (n, "PASS" if passed else "FAIL", name,
                                       "" if passed else " | dapat: %s" % (detail,)))
    return all(p for _, p, _ in res)


def main(argv):
    tok = load_tokens()
    args = argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "--selftest":
        return selftest(tok)
    return print_report(args[0], run(args[0], tok))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
