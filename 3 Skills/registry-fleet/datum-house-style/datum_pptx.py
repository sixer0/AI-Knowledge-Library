# -*- coding: utf-8 -*-
"""
datum_pptx.py — builder deck presentasi DATUM berbasis token v2.0.0
(kelas builder/render DHS-RB-05, 2026-10-05; kartu t_28d93e3c).

PROVENANS: TIDAK ada garis builder pptx terbukti di disk (probe find/grep
05-10 pada docs/ = 0 konsumen python-pptx terverifikasi untuk DATUM). Modul ini
karena itu kelas BARU token-driven: palet dan wajah dibaca dari tokens.json
(colour.interior/wrapper + type.faces/scale) lewat datumbind.tokens_path();
chrome mengikuti pola DOCX terbukti (pita klasifikasi MAROON kapital condensed,
eyebrow signal amber, judul condensed bold ink900, badan serif). Provenans
butir-per-butir: sumber = tokens.json + spec 000 RevA Tabel 3.2-3.4; BUKAN
restorasi Rev J. Limit guard nama N1 ditegakkan saat save.

Pemakaian:
    from datum_pptx import DatumDeck
    K = DatumDeck(title="...", doc_no="00X-...", rev="A")
    K.title_slide(kicker="...", deck="satu kalimat")
    s = K.content_slide("Judul pernyataan")
    K.bullet(s, "isi", level=0)
    K.table_slide("Tabel 1 · Judul pernyataan", rows, source="SUMBER ...")
    K.save("out.pptx")
"""
import json, os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

import datumcheck as DC
from datumbind import tokens_path

_TOK = json.load(open(tokens_path(), encoding="utf-8"))
_COL = _TOK["colour"]
_TYPE = _TOK["type"]
_FACES = _TYPE["faces"]
_SCALE = _TYPE["scale_pt"]

def rgb(tok_hex):
    return RGBColor.from_string(tok_hex.lstrip("#").upper())

INK900 = rgb(_COL["interior"]["ink900"]); INK700 = rgb(_COL["interior"]["ink700"])
INK400 = rgb(_COL["interior"]["ink400"]); INK200 = rgb(_COL["interior"]["ink200"])
PAPER = rgb(_COL["interior"]["paper"]); SIGNAL = rgb(_COL["interior"]["signal"])
ALERT = rgb(_COL["interior"]["alert"]); LINKC = rgb(_COL["interior"]["link"])
SEAL = rgb(_COL["wrapper"]["seal"]); WHITE = RGBColor(0xFF, 0xFF, 0xFF)

COND = _FACES["condensed"]; SERIF = _FACES["serif"]; MONO = _FACES["mono"]

# kanvas 16:9 DATUM (lebar tetap; tinggi turunan)
SLIDE_W = Inches(13.333); SLIDE_H = Inches(7.5)


class DatumDeck:
    def __init__(self, title, doc_no, rev, author="", classification="BIASA"):
        DC.name_guard(doc_no)
        self.title, self.doc_no, self.rev = title, doc_no, rev
        self.classification = classification
        self.prs = Presentation()
        self.prs.slide_width = SLIDE_W
        self.prs.slide_height = SLIDE_H
        cp = self.prs.core_properties
        cp.title = title
        cp.author = author or "Divisi Engineering PT Gemilang Satria Perkasa"
        cp.comments = f"{doc_no} Rev {rev} gaya DATUM v2.0 (token-driven)"
        self.blank = self.prs.slide_layouts[6]

    def _band(self, slide, text_left, text_right=None):
        """Pita klasifikasi MAROON setinggi 0.42 in di puncak (pola wrapper S1)."""
        from pptx.enum.shapes import MSO_SHAPE
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, Inches(0.42))
        bar.fill.solid(); bar.fill.fore_color.rgb = SEAL
        bar.line.fill.background()
        tf = bar.text_frame
        tf.margin_top = tf.margin_bottom = Pt(2)
        r = tf.paragraphs[0].add_run(); r.text = text_left
        r.font.name = COND; r.font.size = Pt(10); r.font.bold = True
        r.font.color.rgb = WHITE
        if text_right:
            p2 = tf.paragraphs[0]
            r2 = p2.add_run(); r2.text = "\t" * 6 + text_right
            r2.font.name = COND; r2.font.size = Pt(10); r2.font.bold = True
            r2.font.color.rgb = WHITE
        return bar

    def _textbox(self, slide, l, t, w, h):
        tb = slide.shapes.add_textbox(l, t, w, h)
        return tb.text_frame

    def title_slide(self, kicker="", deck=""):
        s = self.prs.slides.add_slide(self.blank)
        self._band(s, "KLASIFIKASI \u00b7 " + self.classification.upper(),
                   f"{self.doc_no} \u00b7 REV {self.rev}")
        ks = _SCALE["chapter_kicker"]
        tf = self._textbox(s, Inches(0.9), Inches(2.4), Inches(11.5), Inches(0.5))
        r = tf.paragraphs[0].add_run(); r.text = kicker.upper()
        r.font.name = COND; r.font.size = Pt(ks["size"] * 1.6)
        r.font.bold = True; r.font.color.rgb = SIGNAL
        cs = _SCALE["chapter_title"]
        tf = self._textbox(s, Inches(0.9), Inches(3.0), Inches(11.5), Inches(1.6))
        r = tf.paragraphs[0].add_run(); r.text = self.title
        r.font.name = COND; r.font.size = Pt(34)
        r.font.bold = True; r.font.color.rgb = INK900
        if deck:
            tf = self._textbox(s, Inches(0.9), Inches(4.7), Inches(11.5), Inches(0.8))
            r = tf.paragraphs[0].add_run(); r.text = deck
            r.font.name = SERIF; r.font.size = Pt(16); r.font.color.rgb = INK700
        return s

    def content_slide(self, heading):
        """Judul = pernyataan (CEK-04 ditegakkan di situs-panggil)."""
        DC.check_heading(heading)
        s = self.prs.slides.add_slide(self.blank)
        self._band(s, self.title + "  \u00b7  " + self.classification.upper())
        tf = self._textbox(s, Inches(0.9), Inches(0.7), Inches(11.5), Inches(0.9))
        r = tf.paragraphs[0].add_run(); r.text = heading
        sh = _SCALE["section_heading"]
        r.font.name = COND; r.font.size = Pt(20); r.font.bold = True
        r.font.color.rgb = INK900
        return s

    def bullet(self, slide, text, level=0, size=14):
        body = getattr(slide, "_datum_body", None)
        if body is None:
            body = self._textbox(slide, Inches(1.1), Inches(1.8),
                                 Inches(11.1), Inches(5.2))
            slide._datum_body = body
        p = body.paragraphs[0] if not body.paragraphs[0].runs else body.add_paragraph()
        p.level = level
        r = p.add_run(); r.text = text
        r.font.name = SERIF; r.font.size = Pt(size); r.font.color.rgb = INK700
        return p

    def table_slide(self, heading, rows, source):
        """Tabel DATUM: tanpa garis vertikal digambar manual (grid default mati),
        kepala condensed kapital, angka MONO. CEK-10 SUMBER wajib."""
        DC.check_heading(heading)
        DC.check_source_line(source, heading[:40])
        ncols = len(rows[0])
        DC.table_guards(heading[:24], [[str(c) for c in r] for r in rows],
                        [128.0 / ncols] * ncols)
        s = self.prs.slides.add_slide(self.blank)
        self._band(s, self.title + "  \u00b7  " + self.classification.upper())
        tf = self._textbox(s, Inches(0.9), Inches(0.7), Inches(11.5), Inches(0.9))
        r = tf.paragraphs[0].add_run(); r.text = heading
        r.font.name = COND; r.font.size = Pt(20); r.font.bold = True
        r.font.color.rgb = INK900
        nrows = len(rows)
        tbl_shape = s.shapes.add_table(nrows, ncols, Inches(0.9), Inches(1.8),
                                       Inches(11.5), Inches(0.4 * nrows))
        tbl = tbl_shape.table
        for ri, row in enumerate(rows):
            for ci, val in enumerate(row):
                cell = tbl.cell(ri, ci)
                cell.text = str(val)
                pr = cell.text_frame.paragraphs[0]
                for rn in pr.runs:
                    if ri == 0:
                        rn.font.name = COND; rn.font.size = Pt(11)
                        rn.font.bold = True; rn.font.color.rgb = INK900
                    else:
                        rn.font.name = SERIF; rn.font.size = Pt(11)
                        rn.font.color.rgb = INK700
        tf = self._textbox(s, Inches(0.9), Inches(6.7), Inches(11.5), Inches(0.4))
        r = tf.paragraphs[0].add_run(); r.text = "SUMBER " + source
        r.font.name = MONO; r.font.size = Pt(9); r.font.color.rgb = INK400
        return s

    def save(self, path):
        DC.name_guard(os.path.basename(path))
        self.prs.save(path)
        return path


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
