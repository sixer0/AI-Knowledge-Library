#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Markdown -> Word (.docx) converter for GSP report deliverables.

Usage:
  python build_md_to_docx.py <src.md> <out.docx> ["TITLE"] ["SUBTITLE"] ["META"]

Behaviour (validated 2026-08-24 on 3 large GSP reports):
  - A4 page, 2cm margins, Calibri 10.5 body.
  - Custom centered title block (title/subtitle/meta) from argv.
  - The FIRST markdown H1 line is treated as the document title and skipped
    (already rendered in the title block). H2 -> Heading 1, H3 -> Heading 2,
    H4+ -> Heading 3 (Word navigation pane friendly).
  - Tables: '| ... |' blocks, header row bold + shaded DCE6F1, compact 8-8.5pt.
  - Code fences: Consolas 8.5pt with light-gray shading (F2F2F2).
  - Inline **bold**, *italic*, `code` (Consolas) via add_runs_with_markup.
  - Bullets '- ' -> List Bullet; numbered '1. ' -> List Number; '> ' italic.
  - Footer: centered PAGE field.
Requires: pip install python-docx  (verified 1.2.0)
Verify after run: docx_validate.py + docx_read.py --structure
"""
import re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = sys.argv[1] if len(sys.argv) > 1 else r"input.md"
OUT = sys.argv[2] if len(sys.argv) > 2 else r"output.docx"
DOC_TITLE = sys.argv[3] if len(sys.argv) > 3 else "LAPORAN"
DOC_SUBTITLE = sys.argv[4] if len(sys.argv) > 4 else ""
DOC_META = sys.argv[5] if len(sys.argv) > 5 else "Disusun oleh Brahma (PT. Gemilang Satria Perkasa)"

GSP_BLUE = RGBColor(0x1F, 0x3A, 0x5F)
GSP_ACCENT = RGBColor(0x0E, 0x6E, 0x6E)
GRAY = RGBColor(0x44, 0x44, 0x44)

doc = Document()
for section in doc.sections:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)

normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(10.5)
normal.paragraph_format.space_after = Pt(4)
rpr = normal.element.get_or_add_rPr()
rfonts = rpr.get_or_add_rFonts()
rfonts.set(qn("w:eastAsia"), "Calibri")

for level, size, color in [("Heading 1", 17, GSP_BLUE), ("Heading 2", 13.5, GSP_BLUE), ("Heading 3", 11.5, GSP_ACCENT)]:
    st = doc.styles[level]
    st.font.name = "Calibri"
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = color
    st.paragraph_format.space_before = Pt(12 if level == "Heading 1" else 8)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.keep_with_next = True


def add_runs_with_markup(par, text):
    tokens = re.split(r"(\*\*.*?\*\*|\*.*?\*|`.*?`)", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            r = par.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            r = par.add_run(tok[1:-1]); r.italic = True
        elif tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
            r = par.add_run(tok[1:-1]); r.font.name = "Consolas"; r.font.size = Pt(9.5)
        else:
            par.add_run(tok)


def add_code_block(lines):
    for i, ln in enumerate(lines):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(ln if ln else " ")
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x20, 0x20, 0x20)
        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "F2F2F2")
        pPr.append(shd)


def add_table(rows):
    ncols = max(len(r) for r in rows)
    tbl = doc.add_table(rows=len(rows), cols=ncols)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = True
    for i, row in enumerate(rows):
        for j in range(ncols):
            cell = tbl.cell(i, j)
            txt = row[j] if j < len(row) else ""
            cell.text = ""
            par = cell.paragraphs[0]
            par.paragraph_format.space_after = Pt(1)
            r = par.add_run(txt)
            r.font.size = Pt(8.5 if i == 0 else 8)
            if i == 0:
                r.bold = True
                tcPr = cell._tc.get_or_add_tcPr()
                shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "DCE6F1")
                tcPr.append(shd)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


# Title block
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run(DOC_TITLE); r.bold = True; r.font.size = Pt(22); r.font.color.rgb = GSP_BLUE
if DOC_SUBTITLE:
    s = doc.add_paragraph(); s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = s.add_run(DOC_SUBTITLE); r.font.size = Pt(12); r.font.color.rgb = GRAY
m = doc.add_paragraph(); m.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = m.add_run(DOC_META); r.italic = True; r.font.size = Pt(10); r.font.color.rgb = GRAY
doc.add_paragraph()

with open(SRC, encoding="utf-8") as f:
    raw = f.read()

lines = raw.split("\n")
body = []
seen_h1 = False
for ln in lines:
    if not seen_h1 and ln.startswith("# "):
        seen_h1 = True
        continue
    body.append(ln)

i, n = 0, len(body)
while i < n:
    ln = body[i].rstrip()
    if not ln.strip():
        i += 1
        continue
    if ln.startswith("```"):
        block = []
        i += 1
        while i < n and not body[i].startswith("```"):
            block.append(body[i].rstrip())
            i += 1
        i += 1
        add_code_block(block)
        continue
    if ln.startswith("|") and i + 1 < n and body[i + 1].strip().startswith("|---"):
        header = [c.strip() for c in ln.strip().strip("|").split("|")]
        i += 2
        rows = []
        while i < n and body[i].strip().startswith("|"):
            rows.append([c.strip() for c in body[i].strip().strip("|").split("|")])
            i += 1
        add_table([header] + rows)
        continue
    if ln.startswith("---"):
        i += 1
        continue
    hm = re.match(r"^(#{1,6})\s+(.*)$", ln)
    if hm:
        level = len(hm.group(1))
        mapped = {2: 1, 3: 2}.get(level, 3)
        p = doc.add_paragraph(style=f"Heading {mapped}")
        add_runs_with_markup(p, hm.group(2).strip())
        i += 1
        continue
    if ln.startswith("- "):
        p = doc.add_paragraph(style="List Bullet")
        add_runs_with_markup(p, ln[2:])
        i += 1
        continue
    if re.match(r"^\d+\.\s+", ln):
        p = doc.add_paragraph(style="List Number")
        add_runs_with_markup(p, re.sub(r"^\d+\.\s+", "", ln))
        i += 1
        continue
    if ln.startswith("> "):
        p = doc.add_paragraph()
        r = p.add_run(ln[2:]); r.italic = True; r.font.color.rgb = GRAY
        i += 1
        continue
    p = doc.add_paragraph()
    add_runs_with_markup(p, ln)
    i += 1

# Footer page numbers
footer = doc.sections[0].footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = fp.add_run()
fld1 = OxmlElement("w:fldChar"); fld1.set(qn("w:fldCharType"), "begin")
instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve"); instr.text = "PAGE"
fld2 = OxmlElement("w:fldChar"); fld2.set(qn("w:fldCharType"), "end")
run._r.append(fld1); run._r.append(instr); run._r.append(fld2)
run.font.size = Pt(8)

doc.save(OUT)
print("Saved:", OUT)
