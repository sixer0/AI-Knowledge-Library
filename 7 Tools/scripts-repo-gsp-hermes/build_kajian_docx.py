#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert the Brahma ecosystem kajian markdown into a styled Word .docx."""
import re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md"
OUT = sys.argv[2] if len(sys.argv) > 2 else r"C:/Users/TRIAL/workspace/Kajian_Ekosistem_Brahma_GSP_2026-08-24.docx"
DOC_TITLE = sys.argv[3] if len(sys.argv) > 3 else "KAJIAN KOMPREHENSIF EKOSISTEM BRAHMA"
DOC_SUBTITLE = sys.argv[4] if len(sys.argv) > 4 else "GSP Agent Headquarter · Fleet 40 Profil · Bridge · Webstack · Knowledge Systems"
DOC_META = sys.argv[5] if len(sys.argv) > 5 else "Disusun oleh Brahma (AI Orchestrator, PT. Gemilang Satria Perkasa) — 24 Agustus 2026"

GSP_BLUE = RGBColor(0x1F, 0x3A, 0x5F)
GSP_ACCENT = RGBColor(0x0E, 0x6E, 0x6E)
GRAY = RGBColor(0x44, 0x44, 0x44)

doc = Document()

# Page setup A4 with normal margins
for section in doc.sections:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)

# Base style
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
    """Handle **bold**, *italic*, and `code` inline tokens."""
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
        if i < len(lines) - 1:
            continue

def add_table(rows):
    ncols = max(len(r) for r in rows)
    nrows = len(rows)
    tbl = doc.add_table(rows=nrows, cols=ncols)
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
            if i == 0:
                r = par.add_run(txt)
                r.bold = True
                r.font.size = Pt(8.5)
                tcPr = cell._tc.get_or_add_tcPr()
                shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "DCE6F1")
                tcPr.append(shd)
            else:
                r = par.add_run(txt)
                r.font.size = Pt(8)
    # reduce cell margins for compactness
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# Title block
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run(DOC_TITLE)
r.bold = True; r.font.size = Pt(22); r.font.color.rgb = GSP_BLUE
s = doc.add_paragraph(); s.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = s.add_run(DOC_SUBTITLE)
r.font.size = Pt(12); r.font.color.rgb = GRAY
m = doc.add_paragraph(); m.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = m.add_run(DOC_META)
r.italic = True; r.font.size = Pt(10); r.font.color.rgb = GRAY
doc.add_paragraph()

with open(SRC, encoding="utf-8") as f:
    raw = f.read()

# Skip the markdown H1 title line(s) at the top (already rendered in title block)
lines = raw.split("\n")
body = []
seen_h1 = False
for ln in lines:
    if not seen_h1 and ln.startswith("# "):
        seen_h1 = True
        continue
    body.append(ln)

i = 0
n = len(body)
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
        i += 1  # skip closing fence
        add_code_block(block)
        continue
    if ln.startswith("|") and i + 1 < n and body[i + 1].strip().startswith("|---"):
        # table: header | separator | rows
        rows = []
        header = [c.strip() for c in ln.strip().strip("|").split("|")]
        i += 2  # skip separator
        while i < n and body[i].strip().startswith("|"):
            row = [c.strip() for c in body[i].strip().strip("|").split("|")]
            rows.append(row)
            i += 1
        add_table([header] + rows)
        continue
    if ln.startswith("---"):
        i += 1
        continue
    hm = re.match(r"^(#{1,6})\s+(.*)$", ln)
    if hm:
        level = len(hm.group(1))
        text = hm.group(2).strip()
        # shift down one: H2->Heading1, H3->Heading2, H4+->Heading3 (H1 title is the custom title block)
        mapped = {2: 1, 3: 2}.get(level, 3)
        style = f"Heading {mapped}"
        p = doc.add_paragraph(style=style)
        add_runs_with_markup(p, text)
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
    # normal paragraph
    p = doc.add_paragraph()
    add_runs_with_markup(p, ln)
    i += 1

# Footer page numbers
section = doc.sections[0]
footer = section.footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = fp.add_run()
fldChar1 = OxmlElement("w:fldChar"); fldChar1.set(qn("w:fldCharType"), "begin")
instrText = OxmlElement("w:instrText"); instrText.set(qn("xml:space"), "preserve"); instrText.text = "PAGE"
fldChar2 = OxmlElement("w:fldChar"); fldChar2.set(qn("w:fldCharType"), "end")
run._r.append(fldChar1); run._r.append(instrText); run._r.append(fldChar2)
run.font.size = Pt(8)

doc.save(OUT)
print("Saved:", OUT)
