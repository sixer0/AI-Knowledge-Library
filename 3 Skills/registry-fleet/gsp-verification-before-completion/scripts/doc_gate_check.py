#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""doc_gate_check.py - GERBANG deterministik artefak dokumen (.xlsx/.docx) lane verifier fleet GSP.

Kelas cacat: F1 kesalahan data tabel, F2 hyperlink/rel belum aktif atau rusak, F3 URL hidup tapi
tidak relevan dengan entitas barisnya. Lahir dari misi VERIF-GATE-0904 (rubric R1-R3 terkunci);
provenansi lengkap ada di references/document-artifact-verification.md pada skill yang sama.

DEVIASI bernama DEV-C01 (syarat pemblokir C-01 SKILL-DECISION.md): lapisan transport TIDAK disalin
verbatim. Fungsi warisan gate_accuracy_100.py memakai urlopen tanpa header Accept-Encoding dan tanpa
dekompresi, sehingga pada server yang memaksa gzip (terukur 04-09: www.python.org status=200
content-encoding=gzip magic 1f8b, <title> hanya terbaca setelah gunzip) sinyal title/OG/body selalu
nol dan entitas yang benar bisa divonis SALAH-TARGET. Skrip ini mengirim Accept-Encoding: gzip,
deflate, membaca header Content-Encoding, mendekompresi gzip/deflate sebelum ekstraksi judul/OG/isi,
lalu mencatat content_encoding serta panjang hasil dekompresi pada bukti. Selain transport, logika
STOP/norm/name_tokens/abs_url/dom_of/entity_match disalin VERBATIM dari skrip gerbang akurasi P4
(gate_accuracy_100.py) sesuai D-TA-07. Skrip ini TIDAK memuat path misi apa pun: seluruh path dan
kolom datang dari argumen CLI/config (P-A).

DEVIASI bernama DEV-DTA04 (penyelarasan D-TA-04 dengan ambang warisan D-TA-07): vonis BENAR memakai
aturan warisan (host_hit OR title_hit OR seq_hit OR body_hits>=2), lalu entitas dengan tepat 1 sinyal
dinaikkan menjadi NEEDS_REVIEW berdasar D-TA-04 ("1 sinyal = NEEDS_REVIEW dengan bukti, bukan lulus
diam-diam"). 0 sinyal = SALAH-TARGET (pemblokir).

Semantik pemblokir (D-TA-04, turunan Decision Log D-02): PEMBLOKIR = temuan F1 apa pun, cacat
struktur rel F2b, SALAH-TARGET F3 > 0, crash. CATATAN (tidak memblokir, masuk notes_register.csv) =
MATI, HTTP4XX, REDIRECT-SILANG, KOSONG, entity-context tidak tersedia. 1 sinyal = NEEDS_REVIEW.

Pustaka: stdlib + openpyxl + python-docx. Pola jalan yang didukung fleet:
  uv run --python 3.11 --with openpyxl --with python-docx python doc_gate_check.py \
      --target <file.xlsx|file.docx> --outdir <dir> [--mode gate|fixture] [--expect manifest.json]
Exit code (D-TA-05): 0 PASS, 2 FAIL, 3 NEEDS_REVIEW, 1 error/crash. Crash tidak pernah exit 0.
"""
import argparse
import csv
import gzip
import hashlib
import io
import json
import os
import posixpath
import re
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from xml.etree import ElementTree as ET

VERSION = "1.2.0"
UA = "GSP-DocGate/1.0 (+kontak ops@gspsp.co.id)"

# ---------------------------------------------------------------- warisan gate_accuracy_100.py (VERBATIM, D-TA-07)
STOP = {"co", "ltd", "limited", "inc", "corp", "corporation", "company", "the", "group", "and",
        "technologies", "technology", "tech", "systems", "system", "solution", "solutions",
        "shanghai", "beijing", "china", "chinese", "international", "industries", "industry",
        "holding", "holdings", "development", "developments", "engineering", "science", "sciences"}


def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())


def name_tokens(n):
    quoted = re.findall(r"[\"'\u2018\u2019\u201c\u201d\u00ab]([A-Za-z0-9 .&-]{2,20})[\"'\u2018\u2019\u201c\u201d\u00bb]", n or "")
    qtoks = [t for q in quoted for t in norm(q).split() if len(t) > 1]
    ts = [t for t in norm(n).split() if len(t) > 2 and t not in STOP]
    ts = qtoks + [t for t in ts if t not in qtoks]
    return ts[:8] or [t for t in norm(n).split() if len(t) > 2][:8]


def abs_url(v):
    x = (v or "").strip()
    if not x:
        return None
    if not x.startswith(("http://", "https://")):
        x = "https://" + x
    return x


def dom_of(u):
    return re.sub(r"^www\.", "", re.sub(r"https?://", "", u or "").split("/")[0]).lower()


def entity_match(name, url, status, final_url, body):
    ts = name_tokens(name)
    short = [t for t in norm(name).split() if 2 < len(t) <= 4 and t not in STOP]
    ts = ts + [t for t in short if t not in ts]
    if not ts:
        return False, {"no_tokens": True}
    dom = dom_of(url)
    fdom = dom_of(final_url)
    flat_dom = dom.replace("-", "").replace(".", "").replace("_", "")
    flat_fdom = fdom.replace("-", "").replace(".", "").replace("_", "")

    def _dom_ok(t):
        s = t.replace(" ", "")
        if len(s) > 4:
            return s in flat_dom or s in flat_fdom
        labels = [x for x in re.split(r"[.-]", dom_of(url) + " " + dom_of(final_url)) if x]
        return any(x == s or x.startswith(s) or s in x.split("-") for x in labels)

    host_hit = any(_dom_ok(t) for t in ts)
    try:
        text = body.decode("utf-8", "ignore").lower()
    except Exception:
        text = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S)
    title = norm(m.group(1)) if m else ""
    og = re.search(r'og:title[^>]*content="([^"]+)"', text)
    og_t = norm(og.group(1)) if og else ""
    body_flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))[:80_000]
    title_hit = any((t in title or t in og_t) for t in ts if len(t) > 3) or any(
        (" " + t + " ") in (" " + title + " ") or (" " + t + " ") in (" " + og_t + " ") for t in ts if len(t) <= 4)
    two = [t for t in norm(name).split() if len(t) == 2]
    title_hit = title_hit or any((" " + t + " ") in (" " + title + " ") or (" " + t + " ") in (" " + og_t + " ") for t in two)
    seq = " ".join(ts[:2])
    seq_hit = len(ts) >= 2 and (seq in title or seq in og_t or seq in body_flat[:20_000])
    body_hits = sum(1 for t in ts if len(t) > 3 and t in body_flat)
    ok = host_hit or title_hit or seq_hit or body_hits >= 2
    return ok, {"host_hit": host_hit, "title_hit": title_hit, "seq_hit": seq_hit, "body_hits": body_hits,
                "final_dom": fdom[:60], "title": title[:70]}


def signal_count(sig):
    """Jumlah sinyal entitas yang menyala (dipakai untuk lapis NEEDS_REVIEW DEV-DTA04)."""
    if not sig or sig.get("no_tokens"):
        return 0
    n = 0
    if sig.get("host_hit"):
        n += 1
    if sig.get("title_hit"):
        n += 1
    if sig.get("seq_hit"):
        n += 1
    if (sig.get("body_hits") or 0) >= 2:
        n += 1
    return n


# ---------------------------------------------------------------- transport (DEV-C01)
def fetch(url, timeout=18):
    """Return dict(status, final_url, body, content_encoding, raw_len, decoded_len)."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en;q=0.8,id;q=0.6,zh;q=0.4",
    })
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        raw = r.read(150_000)
        ce = (r.headers.get("Content-Encoding") or "").lower()
        status, final = r.status, r.geturl()
    raw_len = len(raw)
    decoded = raw
    note = ""
    if "gzip" in ce or raw[:2] == b"\x1f\x8b":
        try:
            decoded = gzip.decompress(raw)
            note = "gunzip"
        except Exception as e:
            note = "gunzip_gagal:" + type(e).__name__
    elif "deflate" in ce or raw[:2] == b"\x78\x9c" or raw[:2] == b"\x78\xda":
        try:
            decoded = zlib.decompress(raw, -zlib.MAX_WBITS)
            note = "inflate"
        except Exception:
            try:
                decoded = zlib.decompress(raw)
                note = "zlib"
            except Exception as e:
                note = "inflate_gagal:" + type(e).__name__
    return {"status": status, "final_url": final, "body": decoded, "content_encoding": ce,
            "raw_len": raw_len, "decoded_len": len(decoded), "decode_note": note}


# ---------------------------------------------------------------- util
URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>\"'\)\]\}>]+", re.I)
PLACEHOLDER_RES = [
    (re.compile(r"^#(REF|N/A|VALUE!|DIV/0!|NAME\?|NULL!|NUM!)", re.I), "sentinel_error_excel"),
    (re.compile(r"^\[object [A-Za-z]+\]$", re.I), "js_object_stringified"),
    (re.compile(r"^(None|nan|NaN|NULL|null|undefined|NaT)$"), "python_null_leak"),
    (re.compile(r"^\s*(lorem ipsum|placeholder|tbd|to be determined|todo|n/a - isi)\s*$", re.I), "placeholder_text"),
]
# Slot pengisi (template_slot): HANYA kurung siku whose ISI adalah frasa penanda pengisian
# utuh ('[isi]', '[wajib diisi]', '[isi] ...prosa...'). Preseden t_b0cf1dc7 (VERDICT VGV-T1
# akar-2): pola substring '(isi|fill|insert|wajib)' menelan anotasi data sah
# '[validated=YES; source=boo-vision.com]' (substring 'isi' dalam 'vision'/'vegvisir')
# -> 11 positif palsu F1d pada expo26. Anotasi ber-'='/';'/'source=' bukan slot.
FILL_INNER_RE = re.compile(
    r"^(?:wajib\s+)?(?:isi|diisi|fill(?:ed)?(?:\s+here)?|insert(?:\s+here)?|todo|tbd"
    r"|placeholder|ganti(?:\s+dengan\s+\S{1,15})?|lorem\s+ipsum|x{3,}|y{3,})$", re.I)
BRACKET_SEG_RE = re.compile(r"\[([^\]\[]{1,40})\]")


def placeholder_rule(s):
    """Nama aturan placeholder untuk satu teks sel/paragraf; None bila bersih. Deterministik."""
    for rx, rule in PLACEHOLDER_RES:
        if rx.search(s):
            return rule
    for inner in BRACKET_SEG_RE.findall(s):
        if FILL_INNER_RE.match(inner.strip()):
            return "template_slot"
    return None
TOTAL_HDR_RE = re.compile(r"(^|\b)(total|jumlah|subtotal|grand\s*total)\b", re.I)
TOTAL_LABEL_RE = re.compile(r"^\s*(total|subtotal|jumlah|grand\s*total|jumlah\s*keseluruhan|total\s*keseluruhan)\b", re.I)
# D-03 (kartu t_39db5b93, pasca VERDICT-R2/COUNTERSIGN-R2): label-total dibagi dua tier.
# TOTAL_LABEL_RE di atas TETAP dipakai untuk batas blok & skip heuristic (konservatif);
# keputusan "baris ini diuji sebagai penjumlah" memakai total_label_tier() di bawah.
# Nama seksi enumerasi ('Total enam sheet pendalaman' - preseden B10 expo26) adalah
# agregat lintas-sheet, bukan penjumlah blok tetangga; disambiguasi leksikal murni tidak
# cukup karena preseden B70 ('Total delapan sheet pendalaman') MEMANG penjumlah blok ->
# tier ambiguous tetap DIUJI dua arah, hanya vonis ketidakcocokan diturunkan ke CATATAN.
ENUM_SECTION_RE = re.compile(
    r"^\s*(?:total|subtotal|jumlah|grand\s*total)\s+"
    r"(?:satu|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|sepuluh|sebelas|"
    r"dua\s+belas|seratus|\d{1,4})\s+\S", re.I)


def total_label_tier(label):
    """Tier label-total per keputusan controller D-03: 'strict' | 'ambiguous' | None.

    strict    = label generik ('Total', 'Total Biaya', 'SUBTOTAL', 'Total (netto)') ->
                ketidakcocokan dua arah tetap FAIL pemblokir.
    ambiguous = nama seksi enumerasi ('Total <kata-bilangan> <benda>') -> ketidakcocokan
                dua arah turun ke CATATAN NEEDS_REVIEW non-pemblokir (D-03 B/C).
    """
    if not TOTAL_LABEL_RE.search(label or ""):
        return None
    if ENUM_SECTION_RE.match(label or ""):
        return "ambiguous"
    return "strict"

PCT_HDR_RE = re.compile(r"(%|persen|pct|percent)", re.I)
NAME_HDR_RE = re.compile(r"(name|exhibitor|entitas|perusahaan|company|nama|peserta)", re.I)
URL_HDR_RE = re.compile(r"(website|\burl\b|\bsite\b|situs|homepage|tautan|taut|\blink\b)", re.I)
KEY_HDR_RE = re.compile(r"^(no|no\.|nomor|id|item|kode)\b", re.I)


def parse_num(v, dot_thousands=False):
    """Parse angka deterministik dari sel/teks. Return float atau None.

    dot_thousands=True dipakai ketika kolom/sheet menunjukkan pola ribuan bertitik (mis.
    '10.011.972.125' gaya Indonesia), sehingga '2.450' dibaca 2450 bukan 2.45. Pola >=2 kelompok
    tiga digit sudah pasti ribuan dan dikenali tanpa flag.
    """
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if not s:
        return None
    s = re.sub(r"(?i)^(rp|usd|\$|eur|idr)\s*", "", s)
    s = re.sub(r"(?i)\s*(rp|idr)\s*$", "", s)
    s = s.replace("%", "").replace("\u00a0", " ").strip()
    if re.fullmatch(r"-?[\d.,]+", s) is None:
        return None
    neg = s.startswith("-")
    s = s.lstrip("-")
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")     # desimal koma (gaya Indonesia)
        else:
            s = s.replace(",", "")                        # desimal titik (gaya Inggris)
    elif "," in s:
        head, _, tail = s.rpartition(",")
        if head and len(tail) in (1, 2) and "," not in head:
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "." in s:
        groups = s.split(".")
        if len(groups) > 2 and all(len(g) == 3 for g in groups[1:]):
            s = s.replace(".", "")                        # 10.011.972 -> ribuan bertitik
        elif len(groups) == 2 and len(groups[1]) == 3 and dot_thousands:
            s = s.replace(".", "")                        # 2.450 ikut pola kolom ribuan
    try:
        f = float(s)
    except ValueError:
        return None
    return -f if neg else f


DOT_THOUSANDS_RE = re.compile(r"\b\d{1,3}(?:\.\d{3}){2,}\b")


def col_dot_thousands(rows):
    """Deteksi pola ribuan bertitik pada sekumpulan nilai (deterministik, tanpa tebak locale)."""
    for vals in rows:
        for v in vals:
            if isinstance(v, str) and DOT_THOUSANDS_RE.search(v):
                return True
    return False


def close_enough(a, b):
    return abs(a - b) <= max(0.01, abs(b) * 0.005)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- model
class Finding(object):
    def __init__(self, check, cls, location, desc):
        self.check = check
        self.cls = cls
        self.location = location
        self.desc = desc


class Note(object):
    def __init__(self, kind, location, detail):
        self.kind = kind
        self.location = location
        self.detail = detail


class UrlRec(object):
    def __init__(self, source, loc, url, name="", key=""):
        self.source = source      # xlsx-cell | xlsx-rel | docx-hyperlink | docx-rel | plain-text
        self.loc = loc            # alamat presisi (Sheet!B7 / docx:part#element)
        self.url = url
        self.name = name          # konteks entitas (kosong bila tidak ada)
        self.key = key
        self.verdict = ""         # HIDUP | MATI | HTTP4XX | SKIP-NET
        self.status = ""
        self.final_url = ""
        self.entity = ""          # BENAR | SALAH-TARGET | NEEDS_REVIEW | TANPA_NAMA | SKIP-NET
        self.sig = {}


class RelRec(object):
    def __init__(self, part, rid, target, mode, rtype):
        self.part = part
        self.rid = rid
        self.target = target
        self.mode = mode
        self.type = rtype


class Doc(object):
    def __init__(self, path):
        self.path = path
        self.ext = os.path.splitext(path)[1].lower()
        self.fmt = self.ext.lstrip(".")
        self.read_error = ""
        self.sheets = []          # [{name, header_row, headers:[], records:[{row, addr:{}, values:{}}]}]
        self.urls = []
        self.rels = []
        self.placeholders = []    # [(loc, value, rule)]
        self.raw_tokens = {}      # statistik mentah utk gerbang kelengkapan
        self.records_total = 0
        self.empty_fields = []    # [(loc, field)] -> KOSONG
        self.notes_extra = []


# ---------------------------------------------------------------- XLSX reader
NS_MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NS_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NS_PKGREL = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _xlsx_sheet_partmap(z):
    """nama sheet -> (path part worksheet, path part rels-nya) lewat workbook.xml + rels."""
    wb_rels = {}
    if "xl/_rels/workbook.xml.rels" in z.namelist():
        root = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        for r in root.findall(NS_PKGREL + "Relationship"):
            tgt = r.get("Target") or ""
            if tgt.startswith("/"):
                tgt = tgt.lstrip("/")
            elif not tgt.startswith("xl/"):
                tgt = "xl/" + tgt.lstrip("./")
            wb_rels[r.get("Id")] = (tgt, r.get("Type", ""), r.get("TargetMode", ""))
    out = []
    if "xl/workbook.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/workbook.xml"))
        for sh in root.iter(NS_MAIN + "sheet"):
            nm = sh.get("name")
            rid = sh.get(NS_REL + "id")
            part = wb_rels.get(rid, (None, "", ""))[0]
            if part:
                # posixpath: nama entri zip SELALU pakai garis miring; os.path.join di Windows
                # menghasilkan backslash -> lookup rels gagal senyap -> semua hyperlink salah vonis dangling
                out.append((nm, part, posixpath.join(posixpath.dirname(part), "_rels",
                                                      posixpath.basename(part) + ".rels")))
    return out


def read_xlsx(path, doc):
    import openpyxl
    wb = None
    errs = []
    nolink = False
    for kw in ({"data_only": True}, {"data_only": True, "keep_links": False},
               {"data_only": True, "read_only": True}):
        try:
            wb = openpyxl.load_workbook(path, **kw)
            nolink = not kw.get("keep_links", True)
            break
        except Exception as e:
            errs.append("%s(%s): %s" % (type(e).__name__, ",".join(kw), e))
    if wb is None:
        # openpyxl bisa gagal pada rel rusak (KeyError rId). Jalur XML (zipfile) tetap jalan untuk
        # F2a/F2b, tetapi dump sel F1 tidak tersedia -> dicatat sebagai kegagalan keutuhan baca.
        doc.read_error = "openpyxl gagal memuat workbook (%s)" % " | ".join(errs)
    if nolink:
        doc.notes_extra.append(("pustaka", "openpyxl", "muat dengan keep_links=False karena rel rusak: %s" % errs[-1]))
    z = zipfile.ZipFile(path)
    partmap = _xlsx_sheet_partmap(z)
    part_by_name = {nm: (p, rp) for nm, p, rp in partmap}
    hidden = set()
    try:
        wroot = ET.fromstring(z.read("xl/workbook.xml"))
        for sh in wroot.iter(NS_MAIN + "sheet"):
            if (sh.get("state") or "") in ("hidden", "veryHidden"):
                hidden.add(sh.get("name"))
    except Exception:
        pass
    doc.raw_tokens["hidden_sheets"] = sorted(hidden)

    # hyperlink mentah per part worksheet + rels per part
    raw_hyper = 0
    for nm, (part, relpart) in part_by_name.items():
        rels = {}
        if relpart in z.namelist():
            try:
                rroot = ET.fromstring(z.read(relpart))
                for r in rroot.findall(NS_PKGREL + "Relationship"):
                    rec = RelRec(relpart, r.get("Id"), r.get("Target") or "", r.get("TargetMode") or "", r.get("Type") or "")
                    doc.rels.append(rec)
                    rels[r.get("Id")] = rec
            except ET.ParseError as e:
                doc.rels.append(RelRec(relpart, "-", "XML_PARSE_ERROR:%s" % e, "", ""))
        if part not in z.namelist():
            continue
        xtext = z.read(part).decode("utf-8", "ignore")
        raw_hyper += len(re.findall(r"<hyperlink\b", xtext))
        for m in re.finditer(r"<hyperlink\b([^>]*)/?>", xtext):
            attrs = dict(re.findall(r'(\w+(?::\w+)?|r:id)="([^"]*)"', m.group(1)))
            ref = attrs.get("ref", "")
            rid = attrs.get("r:id") or attrs.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id") or ""
            tgt = attrs.get("location", "")
            rl = rels.get(rid)
            target = (rl.target if rl else None) or tgt
            doc.urls.append(UrlRec("xlsx-cell", "%s!%s" % (nm, ref or rid), target or "(REL_HILANG:%s)" % rid))
            if rl is None and not tgt:
                doc.rels.append(RelRec(part, rid, "(DANGLING: rId dirujuk sel tapi tiada di rels)", "", ""))
    doc.raw_tokens["xlsx_hyperlink_tags"] = raw_hyper

    # nilai sel + hyperlink objek openpyxl (cross-check kelengkapan; lewati bila wb None/keep_links=False)
    op_hyper = []
    if wb is not None and not nolink:
        for sn in wb.sheetnames:
            ws = wb[sn]
            for row in ws.iter_rows():
                for c in row:
                    hl = getattr(c, "hyperlink", None)   # ReadOnlyCell tidak punya atribut hyperlink
                    if hl is not None and getattr(hl, "target", None):
                        op_hyper.append(("%s!%s" % (sn, getattr(c, "coordinate", "?")), hl.target))
    doc.raw_tokens["openpyxl_cell_hyperlinks"] = len(op_hyper)
    doc.raw_tokens["openpyxl_cell_hyperlink_targets"] = sorted({t for _, t in op_hyper})

    # URL polos dalam teks sel
    if wb is not None:
        for sn in wb.sheetnames:
            for row in wb[sn].iter_rows(values_only=False):
                for c in row:
                    if isinstance(c.value, str):
                        for u in URL_RE.findall(c.value):
                            doc.urls.append(UrlRec("plain-text", "%s!%s" % (sn, c.coordinate), u.rstrip(".,;")))

    # rekaman tabel (header + baris data) per sheet
    if wb is not None:
        for sn in wb.sheetnames:
            ws = wb[sn]
            grid = []
            for r_i, row in enumerate(ws.iter_rows(values_only=False), start=1):
                grid.append([(c.coordinate, c.value) for c in row])
                if r_i >= 20000:
                    break
            doc.sheets.append({"name": sn, "grid": grid, "hidden": sn in hidden})

    # placeholder scan semua sel
    if wb is not None:
        for sn in wb.sheetnames:
            for row in wb[sn].iter_rows():
                for c in row:
                    if c.value is None:
                        continue
                    s = str(c.value).strip()
                    if not s:
                        continue
                    rule = placeholder_rule(s)
                    if rule:
                        doc.placeholders.append(("%s!%s" % (sn, c.coordinate), s[:60], rule))
    if wb is not None:
        wb.close()
    z.close()


# ---------------------------------------------------------------- DOCX reader
W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def _docx_parts(z):
    parts = []
    for n in z.namelist():
        if re.fullmatch(r"word/(document|header\d*|footer\d*)\.xml", n):
            parts.append(n)
    return sorted(parts)


def _rels_for(z, part):
    rp = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
    out = {}
    if rp in z.namelist():
        try:
            root = ET.fromstring(z.read(rp))
            for r in root.findall(NS_PKGREL + "Relationship"):
                out[r.get("Id")] = RelRec(rp, r.get("Id"), r.get("Target") or "", r.get("TargetMode") or "", r.get("Type") or "")
        except ET.ParseError as e:
            out["(PARSE_ERROR)"] = RelRec(rp, "-", "XML_PARSE_ERROR:%s" % e, "", "")
    return out, rp


def _wtext(el):
    return "".join(t.text or "" for t in el.iter(W_NS + "t"))


def _docx_cellmap(root, part):
    """Peta id(elemen w:p / w:hyperlink) -> alamat sel 'docx:tabelN!rR/cC' untuk tabel tingkat
    tubuh (penomoran sama dengan urutan python-docx: anak langsung w:body). Paragraf di dalam
    tabel kini beralamat sel, bukan indeks paragraf global (koreksi manifest t_b0cf1dc7).
    Keterbatasan: tabel bersarang memakai alamat sel tabel terluar."""
    out = {}
    if part != "word/document.xml":
        return out
    body = root.find(W_NS + "body")
    if body is None:
        return out
    ti = 0
    for el in body:
        if el.tag != W_NS + "tbl":
            continue
        ti += 1
        ri = 0
        for tr in el.findall(W_NS + "tr"):
            ri += 1
            ci = 0
            for tc in tr.findall(W_NS + "tc"):
                ci += 1
                addr = "docx:tabel%d!r%d/c%d" % (ti, ri, ci)
                for subel in tc.iter():
                    if subel.tag in (W_NS + "p", W_NS + "hyperlink"):
                        out.setdefault(id(subel), addr)
    return out


def read_docx(path, doc):
    try:
        z = zipfile.ZipFile(path)
    except Exception as e:
        doc.read_error = "%s: %s" % (type(e).__name__, e)
        return
    parts = _docx_parts(z)
    doc.raw_tokens["docx_parts"] = parts
    n_hlink_tags = 0
    n_ext_rels = 0
    for part in parts:
        if part not in z.namelist():
            continue
        rels, rp = _rels_for(z, part)
        for rid, rec in sorted(rels.items()):
            doc.rels.append(rec)
            if (rec.mode or "").lower() == "external":
                n_ext_rels += 1
                if re.match(r"https?://", rec.target or "", re.I):
                    doc.urls.append(UrlRec("docx-rel", "%s#%s" % (part, rid), rec.target))
        try:
            root = ET.fromstring(z.read(part))
        except ET.ParseError as e:
            doc.rels.append(RelRec(part, "-", "XML_PARSE_ERROR:%s" % e, "", ""))
            continue
        cellmap = _docx_cellmap(root, part)
        for el in root.iter(W_NS + "hyperlink"):
            n_hlink_tags += 1
            rid = el.get(R_NS + "id") or ""
            tgt = el.get(W_NS + "href") or ""
            txt = _wtext(el)
            rl = rels.get(rid)
            target = (rl.target if rl else None) or tgt
            loc = cellmap.get(id(el)) or "%s#hyperlink[%s]" % (part, rid or txt[:24] or "anon")
            if not rl and not tgt:
                doc.rels.append(RelRec(part, rid or "(tanpa r:id)", "(DANGLING: hyperlink tanpa target)", "", ""))
            if target:
                doc.urls.append(UrlRec("docx-hyperlink", loc, target))
        # teks paragraf + tabel
        paras = [(_wtext(p), p) for p in root.iter(W_NS + "p")]
        for txt, _p in paras:
            ploc = cellmap.get(id(_p)) or ("%s#paragraf" % part)
            for u in URL_RE.findall(txt or ""):
                doc.urls.append(UrlRec("plain-text", ploc, u.rstrip(".,;")))
    doc.raw_tokens["docx_hyperlink_tags"] = n_hlink_tags
    doc.raw_tokens["docx_external_rels"] = n_ext_rels

    # tabel via python-docx (kenyamanan; ekstraksi rel/URL sudah lewat XML mentah)
    try:
        import docx
        d = docx.Document(path)
        tables = d.tables
    except Exception as e:
        doc.notes_extra.append(("pustaka", "python-docx", "%s: %s" % (type(e).__name__, e)))
        tables = []
    ti = 0
    for t in tables:
        ti += 1
        grid = []
        for ri, row in enumerate(t.rows, start=1):
            cells = []
            for ci, cell in enumerate(row.cells, start=1):
                cells.append(("r%d/c%d" % (ri, ci), cell.text))
            grid.append(cells)
        doc.sheets.append({"name": "docx:tabel%d" % ti, "grid": grid, "hidden": False})
    # placeholder scan teks seluruh paragraf
    for part in parts:
        if part not in z.namelist():
            continue
        try:
            root = ET.fromstring(z.read(part))
        except ET.ParseError:
            continue
        cellmap = _docx_cellmap(root, part)  # parse ulang -> id elemen baru, peta WAJIB dibangun ulang
        for i, p in enumerate(root.iter(W_NS + "p"), start=1):
            s = (_wtext(p) or "").strip()
            if not s:
                continue
            rule = placeholder_rule(s)
            if rule:
                loc = cellmap.get(id(p)) or ("%s#paragraf%d" % (part, i))
                doc.placeholders.append((loc, s[:60], rule))
    z.close()


# ---------------------------------------------------------------- analisis F1
def resolve_columns(headers, args):
    """Return (idx_name, idx_url, idx_keys, keys_mode) berbasis argumen atau heuristik.

    keys_mode: explicit | header | fallback-name (fallback ke kolom nama = perlu review)."""
    low = {i: (h or "") for i, h in enumerate(headers)}

    def by_name(spec):
        if spec is None:
            return None
        s = str(spec).strip()
        if s.isdigit():
            i = int(s) - 1
            return i if 0 <= i < len(headers) else None
        for i, h in low.items():
            if norm(h) == norm(s):
                return i
        for i, h in low.items():
            if s.lower() in (h or "").lower():
                return i
        return None

    idx_name = by_name(args.name_col) or by_name(args.entity_col)
    if idx_name is None:
        for i, h in low.items():
            if NAME_HDR_RE.search(h or ""):
                idx_name = i
                break
    idx_url = by_name(args.url_col)
    if idx_url is None:
        for i, h in low.items():
            if URL_HDR_RE.search(h or ""):
                idx_url = i
                break
    idx_keys = []
    for spec in (args.key_col or []):
        i = by_name(spec)
        if i is not None:
            idx_keys.append(i)
    keys_mode = "explicit" if idx_keys else ""
    if not idx_keys:
        idx_keys = [i for i, h in low.items() if KEY_HDR_RE.match((h or "").strip())]
        if idx_keys:
            keys_mode = "header"
    if not idx_keys and idx_name is not None:
        idx_keys = [idx_name]
        keys_mode = "fallback-name"   # fallback BUTA -> ditandai, lihat F1c
    return idx_name, idx_url, idx_keys, keys_mode


def find_header_row(grid, args):
    if args.header_row:
        return min(args.header_row, len(grid)) - 1 if grid else 0
    best, best_score = 0, -1
    for i, row in enumerate(grid[:12]):
        filled = [v for _, v in row if v not in (None, "")]
        texty = sum(1 for _, v in row if isinstance(v, str) and v.strip())
        score = texty - 0.5 * (len(filled) - texty)
        if score > best_score:
            best, best_score = i, score
    return best


def analyze_tables(doc, args, findings, notes):
    """F1b aritmetika turunan, F1c duplikat kunci, F1d placeholder. Mengembalikan ringkasan."""
    stats = {"sheets": [], "records": 0, "cols": {}, "arith_checked": 0, "total_review": 0}
    for sh in doc.sheets:
        grid = sh["grid"]
        if not grid:
            continue
        hi = find_header_row(grid, args)
        headers = [("" if v is None else str(v)).strip() for _, v in grid[hi]]
        idx_name, idx_url, idx_keys, keys_mode = resolve_columns(headers, args)
        stats["sheets"].append(sh["name"])
        stats["cols"][sh["name"]] = {"header_row": hi + 1,
                                     "name": headers[idx_name] if idx_name is not None else None,
                                     "url": headers[idx_url] if idx_url is not None else None,
                                     "keys": [headers[i] for i in idx_keys]}
        if sh.get("hidden"):
            notes.append(Note("SHEET_TERSEMBUNYI", sh["name"], "sheet ikut dibaca; verifikasi apakah sah"))
        rows = grid[hi + 1:]
        recs = [r for r in rows if any(v not in (None, "") for _, v in r)]
        stats["records"] += len(recs)
        dotk = col_dot_thousands([[v for _, v in r] for r in recs])
        if dotk:
            notes.append(Note("ANGKA_LOKAL", sh["name"],
                              "pola ribuan bertitik terdeteksi -> angka dibaca dengan konvensi Indonesia"))
        sh["_headers"] = headers
        sh["_idx"] = (idx_name, idx_url, idx_keys)
        sh["_records"] = recs

        # --- F1b(i) TOTAL baris: kolom berlabel total harus = jumlah/hasil kali angka lain sebaris
        for r in recs:
            addr = {i: a for i, (a, _) in enumerate(r)}
            vals = {i: v for i, (_, v) in enumerate(r)}
            label = str(vals.get(0) or "").strip()
            if TOTAL_LABEL_RE.search(label):
                continue  # baris TOTAL ditangani pemeriksaan total_kolom, bukan total_baris
            for i, h in enumerate(headers):
                if i == 0 or not TOTAL_HDR_RE.search(h or ""):
                    continue
                stated = parse_num(vals.get(i), dotk)
                if stated is None:
                    continue
                parts = [parse_num(vals[j], dotk) for j in sorted(vals) if j != i and j != 0
                         and not PCT_HDR_RE.search(headers[j] or "")]
                parts = [p for p in parts if p is not None]
                if len(parts) < 2:
                    continue
                exp = sum(parts)
                prod = 1.0
                for p in parts:
                    prod *= p
                stats["arith_checked"] += 1
                # sah bila stated = jumlah komponen ATAU hasil kali komponen (layout Qty x Price = Total)
                if not (close_enough(stated, exp) or (len(parts) <= 3 and close_enough(stated, prod))):
                    findings.append(Finding(2, "F1b", "%s!%s" % (sh["name"], addr.get(i, "#%d" % i)),
                                            "total_baris kolom '%s' = %s padahal jumlah komponen %s dan hasil kali %s [%s]"
                                            % (h, fmt_num(stated), fmt_num(exp), fmt_num(prod), label[:24])))
                break  # satu kolom total per baris cukup

        # --- F1b(ii) TOTAL kolom (D-03 kartu t_39db5b93): komponen dijumlah ke ARAH BAWAR
        # dulu (kasus PROPOSAL-SWMS tabel10!r6), lalu arah ATAS (preseden expo26 B70); jalan
        # kontigu dan POTONG pada baris kosong / baris berlabel teks tanpa angka / baris
        # total lain; toleransi close_enough tidak berubah. Vonis sah bila stated = jumlah
        # prefiks run terdekat (blok yang menempel baris label) pada SALAH SATU arah.
        # Ketidakcocokan di KEDUA arah: label strict tetap FAIL pemblokir (kontrol mutasi
        # +0,8% wajib terdeteksi); label nama-seksii enumerasi (tier ambiguous, preseden
        # B10 'Total enam sheet pendalaman' yang agregatnya lintas-sheet) turun ke CATATAN
        # NEEDS_REVIEW non-pemblokir ber-alasan tercetak (D-03 B/C), bukan FAIL senyap.
        ncols = max((len(r) for r in recs), default=0)
        for k, r in enumerate(rows):
            label = str(r[0][1] if r else "").strip()
            tier = total_label_tier(label)
            if tier is None:
                continue
            for j in range(1, ncols):
                if j < len(headers) and PCT_HDR_RE.search(headers[j] or ""):
                    continue  # kolom persentase tidak menjumlah (persen bukan besaran aditif)
                stated = parse_num(r[j][1] if j < len(r) else None, dotk)
                if stated is None:
                    continue
                def walk(m, step):
                    vals = []
                    mixed = False
                    while 0 <= m < len(rows):
                        rr = rows[m]
                        if not any(v not in (None, "") for _, v in rr):
                            break  # berjeda kosong = batas blok
                        lab2 = str(rr[0][1] if rr else "").strip()
                        if TOTAL_LABEL_RE.search(lab2):
                            break  # baris total lain = batas blok
                        v = parse_num(rr[j][1] if j < len(rr) else None, dotk)
                        if v is not None:
                            vals.append(v)
                        elif not any(parse_num(v2, dotk) is not None for _, v2 in rr):
                            break  # baris tanpa angka sama sekali (judul/catatan/header) = batas blok
                        # baris data tanpa angka di kolom ini tapi berangka di kolom lain:
                        # lanjut (mis. sel '#REF!' tidak memotong run kolom tetangga);
                        # D-03: lintasan semacam ini membuat blok "kolom campur" -> mixed.
                        else:
                            mixed = True
                        m += step
                    return vals, mixed
                down, mixed_d = walk(k + 1, +1)
                up, mixed_u = walk(k - 1, -1)
                if max(len(up), len(down)) < 2:
                    continue
                ok = False
                for seq in (down, up):  # arah BAWAR didahulukan (D-03 B)
                    acc = 0.0
                    for ncomp, v in enumerate(seq, start=1):
                        acc += v
                        if ncomp >= 2 and close_enough(stated, acc):
                            ok = True
                            break
                    if ok:
                        break
                stats["arith_checked"] += 1
                if not ok:
                    seq, dirn = (down, "bawah") if len(down) >= len(up) else (up, "atas")
                    loc = "%s!%s" % (sh["name"], r[j][0] if j < len(r) else "#%d" % j)
                    detail = ("total_kolom baris '%s' = %s padahal jumlah %d butir terdekat di %s = %s"
                              % (label[:28], fmt_num(stated), len(seq), dirn, fmt_num(sum(seq))))
                    # Struktur blok meragukan (D-03 B "jeda/kolom campur"): KEDUA kandidat
                    # blok sama-sama memuat baris lintasan tanpa angka di kolom ini -> alat
                    # tidak bisa memastikan blok komponen mana yang dibandingkan. Preseden
                    # FX-F1B-04 (Data!C7, satu sisi saja bercampur) TIDAK kena -> tetap FAIL;
                    # preseden kontrol mutasi PROPOSAL-SWMS tabel10 (kedua sisi bersih) FAIL.
                    meragukan = mixed_u and mixed_d
                    if tier == "ambiguous" or meragukan:
                        why = ("label '%s' berbentuk nama seksi enumerasi (agregat bisa lintas-sheet, "
                               "blok tetangga belum tentu komponennya)" % label[:40]
                               if tier == "ambiguous" else
                               "struktur blok meragukan: kedua kandidat blok memuat baris lintasan "
                               "tanpa angka di kolom ini (jeda/kolom campur)")
                        stats["total_review"] += 1
                        notes.append(Note("NEEDS_REVIEW", loc,
                                          "%s; %s - vonis D-03: CATATAN non-pemblokir, tinjau manusia"
                                          % (why, detail)))
                    else:
                        findings.append(Finding(2, "F1b", loc, detail))

        # --- F1b(iii) PERSENTASE: kolom % harus konsisten dgn dua angka lain sebaris
        pct_cols = [i for i, h in enumerate(headers) if PCT_HDR_RE.search(h or "")]
        for r in recs:
            label = str(r[0][1] if r else "").strip()
            if TOTAL_LABEL_RE.search(label):
                continue  # baris TOTAL tidak diuji persentasenya (angka agregat, bukan rasio baris)
            vals = {i: v for i, (_, v) in enumerate(r)}
            for i in pct_cols:
                pv = parse_num(vals.get(i), dotk)
                if pv is None or pv <= 0:
                    continue
                others = [parse_num(vals[j], dotk) for j in sorted(vals) if j != i and j != 0]
                others = [o for o in others if o is not None and o != 0]
                if len(others) < 2:
                    continue
                # sah bila ADA pasangan kolom yang menghasilkan persentase ini (dua arah),
                # bukan hanya dua angka pertama: mencegah positif palsu pada tabel banyak kolom
                stats["arith_checked"] += 1
                ok = False
                for x in range(len(others)):
                    for y in range(x + 1, len(others)):
                        a, b = others[x], others[y]
                        if close_enough(pv, a / b * 100.0) or close_enough(pv, b / a * 100.0):
                            ok = True
                            break
                    if ok:
                        break
                if not ok:
                    a, b = others[0], others[1]
                    findings.append(Finding(2, "F1b", "%s!%s" % (sh["name"], dict((k2, a2) for k2, (a2, _) in enumerate(r)).get(i, "#%d" % i)),
                                            "persentase %s%% tidak cocok dgn %s/%s=%.1f%% (atau kebalikannya %.1f%%)"
                                            % (fmt_num(pv), fmt_num(a), fmt_num(b), a / b * 100.0, b / a * 100.0)))

        # --- F1c duplikat kunci
        if idx_keys:
            # Preseden t_b0cf1dc7 (akar-3): fallback BUTA ke kolom nama saat --key-col tidak
            # ada di sheet menghapus dimensi (SOROTAN-TIERB kehilangan Expo -> positif palsu
            # lintas-expo). Kini: kunci gabungan kolom dimensi pertama + nama bila kolom
            # pertama bukan nama, dan SETIAPI fallback dicatat FALLBACK-REVIEW.
            composite = (keys_mode == "fallback-name" and idx_name is not None and idx_name != 0)
            if keys_mode == "fallback-name":
                notes.append(Note("FALLBACK-REVIEW", sh["name"],
                                  "kolom kunci (%s) tidak ada di sheet ini; duplikat dinilai dari kolom nama%s - tinjau manual sebelum vonis"
                                  % (", ".join(args.key_col or []) or "auto",
                                     (" + dimensi pertama '%s'" % headers[0]) if composite else "")))
            seen = {}
            for r in recs:
                kv = []
                if composite:
                    kv.append(norm(str(r[0][1])) if r and r[0][1] is not None else "")
                for i in idx_keys:
                    kv.append(norm(str(r[i][1])) if i < len(r) and r[i][1] is not None else "")
                key = "|".join(kv)
                if not key.strip():
                    continue
                label = str(r[0][1] if r else "").strip()[:28]
                if TOTAL_LABEL_RE.search(label):
                    continue
                seen.setdefault(key, []).append(r)
            for key, rs in sorted(seen.items()):
                if len(rs) > 1:
                    addrs = ", ".join("%s!%s" % (sh["name"], r[idx_keys[0]][0]) for r in rs)
                    keycols = ([headers[0]] if composite else []) + [headers[i] for i in idx_keys]
                    tag = ""
                    if keys_mode == "fallback-name":
                        tag = " [FALLBACK-REVIEW: kunci %s]" % "+".join(c for c in keycols if c)
                    findings.append(Finding(3, "F1c", addrs,
                                            "duplikat kunci %s muncul %dx (kolom kunci: %s)%s"
                                            % (key[:40], len(rs), ", ".join(keycols), tag)))

        # --- KOSONG pada field beban-rilis (catatan, bukan pemblokir)
        if idx_url is not None:
            for r in recs:
                label = str(r[0][1] if r else "").strip()
                if TOTAL_LABEL_RE.search(label):
                    continue
                v = r[idx_url][1] if idx_url < len(r) else None
                if v is None or str(v).strip() == "":
                    notes.append(Note("KOSONG", "%s!%s" % (sh["name"], r[idx_url][0]), "field URL kosong pada baris '%s'" % label))
    return stats


def fmt_num(x):
    if x is None:
        return "-"
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return ("%.4f" % x).rstrip("0").rstrip(".")


# ---------------------------------------------------------------- F2 ekstraksi & rel
def _loc_specific(loc):
    """True bila alamat menunjuk sel/koordinat (sheet!KOORD atau tabel!rR/cC), bukan rel/paragraf."""
    l = loc or ""
    return bool(re.search(r"![A-Z]{1,3}\d+$", l) or re.search(r"!r\d+/c\d+$", l))


def analyze_urls(doc, args, findings, notes):
    """Kelengkapan ekstraksi (CHECK 5) + keutuhan rel (CHECK 6). Return daftar URL unik siap probe."""
    seen = {}
    for u in doc.urls:
        raw = (u.url or "").strip()
        if not raw or raw.startswith("("):
            continue
        sch = re.match(r"^([a-zA-Z][a-zA-Z0-9+.\-]*):", raw)
        if sch and sch.group(1).lower() not in ("http", "https") and not raw.lower().startswith("www."):
            notes.append(Note("SKEMA_NON_HTTP", u.loc or raw, "%s skema=%s (tidak diprobe)" % (raw[:80], sch.group(1).lower())))
            continue
        uu = abs_url(raw)
        u.norm = uu
        if uu not in seen:
            seen[uu] = u
        elif _loc_specific(u.loc) and not _loc_specific(seen[uu].loc):
            seen[uu] = u   # preseden t_b0cf1dc7: objek hyperlink dalam sel lebih presisi utk F3
                           # daripada rel generik part#rId / '#paragraf' tanpa alamat
    # kelengkapan: setiap rel eksternal http(s) wajib punya rekaman URL
    rel_targets = {abs_url(r.target) for r in doc.rels
                   if (r.mode or "").lower() == "external" and re.match(r"https?://", r.target or "", re.I)}
    missing = sorted(t for t in rel_targets if t not in seen)
    for t in missing:
        findings.append(Finding(5, "F2a", "rel:%s" % t[:80], "rel eksternal ada tapi URL-nya tidak terekstrak (ekstraksi tidak lengkap)"))
    # kelengkapan docx: tag <w:hyperlink> harus tercermin pada rekaman
    if doc.fmt == "docx":
        tags = doc.raw_tokens.get("docx_hyperlink_tags", 0)
        got = sum(1 for u in doc.urls if u.source == "docx-hyperlink")
        if tags and got < tags:
            findings.append(Finding(5, "F2a", "docx:hyperlink", "tag <w:hyperlink>=%d tapi rekaman hyperlink=%d (ada yang lolos)" % (tags, got)))
    if doc.fmt == "xlsx":
        tags = doc.raw_tokens.get("xlsx_hyperlink_tags", 0)
        got = sum(1 for u in doc.urls if u.source == "xlsx-cell")
        if tags and got < tags:
            findings.append(Finding(5, "F2a", "xlsx:hyperlink", "tag <hyperlink>=%d tapi rekaman sel hyperlink=%d" % (tags, got)))
        for t in doc.raw_tokens.get("openpyxl_cell_hyperlink_targets", []):
            if abs_url(t) not in seen:
                findings.append(Finding(5, "F2a", "openpyxl:%s" % t[:80], "hyperlink objek openpyxl tidak terekstrak lewat XML mentah"))
    if not doc.urls:
        notes.append(Note("TANPA_URL", doc.path, "tidak ada URL yang terekstrak dari berkas ini"))

    # CHECK 6 keutuhan rel
    for r in doc.rels:
        bad = []
        t = r.target or ""
        if t.startswith("(DANGLING") or "DANGLING" in t:
            bad.append("rel_dangling")
        if "XML_PARSE_ERROR" in t:
            bad.append("rels_part_rusak:" + t[:60])
        if t and (t != t.strip()):
            bad.append("target_ber_spasi_awal_akhir")
        if t and re.search(r"\s", t.strip()) and not t.strip().startswith("(DANGLING"):
            bad.append("target_ber_spasi_internal")
        if (r.mode or "").lower() == "external" and t and not re.match(r"https?://", t, re.I):
            if not re.match(r"(?i)^(mailto:|tel:|sms:|ftp:)", t):
                bad.append("eksternal_tanpa_skema_http")
        if t.startswith("file:") or t.lower().startswith("c:"):
            bad.append("target_path_lokal")
        for b in bad:
            findings.append(Finding(6, "F2b", "%s#%s" % (r.part, r.rid), "%s: target=%r mode=%s" % (b, t[:90], r.mode or "-")))
    return seen


def attach_entity_context(doc, args):
    """Tempelkan nama entitas ke URL lewat alamat sel/paragraf (baris yang sama)."""
    addr_index = {}
    for sh in doc.sheets:
        idx = sh.get("_idx") or (None, None, [])
        idx_name = idx[0]
        for r in sh.get("_records", []):
            for i, (a, v) in enumerate(r):
                key = "%s!%s" % (sh["name"], a)
                nm = ""
                if idx_name is not None and idx_name < len(r) and r[idx_name][1] is not None:
                    nm = str(r[idx_name][1]).strip()
                addr_index.setdefault(key, []).append((nm, str(v)[:40] if v is not None else ""))
    for u in doc.urls:
        hits = addr_index.get(u.loc)
        if hits:
            nm = next((h[0] for h in hits if h[0]), "")
            if nm:
                u.name = nm
                u.key = nm
    # docx: hyperlink di dalam sel tabel -> nama dari kolom nama tabel yang sama/baris
    for sh in doc.sheets:
        if not sh["name"].startswith("docx:"):
            continue
        idx = sh.get("_idx") or (None, None, [])
        idx_name = idx[0]
        for r in sh.get("_records", []):
            nm = ""
            if idx_name is not None and idx_name < len(r) and r[idx_name][1]:
                nm = str(r[idx_name][1]).strip()
            if not nm:
                continue
            for i, (a, v) in enumerate(r):
                if not isinstance(v, str):
                    continue
                for m in URL_RE.findall(v):
                    for u in doc.urls:
                        if u.url.rstrip(".,;") == m.rstrip(".,;") and not u.name:
                            u.name = nm
                            u.key = nm


# ---------------------------------------------------------------- probe jaringan
def load_cache(outdir):
    cache = {}
    p = os.path.join(outdir, "evidence_urls.jsonl")
    if os.path.exists(p):
        with io.open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                if rec.get("url"):
                    cache[rec["url"]] = rec
    return cache


def probe_all(urls, args, outdir, notes):
    """urls: dict url->UrlRec. Resume dari evidence_urls.jsonl di outdir."""
    cache = load_cache(outdir)
    ev_path = os.path.join(outdir, "evidence_urls.jsonl")
    ev_f = io.open(ev_path, "a", encoding="utf-8")
    lock = threading.Lock()
    todo = [u for u in sorted(urls) if u not in cache]

    def one(u):
        rec = {"url": u, "ts": time.strftime("%F %H:%M:%S")}
        body = None
        try:
            r = fetch(u, timeout=args.timeout)
            body = r["body"]
            rec.update(status=r["status"], final_url=r["final_url"], content_encoding=r["content_encoding"],
                       raw_len=r["raw_len"], decoded_len=r["decoded_len"], decode_note=r["decode_note"])
            rec["verdict"] = "HIDUP" if 200 <= r["status"] < 400 else ("HTTP4XX" if 400 <= r["status"] < 500 else "MATI")
        except urllib.error.HTTPError as e:
            rec.update(status=e.code, final_url=u, verdict=("HTTP4XX" if 400 <= e.code < 500 else "MATI"),
                       content_encoding="", raw_len=0, decoded_len=0, decode_note="http_error")
        except Exception as e:
            rec.update(status=type(e).__name__, final_url="", verdict="MATI", content_encoding="",
                       raw_len=0, decoded_len=0, decode_note=type(e).__name__)
        return rec, body

    results = dict(cache)
    bodies_mem = {}
    if todo and args.workers > 0:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(one, u): u for u in todo}
            for fu in as_completed(futs):
                rec, body = fu.result()
                if body is not None:
                    bodies_mem[rec["url"]] = {"status": rec.get("status"), "final_url": rec.get("final_url", ""),
                                              "body": body}
                with lock:
                    ev_f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    ev_f.flush()
                results[rec["url"]] = rec
    ev_f.close()

    for u, rec in results.items():
        ur = urls.get(u)
        if ur is None:
            continue
        ur.verdict = rec.get("verdict", "")
        ur.status = rec.get("status", "")
        ur.final_url = rec.get("final_url", "")
        ur.sig["_transport"] = {k: rec.get(k) for k in ("content_encoding", "raw_len", "decoded_len", "decode_note")}
        if ur.verdict == "MATI":
            notes.append(Note("MATI", ur.loc or u, "%s status=%s" % (u, ur.status)))
        elif ur.verdict == "HTTP4XX":
            notes.append(Note("HTTP4XX", ur.loc or u, "%s status=%s" % (u, ur.status)))
        if ur.final_url and dom_of(ur.final_url) and dom_of(u) and dom_of(ur.final_url) != dom_of(u):
            notes.append(Note("REDIRECT-SILANG", ur.loc or u, "%s -> %s" % (u, ur.final_url)))
    return results, bodies_mem


def bodies_for(results, urls, args, bodies_mem):
    """Body utk entity-match: pakai hasil probe di memori; URL dari cache resume diambil ulang sekali."""
    out = {}
    for u, rec in sorted(results.items()):
        if rec.get("verdict") != "HIDUP":
            continue
        if u in bodies_mem:
            out[u] = bodies_mem[u]
            continue
        try:
            out[u] = fetch(u, timeout=args.timeout)
        except Exception:
            out[u] = None
    return out


# ---------------------------------------------------------------- CHECK 9/10
def check_evidence(outdir, args, n_records, n_urls, findings):
    rep = sorted(f for f in os.listdir(outdir) if f.startswith("gate_report_"))
    if not rep:
        findings.append(Finding(9, "BUKTI", outdir, "laporan gate tidak tertulis"))
    et = os.path.join(outdir, "evidence_tables.jsonl")
    eu = os.path.join(outdir, "evidence_urls.jsonl")
    lines_t = sum(1 for l in io.open(et, encoding="utf-8") if l.strip()) if os.path.exists(et) else -1
    lines_u = sum(1 for l in io.open(eu, encoding="utf-8") if l.strip()) if os.path.exists(eu) else -1
    if lines_t < 0:
        findings.append(Finding(9, "BUKTI", et, "evidence_tables.jsonl tidak ada"))
    elif lines_t < n_records:
        findings.append(Finding(9, "BUKTI", et, "rekaman dump %d < rekaman terbaca %d" % (lines_t, n_records)))
    if lines_u < 0:
        findings.append(Finding(9, "BUKTI", eu, "evidence_urls.jsonl tidak ada"))
    elif lines_u < n_urls:
        findings.append(Finding(9, "BUKTI", eu, "bukti URL %d < URL terprobes/sempurna %d" % (lines_u, n_urls)))
    for extra in ("notes_register.csv", "failures.csv"):
        if not os.path.exists(os.path.join(outdir, extra)):
            findings.append(Finding(9, "BUKTI", os.path.join(outdir, extra), "berkas bukti tidak ada"))
    return lines_t, lines_u


# ---------------------------------------------------------------- CLI
def build_parser():
    ap = argparse.ArgumentParser(
        prog="doc_gate_check.py",
        description="Gerbang deterministik artefak dokumen .xlsx/.docx (F1 tabel, F2 hyperlink/rel, F3 entity-match). "
                    "Kontrak CLI D-TA-02; flag kartu lama (--out/--no-probe/--entity-col/--name-col N) diterima sebagai alias.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("target_pos", nargs="?", help="posisi alternatif untuk --target")
    ap.add_argument("--target", help="berkas .xlsx atau .docx yang diverifikasi")
    ap.add_argument("--outdir", help="direktori bukti (dibuat bila belum ada)")
    ap.add_argument("--out", dest="out_alias", help="ALIAS kartu C1 untuk --outdir")
    ap.add_argument("--mode", choices=["gate", "fixture"], default="gate")
    ap.add_argument("--expect", help="manifest fixture_expected.json (mengaktifkan CHECK 10)")
    ap.add_argument("--config", help="JSON berisi default argumen (key sama dengan flag)")
    ap.add_argument("--sheet", action="append", default=[], help="nama sheet (boleh berulang); default sheet pertama")
    ap.add_argument("--all-sheets", action="store_true", help="baca semua sheet (termasuk tersembunyi)")
    ap.add_argument("--header-row", type=int, default=0, help="nomor baris header (0 = deteksi heuristik)")
    ap.add_argument("--name-col", help="nama kolom entitas ATAU indeks 1-based")
    ap.add_argument("--entity-col", help="ALIAS: indeks 1-based atau nama kolom entitas")
    ap.add_argument("--url-col", default="Website", help="nama kolom URL ATAU indeks 1-based")
    ap.add_argument("--key-col", action="append", default=[], help="kolom kunci duplikat (boleh berulang)")
    ap.add_argument("--timeout", type=float, default=18.0, help="detik per probe")
    ap.add_argument("--workers", type=int, default=10, help="konkurensi probe")
    ap.add_argument("--skip-network", action="store_true", help="tanpa probe hidup (CHECK 7 jadi NEEDS_REVIEW)")
    ap.add_argument("--no-probe", dest="skip_network", action="store_true", help="ALIAS kartu C1 untuk --skip-network")
    ap.add_argument("--whitelist", help="CSV whitelist (sheet,no,url,alasan) seperti pola gate_accuracy_100")
    ap.add_argument("--keep-body", action="store_true", help="simpan potongan body HTML di bukti (default mati)")
    return ap


def merge_config(ap, args):
    if getattr(args, "config", None) and os.path.exists(args.config):
        cfg = json.load(io.open(args.config, encoding="utf-8"))
        cur = {k: v for k, v in vars(args).items()}
        for k, v in cfg.items():
            if k not in cur:
                continue
            if isinstance(cur[k], list):
                if not cur[k]:
                    setattr(args, k, v if isinstance(v, list) else [v])
            elif cur[k] in (None, False, 0, []) or (k.endswith("_alias")):
                setattr(args, k, v)
    if not args.target and args.target_pos:
        args.target = args.target_pos
    if not args.outdir:
        args.outdir = args.out_alias
    if not args.outdir:
        args.outdir = os.path.join(os.path.dirname(os.path.abspath(args.target or ".")) or ".", "docgate_out")
    return args


def load_whitelist(path):
    wl = {}
    if path and os.path.exists(path):
        for r in csv.DictReader(io.open(path, encoding="utf-8-sig")):
            wl[(r.get("sheet", ""), str(r.get("no", "")))] = r
    return wl


# ---------------------------------------------------------------- utama
def run(args, argv):
    ts = time.strftime("%Y%m%d_%H%M%S")
    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)
    checks = []
    findings = []
    notes = []

    def add(n, status, text):
        checks.append((n, status, text))

    target = os.path.abspath(args.target or "")
    doc = Doc(target)
    if not os.path.exists(target):
        findings.append(Finding(1, "F1a", target, "berkas target tidak ada"))
        add(1, "FAIL", "F1a keutuhan baca - berkas tidak ada: %s" % target)
        add(2, "INFO", "F1b dilewati (berkas tidak terbaca)")
        add(3, "INFO", "F1c dilewati")
        add(4, "INFO", "F1d dilewati")
        add(5, "INFO", "F2a dilewati")
        add(6, "INFO", "F2b dilewati")
        add(7, "INFO", "F2c dilewati")
        add(8, "INFO", "F3 dilewati")
        add(9, "INFO", "bukti sebagian ditulis")
        if args.expect:
            add(10, "FAIL", "manifest tidak dapat diuji tanpa berkas")
            findings.append(Finding(10, "MANIFEST", target, "target tidak ada sehingga manifest tidak teruji"))
        dump_tables(outdir, doc, {"sheets": [], "records": 0, "cols": {}, "arith_checked": 0})
        write_notes(outdir, notes)
        write_failures(outdir, findings)
        return finish(args, outdir, ts, checks, findings, notes, doc, 0, 0)

    if doc.fmt not in ("xlsx", "docx"):
        doc.read_error = "format %s tidak didukung (hanya .xlsx/.docx)" % doc.ext
    if doc.fmt == "xlsx":
        read_xlsx(target, doc)
    else:
        read_docx(target, doc)

    # seleksi sheet/tabel (D-TA-02: default workbook = sheet pertama; docx = semua tabel)
    skipped = []
    if args.sheet:
        want = [s.strip() for s in args.sheet if s.strip()]
        keep = [sh for sh in doc.sheets if sh["name"] in want or any(w in sh["name"] for w in want)]
        missing = [w for w in want if not any(w == sh["name"] or w in sh["name"] for sh in doc.sheets)]
        if missing:
            notes.append(Note("SHEET_TIDAK_ADA", ", ".join(missing), "nama sheet diminta tapi tidak ada di berkas"))
        skipped = [sh["name"] for sh in doc.sheets if sh not in keep]
        doc.sheets = keep
    elif doc.fmt == "xlsx" and not args.all_sheets and len(doc.sheets) > 1:
        skipped = [sh["name"] for sh in doc.sheets[1:]]
        doc.sheets = doc.sheets[:1]
        notes.append(Note("SHEET_DILEWATI", ", ".join(skipped),
                          "default hanya sheet pertama (D-TA-02); pakai --sheet atau --all-sheets untuk sisanya"))

    # ---- ekstraksi URL + rel (dini: vonis CHECK 1 butuh tahu apakah berkas memuat URL)
    url_map = analyze_urls(doc, args, findings, notes)

    # ---- CHECK 1 F1a keutuhan baca
    stats = {"sheets": [], "records": 0, "cols": {}, "arith_checked": 0}
    if doc.read_error:
        add(1, "FAIL", "F1a keutuhan baca - %s" % doc.read_error)
        findings.append(Finding(1, "F1a", target, "berkas tidak terbaca: %s" % doc.read_error))
    else:
        stats = analyze_tables(doc, args, findings, notes)
        cols = stats["cols"]
        miss = [n for n, c in cols.items() if not c.get("url")]
        add(1, "PASS", "F1a keutuhan baca (format=%s, sheet/tabel=%d %s, rekaman=%d, baris_header=%s, kolom_url=%s, kolom_nama=%s)%s"
            % (doc.fmt, len(stats["sheets"]), json.dumps(stats["sheets"], ensure_ascii=False)[:120], stats["records"],
               json.dumps([c["header_row"] for c in cols.values()]),
               json.dumps([c["url"] for c in cols.values()], ensure_ascii=False),
               json.dumps([c["name"] for c in cols.values()], ensure_ascii=False),
               ("; sheet dilewati: " + ", ".join(skipped)[:120]) if skipped else ""))
        if miss:
            per_sheet = []
            for n in miss:
                recs_here = sum(1 for u in doc.urls if (u.loc or "").startswith(n + "!"))
                per_sheet.append("%s(%d rekaman URL)" % (n, recs_here))
            notes.append(Note("KOLOM_URL", ", ".join(miss),
                              "kolom URL tidak terselesaikan pada sheet tsb (butuh --url-col bila sheet itu tabel rekaman); %s - catatan cakupan, bukan pemblokir (preseden t_b0cf1dc7)"
                              % ", ".join(per_sheet)))

    # ---- CHECK 2 F1b
    attach_entity_context(doc, args)  # butuh indeks kolom hasil analisis tabel
    for kind, loc, detail in doc.notes_extra:   # catatan tingkat pembaca (mis. fallback pustaka)
        notes.append(Note(kind, loc, detail))
    n2 = [f for f in findings if f.check == 2]
    n2rev = stats.get("total_review", 0)
    add(2, "FAIL" if n2 else "PASS", "F1b aritmetika turunan (%d uji, %d temuan%s)%s"
        % (stats["arith_checked"], len(n2),
           (", %d CATATAN NEEDS_REVIEW non-pemblokir lihat register" % n2rev) if n2rev else "",
           (": " + "; ".join(sorted(set("%s" % f.location for f in n2))[:8])) if n2 else ""))

    # ---- CHECK 3 F1c
    n3 = [f for f in findings if f.check == 3]
    add(3, "FAIL" if n3 else "PASS", "F1c duplikat kunci (%d temuan)%s"
        % (len(n3), (": " + "; ".join(f.location for f in n3[:6])) if n3 else ""))

    # ---- CHECK 4 F1d
    for loc, val, rule in doc.placeholders:
        findings.append(Finding(4, "F1d", loc, "placeholder/sentinel rusak (%s): %r" % (rule, val)))
    n4 = [f for f in findings if f.check == 4]
    add(4, "FAIL" if n4 else "PASS", "F1d placeholder rusak (%d temuan)%s"
        % (len(n4), (": " + "; ".join(sorted(set(f.location for f in n4))[:8])) if n4 else ""))

    # ---- CHECK 5 F2a / CHECK 6 F2b
    n5 = [f for f in findings if f.check == 5]
    add(5, "FAIL" if n5 else "PASS", "F2a ekstraksi lengkap (sumber URL=%d unik=%d; sumber=%s)%s"
        % (len(doc.urls), len(url_map), json.dumps({k: v for k, v in sorted(
            _count_sources(doc.urls).items())}), ("; temuan: " + "; ".join(f.desc[:60] for f in n5[:4])) if n5 else ""))
    n6 = [f for f in findings if f.check == 6]
    add(6, "FAIL" if n6 else "PASS", "F2b keutuhan rel (rel eksternal=%d, temuan=%d)%s"
        % (sum(1 for r in doc.rels if (r.mode or "").lower() == "external"), len(n6),
           (": " + "; ".join("%s %s" % (f.location, f.desc[:70]) for f in n6[:6])) if n6 else ""))

    # ---- CHECK 7 F2c probe hidup
    results = {}
    bodies_mem = {}
    if args.skip_network:
        add(7, "NEEDS_REVIEW", "F2c probe hidup dilewati (--skip-network): vonis jaringan TIDAK terbukti, %d URL menunggu probe" % len(url_map))
        for u in sorted(url_map):
            notes.append(Note("SKIP-NETWORK", url_map[u].loc or u, u))
    elif not url_map:
        add(7, "PASS", "F2c probe hidup (0 URL untuk diprobe)")
    else:
        results, bodies_mem = probe_all(url_map, args, outdir, notes)
        probed = [u for u in sorted(url_map) if url_map[u].verdict]
        n_dead = sum(1 for u in probed if url_map[u].verdict in ("MATI", "HTTP4XX"))
        n_live = sum(1 for u in probed if url_map[u].verdict == "HIDUP")
        add(7, "PASS", "F2c probe hidup (diprobe=%d HIDUP=%d MATI/4XX=%d sebagai CATATAN, timeout=%ss workers=%d)%s"
            % (len(probed), n_live, n_dead, args.timeout, args.workers,
               ("; contoh mati: " + ", ".join(sorted(url_map[u].url for u in probed if url_map[u].verdict != "HIDUP")[:4])) if n_dead else ""))

    # ---- CHECK 8 F3 entity-match (selalu diekskusi sesuai D-TA-03)
    bodies = bodies_for(results, url_map, args, bodies_mem) if results else {}
    n_wrong = []
    n_review = []
    n_ok = 0
    n_noname = 0
    for u in sorted(url_map):
        ur = url_map[u]
        if ur.verdict != "HIDUP":
            ur.entity = "TANPA_PROBE_BERHASIL"
            continue
        if not ur.name:
            ur.entity = "TANPA_NAMA"
            n_noname += 1
            notes.append(Note("ENTITY-CONTEXT", ur.loc or u, "nama entitas tidak resolvable utk %s" % u))
            continue
        b = bodies.get(u)
        if not b:
            ur.entity = "BODY_GAGAL"
            continue
        ok, sig = entity_match(ur.name, u, b["status"], b["final_url"], b["body"])
        sc = signal_count(sig)
        ur.sig.update(sig)
        ur.sig["signals"] = sc
        if not ok:
            ur.entity = "SALAH-TARGET"
            n_wrong.append(ur)
        elif sc <= 1:
            ur.entity = "NEEDS_REVIEW"
            n_review.append(ur)
        else:
            ur.entity = "BENAR"
            n_ok += 1
    for ur in n_wrong:
        findings.append(Finding(8, "F3", "%s|%s" % (ur.loc, ur.name),
                                "SALAH-TARGET %s (status=%s final=%s sinyal=%s judul='%s')"
                                % (ur.url, ur.status, ur.final_url[:70],
                                   json.dumps({k: v for k, v in ur.sig.items() if k != "_transport"}),
                                   str(ur.sig.get("title", ""))[:50])))
    for ur in n_review:
        findings.append(Finding(99, "F3", "%s|%s" % (ur.loc, ur.name), "1 sinyal saja"))
    if args.skip_network and url_map:
        add(8, "NEEDS_REVIEW", "F3 entity-match belum terbukti (probe dilewati, %d URL menunggu)" % len(url_map))
    elif not url_map:
        add(8, "PASS", "F3 entity-match (0 URL untuk dicocokkan)")
    else:
        add(8, "FAIL" if n_wrong else ("NEEDS_REVIEW" if n_review else "PASS"),
            "F3 entity-match (bernama=%d BENAR=%d SALAH-TARGET=%d NEEDS_REVIEW=%d tanpa-konteks=%d)%s"
            % (len(url_map) - n_noname, n_ok, len(n_wrong), len(n_review), n_noname,
               (": " + "; ".join("%s|%s -> %s" % (ur.loc, ur.name, ur.url)[:130] for ur in n_wrong[:5])) if n_wrong else ""))
    review_only = [f for f in findings if f.check == 99]
    findings = [f for f in findings if f.check != 99]

    # ---- bukti di disk
    merge_url_evidence(outdir, doc, url_map, results, bodies, args)
    dump_tables(outdir, doc, stats)
    write_notes(outdir, notes)
    write_failures(outdir, findings)
    # laporan sementara ditulis dulu agar CHECK 9 menguji berkas yang benar-benar ada,
    # lalu ditimpa finish() dengan versi final (memuat CHECK 9 dan CHECK 10)
    render_report(args, outdir, ts, checks, findings, notes, [], verdict_of(findings, checks))
    n_ev_urls = sum(1 for u in url_map if url_map[u].verdict)
    lt, lu = check_evidence(outdir, args, stats["records"], n_ev_urls, findings)
    n9 = [f for f in findings if f.check == 9]
    add(9, "FAIL" if n9 else "PASS", "bukti di disk (evidence_tables=%d baris, evidence_urls=%d baris, notes=%d, failures=%d)%s"
        % (lt, lu, len(notes), len(findings), ("; " + "; ".join(f.desc[:60] for f in n9)) if n9 else ""))

    # ---- CHECK 10 manifest
    expect_ok = True
    if args.expect:
        man = json.load(io.open(args.expect, encoding="utf-8"))
        fx = next((f for f in man.get("fixtures", []) if os.path.basename(f.get("file", "")) == os.path.basename(target)), None)
        if fx is None:
            add(10, "FAIL", "kesesuaian manifest - %s tidak terdaftar di %s" % (os.path.basename(target), args.expect))
            findings.append(Finding(10, "MANIFEST", os.path.basename(target), "tidak terdaftar di manifest"))
            expect_ok = False
        else:
            want_v = fx.get("expected_verdict")
            want_checks = sorted(set(int(x) for x in fx.get("expected_failed_checks", [])))
            got_checks = sorted(set(f.check for f in findings))
            got_v = verdict_of(findings, checks)
            n_defects = len(fx.get("defects", []))
            probs = []
            if got_v != want_v:
                probs.append("verdict=%s harusnya %s" % (got_v, want_v))
            if got_checks != want_checks:
                probs.append("CHECK gagal=%s harusnya %s" % (got_checks, want_checks))
            if len(findings) != n_defects:
                probs.append("cacat terdeteksi=%d harusnya %d sesuai manifest" % (len(findings), n_defects))
            # expected_notes: vonis CATATAN (MATI/KOSONG/ENTITY-CONTEXT) wajib muncul di register
            note_kinds = {}
            for n in notes:
                note_kinds[n.kind] = note_kinds.get(n.kind, 0) + 1
            for en in fx.get("expected_notes", []):
                have = note_kinds.get(en["kind"], 0)
                if have < int(en.get("min_count", 1)):
                    probs.append("notes_register kurang: %s tercatat %d harusnya >=%d (%s)"
                                 % (en["kind"], have, int(en.get("min_count", 1)), en.get("why", "")))
            expect_ok = not probs
            add(10, "PASS" if expect_ok else "FAIL", "kesesuaian manifest (%s)%s"
                % (os.path.basename(target), "; " + "; ".join(probs) if probs
                   else " - verdict, set CHECK, jumlah cacat, dan register catatan cocok"))
            if not expect_ok:
                findings.append(Finding(10, "MANIFEST", os.path.basename(target), "; ".join(probs)[:400]))

    return finish(args, outdir, ts, checks, findings, notes, doc, stats["records"], len(url_map), expect_ok, review_only)


def _count_sources(urls):
    c = {}
    for u in urls:
        c[u.source] = c.get(u.source, 0) + 1
    return c


def verdict_of(findings, checks):
    if findings or any(s == "FAIL" for _, s, _ in checks):
        return "FAIL"
    if any(s == "NEEDS_REVIEW" for _, s, _ in checks):
        return "NEEDS_REVIEW"
    return "PASS"


def merge_url_evidence(outdir, doc, url_map, results, bodies, args):
    """Tulis ulang evidence_urls.jsonl jadi rekaman lengkap per URL (lokasi+nama+vonis+sinyal+transport).

    Basis = baris transport hasil probe; rekaman gabungan menimpa file sehingga bukti akhir memuat
    kolom entity-match sesuai MG-R3, sementara resume tetap membaca kolom 'url'+'verdict' yang sama.
    """
    p = os.path.join(outdir, "evidence_urls.jsonl")
    base = {}
    if os.path.exists(p):
        for line in io.open(p, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("url"):
                base[r["url"]] = r
    with io.open(p, "w", encoding="utf-8") as f:
        for u in sorted(url_map):
            ur = url_map[u]
            rec = dict(base.get(u) or {})
            rec.update({"url": u, "source": ur.source, "location": ur.loc, "entity_name": ur.name,
                        "key": ur.key, "verdict": ur.verdict, "net_verdict": ur.verdict,
                        "status": ur.status,
                        "final_url": ur.final_url, "entity_verdict": ur.entity,
                        "signals": {k: v for k, v in ur.sig.items() if k != "_transport"},
                        "transport": ur.sig.get("_transport", {}),
                        "body_len": len((bodies.get(u) or {}).get("body") or b"")})
            if args.keep_body and bodies.get(u):
                rec["body_head"] = bodies[u]["body"][:600].decode("utf-8", "ignore")
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return len(url_map)


def dump_tables(outdir, doc, stats):
    p = os.path.join(outdir, "evidence_tables.jsonl")
    with io.open(p, "w", encoding="utf-8") as f:
        for sh in doc.sheets:
            hdr = sh.get("_headers", [])
            for r in sh.get("_records", []):
                rec = {"sheet": sh["name"], "cells": {}}
                for i, (a, v) in enumerate(r):
                    h = hdr[i] if i < len(hdr) else ""
                    rec["cells"][a] = {"header": h, "value": ("" if v is None else str(v))[:300]}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.write(json.dumps({"_meta": "stats", "stats": stats}, ensure_ascii=False) + "\n")


def write_notes(outdir, notes):
    p = os.path.join(outdir, "notes_register.csv")
    with io.open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["jenis", "lokasi", "detail"])
        for n in sorted(notes, key=lambda x: (x.kind, x.location, x.detail)):
            w.writerow([n.kind, n.location, n.detail[:300]])


def write_failures(outdir, findings):
    p = os.path.join(outdir, "failures.csv")
    with io.open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["check", "kelas", "alamat_presisi", "detail"])
        for fi in sorted(findings, key=lambda x: (x.check, x.location, x.desc)):
            w.writerow([fi.check, fi.cls, fi.location, fi.desc[:400]])


def render_report(args, outdir, ts, checks, findings, notes, review_only, verdict):
    lines = ["doc_gate_check.py v%s - target=%s" % (VERSION, os.path.abspath(args.target or "")),
             "mode=%s skip_network=%s timeout=%s workers=%s ts=%s" % (args.mode, args.skip_network, args.timeout, args.workers, time.strftime("%F %H:%M:%S")),
             "UA=%s" % UA, ""]
    for n, s, t in sorted(checks, key=lambda x: x[0]):
        lines.append("CHECK %d: %s - %s" % (n, s, t))
    if review_only:
        lines.append("")
        lines.append("INFO - entity-match 1 sinyal (perlu penilaian manusia, bukan lulus diam-diam): %d" % len(review_only))
        for f in review_only[:20]:
            lines.append("INFO -   %s" % f.location)
    lines.append("")
    lines.append("CATATAN register=%d ; FAILURE pemblokir=%d" % (len(notes), len(findings)))
    lines.append("VERDICT: %s" % verdict)
    text = "\r\n".join(lines) + "\r\n"
    rp = os.path.join(outdir, "gate_report_%s.txt" % ts)
    with io.open(rp, "w", encoding="utf-8") as f:
        f.write(text)
    return rp, text


def finish(args, outdir, ts, checks, findings, notes, doc, n_records, n_urls, expect_ok=True, review_only=()):
    verdict = verdict_of(findings, checks)
    if args.expect and not expect_ok and verdict == "PASS":
        verdict = "FAIL"
    rp, text = render_report(args, outdir, ts, checks, findings, notes, review_only, verdict)
    sys.stdout.write(text)
    sys.stdout.flush()
    if verdict == "FAIL":
        return 2
    if verdict == "NEEDS_REVIEW":
        return 3
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = build_parser()
    args = ap.parse_args(argv)
    args = merge_config(ap, args)
    try:
        return run(args, argv)
    except SystemExit:
        raise
    except Exception as e:
        sys.stderr.write("CRASH doc_gate_check: %s: %s\n" % (type(e).__name__, e))
        import traceback
        traceback.print_exc()
        sys.stdout.write("CHECK 1: FAIL - F1a keutuhan baca - crash %s: %s\r\n" % (type(e).__name__, e))
        sys.stdout.write("VERDICT: FAIL\r\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
