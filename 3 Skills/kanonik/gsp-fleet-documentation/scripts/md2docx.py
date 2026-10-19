#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Converter Markdown profesional → DOCX (python-docx), tanpa pandoc/libreoffice.
Menangani: heading #..####, tabel pipe (header shading navy), bullet/numbered list,
bold/italic/code inline, blockquote, horizontal rule, code block, dan cover page terpisah.

Usage:
    python3 md2docx.py in.md out.docx \
        --title "JUDUL DOKUMEN" \
        --subtitle "Subtitle" \
        --meta "Nomor Dokumen=001/GSP/BRA/VIII/2026" \
        --meta "Klasifikasi=Terbatas — Internal" \
        --meta "Tanggal Terbit=21 Agustus 2026" \
        --meta "Disusun oleh=GSP Agent Headquarter — Brahma"

Catatan: TOC markdown tidak dijadikan field TOC Word otomatis; heading H1 tetap
terstruktur sehingga Word bisa generate TOC manual bila perlu.
"""
import argparse, os, re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x0F, 0x2A, 0x4A)
ACCENT = RGBColor(0x1F, 0x4E, 0x79)
GREY = RGBColor(0x59, 0x59, 0x59)
BODY = RGBColor(0x21, 0x21, 0x21)

def set_cell_bg(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)

def add_hr(doc):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1'); bottom.set(qn('w:color'), '0F2A4A')
    pBdr.append(bottom); pPr.append(pBdr)

INLINE_RE = re.compile(r'(\*\*.+?\*\*|\*.+?\*|`[^`]+`)')
def add_inline(p, text, base_bold=False, size=None, color=None):
    for tok in INLINE_RE.split(text):
        if not tok:
            continue
        if tok.startswith('**') and tok.endswith('**'):
            r = p.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith('`') and tok.endswith('`'):
            r = p.add_run(tok[1:-1]); r.font.name = 'Courier New'
            r._element.rPr.rFonts.set(qn('w:cs'), 'Courier New')
            r.font.size = Pt((size or 11) - 0.5)
        elif tok.startswith('*') and tok.endswith('*') and len(tok) > 2:
            r = p.add_run(tok[1:-1]); r.italic = True
        else:
            r = p.add_run(tok)
        r.bold = r.bold or base_bold
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = color

def set_style(doc):
    st = doc.styles['Normal']
    st.font.name = 'Calibri'; st.font.size = Pt(11); st.font.color.rgb = BODY
    st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.15
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
    for hname, sz, col in [('Heading 1', 16, NAVY), ('Heading 2', 14, ACCENT),
                           ('Heading 3', 12, ACCENT), ('Heading 4', 11.5, NAVY)]:
        h = doc.styles[hname]
        h.font.name = 'Calibri'; h.font.size = Pt(sz); h.font.bold = True
        h.font.color.rgb = col
        h.paragraph_format.space_before = Pt(14 if hname != 'Heading 1' else 20)
        h.paragraph_format.space_after = Pt(8 if hname != 'Heading 1' else 10)
        h.paragraph_format.keep_with_next = True

def add_table(doc, rows):
    ncols = max(len(r) for r in rows)
    tbl = doc.add_table(rows=len(rows), cols=ncols)
    tbl.style = 'Table Grid'; tbl.alignment = WD_TABLE_ALIGNMENT.CENTER; tbl.autofit = True
    for i, row in enumerate(rows):
        for j in range(ncols):
            cell = tbl.cell(i, j)
            txt = row[j] if j < len(row) else ''
            cell.text = ''
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2); p.paragraph_format.space_before = Pt(2)
            add_inline(p, txt, base_bold=(i == 0), size=9.5 if i == 0 else 10,
                       color=(RGBColor(0xFF, 0xFF, 0xFF) if i == 0 else BODY))
            if i == 0:
                set_cell_bg(cell, '0F2A4A')
            elif i % 2 == 0:
                set_cell_bg(cell, 'F2F6FA')
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def parse_markdown(md_path):
    lines = open(md_path, encoding='utf-8').read().split('\n')
    blocks = []; i = 0; in_code = False; codebuf = []
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith('```'):
            if in_code:
                blocks.append(('code', '\n'.join(codebuf))); codebuf = []; in_code = False
            else:
                in_code = True
            i += 1; continue
        if in_code:
            codebuf.append(ln); i += 1; continue
        if not ln.strip():
            i += 1; continue
        if ln.strip() == '---':
            blocks.append(('hr', '')); i += 1; continue
        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            blocks.append((f'h{len(m.group(1))}', m.group(2).strip())); i += 1; continue
        if ln.startswith('> '):
            buf = [ln[2:]]
            while i + 1 < len(lines) and lines[i + 1].startswith('> '):
                i += 1; buf.append(lines[i + 1][2:])
            blocks.append(('quote', '\n'.join(buf))); i += 1; continue
        if ln.strip().startswith('|'):
            buf = [ln]
            while i + 1 < len(lines) and lines[i + 1].strip().startswith('|'):
                i += 1; buf.append(lines[i + 1])
            rows = []
            for rl in buf:
                cells = [c.strip() for c in rl.strip().strip('|').split('|')]
                if re.match(r'^:?-{2,}:?$', cells[0].replace(' ', '')):
                    continue
                rows.append(cells)
            if rows:
                blocks.append(('table', rows))
            i += 1; continue
        m = re.match(r'^\s*[-*]\s+(.*)$', ln)
        if m:
            blocks.append(('bullet', m.group(1).strip())); i += 1; continue
        m = re.match(r'^\s*\d+[.)]\s+(.*)$', ln)
        if m:
            blocks.append(('numbered', m.group(1).strip())); i += 1; continue
        buf = [ln]
        while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(
                ('#', '|', '>', '- ', '* ', '```', '---')) and not re.match(r'^\s*\d+[.)]\s', lines[i + 1]):
            i += 1; buf.append(lines[i + 1])
        blocks.append(('para', ' '.join(x.strip() for x in buf))); i += 1; continue
    return blocks

def build_docx(md_path, out_path, title, subtitle, meta_rows):
    blocks = parse_markdown(md_path)
    doc = Document()
    for section in doc.sections:
        section.page_height = Cm(29.7); section.page_width = Cm(21.0)
        section.top_margin = Cm(2.5); section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3.0); section.right_margin = Cm(2.5)
    set_style(doc)

    # COVER PAGE
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('PT. GEMILANG SATRIA PERKASA'); r.bold = True; r.font.size = Pt(20); r.font.color.rgb = NAVY
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('DOKUMENTASI TEKNIS & ORGANISASI'); r.font.size = Pt(12); r.font.color.rgb = GREY
    for _ in range(3):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title); r.bold = True; r.font.size = Pt(26); r.font.color.rgb = NAVY
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(subtitle); r.font.size = Pt(14); r.font.color.rgb = ACCENT
    doc.add_paragraph(); add_hr(doc); doc.add_paragraph()
    meta_tbl = doc.add_table(rows=len(meta_rows), cols=2)
    meta_tbl.style = 'Table Grid'; meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (k, v) in enumerate(meta_rows):
        c0 = meta_tbl.cell(i, 0); c1 = meta_tbl.cell(i, 1)
        c0.text = ''; c1.text = ''
        r = c0.paragraphs[0].add_run(k); r.bold = True; r.font.size = Pt(11); r.font.color.rgb = NAVY
        add_inline(c1.paragraphs[0], v, size=11)
        set_cell_bg(c0, 'EAF0F6')
    doc.add_page_break()

    # KONTEN
    in_toc = False
    for kind, payload in blocks:
        if kind == 'h1':
            txt = payload.strip()
            if txt.upper() == 'DAFTAR ISI':
                in_toc = True
            elif txt.startswith('RINGKASAN'):
                in_toc = False
            doc.add_heading(txt, level=1)
        elif kind == 'h2':
            doc.add_heading(payload, level=2)
        elif kind == 'h3':
            doc.add_heading(payload, level=3)
        elif kind == 'h4':
            doc.add_heading(payload, level=4)
        elif kind == 'para':
            p = doc.add_paragraph()
            add_inline(p, payload, size=10.5 if in_toc else None, color=ACCENT if in_toc else None)
        elif kind == 'bullet':
            p = doc.add_paragraph(style='List Bullet'); add_inline(p, payload)
        elif kind == 'numbered':
            p = doc.add_paragraph(style='List Number'); add_inline(p, payload)
        elif kind == 'quote':
            p = doc.add_paragraph()
            pPr = p._p.get_or_add_pPr()
            pBdr = OxmlElement('w:pBdr'); left = OxmlElement('w:left')
            left.set(qn('w:val'), 'single'); left.set(qn('w:sz'), '12')
            left.set(qn('w:space'), '4'); left.set(qn('w:color'), '0F2A4A')
            pBdr.append(left); pPr.append(pBdr)
            p.paragraph_format.left_indent = Cm(0.6)
            add_inline(p, payload, size=10.5)
        elif kind == 'hr':
            add_hr(doc)
        elif kind == 'table':
            add_table(doc, payload)
        elif kind == 'code':
            p = doc.add_paragraph()
            pPr = p._p.get_or_add_pPr()
            shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), 'F2F2F2')
            pPr.append(shd)
            p.paragraph_format.left_indent = Cm(0.5)
            r = p.add_run(payload); r.font.name = 'Courier New'; r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            r._element.rPr.rFonts.set(qn('w:cs'), 'Courier New')
    doc.save(out_path)
    return out_path

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--meta", action="append", default=[], help='pasangan "K=V" berulang')
    args = ap.parse_args()
    meta = [tuple(kv.split("=", 1)) for kv in args.meta]
    out = build_docx(args.input, args.output, args.title, args.subtitle, meta)
    d = Document(out)
    print("WROTE", out, os.path.getsize(out), "bytes")
    print("paragraphs:", len(d.paragraphs), "| tables:", len(d.tables),
          "| headings:", sum(1 for p in d.paragraphs if p.style.name.startswith('Heading')))
