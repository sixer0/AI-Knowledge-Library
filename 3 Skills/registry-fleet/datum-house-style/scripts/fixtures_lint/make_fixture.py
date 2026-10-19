# -*- coding: utf-8 -*-
"""make_fixture.py — pembangkit corpus basal rusak untuk selftest datum_lint.
Hasil: basal_rusak.docx (nama mengandung underscore = bahan DATUM-38).
Setiap cacat ditanam sesuai butir yang harus ditangkap; lihat EXPECTED di datum_lint.selftest."""
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml

OUT = Path(__file__).resolve().parent / "basal_rusak.docx"
NSW = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

doc = Document()

# DATUM-05: wajah default Office dipakai langsung pada run (terlihat di document.xml)
p = doc.add_paragraph()
r = p.add_run("Teks sampul memakai wajah bawaan Office.")
r.font.name = "Calibri"
doc.styles["Normal"].font.name = "Calibri"

# DATUM-06: paragraf center di area sampul
p = doc.add_paragraph("SAMPUL PUSAT")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# DATUM-04: heading berbentuk pertanyaan
doc.add_heading("Apakah sistem ini aman?", level=1)
doc.add_heading("Berapa biaya total?", level=2)
# DATUM-03: em-dash di heading + padat di badan
doc.add_heading("Tinjauan \u2014 menyeluruh", level=2)
doc.add_paragraph("Nilai \u2014 penting \u2014 dicatat \u2014 dengan \u2014 em-dash \u2014 berlebihan \u2014 di sini.")

# DATUM-16 / 17 / 19: pola teks
doc.add_paragraph("Beban 50mm pada busbar dan arus 12% naik.")          # 16
doc.add_paragraph("Arus nominal \u00b13 A diberikan tanpa penjelasan.")   # 17
doc.add_paragraph("PPN 10 % dihitung dari harga jual.")                  # 19

# DATUM-11: angka beban-rilis telanjang berdiri sendiri
doc.add_paragraph("999,888 kW")

# DATUM-31: sumber Mermaid
doc.add_paragraph("graph TD")
doc.add_paragraph("A-->B")

# DATUM-01: baris ubin KPI (2x4, seluruh sel angka)
tk = doc.add_table(rows=2, cols=4)
for j, txt in enumerate(["Q1", "Q2", "Q3", "Q4"]):
    tk.rows[0].cells[j].text = txt
for j, txt in enumerate(["120,5", "31,2", "88,0", "7,4"]):
    tk.rows[1].cells[j].text = txt

# DATUM-07/09/10/20/21: tabel data angka tanpa satuan/SUMBER, insideV aktif,
# garis tipis sz=2, sel gabungan gridSpan, isian di luar palet
t = doc.add_table(rows=4, cols=3)
t._tbl.tblPr.append(parse_xml(
    '<w:tblBorders %s>'
    '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="101418"/>'
    '<w:top w:val="single" w:sz="2" w:space="0" w:color="101418"/>'
    '</w:tblBorders>' % NSW))
for j, txt in enumerate(["Item", "Jumlah", "Biaya"]):
    t.rows[0].cells[j].text = txt
for i, vals in enumerate([["Besi", "12,5", "480"], ["Beton", "31,2", "920"], ["Upah", "88,0", "150"]]):
    for j, txt in enumerate(vals):
        t.rows[i + 1].cells[j].text = txt
tc = t.rows[2].cells[1]._tc
tr = tc.getparent()
tcs = tr.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc')
tcPr = tc.get_or_add_tcPr()
tcPr.append(parse_xml('<w:gridSpan %s w:val="2"/>' % NSW))
tr.remove(tcs[2])  # gabung kolom 2+3 pada baris data -> sel gabungan sah
tcPr2 = t.rows[3].cells[0]._tc.get_or_add_tcPr()
tcPr2.append(parse_xml('<w:shd %s w:val="clear" w:color="auto" w:fill="EEEEEE"/>' % NSW))

# DATUM-02: callout terisi dengan pita warna
p = doc.add_paragraph("Kotak sorot terisi dengan bar warna.")
pPr = p._p.get_or_add_pPr()
pPr.append(parse_xml(
    '<w:pBdr %s><w:left w:val="single" w:sz="18" w:space="2" w:color="D98324"/></w:pBdr>' % NSW))
pPr.append(parse_xml('<w:shd %s w:val="clear" w:color="auto" w:fill="FFE9C6"/>' % NSW))

doc.save(str(OUT))
print("fixture ditulis:", OUT)
