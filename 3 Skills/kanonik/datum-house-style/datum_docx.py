# -*- coding: utf-8 -*-
"""
datum_docx.py — builder DOCX berbasis token paket datum-house-style v2.0.0
(kelas builder/render DHS-RB-05, 2026-10-05; kartu t_28d93e3c).

PROVENANS: pola helper diekstrak dari garis builder DATMANUAL terbukti
(build_manual_datum.py, penghasil docx 100 hal lolos VERIF-final-4 CHECK 1-14;
helper oei/style_run/fmt_para/fix_table/cell_borders/add_field/hyperlink_runs/
page_ground/setup_*/interior_footer diadaptasi verbatim-struktur) dan
build_contoh_datum_docx.py. SEMUA nilai gaya dibaca dari tokens.json lewat
datumbind.tokens_path() — tidak ada hex/nama font hardcoded (aturan paket #4).
Bukan restorasi mesin v1.8 Rev J (PUTUSAN-GAP-09 D-1).

Temuan E-04 (000 RevA L1000) dihormati: tidak ada build saat import; semua
eksekusi lewat __main__ atau pemanggil eksplisit.

Pemakaian:
    from datum_docx import DatumDocx
    D = DatumDocx(title="...", doc_no="00X/GSP-STD-X-2026", rev="A", ...)
    D.cover(); D.start_interior()
    D.heading("Judul pernyataan", level=1); D.para("prosa **tebal** `mono` https://tautan")
    D.table(rows, source="SUMBER ...", widths_mm=[40, 88])
    D.derivation(d)          # d = datumbind.Derivation yang sudah build()
    D.save("out.docx")       # guard N1 nama berkas + updateFields + properti inti

Setiap tabel/figur melewati datumcheck.situs-panggil (G1-G3+N1 + cek ulang
03/04/09/10/16) sebelum masuk dokumen — preseden 000 RevA tabel 8.2.
"""
import json, os, re, sys, datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import datumcheck as DC
from datumcheck import num_floor_mm, solve_widths
from datumbind import tokens_path, BindDefect

# ------------------------------------------------------------------ token
_TOK = json.load(open(tokens_path(), encoding="utf-8"))
_COL = _TOK["colour"]
_TYPE = _TOK["type"]
_GRID = _TOK["grid_mm"]
_RULES = _TOK["rules_mm"]
_SCALE = _TYPE["scale_pt"]
_FACES = _TYPE["faces"]

def face(role_key):
    """Nama wajah dari token (faces key), mis. 'serif'/'condensed'/'mono'."""
    return _FACES[role_key]

SERIF = face("serif"); COND = face("condensed"); MONO = face("mono")

def _hex(tok_hex):
    return tok_hex.lstrip("#").upper()

INK900 = _hex(_COL["interior"]["ink900"]); INK700 = _hex(_COL["interior"]["ink700"])
INK400 = _hex(_COL["interior"]["ink400"]); INK200 = _hex(_COL["interior"]["ink200"])
INK100 = _hex(_COL["interior"]["ink100"]); I_PAPER = _hex(_COL["interior"]["paper"])
SIGNAL = _hex(_COL["interior"]["signal"]); ALERT = _hex(_COL["interior"]["alert"])
VERD = _hex(_COL["interior"]["verd"]);     LINK = _hex(_COL["interior"]["link"])
W_PAPER = _hex(_COL["wrapper"]["paper"]);  SEAL = _hex(_COL["wrapper"]["seal"])
CREAM = _hex(_COL["wrapper"]["cream"])
MARKS = _TOK["marks"]

# tangga mm->sz dari token rules_mm (peta builder S1 baris 56-59)
_SZ_MAP = {_RULES["primary"]: _RULES["word_ladder_sz"][3],   # 0,45 -> sz10
           _RULES["below_header"]: _RULES["word_ladder_sz"][1],  # 0,25 -> sz6
           _RULES["hair"]: _RULES["word_ladder_sz"][0],      # 0,20 -> sz5
           _RULES["revision_bar"]: _RULES["word_ladder_sz"][4]}  # 0,50 -> sz11
SZ_045 = _SZ_MAP[_RULES["primary"]]; SZ_025 = _SZ_MAP[_RULES["below_header"]]
SZ_020 = _SZ_MAP[_RULES["hair"]];    SZ_050 = _SZ_MAP[_RULES["revision_bar"]]

CONTENT_W_MM = float(_GRID["text_column"])                    # 128
CONTENT_W_PT = CONTENT_W_MM / 25.4 * 72.0
FULL_W_MM = float(_GRID["full_span"])                         # 166
FULL_W_PT = FULL_W_MM / 25.4 * 72.0
# RAIL rev B (RAIL-1008, putusan user 08-10): rail = properti PER-PARAGRAF.
# Margin fisik halaman PENUH; paragraf berprovenans menyempit sendiri dengan
# w:ind right = gutter+rail, chip framePr menempati rail di kanannya.
RAIL_HOST_MM = float(_GRID["gutter"]) + float(_GRID["evidence_rail"])       # 38 mm
RAIL_W_TW = round(float(_GRID["evidence_rail"]) * 1440 / 25.4)              # 32 mm
RAIL_X_TW = round((float(_GRID["text_column"]) + float(_GRID["gutter"])) * 1440 / 25.4)  # 134 mm
# Bentuk byte kanonis framePr chip rail PASCA round-trip Word (repaginate+Save,
# jalur pages_measure). Word menulis ulang CT_FramePr ke bentuk minimal: hRule/
# yAlign hilang karena memang nilai default, urutan atribut dinormalisasi, dan
# hAnchor="margin" BERTAHAN (nama sah ECMA-376; kartu t_fcdd32ac ukur 09-10).
# Assert byte-jadi builder WAJIB membandingkan terhadap bentuk ini, BUKAN bentuk
# pra-save hasil helper. Nilai w/x diturunkan token (nol hardcode angka).
RAIL_FRAMEPR_POST = ('<w:framePr w:w="%d" w:wrap="none" w:hAnchor="margin" '
                     'w:x="%d"/>' % (RAIL_W_TW, RAIL_X_TW))
TEXT_BLOCK_H_MM = 247.0   # badan halaman A4 DATUM (DATUM-33 limit; M01 build table)

RPR_ORDER = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps",
             "strike", "dstrike", "outline", "shadow", "emboss", "imprint",
             "noProof", "snapToGrid", "vanish", "webHidden", "color", "spacing",
             "w", "kern", "position", "sz", "szCs", "highlight", "u", "vertAlign"]
PPR_ORDER = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr",
             "widowControl", "numPr", "suppressLineNumbers", "pBdr", "shd",
             "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
             "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN",
             "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind",
             "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc",
             "textDirection", "textAlignment"]
TBLPR_ORDER = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual",
               "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders",
               "shd", "tblLayout", "tblLook"]
TCPR_ORDER = ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders",
              "shd", "noWrap", "tcMar", "textDirection", "tcFitText",
              "vAlign", "hideMark"]


def oei(parent, order, el):
    """Sisipkan elemen mematuhi urutan skema OOXML (helper warisan S1)."""
    key = el.tag.split("}")[-1]
    idx = order.index(key) if key in order else len(order)
    pos = 0
    for child in parent:
        ckey = child.tag.split("}")[-1]
        cidx = order.index(ckey) if ckey in order else len(order)
        if cidx > idx:
            break
        pos += 1
    for existing in parent.findall(el.tag):
        parent.remove(existing)
    parent.insert(pos, el)


def val_el(tag, attr, v):
    el = OxmlElement(tag)
    el.set(qn("w:" + attr), str(v))
    return el


def style_run(r, font, size, color=None, bold=False, italic=False, track=None,
              underline=False):
    rPr = r._r.get_or_add_rPr()
    rf = OxmlElement("w:rFonts")
    for a in ("ascii", "hAnsi", "eastAsia", "cs"):
        rf.set(qn("w:" + a), font)
    oei(rPr, RPR_ORDER, rf)
    if bold:
        oei(rPr, RPR_ORDER, OxmlElement("w:b"))
    if italic:
        oei(rPr, RPR_ORDER, OxmlElement("w:i"))
    if color:
        oei(rPr, RPR_ORDER, val_el("w:color", "val", color))
    if underline:
        oei(rPr, RPR_ORDER, val_el("w:u", "val", "single"))
    if track is not None:
        oei(rPr, RPR_ORDER, val_el("w:spacing", "val", track))
    sz = int(round(size * 2))
    oei(rPr, RPR_ORDER, val_el("w:sz", "val", sz))
    oei(rPr, RPR_ORDER, val_el("w:szCs", "val", sz))


def fmt_para(p, line_pt=None, before=0.0, after=0.0, keep=False, align=None,
             page_break=False, indent=None, hanging=None, line_rule=None):
    pPr = p._p.get_or_add_pPr()
    if page_break:
        oei(pPr, PPR_ORDER, OxmlElement("w:pageBreakBefore"))
    if keep:
        oei(pPr, PPR_ORDER, OxmlElement("w:keepNext"))
    sp = OxmlElement("w:spacing")
    if line_pt is not None:
        sp.set(qn("w:line"), str(int(round(line_pt * 20))))
        sp.set(qn("w:lineRule"), "exact")
    elif line_rule == "auto":
        # ENH-C: lepas lineRule exact warisan gaya Normal tanpa memaku tinggi baris;
        # inline image butuh garis auto supaya bingkai garis mengikuti tinggi gambar,
        # bukan gambar meluber ke atas menggaruki paragraf sebelumnya (repro 08-10).
        sp.set(qn("w:line"), "240")
        sp.set(qn("w:lineRule"), "auto")
    sp.set(qn("w:before"), str(int(round(before * 20))))
    sp.set(qn("w:after"), str(int(round(after * 20))))
    oei(pPr, PPR_ORDER, sp)
    if indent is not None or hanging is not None:
        ind = OxmlElement("w:ind")
        if indent is not None:
            ind.set(qn("w:left"), str(int(round(indent * 20))))
        if hanging is not None:
            ind.set(qn("w:hanging"), str(int(round(hanging * 20))))
        oei(pPr, PPR_ORDER, ind)
    if align is not None:
        mapv = {WD_ALIGN_PARAGRAPH.JUSTIFY: "both", WD_ALIGN_PARAGRAPH.LEFT: "left",
                WD_ALIGN_PARAGRAPH.RIGHT: "right", WD_ALIGN_PARAGRAPH.CENTER: "center"}
        oei(pPr, PPR_ORDER, val_el("w:jc", "val", mapv[align]))


INLINE_RE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\*[^*\n]+(?<!\*)\*(?!\*)"
                       r"|https?://[^\s|)]+|doi\.org/[^\s|)<>,;]+|iso\.org/[^\s|)<>,;]+"
                       r"|(?<![\d./])10\.\d{4}/[^\s|)<>,;]+)")


class RelBag:
    """Pengumpul rel hyperlink per bagian dokumen (warisan S1)."""
    def __init__(self, doc):
        self.doc = doc

    def add(self, part, url):
        from docx.opc.constants import RELATIONSHIP_TYPE as RT
        return part.relate_to(url, RT.HYPERLINK, is_external=True)


def cell_fill(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    oei(tcPr, TCPR_ORDER, shd)


def cell_margins(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for tag, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        if v is None:
            continue
        el = OxmlElement("w:" + tag)
        el.set(qn("w:w"), str(int(round(v * 20))))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    oei(tcPr, TCPR_ORDER, mar)


def cell_borders(cell, spec):
    tcPr = cell._tc.get_or_add_tcPr()
    tb = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        if edge not in spec:
            continue
        v = spec[edge]
        el = OxmlElement("w:" + edge)
        if v == "none":
            el.set(qn("w:val"), "nil")
        else:
            sz, color = v
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(sz))
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), color)
        tb.append(el)
    oei(tcPr, TCPR_ORDER, tb)


def fix_table(table, widths_pt):
    table.autofit = False
    tblPr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    oei(tblPr, TBLPR_ORDER, layout)
    tw = val_el("w:tblW", "w", int(round(sum(widths_pt) * 20)))
    tw.set(qn("w:type"), "dxa")
    oei(tblPr, TBLPR_ORDER, tw)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:" + edge)
        el.set(qn("w:val"), "nil")
        borders.append(el)
    oei(tblPr, TBLPR_ORDER, borders)
    grid = table._tbl.find(qn("w:tblGrid"))
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths_pt):
        gc.set(qn("w:w"), str(int(round(w * 20))))
    for row in table.rows:
        for cell, w in zip(row.cells, widths_pt):
            tcW = OxmlElement("w:tcW")
            tcW.set(qn("w:w"), str(int(round(w * 20))))
            tcW.set(qn("w:type"), "dxa")
            oei(cell._tc.get_or_add_tcPr(), TCPR_ORDER, tcW)


def cell_text(cell, runs, line_pt, align=None):
    p = cell.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    fmt_para(p, line_pt=line_pt, align=align)
    for spec in runs:
        r = p.add_run(spec["t"])
        style_run(r, spec.get("f", COND), spec.get("s", 7.5), spec.get("c"),
                  spec.get("b", False), spec.get("i", False), spec.get("t2"))
    va = OxmlElement("w:vAlign")
    va.set(qn("w:val"), "center")
    oei(cell._tc.get_or_add_tcPr(), TCPR_ORDER, va)


def para_border(p, edge, sz, color):
    pPr = p._p.get_or_add_pPr()
    pbdr = pPr.find(qn("w:pBdr"))
    if pbdr is None:
        pbdr = OxmlElement("w:pBdr")
        oei(pPr, PPR_ORDER, pbdr)
    el = OxmlElement("w:" + edge)
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(max(sz, _RULES["word_ladder_sz"][0])))  # lantai photocopy
    el.set(qn("w:space"), "2")
    el.set(qn("w:color"), color)
    pbdr.append(el)


def tab_right(p, pos_twips, leader=None):
    pPr = p._p.get_or_add_pPr()
    tabs = OxmlElement("w:tabs")
    t = OxmlElement("w:tab")
    t.set(qn("w:val"), "right")
    if leader:
        t.set(qn("w:leader"), leader)
    t.set(qn("w:pos"), str(pos_twips))
    tabs.append(t)
    oei(pPr, PPR_ORDER, tabs)


def add_field(p, instr, cached="", font=None, size=6.2, color=None, bold=False):
    font = font or MONO; color = color or INK900
    r1 = p.add_run(); style_run(r1, font, size, color, bold)
    fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin")
    r1._r.append(fc)
    r2 = p.add_run(); style_run(r2, font, size, color, bold)
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
    it.text = " %s " % instr
    r2._r.append(it)
    r3 = p.add_run(); style_run(r3, font, size, color, bold)
    fs = OxmlElement("w:fldChar"); fs.set(qn("w:fldCharType"), "separate")
    r3._r.append(fs)
    r4 = p.add_run(cached); style_run(r4, font, size, color, bold)
    r5 = p.add_run(); style_run(r5, font, size, color, bold)
    fe = OxmlElement("w:fldChar"); fe.set(qn("w:fldCharType"), "end")
    r5._r.append(fe)


_NUM_RE = re.compile(r"^[\d.,%\u00b1\s\-]+\s*(%|x|mm|m|kVA|kW|Hz)?$")


class DatumDocx:
    """Dokumen DATUM lengkap: sampul wrapper + interior rail, semua gaya dari token."""

    def __init__(self, title, doc_no, rev, issue_date="", author="",
                 subject="", category="Report", comments="",
                 classification="BIASA", copies="SALINAN 01 DARI 01 \u00b7 "
                 "PENGGUNAAN INTERNAL GSP", n_pages_hint="2",
                 caption_sep=" - "):
        DC.name_guard(doc_no)
        self.title, self.doc_no, self.rev = title, doc_no, rev
        self.classification, self.copies = classification, copies
        self.n_pages_hint = n_pages_hint
        # FIX-DATUM-ENGINE (t_9b9494b6, vonis DIST-2 F-1): pemisah slug caption
        # adalah properti dokumen; default baru ASCII " - " agar zona badan
        # bersih U+00B7 tanpa sanitasi hilir. Edisi lama mereproduksi byte
        # asalnya lewat caption_sep=" \u00b7 " (glif chrome sampul/kepala/kaki
        # bukan lingkup tiket ini - sah per deklarasi D16).
        self.caption_sep = caption_sep
        self.rel_bag = RelBag(None)
        self.t_seq = 0
        self.f_seq = 0
        self.doc = Document()
        st = self.doc.styles["Normal"]
        st.font.name = SERIF
        st.font.size = Pt(_SCALE["body"]["size"])
        st.font.color.rgb = RGBColor.from_string(INK700)
        cp = self.doc.core_properties
        cp.title = title
        cp.author = author or "Divisi Engineering PT Gemilang Satria Perkasa"
        cp.subject = subject or title
        cp.category = category
        cp.comments = comments
        cp.created = datetime.datetime.now().replace(microsecond=0)
        cp.modified = cp.created
        # latar halaman: w:background + displayBackgroundShape (warisan S1 KD-05)
        bg = OxmlElement("w:background")
        bg.set(qn("w:color"), I_PAPER)
        self.doc.element.insert(0, bg)
        dbs = OxmlElement("w:displayBackgroundShape")
        sett = self.doc.settings.element
        zoom = sett.find(qn("w:zoom"))
        if zoom is not None:
            zoom.addnext(dbs)
        else:
            sett.insert(0, dbs)
        # G-DQ-12: updateFields true agar field halaman terisi saat dibuka.
        # Urutan skema CT_Settings: updateFields WAJIB sebelum w:compat — bila
        # di-append di ujung, Word membuangnya saat save (temuan uji COM DHS-RB-05).
        if sett.find(qn("w:updateFields")) is None:
            uf = OxmlElement("w:updateFields")
            uf.set(qn("w:val"), "true")
            compat = sett.find(qn("w:compat"))
            if compat is not None:
                compat.addprevious(uf)
            else:
                sett.append(uf)
        self.rel_bag.doc = self.doc

    # ------------------------------------------------------------- sampul
    def setup_cover(self, sec):
        # FIX-LAYOUT t_038cc407 (06-10): grid_mm.page dalam mm; Cm butuh cm —
        # konvensi /10.0 sama dengan margin. Tanpa ini halaman jadi 210x297 CM
        # dan Word membungkus pgSz ke 16-bit saat save embed (53519x37306).
        sec.page_width, sec.page_height = Cm(_GRID["page"][0] / 10.0), Cm(_GRID["page"][1] / 10.0)
        m = _GRID["inner_margin"] / 10.0
        sec.left_margin, sec.right_margin = Cm(m), Cm(m - 0.4)
        sec.top_margin, sec.bottom_margin = Cm(2.60), Cm(2.40)
        sec.header_distance, sec.footer_distance = Cm(1.30), Cm(1.30)

    def cover(self, kicker="", deck="", identity=None):
        sec = self.doc.sections[0]
        self.setup_cover(sec)
        s = _SCALE["chapter_kicker"]
        p = self.doc.add_paragraph(); fmt_para(p, line_pt=1)
        style_run(p.add_run(""), COND, 1)
        band = self.doc.add_table(rows=1, cols=2)
        fix_table(band, [CONTENT_W_PT / 2, CONTENT_W_PT / 2])
        for cell, txt in zip(band.rows[0].cells,
                             ["KLASIFIKASI \u00b7 " + self.classification, self.copies]):
            cell_fill(cell, SEAL)
            cell_text(cell, [{"t": txt, "f": COND, "s": 7.5, "c": "FFFFFF", "b": True}],
                      line_pt=12)
        spacer_pt = 120
        self._spacer(spacer_pt)
        if kicker:
            p = self.doc.add_paragraph(); fmt_para(p, line_pt=12, after=4)
            style_run(p.add_run(kicker.upper()), face(s["face"]), s["size"], SIGNAL,
                      bold=True, track=int(s.get("track_em", 0) * 1000))
        p = self.doc.add_paragraph(); fmt_para(p, line_pt=26, after=6)
        cs = _SCALE["chapter_title"]
        style_run(p.add_run(self.title), face(cs["face"]), 20, INK900, bold=True)
        if deck:
            p = self.doc.add_paragraph(); fmt_para(p, line_pt=14, after=10)
            style_run(p.add_run(deck), SERIF, 10.5, INK700)
        for l1, v1, l2, v2 in (identity or []):
            p = self.doc.add_paragraph(); fmt_para(p, line_pt=12, before=2)
            style_run(p.add_run(l1 + "  "), COND, 7, INK400, bold=True)
            style_run(p.add_run(v1 + "    "), MONO, 8.5, INK900, bold=True)
            style_run(p.add_run(l2 + "  "), COND, 7, INK400, bold=True)
            style_run(p.add_run(v2), MONO, 8.5, INK900, bold=True)
        return self

    # ------------------------------------------------------------ interior
    def setup_interior(self, sec):
        # FIX-LAYOUT t_038cc407 (06-10): mm -> cm, sama seperti setup_cover.
        # RAIL rev B (RAIL-1008 putusan user 08-10): margin fisik PENUH
        # (kanan = outer_margin saja); rail menjadi properti per-paragraf
        # lewat rail_host()/rail_chip(), bukan pemangkasan margin halaman.
        sec.page_width, sec.page_height = Cm(_GRID["page"][0] / 10.0), Cm(_GRID["page"][1] / 10.0)
        lm = _GRID["inner_margin"] / 10.0
        rm = _GRID["outer_margin"] / 10.0
        sec.left_margin, sec.right_margin = Cm(lm), Cm(rm)
        sec.top_margin, sec.bottom_margin = Cm(2.60), Cm(2.60)
        sec.header_distance, sec.footer_distance = Cm(1.00), Cm(0.90)

    def start_interior(self, chapter_label=""):
        sec = self.doc.add_section(WD_SECTION.NEW_PAGE)
        self.setup_interior(sec)
        sec.header.is_linked_to_previous = False
        hp = sec.header.paragraphs[0]
        fmt_para(hp, line_pt=9.0)
        tab_right(hp, int(round(FULL_W_PT * 20)))   # RAIL rev B: kepala full-span 166 mm
        rh = _SCALE["running_head"]
        style_run(hp.add_run("PT GEMILANG SATRIA PERKASA \u00b7 " + chapter_label + "\t"),
                  face(rh["face"]), rh["size"], INK400)
        style_run(hp.add_run(self.classification.upper()), face(rh["face"]),
                  rh["size"], ALERT, bold=True, track=12)
        rp = sec.header.add_paragraph(); fmt_para(rp, line_pt=2.5)
        para_border(rp, "bottom", SZ_020, INK200)   # garis 166 mm di bawah kepala (full-span)
        self._footer_register(sec)
        return sec

    def _footer_register(self, sec):
        """Blok register kaki empat sel mono: nomor | REV | LEMBAR n/N | kelas.
        RAIL rev B: lebar penuh 166 mm (sebelumnya terpangkas 128 mm)."""
        sec.footer.is_linked_to_previous = False
        ft = sec.footer.add_table(rows=1, cols=4, width=Cm(FULL_W_MM / 10.0))
        _f = FULL_W_MM / CONTENT_W_MM
        fix_table(ft, [120.0 * _f, 95.0 * _f, 95.0 * _f, 52.8 * _f])
        cells = ft.rows[0].cells
        for c in cells:
            cell_borders(c, {"top": (SZ_045, INK900), "bottom": "none",
                             "left": "none", "right": "none"})
            cell_margins(c, top=1.5, bottom=0, left=0, right=4)

        def mix(cell, parts):
            p = cell.paragraphs[0]
            for r0 in list(p.runs):
                r0._r.getparent().remove(r0._r)
            fmt_para(p, line_pt=9.5)
            for t, b in parts:
                r = p.add_run(t)
                style_run(r, MONO, 6.2, INK900 if b else INK400, bold=b)
        mix(cells[0], [("GSP \u00b7 ", False), (self.doc_no, True)])
        mix(cells[1], [("REV ", False), (self.rev, True)])
        p = cells[2].paragraphs[0]
        for r0 in list(p.runs):
            r0._r.getparent().remove(r0._r)
        fmt_para(p, line_pt=9.5)
        r = p.add_run("LEMBAR "); style_run(r, MONO, 6.2, INK900, bold=True)
        add_field(p, "PAGE", "2", bold=True)
        r = p.add_run(" DARI "); style_run(r, MONO, 6.2, INK900, bold=True)
        add_field(p, "NUMPAGES", self.n_pages_hint, bold=True)
        mix(cells[3], [(self.classification.upper(), False)])

    # -------------------------------------------------------------- konten
    def _spacer(self, pt):
        p = self.doc.add_paragraph(); fmt_para(p, line_pt=pt)
        style_run(p.add_run(""), COND, 1)
        return p

    def heading(self, text, level=1, page_break=False):
        """Judul = pernyataan. Cek 04 (question-form) ditegakkan di situs-panggil."""
        DC.check_heading(text)
        key = "chapter_title" if level == 1 else "section_heading"
        s = _SCALE[key]
        p = self.doc.add_paragraph()
        fmt_para(p, line_pt=s.get("leading", s["size"] * 1.25),
                 before=10 if level == 1 else 6, after=4, keep=True,
                 page_break=page_break)
        style_run(p.add_run(text.upper() if s.get("upper") else text),
                  face(s["face"]), s["size"], _hex(_COL["interior"][s["colour"]]),
                  bold=(s["weight"] >= 600),
                  track=int(s.get("track_em", 0) * 1000) or None)
        return p

    def _hyperlink_runs(self, p, url, base_size, text=None):
        rid = self.rel_bag.add(p.part, url)
        h = OxmlElement("w:hyperlink")
        h.set(qn("r:id"), rid)
        r_el = OxmlElement("w:r")
        rPr = OxmlElement("w:rPr")
        rf = OxmlElement("w:rFonts")
        for a in ("ascii", "hAnsi", "cs"):
            rf.set(qn("w:" + a), MONO)
        rPr.append(rf)
        rPr.append(val_el("w:color", "val", LINK))       # SPK-002 butir 8: warna tegas
        rPr.append(val_el("w:u", "val", "single"))       # + garis bawah terlihat
        szv = int(round((base_size - 0.8) * 2))
        rPr.append(val_el("w:sz", "val", szv))
        r_el.append(rPr)
        t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve")
        t.text = text or url
        r_el.append(t)
        h.append(r_el)
        p._p.append(h)

    def _inline(self, container, text, base, line_pt, **kw):
        """Parser inline md-lite (bold/mono/italic/url->hyperlink) warisan S1."""
        p = container.add_paragraph()
        fmt_para(p, line_pt=line_pt, **kw)
        for tok in INLINE_RE.split(text):
            if not tok:
                continue
            if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
                r = p.add_run(tok[2:-2])
                style_run(r, base["f"], base["s"], base["c"], True)
            elif tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
                r = p.add_run(tok[1:-1])
                style_run(r, MONO, base["s"] - 0.8, base["c"])
            elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
                r = p.add_run(tok[1:-1])
                style_run(r, base["f"], base["s"], base["c"], italic=True)
            elif re.match(r"^(https?://|doi\.org/|iso\.org/)", tok):
                url = tok.rstrip(".,;)")
                tgt = ("https://" + url) if url.startswith(("doi.org/", "iso.org/")) else url
                self._hyperlink_runs(p, tgt, base["s"], text=tok.rstrip(".,;)"))
            elif re.match(r"^10\.\d{4}/", tok):
                url = tok.rstrip(".,;)")
                self._hyperlink_runs(p, "https://doi.org/" + url, base["s"], text=url)
            else:
                DC.check_value_unit(tok)      # cek 16 di situs-panggil
                r = p.add_run(tok)
                style_run(r, base["f"], base["s"], base["c"])
        return p

    def para(self, text, role="body", align=None, keep=False):
        s = _SCALE[role]
        base = {"f": face(s["face"]), "s": s["size"], "c": _hex(_COL["interior"][s["colour"]])}
        return self._inline(self.doc, text, base, s.get("leading", s["size"] * 1.4),
                            after=4, keep=keep, align=align)

    # ------------------------------------------------ rail bukti per-paragraf
    def rail_host(self, p):
        """RAIL rev B (RAIL-1008): sempitkan paragraf inang ke kolom 128 mm
        lewat w:ind right = gutter+rail (38 mm) TANPA memangkas margin halaman.
        Dipanggil hanya untuk paragraf yang benar-benar berprovenans."""
        pPr = p._p.get_or_add_pPr()
        ind = pPr.find(qn("w:ind"))
        if ind is None:
            ind = OxmlElement("w:ind")
            oei(pPr, PPR_ORDER, ind)
        ind.set(qn("w:right"), str(int(round(RAIL_HOST_MM * 1440 / 25.4))))  # 38 mm
        return p

    def rail_chip(self, text, role="evidence_rail"):
        """Satu chip provenans di rail 32 mm: paragraf ber-w:framePr melekat
        hAnchor=margin offset 134 mm, wrap none, yAlign auto (mengikuti aliran).
        Nama atribut SAH ECMA-376 CT_FramePr adalah w:hAnchor (BUKAN w:anchorH —
        nama tak dikenal Word dibuang saat repaginate lalu ditulis default
        hAnchor="text"; defect CTXWIN-1009, kartu t_fcdd32ac). Bentuk byte yang
        DIUKUR builder = bentuk PASCA round-trip Word: lihat RAIL_FRAMEPR_POST.
        Gaya dibaca runtime dari token (role evidence_rail), nol hardcode."""
        s = _SCALE[role]
        p = self.doc.add_paragraph()
        pPr = p._p.get_or_add_pPr()
        fr = OxmlElement("w:framePr")
        fr.set(qn("w:w"), str(RAIL_W_TW))
        fr.set(qn("w:hRule"), "auto")
        fr.set(qn("w:wrap"), "none")
        fr.set(qn("w:hAnchor"), "margin")
        fr.set(qn("w:x"), str(RAIL_X_TW))
        fr.set(qn("w:yAlign"), "auto")
        oei(pPr, PPR_ORDER, fr)
        fmt_para(p, line_pt=s.get("leading", s["size"] * 1.4))
        ctxt = text.upper() if s.get("upper") else text
        style_run(p.add_run(ctxt), face(s["face"]), s["size"],
                  _hex(_COL["interior"][s["colour"]]))
        return p

    def derivation(self, d):
        """Blok derivasi datumbind: label + baris mono + penutup asumsi (DATUM \u00a78)."""
        label, lines, note = d.build()
        s = _SCALE["derivation"]
        p = self.doc.add_paragraph(); fmt_para(p, line_pt=11, before=6, after=2, keep=True)
        style_run(p.add_run(label), COND, 8.5, INK900, bold=True)
        for ln in lines:
            p = self.doc.add_paragraph(); fmt_para(p, line_pt=s["leading"])
            style_run(p.add_run(ln), MONO, s["size"], _hex(_COL["interior"][s["colour"]]))
        p = self.doc.add_paragraph(); fmt_para(p, line_pt=11, after=6)
        style_run(p.add_run(note), SERIF, 8.5, INK400, italic=True)
        return self

    def table(self, rows, source, widths_mm=None, apparatus=False):
        """Tabel konten DATUM: caption ATAS + SUMBER bawah, tanpa garis vertikal,
        kepala berulang (w:tblHeader), kolom angka rata kanan MONO.
        Semua baris/lebar/teks melewati datumcheck situs-panggil dulu."""
        rows = [[str(c) for c in r] for r in rows]
        ncols = len(rows[0])
        if widths_mm is None:
            # L-01: solver lantai (satu matcher dengan build_rakit.py) agar kolom
            # angka bergrup titik tidak wrap-digit. widths_mm eksplisit tetap
            # dihormati dan diuji G4 di bawah, bukan dihitung ulang.
            widths_mm = solve_widths(rows, CONTENT_W_MM)
        self.t_seq += 1
        tid = "TABEL %d" % self.t_seq
        if not apparatus:
            DC.table_guards(tid, rows, widths_mm)
        widths_pt = [w / 25.4 * 72.0 for w in widths_mm]
        if not apparatus:
            heads = [h for h in rows[0] if h][:3]
            slug = self.caption_sep.join(heads).upper()[:64] or "TANPA LABEL KEPALA"
            p = self.doc.add_paragraph()
            fmt_para(p, line_pt=10.5, before=6.0, after=2.0, keep=True)
            style_run(p.add_run(tid + " "), MONO, 7.5, INK900, bold=True, track=8)
            style_run(p.add_run(slug + ". "), COND, 7.5, INK700, bold=True)
            style_run(p.add_run("memuat %d kepala kolom sepanjang %d baris data."
                                % (len([h for h in rows[0] if h]), len(rows) - 1)),
                      COND, 7.0, INK400)
        tbl = self.doc.add_table(rows=len(rows), cols=ncols)
        fix_table(tbl, widths_pt)
        ts = _SCALE["table_body"]; ns = _SCALE["table_numerals"]
        hs = _SCALE["table_header"]
        numeric_col = []
        for c in range(ncols):
            vals = [rows[r][c] for r in range(1, len(rows))]
            num = sum(1 for v in vals if _NUM_RE.match(v)) if vals else 0
            numeric_col.append(bool(vals) and num >= max(1, int(0.7 * len(vals))))
        for ri, row in enumerate(rows):
            for ci, val in enumerate(row):
                cell = tbl.rows[ri].cells[ci]
                cell_margins(cell, top=1.2, bottom=1.2, left=0, right=4)
                if ri == 0:
                    cell_borders(cell, {"top": (SZ_045, INK900),
                                        "bottom": (SZ_025, INK400),
                                        "left": "none", "right": "none"})
                    trPr = tbl.rows[0]._tr.get_or_add_trPr()
                    trPr.append(OxmlElement("w:cantSplit"))
                    th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true")
                    trPr.append(th)
                    cell_text(cell, [{"t": val, "f": face(hs["face"]), "s": 7.0,
                                      "c": INK900, "b": True, "t2": 12}], line_pt=10.5)
                else:
                    cell_borders(cell, {"bottom": (SZ_020, INK200), "top": "none",
                                        "left": "none", "right": "none"})
                    tbl.rows[ri]._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
                    if numeric_col[ci]:
                        cell_text(cell, [{"t": val, "f": MONO, "s": ns["size"],
                                          "c": INK900}],
                                  line_pt=10.5, align=WD_ALIGN_PARAGRAPH.RIGHT)
                    else:
                        p = cell.paragraphs[0]
                        for r0 in list(p.runs):
                            r0._r.getparent().remove(r0._r)
                        fmt_para(p, line_pt=10.5)
                        for tk in INLINE_RE.split(val):
                            if not tk:
                                continue
                            if tk.startswith("`") and tk.endswith("`") and len(tk) > 2:
                                r = p.add_run(tk[1:-1]); style_run(r, MONO, 6.8, INK900)
                            elif tk.startswith("**") and tk.endswith("**"):
                                r = p.add_run(tk[2:-2]); style_run(r, COND, ts["size"], INK900, bold=True)
                            elif re.match(r"^(https?://|doi\.org/|iso\.org/)", tk):
                                url = tk.rstrip(".,;)")
                                tgt = ("https://" + url) if url.startswith(("doi.org/", "iso.org/")) else url
                                self._hyperlink_runs(p, tgt, ts["size"], text=tk.rstrip(".,;)"))
                            elif re.match(r"^10\.\d{4}/", tk):
                                url = tk.rstrip(".,;)")
                                self._hyperlink_runs(p, "https://doi.org/" + url,
                                                     ts["size"], text=url)
                            else:
                                r = p.add_run(tk); style_run(r, COND, ts["size"], INK700)
                        va = OxmlElement("w:vAlign"); va.set(qn("w:val"), "center")
                        oei(cell._tc.get_or_add_tcPr(), TCPR_ORDER, va)
        if not apparatus:
            DC.check_source_line(source, tid)     # cek 10: wajib baris SUMBER
            p = self.doc.add_paragraph()
            fmt_para(p, line_pt=9.0, before=1.5, after=6.0)
            para_border(p, "top", SZ_020, INK200)
            style_run(p.add_run("SUMBER "), MONO, 6.5, INK400, bold=True)
            style_run(p.add_run(source + "  "), MONO, 6.5, INK400)
            style_run(p.add_run("PROVENANS " + MARKS["PEMASOK"] + " PEMASOK"),
                      MONO, 6.5, INK400)
        self._spacer(6)
        return tbl

    def figure(self, image_path, w_mm, h_mm, caption, source):
        """Gambar: guard N1 nama berkas + DATUM-33 tinggi <= blok teks 247 mm +
        caption + SUMBER (cek 29/30)."""
        DC.name_guard(os.path.basename(image_path))
        DC.figure_guards(caption, h_mm)
        DC.check_source_line(source, caption[:40])
        DC.px_guard(image_path, w_mm)   # ENH-D E-08: resolusi efektif >= 150 dpi
        p = self.doc.add_paragraph()
        # ENH-C: garis auto (bukan exact setinggi gambar) + keepNext; exact memaksa
        # Word menggambar gambar meluber ke atas garis dan menimpa paragraf sebelum
        # figur pada paginasi tertentu (cacat EOSADINT RevB hlm 11/15/29, repro 08-10).
        fmt_para(p, line_rule="auto", before=6, keep=True)
        r = p.add_run()
        r.add_picture(image_path, width=Cm(w_mm / 10.0), height=Cm(h_mm / 10.0))
        self.f_seq += 1
        p = self.doc.add_paragraph(); fmt_para(p, line_pt=10.5, after=2, keep=True)
        style_run(p.add_run("GAMBAR %d " % self.f_seq), MONO, 7.5, INK900, bold=True, track=8)
        style_run(p.add_run(caption), COND, 7.2, INK700)
        p = self.doc.add_paragraph(); fmt_para(p, line_pt=9.0, before=1.5, after=6)
        para_border(p, "top", SZ_020, INK200)
        style_run(p.add_run("SUMBER "), MONO, 6.5, INK400, bold=True)
        style_run(p.add_run(source), MONO, 6.5, INK400)
        return self

    def save(self, path):
        DC.name_guard(os.path.basename(path))
        self.doc.save(path)
        return path



# ---------------------------------------------------------------- chip rail: lapis baca
def chip_texts_para(body_xml):
    """Lapis baca KANONIS teks chip rail untuk assert konten-kekal (G-RAIL-1c).

    Kembalikan list teks gabungan per PARAGRAF ber-w:framePr (satu entri per chip),
    sudah di-strip. Bandingkan terhadap manifest di sini, BUKAN di lapis w:r per-run:
    dengan hAnchor="margin" aktif Word merepaginasi run yang melewati lebar frame saat
    round-trip embed dan memecah satu chip menjadi dua w:r, sehingga sensor per-run
    positif-palsu 'chip hilang' (terukur pada byte post-embed attr-margin/attr-minmargin,
    kartu t_fcdd32ac; vonis ulang manager t_618c93d4; preseden pitfalls #9 skill
    gsp-verification-before-completion). Konten paragraf kekal -> lapis paragraf bersih.

    Menerima bytes/str XML part word/document.xml ATAU path .docx. Tidak mengubah
    semantik G-RAIL-1..3: hanya menyeragamkan LAPIS PEMBACAAN. Builder masa depan WAJIB
    memanggil fungsi ini alih-alih merakit pembacaan per-run sendiri.
    """
    import zipfile as _zip
    from xml.etree import ElementTree as _ET

    W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

    def _q(tag):
        return "{%s}%s" % (W, tag)

    if isinstance(body_xml, (bytes, bytearray)) and body_xml[:2] == b"PK":
        body_xml = _zip.ZipFile(__import__("io").BytesIO(body_xml)).read("word/document.xml")
    if isinstance(body_xml, (bytes, bytearray)):
        root = _ET.fromstring(body_xml)
    elif hasattr(body_xml, "read"):                      # file-like
        root = _ET.fromstring(body_xml.read())
    elif isinstance(body_xml, str) and body_xml.lower().endswith(".docx"):
        root = _ET.fromstring(_zip.ZipFile(body_xml).read("word/document.xml"))
    elif isinstance(body_xml, str):                      # mentah XML string
        root = _ET.fromstring(body_xml.encode("utf-8"))
    else:
        raise TypeError("chip_texts_para: input harus bytes XML, str XML/path .docx, atau file-like")

    out = []
    for p in root.iter(_q("p")):
        pPr = p.find(_q("pPr"))
        if pPr is None or pPr.find(_q("framePr")) is None:
            continue
        joined = "".join(t.text or "" for t in p.iter(_q("t"))).strip()
        if joined:
            out.append(joined)
    return out


if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
