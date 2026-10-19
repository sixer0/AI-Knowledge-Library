# -*- coding: utf-8 -*-
"""selftest_builder.py — gerbang eksekusi dua arah kelas builder/render DATUM
v2.0.0 (DHS-RB-05 t_28d93e3c; preseden t_a21e89ab: kompilasi bukan gerbang,
jalankan dan baca exit code; basal rusak wajib tertangkap sebelum klaim GREEN).

Cara pakai: letakkan BERDAMPINGAN dengan datum_docx.py, datumcheck.py,
datum_xlsx.py, datum_pptx.py, embed_fonts.py, datumbind.py, tokens.json lalu:
    uv run --python 3.11 --with python-docx --with openpyxl --with python-pptx \
        python selftest_builder.py
Cetak CHECK n: PASS|FAIL per butir + VERDICT akhir; exit != 0 bila ada FAIL.
Arah dua-duanya diuji: basal BENAR harus lolos, cacat tanam harus DITOLAK.
"""
import json, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import datumcheck as DC
from datumcheck import CheckDefect
import datum_docx as DD
from datumbind import Register, Derivation, tokens_path

fails = []


def check(n, name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    if not cond:
        fails.append(name)
    print(f"CHECK {n}: {tag} — {name}" + (f" | {detail}" if detail else ""))


def expect_raise(n, name, fn):
    try:
        fn()
        check(n, name, False, "tidak raise")
    except CheckDefect as ex:
        check(n, name, True, str(ex)[:70])


# ================= A. guard situs-panggil (basal rusak -> ditolak) ==========
expect_raise("A1", "GUARD-N1 menolak underscore nama berkas",
             lambda: DC.name_guard("laporan_harian.docx"))
check("A1b", "GUARD-N1 meloloskan nama tanpa underscore",
      DC.name_guard("Laporan Harian.docx") is True)

expect_raise("A2", "GUARD-G1 menolak baris cacah sel beda dari kepala",
             lambda: DC.table_guards("TABEL 1",
                                     [["A", "B", "C"], ["1", "2"]], [40, 44, 44]))
expect_raise("A3", "GUARD-G2 menolak jumlah lebar bukan 128/166 mm",
             lambda: DC.table_guards("TABEL 2",
                                     [["A", "B"], ["1", "2"]], [50, 50]))
check("A3b", "GUARD-G2 meloloskan 128 mm tepat",
      DC.table_guards("TABEL 3", [["A", "B"], ["1", "2"]], [40, 88]) is True)
check("A3c", "GUARD-G2 meloloskan 166 mm penuh",
      DC.table_guards("TABEL 4", [["A", "B"], ["1", "2"]], [66, 100]) is True)
expect_raise("A4", "GUARD-G3 menolak teks sel jebol lebar",
             lambda: DC.table_guards("TABEL 5",
                                     [["A", "B"], ["x" * 400, "2"]], [40, 88]))
expect_raise("A5", "CEK-04 menolak judul pertanyaan",
             lambda: DC.check_heading("Apa itu gaya DATUM?"))
expect_raise("A5b", "CEK-04 menolak kata tanya di awal",
             lambda: DC.check_heading("Bagaimana cara mengukur"))
check("A5c", "CEK-04 meloloskan judul klaim",
      DC.check_heading("Gaya DATUM menekan cacat angka") is True)
expect_raise("A6", "CEK-16 menolak nilai-unit tanpa spasi",
             lambda: DC.check_value_unit("beban 12mm terpasang"))
check("A6b", "CEK-16 meloloskan nilai-unit ber-spasi",
      DC.check_value_unit("beban 12 mm terpasang") is True)
expect_raise("A7", "CEK-10 menolak tabel tanpa SUMBER",
             lambda: DC.check_source_line("", "TABEL 9"))
expect_raise("A8", "DATUM-33 menolak figur lebih tinggi dari blok teks",
             lambda: DC.figure_guards("Gambar uji", 250.0))
check("A8b", "DATUM-33 meloloskan figur 247 mm",
      DC.figure_guards("Gambar uji", 247.0) is True)

# ================= B. builder DOCX basal baik (build nyata) ==================
N = Register(data={
    "nilai basis": {"v": 1250000.0, "dec": 0, "unit": "Rp", "mark": "TERUKUR", "src": "st"},
    "nilai skenario": {"v": 950000.0, "dec": 0, "unit": "Rp", "mark": "TERUKUR", "src": "st"},
    "ruang nilai": {"v": 300000.0, "dec": 0, "unit": "Rp", "mark": "DITURUNKAN", "src": "st"},
})
d = Derivation("D-ST 05", N)
d.line("nilai basis", "nilai basis"); d.line("nilai skenario", "nilai skenario")
d.result("ruang nilai terbuka", "nilai basis - nilai skenario", "ruang nilai")
d.closes("bila asumsi gagal, model ditinjau ulang sebelum terbit.")

GOOD = os.path.join(HERE, "st-baik.docx")   # nama patuh N1 (tanpa underscore)
D = DD.DatumDocx(title="Uji Gerbang Builder DATUM", doc_no="900/GSP/STD/X/2026",
                 rev="A", subject="selftest DHS-RB-05")
D.cover(kicker="uji mesin", deck="satu kalimat pengantar.",
        identity=[("NOMOR", "900-GSP-STD-X-2026", "REVISI", "Rev A"),
                  ("KLASIFIKASI", "BIASA", "TUJUAN", "gerbang selftest")])
D.start_interior("UJI")
D.heading("Mesin builder menegakkan guard sejak situs-panggil", level=1)
D.para("Prosa dengan **tebal**, `mono`, dan tautan https://example.com/gsp "
       "sepanjang satu baris untuk menguji parser inline.")
D.para(f"Nilai pekerjaan {N.rp('nilai basis')} dengan ruang {N.rp('ruang nilai')}.")
D.derivation(d)
D.table([["Komponen", "Beban", "Catatan"],
         ["Panel", "12 mm", "ruang https://example.com/b"],
         ["Rangka", "44 mm", "kaku"]],
        source="ukur alat misi uji (selftest DHS-RB-05)")
D.save(GOOD)
check("B1", "builder DOCX basal baik tersimpan", os.path.isfile(GOOD),
      f"{os.path.getsize(GOOD)} B")

n_link, link_def = DC.audit_links(GOOD)
check("B2", f"tautan hasil build aktif-terlihat ({n_link} tautan)",
      n_link >= 2 and not link_def, "; ".join(link_def[:4]))
check("B3", "em dash nol pada hasil build", not DC.audit_em_dash(GOOD))
check("B4", "properti inti hasil build nyata", not DC.audit_props(GOOD))
check("B5", "updateFields true pada hasil build", DC.audit_update_fields(GOOD))

# bind audit datumbind terhadap hasil build builder (lintasan dua mesin)
stray = Register(data=N.d).audit_docx(GOOD, allow=("900", "2026", "01", "12", "44"),
                                       quiet=True)
check("B6", "bind audit nol stray pada hasil build", stray == [], str(stray))

# B7/B8 FIX-DATUM-ENGINE (t_9b9494b6): pemisah caption properti dokumen,
# default ASCII, jalur legacy mereproduksi byte edisi lama.
import zipfile as _zf


def _doc_xml(path):
    with _zf.ZipFile(path) as z:
        return z.read("word/document.xml").decode("utf-8")


_x = _doc_xml(GOOD)
check("B7", "caption slug default ASCII tanpa U+00B7 (F-1)",
      "KOMPONEN - BEBAN - CATATAN" in _x and "KOMPONEN \u00b7 BEBAN" not in _x)
LEGACY = os.path.join(HERE, "st-legacy.docx")
DL = DD.DatumDocx(title="Uji Legacy Separator DATUM", doc_no="902/GSP/STD/X/2026",
                  rev="A", subject="selftest t_9b9494b6", caption_sep=" \u00b7 ")
DL.start_interior("UJI LEGACY")
DL.table([["Komponen", "Beban", "Catatan"],
          ["Panel", "12 mm", "uji"],
          ["Rangka", "44 mm", "uji"]],
         source="probe mesin uji (selftest t_9b9494b6)")
DL.save(LEGACY)
check("B8", "parameter caption_sep=' \\u00b7 ' memulihkan slug warisan",
      "KOMPONEN \u00b7 BEBAN \u00b7 CATATAN" in _doc_xml(LEGACY))

# ================= C. audit menangkak DOCX jahat ============================
EVIL = os.path.join(HERE, "st-jahat.docx")
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
doc = Document()
doc.add_paragraph("Angka karangan 1.234.567 dan em dash \u2014 terlarang.")
p = doc.add_paragraph()
h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), "rIdX")
r_el = OxmlElement("w:r"); t = OxmlElement("w:t"); t.text = "tautan tanpa rel sah"
r_el.append(t); h.append(r_el); p._p.append(h)
doc.save(EVIL)
nl, defs = DC.audit_links(EVIL)
check("C1", "audit menolak tautan tanpa rel http/penampilan", bool(defs),
      "; ".join(defs[:3]))
check("C2", "audit menangkap em dash di lapisan XML", bool(DC.audit_em_dash(EVIL)))
check("C3", "audit menolak properti inti kosong (title)",
      any("title" in x for x in DC.audit_props(EVIL)))
check("C4", "audit menolak updateFields absen", not DC.audit_update_fields(EVIL))
rc = DC.run_cli([EVIL])
check("C5", "CLI datumcheck exit 1 pada basal jahat", rc == 1, f"exit={rc}")

# ================= D. builder XLSX ==========================================
try:
    import datum_xlsx as DX
    WX = os.path.join(HERE, "st-buku.xlsx")
    W = DX.DatumWorkbook(title="Uji Workbook DATUM", doc_no="901-GSP-STD-X-2026", rev="A")
    W.cover(kicker="uji", judul="Uji Workbook DATUM", deck="deck",
            identity=[("NOMOR", "901", "REV", "A")])
    ws = W.sheet("HASIL UJI")
    W.header(ws, ["Item", "Beban", "Catatan"], widths=[24, 12, 40])
    W.row(ws, ["Panel", 12.5, "ukur"], numeric_cols={1})
    W.row(ws, ["Rangka", 44.0, "kaku"], numeric_cols={1})
    W.source_line(ws, "selftest DHS-RB-05")
    W.save(WX)
    check("D1", "builder XLSX basal baik tersimpan", os.path.isfile(WX),
          f"{os.path.getsize(WX)} B")
    from openpyxl import load_workbook
    wb = load_workbook(WX)
    c = wb["HASIL UJI"].cell(row=4, column=3)   # kolom angka baris data pertama
    check("D2", "kolom angka workbook MONO rata kanan",
          c.font.name == DX.F_MONO and c.alignment.horizontal == "right",
          f"{c.font.name}/{c.alignment.horizontal}")
    try:
        W.sheet("nama_salah")
        check("D3", "GUARD-N1 menolak nama sheet underscore", False, "tidak raise")
    except CheckDefect:
        check("D3", "GUARD-N1 menolak nama sheet underscore", True)
except ImportError as ex:
    check("D1", "openpyxl tersedia", False, repr(ex))

# ================= E. builder PPTX ==========================================
try:
    import datum_pptx as DP
    WP = os.path.join(HERE, "st-deck.pptx")
    K = DP.DatumDeck(title="Uji Deck DATUM", doc_no="902-GSP-STD-X-2026", rev="A")
    K.title_slide(kicker="uji", deck="satu kalimat")
    s = K.content_slide("Isi slide adalah pernyataan, bukan pertanyaan")
    K.bullet(s, "butir pertama")
    K.table_slide("Tabel uji · kepala dan data",
                  [["Item", "Nilai"], ["A", "1"]], source="selftest DHS-RB-05")
    K.save(WP)
    check("E1", "builder PPTX basal baik tersimpan", os.path.isfile(WP),
          f"{os.path.getsize(WP)} B")
    try:
        K.content_slide("Mengapa deck ini gagal?")
        check("E2", "CEK-04 menolak judul slide pertanyaan", False, "tidak raise")
    except CheckDefect:
        check("E2", "CEK-04 menolak judul slide pertanyaan", True)
except ImportError as ex:
    check("E1", "python-pptx tersedia", False, repr(ex))

# ================= F. embed_fonts ===========================================
try:
    import embed_fonts as EF
    try:
        res = EF.ensure_fonts()
        check("F1", "ensure_fonts trio Plex terdaftar di host", all(res.values()),
              ", ".join(res))
    except EF.FontDefect as ex:
        check("F1", "ensure_fonts trio Plex terdaftar di host", False, str(ex)[:80])
    # arah merah: keluarga khayalan wajib raise
    try:
        EF.ensure_fonts(families=["Nonexistent Face"])
        check("F2", "ensure_fonts hard-fail wajah absen", False, "tidak raise")
    except EF.FontDefect:
        check("F2", "ensure_fonts hard-fail wajah absen", True)
except ImportError as ex:
    check("F1", "embed_fonts terimport", False, repr(ex))

# ================= G. anti-hardcode token ===================================
hard = []
for mod in ("datum_docx.py", "datum_xlsx.py", "datum_pptx.py", "datumcheck.py"):
    src = open(os.path.join(HERE, mod), encoding="utf-8").read()
    body = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    for hexlit in ("101418", "2B3640", "6B7783", "FBFAF7", "FCFCFB", "0563C1",
                   "B45309", "6E1420", "IBM Plex"):
        if hexlit in body:
            hard.append(f"{mod}:{hexlit}")
check("G1", "nol heks/nama font hardcoded di modul builder (token-driven)",
      not hard, "; ".join(hard[:6]))
grep_root = [m for m in ("datum_docx.py", "datum_xlsx.py", "datum_pptx.py",
                         "datumcheck.py", "embed_fonts.py")
             if "/root/.claude" in open(os.path.join(HERE, m), encoding="utf-8").read()]
check("G2", "nol jalur mati /root/.claude di modul baru", not grep_root,
      str(grep_root))

# ================= H. rail chip framePr sah (CTXWIN-1009 t_fcdd32ac) ========
# Dua arah: (H1) keluaran helper wajib memuat w:hAnchor dan TIDAK memuat
# w:anchorH (deterministik tanpa COM); (H2) konstanta bentuk pasca-save token-
# driven; (H3) round-trip Word idempoten atas bentuk kanonis — bersyarat pywin32.
import re as _re
import subprocess as _sp

RAILDOC = os.path.join(HERE, "st-rail.docx")
RL = DD.DatumDocx(title="Selftest Rail Chip DATUM", doc_no="903/GSP/STD/X/2026",
                  rev="A", subject="selftest t_fcdd32ac")
RL.start_interior("UJI RAIL CHIP")
_rp = RL.para("Paragraf uji provenans dengan sitasi [S01].")
RL.rail_host(_rp)
RL.rail_chip("[S01 00:11] SUMBER UJI")
RL.save(RAILDOC)
_fr_pre = _re.findall(r"<w:framePr[^>]*/?>", _doc_xml(RAILDOC))
check("H1", "rail_chip menulis atribut sah w:hAnchor, nol w:anchorH (F CTXWIN-1009)",
      len(_fr_pre) == 1 and 'w:hAnchor="margin"' in _fr_pre[0]
      and "w:anchorH" not in _fr_pre[0],
      _fr_pre[0][:110] if _fr_pre else "framePr tidak ditemukan")
check("H2", "konstanta RAIL_FRAMEPR_POST token-driven == nilai ukur",
      getattr(DD, "RAIL_FRAMEPR_POST", "") ==
      '<w:framePr w:w="%d" w:wrap="none" w:hAnchor="margin" w:x="%d"/>'
      % (DD.RAIL_W_TW, DD.RAIL_X_TW),
      getattr(DD, "RAIL_FRAMEPR_POST", "(konstanta absent)")[:110])
try:
    import win32com.client  # noqa: F401
    _have_com = True
except ImportError:
    _have_com = False
if _have_com:
    _T = os.environ.get("LOCALAPPDATA", "/tmp") + "/Temp/selftest_rail_t_fcdd32ac"
    os.makedirs(_T, exist_ok=True)
    _com = os.path.join(_T, "com_mission.py")
    with open(_com, "w", encoding="utf-8") as f:
        f.write('import sys\nimport win32com.client as wc\n'
                'p = sys.argv[1]\napp = wc.DispatchEx("Word.Application")\n'
                'app.Visible = False\napp.DisplayAlerts = 0\n'
                'doc = app.Documents.Open(p, ReadOnly=False, AddToRecentFiles=False)\n'
                'doc.Repaginate()\n'
                'try:\n    doc.Content.Fields.Update()\nexcept Exception:\n    pass\n'
                'for si in range(1, doc.Sections.Count + 1):\n'
                '    sec = doc.Sections(si)\n'
                '    for fi in (1, 2, 3):\n'
                '        try:\n'
                '            sec.Footers(fi).Range.Fields.Update()\n'
                '            sec.Headers(fi).Range.Fields.Update()\n'
                '        except Exception:\n            pass\n'
                'doc.Repaginate()\n'
                'pages = int(doc.ComputeStatistics(2))\n'
                'doc.Save()\ndoc.Close(False)\napp.Quit()\n'
                'print("PAGES:", pages)\n')
    _rc = _sp.run([sys.executable, _com, RAILDOC], capture_output=True,
                  text=True, timeout=300)
    _fr_post = _re.findall(r"<w:framePr[^>]*/?>", _doc_xml(RAILDOC))
    _canon = getattr(DD, "RAIL_FRAMEPR_POST", "(konstanta absent)")
    check("H3", "round-trip Word: framePr == RAIL_FRAMEPR_POST (bentuk pasca-save)",
          _rc.returncode == 0 and len(_fr_post) == 1
          and _fr_post[0] == _canon,
          (_fr_post[0][:110] if _fr_post else "framePr hilang") +
          f" | rc={_rc.returncode} {(_rc.stderr or '')[:60]}")
else:
    print("CHECK H3: SKIP — pywin32 tidak tersedia di interpreter ini "
          "(cek round-trip bersyarat, bukan FAIL)")

for junk in ("st-baik.docx", "st-jahat.docx", "st-legacy.docx", "st-rail.docx",
             "st-buku.xlsx", "st-deck.pptx"):
    p = os.path.join(HERE, junk)
    if os.path.exists(p):
        os.remove(p)

print("VERDICT: " + ("PASS" if not fails else "FAIL — " + ", ".join(fails)))
sys.exit(0 if not fails else 1)
