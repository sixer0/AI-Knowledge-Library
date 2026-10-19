#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""datum_diagram.py — kelas DIAGRAM/INFOGRAF paket datum-house-style v2.0.0
(kartu DHS-RB-04 t_446765d6; putusan GAP-09 D-1 jalur hibrida B+C).

STATUS PROVENSANS (WAJIB BACA)
  Ini REBUILD lini baru v2.0.0 dari spesifikasi tertulis, BUKAN restorasi
  `datum_diagram.py` v1.3/v1.8 Rev J. Vonis probe PUTUSAN-GAP-09: engine Rev J
  tidak ada di disk (0 hit pada lima root, 05-10). Setiap butir di bawah
  menunjuk sumbernya lewat penanda P1..P9 / T di bawah.

SUMBER SPESIFIKASI (path tetap, tidak disalin)
  P1  000-GSP-STD RevA 6.2 Tabel 6.1 — bidang minimum diagram-spec
      (Datum House Style Standard/DATUM_House_Style_Explained_000-GSP-STD-X-2026_RevA.docx.md baris 656-669)
  P2  000 RevA 6.3 Tabel 6.2 baris 676-688 — 9 keluarga, 7 mesin layout
  P3  000 RevA 6.3 Tabel 6.3 baris 690-703 — 10 bentuk simpul + notasinya
  P4  000 RevA 6.3 Tabel 6.4 baris 705-714 — 6 jenis konektor (pola garis dulu, warna kemudian)
  P5  000 RevA 6.3 Tabel 72 baris 716-721 — jangkar dikipas, lompatan silang,
      detur hambatan, kisi 10,667 x 4,7625 mm, satu lebar per tingkat, zona
      kepercayaan digambar lewat penutupan, satu aksen, <=5 nilai warna, legenda = baris kunci
  P6  000 RevA 6.4 baris 722-734 — apparatus page/figure, komentar
      DATUM-APPARATUS-REQUIRED (dilaporkan lint cek 36), render 300 dpi
  P7  000 RevA 6.5 baris 737-741 — sumber Mermaid dalam keluaran gagalkan cek 31
  P8  M01 docs/2026-10-04-datum-manual/measurement/01-instrumen-penegakan.md
      2.1 baris 92-105 — cek tahap build/file DATUM-24,26,27,28,29,30,32,33,34,35,37
  P9  000 RevA register temuan baris 1004/1015/1016 — E-08 (tulis mm, jangan px
      polos di root SVG), E-19 (implementasikan --estimate), E-20 (default
      apparatus = page, bukan figure)
  T   tokens.json v2.0.0 paket ini, dibaca lewat datumbind.tokens_path().
      PALET, NAMA WAJAH, SKALA TIPO, GRID, TANGGA GARIS DAN GLIF DIAMBIL DARI
      TOKEN — tidak ada satu pun hex/mm gaya yang dihardcode di berkas ini.

Yang TIDAK dikerjakan berkas ini (milik kartu saudara, disiplin D-3):
  datum_render.py (PNG 300 dpi) dan datumword.py (penempatan .docx) = DHS-RB-05;
  datum_lint.py 38 cek = DHS-RB-02. Berkas ini menjalankan cek Tahap-build dan
  melaporkan secara jujur daftar cek yang benar-benar dieksekusi (banner jujur).
"""
import argparse
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _import_datumbind():
    """Cari datumbind.py di direktori ini lalu di induknya (paket dipasang FLAT
    sesuai SKILL.md DHS-RB-01; pencarian induk memberi toleransi bila kelak
    dipindah ke scripts/). Resolver token tetap satu: datumbind.tokens_path()."""
    d = HERE
    for _hop in range(2):
        if os.path.exists(os.path.join(d, "datumbind.py")):
            if d not in sys.path:
                sys.path.insert(0, d)
            from datumbind import tokens_path
            return tokens_path
        d = os.path.dirname(d)
    raise ImportError("datumbind.py tidak ditemukan di %s maupun induknya" % HERE)


tokens_path = _import_datumbind()


class DiagramDefect(Exception):
    """Cacat spesifikasi/geometri yang memblokir rilis (setara BindDefect)."""


# ---------------------------------------------------------------- token (T)
def load_tokens():
    t = json.load(open(tokens_path(), encoding="utf-8"))
    need = ("colour", "type", "grid_mm", "rules_mm", "marks", "numerals")
    missing = [k for k in need if k not in t]
    if missing:
        raise DiagramDefect("tokens.json tidak lengkap, seksi hilang: %s" % ", ".join(missing))
    return t


TOK = load_tokens()
INTERIOR = TOK["colour"]["interior"]          # T colour.interior (palet dalam halaman)
WRAPPER = TOK["colour"]["wrapper"]
FACES = TOK["type"]["faces"]                  # T type.faces
SCALE = TOK["type"]["scale_pt"]               # T type.scale_pt (peran -> pt)
TRACK = TOK["type"]["tracking_em"]            # T type.tracking_em
GRID = TOK["grid_mm"]                         # T grid_mm
RULES = TOK["rules_mm"]                       # T rules_mm
MARKS = {k: v for k, v in TOK["marks"].items() if not k.startswith("_")}  # T marks
NUM = TOK["numerals"]                         # T numerals

PAPER = INTERIOR["paper"]                     # dasar putih/near-putih sejak Rev J (P5/P8 konteks)
INK_TEXT = "ink700"                           # peran baca (T type.roles.reading.colour)

# Turunan token — semua angka gaya hidup di tokens.json, bukan di sini.
# Kisi dihitung ulang dari induknya supaya kelipatan penuh tepat mengenai 128/166
# (token menyimpan 10,6667 yang bila dikali 12 menghasilkan 128,0004 dan memicu
# DATUM-37 palsu). Catatan token grid_mm._lattice_note menuliskan rumus ini.
_LX_TOK = float(GRID["horizontal_lattice"])
_LX_CALC = float(GRID["text_column"]) / 12.0
LATTICE_X = _LX_CALC if abs(_LX_CALC - _LX_TOK) < 1e-3 else _LX_TOK
_LY_TOK = float(GRID["vertical_lattice"])
_LY_CALC = float(TOK["type"]["baseline_pt"]) * 25.4 / 72.0   # pt->mm (fungsi pt2mm belum terdefinisi di sini)
LATTICE_Y = _LY_CALC if abs(_LY_CALC - _LY_TOK) < 1e-3 else _LY_TOK
ALLOWED_WIDTHS = (float(GRID["text_column"]), float(GRID["full_span"]))  # P1 width_mm
STROKE_FLOOR_MM = float(RULES["photocopy_floor"])     # P8 DATUM-27 <- T rules_mm.photocopy_floor
STROKE_PRIMARY = float(RULES["primary"])              # T rules_mm.primary
STROKE_HAIR = float(RULES["hair"])                    # T rules_mm.hair
BASELINE_PT = float(TOK["type"]["baseline_pt"])       # T type.baseline_pt

# Limit verbatim spesifikasi (bukan token gaya; P8 + P1). Dicatat per butir.
LIMITS = {
    "diagram_type_min_pt": 5.5,      # P8 DATUM-28 verbatim "Diagram type below 5,5 pt"
    "text_block_max_mm": 247.0,      # P8 DATUM-33 verbatim "Figure taller than the 247 mm text block"
    "max_colour_values": 5,          # P5 Tabel 72 + P8 DATUM-25 "<= 5 colour values in one figure"
    "max_accented_subjects": 1,      # P8 DATUM-26 "<= 1 accented subject in one figure"
    "hop_radius_mm": 0.9,            # geometri lokal: jari-jari lompatan silang (bukan token gaya)
    "_note": "Palet/grid/tipografi TIDAK ada di sini; hanya ambang cacat yang tertulis verbatim di 000 RevA Tabel 8.1.",
}

# Peran tipografi yang benar-benar dicetak engine — tiap satu diuji terhadap
# ambang DATUM-28 memakai ukuran dari token, bukan angka yang ditulis di sini.
DIAGRAM_ROLES = ("caption", "source_line", "table_header", "evidence_rail", "register_block")

# ------------------------------------------------- P2: keluarga & mesin layout
FAMILIES = {
    "layered":   {"draw_when": "komponen masuk strata: tingkat, zona, lapisan", "engine": "layout_layered"},
    "topology":  {"draw_when": "perangkat dan tautan jaringan; setiap tautan berlabel", "engine": "layout_layered"},
    "stack":     {"draw_when": "didaftarkan sebagai keluarga; tanpa layout/sampel sendiri", "engine": "layout_layered"},
    "flow":      {"draw_when": "prosedur berurutan dengan gerbang keputusan", "engine": "layout_flow"},
    "swimlane":  {"draw_when": "siapa yang bertindak adalah intinya; lajur = akuntabilitas", "engine": "layout_swimlane"},
    "sequence":  {"draw_when": "urutan pesan atas waktu; waktu memiliki sumbu vertikal", "engine": "layout_sequence"},
    "sld":       {"draw_when": "rantai daya/sinyul digantung dari rel bus", "engine": "layout_sld"},
    "rack":      {"draw_when": "elevasi rak; posisi U menanggung beban", "engine": "layout_rack"},
    "graph":     {"draw_when": "selain itu, ditempatkan lewat col dan row", "engine": "layout_graph"},
}

# ------------------------------------------------------- P3: bentuk simpul
SHAPES = {
    "box":           {"means": "komponen, langkah proses, peralatan", "notation": "universal", "radius": False},
    "stadium":       {"means": "awal atau akhir; satu-satunya bentuk yang boleh beradius", "notation": "ISO 5807", "radius": True},
    "diamond":       {"means": "keputusan; setiap keluaran berlabel", "notation": "ISO 5807", "radius": False},
    "parallelogram": {"means": "masukan atau keluaran", "notation": "ISO 5807", "radius": False},
    "cylinder":      {"means": "data tersimpan, arsip", "notation": "universal", "radius": False},
    "hexagon":       {"means": "persiapan, gerbang", "notation": "ISO 5807, BPMN", "radius": False},
    "doubled":       {"means": "subsistem dengan struktur lanjutan", "notation": "UML component", "radius": False},
    "shadowed":      {"means": "entitas eksternal di luar batas", "notation": "DFD Gane-Sarson", "radius": False},
    "circle":        {"means": "persimpangan, penyambung luar-halaman", "notation": "universal", "radius": False},
    "bus":           {"means": "rel bus atau backplane, garis berat", "notation": "IEC 60617", "radius": False},
}

# ------------------------------------------- P4: jenis konektor (nama token!)
EDGE_KINDS = {
    "data":    {"pattern": "solid", "colour": "ink900", "head": "solid", "iso": "01.1",
                "use": "substansi yang bergerak melalui sistem"},
    "control": {"pattern": "dashed", "colour": "ink700", "head": "open", "iso": "02.1",
                "use": "perintah, pemicu, orkestrasi"},
    "sync":    {"pattern": "dotted", "colour": "ink400", "head": "open", "iso": "-",
                "use": "replikasi, mirroring, heartbeat"},
    "accent":  {"pattern": "solid", "colour": "signal", "head": "solid", "iso": "01.1",
                "use": "satu jalur yang tidak boleh dilewatkan pembaca"},
    "alert":   {"pattern": "longdash", "colour": "alert", "head": "open", "iso": "-",
                "use": "kegagalan, penolakan, jalur pengecualian"},
    "verify":  {"pattern": "dashdot", "colour": "verd", "head": "open", "iso": "04.1",
                "use": "uji integritas, atestasi, audit"},
}

DASH_PATTERNS = {  # pola garis ISO 128-2 dalam mm (geometri, bukan palet)
    "solid": None, "dashed": "3.2,1.6", "dotted": "0.2,1.1",
    "longdash": "7.1,1.6", "dashdot": "7.1,1.6,0.2,1.6",
}

SPEC_FIELDS = {  # P1 Tabel 6.1 — bidang minimum diagram-spec
    "family": "salah satu keluarga Tabel 6.2; dipilih PRISMA, bukan DATUM",
    "id": "nomor berawalan bab",
    "title": "satu kalimat berakhir titik",
    "classification": "diputuskan bersama dokumen induk, tidak sendiri",
    "nodes[]": "id, label, class (tier/lane/col/row), sub, mark, tag",
    "edges[]": "from, to, kind dan label — keempatnya wajib",
    "legend[]": "baris kunci saat glif rumah muncul; catatan khusus",
    "notes[]": "carve-out dan konvensi",
    "sources[]": "minimal satu dokumen dan klausul tempat gambar dibangun",
    "labels_verified": "false berarti draft: render dan tinjau, jangan kirim",
    "width_mm": "128 atau 166, jangan di antaranya",
    "apparatus": "page untuk gambar di .docx/.pptx, figure untuk SVG berdiri sendiri",
}


# ------------------------------------------------------------- util geometri
def pt2mm(pt):
    return float(pt) * 25.4 / 72.0


def snap(v, unit):
    return round(float(v) / unit) * unit


def snap_floor(v, unit):
    """Kebulatkan ke bawah pada kisi — dipakai untuk lebar agar tidak pernah
    melewati tepi lembar akibat pembulatan naik (P8 DATUM-37)."""
    n = math.floor(float(v) / unit + 1e-9)
    return max(n, 0) * unit


def snap_ceil(v, unit):
    """Kebulatkan ke ATAS pada kisi — dipakai posisi kiri kolom pada penataan
    ulang anti-tumpuan (BUG-DIAG-ROWPACK) agar celah antar simpul tidak pernah
    menyusut di bawah kebutuhan oleh pembulatan (kebalikan snap_floor)."""
    n = math.ceil(float(v) / unit - 1e-9)
    return max(n, 0) * unit


def fmt_num(value, dec=0):
    """Konvensi angka DATUM dari token numerals (T numerals): ribu '.', desimal ','."""
    s = ("%.*f" % (int(dec), float(value)))
    ip, _, dp = s.partition(".")
    neg = ip.startswith("-")
    ip = ip.lstrip("-")
    ip = ".".join(re.findall(r"\d{1,3}", ip[::-1]))[::-1]  # ribuan (P: T numerals.thousands)
    out = ip + (NUM["decimal"] + dp if dp else "")
    return ("-" if neg else "") + out


def role(name):
    if name not in SCALE:
        raise DiagramDefect("peran tipografi '%s' tidak ada di tokens.json type.scale_pt" % name)
    return SCALE[name]


def face_of(role_name):
    r = role(role_name)
    key = r.get("face", "condensed")
    if key not in FACES:
        raise DiagramDefect("wajah '%s' tidak ada di tokens.json type.faces" % key)
    return FACES[key]


def colour_of(token_name):
    """Semua warna lewat nama token interior; hex tidak pernah ditulis di sini."""
    if token_name not in INTERIOR:
        raise DiagramDefect("token warna '%s' tidak ada di tokens.json colour.interior" % token_name)
    return INTERIOR[token_name]


def est_text_mm(text, role_name):
    """Perkiraan lebar teks (mm) dari ukuran peran token; dipakai untuk lebar simpul."""
    r = role(role_name)
    return len(str(text)) * pt2mm(r["size"]) * 0.56


# --------------------------------------------------------------- baca spek
MERMAID_TELL = ("```mermaid", "graph TD", "graph LR", "flowchart TD", "flowchart LR",
                "sequenceDiagram", "stateDiagram")  # P7: sumber Mermaid = cek 31


def load_spec(path):
    if path.lower().endswith((".mmd", ".mermaid")):
        raise DiagramDefect("DATUM-31: sumber Mermaid (%s) dilarang dalam keluaran (P7)" % path)
    raw = open(path, encoding="utf-8").read()
    low = raw.lower()
    for tell in MERMAID_TELL:
        if tell in low:
            raise DiagramDefect("DATUM-31: sumber Mermaid terdeteksi ('%s') — gambar dibangun dari diagram-spec.json, bukan Mermaid (P7)" % tell)
    try:
        spec = json.loads(raw)
    except ValueError as ex:
        raise DiagramDefect("diagram-spec bukan JSON valid: %s" % ex)
    return mirror_source(spec)


def mirror_source(spec):
    """P1/Tabel 6.1 SOURCE: mesin membaca `source`, bukan `sources[]`; spesimen
    mencerminkan satu ke yang lain (baris 669)."""
    if "source" in spec and "sources" not in spec:
        spec["sources"] = spec["source"] if isinstance(spec["source"], list) else [spec["source"]]
    elif "sources" in spec and "source" not in spec:
        spec["source"] = spec["sources"]
    return spec


# ------------------------------------------------------- validasi spesifikasi
def validate_spec(spec):
    """Cek kontrak P1 + cek tahap-build P8 yang bisa diputuskan dari spek saja.
    Mengembalikan daftar cek yang benar-benar dieksekusi."""
    ran = []

    fam = spec.get("family")
    if fam not in FAMILIES:
        raise DiagramDefect("family '%s' bukan salah satu dari %s (P1/P2)" % (fam, "/".join(sorted(FAMILIES))))
    ran.append("P1-family")

    fid = str(spec.get("id", ""))
    if not re.search(r"\d+\.\d+", fid):
        raise DiagramDefect("id '%s' bukan nomor berawalan bab seperti 4.2 (P1)" % fid)
    ran.append("P1-id")

    title = str(spec.get("title", "")).strip()
    if not title.endswith("."):
        raise DiagramDefect("title harus satu kalimat berakhir titik (P1): '%s'" % title)
    ran.append("P1-title")

    if not str(spec.get("classification", "")).strip():
        raise DiagramDefect("classification wajib diputuskan bersama dokumen induk (P1)")
    ran.append("P1-classification")

    w = float(spec.get("width_mm", 0))
    if not any(abs(w - a) < 1e-6 for a in ALLOWED_WIDTHS):
        raise DiagramDefect("width_mm %s harus salah satu dari %s (P1: 128 atau 166, jangan di antaranya)"
                            % (w, [int(a) for a in ALLOWED_WIDTHS]))
    ran.append("P1-width_mm")

    apparatus = spec.get("apparatus", "page")  # P9 E-20: default page, bukan figure
    if apparatus not in ("page", "figure"):
        raise DiagramDefect("apparatus '%s' harus page atau figure (P1/P9-E-20)" % apparatus)
    ran.append("P1-apparatus")

    srcs = spec.get("sources") or []
    if not isinstance(srcs, list) or not srcs:
        raise DiagramDefect("sumber wajib: minimal satu dokumen+klausul (P1 sources[])")
    ran.append("P1-sources")

    nodes = spec.get("nodes") or []
    if not nodes:
        raise DiagramDefect("nodes[] kosong — gambar tanpa komponen nyata melanggar MAT-09 (P8)")
    ids = set()
    notations = set()
    marks_used = set()
    for n in nodes:
        nid = n.get("id")
        if not nid or not str(n.get("label", "")).strip():
            raise DiagramDefect("simpul wajib id dan label (P1 nodes[]): %r" % n)
        if nid in ids:
            raise DiagramDefect("id simpul ganda: %s" % nid)
        ids.add(nid)
        shp = n.get("shape", "box")
        if shp not in SHAPES:
            raise DiagramDefect("bentuk '%s' bukan salah satu dari %s (P3)" % (shp, "/".join(sorted(SHAPES))))
        if not isinstance(n.get("class"), dict):
            raise DiagramDefect("simpul %s wajib class (tier/lane/col/row) (P1)" % nid)
        notations.add(SHAPES[shp]["notation"])
        mk = n.get("mark")
        if mk is not None:
            if mk not in MARKS:
                raise DiagramDefect("glif asal '%s' bukan glif rumah %s (T marks)" % (mk, "/".join(sorted(MARKS))))
            marks_used.add(mk)
    ran.append("P1-nodes+P3-shapes")

    # P8 DATUM-35: satu dialek simbol per gambar (universal boleh berdampingan).
    dialects = {t for t in notations if t != "universal"}
    if len(dialects) > 1:
        raise DiagramDefect("DATUM-35: lebih dari satu dialek simbol dalam satu gambar (%s) — satu notasi per gambar (P3/P5)"
                            % ", ".join(sorted(dialects)))
    ran.append("DATUM-35")

    edges = spec.get("edges") or []
    accented = 0
    for e in edges:
        for key in ("from", "to", "kind", "label"):
            if key not in e or e[key] in (None, ""):
                raise DiagramDefect("DATUM-24: konektor wajib keempat bidang from/to/kind/label (P1/P8): %r" % e)
        if e["from"] not in ids or e["to"] not in ids:
            raise DiagramDefect("konektor merujuk simpul tak dikenal: %s->%s" % (e["from"], e["to"]))
        if e["kind"] not in EDGE_KINDS:
            raise DiagramDefect("jenis konektor '%s' bukan salah satu dari %s (P4)" % (e["kind"], "/".join(sorted(EDGE_KINDS))))
        if e["kind"] == "accent":
            accented += 1
    if accented > int(LIMITS["max_accented_subjects"]):
        raise DiagramDefect("DATUM-26: %s subjek beraksen, maksimum %s per gambar (P5/P8)"
                            % (accented, LIMITS["max_accented_subjects"]))
    ran.append("DATUM-24")
    ran.append("DATUM-26")

    # P8 DATUM-34: glif rumah wajib baris kunci terbit.
    if marks_used:
        legend_text = " ".join(str(x) for x in (spec.get("legend") or []))
        missing = [m for m in sorted(marks_used) if m not in legend_text and MARKS[m] not in legend_text]
        if missing:
            raise DiagramDefect("DATUM-34: glif rumah %s dipakai tanpa baris kunci terbit (P5/P8)" % ", ".join(missing))
    ran.append("DATUM-34")

    # P8 MAT-09 sebagian: bentuk keputusan wajib keluaran berlabel (P3 diamond).
    for n in nodes:
        if n.get("shape") == "diamond":
            outs = [e for e in edges if e["from"] == n["id"]]
            if not outs:
                raise DiagramDefect("keputusan '%s' tanpa keluaran berlabel (P3: every exit labelled)" % n["id"])
    ran.append("P3-diamond-exits")
    return ran


# ------------------------------------------------------------- mesin layout
class Sheet(object):
    """Permukaan gambar dalam mm (1 satuan SVG = 1 mm, pelajaran E-08)."""

    def __init__(self, width_mm):
        self.W = float(width_mm)
        self.nodes = {}
        self.zones = []
        self.lanes = []
        self.lifelines = []
        self.bus = None
        self.top = LATTICE_Y * 2
        self.foot = 0.0   # BUG-DATUM-DIAGRAM: cadangan kaki apparatus (mm), diisi build_svg

    def height(self):
        ys = [n["y"] + n["h"] for n in self.values_list()]
        if self.lanes:
            ys += [l["y"] + l["h"] for l in self.lanes]
        if getattr(self, "msg_end", None):
            ys.append(self.msg_end)
        return snap(max(ys) if ys else self.top, LATTICE_Y) + LATTICE_Y * 2 + self.foot

    def values_list(self):
        return list(self.nodes.values())


def _foot_lines(spec):
    """BUG-DATUM-DIAGRAM (kartu t_ef103378, laporan FIGUR-1 t_559f107b): berapa
    baris teks kaki apparatus yang akan dicetak build_svg di bawah gambar.
    figure = caption + KEY (bila legend) + SUMBER; page = KEY saja bila legend."""
    if spec.get("apparatus", "page") == "figure":
        return 2 + (1 if spec.get("legend") else 0)
    return 1 if spec.get("legend") else 0


def _foot_reserve_mm(spec):
    """Tinggi yang dicadangkan Sheet.height() untuk blok kaki apparatus.
    Sebelum tambal ini kaki digambar pada H-2*LATTICE_Y tanpa reserve sehingga
    garis dasarnya mendarat di dalam/di atas simpul baris terakhir."""
    return _foot_lines(spec) * LATTICE_Y


def _node_size(n, sheet, tier_nodes=None):
    """Lebar: kelipatan kisi; satu lebar per tingkat (P5). Tinggi: kelipatan baseline."""
    label_w = est_text_mm(n.get("label", ""), "caption")
    sub_w = est_text_mm(n.get("sub", ""), "source_line") if n.get("sub") else 0.0
    need = max(label_w, sub_w) + pt2mm(role("caption")["size"]) * 1.2
    w = snap(need, LATTICE_X)
    if tier_nodes:
        w = max(snap(max(est_text_mm(t.get("label", ""), "caption") +
                          (est_text_mm(t.get("sub", ""), "source_line") if t.get("sub") else 0)
                          + pt2mm(role("caption")["size"]) * 1.2 for t in tier_nodes), LATTICE_X), LATTICE_X * 3)
    w = max(w, LATTICE_X * 3)
    units = 3
    if n.get("sub"):
        units += 1
    if n.get("tag"):
        units += 1
    h = snap(units * LATTICE_Y * 2, LATTICE_Y)
    return w, h


def layout_layered(spec, sheet):
    """Tingkat vertikal; satu lebar per tingkat (P5). Dipakai layered/topology/stack."""
    tiers = []
    index = {}
    for n in spec["nodes"]:
        t = str(n.get("class", {}).get("tier", n.get("class", {}).get("row", 0)))
        if t not in index:
            index[t] = len(tiers)
            tiers.append((t, []))
        tiers[index[t]][1].append(n)
    y = sheet.top
    for _, group in tiers:
        m = len(group)
        gap = LATTICE_X
        w = snap((sheet.W - (m - 1) * gap) / float(m), LATTICE_X)
        w = max(min(w, LATTICE_X * 10), LATTICE_X * 3)
        hs = []
        for n in group:
            _, h = _node_size(n, sheet, tier_nodes=group)
            hs.append(h)
        hmax = max(hs)
        total = m * w + (m - 1) * gap
        x = snap(max(0.0, (sheet.W - total) / 2.0), LATTICE_X)
        for i, n in enumerate(group):
            sheet.nodes[n["id"]] = {"id": n["id"], "spec": n, "x": x + i * (w + gap), "y": y, "w": w, "h": hmax,
                                    "tier": str(n.get("class", {}).get("tier", ""))}
        y = y + hmax + snap(BASELINE_PT * 2, LATTICE_Y)
    return sheet


def layout_flow(spec, sheet):
    """Rantai berurutan; simpul melebar untuk keputusan (P2 flow).

    ENH-D (E-30, register 000 RevA): kunci opsional spec['per_row'] membungkus
    rantai jadi beberapa baris (baris-first, urutan baca kiri-kanan lalu turun),
    sehingga flow panjang tidak melewati halaman A4 (DATUM-37). Tanpa per_row
    perilaku lama tetap: satu kolom vertikal terpusat."""
    per_row = spec.get("per_row")
    if per_row and int(per_row) > 0:
        gap = LATTICE_X
        # per_row adalah ATASAN: jumlah kolom dibatasi yang benar-benar muat
        # dengan lebar minimum 3 kisi (uji dua arah 08-10: 5x32+4x10,7 > 166 mm)
        k_max = int((sheet.W + gap) // (LATTICE_X * 3 + gap))
        k = max(1, min(int(per_row), k_max))
        rows = [spec["nodes"][i:i + k] for i in range(0, len(spec["nodes"]), k)]
        y = sheet.top
        for group in rows:
            m = len(group)
            w = snap((sheet.W - (m - 1) * gap) / float(m), LATTICE_X)
            # snap bisa membulat ke ATAS dan membuat total baris meluap lembar
            # (DATUM-37 menangkap ini saat uji dua arah 08-10): susut sampai muat.
            while m * w + (m - 1) * gap > sheet.W and w > LATTICE_X * 3:
                w -= LATTICE_X
            w = max(w, LATTICE_X * 3)
            hs = []
            for n in group:
                _, h = _node_size(n, sheet, tier_nodes=group)
                if n.get("shape") == "diamond":
                    h = snap(h * 1.25, LATTICE_Y)
                hs.append(h)
            hmax = max(hs)
            total = m * w + (m - 1) * gap
            x = snap(max(0.0, (sheet.W - total) / 2.0), LATTICE_X)
            for i, n in enumerate(group):
                nh = hs[i]
                nx = x + i * (w + gap)  # mode bungkus: kolom tetap, belah ketupat
                ww = min(w, sheet.W - nx)  # tidak boleh melebar 1,6x melewati lembar
                sheet.nodes[n["id"]] = {"id": n["id"], "spec": n, "x": nx,
                                        "y": y, "w": ww, "h": nh}
            y += hmax + snap(BASELINE_PT * 2, LATTICE_Y)
        return sheet
    w = snap(sheet.W * 0.42, LATTICE_X)
    y = sheet.top
    for n in spec["nodes"]:
        nw, nh = _node_size(n, sheet)
        if n.get("shape") == "diamond":
            nw = snap(nw * 1.6, LATTICE_X)
        sheet.nodes[n["id"]] = {"id": n["id"], "spec": n, "x": snap((sheet.W - nw) / 2.0, LATTICE_X),
                                "y": y, "w": nw, "h": nh}
        y += nh + snap(BASELINE_PT * 2, LATTICE_Y)
    return sheet


def layout_swimlane(spec, sheet):
    """Lajur = akuntabilitas (P2 swimlane)."""
    lanes = []
    li = {}
    for n in spec["nodes"]:
        ln = str(n.get("class", {}).get("lane", "tanpa lajur"))
        if ln not in li:
            li[ln] = len(lanes)
            lanes.append(ln)
        n["_lane_i"] = li[ln]
    gutter = snap(LATTICE_X * 3, LATTICE_X)
    per_lane = {ln: [] for ln in lanes}
    for n in spec["nodes"]:
        per_lane[lanes[n["_lane_i"]]].append(n)
    y = sheet.top
    for ln in lanes:
        group = per_lane[ln]
        hs = [_node_size(n, sheet)[1] for n in group]
        lh = max(hs) if hs else snap(3 * LATTICE_Y * 2, LATTICE_Y)
        x = gutter + LATTICE_X
        for n in group:
            nw, nh = _node_size(n, sheet)
            sheet.nodes[n["id"]] = {"id": n["id"], "spec": n, "x": x, "y": y + (lh - nh) / 2.0, "w": nw, "h": nh}
            x += nw + LATTICE_X
        sheet.lanes.append({"name": ln, "y": y, "h": lh})
        y += lh + snap(BASELINE_PT, LATTICE_Y)
    sheet.gutter_w = gutter
    return sheet


def layout_sequence(spec, sheet):
    """Waktu memiliki sumbu vertikal (P2 sequence): aktor = kolom, pesan = baris waktu."""
    actors = spec["nodes"]
    m = max(1, len(actors))
    colw = snap(sheet.W / float(m), LATTICE_X)
    head_h = max(_node_size(n, sheet)[1] for n in actors)
    for i, n in enumerate(actors):
        nw, nh = _node_size(n, sheet)
        nw = min(nw, colw - LATTICE_X)
        sheet.nodes[n["id"]] = {"id": n["id"], "spec": n, "x": snap(i * colw + (colw - nw) / 2.0, LATTICE_X),
                                "y": sheet.top, "w": nw, "h": head_h}
        sheet.lifelines.append({"x": snap(i * colw + colw / 2.0, LATTICE_X), "top": sheet.top + head_h})
    sheet.msg_y = sheet.top + head_h + snap(BASELINE_PT * 2, LATTICE_Y)
    sheet.msg_step = snap(BASELINE_PT * 3, LATTICE_Y)
    return sheet


def layout_sld(spec, sheet):
    """Rel bus di atas, cabang menggantung di bawahnya (P2 sld; P9 E-17)."""
    buses = [n for n in spec["nodes"] if n.get("shape") == "bus"]
    if not buses:
        raise DiagramDefect("E-17: keluarga sld butuh rel bus sebelum engine dapat merute cabang tanpa konektor menggantung (P6/register E-17)")
    others = [n for n in spec["nodes"] if n.get("shape") != "bus"]
    b = buses[0]
    bh = snap(2 * LATTICE_Y, LATTICE_Y)
    sheet.nodes[b["id"]] = {"id": b["id"], "spec": b, "x": 0.0, "y": sheet.top, "w": sheet.W, "h": bh}
    sheet.bus = {"y": sheet.top + bh / 2.0, "id": b["id"]}
    m = max(1, len(others))
    gap = LATTICE_X
    w = snap((sheet.W - (m - 1) * gap) / float(m), LATTICE_X)
    w = max(min(w, LATTICE_X * 8), LATTICE_X * 3)
    y = sheet.top + bh + snap(BASELINE_PT * 2, LATTICE_Y)
    for i, n in enumerate(others):
        nw, nh = _node_size(n, sheet)
        nw = min(nw, w)
        sheet.nodes[n["id"]] = {"id": n["id"], "spec": n,
                                "x": snap(i * (w + gap) + (w - nw) / 2.0, LATTICE_X), "y": y, "w": nw, "h": nh}
    return sheet


def layout_rack(spec, sheet):
    """Elevasi rak: posisi U menanggung beban (P2 rack)."""
    colw = snap(LATTICE_X * 8, LATTICE_X)
    x = snap((sheet.W - colw) / 2.0, LATTICE_X)
    items = sorted(spec["nodes"], key=lambda n: int(n.get("class", {}).get("row", 0)))
    y = sheet.top
    for n in items:
        u = int(n.get("u", 1))
        nh = snap(u * LATTICE_Y * 2, LATTICE_Y)
        sheet.nodes[n["id"]] = {"id": n["id"], "spec": n, "x": x, "y": y, "w": colw, "h": nh}
        y += nh
    sheet.rack_x = x
    return sheet


def _graph_min_width(n):
    """Lebar minimum simpul graph: kebutuhan teks mentah (label/sub + rem-rem
    caption) atau 3 kisi, mana yang lebih besar. Batas bawah rapat untuk
    penataan ulang anti-tumpuan (BUG-DIAG-ROWPACK): di bawah ini teks pasti
    meluap kotak, jadi keadaan tanpa kandidat = benar-benar tak muat."""
    label_w = est_text_mm(n.get("label", ""), "caption")
    sub_w = est_text_mm(n.get("sub", ""), "source_line") if n.get("sub") else 0.0
    return max(max(label_w, sub_w) + pt2mm(role("caption")["size"]) * 1.2, LATTICE_X * 3)


def _graph_column_pos(spec, sheet, cols, ests):
    """BUG-DIAG-ROWPACK (kartu t_787b26a9): menutup sisa-known yang sengaja
    ditinggalkan t_ef103378. Pitch seragam lama hanya diuji terhadap TEPI KANAN
    (p_cap dari lebar kolom terakhir), sehingga dua kolom bertetangga yang
    berbagi SATU baris bisa saling menumpuk di tengah kanvas:
    x(kol_i) + w(simpul_i) > x(kol_i+1). Terukur pada figuran RAFIF-MF-1009:
    5 tumpuan nyata pada 3 spek graph (G3.1 satu, G7.3 tiga, G11.2 satu) dengan
    celah tembus 10,67..21,33 mm; simpul terpotong clamp DATUM-37 build_svg dan
    konektor antar simpul kehilangan titik jangkar sah.

    Mekanik deterministik (angka hanya dari kisi token + estimasi teks):
      (1) posisi seragam lama -> uji tumpuan PER BARIS; bersih = KEMBALI PERSIS
          posisi lama (spek sehat tidak berubah geometri: nol regresi keluaran);
      (2) ada tumpuan: relaksasi kiri->kanan, tiap kolom didorong ke kanan sampai
          celah terhadap simpul se-barisnya >= 1 kisi (snap_ceil, monotik naik);
      (3) hasil dorong melewati tepi kanan: rapatkan simpul TERLEBAR yang ikut
          baris bermasalah satu kisi per putar (snap_floor, tidak pernah di bawah
          kebutuhan teks mentah) lalu relaksasi ulang — 'rapatkan sampai muat';
      (4) masih tidak muat padahal semua simpul sudah di bawah kebutuhan teks:
          DITOLAK dengan cacat DATUM-37/ROWPACK bernama, bukan digambar
          bertumpukan (preseden t_ef103378: tolak hanya keadaan tak muat);
      (5) blok hasil dorong dipusatkan sama seperti jalur lama (geser seragam,
          celah relatif tidak berubah)."""
    gap = LATTICE_X
    last_w = max(ests[n["id"]][0] for n in spec["nodes"]
                 if int(n.get("class", {}).get("col", 0)) == cols[-1])
    p_default = LATTICE_X * 4
    p_cap = (sheet.W - last_w) / float(len(cols) - 1)
    p = p_default if p_default <= p_cap + 1e-9 else snap_floor(p_cap, LATTICE_X)
    if p < LATTICE_X * 3 - 1e-9:
        raise DiagramDefect("DATUM-37: %d kolom graph tidak muat di %.1f mm "
                            "(pitch tersedia %.2f mm di bawah lebar minimum simpul %.2f mm)"
                            " — rapatkan col/row atau persempit label (P8, layout_graph)"
                            % (len(cols), sheet.W, p_cap, LATTICE_X * 3))
    total = (len(cols) - 1) * p + last_w
    x0 = snap_floor(max(0.0, (sheet.W - total) / 2.0), LATTICE_X)
    pos = {c: x0 + i * p for i, c in enumerate(cols)}

    # indeks deterministik: kolom tiap simpul + urutan simpul per baris
    col_of, rows = {}, {}
    for n in spec["nodes"]:
        c = int(n.get("class", {}).get("col", 0))
        r = int(n.get("class", {}).get("row", 0))
        col_of[n["id"]] = c
        rows.setdefault(r, []).append(n["id"])
    for r in rows:
        rows[r].sort(key=lambda nid: (col_of[nid], nid))

    def collide(x):
        hits = []
        for r in sorted(rows):
            ids = rows[r]
            for a, b in zip(ids, ids[1:]):
                ov = x[col_of[a]] + ests[a][0] - x[col_of[b]]
                if ov > 1e-6:
                    hits.append((r, a, b, round(ov, 2)))
        return hits

    hits = collide(pos)
    if not hits:
        return pos                                   # bersih: geometri lama utuh

    mins = {n["id"]: _graph_min_width(n) for n in spec["nodes"]}
    involved = set()
    for r, a, b, ov in hits:
        involved.update((a, b))

    # Ruang tambahan yang sah: saat ada tumpuan, blok boleh dipindah ke MARGIN
    # KIRI (pusat hanya kosmetik; memakai lebar kanvas penuh lebih benar daripada
    # memotong kotak simpul). Relaksasi tetap monotik kanan dari basis mana pun.
    left_base = {c: snap(max(0.0, pos[c] - x0), LATTICE_X) for c in cols}

    def relax(base_pos, g):
        """Dorong kolom ke kanan sampai tiap pasangan se-baris ber-celah >= g."""
        x = dict(base_pos)
        for _ in range(len(cols) * max(1, len(rows)) + 4):
            moved = False
            for c in cols[1:]:
                need = None
                for r in rows.values():
                    for a, b in zip(r, r[1:]):
                        if col_of[b] != c:
                            continue
                        req = x[col_of[a]] + ests[a][0] + g
                        need = req if need is None else max(need, req)
                if need is not None and need > x[c] + 1e-6:
                    x[c] = snap_ceil(need, LATTICE_X)
                    moved = True
            if not moved:
                break
        return x

    def overflow(x):
        return [nid for nid in ests if x[col_of[nid]] + ests[nid][0] > sheet.W + 1e-6]

    def shrink_target(nid):
        """Lebar baru satu kisi lebih sempit: tetap kelipatan kisi, tidak pernah
        di bawah kebutuhan teks mentah (snap_ceil agar tetap dikunci kisi), dan
        selalu benar-benar lebih kecil dari lebar sekarang."""
        floor_w = snap_ceil(mins[nid], LATTICE_X)
        return max(floor_w, snap_floor(ests[nid][0] - LATTICE_X, LATTICE_X))

    # Tangga celah (deterministik, turun dari 1 kisi ke nol): 'celah 0' berarti
    # dua simpul se-baris BERSEBELAHAN tepat pada tepi (bukan tumpuan) dan tetap
    # jauh lebih baik daripada clamp senyap build_svg yang memotong kotak.
    # Menolak hanya dilakukan setelah semua anak tangga habis (preseden
    # t_ef103378: 'rapatkan sampai muat, tolak hanya keadaan benar-benar tak muat').
    # Tangga strategi deterministik (basis posisi x celah minimum), dari yang
    # paling longgar ke paling ketat; tiap anak tangga mencoba (a) relaksasi utuh,
    # (b) rapatkan simpul yang masih di ATAS kebutuhan teks mentah, lalu (c) baru
    # rapatkan sampai persis di kebutuhan teks sebagai daya-ikat terakhir. Lebar
    # tidak pernah turun di bawah kebutuhan teks lewat jalur ini: kalau tetap
    # tidak muat, gambar DITOLAK bernama, bukan di-clamp senyap build_svg.
    def solve(basis_pos, g):
        x = relax(basis_pos, g)
        r = 0
        for strict in (False, True):
            while overflow(x):
                def room(nid):
                    tgt = shrink_target(nid)
                    if tgt >= ests[nid][0] - 1e-9:
                        return False
                    return strict or ests[nid][0] > snap_ceil(mins[nid], LATTICE_X) + 1e-9
                cand = sorted((nid for nid in ests if room(nid)),
                              key=lambda nid: (-ests[nid][0], nid))
                if not cand or r > 600:
                    break
                victim = cand[0]
                ests[victim] = (shrink_target(victim), ests[victim][1])
                involved.add(victim)
                r += 1
                x = relax(basis_pos, g)
            if not overflow(x):
                return x, r
        return None, r

    ladder = ((pos, LATTICE_X, "center+gap1"), (pos, 0.0, "center+gap0"),
              (left_base, LATTICE_X, "left+gap1"), (left_base, 0.0, "left+gap0"))
    x = None
    strategy = ""
    rounds = 0
    for basis, g, tag in ladder:
        trial, r = solve(basis, g)
        rounds += r
        if trial is not None:
            x, strategy = trial, tag
            break

    if x is None:
        worst = max((sum(ests[a][0] for a in ids) + gap * (len(ids) - 1)
                     for ids in rows.values() if len(ids) > 1), default=0.0)
        raise DiagramDefect("DATUM-37/ROWPACK: %d kolom graph berbagi baris tidak muat di "
                            "%.1f mm setelah dorong-kolom dan rapat-lebar (baris terlapar butuh "
                            "%.2f mm) — beri row berbeda atau persempit label/sub (P8, layout_graph)"
                            % (len(cols), sheet.W, worst))

    # pusatkan blok (geser seragam: celah relatif tetap, tepi kanan tetap aman)
    used = max(x[c] + max([ests[n["id"]][0] for n in spec["nodes"] if col_of[n["id"]] == c]
                          or [0.0]) for c in cols)
    shift = snap_floor(max(0.0, (sheet.W - used) / 2.0), LATTICE_X)
    if shift > 1e-9:
        trial = {c: snap(x[c] + shift, LATTICE_X) for c in cols}
        if not overflow(trial) and not collide(trial):
            x = trial
    sheet.rowpack = {"baseline_hits": len(hits), "rounds": rounds, "strategy": strategy,
                     "pitch_mm": round(x[cols[1]] - x[cols[0]], 2) if len(cols) > 1 else 0.0}
    return x


def layout_graph(spec, sheet):
    """Ditempatkan lewat col dan row pada kisi (P2 graph, P5 kisi).

    BUG-DATUM-DIAGRAM (kartu t_ef103378, laporan FIGUR-1 t_559f107b): pitch
    tetap col*4*LATTICE_X tidak menguji x+w <= sheet.W -> simpul kolom kanan
    melebar keluar kanvas lalu dipersempit DIAM-DIAM oleh clamp DATUM-37 di
    build_svg (teks meluap kotaknya). Sekarang `col` diperlakukan sebagai slot
    berurutan dari kolom yang HADIR: pitch 4*LX selama muat; bila tidak,
    dirapatkan sampai muat tepi kanan dan hasilnya dipusatkan; hanya bila
    tetap tidak muat (pitch di bawah lebar minimum simpul 3*LX) gambar
    DITOLAK dengan cacat DATUM-37 bernama, bukan di-clamp senyap.

    BUG-DIAG-ROWPACK (kartu t_787b26a9): sisa-known yang tadinya ditinggalkan
    tiket ini — tumpuan antar simpul dalam SATU baris ketika dua kolom
    bertetangga berbagi baris (x_i + w_i > x_i+1; terukur 5 kejadian pada
    figuran RAFIF-MF-1009: G3.1, G7.3 x3, G11.2) — kini ditangani
    `_graph_column_pos`: uji tumpuan per baris, relaksasi kolom ke kanan,
    rapatkan-lebar bertingkat, tolak bernama bila sungguh tak muat. Spek yang
    sudah bersih kembali ke posisi rumus lama PERSIS (nol regresi geometri).
    Kolom tunggal atau kolom yang lebarnya sendiri melewati lembar mengikuti
    jalur lama (clamp build_svg; preseden basal merah DATUM-32 dinding dan
    DATUM-37 col=20)."""
    ests = {}
    cols = []
    for n in spec["nodes"]:
        c = int(n.get("class", {}).get("col", 0))
        if c not in cols:
            cols.append(c)
        ests[n["id"]] = _node_size(n, sheet)
    cols.sort()
    maxw = {}
    for n in spec["nodes"]:
        c = int(n.get("class", {}).get("col", 0))
        maxw[c] = max(maxw.get(c, 0.0), ests[n["id"]][0])
    # jalur lama dipertahankan bila: satu kolom, ada kolom yang anchor lamanya
    # sudah jauh di luar lembar (basal merah DATUM-37), atau ada kolom yang
    # lebarnya sendiri melewati lembar (basal merah DATUM-32 dinding).
    adaptive = (len(cols) > 1
                and all(w <= sheet.W + 1e-6 for w in maxw.values())
                and all(c * LATTICE_X * 4 < sheet.W - 1e-6 for c in cols))
    if adaptive:
        pos = _graph_column_pos(spec, sheet, cols, ests)
    else:
        pos = {c: c * LATTICE_X * 4 for c in cols}
    for n in spec["nodes"]:
        c = int(n.get("class", {}).get("col", 0))
        r = int(n.get("class", {}).get("row", 0))
        nw, nh = ests[n["id"]]
        x = snap(pos[c], LATTICE_X)
        y = snap(sheet.top + r * LATTICE_Y * 8, LATTICE_Y)
        if adaptive and x + nw > sheet.W + 1e-6:
            raise DiagramDefect("DATUM-37: simpul %s keluar lebar lembar (%.1f..%.1f dari %.1f mm) "
                                "setelah penempatan kolom (P8, layout_graph)"
                                % (n["id"], x, x + nw, sheet.W))
        sheet.nodes[n["id"]] = {"id": n["id"], "spec": n, "x": x, "y": y, "w": nw, "h": nh}
    return sheet


LAYOUTS = {name: meta["engine"] for name, meta in FAMILIES.items()}  # P2: 9 nama, 7 mesin


# ------------------------------------------------------------------ rute
def _side_of(a, b):
    acx, acy = a["x"] + a["w"] / 2.0, a["y"] + a["h"] / 2.0
    bcx, bcy = b["x"] + b["w"] / 2.0, b["y"] + b["h"] / 2.0
    dx, dy = bcx - acx, bcy - acy
    # Rel bus selebar lembar: cabang selalu masuk/keluar lewat sisi horizontal,
    # kecuali target benar-benar di bawah/atas rel (kasus sld, P2/E-17).
    if a["spec"].get("shape") == "bus":
        return "bottom" if bcy > acy else "top"
    if b["spec"].get("shape") == "bus":
        return "top" if bcy > acy else "bottom"
    if abs(dy) >= abs(dx):
        return "bottom" if dy > 0 else "top"
    return "right" if dx > 0 else "left"


def _anchor(node, side, slot, slots):
    """Jangkar dikipas: garis keluar dari titik berbeda pada sisi kotak (P5).
    ENH-D E-17: rel bus digambar sebagai garis tebal di TENGAH blok; tap cabang
    wajib mendarat di garis rel itu (bukan tepi bawah blok) agar tidak terbaca
    menggantung di bawah rel."""
    frac = (slot + 1.0) / (slots + 1.0)
    if node["spec"].get("shape") == "bus" and side in ("bottom", "top"):
        return (node["x"] + node["w"] * frac, node["y"] + node["h"] / 2.0)
    if side == "bottom":
        return (node["x"] + node["w"] * frac, node["y"] + node["h"])
    if side == "top":
        return (node["x"] + node["w"] * frac, node["y"])
    if side == "right":
        return (node["x"] + node["w"], node["y"] + node["h"] * frac)
    return (node["x"], node["y"] + node["h"] * frac)


def _rect_hit(p, q, node, pad=0.05):
    """Apakah segmen p->q menembus interior kotak node."""
    x1, y1 = node["x"] + pad, node["y"] + pad
    x2, y2 = node["x"] + node["w"] - pad, node["y"] + node["h"] - pad
    ax, ay = p[0], p[1]
    bx, by = q[0], q[1]
    if abs(ay - by) < 1e-9:  # horizontal
        return min(ax, bx) < x2 and max(ax, bx) > x1 and y1 < ay < y2
    if abs(ax - bx) < 1e-9:  # vertikal
        return min(ay, by) < y2 and max(ay, by) > y1 and x1 < ax < x2
    steps = 24  # diagonal pendek: sampling
    for i in range(steps + 1):
        t = i / float(steps)
        sx, sy = ax + (bx - ax) * t, ay + (by - ay) * t
        if x1 < sx < x2 and y1 < sy < y2:
            return True
    return False


def route_sequence_messages(spec, sheet):
    """Keluarga sequence: pesan adalah garis horizontal pada baris waktu bertingkat
    (P2 'waktu memiliki sumbu vertikal'); tiap pesan naik satu langkah baseline."""
    order = {n["id"]: i for i, n in enumerate(spec["nodes"])}
    xs = [ll["x"] for ll in sheet.lifelines]
    paths = []
    y = float(getattr(sheet, "msg_y", sheet.top))
    step = float(getattr(sheet, "msg_step", snap(BASELINE_PT * 3, LATTICE_Y)))
    for e in spec["edges"]:
        a, b = order[e["from"]], order[e["to"]]
        xa, xb = xs[a], xs[b]
        if abs(xa - xb) < 1e-9:      # pesan ke diri sendiri: lipatan kecil
            xb = xa + LATTICE_X * 2
        paths.append({"edge": e, "pts": [(xa, y), (xb, y)]})
        y += step
    return paths


def route_edges(spec, sheet):
    """Ortogonal + kipas + detur hambatan (P5). Mengembalikan daftar jalur titik."""
    nodes = sheet.nodes
    opp = {"bottom": "top", "top": "bottom", "right": "left", "left": "right"}
    grouped = {}
    for e in spec["edges"]:
        a, b = nodes[e["from"]], nodes[e["to"]]
        sa = _side_of(a, b)
        grouped.setdefault((e["from"], sa), []).append(e)
        grouped.setdefault((e["to"], opp[sa]), []).append(e)
    paths = []
    for e in spec["edges"]:
        a, b = nodes[e["from"]], nodes[e["to"]]
        sa = _side_of(a, b)
        sb = opp[sa]
        ia = grouped[(e["from"], sa)].index(e)
        ib = grouped[(e["to"], sb)].index(e)
        p = _anchor(a, sa, ia, len(grouped[(e["from"], sa)]))
        q = _anchor(b, sb, ib, len(grouped[(e["to"], sb)]))
        stub = snap(LATTICE_Y, LATTICE_Y)
        if sa in ("bottom", "top"):
            pa = (p[0], p[1] + (stub if sa == "bottom" else -stub))
            # ENH-D E-17: stub target ARAH BALIK dari batas (masuk dari luar),
            # bukan searah (menembus simpul lalu naik lagi = konektor menggantung)
            pb = (q[0], q[1] + (stub if sb == "bottom" else -stub))
            midy = snap((pa[1] + pb[1]) / 2.0, LATTICE_Y)
            pts = [p, pa, (pa[0], midy), (pb[0], midy), pb, q]
        else:
            pa = (p[0] + (stub if sa == "right" else -stub), p[1])
            pb = (q[0] + (stub if sb == "right" else -stub), q[1])
            midx = snap((pa[0] + pb[0]) / 2.0, LATTICE_X)
            pts = [p, pa, (midx, pa[1]), (midx, pb[1]), pb, q]
        pts = _detour(pts, (e["from"], e["to"]), nodes, sheet.W)
        paths.append({"edge": e, "pts": pts})
    return paths


def _blocked(pts, endpoints, nodes, bounds=None):
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        if bounds is not None:
            W = bounds
            for (px, py) in ((ax, ay), (bx, by)):
                if px < -1e-6 or px > W + 1e-6 or py < -1e-6:
                    return {"id": "<luar lembar>"}
        for nid, nd in nodes.items():
            if nid in endpoints:
                continue
            if _rect_hit((ax, ay), (bx, by), nd):
                return nd
    return None


def _detour(pts, endpoints, nodes, bounds=None):
    """P5: detur hambatan mengelilingi kotak tak terkait; gagal = DATUM-32.
    Jalur yang keluar lebar lembar tidak dianggap solusi (P8 DATUM-37)."""
    cur = pts
    for _attempt in range(6):
        hit = _blocked(cur, endpoints, nodes, bounds)
        if hit is None:
            return cur
        if "y" not in hit:      # sentinel luar-lembar: tidak ada kotak untuk dikelilingi
            break
        start, end = cur[0], cur[-1]
        pad = snap(LATTICE_Y * 2, LATTICE_Y)
        below = snap(hit["y"] + hit["h"] + pad, LATTICE_Y)
        above = snap(hit["y"] - pad, LATTICE_Y)
        right = snap(hit["x"] + hit["w"] + pad, LATTICE_X)
        left = snap(hit["x"] - pad, LATTICE_X)
        cands = []
        for cy in (below, above):
            if cy >= 0:
                cands.append([start, (start[0], cy), (end[0], cy), end])
                cands.append([start, (start[0], cy), (right, cy), (right, end[1]), end])
                cands.append([start, (start[0], cy), (left, cy), (left, end[1]), end])
        for cx in (right, left):
            if cx >= 0:
                cands.append([start, (cx, start[1]), (cx, end[1]), end])
        ok = [c for c in cands if _blocked(c, endpoints, nodes, bounds) is None]
        if not ok:
            break
        # pilih jalur terpendek yang bersih agar gambar tetap hemat
        cur = min(ok, key=lambda c: sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(c, c[1:])))
    hit = _blocked(cur, endpoints, nodes, bounds)
    if hit is None:
        return cur
    raise DiagramDefect("DATUM-32: konektor %s->%s terpaksa menembus kotak tak terkait '%s' dan detur gagal (P5/P8)"
                        % (endpoints[0], endpoints[1], hit["id"]))


def add_crossing_hops(paths):
    """P5: lintasan horizontal melompat di atas lintasan vertikal (jari-jari LIMITS.hop_radius_mm)."""
    hops = []
    for i, p in enumerate(paths):
        segs = list(zip(p["pts"], p["pts"][1:]))
        for j, q in enumerate(paths):
            if j <= i:
                continue
            for s2 in zip(q["pts"], q["pts"][1:]):
                for (ax, ay), (bx, by) in segs:
                    (cx, cy), (dx, dy) = s2
                    hor = abs(ay - by) < 1e-9
                    ver = abs(cx - dx) < 1e-9
                    if not (hor and ver):
                        continue
                    if (min(ax, bx) < cx < max(ax, bx)) and (min(cy, dy) < ay < max(cy, dy)):
                        hops.append((i, cx, ay))
    return hops


# ------------------------------------------------------------- render SVG
def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _svg_text(x, y, text, role_name, colour_token=None, anchor="middle", upper=None, track=None, weight=None):
    r = role(role_name)
    size = pt2mm(r["size"])
    face = face_of(role_name)
    col = colour_of(colour_token or r.get("colour", INK_TEXT))
    txt = str(text)
    if upper or r.get("upper"):
        txt = txt.upper()
    ls = ""
    tr = track if track is not None else r.get("track_em")
    if tr:
        ls = ' letter-spacing="%s"' % round(pt2mm(r["size"]) * float(tr), 3)
    w = weight or r.get("weight", 400)
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s" font-weight="%s" fill="%s" '
            'text-anchor="%s"%s>%s</text>'
            % (round(x, 2), round(y, 2), _esc(face), round(size, 3), w, col, anchor, ls, _esc(txt)))


def _shape_svg(nd, stroke_tok, fill, extra):
    n = nd["spec"]
    shape = n.get("shape", "box")
    x, y, w, h = nd["x"], nd["y"], nd["w"], nd["h"]
    sw = extra.get("stroke_w", STROKE_PRIMARY)
    col = colour_of(stroke_tok)
    common = 'data-node="%s" fill="%s" stroke="%s" stroke-width="%s"' % (_esc(nd["id"]), fill, col, sw)
    if shape == "stadium":  # P3: satu-satunya bentuk yang boleh beradius
        r = h / 2.0
        return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" ry="%s" %s/>' % (
            round(x, 2), round(y, 2), round(w, 2), round(h, 2), round(r, 2), round(r, 2), common)
    if shape == "diamond":
        pts = "%s,%s %s,%s %s,%s %s,%s" % (round(x + w / 2, 2), round(y, 2), round(x + w, 2), round(y + h / 2, 2),
                                           round(x + w / 2, 2), round(y + h, 2), round(x, 2), round(y + h / 2, 2))
        return '<polygon points="%s" %s/>' % (pts, common)
    if shape == "parallelogram":
        k = w * 0.18
        pts = "%s,%s %s,%s %s,%s %s,%s" % (round(x + k, 2), round(y, 2), round(x + w, 2), round(y, 2),
                                           round(x + w - k, 2), round(y + h, 2), round(x, 2), round(y + h, 2))
        return '<polygon points="%s" %s/>' % (pts, common)
    if shape == "hexagon":
        k = w * 0.22
        pts = "%s,%s %s,%s %s,%s %s,%s %s,%s %s,%s" % (
            round(x + k, 2), round(y, 2), round(x + w - k, 2), round(y, 2), round(x + w, 2), round(y + h / 2, 2),
            round(x + w - k, 2), round(y + h, 2), round(x + k, 2), round(y + h, 2), round(x, 2), round(y + h / 2, 2))
        return '<polygon points="%s" %s/>' % (pts, common)
    if shape == "cylinder":
        ry = h * 0.16
        return ('<path d="M%s %s a%s %s 0 0 0 %s 0 L%s %s a%s %s 0 0 1 -%s 0 Z" %s/>' % (
            round(x, 2), round(y + ry, 2), round(w / 2, 2), round(ry, 2), round(w, 2),
            round(x + w, 2), round(y + h - ry, 2), round(w / 2, 2), round(ry, 2), round(w, 2), common))
    if shape == "circle":
        return '<circle cx="%s" cy="%s" r="%s" %s/>' % (round(x + w / 2, 2), round(y + h / 2, 2),
                                                        round(min(w, h) / 2, 2), common)
    if shape == "bus":  # P3: rel berat — garis tebal penuh lebar
        return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>' % (
            round(x, 2), round(y + h / 2, 2), round(x + w, 2), round(y + h / 2, 2), col,
            round(STROKE_PRIMARY * 3, 2))
    if shape == "doubled":
        return ('<rect x="%s" y="%s" width="%s" height="%s" %s/><rect x="%s" y="%s" width="%s" height="%s" '
                'fill="none" stroke="%s" stroke-width="%s"/><line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>' % (
                    round(x, 2), round(y, 2), round(w, 2), round(h, 2), common,
                    round(x + 1.2, 2), round(y + 1.2, 2), round(w - 2.4, 2), round(h - 2.4, 2), col, round(STROKE_HAIR, 2),
                    round(x + 1.2, 2), round(y + h / 2, 2), round(x + w - 1.2, 2), round(y + h / 2, 2), col, round(STROKE_HAIR, 2)))
    if shape == "shadowed":  # entitas eksternal: bingkai + bayangan hairline
        off = snap(LATTICE_Y / 2, 0.1)
        return ('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="%s"/>'
                '<rect x="%s" y="%s" width="%s" height="%s" %s/>' % (
                    round(x + off, 2), round(y + off, 2), round(w, 2), round(h, 2), colour_of("ink200"), round(STROKE_HAIR, 2),
                    round(x, 2), round(y, 2), round(w, 2), round(h, 2), common))
    return '<rect x="%s" y="%s" width="%s" height="%s" %s/>' % (round(x, 2), round(y, 2), round(w, 2), round(h, 2), common)


def build_svg(spec, release=False):
    """Spek -> (svg, laporan). Cek yang dijalankan dicatat jujur (banner jujur P8)."""
    ran = validate_spec(spec)
    if release and spec.get("labels_verified") is not True:
        raise DiagramDefect("labels_verified bukan true: gambar adalah draft, render dan tinjau, jangan kirim (P1)")
    if release:
        ran.append("P1-labels_verified")

    sheet = Sheet(spec["width_mm"])
    engine = getattr(sys.modules[__name__], FAMILIES[spec["family"]]["engine"])
    engine(spec, sheet)

    # P5/P8: simpul dikunci ke kisi, lebar di-clamp ke tepi lembar, dan tidak
    # boleh keluar lebar penuh (DATUM-37). Rel bus memang selebar lembar.
    for nd in sheet.nodes.values():
        nd["x"] = snap(nd["x"], LATTICE_X)
        nd["y"] = snap(nd["y"], LATTICE_Y)
        nd["w"] = snap(nd["w"], LATTICE_X)
        nd["h"] = snap(nd["h"], LATTICE_Y)
        if nd["spec"].get("shape") != "bus":
            avail = snap_floor(sheet.W - nd["x"], LATTICE_X)
            if nd["w"] > avail:
                nd["w"] = avail
        if nd["x"] < -1e-6 or nd["x"] >= sheet.W or nd["w"] <= 0 or nd["x"] + nd["w"] > sheet.W + 1e-6:
            raise DiagramDefect("DATUM-37: simpul %s keluar lebar lembar (%.3f..%.3f dari %.1f mm) (P8)"
                                % (nd["id"], nd["x"], nd["x"] + nd["w"], sheet.W))
    ran.append("DATUM-37-lebar")

    if spec["family"] == "sequence":
        paths = route_sequence_messages(spec, sheet)
        sheet.msg_end = max(p["pts"][0][1] for p in paths) if paths else sheet.msg_y
        ran.append("P2-sequence-time-vertical")
    else:
        paths = route_edges(spec, sheet)
    hops = add_crossing_hops(paths)
    ran.append("DATUM-32")  # ditegakkan oleh _detour/route_edges (gagal = raise)

    # P8 DATUM-28: tidak ada tipe yang dicetak engine di bawah ambang 5,5 pt.
    # Ambang verbatim dalam pt; ukuran wajah dibaca dari token, jadi bila
    # tokens.json diturunkan di bawah ambang, engine menolak (bukan diam-diam).
    for rname in DIAGRAM_ROLES:
        if float(role(rname)["size"]) < LIMITS["diagram_type_min_pt"]:
            raise DiagramDefect("DATUM-28: peran %s mencetak %.2f pt di bawah ambang %.1f pt (P8)"
                                % (rname, float(role(rname)["size"]), LIMITS["diagram_type_min_pt"]))
    ran.append("DATUM-28")

    # P8 DATUM-27: semua garis >= lantai fotokopi dari token.
    for sw in (STROKE_PRIMARY, STROKE_HAIR, STROKE_PRIMARY * 3):
        if sw < STROKE_FLOOR_MM - 1e-9:
            raise DiagramDefect("DATUM-27: garis %.3f mm di bawah lantai fotokopi %.3f mm (T rules_mm, P8)" % (sw, STROKE_FLOOR_MM))
    ran.append("DATUM-27")

    # BUG-DATUM-DIAGRAM (kartu t_ef103378): blok kaki apparatus (caption/KEY/
    # SUMBER pada apparatus figure, KEY pada page ber-legend) dicetak di bawah
    # gambar; tanpa cadangan ini garis dasarnya mendarat di dalam simpul baris
    # terakhir (cacat dilaporkan FIGUR-1 t_559f107b, semua diagram ber-legend).
    sheet.foot = _foot_reserve_mm(spec)
    H = sheet.height()
    # P8 DATUM-33: gambar tidak boleh lebih tinggi dari blok teks halaman.
    if H > LIMITS["text_block_max_mm"] + 1e-6:
        raise DiagramDefect("DATUM-33: tinggi gambar %.2f mm melewati blok teks %.1f mm (P8)"
                            % (H, LIMITS["text_block_max_mm"]))
    ran.append("DATUM-33")

    # P5/P8 DATUM-25: <=5 nilai warna per gambar. Pewarnaan dihitung dari yang
    # benar-benar dicetak engine (garis simpul, teks peran, glif, konektor, arsiran).
    used = set()
    for nd in sheet.nodes.values():
        used.add(node_stroke_token(nd))
    for rname in ("caption", "source_line", "table_header"):
        used.add(role(rname).get("colour", INK_TEXT))
    for nd in sheet.nodes.values():
        if nd["spec"].get("mark"):
            used.add("signal")          # glif rumah: mono amber/signal (pitfall warisan)
        if nd["spec"].get("class", {}).get("accent") or nd["spec"].get("class", {}).get("secondary"):
            used.add("ink400")          # isian arsiran memakai tinta 400
    if sheet.lanes or sheet.lifelines:
        used.add("ink200")              # pemisah lajur / garis kehidupan rambut
    for z in spec.get("zones") or []:
        used.add("ink400")
    for p in paths:
        used.add(EDGE_KINDS[p["edge"]["kind"]]["colour"])
    used = {colour_of(t) for t in used}
    used.discard(PAPER)
    if len(used) > int(LIMITS["max_colour_values"]):
        raise DiagramDefect("DATUM-25: %d nilai warna dalam satu gambar, maksimum %d (temuan E-16: plafon ini nyata) (P5/P8)"
                            % (len(used), LIMITS["max_colour_values"]))
    ran.append("DATUM-25")

    apparatus = spec.get("apparatus", "page")
    out = []
    # P9 E-08: root SVG membawa mm, bukan px polos.
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="%smm" height="%smm" '
               'viewBox="0 0 %s %s" version="1.1">' % (round(sheet.W, 3), round(H, 3), round(sheet.W, 3), round(H, 3)))
    out.append('<!-- generator datum_diagram.py v2.0.0 (rebuild DHS-RB-04, BUKAN restorasi v1.3/Rev J) | '
               'family=%s | token=%s -->' % (_esc(spec["family"]), _esc(os.path.basename(tokens_path()))))
    if apparatus == "page":  # P6: komentar kewajiban apparatus, dilaporkan lint cek 36
        out.append("<!-- DATUM-APPARATUS-REQUIRED: caption, source dan baris kunci dicetak oleh halaman, bukan oleh SVG ini (P6, lint cek 36) -->")
    out.append('<defs>')
    # P5/catatan fotokopi: isian diagram berupa arsiran 45/135 derajat, bukan tint abu-abu.
    out.append('<pattern id="datum-hatch45" width="1.6" height="1.6" patternUnits="userSpaceOnUse" '
               'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.6" stroke="%s" stroke-width="0.3"/></pattern>'
               % colour_of("ink400"))
    out.append('<pattern id="datum-hatch135" width="1.6" height="1.6" patternUnits="userSpaceOnUse" '
               'patternTransform="rotate(135)"><line x1="0" y1="0" x2="0" y2="1.6" stroke="%s" stroke-width="0.3"/></pattern>'
               % colour_of("ink400"))
    for kind, meta in sorted(EDGE_KINDS.items()):  # kepala panah per jenis (P4: solid/open)
        col = colour_of(meta["colour"])
        if meta["head"] == "solid":
            out.append('<marker id="head-%s" markerWidth="4" markerHeight="4" refX="3.4" refY="1.6" orient="auto">'
                       '<path d="M0,0 L3.6,1.6 L0,3.2 Z" fill="%s"/></marker>' % (kind, col))
        else:
            out.append('<marker id="head-%s" markerWidth="4" markerHeight="4" refX="3.4" refY="1.6" orient="auto">'
                       '<path d="M0,0 L3.6,1.6 L0,3.2" fill="none" stroke="%s" stroke-width="0.35"/></marker>' % (kind, col))
    out.append("</defs>")
    out.append('<rect x="0" y="0" width="%s" height="%s" fill="%s"/>' % (round(sheet.W, 3), round(H, 3), PAPER))

    # lajur akuntabilitas + garis pemisah rambut (P2 swimlane, T rules_mm.hair)
    gutter_w = float(getattr(sheet, "gutter_w", 0.0))
    for lane in sheet.lanes:
        out.append('<line x1="0" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>' % (
            round(lane["y"], 2), round(sheet.W, 2), round(lane["y"], 2), colour_of("ink200"), round(STROKE_HAIR, 2)))
        # label lajur duduk di parit kiri, rata kiri, di dalam pita lajur
        out.append(_svg_text(0.5, lane["y"] + pt2mm(role("table_header")["size"]) + LATTICE_Y / 2.0,
                             lane["name"], "table_header", colour_token="ink400", anchor="start"))
        if gutter_w:
            out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>' % (
                round(gutter_w, 2), round(lane["y"], 2), round(gutter_w, 2),
                round(lane["y"] + lane["h"], 2), colour_of("ink200"), round(STROKE_HAIR, 2)))

    for ll in sheet.lifelines:
        out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-dasharray="%s"/>' % (
            round(ll["x"], 2), round(ll["top"], 2), round(ll["x"], 2), round(H - LATTICE_Y, 2),
            colour_of("ink200"), round(STROKE_HAIR, 2), DASH_PATTERNS["dashed"]))

    # zona kepercayaan: penutupan garis putus + tab label, tanpa isian (P5)
    for z in spec.get("zones") or []:
        members = [sheet.nodes[m] for m in z.get("members", []) if m in sheet.nodes]
        if not members:
            raise DiagramDefect("zona '%s' tanpa anggota dikenal (P5 trust zone)" % z.get("id"))
        zx = min(m["x"] for m in members) - LATTICE_X / 2
        zy = min(m["y"] for m in members) - LATTICE_Y * 2
        zw = max(m["x"] + m["w"] for m in members) - zx + LATTICE_X / 2
        zh = max(m["y"] + m["h"] for m in members) - zy + LATTICE_Y * 2
        out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="%s" stroke-dasharray="%s"/>' % (
            round(zx, 2), round(zy, 2), round(zw, 2), round(zh, 2), colour_of("ink400"), round(STROKE_HAIR, 2),
            DASH_PATTERNS["dashed"]))
        out.append(_svg_text(zx + 1.0, zy + pt2mm(5.0), z.get("label", z.get("id", "zona")), "table_header",
                             colour_token="ink400", anchor="start"))

    # konektor — BUG-DATUM-DIAGRAM (kartu t_ef103378): label tepi dikumpulkan
    # dulu; SEMUA jalur dan hop digambar lebih dahulu, baru tiap label diberi
    # pita knockout kertas lalu teksnya. Urutan ini menjamin tidak ada garis
    # konektor (milik jalur mana pun) tercetak di atas teks label.
    edge_labels = []
    for p in paths:
        kind = p["edge"]["kind"]
        meta = EDGE_KINDS[kind]
        col = colour_of(meta["colour"])
        dash = DASH_PATTERNS[meta["pattern"]]
        pts = p["pts"]
        d = "M " + " L ".join("%s %s" % (round(x, 2), round(y, 2)) for x, y in pts)
        weight = round(STROKE_PRIMARY * 1.6, 2) if kind == "accent" else round(STROKE_PRIMARY, 2)
        attrs = 'fill="none" stroke="%s" stroke-width="%s"' % (col, weight)
        if dash:
            attrs += ' stroke-dasharray="%s"' % dash
        out.append('<path d="%s" %s marker-end="url(#head-%s)"/>' % (d, attrs, kind))
        size_mm = pt2mm(role("evidence_rail")["size"])
        lw = est_text_mm(p["edge"]["label"], "evidence_rail")
        mx, my = _label_pos(pts, sheet.nodes, lw, size_mm * 1.4)
        edge_labels.append((mx, my - pt2mm(1.2), p["edge"]["label"], meta["colour"]))
    for (i, hx, hy) in hops:  # lompatan silang pada lintasan horizontal (P5)
        r = float(LIMITS["hop_radius_mm"])
        # BUG-DATUM-DIAGRAM (kartu t_ef103378, laporan FIGUR-2 t_a3146011): kind
        # adalah STRING nama jenis, bukan dict — indeks ganda = TypeError setiap
        # crossing-hop nyata (crash terbukti G10.3). Nama token diambil via EDGE_KINDS.
        out.append('<path d="M %s %s A %s %s 0 0 1 %s %s" fill="none" stroke="%s" stroke-width="%s"/>' % (
            round(hx - r, 2), round(hy, 2), round(r, 2), round(r, 2), round(hx + r, 2), round(hy, 2),
            colour_of(EDGE_KINDS[paths[i]["edge"]["kind"]]["colour"]), round(STROKE_PRIMARY, 2)))
    for (mx, my, lab, col_tok) in edge_labels:
        out.append(_label_knockout(mx, my, lab, sheet.W))
        out.append(_svg_text(mx, my, lab, "evidence_rail",
                             colour_token=col_tok, anchor="middle"))

    # simpul + label + glif asal
    for nd in sheet.nodes.values():
        n = nd["spec"]
        tok = node_stroke_token(nd)
        fill = "none"
        if n.get("class", {}).get("accent"):
            fill = "url(#datum-hatch45)"
        elif n.get("class", {}).get("secondary"):
            fill = "url(#datum-hatch135)"
        out.append(_shape_svg(nd, tok, fill, {"stroke_w": STROKE_PRIMARY}))
        cx, cy = nd["x"] + nd["w"] / 2.0, nd["y"] + nd["h"] / 2.0
        out.append(_svg_text(cx, cy, n["label"], "caption", colour_token="ink900"))
        if n.get("sub"):
            out.append(_svg_text(cx, cy + pt2mm(role("caption")["size"]), n["sub"], "source_line"))
        if n.get("mark"):
            # pitfall warisan: glif rumah tetap mono (amber/signal) di XML, jangan tukar wajah
            out.append('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" text-anchor="end">%s</text>' % (
                round(nd["x"] + nd["w"] - pt2mm(1.5), 2), round(nd["y"] + pt2mm(role("caption")["size"]), 2),
                _esc(FACES["mono"]), round(pt2mm(role("register_block")["size"]), 3), colour_of("signal"),
                _esc(MARKS[n["mark"]])))
        if n.get("tag"):
            out.append(_svg_text(nd["x"] + pt2mm(1.5), nd["y"] + pt2mm(role("caption")["size"]), n["tag"],
                                 "table_header", colour_token="ink400", anchor="start"))

    # apparatus = figure: SVG mengemban caption, sumber dan baris kunci sendiri (P6)
    foot = H - LATTICE_Y * 2
    if apparatus == "figure":
        out.append(_svg_text(0, foot, "%s  %s" % (spec["id"], spec["title"]), "caption",
                             colour_token="ink700", anchor="start"))
        foot -= LATTICE_Y
        if spec.get("legend"):
            out.append(_svg_text(0, foot, "KEY  " + "  ·  ".join(str(x) for x in spec["legend"]), "table_header",
                                 colour_token="ink400", anchor="start", track=TRACK["micro_label_wider"]))
            foot -= LATTICE_Y
        out.append(_svg_text(0, foot, "SUMBER  " + "; ".join(str(x) for x in spec["sources"]), "source_line",
                             colour_token="ink400", anchor="start"))
    else:
        if spec.get("legend"):
            out.append(_svg_text(0, foot, "KEY  " + "  ·  ".join(str(x) for x in spec["legend"]), "table_header",
                                 colour_token="ink400", anchor="start", track=TRACK["micro_label_wider"]))
    out.append("</svg>")
    svg = "\n".join(out) + "\n"

    # P8 DATUM-29/30 pada keluaran sendiri: bila apparatus=figure, SVG wajib
    # memikul caption bernomor dan baris SUMBER; apparatus=page wajib menyatakan
    # kewajiban itu lewat komentar (dilaporkan lint cek 36, P6).
    if apparatus == "figure":
        if ("SUMBER" not in svg) or ("%s  %s" % (spec["id"], spec["title"])) not in svg:
            raise DiagramDefect("DATUM-29/30: apparatus figure tanpa caption bernomor atau baris SUMBER di SVG (P6/P8)")
    elif "DATUM-APPARATUS-REQUIRED" not in svg:
        raise DiagramDefect("DATUM-36 kewajiban apparatus tidak tercatat pada apparatus page (P6)")
    ran.append("DATUM-29/30")

    report = {"checks_run": ran, "width_mm": sheet.W, "height_mm": H, "colour_values": sorted(used),
              "n_colour": len(used), "n_hops": len(hops), "n_nodes": len(sheet.nodes),
              "n_edges": len(paths), "apparatus": apparatus, "family": spec["family"]}
    return svg, report


def pt2mm_zero(mm):  # dipertahankan untuk uji silang konversi (dipakai selftest)
    return float(mm)


def node_stroke_token(nd):
    """Kelas simpul -> nama token warna (P4/P5; tidak ada hex di kode)."""
    c = nd["spec"].get("class", {}) or {}
    if c.get("accent"):
        return "signal"
    if c.get("external") or nd["spec"].get("shape") == "shadowed":
        return "ink400"
    if nd["spec"].get("shape") == "bus":
        return "ink900"
    return "ink700"


def _mid_label(pts):
    """Titik tengah lintasan untuk label konektor."""
    segs = list(zip(pts, pts[1:]))
    if not segs:
        return 0, 0
    longest = max(segs, key=lambda s: math.hypot(s[1][0] - s[0][0], s[1][1] - s[0][1]))
    return ((longest[0][0] + longest[1][0]) / 2.0, (longest[0][1] + longest[1][1]) / 2.0)


def _label_pos(pts, nodes, lw, lh):
    """BUG-DATUM-DIAGRAM (kartu t_ef103378, vonis visual controller kartu induk):
    label tepi (YA/TIDAK/kind) dulu selalu duduk di titik tengah segmen terpanjang
    tanpa uji hambatan -> garis konektor menembus teks atau teks mendarat di atas
    judul simpul. Kandidat = titik tengah tiap segmen (urut dari terpanjang);
    pilih yang pertama di luar kotak simpul mana pun (dibesarkan setengah kotak
    label). Semua kandidat bertabrakan = perilaku lama (titik tengah terpanjang),
    dengan knockout kertas di langkah render agar garis tetap tidak menembus teks."""
    def _len(s):
        return math.hypot(s[1][0] - s[0][0], s[1][1] - s[0][1])
    segs = list(zip(pts, pts[1:]))
    if not segs:
        return 0.0, 0.0
    order = sorted(range(len(segs)), key=lambda i: -_len(segs[i]))
    pad_x, pad_y = lw / 2.0 + 0.8, lh / 2.0 + 0.4
    for i in order:
        (ax, ay), (bx, by) = segs[i]
        mx, my = (ax + bx) / 2.0, (ay + by) / 2.0
        hit = any(nd["x"] - pad_x <= mx <= nd["x"] + nd["w"] + pad_x
                  and nd["y"] - pad_y <= my <= nd["y"] + nd["h"] + pad_y
                  for nd in nodes.values())
        if not hit:
            return mx, my
    return _mid_label(pts)


def _label_knockout(mx, my, text, sheet_w):
    """Pita kertas pemutus garis di belakang label tepi (latar token PAPER,
    bukan warna baru — DATUM-25 menghitung nilai warna terpakai, kertas dibuang
    dari hitungan). my = garis dasar teks."""
    size = pt2mm(role("evidence_rail")["size"])
    tr = role("evidence_rail").get("track_em")
    lw = est_text_mm(text, "evidence_rail") + (pt2mm(size) * float(tr) * len(str(text)) if tr else 0.0)
    kw, kh = lw + 1.6, size * 1.7
    kx = min(max(mx - kw / 2.0, 0.0), max(0.0, sheet_w - kw))
    ky = my - size * 1.15
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (
        round(kx, 2), round(ky, 2), round(kw, 2), round(kh, 2), PAPER)


def estimate(spec):
    """P9 E-19: perkirakan geometri tanpa menulis berkas."""
    svg, rep = build_svg(spec, release=False)
    return rep


def render_hint(rep):
    """P6: PNG 300 dpi untuk .docx — hitung piksel dari lebar mm yang dinyatakan."""
    dpi = 300
    px = lambda mm: int(round(mm / 25.4 * dpi))
    return {"dpi": dpi, "width_px": px(rep["width_mm"]), "height_px": px(rep["height_mm"]),
            "note": "PNG dihasilkan datum_render.py (DHS-RB-05); helper .docx melepas spasi baris %s pt (P6)" % TOK["type"]["baseline_pt"]}


# --------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(prog="datum_diagram.py", description="Engine diagram DATUM v2.0.0 (spek JSON -> SVG mm)")
    ap.add_argument("spec", nargs="?", help="berkas diagram-spec.json")
    ap.add_argument("-o", "--out", help="tujuan SVG")
    ap.add_argument("--schema", action="store_true", help="cetak bidang minimum spek (P1 Tabel 6.1)")
    ap.add_argument("--list", action="store_true", help="cetak keluarga/bentuk/jenis konektor (P2/P3/P4)")
    ap.add_argument("--estimate", action="store_true", help="P9 E-19: perkirakan geometri tanpa menulis SVG")
    ap.add_argument("--release", action="store_true", help="gerbang rilis: labels_verified wajib true")
    ap.add_argument("--json", action="store_true", help="laporan sebagai JSON")
    args = ap.parse_args(argv)

    if args.schema:
        print(json.dumps({"fields": SPEC_FIELDS, "families": sorted(FAMILIES), "shapes": sorted(SHAPES),
                          "edge_kinds": sorted(EDGE_KINDS), "limits": LIMITS,
                          "token_source": tokens_path()}, ensure_ascii=False, indent=2))
        return 0
    if args.list:
        print("FAMILIES (P2: %d nama, %d mesin)" % (len(FAMILIES), len(set(LAYOUTS.values()))))
        for k, v in sorted(FAMILIES.items()):
            print("  %-9s %-18s %s" % (k, v["engine"], v["draw_when"]))
        print("SHAPES (P3: %d)" % len(SHAPES))
        for k, v in sorted(SHAPES.items()):
            print("  %-14s %-14s %s" % (k, v["notation"], v["means"]))
        print("EDGE_KINDS (P4: %d)" % len(EDGE_KINDS))
        for k, v in sorted(EDGE_KINDS.items()):
            print("  %-8s %-9s %-7s iso %-5s %s" % (k, v["pattern"], v["head"], v["iso"], v["use"]))
        return 0
    if not args.spec:
        ap.error("butuhkan berkas diagram-spec.json (atau --schema/--list)")
    try:
        spec = load_spec(args.spec)
        if args.estimate:
            rep = estimate(spec)
            rep["render_hint"] = render_hint(rep)
            print(json.dumps(rep, ensure_ascii=False, indent=2) if args.json else json.dumps(rep, ensure_ascii=False))
            return 0
        svg, rep = build_svg(spec, release=args.release)
        out = args.out or (os.path.splitext(args.spec)[0] + ".svg")
        open(out, "w", encoding="utf-8").write(svg)
        rep["out"] = out
        rep["bytes"] = len(svg.encode("utf-8"))
        print(json.dumps(rep, ensure_ascii=False, indent=2) if args.json else json.dumps(rep, ensure_ascii=False))
        return 0
    except DiagramDefect as ex:
        sys.stderr.write("DIAGRAM DEFECT: %s\n" % ex)
        return 1


if __name__ == "__main__":
    sys.exit(main())
