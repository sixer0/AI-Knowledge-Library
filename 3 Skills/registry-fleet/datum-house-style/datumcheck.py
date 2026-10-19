# -*- coding: utf-8 -*-
"""
datumcheck.py — guard situs-panggil + audit berkas jadi DATUM v2.0.0
(kelas builder/render DHS-RB-05, 2026-10-05; kartu t_28d93e3c).

PROVENANS: empat guard G1-G3+N1 dan cek ulang 03/04/09/10/16 saat objek dibuat
diambil dari spesifikasi 000 RevA tabel 8.2 (D000:L937, lewat M01 seksi 2.2 yang
diukur ulang 05-10: 4 guard). Limit lebar guard (128/166 mm) dibaca dari
tokens.json grid_mm, bukan hardcoded. Audit berkas jadi (halaman nyata, tautan
aktif-terlihat SPK-002 butir 8, glif daftar hitam U+2014) pola checker garis
check_contoh_datum_short.py + verif_datum_ver04.py. Bukan restorasi Rev J.

Nama modul tanpa garis bawah sesuai DATUM \u00a714 (preseden datumbind.py).

Kelas guard situs-panggil (dipanggil datum_docx saat objek dibuat):
    table_guards(tid, rows, widths_mm)  -> G1 cacah sel, G2 jumlah lebar, G3 teks
    name_guard(name)                    -> N1 underscore pada nama apa pun
    check_heading(text)                 -> cek 04 judul pertanyaan; cek 03 em-dash
    check_value_unit(tok)               -> cek 16 nilai+unit tanpa spasi
    check_source_line(src, ctx)         -> cek 10 baris SUMBER wajib
    figure_guards(caption, h_mm)        -> cek 30 caption + DATUM-33 tinggi figur

Kelas audit berkas jadi (CLI):
    python datumcheck.py <dok.docx> [--pages-com]
      CHECK A1 halaman nyata (Word COM ComputeStatistics(2); tanpa --pages-com
             hanya estimasi dari field cache — dicetak sebagai ESTIMASI)
      CHECK A2 tautan aktif-terlihat: tiap w:hyperlink punya rel eksternal http(s),
             run ber-warna LINK token DAN w:u single (SPK-002 butir 8)
      CHECK A3 glif U+2014 (em dash) nol di seluruh lapisan teks (gerbang A1)
      CHECK A4 properti inti terisi (title/creator/created nyata, epoch nol)
      CHECK A5 updateFields true di settings.xml (G-DQ-12)
      CHECK A6 baterai figur ENH-E pada padanan PDF (overflow/caption/overlap/void)
      CHECK A7 wrap-digit sel tabel: angka bergrup titik terpotong (polA vrf_wrap2)
    exit 0 semua lolos, exit 1 ada cacat (daftar tercetak).

GUARD-G4 (situs-panggil): lantai lebar kolom numerik — setiap kolom yang memuat token
    angka bergrup titik (mis. 335.029.109.47) wajib lebar >= num_floor_mm(token)
    = len(tok)*0,60 em*(skala table_numerals/72*25,4)+2,0 mm. Solver lantai solve_widths()
    dipakai oleh datum_docx.table() bila widths_mm=None; widths_mm eksplisit tetap
    diuji G4. Formula kanonis dari build_rakit.py:226 perkasus DEMSEXP (kartu t_ea2a0ae5).
"""
import json, os, re, sys, zipfile

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from datumbind import tokens_path

_TOK = json.load(open(tokens_path(), encoding="utf-8"))
_GRID = _TOK["grid_mm"]
_COL = _TOK["colour"]
LINK_HEX = _COL["interior"]["link"].lstrip("#").upper()
OK_WIDTHS_MM = (float(_GRID["text_column"]), float(_GRID["full_span"]))  # 128 | 166
TEXT_BLOCK_H_MM = 247.0   # DATUM-33 limit tinggi figur terhadap blok teks A4

# regex cek 16: angka langsung menempel unit huruf (mis. '12mm', '5kg') tanpa
# terpicu oleh pipa tabel markdown (lookbehind mengecualikan '|')
_VALUE_UNIT_RE = re.compile(r"(?<![\\w.,|])\d+(?:[.,]\d+)?(?:mm|cm|km|kg|kW|kVA|Hz|MPa|kPa)\b")
_QUESTION_HEAD_RE = re.compile(r"^(apa|siapa|kapan|di mana|bagaimana|mengapa|kenapa|apakah)\b", re.I)
EM_DASH = "\u2014"

# token angka bergrup titik (335.029.109.47) — dipakai G4 lantai kolom numerik
# dan solver lantai solve_widths(). Satu matcher: build_rakit.py:226 perkasus
# DEMSEXP (kartu t_ea2a0ae5) memakai regex yang sama; jangan duplikasi.
_NUM_TOKEN_RE = re.compile(r"\d{1,3}(?:\.\d{3})+(?:\.\d+)?")

# pola wrap-digit: baris berakhir dengan grup desimal tak lengkap (mis. .47)
_WRAP_RE = re.compile(r"^\d{1,3}(?:\.\d{3}){1,3}\.\d{1,2}$")

# skala table_numerals dari tokens.json (nol pt literal; dihitung sekali di import)
_NUM_PT = float(_TOK["type"]["scale_pt"]["table_numerals"]["size"])
_EM_MM = _NUM_PT / 72.0 * 25.4


def num_floor_mm(tok):
    """Lantai lebar kolom agar token angka DATUM tampil satu baris (L-01).
    Formula kanonis build_rakit.py:226 perkasus DEMSEXP (kartu t_ea2a0ae5):
    Advance mono terukur PDF = 0,599 em/karakter; dipakai batas atas 0,60 em.
    Skala table_numerals dari tokens.json lewat datumbind.tokens_path().
    """
    return len(tok) * 0.60 * _EM_MM + 2.0


def solve_widths(rows, total_mm=128.0):
    """Solver lantai: tiap kolom angka bergrup titik wajib >= num_floor_mm(token
    terpanjangnya). Dipakai datum_docx.table() bila widths_mm=None (satu matcher
    dengan build_rakit.py). widths_mm eksplisit tetap diuji G4, bukan dihitung."""
    rows = [[str(c) for c in r] for r in rows]
    n = len(rows[0])
    maxlen = [max(len(r[i]) for r in rows) for i in range(n)]
    wmin = [max(6.0, ((maxlen[i] / 3.0) - 8) / 2.05 + 0.2) for i in range(n)]
    for i in range(n):
        toks = [t for r in rows for t in _NUM_TOKEN_RE.findall(str(r[i]))]
        if toks:
            wmin[i] = max(wmin[i], max(num_floor_mm(t) for t in toks))
    if sum(wmin) > total_mm:
        f = total_mm / sum(wmin)
        wmin = [w * f for w in wmin]
    rem = total_mm - sum(wmin)
    wt = [max(m_, 4) ** 0.8 for m_ in maxlen]
    s = sum(wt) or 1.0
    w = [wmin[i] + rem * wt[i] / s for i in range(n)]
    w = [round(x, 1) for x in w]
    w[w.index(max(w))] += round(total_mm - sum(w), 1)
    for _ in range(6):
        deficit = False
        for i in range(n):
            toks = [t for r in rows for t in _NUM_TOKEN_RE.findall(str(r[i]))]
            need = max((num_floor_mm(t) for t in toks), default=0.0)
            if need and w[i] + 1e-9 < need:
                j = max(range(n), key=lambda k: w[k])
                if j == i or w[j] <= wmin[j] + 0.1:
                    break
                mv = min(0.5, w[j] - max(wmin[j], w[i] + 0.5))
                if mv <= 0:
                    break
                w[j] = round(w[j] - mv, 1)
                w[i] = round(w[i] + mv, 1)
                deficit = True
        if not deficit:
            break
    return [round(x, 1) for x in w]


def audit_wrap_digit(pdf):
    """CHECK A7: angka DATUM terpotong di sel tabel = baris berakhir '.XX' (grup
    pemisah tak lengkap) PLUS kelanjutan digit tunggal tepat di bawahnya pada
    kolom yang sama (polA vrf_wrap2, kartu t_ea2a0ae5). Kembalikan daftar temuan.
    SKIP mengikuti A6: padanan PDF belum ada -> SKIP; ImportError pymupdf -> SKIP.
    Known-limit: angka SAH berformat grup-titik dengan desimal dua digit (mis.
    rasio/kurs) akan tervonis temuan — register rupiah DATUM Final-4 tidak memuat
    bentuk itu, jadi ambang diterima; bila suatu misi menabraknya, jalurnya
    defect->proposal untuk pengecualian ber-allow-list, bukan pelonggaran global."""
    try:
        import pymupdf
    except ImportError:
        return None  # SKIP
    d = pymupdf.open(pdf)
    hits = []
    for pno, page in enumerate(d, 1):
        lines = []
        for b in page.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for ln in b["lines"]:
                t = "".join(s["text"] for s in ln["spans"]).strip()
                if t:
                    lines.append((ln["bbox"], t))
        for bb, t in lines:
            if _WRAP_RE.match(t):
                cont = [t2 for bb2, t2 in lines
                        if abs(bb2[0] - bb[0]) < 8 and 0 < bb2[1] - bb[3] < 16
                        and re.fullmatch(r"\d{1,2}", t2)]
                hits.append((pno, t, cont))
    return hits


class CheckDefect(Exception):
    """Cacat yangdecidable dari argumen panggilan — berhenti di situs-panggil."""


# ------------------------------------------------------------- guard nama
def name_guard(name):
    """GUARD-N1: garis bawah pada nama berkas/folder/sheet apa pun = cacat."""
    if "_" in name:
        raise CheckDefect(f"GUARD-N1: nama '{name}' memuat garis bawah. "
                          f"Pakai pemisah spasi atau hubung (DATUM \u00a714).")
    return True


# ------------------------------------------------------- guard tabel G1-G3
def table_guards(tid, rows, widths_mm, tol_mm=0.05):
    """G1: setiap baris sama cacah selnya dengan kepala.
    G2: jumlah lebar kolom harus 128 mm atau 166 mm (toleransi 0,05 mm, G-DQ-06).
    G3: teks sel terlalu panjang untuk lebarnya (perkiraan kasar pt/karakter)."""
    if not rows:
        raise CheckDefect(f"{tid}: tabel kosong.")
    n0 = len(rows[0])
    for ri, row in enumerate(rows):
        if len(row) != n0:
            raise CheckDefect(f"GUARD-G1 {tid}: baris {ri+1} memuat {len(row)} sel, "
                              f"kepala {n0} sel. Ratakan sebelum build.")
    tot = sum(widths_mm)
    if min(abs(tot - w) for w in OK_WIDTHS_MM) > tol_mm:
        raise CheckDefect(f"GUARD-G2 {tid}: jumlah lebar kolom {tot:.2f} mm bukan "
                          f"{OK_WIDTHS_MM[0]:.0f} mm maupun {OK_WIDTHS_MM[1]:.0f} mm "
                          f"(grid tokens.json).")
    # G3: ~2.05 karakter per mm pada 8,2 pt condensed (kalibrasi longgar; tujuan =
    # menangkap sel yang jelas jebol kolom, bukan kalkulasi tipografi penuh)
    for ci, w in enumerate(widths_mm):
        cap = int(w * 2.05) + 8
        for ri in range(1, len(rows)):
            txt = str(rows[ri][ci])
            if len(txt) > cap * 3:      # wrap 3 baris maksimum wajar untuk baris data
                raise CheckDefect(f"GUARD-G3 {tid}: teks baris {ri+1} kolom {ci+1} "
                                  f"({len(txt)} char) jauh melebihi lebar {w:.1f} mm.")
    # G4: lantai lebar kolom numerik (L-01 / buta-titik). Setiap kolom yang memuat
    # token angka bergrup titik (335.029.109.47) wajib lebar >= num_floor_mm(token);
    # kolom tanpa token angka bergrup titik dilewati. Formula kanonis
    # (build_rakit.py:226 perkasus DEMSEXP, kartu t_ea2a0ae5).
    for ci, w in enumerate(widths_mm):
        col = [str(rows[ri][ci]) for ri in range(len(rows))]
        toks = [t for cell in col for t in _NUM_TOKEN_RE.findall(cell)]
        if not toks:
            continue
        need = max(num_floor_mm(t) for t in toks)
        if w + 1e-9 < need:
            raise CheckDefect(f"GUARD-G4 {tid}: kolom {ci+1} lebar {w:.1f} mm di bawah "
                              f"lantai token '{max(toks, key=len)}' = {need:.1f} mm. "
                              f"Angka bergrup titik akan wrap-digit (L-01).")
    return True


# ----------------------------------------------------- cek ulang situs-panggil
def check_heading(text):
    """Cek 04: judul berbentuk pertanyaan = cacat (limit 0, M01 DATUM-04)."""
    t = text.strip()
    if t.endswith("?") or _QUESTION_HEAD_RE.match(t):
        raise CheckDefect(f"CEK-04: judul '{t[:60]}' berbentuk pertanyaan. "
                          f"Setiap judul adalah klaim.")
    if EM_DASH in t:
        raise CheckDefect(f"CEK-03: em dash (U+2014) pada judul '{t[:60]}' "
                          f"— nol mutlak di kepala.")
    return True


def check_value_unit(tok):
    """Cek 16: nilai dan unit wajib dipisah spasi (limit 0)."""
    m = _VALUE_UNIT_RE.search(tok)
    if m:
        raise CheckDefect(f"CEK-16: '{m.group(0)}' menempel nilai ke unit tanpa "
                          f"spasi (konvensi numerals tokens.json).")
    return True


def check_source_line(src, ctx):
    """Cek 10/29: tabel/figur tanpa baris SUMBER = cacat."""
    if not src or not str(src).strip():
        raise CheckDefect(f"CEK-10: {ctx} tanpa baris SUMBER. Setiap tabel/figur "
                          f"menunjuk sumbernya.")
    return True


def px_guard(image_path, w_mm):
    """DATUM-39 (ENH-D E-08): px lebar sumber vs lebar tempel wajib >= 150 dpi
    efektif. Kelas cacat lama: figsize memakai mm seolah inci membuat PNG
    3,78x terlalu besar lalu diturunkan Word sampai huruf chart tampil 75%."""
    try:
        from PIL import Image
    except ImportError:
        return True  # tanpa PIL: dilewati jujur, jalur render tetap mengukur F5
    try:
        with Image.open(image_path) as im:
            px_w = im.size[0]
    except Exception:
        return True
    eff_dpi = px_w / (float(w_mm) / 25.4)
    if eff_dpi < 150.0:
        raise CheckDefect(f"DATUM-39/E-08: {os.path.basename(image_path)} {px_w}px "
                          f"untuk {w_mm} mm = {eff_dpi:.0f} dpi efektif < 150. Simpan "
                          f"300 dpi dengan figsize dalam INCI (mm/25,4).")
    return True


def figure_guards(caption, h_mm):
    """Cek 30 (caption wajib) + DATUM-33 (tinggi figur <= blok teks 247 mm)."""
    if not caption or not caption.strip():
        raise CheckDefect("CEK-30: figur tanpa nomor/caption.")
    if float(h_mm) > TEXT_BLOCK_H_MM:
        raise CheckDefect(f"DATUM-33: figur {h_mm} mm lebih tinggi dari blok teks "
                          f"{TEXT_BLOCK_H_MM} mm.")
    return True


# --------------------------------------------------------- audit berkas jadi
def _docx_xml_parts(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        docs = {n: z.read(n).decode("utf-8", "replace")
                for n in names if n.endswith(".xml")}
    return docs


def audit_links(path):
    """SPK-002 butir 8: tiap hyperlink = rel eksternal http(s) + run berwarna
    token LINK + underline single. Kembalikan daftar defect. Semua lapisan
    (document + header/footer) dipindai; r:id apa pun (bukan hanya rIdN) diuji."""
    from docx import Document
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    docs = _docx_xml_parts(path)
    d = Document(path)
    rid_map = {}
    parts = [d.part]
    for sec in d.sections:
        parts += [sec.header.part, sec.footer.part,
                  sec.first_page_header.part, sec.first_page_footer.part,
                  sec.even_page_header.part, sec.even_page_footer.part]
    for part in parts:
        try:
            for rid, rel in part.rels.items():
                if rel.reltype == RT.HYPERLINK:
                    rid_map[rid] = rel.target_ref
        except Exception:
            continue
    defects = []
    n_link = 0
    layer_names = [n for n in docs
                   if n in ("word/document.xml",)
                   or re.match(r"word/(header|footer)\d*\.xml$", n)]
    for lname in layer_names:
        xml = docs[lname]
        for m in re.finditer(r"<w:hyperlink\b([^>]*)>(.*?)</w:hyperlink>",
                             xml, re.S):
            n_link += 1
            attrs, inner = m.group(1), m.group(2)
            rid_m = re.search(r'r:id="([^"]+)"', attrs)
            tgt = None
            if rid_m:
                tgt = rid_map.get(rid_m.group(1))
            label = (rid_m.group(1) if rid_m else lname) 
            if not tgt or not str(tgt).startswith(("http://", "https://")):
                defects.append(f"tautan {label}: tanpa rel eksternal http(s) "
                               f"sah ({tgt!r})")
                continue
            inner_q = inner.replace("'", '"')
            if ('w:color w:val="%s"' % LINK_HEX) not in inner_q:
                defects.append(f"tautan {label} -> {str(tgt)[:50]}: warna run bukan "
                               f"token LINK {LINK_HEX} (mati terasa)")
            if "<w:u " not in inner_q:
                defects.append(f"tautan {label} -> {str(tgt)[:50]}: tanpa garis "
                               f"bawah (SPK-002 butir 8: defect tampil-tautan)")
    return n_link, defects


def audit_em_dash(path):
    docs = _docx_xml_parts(path)
    hits = []
    for n, x in docs.items():
        x2 = x.replace("&amp;", "&")
        cnt = x2.count(EM_DASH)
        if cnt:
            hits.append((n, cnt))
    return hits


def audit_props(path):
    from docx import Document
    cp = Document(path).core_properties
    defects = []
    if not (cp.title or "").strip():
        defects.append("core.title kosong")
    if not (cp.author or "").strip():
        defects.append("core.creator kosong")
    cr = cp.created
    if cr is None or cr.year < 2020:
        defects.append(f"core.created epoch/tidak nyata: {cr}")
    return defects


def audit_update_fields(path):
    docs = _docx_xml_parts(path)
    s = docs.get("word/settings.xml", "")
    if 'w:updateFields' not in s:
        return False
    # posisi skema: updateFields harus sebelum w:compat agar tidak dibuang Word
    i_uf, i_cp = s.find('w:updateFields'), s.find('w:compat')
    return i_cp == -1 or i_uf < i_cp


def page_count_com(path, timeout_note=""):
    """Halaman NYATA lewat Word COM (alat nyata, bukan perkiraan).
    Pitfall warisan: buka ReadOnly=False, AddToRecentFiles=False; Close(False).
    Return (pages:int|None, error:str|None)."""
    try:
        import win32com.client
    except Exception as ex:
        return None, f"pywin32 tidak tersedia: {ex!r}"
    app = None
    try:
        app = win32com.client.DispatchEx("Word.Application")
        app.Visible = False
        app.DisplayAlerts = 0
        doc = app.Documents.Open(os.path.abspath(path), ReadOnly=False,
                                 AddToRecentFiles=False)
        try:
            doc.Repaginate()
            for si in range(1, doc.Sections.Count + 1):
                sec = doc.Sections(si)
                for fi in range(1, 4):
                    try:
                        sec.Footers(fi).Range.Fields.Update()
                    except Exception:
                        pass
            doc.Repaginate()
            pages = int(doc.ComputeStatistics(2))   # wdStatisticPages
        finally:
            doc.Close(False)
        return pages, None
    except Exception as ex:
        return None, repr(ex)
    finally:
        if app is not None:
            try:
                app.Quit()
            except Exception:
                pass


def run_cli(argv):
    if not argv:
        print(__doc__)
        return 0
    path = argv[0]
    want_com = "--pages-com" in argv
    rc = 0
    fails = []

    def report(n, ok, nama, detail=""):
        nonlocal rc
        tag = "PASS" if ok else "FAIL"
        if not ok:
            rc = 1; fails.append(nama)
        print(f"CHECK {n}: {tag} — {nama}" + (f" | {detail}" if detail else ""))

    n_link, link_def = audit_links(path)
    report("A2", not link_def, f"tautan aktif-terlihat ({n_link} tautan)",
           "; ".join(link_def[:6]))
    hits = audit_em_dash(path)
    report("A3", not hits, "em dash U+2014 nol semua lapisan XML",
           str(hits[:4]))
    dp = audit_props(path)
    report("A4", not dp, "properti inti nyata", "; ".join(dp))
    report("A5", audit_update_fields(path), "settings.xml updateFields=true (G-DQ-12)")
    # CHECK A6 (ENH-E): baterai figur pada padanan PDF terbit; rilis diblokir bila >0
    pdf = path.rsplit(".", 1)[0] + ".pdf"
    if os.path.exists(pdf):
        try:
            import datum_figur
            res, err = datum_figur.battery(pdf)
            if err:
                report("A6", False, "baterai figur ENH-E pada PDF terbit", err)
            else:
                d = res["defects"]
                detail = ("figur=%d overflow=%s caption=%d/%d overlap=%d void=%d"
                          % (res["figures"], res["overflow_pages"] or "0",
                             res["caption_ok"], res["caption_total"],
                             len(res["overlap"]), res["void_pages"] or 0))
                report("A6", d == 0, "baterai figur ENH-E pada PDF terbit",
                       detail + ("" if d == 0 else " | DEFECTS=%d" % d))
        except ImportError:
            print("CHECK A6: SKIP — pymupdf tidak tersedia untuk baterai figur")
    else:
        print("CHECK A6: SKIP — padanan PDF belum ada (render lalu jalankan ulang; "
              "void galeri dideklarasikan via datum_figur.py --allow-void)")
    # CHECK A7 (L-01): wrap-digit sel tabel — angka bergrup titik terpotong
    if os.path.exists(pdf):
        hits = audit_wrap_digit(pdf)
        if hits is None:
            print("CHECK A7: SKIP — pymupdf tidak tersedia")
        else:
            report("A7", len(hits) == 0,
                   "wrap-digit sel tabel (angka bergrup titik terpotong)",
                   f"temuan={len(hits)}" + ("" if not hits else " | " + "; ".join(
                       f"{t} (h. {c})" for _, t, c in hits[:4])))
    else:
        print("CHECK A7: SKIP — padanan PDF belum ada (render lalu jalankan ulang)")
    if want_com:
        pages, err = page_count_com(path)
        report("A1", pages is not None and pages > 0,
               "jumlah halaman nyata (Word COM)",
               f"pages={pages}" if pages else f"error: {err}")
    else:
        print("CHECK A1: SKIP — halaman nyata butuh --pages-com (Word COM)")
    print("VERDICT: " + ("PASS" if rc == 0 else "FAIL — " + ", ".join(fails)))
    return rc


if __name__ == "__main__":
    sys.exit(run_cli(sys.argv[1:]))
