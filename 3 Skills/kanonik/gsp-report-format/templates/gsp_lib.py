#!/usr/bin/env python3
"""gsp_lib.py - Helper pembangun dokumen GSP sesuai Acuan 020/GSP/STD/VIII/2026 RevA.

Terbukti 25-08-2026 pada laporan ADINT (GSP-TR-ADINT-DEEP-2026-RevA.docx).
Menerapkan: grid A4 (margin 24/20/13/13 mm), tumpukan huruf fallback office
(Segoe UI Semibold = struktur, Georgia = baca, Consolas = data), palet interior
hex, header/footer 4 sel + chip klasifikasi + field LEMBAR n DARI N, blok bukti
4 tanda, grammar tabel (keterangan di atas, SUMBER di bawah, tanpa garis
vertikal), normalisasi em-dash (butir 9 checklist).
Catatan jujur: IBM Plex tidak selalu terpasang; fallback office dipakai sesuai
izin acuan. Tanpa mesin render resmi gspdatum.py; struktur, bahasa, aparatus,
penomoran, dan palet diterapkan manual.
"""
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Palet interior (Tabel 2.3 acuan) ─────────────────────────────────────────
PAPER   = RGBColor(0xFC, 0xFC, 0xFB)
INK900  = RGBColor(0x10, 0x14, 0x18)
INK700  = RGBColor(0x2B, 0x36, 0x40)
INK400  = RGBColor(0x6B, 0x77, 0x83)
INK200  = RGBColor(0xC3, 0xCB, 0xD1)
INK100  = RGBColor(0xEF, 0xF2, 0xF4)
SIGNAL  = RGBColor(0xB4, 0x53, 0x09)   # amber
ALERT   = RGBColor(0x9B, 0x1C, 0x1C)   # merah
VERD    = RGBColor(0x2F, 0x6F, 0x6B)   # hijau-teal

FONT_STRUKTUR = "Segoe UI Semibold"
FONT_BACA     = "Georgia"
FONT_DATA     = "Consolas"

DOC_ID      = "021/GSP/LAP/VIII/2026"      # ganti per dokumen
DOC_REV     = "REV A"
DOC_TANGGAL = "25-VIII-2026"
DOC_KLASIF  = "TERBATAS"
DOC_JUDUL   = "Judul Dokumen GSP"


def _norm_em(t):
    """Normalisasi em-dash (D17 MUTLAK): nol U+2014 lolos ke dokumen.
    Implementasi memakai kode titik kode agar berkas sumber sendiri bebas
    pemancar U+2014 literal maupun escape."""
    if not t:
        return t
    em = chr(0x2014)
    t = t.replace(" " + em + " ", ", ")
    t = t.replace(em, "-")
    return t


def style_run(run, font=FONT_BACA, size=9.5, color=INK700, bold=False, italic=False,
              caps=False, tracking=None):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    if caps:
        run.font.all_caps = True
    rPr = run._r.get_or_add_rPr()
    if tracking is not None:
        sp = OxmlElement("w:spacing"); sp.set(qn("w:val"), str(int(tracking * 100)))
        rPr.append(sp)
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts"); rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), font); rFonts.set(qn("w:hAnsi"), font)
    return run


def set_cell_bg(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def set_cell_margins(cell, top=40, start=60, bottom=40, end=60):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for tag, val in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        el = OxmlElement(f"w:{tag}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        tcMar.append(el)
    tcPr.append(tcMar)


def set_table_borders_horizontal(table, top_mm=0.45, head_mm=0.25, row_mm=0.2,
                                 bottom_mm=0.45, color="101418"):
    """Grammar tabel: tanpa garis vertikal; horizontal bertingkat (Bagian 6)."""
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge, sz in (("top", top_mm), ("bottom", bottom_mm)):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(int(sz * 8)))
        el.set(qn("w:color"), color)
        borders.append(el)
    for edge in ("left", "right", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "none")
        borders.append(el)
    el = OxmlElement("w:insideH")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(int(row_mm * 8)))
    el.set(qn("w:color"), "C3CBD1")
    borders.append(el)
    tblPr.append(borders)
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = OxmlElement("w:tcBorders")
            b = OxmlElement("w:bottom")
            b.set(qn("w:val"), "single")
            b.set(qn("w:sz"), str(int(head_mm * 8)))
            b.set(qn("w:color"), color)
            tcBorders.append(b)
            tcPr.append(tcBorders)


def add_field(paragraph, field_code):
    """Sisipkan field Word (PAGE/NUMPAGES) untuk LEMBAR n DARI N otomatis."""
    run = paragraph.add_run()
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = field_code
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    run._r.append(f1); run._r.append(it); run._r.append(f2)
    return run


def setup_section(doc, margin_left=24, margin_right=20, margin_top=13, margin_bottom=13):
    sec = doc.sections[0]
    sec.page_width = Mm(210)
    sec.page_height = Mm(297)
    sec.left_margin = Mm(margin_left)
    sec.right_margin = Mm(margin_right)
    sec.top_margin = Mm(margin_top)
    sec.bottom_margin = Mm(margin_bottom)
    sec.header_distance = Mm(8)
    sec.footer_distance = Mm(8)
    return sec


def add_header_footer(doc, org="PT GEMILANG SATRIA PERKASA",
                      divisi="ENGINEERING & TECHNICAL INTELLIGENCE DIVISION"):
    sec = doc.sections[0]
    # Header: kiri identitas; kanan chip klasifikasi; garis tipis
    header = sec.header
    header.is_linked_to_previous = False
    htbl = header.add_table(rows=1, cols=2, width=Mm(166))
    htbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1, c2 = htbl.rows[0].cells
    set_cell_margins(c1, top=20, bottom=20)
    set_cell_margins(c2, top=20, bottom=20)
    p1 = c1.paragraphs[0]
    # D16: pemisah U+00B7 pada blok header/footer = string blok terkendali verbatim master design.
    r = p1.add_run(f"{org} · {divisi} · {DOC_JUDUL.upper()}")
    style_run(r, FONT_DATA, 6.8, INK400, caps=True, tracking=0.16)
    p2 = c2.paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p2.add_run(f"  {DOC_KLASIF}  ")
    style_run(r, FONT_DATA, 6.8, ALERT, bold=True)
    set_cell_bg(c2, "9B1C1C")
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    # Footer 4 sel: ID | REV · tgl | LEMBAR n DARI N | chip (pemisah REV = string blok terkendali D16)
    footer = sec.footer
    footer.is_linked_to_previous = False
    ftbl = footer.add_table(rows=1, cols=4, width=Mm(166))
    ftbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cells = ftbl.rows[0].cells
    for c in cells:
        set_cell_margins(c, top=20, bottom=20)
    for i, c in enumerate(cells):
        p = c.paragraphs[0]
        if i == 2:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run("LEMBAR "); style_run(r, FONT_DATA, 6.8, INK400)
            add_field(p, "PAGE")
            for run in p.runs[-1:]: style_run(run, FONT_DATA, 6.8, INK400)
            r = p.add_run(" DARI "); style_run(r, FONT_DATA, 6.8, INK400)
            add_field(p, "NUMPAGES")
            for run in p.runs[-1:]: style_run(run, FONT_DATA, 6.8, INK400)
        elif i == 3:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(f"  {DOC_KLASIF}  ")
            style_run(r, FONT_DATA, 6.8, ALERT, bold=True)
            set_cell_bg(c, "9B1C1C")
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        else:
            r = p.add_run([f"GSP · {DOC_ID}", f"{DOC_REV} · {DOC_TANGGAL}"][i])
            style_run(r, FONT_DATA, 6.8, INK400)


def add_kicker(doc, text, color=SIGNAL):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text.upper())
    style_run(r, FONT_STRUKTUR, 6.8, color, bold=True, caps=True, tracking=0.16)
    return p


def add_h1(doc, number, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(f"{number}  {title}")
    style_run(r, FONT_STRUKTUR, 16, INK900, bold=True)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr"); bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "12"); bottom.set(qn("w:color"), "101418")
    pBdr.append(bottom); pPr.append(pBdr)
    return p


def add_h2(doc, number, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(f"{number}  {title}")
    style_run(r, FONT_STRUKTUR, 11, INK900, bold=True)
    return p


def add_para(doc, text, size=9.5, color=INK700, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
             space_after=4, first_indent=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = Pt(13.5)
    if first_indent:
        p.paragraph_format.first_line_indent = Mm(first_indent)
    r = p.add_run(_norm_em(text))
    style_run(r, FONT_BACA, size, color)
    return p


def add_evidence_block(doc, label, meaning, lines, color=SIGNAL, label_color=SIGNAL):
    """Blok bukti: paragraf asal pengetahuan, garis kiri tebal berwarna, label rel kapital.
    label: '■' TERUKUR, '◈' DITURUNKAN, '◇' PEMASOK, '△' ASUMSI."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl.autofit = False
    cell = tbl.rows[0].cells[0]
    cell.width = Mm(128)
    set_cell_margins(cell, top=80, bottom=80, start=140, end=80)
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single"); left.set(qn("w:sz"), "24")
    left.set(qn("w:color"), "%02X%02X%02X" % (color[0], color[1], color[2]))
    tcBorders.append(left)
    tcPr.append(tcBorders)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f"{label}  {_norm_em(meaning)}")
    style_run(r, FONT_STRUKTUR, 7.5, label_color, bold=True, caps=True, tracking=0.1)
    for line in lines:
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_after = Pt(2)
        p2.paragraph_format.line_spacing = Pt(12.5)
        r2 = p2.add_run(_norm_em(line))
        style_run(r2, FONT_BACA, 8.6, INK700)
    return tbl


def add_table(doc, caption, source, headers, rows, col_widths=None, header_color=INK900):
    """Tabel standar: keterangan DI ATAS, tanpa garis vertikal, SUMBER di bawah."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(_norm_em(caption))
    style_run(r, FONT_DATA, 8.6, SIGNAL, bold=True)
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    if col_widths:
        for j, w in enumerate(col_widths):
            for cell in tbl.columns[j].cells:
                cell.width = Mm(w)
    for j, h in enumerate(headers):
        cell = tbl.rows[0].cells[j]
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        style_run(r, FONT_STRUKTUR, 8.6, header_color, bold=True, caps=True)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tbl.rows[i + 1].cells[j]
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            text = _norm_em(val)
            mono = isinstance(val, str) and any(ch.isdigit() for ch in val[:6])
            r = p.add_run(text)
            style_run(r, FONT_DATA if mono else FONT_BACA, 8.6, INK700)
    set_table_borders_horizontal(tbl)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(f"SUMBER  {_norm_em(source)}")
    style_run(r, FONT_DATA, 7.2, INK400)
    return tbl


def add_rev_table(doc, rows):
    """Riwayat revisi: REV | TANGGAL | PERUBAHAN | PEMICU | DAMPAK | OLEH."""
    add_table(doc, "TABEL 10.1  Riwayat revisi. Revisi terbaru di baris teratas; baris lama tidak pernah diubah atau dihapus.",
              "ARSIP GSP-AR-001 6.1.",
              ["REV", "TANGGAL", "PERUBAHAN", "PEMICU", "DAMPAK", "OLEH"],
              rows, col_widths=[12, 22, 52, 30, 30, 20])
