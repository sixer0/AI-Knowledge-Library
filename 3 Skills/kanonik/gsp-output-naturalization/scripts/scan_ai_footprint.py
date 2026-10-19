#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_ai_footprint.py - Scanner deterministik jejak AI pada keluaran GSP.

Rumah skill : gsp-output-naturalization (kanonik workspace/gsp-hermes/skills/)
Kontrak    : docs/2026-09-02-naturalisasi-output/ (misi naturalisasi-output)
Blueprint  : identification/02_structured.md langkah 9 (kartu NAT-S9)

Kebijakan mengikat yang diimplementasikan (pekerja TIDAK membuka ulang keputusan):
  D-TA-04  en dash U+2013 sah HANYA pada pola rentang angka antara dua digit;
           kemunculan dilaporkan sebagai baris INFO, bukan pelanggaran.
  D-TA-05  profil check per kanal; C-6/C-7/C-10 tidak berlaku di K1 chat / K4 notif.
  D-TA-07  summary/kanban_comment = prosa (tunduk gerbang); metadata mesin dikecualikan
           dari metrik prosa, TETAPI dihitung untuk U+2014 / U+00B7.
  D-TA-08  media sosial parsial: A1/A2 tetap mutlak, sisanya dilaporkan INFO.
  D-TA-09  agregasi: >=2 indikator berat terpicu ATAU 3+ indikator HIGH -> FAIL.
  D-TA-10  satu run scanner tidak pernah mengklaim cakupan fleet-wide.

Sumber aturan (pointer, jangan disalin ke sini):
  RT seksi 2.2 / 5.2 : docs/.../identification/01_translated.md (A1-A7, B1-B9, C-1..C-10)
  matriks sweep      : $LOCALAPPDATA/hermes/skills/gsp/gsp-verification-before-completion/
                       references/ai-footprint-sweep.md baris 17-33 (metode per format,
                       kasus escape/emitter)
  Module H           : gsp-document-quality-standards/SKILL.md H.2-H.6 (ambang ID)

Determinisme (kriteria S-5): tanpa stempel waktu, tanpa acak, semua iterasi koleksi
di-sort; dua run beruntun pada masukan sama menghasilkan byte yang identik.

KEBERSIHAN SUMBER (pola ai-footprint-sweep.md:5-10 + SKILL.md pitfalls): berkas ini
tidak memuat literal U+2014 / U+00B7 maupun bentuk escape/entity-nya sebagai teks
mentah. Karakter sasaran disusun lewat chr()/fragmen sehingga scanner tidak menandai
dirinya sendiri saat dipakai menyapu folder skill.

Keluaran : baris "CHECK n: PASS|FAIL|N/A|INFO - nama | detail" + "VERDICT: PASS|FAIL".
Exit code: 0 = tidak ada FAIL, 1 = ada FAIL (termasuk kanal tidak dikenal).
"""

import argparse
import html
import html.parser
import io
import json
import os
import re
import shutil
import sys
import tempfile
import tokenize
import zipfile

__version__ = "1.11.0"

# ---------------------------------------------------------------------------
# Karakter sasaran - disusun dari kode titik, bukan literal (lihat docstring)
# ---------------------------------------------------------------------------
EM_DASH = chr(0x2014)           # U+2014 em dash    -> A1 / C-1 (mutlak)
EN_DASH = chr(0x2013)           # U+2013 en dash    -> INFO dalam pola rentang angka
MID_DOT = chr(0x00B7)           # U+00B7 middle dot -> A2 / C-2 (mutlak di luar D16)

_BS = chr(0x005C)               # backslash
_AMP = chr(0x0026)              # ampersand


def _esc_form(hex_re):
    """Bentuk escape Python (backslash-u-hex / backslash-x-hex) sebagai pola regex."""
    return re.compile(re.escape(_BS) + "+[uU]0*" + hex_re + r"\b|" +
                      re.escape(_BS) + "+x0*" + hex_re + r"\b", re.IGNORECASE)


def _ent_dec(decimal):
    """Bentuk entity HTML desimal."""
    return re.compile(re.escape(_AMP + "#") + decimal + ";")


def _ent_hex(hex_re):
    """Bentuk entity HTML heksadesimal."""
    return re.compile(re.escape(_AMP + "#x") + "0*" + hex_re + ";", re.IGNORECASE)


def _ent_named(name):
    return re.compile(re.escape(_AMP + name) + ";", re.IGNORECASE)


EM_LITERAL_RE = re.compile(EM_DASH)
EM_FORM_RES = [_esc_form("2014"), _ent_dec("8212"), _ent_hex("2014"),
               _ent_named("mdash")]
MD_LITERAL_RE = re.compile(MID_DOT)
MD_FORM_RES = [_esc_form("b7"), _ent_dec("183"), _ent_hex("b7"), _ent_named("middot")]

# D-TA-04: satu-satunya pola en dash yang diizinkan; hasil dilaporkan INFO, bukan FAIL.
EN_DASH_RANGE_RE = re.compile(r"(?<=\d)" + EN_DASH + r"(?=\d)")

# Penanda blok terkendali D16 (pengecualian middle dot). Skop = SATU BERKAS:
# preseden nyata fleet (gsp-design-system-grill/references/master-design/gsp-ds-set-*.md)
# menaruh marker di kaki berkas sedangkan glyph-nya di kepala berkas, jadi skop
# per-baris atau per-blok akan salah menandai 21 berkas master design sebagai cacat.
# NAT-HIL-SC1 butir 1 (kartu t_c79b5f6d): kuantifier possessive pada alternatif
# minus dan pada bintang luar. Versi v1.2.0 `(?:>|#|-{3,}|<!--)*` meledak
# eksponensial pada baris pemisah 64 tanda minus (pesan gsp-custodian id=292,
# 6753 karakter, membekukan scanner >60 detik; bukti verify-chat-sweep.md seksi 6
# + verify-chat-sweep-custodian-diag.json). Alternatif saling lepas pada karakter
# awal (>, #, -, <) sehingga possessive tidak mengubah bahasa yang diterima,
# hanya memangkas backtracking menjadi kasus-linear.
D16_MARKER_RE = re.compile(
    r"(?:^|\n)\s*(?:>|#|-{3,}+|<!--)*+\s*Penanda\s+D16\s*:|(?:^|\n)\s*#\s*D16\b")

# D18 lapis satu (GAYA-AHLI-1005 S14, putusan t_dbb77bfe M-03): DAFTAR TERTUTUP
# baris aparatus rumah. Bukan pembebas: vonis C-1/C-2 tetap mutlak terhadap
# total mentah (gate-options 8.3 tidak dilanggar); daftar ini hanya menjadi
# dasar baris INFO rincian (temuan aparatus vs temuan prosa) pada berkas
# berpenanda D16, sehingga vonis dapat dibaca tanpa menciptakan celah.
_APPARATUS_MD_LINE_RE = re.compile(
    r"^\s*(?:[-*>|#]+\s*)?(?:klasifikasi|kepemilikan|distribusi(?:\s+terkendali)?|"
    r"pita\s+klasifikasi|kop\s+klasifikasi)\s*[:=]\s*[^:]*$", re.IGNORECASE)
_APPARATUS_PROV_LINE_RE = re.compile(
    r"^\s*(?:[-*>|#]+\s*)?(?:provenans|provenance|basis\s+pin)\b[^\n]*$",
    re.IGNORECASE)


def _apparatus_line(line):
    """True bila baris termasuk daftar tertutup aparatus rumah (D18 lapis satu)."""
    return bool(_APPARATUS_MD_LINE_RE.search(line) or
                _APPARATUS_PROV_LINE_RE.search(line))

# Penanda blok terkendali kebijakan (kartu t_ec8bfdab; spesifikasi
# nat-s9hil-gate-options.md seksi 8). Sintaks mengikuti bentuk D16 (varian baris
# kutipan dan varian heading) supaya tidak menambah dialek baru. Skop SENGAJA
# per-blok (sampai heading berikutnya), berbeda dari D16 yang per-berkas.
POLICY_BLOCK_RE = re.compile(
    r"^\s*(?:>\s*|<!--\s*|-{3,}\s*)?\s*Penanda\s+Kebijakan\s*:\s*(\S.*?)\s*(?:-->)?\s*$"
    r"|^\s*#{1,6}\s+Kebijakan\s*:\s*(\S.*?)\s*$", re.IGNORECASE)
# Rujukan kartu tugas WAJIB pada alasan penanda (gate-options 8.1): penanda
# tanpa rujukan dianggap tidak sah dan seluruh check tetap jalan pada blok itu.
CARD_REF_RE = re.compile(r"\bt_[0-9a-zA-Z]{6,}\b")
# D18 lapis dua (GAYA-AHLI-1005 S14, putusan M-03): blok kutipan EKSTERNAL
# (surat/vendor/header forwarded) dengan rujukan sumber WAJIB. Sintaks mengikuti
# dialek penanda kebijakan (varian baris kutipan/heading/komentar HTML) supaya
# tidak menambah dialek baru; skop per-blok sampai heading berikutnya, sama
# seperti POLICY_BLOCK_RE. Rujukan sah = kartu t_xxxxxxxx ATAU alamat sumber
# eksternal (kata kunci sumber/from/pengirim/dari/arsip/verbatim, nama berkas,
# atau akun @). Tanpa salah satunya, penanda ditolak dan seluruh check tetap
# jalan pada blok itu (kelas aturan gate-options 8.1). Kelas yang dikecualikan:
# daftar hitam A4/A5/A6/A7/C-4 dan metrik B (I-5: prosa manusia/vendor bukan
# karya penulis GSP) - C-1/C-2/C-3/C-5 tetap tidak tersentuh.
D18_QUOTE_RE = re.compile(
    r"^\s*(?:>\s*|<!--\s*|-{3,}\s*)?\s*(?:Blok\s+Kutipan|Kutipan\s+Blok)"
    r"\s*:\s*(\S.*?)\s*(?:-->)?\s*$"
    r"|^\s*#{1,6}\s+(?:Blok\s+Kutipan|Kutipan\s+Blok)\s*:\s*(\S.*?)\s*$",
    re.IGNORECASE)
_D18_SRC_RE = re.compile(
    r"(?:\bt_[0-9a-zA-Z]{6,}\b|sumber\s*[:=]|from\s*[:=]|pengirim\s*[:=]"
    r"|dari\s*[:=]|arsip|verbatim|\.docx?\b|\.pdf\b|\.txt\b|\.md\b"
    r"|\.eml\b|\.msg\b|@)", re.IGNORECASE)
# Satu-satunya kode yang boleh dikecualikan oleh penanda blok (gate-options 8.3).
# A4/A6/A7 ikut karena baris C-4 adalah agregatnya per RT 5.2. C-1, C-2, C-3,
# C-5, C-10, dan A5 berada di luar daftar ini dan tetap dinilai penuh pada
# seluruh lapisan berkas (putusan nat-s9hil-putusan.md butir 1: mutlak).
POLICY_EXEMPT_CODES = frozenset((
    "A4", "A6", "A7", "C-4", "C-6", "C-7", "C-8", "C-8b", "C-9a", "C-9b",
    "C-9", "C-12", "C-13", "C-14", "C-15", "C-16", "C-17", "C-18", "C-19",
    "C-20", "C-21", "C-22", "C-23", "C-24", "C-25", "C-26", "C-27", "C-28",
    "C-33", "D-TA-09"))

# Marker naturalisasi C-10 (kartu t_19e648d4; cacat ukur gate-options seksi 3
# butir K-2). Bug lama: regex `naturalisasi\s*:\s*PASS` dibaca pada SELURUH
# lapisan terbaca sehingga kalimat yang MENJELASKAN format marker ikut dianggap
# marker (positif palsu; kelas bug pelajaran CHECK 9: alat ukur buta deskripsi
# inline). Posisi sah untuk deliverable:
#   1. baris frontmatter YAML dengan kunci `naturalisasi` bernilai PASS; atau
#   2. baris mandiri tempat marker adalah SELURUH isi baris, termasuk bentuk
#      baris tabel kaki: `naturalisasi: PASS (<skrip>, <tanggal>)` atau
#      `| naturalisasi: PASS | <skrip> | <tanggal> |`.
# Bukan posisi sah: penggalan di dalam kalimat prosa, blok kode berpagar
# (contoh pemakaian), sel tengah/belakang tabel penjelasan, dan baris yang
# memuat placeholder sudut <...> (placeholder = dokumentasi format, bukan
# nilai marker sungguhan).
MARKER_LINE_RE = re.compile(
    r"^naturalisasi\s*:\s*PASS(?:\s*\([^()<>]*\))?[.,;:]?$", re.IGNORECASE)


def _marker_line_ok(line):
    """True bila baris adalah marker utuh pada posisi sah (bukan penjelasan)."""
    s = line.strip()
    if not s or "<" in s:                     # placeholder sudut = dokumentasi
        return False
    if s.startswith("|"):
        cell = s.strip().strip("|").split("|")[0]
    else:
        cell = s
    return bool(MARKER_LINE_RE.match(cell.strip().strip("`*_")))


def find_naturalization_marker(doc):
    """Kembalikan label posisi marker sah pertama, atau None."""
    for line in (doc.frontmatter or "").split("\n"):
        if _marker_line_ok(line):
            return "frontmatter"
    for seg in doc.segments:
        if seg.origin == ORIGIN_CODE:
            continue                          # blok kode = contoh pemakaian
        for line in seg.text.split("\n"):
            if _marker_line_ok(line):
                return seg.label
    return None


# ---------------------------------------------------------------------------
# Daftar hitam frasa (C-4 = A4/A6/A7; A5 dilaporkan terpisah)
# ---------------------------------------------------------------------------
# M-17 (GAYA-AHLI-1005 S14, putusan t_dbb77bfe): daftar hitam ini TIDAK boleh
# diperluas dengan kelas penguat (holistik, sinergi, terdepan, sangat+adjektif,
# dll.) maupun kemubaziran sinonim. Bukti G3: manusia memakai penguat LEBIH padat
# dari fleet (0,76 vs 0,51 per 1.000 kata) sehingga kelas itu tanpa daya pisah -
# menagihnya = positif palsu sistematis (kelas cacat M-14). Aturan benar untuk
# penguat: tagih angkanya (densitas B4), jangan hapus katanya (D-06). Probe
# 05-10: keenam kata itu memang tidak ada di daftar mana pun hari ini.
BLACKLIST_A4 = [
    "hope this helps", "just let me know", "let me know if", "feel free to ask",
    "as an ai", "i am an ai", "as a large language model", "happy to help",
    "great question", "sure! here", "certainly! here",
    "semoga membantu", "jangan ragu bertanya", "jangan ragu untuk bertanya",
    "berikut adalah rangkuman", "tentu saja! berikut", "dengan senang hati",
    "terima kasih atas pertanyaan anda", "pertanyaan yang bagus",
    "sebagai model bahasa", "sebagai ai",
]
BLACKLIST_A6 = [
    "demikianlah pembahasan", "dengan demikian dapat disimpulkan bahwa",
    "dapat disimpulkan bahwa", "kesimpulan: langkah ini penting",
    "in conclusion, it can be said that", "to summarize the above",
    "sebagai penutup, dapat dikatakan", "akhir kata, demikianlah",
]
BLACKLIST_A7 = [
    "di era digital yang berkembang pesat", "di era digital ini",
    "di era modern ini", "seiring perkembangan teknologi",
    "seiring perkembangan zaman", "tidak dapat dipungkiri bahwa",
    "perlu dipahami bahwa", "in the rapidly evolving landscape",
    "it is important to note that", "dalam era globalisasi",
]
# A5: label ruang kerja / fungsi internal yang bocor ke narasi (RT M-5, contract:16).
BLACKLIST_A5 = [
    "scratchpad", "todo for me", "dispatch hq", "delegate_task", "my workspace folder",
    "workspace scratch",
]
_A5_CODE_NAMES = ["kanban" + "_complete", "kanban" + "_comment", "kanban" + "_block",
                  "skill" + "_view(", "kanban" + "_create"]
# B4: kosakata AI-typical ID (H.4.4) + blacklist EN (H.6.1), versi non-pembuka.
BLACKLIST_B4 = [
    "hal ini dikarenakan", "merupakan hal yang penting", "sangat signifikan",
    "dalam rangka", "terkait dengan", "perlu diingat bahwa",
    "this demonstrates the importance of", "there are several factors to consider",
    "has the potential to", "furthermore", "moreover", "in addition,",
    "baru-baru ini", "akhir-akhir ini",
    # NAT-GATE-R2 (30-09): H.1.2 butir 2 melarang 'Penulis' sebagai rujukan diri
    # sejak awal standar, tetapi kata itu tidak pernah masuk daftar hitam mana pun
    # (bukti: LAPORAN-ADINT penulis=8, lolos semua check). Densitas ambang B4
    # (<=1/1.000 kata) menahan pemakaian sah ('penulis buku terkenal').
    "oleh penulis", "penulis buka", "penulis tulis", "penulis catat",
    "penulis rekomendasi", "bagi penulis", "menurut penulis",
]
# B5: transisi per kategori (Module H.3.4). Share > 60% satu jenis = monoton.
TRANSITION_GROUPS = {
    "tambah": ["selanjutnya", "selain itu", "di samping itu", "lebih lanjut",
               "furthermore", "moreover", "in addition"],
    "kontras": ["namun", "akan tetapi", "di sisi lain", "sebaliknya", "however"],
    "sebab-akibat": ["karena itu", "dengan demikian", "oleh karena itu", "maka"],
    "elaborasi": ["dengan kata lain", "artinya", "dalam hal ini"],
    "penekanan": ["justru", "terlebih", "apalagi", "paling penting"],
}
HEDGE_WORDS = ["dapat", "mungkin", "berpotensi", "diprediksi", "cenderung"]
LIMITATION_WORDS = ["keterbatasan", "batasan", "kekurangan", "risiko", "asumsi",
                    "belum termasuk", "belum memasukkan", "di luar cakupan",
                    "tidak mencakup", "tidak termasuk", "belum terverifikasi",
                    "limitation"]

# Kanal (RT seksi 3.1 / D-TA-05).
CHANNELS = {
    "chat": "K1 chat ke user (formal-effisien)",
    "doc": "K2 dokumen dan laporan (formal institusional)",
    "deck": "K3 deck presentasi (formal institusional)",
    "notif": "K4 notifikasi cron / gateway (formal-netral)",
    "kanban": "K5 ringkasan handoff dan komentar kanban",
    "etalase": "K6 artefak etalase / paket serah terima",
    "kitab": "K7 naskah panjang gaya kitab (audiens remaja)",
    "standar": "K8 naskah standar normatif rumah (gerbang yang menegakkan, bukan prosa biasa)",
    "sosmed": "media sosial / konten kreatif (parsial, D-TA-08)",
}
CHANNEL_ALIASES = {
    "k1": "chat", "k2": "doc", "k3": "deck", "k4": "notif", "k5": "kanban",
    "k6": "etalase", "k7": "kitab", "k8": "standar", "normatif": "standar",
    "sosial-media": "sosmed", "media-sosial": "sosmed",
    "dokumen": "doc", "notifikasi": "notif", "presentasi": "deck",
    "buku": "kitab", "naskah": "kitab",
}
SHORT_CHANNELS = ("chat", "notif")            # D-TA-05: metrik panjang/marker mati
HIGH_INDICATORS = ("B1", "B2", "B3", "B8")    # severity HIGH menurut Module H.6.2
# K7 kanal kitab (PUTUSAN t_77fd88c3 butir 5): indikator berat kelas kepadatan gaya
# yang bertabrakan dengan genre buku pelajaran DIRUNTUHKAN menjadi INFO pada kanal
# kitab - tetap tercetak dengan alasan eksplisit, tidak memicu triggered[], sehingga
# tidak masuk agregasi D-TA-09. C-6/B1 dan C-16/B14 tidak diruntuhkan: dibalik arah
# menjadi plafon atas (lihat _KITAB_AVG_CEILING).
KITAB_DEMOTE_CODES = frozenset(("B2", "B6", "B10", "B11", "B13"))
# K8 kanal standar (PUTUSAN t_eec55819 06-10-2026, misi GAYA-AHLI-1005 KAL2):
# naskah standar normatif rumah yang badan aturannya MENDEFINISIKAN namespace
# kode sendiri dan MENEGAKKAN standar lain (kelas STD-*/SOP/KAK). Kanal aditif:
# delta perilaku terhadap doc HANYA dua (C-7 rasio, C-8 residu label), keduanya
# cetak alasan eksplisit. Eligibilitas ditegakkan controller sebelum sapuan
# (norma I-4), bukan oleh scanner. Tidak ada demosi B-code ala kitab.
STANDAR_SHORT_RATIO = 0.20   # C-7 kanal standar: paragraf <3 kalimat <= 20% total
# Kosakata tertutup kepala bidang skema S-2 (PUTUSAN t_eec55819 seksi 2(a)
# butir 3): konstanta scanner, TIDAK dibaca dari dokumen - tidak ada celah
# swa-deklarasi oleh objek yang diukur. Perluasan hanya lewat jalur M-6.
STANDAR_FIELD_LABELS = frozenset((
    "Pernyataan", "Fungsi bagi pembaca", "Bukti manusia",
    "Kontras fleet", "Instrumen penegak", "Predikat verifikasi",
))
SELF_NAME = "scan_ai_footprint.py"

ORIGIN_PROSE = "prose"
ORIGIN_CODE = "code"
ORIGIN_META = "metadata"
ORIGIN_TABLE = "table"
ORIGIN_HEADING = "heading"   # judul bukan kalimat prosa: ikut sapuan karakter,
                             # tetapi tidak dihitung pada metrik panjang (H.2.1)


class Seg(object):
    """Sepotong teks hasil ekstraksi beserta lapisan asalnya (bahan pengecualian)."""

    __slots__ = ("text", "origin", "label")

    def __init__(self, text, origin, label):
        self.text = text
        self.origin = origin
        self.label = label


class Doc(object):
    def __init__(self, name, fmt):
        self.name = name
        self.fmt = fmt
        self.segments = []     # lapisan terbaca manusia -> metrik prosa
        self.raw = ""          # lapisan mentah (sumber byte/entity) -> hitung C-1/C-2
        self.frontmatter = ""
        self.supports_prose = True
        self.notes = []
        self.media_count = None   # objek gambar tertanam (docx/pptx; None = tak dinilai)
        # PUTUSAN-HEUR-1009 butir 3 + temuan pendamping (docx saja; format lain
        # kosong -> seluruh perilaku lama identik):
        # prose_mono: sejajar indeks segmen PROSA -> (body_non_mono, mono_str) atau
        #   None bila paragraf tidak memuat run monospace. Dipakai HANYA oleh
        #   lapisan penilaian C-13 (setara backtick markdown).
        # gloss_headings: indeks segmen paragraf bergaya heading Word.
        self.prose_mono = []
        self.gloss_headings = set()

    def add(self, text, origin, label):
        if text:
            self.segments.append(Seg(text, origin, label))

    def readable_text(self):
        return "\n".join(s.text for s in self.segments)

    def prose_text(self, scan_code=False, strip_fn=None):
        """Hanya lapisan prosa (dan kode bila diminta): judul, tabel, dan nilai mesin
        dikecualikan dari metrik panjang/kepadatan H.2.1-H.6.2, tetapi tetap ikut
        sapuan karakter C-1/C-2 lewat readable_text().

        strip_fn (PUTUSAN-HEUR-1009 butir 3): fungsi (indeks_segmen_prosa, teks)
        -> teks, dipakai HANYA oleh lapisan penilaian C-13 untuk mengosongkan run
        monospace docx (setara backtick markdown). None = lapisan utuh seperti
        sebelumnya (regresi byte-identik untuk semua pemanggil lama).
        """
        keep = (ORIGIN_PROSE,)
        out = []
        idx = 0
        for s in self.segments:
            if s.origin in keep:
                txt = strip_fn(idx, s.text) if strip_fn is not None else s.text
                idx += 1
                if txt:
                    out.append(txt)
        if scan_code:
            out += [s.text for s in self.segments if s.origin == ORIGIN_CODE]
        return "\n".join(out)

    def d16_exempt(self):
        return bool(D16_MARKER_RE.search(self.raw) or
                    D16_MARKER_RE.search(self.readable_text()))


def _code_of(nama):
    """Kode check dari nama baris ('C-9a kosakata ...' -> 'C-9a')."""
    return nama.split(" ", 1)[0]


def policy_block_flags(doc):
    """Tandai segmen hasil ekstraksi yang berada dalam blok berpenanda kebijakan.

    Penanda membuka blok sampai heading berikutnya (skop per-blok, gate-options
    8.2). Penanda tanpa rujukan kartu (t_xxxxxxxx) dicatat tidak sah dan tidak
    membuka blok (gate-options 8.1): seluruh check pada segmen itu tetap jalan.
    """
    in_block = False
    valid_here = None
    flags = []
    invalid = []
    for seg in doc.segments:
        blocked = False
        for ln in seg.text.split("\n"):
            s = ln.strip()
            if s.startswith("#"):
                if valid_here is not None and not CARD_REF_RE.search(valid_here):
                    invalid.append(valid_here[:70])
                in_block = False
                valid_here = None
            m = POLICY_BLOCK_RE.match(ln)
            if m:
                if valid_here is not None and not CARD_REF_RE.search(valid_here):
                    invalid.append(valid_here[:70])
                reason = (m.group(1) or m.group(2) or "").strip()
                in_block = bool(CARD_REF_RE.search(reason))
                valid_here = reason if in_block else None
                if not in_block:
                    invalid.append(reason[:70])
                blocked = in_block
        if in_block:
            blocked = True
        flags.append(blocked)
    return flags, sorted(set(invalid))


def outside_policy_text(doc, flags, origins, strip_fn=None):
    """Gabungan segmen ber-asal `origins` yang TIDAK berada dalam blok sah.

    strip_fn (opsional, PUTUSAN-HEUR-1009): dipanggil dengan indeks segmen PROSA
    yang sama seperti prose_text() agar kedua lapisan C-13 konsisten.
    """
    out = []
    n = 0
    for seg, fl in zip(doc.segments, flags):
        i = -1
        if seg.origin == ORIGIN_PROSE:
            i = n
            n += 1
        if (not fl) and seg.origin in origins:
            txt = seg.text
            if strip_fn is not None and i >= 0:
                txt = strip_fn(i, txt)
            if txt:
                out.append(txt)
    return "\n".join(out)


def outside_paragraphs(doc, flags, scan_code):
    """Paragraf prosa di luar blok berpenanda (blok penanda memotong grup)."""
    paras, buf = [], []
    for seg, fl in zip(doc.segments, flags):
        keep = ((seg.origin == ORIGIN_PROSE) or
                (scan_code and seg.origin == ORIGIN_CODE))
        if (not keep) or fl:
            if buf:
                paras.append(" ".join(buf))
                buf = []
            continue
        if seg.text.strip():
            buf.append(seg.text.strip())
        elif buf:
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))
    return [p for p in paras if words_of(p)]


def quote_block_flags(doc):
    """Tandai segmen dalam blok kutipan EKSTERNAL berpenanda D18 lapis dua.

    GAYA-AHLI-1005 S14 (putusan t_dbb77bfe M-03): prosa surat masuk manusia /
    header forwarded milik paket vendor bukan karya penulis GSP (cacat I-5),
    tetapi blok tanpa rujukan sumber tetap tidak sah dan seluruh check jalan
    apa adanya (kelas aturan gate-options 8.1). Skop per-blok sampai heading
    berikutnya, sama seperti POLICY_BLOCK_RE. Rujukan sah: kartu t_xxxxxxxx,
    kata kunci sumber/from/pengirim/dari, kata arsip/verbatim, nama berkas,
    atau akun @ (lihat _D18_SRC_RE).
    """
    in_block = False
    valid_here = None
    flags = []
    invalid = []
    for seg in doc.segments:
        blocked = False
        for ln in seg.text.split("\n"):
            s = ln.strip()
            if s.startswith("#"):
                if valid_here is not None and not _D18_SRC_RE.search(valid_here):
                    invalid.append(valid_here[:70])
                in_block = False
                valid_here = None
            m = D18_QUOTE_RE.match(ln)
            if m:
                if valid_here is not None and not _D18_SRC_RE.search(valid_here):
                    invalid.append(valid_here[:70])
                reason = (m.group(1) or m.group(2) or "").strip()
                in_block = bool(_D18_SRC_RE.search(reason))
                valid_here = reason if in_block else None
                if not in_block:
                    invalid.append(reason[:70])
                blocked = in_block
        if in_block:
            blocked = True
        flags.append(blocked)
    return flags, sorted(set(invalid))


# ---------------------------------------------------------------------------
# Ekstraksi per format (matriks ai-footprint-sweep.md:17-25)
# ---------------------------------------------------------------------------
def split_frontmatter(text):
    """Pisahkan frontmatter YAML/Markdown. Frontmatter dikecualikan dari metrik
    prosa TETAPI tetap ikut dihitung untuk U+2014/U+00B7 (ia tinggal di doc.raw)."""
    if text.startswith(chr(0xFEFF)):
        text = text[1:]
    m = re.match(r"^---[ \t]*\r?\n", text)
    if not m:
        return "", text
    end = text.find("\n---", m.end())
    if end == -1:
        return "", text
    nl = text.find("\n", end + 1)
    if nl == -1:
        return text[m.end():end + 1], ""
    return text[m.end():nl], text[nl + 1:]


def extract_plain(name, text):
    doc = Doc(name, "md" if name.lower().endswith((".md", ".markdown")) else "txt")
    doc.raw = text
    fm, body = split_frontmatter(text)
    doc.frontmatter = fm
    in_code = False
    fence = ""
    for line in body.split("\n"):
        stripped = line.strip()
        if not in_code and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_code = True
            fence = stripped[:3]
            continue
        if in_code and stripped.startswith(fence):
            in_code = False
            continue
        if in_code:
            doc.add(line, ORIGIN_CODE, "fenced-code")
        elif stripped.startswith("|"):
            doc.add(line, ORIGIN_TABLE, "table")
        elif stripped.startswith("#"):
            doc.add(line, ORIGIN_HEADING, "heading")
        else:
            doc.add(line, ORIGIN_PROSE, "prose")
    return doc


def extract_html(name, text):
    doc = Doc(name, "html")
    doc.raw = text

    # NAT-GATE-R4 (05-10-2026, temuan kalibrasi artefak rekap): isi <style> dan
    # <script> adalah kode (P-3 RT 3.2), bukan prosa. Tanpa pembuangan ini,
    # deklarasi CSS `body { font-family: Segoe UI; margin: 0; }` terhitung
    # kalimat dan menjatuhkan vonis palsu C-6/C-7 (terukur: dokumen uji dengan
    # prosa asli 26 kata/kalimat terbaca 15,7). Atribut tag (onclick, alt) tetap
    # lewat parser karena handle_starttag tidak mengambilnya.
    text = re.sub(r"(?is)<(style|script)\b.*?</\1\s*>", " ", text)

    class _TextGrab(html.parser.HTMLParser):
        # NAT-GATE-R4 lanjutan (05-10-2026): isi <table> dan <title>/<head> bukan
        # prosa. Tanpa pemisahan ini seluruh sel satu tabel besar tergabung
        # menjadi 'kalimat' raksasa (terukur 478 kata pada artefak rekap) dan
        # judul dokumen ikut metrik panjang - kelas cacat yang sama dengan
        # ekstraksi PDF yang sudah diberi guard. Padanan perilaku pemecah
        # markdown/docx yang menandai tabel sebagai lapisan sendiri.
        def __init__(self):
            html.parser.HTMLParser.__init__(self, convert_charrefs=True)
            self.chunks = []
            self.meta_chunks = []
            self.table_chunks = []
            self._in_meta = 0
            self._in_table = 0

        def handle_starttag(self, tag, attrs):
            if tag in ("title", "head", "noscript", "template"):
                self._in_meta += 1
            elif tag == "table":
                self._in_table += 1

        def handle_endtag(self, tag):
            if tag in ("title", "head", "noscript", "template") and self._in_meta:
                self._in_meta -= 1
            elif tag == "table" and self._in_table:
                self._in_table -= 1

        def handle_data(self, data):
            if self._in_meta:
                self.meta_chunks.append(data)
            elif self._in_table:
                self.table_chunks.append(data)
            else:
                self.chunks.append(data)

    try:
        grab = _TextGrab()
        grab.feed(text)
        grab.close()
        body = "\n".join(c for c in grab.chunks if c.strip())
        doc.add(body, ORIGIN_PROSE, "text-node")
        doc.add("\n".join(c for c in grab.table_chunks if c.strip()),
                ORIGIN_TABLE, "table-node")
        doc.add("\n".join(c for c in grab.meta_chunks if c.strip()),
                ORIGIN_META, "head-node")
    except Exception as exc:                     # HTML rusak: fallback teks mentah
        doc.notes.append("HTMLParser gagal (%s): pakai teks mentah" % type(exc).__name__)
        doc.add("\n".join(c for c in [text] if c.strip()), ORIGIN_PROSE, "text-node")
    return doc


def extract_json(name, text):
    doc = Doc(name, "json")
    doc.raw = text
    doc.supports_prose = False
    try:
        obj = json.loads(text)
    except Exception as exc:
        doc.notes.append("JSON tidak valid (%s): dihitung sebagai teks mentah"
                         % type(exc).__name__)
        doc.add(text, ORIGIN_META, "json-raw")
        return doc

    def walk(node, key=""):
        if isinstance(node, dict):
            for k in sorted(node.keys()):
                walk(node[k], k)
        elif isinstance(node, list):
            for item in node:
                walk(item, key)
        elif isinstance(node, str):
            # D-TA-07: nilai di bawah kunci mesin bukan prosa untuk dibaca manusia.
            meta = bool(re.search(r"sha|hash|path|uuid|token|_id$|^id$|time|date|"
                                  r"metadata|timestamp", key, re.IGNORECASE))
            doc.add(node, ORIGIN_META if meta else ORIGIN_PROSE, "json:" + key)

    walk(obj)
    if any(s.origin == ORIGIN_PROSE for s in doc.segments):
        doc.supports_prose = True
    return doc


def extract_py(name, text):
    doc = Doc(name, "py")
    doc.raw = text
    doc.supports_prose = False
    try:
        strings, comments = [], []
        with io.BytesIO(text.encode("utf-8")) as fh:
            for tok in tokenize.tokenize(fh.readline):
                if tok.type == tokenize.STRING:
                    strings.append(tok.string)
                elif tok.type == tokenize.COMMENT:
                    comments.append(tok.string)
        doc.add("\n".join(comments), ORIGIN_CODE, "py-comment")
        doc.add("\n".join(strings), ORIGIN_CODE, "py-string")
        doc.notes.append("kode sumber dikecualikan dari metrik prosa (RT 3.2); "
                         "literal + escape tetap dihitung (kasus emitter sweep)")
    except Exception as exc:
        doc.notes.append("tokenize gagal (%s): dihitung sebagai teks mentah"
                         % type(exc).__name__)
        doc.add(text, ORIGIN_CODE, "py-raw")
    return doc


def _zip_xml_parts(path, data=None):
    """Gabungan seluruh part XML arsip Office, termasuk core properties."""
    out = []
    try:
        src = open(path, "rb") if path else io.BytesIO(data)
    except Exception as exc:
        return "ZIP-ERROR %s" % exc
    with src as fh:
        try:
            with zipfile.ZipFile(fh) as zf:
                for nm in sorted(zf.namelist()):
                    if nm.lower().endswith((".xml", ".rels")):
                        try:
                            out.append(zf.read(nm).decode("utf-8", "replace"))
                        except Exception:
                            pass
        except Exception as exc:
            out.append("ZIP-ERROR %s" % exc)
    return "\n".join(out)


def zip_media_count(path=None, data=None):
    """Hitung objek gambar tertanam pada paket docx/pptx (word/media, ppt/media).

    NAT-GATE-R2 C-21: kepala 'Gambar k.n' tanpa objek tertanam = janji visual
    kosong (bukti RAFIF-MOBILE: 0 media di docx 385 halaman). None bila paket
    tidak bisa dibuka (laporkan, jangan vonis).
    """
    try:
        zf = zipfile.ZipFile(path) if path else zipfile.ZipFile(io.BytesIO(data))
        with zf:
            names = zf.namelist()
        return sum(1 for n in names
                   if n.startswith(("word/media/", "ppt/media/"))
                   and not n.endswith("/"))
    except Exception:
        return None


_MONO_FONT_RE = re.compile(r"mono|courier|consolas", re.IGNORECASE)


def _run_font_names(run):
    """Nama font yang dinyatakan sebuah run docx (rPr langsung saja; terukur pada
    artefak Rev A DDV: 94/94 run mono menyatakan nama langsung di rPr, pewarisan
    tingkat gaya tidak dipakai jalur DATUM)."""
    names = []
    try:
        if run.font and run.font.name:
            names.append(run.font.name)
    except Exception:
        pass
    try:
        from docx.oxml.ns import qn
        rpr = run._element.find(qn("w:rPr"))
        if rpr is not None:
            rf = rpr.find(qn("w:rFonts"))
            if rf is not None:
                for attr in ("w:ascii", "w:hAnsi", "w:cs"):
                    v = rf.get(qn(attr))
                    if v:
                        names.append(v)
    except Exception:
        pass
    return names


def _para_split_mono(para):
    """(body_non_mono, mono_str) satu paragraf docx, level RUN: run monospace
    keluar dari penilaian C-13, run serif/sans tetap dinilai penuh - setara
    backtick markdown yang hanya mengosongkan rentang backtick, bukan seluruh
    paragraf (terukur: Rev A 25 dan EOSRAY 23 paragraf campuran mono+nonmono)."""
    keep, mono = [], []
    try:
        runs = list(para.runs)
    except Exception:
        runs = []
    for rr in runs:
        t = rr.text or ""
        if not t:
            continue
        if any(_MONO_FONT_RE.search(fn) for fn in _run_font_names(rr)):
            mono.append(t)
        else:
            keep.append(t)
    return "".join(keep), " ".join(mono)


def _para_style_is_heading(para):
    """Paragraf bergaya heading Word: styleId 'Heading1'..'Heading9' atau nama
    'Heading N'/padanan lokal 'Judul N' (temuan pendamping PUTUSAN-HEUR-1009:
    pencocok heading markdown tidak pernah aktif pada lapisan docx)."""
    try:
        st = para.style
        sid = (st.style_id or "") if st is not None else ""
        nm = (st.name or "") if st is not None else ""
    except Exception:
        return False
    return bool(re.match(r"(?i)^heading[ _-]?[1-9]$", sid)
                or re.match(r"(?i)^(heading|judul)\s+[1-9]$", nm))


def extract_docx(name, data, path=None):
    doc = Doc(name, "docx")
    try:
        import docx
        d = docx.Document(path) if path else docx.Document(io.BytesIO(data))
        for para in d.paragraphs:
            # PUTUSAN-HEUR-1009 butir 3 + temuan pendamping: run monospace
            # dicatat terpisah (keluar HANYA dari lapisan C-13); paragraf bergaya
            # heading Word dicatat sebagai pembuka/penutup blok glosarium. Jalur
            # isi sel tabel tidak tersentuh (kelas data, bukan prosa).
            body, mono_txt = _para_split_mono(para)
            before = len(doc.segments)
            doc.add(para.text, ORIGIN_PROSE, "docx-paragraph")
            if len(doc.segments) > before:
                si = len(doc.segments) - 1
                doc.prose_mono.append(
                    (body, mono_txt) if mono_txt else None)
                if (para.text or "").strip() and _para_style_is_heading(para):
                    doc.gloss_headings.add(si)
        for tbl in d.tables:
            for row in tbl.rows:
                for cell in row.cells:
                    doc.add(cell.text, ORIGIN_TABLE, "docx-cell")
        cp = d.core_properties
        for attr in ("title", "subject", "author", "comments", "keywords",
                     "category", "last_modified_by"):
            doc.add(getattr(cp, attr, "") or "", ORIGIN_META, "core:" + attr)
    except Exception as exc:
        doc.supports_prose = False
        doc.notes.append("python-docx tidak tersedia/gagal (%s): fallback seluruh part "
                         "XML termasuk core properties" % type(exc).__name__)
    doc.raw = _zip_xml_parts(path, data)
    doc.media_count = zip_media_count(path, data)
    return doc


def extract_pptx(name, data, path=None):
    doc = Doc(name, "pptx")
    try:
        import pptx
        prs = pptx.Presentation(path) if path else pptx.Presentation(io.BytesIO(data))
        for idx, slide in enumerate(prs.slides, 1):
            for shape in slide.shapes:
                if getattr(shape, "has_text_frame", False):
                    for para in shape.text_frame.paragraphs:
                        doc.add("".join(r.text for r in para.runs),
                                ORIGIN_PROSE, "pptx-run s%d" % idx)
            if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
                doc.add(slide.notes_slide.notes_text_frame.text,
                        ORIGIN_PROSE, "pptx-notes s%d" % idx)
        cp = prs.core_properties
        for attr in ("title", "subject", "author", "comments", "keywords"):
            doc.add(getattr(cp, attr, "") or "", ORIGIN_META, "core:" + attr)
    except Exception as exc:
        doc.supports_prose = False
        doc.notes.append("python-pptx tidak tersedia/gagal (%s): fallback seluruh part "
                         "XML termasuk core properties" % type(exc).__name__)
    doc.raw = _zip_xml_parts(path, data)
    doc.media_count = zip_media_count(path, data)
    return doc


def extract_xlsx(name, data, path=None):
    doc = Doc(name, "xlsx")
    doc.supports_prose = False          # isi sel = data, bukan paragraf prosa
    try:
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                for val in row:
                    if isinstance(val, str):
                        doc.add(val, ORIGIN_META, "xlsx-cell")
        wb.close()
    except Exception as exc:
        doc.notes.append("openpyxl tidak tersedia/gagal (%s): fallback seluruh part XML"
                         % type(exc).__name__)
    doc.raw = _zip_xml_parts(path, data)
    return doc


def extract_pdf(name, data):
    doc = Doc(name, "pdf")
    doc.supports_prose = False
    text = None
    used = None
    for mod in ("pypdf", "PyPDF2"):
        try:
            m = __import__(mod)
            reader = m.PdfReader(io.BytesIO(data))
            text = "\n".join((pg.extract_text() or "") for pg in reader.pages)
            used = mod
            break
        except Exception:
            text = None
    if text is None:
        raw = data.decode("latin-1", "replace")
        doc.raw = raw
        doc.notes.append("pypdf/PyPDF2 tidak terpasang: fallback byte mentah. Hanya "
                         "bentuk literal/escape/entity yang terbukti; lapisan teks "
                         "berbasis glyph/custom-encoding TIDAK terbukti (laporkan "
                         "sebagai NEEDS_REVIEW manusia, bukan PASS penuh)")
        return doc
    doc.raw = text
    doc.add(text, ORIGIN_META, "pdf-text")
    doc.notes.append("lapisan teks via %s (%d halaman); footer cetak ikut terhitung"
                     % (used, len(reader.pages)))
    return doc


def scan_one(path, opts):
    name = os.path.basename(path)
    ext = os.path.splitext(name)[1].lower()
    with open(path, "rb") as fh:
        data = fh.read()
    if ext in (".md", ".markdown", ".txt", ".text", ".rst", ".csv", ".log"):
        return extract_plain(name, data.decode("utf-8", "replace"))
    if ext in (".html", ".htm", ".xml"):
        return extract_html(name, data.decode("utf-8", "replace"))
    if ext == ".json":
        return extract_json(name, data.decode("utf-8", "replace"))
    if ext in (".py", ".pyi"):
        return extract_py(name, data.decode("utf-8", "replace"))
    if ext == ".docx":
        return extract_docx(name, data, path)
    if ext == ".pptx":
        return extract_pptx(name, data, path)
    if ext in (".xlsx", ".xlsm"):
        return extract_xlsx(name, data, path)
    if ext == ".pdf":
        return extract_pdf(name, data)
    # biner tak dikenal (png, zip, dll): tidak di-scan - matriks sweep baris 25
    doc = Doc(name, ext or "biner")
    doc.supports_prose = False
    doc.raw = ""
    doc.notes.append("format %s tidak di-scan; gunakan berkas pendamping .md "
                     "(matriks sweep baris 25)" % (ext or "biner"))
    return doc


# ---------------------------------------------------------------------------
# Metrik prosa (bahasa Indonesia-first)
# ---------------------------------------------------------------------------
_ABBREV = ("dll.", "dsb.", "dst.", "vs.", "etc.", "hlm.", "hal.", "no.", "dr.",
           "prof.", "ta.", "sda.", "wib.", "utc.", "a.m.", "p.m.", "e.g.", "i.e.")
_WORD_RE = re.compile(r"[0-9A-Za-z\u00c0-\u02ff\u0370-\u03ff'\-/]+")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[\"'\(\[]?[A-Z\u00c0-\u02ff]|\(\d{1,3}\))")


def words_of(text):
    return [w for w in _WORD_RE.findall(text) if re.search(r"[0-9A-Za-z]", w)]


def sentences_of(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    parts, buf = [], ""
    for chunk in _SENT_SPLIT.split(text):
        if not chunk:
            continue
        if buf:
            tail = buf.rstrip().lower()
            if tail.endswith(_ABBREV) or re.search(r"\d+\.\d+$", tail):
                buf = buf + " " + chunk
                continue
            parts.append(buf)
        buf = chunk
    if buf:
        parts.append(buf)
    return [p for p in parts if words_of(p)]


def prose_paragraphs(doc, scan_code):
    """Grupkan baris prosa berurutan menjadi paragraf; tabel/kode memotong grup."""
    paras, buf = [], []
    for seg in doc.segments:
        keep = seg.origin == ORIGIN_PROSE or (scan_code and seg.origin == ORIGIN_CODE)
        if not keep:
            if buf:
                paras.append(" ".join(buf))
                buf = []
            continue
        if seg.text.strip():
            buf.append(seg.text.strip())
        elif buf:
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))
    return [p for p in paras if words_of(p)]


# ---------------------------------------------------------------------------
# Helper hitung
# ---------------------------------------------------------------------------
class Result(object):
    def __init__(self):
        self.rows = []   # daftar (status, nama, detail)

    def add(self, status, nama, detail=""):
        self.rows.append((status, nama, detail))


def count_forms(raw):
    """Hitung tiap bentuk penulisan pada SATU lapisan mentah.

    Lapisan mentah dipakai sebagai sumber tunggal agar satu kemunculan tidak dihitung
    dua kali (mis. entity HTML yang sudah ter-decode di text node). Frontmatter ikut
    lapisan ini sehingga tetap terhitung untuk C-1/C-2.

    Bentuk literal + escape + entity dihitung pada SEMUA format. Keputusan kartu
    NAT-S9 menyebut ketiganya tanpa pembatasan format, dan corpus merah NAT-S10 boleh
    menaruh kasus escape di berkas .md; matriks sweep baris 20-21 hanya menyebut
    bentuk escape sebagai tambahan wajib, bukan pengecualian untuk .md/.txt.
    """
    return {
        "em_lit": len(EM_LITERAL_RE.findall(raw)),
        "em_esc": sum(len(rx.findall(raw)) for rx in EM_FORM_RES),
        "md_lit": len(MD_LITERAL_RE.findall(raw)),
        "md_esc": sum(len(rx.findall(raw)) for rx in MD_FORM_RES),
        "en_all": raw.count(EN_DASH),
        "en_range": len(EN_DASH_RANGE_RE.findall(raw)) +
                    len(EN_DASH_RANGE_RE.findall(html.unescape(raw))),
    }


_BL_RX_CACHE = {}


def _blacklist_rx(p):
    """Regex berbatas kata untuk satu frasa daftar hitam (FIX M-05, kartu S14).

    Batas kata memakai lookaround alfanumerik (bukan \b ASCII murni) agar aman
    pada kata Indonesia berimbuhan, antar-token dipakai \\s+ (tanda seru dan
    koma intra-frasa seperti 'sure! here' / 'in addition,' tetap utuh sebagai
    literal), dan lookaround hanya dipasang pada ujung yang berhuruf/angka.
    """
    toks = [re.escape(x) for x in re.split(r"\s+", p.strip().lower()) if x]
    body = r"\s+".join(toks)
    pat = ""
    if toks and re.match(r"[0-9A-Za-z]", toks[0]):
        pat += r"(?<![\w])"
    pat += body
    if toks and re.match(r"[0-9A-Za-z]", toks[-1]):
        pat += r"(?![\w])"
    return re.compile(pat)


def frasa_hits(text, phrases):
    # FIX M-05 (kartu S14, putusan t_dbb77bfe): pencocokan substring murni `in`
    # menghasilkan positif palsu kelas I-1 - 'as an ai' tertangkap di dalam
    # 'such as an aisle' (kasus nyata RAFIF-ED2, papan CH17) dan vonis A4 masuk
    # jalur absolut() sehingga mampu menggagalkan rilis dokumen benar. Setiap
    # frasa kini regex berbatas kata; cache isi-only deterministik (kunci =
    # teks frasa, tanpa waktu/acak) menjaga dua run byte-identik.
    low = re.sub(r"[*_`]", "", text.lower())
    out = []
    for p in sorted(set(phrases)):
        rx = _BL_RX_CACHE.get(p)
        if rx is None:
            rx = _BL_RX_CACHE[p] = _blacklist_rx(p)
        if rx.search(low):
            out.append(p)
    return out


def rate_per_1000(count, nwords):
    return 0.0 if nwords <= 0 else (count * 1000.0 / nwords)


def emoji_count(text):
    n = 0
    for ch in text:
        o = ord(ch)
        if (0x1F000 <= o <= 0x1FAFF) or (0x2600 <= o <= 0x27BF) or o in (0xFE0F, 0x20E3):
            n += 1
        elif o in (0x2B50, 0x2B55, 0x2705, 0x274C, 0x203C, 0x2049, 0x2764):
            n += 1
    return n


_ITALIC_STAR = re.compile(r"(?<![\w*])\*([^*\n]{1,60})\*(?![\w*])")
_ITALIC_UND = re.compile(r"(?<![\w_])_([^_\n]{1,60})_(?![\w_])")


def italic_terms(text):
    out = []
    for rx in (_ITALIC_STAR, _ITALIC_UND):
        for m in rx.finditer(text):
            term = m.group(1).strip()
            if term and len(words_of(term)):
                out.append(term)
    return out


def is_product_or_standard(term):
    """Nama produk / standar internasional: huruf kapital di depan + digit atau ALLCAPS."""
    return bool(re.match(r"^(?:[A-Z]{2,}[A-Za-z0-9./+-]*|[A-Z][A-Za-z-]+\s+\d[\w.]*)$",
                         term.strip()))


def vertical_bold_runs(paras):
    best = run = 0
    for p in paras:
        if re.match(r"^(?:[-*+]|\d+\.)?\s*\*\*[^*]+\*\*[:.]?\s*$", p.strip()):
            run += 1
            best = max(best, run)
        else:
            run = 0
    return best


# ---------------------------------------------------------------------------
# NAT-HIL-E1 (kartu t_c79b5f6d): indikator berat B10 gaya catatan cepat.
# Bukti: sampel S-09/S-18 sisi mesin lolos scanner v1.2.0 total padahal juri
# memilih lawannya 2/2 (juri-pasangan-kunci.json; juri-hasils.md seksi 5).
# Tiga sinyal leksikal: panah ASCII pengganti kata, rantai titik-koma
# perangkai fragmen tanpa predikat, singkatan chat tak baku (reduplikasi
# angka-2 dan abbreviatur). Ambang konservatif: FAIL hanya bila >=2 sinyal
# BERBEDA terpicu, agar satu panah teknis sah tidak memicu positif palsu.
# ---------------------------------------------------------------------------
_NOTE_ARROW_RE = re.compile(r"[0-9A-Za-z)\]]\s*->\s*[0-9A-Za-z(\[]")
_NOTE_REDUP = ("masing", "sama", "orang", "barang", "banyak", "teman", "anak",
               "hari", "semua", "beda", "berbeda", "kali", "tempat", "benda",
               "dokumen", "laporan", "catatan", "gambar", "surat", "nama",
               "kata", "kartu", "file", "probe", "proses", "profil")
_NOTE_REDUP_RE = re.compile(r"\b(?:" + "|".join(_NOTE_REDUP) + r")2\b")
_NOTE_ABBREV = ("yg", "dgn", "tdk", "sbb", "bbrp", "sdh", "hrs", "sgt", "jg",
                "utk", "blm")
_NOTE_ABBREV_RE = re.compile(r"\b(?:" + "|".join(_NOTE_ABBREV) + r")\b")
NOTE_SEMI_MIN = 2          # minimal titik-koma dalam satu kalimat
NOTE_SEMI_FRAG_MAX = 12.0  # rata-rata kata antar titik-koma di bawah ini
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


def note_style_signals(text_):
    """Daftar sinyal gaya catatan cepat yang terdeteksi pada lapisan teks.

    Rentang kode sebaris (backtick) dibuang lebih dulu: token di dalamnya adalah
    RUJUKAN ke bentuk (mis. dokumentasi daftar hitam di berkas kebijakan), bukan
    pemakaian sungguhan - kelas bug yang sama dengan positif palsu marker C-10
    (gate-options seksi 3 butir K-2) dan CHECK 9 (alat ukur buta deskripsi
    inline). Sisi mesin nyata (S-09/S-18) tidak memakai backtick sehingga daya
    pisah terhadap bukti asli tidak berkurang.
    """
    text_ = _INLINE_CODE_RE.sub(" ", text_)
    sig = []
    low = text_.lower()
    if _NOTE_ARROW_RE.search(text_):
        sig.append("panah ASCII pengganti kata")
    chains = 0
    for s in sentences_of(text_):
        if s.count(";") >= NOTE_SEMI_MIN:
            segs = s.split(";")
            w = sum(len(words_of(g)) for g in segs)
            if w / float(len(segs)) < NOTE_SEMI_FRAG_MAX:
                chains += 1
    if chains:
        sig.append("rantai titik-koma perangkai fragmen (%d kalimat)" % chains)
    hits = sorted(set(m.group(0) for m in _NOTE_REDUP_RE.finditer(low))
                  | set(m.group(0) for m in _NOTE_ABBREV_RE.finditer(low)))
    if hits:
        sig.append("singkatan chat tak baku (%s)" % ", ".join(hits[:5]))
    return sig


# ---------------------------------------------------------------------------
# NAT-GATE-R1 (30-09-2026): indikator berat B11 - kode mesin tanpa label manusia.
# Bukti asal (keluhan user langsung): laporan yang sampai ke manusia masih memuat
# identifier internal fleet (id kartu, status mentah, nama kolom basis data, kode
# gerbang, hash) yang tidak bermakna bagi pembaca. Aturan gaya tinggal di Module
# H.4.6; blok ini adalah alat ukurnya.
#
# Skop sengaja sempit untuk menahan positif palsu:
#   - hanya baris narasi; baris tabel (`| ...`) dan heading dikecualikan karena
#     kepala tabel/heading adalah label yang sah (Module L.4, GSP-SDT);
#   - rentang kode sebaris (backtick) dibuang lebih dulu: token di dalamnya adalah
#     RUJUKAN ke bentuk, bukan pemakaian (preseden C-12 dan marker C-10);
#   - daftar putih standar resmi, satuan, dan bentuk umum teknologi tidak dihitung.
# "Dijelaskan" = pada kalimat yang sama terdapat kurung dengan >= 2 kata penyerta,
# atau kode muncul bersama kata penanda kelas (temuan/keputusan/standar/kartu/
# pemeriksaan/status/lapiran). Ini proksi deterministik dari aturan H.4.6.
# ---------------------------------------------------------------------------
_CODE_CARD_RE = re.compile(r"\bt_[0-9a-z]{6,}\b")
_CODE_STATUS_RE = re.compile(
    r"\b(?:needs[-_]review|in[-_]progress|side[-_]effecting|not[-_]started|"
    r"awaiting[-_][a-z]+|blocked_by[a-z_]*|complete_but)\b")
_CODE_SNAKE_RE = re.compile(
    r"\b[a-z][a-z0-9]*(?:_[a-z][a-z0-9]*){1,}\b")
_CODE_POLICY_RE = re.compile(
    r"\b(?:D[-_]TA[-_]\d+|NAT[-_][A-Z]{2,5}[-_]?\d*[A-Z]?|"
    r"SPK[-_]?\d+|STD[-_][A-Z]{2,6}[-_]\d+|HG[-_][A-Z]*-?\d+|LAD[-_]CARD|"
    r"[A-Z]{1,3}-\d{1,3}(?!\d)[a-z]?|(?<!\[)[A-Z]-\d{1,3}(?![\d,]))")
_CODE_HASH_RE = re.compile(r"\b(?=[0-9a-f]{12,}\b)(?=(?:[0-9a-f]*[a-f]){2})[0-9a-f]{12,}\b")
# Perluasan C-13 (GAYA-AHLI-1005 S14, putusan M-12: C-30 diserap, nomor dicoret).
# Enum status internal = token ALLCAPS bergaris-bawah (READY_FOR_REVIEW,
# IN_PROGRESS_FINAL). Garis-bawah SAJA (tanpa strip) agar tidak bertumpuk dengan
# _CODE_POLICY_RE (SPK-002, D-TA-09 sudah kelas kebijakan) - matcher ganda untuk
# satu gejala dilarang (SPK-002). Identifier API pihak ketiga = camelCase
# bercampur digit (RigidbodyType2D); nama entitas biasa (Hoober) dan merek tanpa
# digit (WhatsApp) TIDAK cocok - kasus merah-hijau CH06/CH08 papan lintas-misi.
# Keduanya KELAS LEMBUT (INFO, tidak pernah FAIL): perluasan visibilitas, bukan
# perluasan pemblokir; kelas keras lama tidak berubah keanggotaannya.
_CODE_ENUM_STATUS_RE = re.compile(r"\b[A-Z][A-Z0-9]*_[A-Z0-9_]{3,}\b")
_CODE_CAMEL_API_RE = re.compile(
    r"\b(?=[A-Za-z0-9]*[0-9])(?=[A-Za-z]*[a-z][A-Z])[A-Z][a-z][a-zA-Z0-9]*\b")
# "Berlabel" = kurung penjelas >= 6 karakter pada kalimat yang sama (bentuk sah
# H.4.6). Kata kelas saja (temuan/kartu/status) TIDAK cukup: "kartu t_91146669"
# tetap jejak mesin bagi pembaca, jadi kata itu sengaja tidak dipakai sebagai
# penanda penjelasan.
_CODE_LABEL_HINT_RE = re.compile(r"\(\s*[^\n)]{6,}\)")
# Kode standar resmi yang boleh lewat tanpa penjelasan (konteks prefix):
# MIL-STD-130, IEC 60335, BS EN 62676, dan sejenisnya (H.4.1 menyebutnya eksplisit).
_CODE_STD_PREFIX_RE = re.compile(r"(?:MIL-|IEC-|BS |EN |DIN |JIS |ANSI-|SNI )$")
_CODE_WHITELIST = (
    # satuan & spesifikasi teknis
    "kw", "kva", "hz", "dpi", "rpm", "mbps", "gbps",
    # bentuk umum teknologi / basis data yang lazim dibaca manusia
    "utf_8", "ascii_only", "snake_case", "kebab_case", "camel_case", "ping_only",
    "to_string", "error_code", "raw_data", "log_file", "web_hook", "e_mail",
    "state_db", "node_modules",
)
_CODE_CLASSES = (
    ("id kartu", _CODE_CARD_RE),
    ("status mentah mesin", _CODE_STATUS_RE),
    ("nama kolom/variabel internal", _CODE_SNAKE_RE),
    ("kode kebijakan/gerbang internal", _CODE_POLICY_RE),
    ("hash atau id panjang", _CODE_HASH_RE),
    ("enum status internal", _CODE_ENUM_STATUS_RE),
    ("identifier API pihak ketiga", _CODE_CAMEL_API_RE),
)
# Kelas baru hasil perluasan M-12: nama produk/standar yang dikenali
# is_product_or_standard() tidak dihitung pada kelas ini (whitelist sah putusan).
_CODE_SOFT_NEW_CLASSES = frozenset(("enum status internal",
                                    "identifier API pihak ketiga"))
# Kelas keras = identifier yang tidak pernah bermakna bagi pembaca manusia, bahkan
# bila diberi kata kelas ("kartu t_91146669" tetap jejak mesin). Hanya kelas ini
# yang menjatuhkan FAIL. Kelas kebijakan/standar (SPK-002, V-1, D-TA-09) terbukti
# ambigu pada laporan nyata - kodenya bisa jadi objek pembicaraan yang sah dan
# penjelasannya boleh berupa prosa, bukan hanya kurung - sehingga dilaporkan INFO
# dan menunggu kalibrasi sebelum ikut menagih (lihat catatan kalibrasi di SKILL.md).
_CODE_HARD_CLASSES = frozenset((
    "id kartu", "status mentah mesin", "hash atau id panjang",
    "nama kolom/variabel internal"))


def _code_lines(text_):
    """Baris narasi yang layak dinilai untuk kode mesin (tanpa tabel/heading/kode).

    URL dibuang lebih dulu (NAT-GATE-R2 30-09): pecahan path URL (mis.
    `.../List_of_most-played_mobile_games_by_player_count`) terhitung sebagai nama
    kolom internal pada korpus nyata - 10 dari 58 identifier keras adalah positif
    palsu kelas ini (ukur_beban_rafif.log). URL memang bukan prosa.
    """
    out = []
    for ln in text_.split("\n"):
        s = ln.strip()
        if not s or s.startswith("|") or s.startswith("#"):
            continue
        ln = _INLINE_CODE_RE.sub(" ", ln)
        ln = re.sub(r"https?://\S+", " ", ln)
        out.append(ln)
    return out


def glossary_codes(doc):
    """Kode yang terdaftar pada bagian daftar istilah/singkatan/glosarium.

    Module H.4.1 sudah mewajibkan dokumen panjang menyertakan DAFTAR SINGKATAN di
    awal lalu memakai jargon langsung. Bagi C-13 bagian itu adalah bentuk pemenuhan
    sah: kode yang terdaftar di sana tidak lagi "tanpa label manusia" bagi pembaca.
    Deteksi deterministik per-heading; tanpa bagian tersebut C-13 menilai penuh
    seperti biasa (tidak ada lolos senyap).
    """
    codes = set()
    in_block = False
    headings = getattr(doc, "gloss_headings", frozenset())
    for si, seg in enumerate(doc.segments):
        # Temuan pendamping PUTUSAN-HEUR-1009 (SEBAGAI TAMBAHAN, bukan pengganti):
        # paragraf docx tidak pernah memuat heading markdown '^#' - paragraf
        # bergaya heading Word membuka/menutup blok dengan semantik yang sama
        # seperti heading markdown (heading non-glosarium menutup blok).
        if si in headings:
            in_block = bool(re.search(
                r"(?:daftar\s+(?:istilah|singkatan|kata)|glosarium|istilah\s+dan\s+singkatan)",
                seg.text, re.IGNORECASE))
            continue
        for ln in seg.text.split("\n"):
            s = ln.strip()
            if re.match(r"^#{1,6}\s", s):
                in_block = bool(re.search(
                    r"(?:daftar\s+(?:istilah|singkatan|kata)|glosarium|istilah\s+dan\s+singkatan)",
                    s, re.IGNORECASE))
                continue
            if not in_block:
                continue
            for rx in (_CODE_CARD_RE, _CODE_POLICY_RE, _CODE_STATUS_RE,
                       _CODE_SNAKE_RE):
                for m in rx.finditer(ln):
                    codes.add(m.group(0).lower())
    return codes


def machine_code_findings(text_, excluded=frozenset()):
    """Daftar (kelas, token) kode mesin yang muncul tanpa label manusiawi."""
    found = []
    seen = set()
    for line in _code_lines(text_):
        for sent in (sentences_of(line) or [line]):
            labeled = bool(_CODE_LABEL_HINT_RE.search(sent))
            if labeled:
                continue
            for klass, rx in _CODE_CLASSES:
                for m in rx.finditer(sent):
                    tok = m.group(0)
                    low = tok.lower()
                    if low in _CODE_WHITELIST or tok.isdigit():
                        continue
                    if klass in _CODE_SOFT_NEW_CLASSES and is_product_or_standard(tok):
                        continue
                    if low in excluded or low.rstrip("s") in excluded:
                        continue
                    head = sent[max(0, m.start() - 10):m.start()]
                    if _CODE_STD_PREFIX_RE.search(head):
                        continue
                    key = (klass, low)
                    if key in seen:
                        continue
                    seen.add(key)
                    found.append((klass, tok))
    return found


# ---------------------------------------------------------------------------
# NAT-GATE-R1 (30-09-2026): indikator berat B12 - gagasan ditulis ulang.
# Bukti asal: materi pendek terasa dipanjangkan paksa karena ambang panjang lama,
# akibatnya informasi yang sama muncul dua kali. Scanner sebelumnya TIDAK punya
# satu pun pemeriksaan pengulangan. Kemiripan diukur lewat himpunan kata (Jaccard)
# pada kalimat >= 6 kata dalam jendela 12 kalimat, agar pengulangan lintas paragraf
# tertangkap tanpa menyeret kalimat yang memang harus berulang (judul, angka).
# ---------------------------------------------------------------------------
_DUP_MIN_WORDS = 6
_DUP_WINDOW = 12
_DUP_SIM = 0.70
_DUP_STOP = frozenset((
    "yang", "dan", "atau", "untuk", "dengan", "pada", "dalam", "ini", "itu", "ke",
    "dari", "bagi", "akan", "sudah", "telah", "adalah", "bila", "jika", "sebagai",
    "bahwa", "tidak", "ya", "the", "a", "an", "of", "to", "in", "on", "is", "are",
))
# Imbuhan Indonesia dilepas lebih dulu: "memeriksa" dan "diperiksa" adalah gagasan
# yang sama, tetapi pencocokan kata persis melihatnya sebagai dua token berbeda.
# Heuristik prefiks (bukan parser morfologi penuh) - cukup untuk menahan bentuk
# aktif/pasif/nominalisasi yang paling sering muncul di laporan, dan sengaja
# mensyaratkan sisa >= 4 karakter agar kata pendek tidak hancur.
_DUP_PREFIXES = ("meng", "mem", "peng", "pem", "per", "men", "di", "ke", "ter", "se")


def _dup_stem(w):
    for p in _DUP_PREFIXES:
        if w.startswith(p) and len(w) - len(p) >= 4:
            return w[len(p):]
    return w


# Kalimat berlabel struktural (kepala tabel/gambar, baris sumber, catatan kaki)
# WAJIB seragam formatnya antar bagian (Module L.3-L.4) sehingga persamaannya
# bukan pengulangan gagasan. Rujukan berkas (.md/.py/...) juga struktural.
_DUP_STRUCT_LEAD = re.compile(
    r"^\s*(?:tabel|gambar|lampiran|bagan|skema|sumber|rujukan|catatan\s+kaki|"
    r"referensi|keterangan|nama\s+berkas|file)\b", re.IGNORECASE)
_DUP_FILE_REF = re.compile(
    r"\.(?:md|py|docx|xlsx|pptx|txt|json|csv|html|zip|pdf|sh|sql|db)\b", re.IGNORECASE)
# Whitelist struktural C-14 (GAYA-AHLI-1005 S14, putusan M-04): daftar TERTUTUP
# pola boilerplate wajib-seragam (blok tanda tangan surat, kepala turunan, baris
# notasi). Populasi salinan-berlebih disempitkan, pemeriksaan TIDAK dihapus:
# gagasan narasi yang ditulis ulang dua kali tetap FAIL (fixture dua arah).
_DUP_BOILER_RE = re.compile(
    r"^\s*(?:dengan\s+hormat|hormat\s+kami|rekomendasi\s*[:;]|keputusan\s*[:;]"
    r"|lampiran\s+keputusan|sumber\s*[:;]|provenans|keterangan\s+gambar"
    r"|catatan\s+kaki|disusun\s+oleh|dikeluarkan\s+(?:di|pada)"
    r"|tanggal\s+dikeluarkan|temuan\s*[:;]|alamat\s*[:;]|perihal\s*[:;]"
    r"|nomor\s+(?:surat|resi|nota)\s*[:;]"
    # v1.9.1 DEFECT-1 (kartu t_7b3a29ad, putusan controller di t_bef365fc):
    # padanan blok tanda tangan Inggris sejajar padanan Indonesia di atas;
    # \b menahan "regarding"/"regardless" agar tidak ikut ter-whitelist.
    r"|kind\s+regards\b|best\s+regards\b|regards\b)", re.IGNORECASE)


def _dup_prose(sent):
    """Kalimat layak dinilai: prosa biasa, bukan label struktural atau rujukan berkas."""
    return not (_DUP_STRUCT_LEAD.match(sent) or _DUP_FILE_REF.search(sent))


def _dup_tokens(sent):
    # lowercase SEBELUM stem: tanpa ini "Gerbang" di awal kalimat dan "gerbang" di
    # tengah kalimat menjadi dua token berbeda dan parafrase lolos (cacat ditemukan
    # selftest CHECK 58, 30-09-2026).
    return frozenset(_dup_stem(w.lower()) for w in words_of(sent)
                     if len(w) > 2 and w.lower() not in _DUP_STOP)


def repeated_idea_groups(paras):
    """Kelompok kalimat yang memuat gagasan yang sama (kemiripan >= ambang).

    Metriknya SALINAN BERLEBIH (ukuran kelompok - 1), bukan jumlah pasangan: satu
    gagasan yang ditulis ulang tiga kali tidak boleh terasa lebih ringan daripada
    dua gagasan yang ditulis ulang masing-masing dua kali. Jendela _DUP_WINDOW
    menahan agar kalimat senada yang terpisah jauh (mis. ringkasan dan kesimpulan)
    tidak otomatis dihitung sebagai cacat yang sama.
    """
    items = []
    for ps in paras:
        for s in sentences_of(ps):
            if (len(words_of(s)) >= _DUP_MIN_WORDS and _dup_prose(s)
                    and not _DUP_BOILER_RE.match(s)):
                items.append((s, _dup_tokens(s)))
    groups = []                      # [token_representatif, [indeks anggota]]
    for i, (si, ti) in enumerate(items):
        if not ti:
            continue
        placed = False
        for g in groups:
            if i - g[1][-1] > _DUP_WINDOW:
                continue
            union = ti | g[0]
            if union and len(ti & g[0]) / float(len(union)) >= _DUP_SIM:
                g[1].append(i)
                placed = True
                break
        if not placed:
            groups.append((ti, [i]))
    texts = [it[0] for it in items]
    big = [[texts[i] for i in g[1]] for g in groups if len(g[1]) > 1]
    extras = sum(len(g) - 1 for g in big)
    return big, extras


# ---------------------------------------------------------------------------
# NAT-GATE-R2 (30-09-2026): lima detektor baru dari penilaian PANDUAN-RAFIF-MOBILE
# + dua tambahan user (bukti ukur: docs/2026-09-30-nat-gate-r1/ukur_*.log).
#   C-15 ekor kalimat (B13)  : rata-rata lulus padahal p99=116 kata, maks 456.
#   C-16 seksi terburuk (B14) : vonis global menutup bab yang menyimpang jauh.
#   C-17 kerangka seragam (B15): pola label Intinya>Asalnya>... 10/10 entri.
#   C-18 kepadatan rujukan (B16): URL mentah 12,2/1.000 kata di prosa; tanggal
#                                 non-baku L.5 1.057 vs bernama 129.
#   C-19 daftar istilah (B16) : berkas berprosa tanpa glosarium (H.4.1 wajib);
#                               ambang panjang DICABUT user 30-09, nilai selalu.
#   C-20 suara penulis (B16)  : H.1.2 melarang 'penulis' tapi tak pernah ditegakkan;
#                               LAPORAN-ADINT: Kami=0, penulis=8, lolos semua.
# Kelas INFO dulu (belum menagih agregasi): C-17/C-18/C-19/C-20 menunggu kalibrasi
# korpus; yang langsung menagih hanya C-15 dan C-16 (cacat sudah terbukti nyata).
# ---------------------------------------------------------------------------
_SENT_MAX_GATE = 80          # langit-langit H.2.1 yang selama ini tak ditegakkan
_SENT_P90_GATE = 60.0        # p90 di atas ini = ekor terlalu tebal
_SECT_MIN_SENTS = 25         # seksi lebih kecil dari ini tidak dinilai (NAT-HIL-E2)
_SECT_AVG_GATE = 14.0        # rata-rata seksi di bawah ini = FAIL seksi
# K7 kanal kitab (PUTUSAN t_77fd88c3, 30-09-2026): plafon atas rata-rata kata per
# kalimat = ambang P1a misi yang TERKUNCI (AMBANG-MUTU KOSONG-01: ASL <= 20).
# Angka ini bukan ambang scanner yang dilonggarkan - ia salinan satu-satunya angka
# mutu naskah kitab; perubahan tetap lewat gerbang AMBANG-MUTU, bukan di sini.
_KITAB_AVG_CEILING = 20.0
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_SCAFFOLD_LABELS = re.compile(
    r"\*{0,2}(Intinya|Asalnya|Temuan/angka|Untuk proyekmu|Uji murah|Batasan|"
    r"Konsekuensinya|Temuan)\*{0,2}\s*[.:]?")
_URL_INLINE_RE = re.compile(r"https?://\S+")
_DATE_ISO_RE = re.compile(r"(?<![\d/])20\d\d-\d\d-\d\d(?![\d])")
_DATE_NAMED_RE = re.compile(
    r"\b\d{1,2} (?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|"
    r"Oktober|November|Desember) 20\d\d\b")
_GLOSSARY_HEADING_RE = re.compile(
    r"(?i)^#{1,6}\s*(?:DAFTAR\s+(?:ISTILAH|SINGKATAN|KATA)|GLOSARIUM)")
_VOICE_KAMI_RE = re.compile(r"\b[Kk]ami\b")
_VOICE_PENULIS_RE = re.compile(r"\b(penulis|Penulis)\b")
_VOICE_STANCE_RE = re.compile(
    r"(?i)\b(kami rekomendasikan|kami sarankan|kami usulkan|kami pilih|kami "
    r"hindari|kami tetapkan|rekomendasi kami|keputusan kami|sebaiknya hindari|"
    r"wajib kamu|jangan kamu)\b")


def _is_enumeration(sent):
    """Kalimat pembawa daftar (pola ': 1) ... ; 2) ...' atau '; a) ... b) ...').

    NAT-GATE-R2 kalibrasi (30-09): daftar persyaratan berformat adalah struktur
    sah dokumen formal - 174 kata pada ANOMALY_SIX ternyata blok '1) Collection
    ... 2) Identification ...'. Ekor yang membuat pembaca jenuh adalah prosa
    mengalir tanpa jeda, bukan daftar berbutir. Butir daftar dikecualikan dari
    pengukuran ekor; metrik lain tetap melihatnya.
    """
    return len(re.findall(r"(?:^|[\s:;,(])(?:\d{1,2}|[a-z])\s*[).]", sent)) >= 2


def _prose_sentences(paras):
    out = []
    for ps in paras:
        for s in sentences_of(ps):
            w = len(words_of(s))
            if w >= 4 and _dup_prose(s) and not _is_enumeration(s):
                out.append(w)
    return out


def sentence_tail_stats(widths):
    """(p90, maks) dari daftar lebar kalimat."""
    if not widths:
        return 0.0, 0
    ws = sorted(widths)
    p90 = ws[min(len(ws) - 1, int(0.9 * len(ws)))]
    return float(p90), max(ws)


def worst_section(paras, min_sents=_SECT_MIN_SENTS):
    """Seksi (paragraf) dengan rata-rata kalimat terpendek di atas ambang ukuran."""
    worst = None
    for ps in paras:
        ws = [len(words_of(s)) for s in sentences_of(ps)
              if len(words_of(s)) >= 4 and _dup_prose(s)]
        if len(ws) < min_sents:
            continue
        avg = sum(ws) / float(len(ws))
        if worst is None or avg < worst[0]:
            worst = (avg, len(ws), ps[:60])
    return worst


def scaffold_sequences(paras):
    """Deteksi urutan label kerangka yang identik pada mayoritas entri berseri."""
    seqs = {}
    total = 0
    for ps in paras:
        labs = tuple(_SCAFFOLD_LABELS.findall(ps))
        if len(labs) >= 3:
            total += 1
            seqs[labs] = seqs.get(labs, 0) + 1
    if total < 5:
        return None
    top = max(seqs.items(), key=lambda kv: kv[1])
    return total, top[0], top[1]


def citation_density(text_, n_words):
    urls = len(_URL_INLINE_RE.findall(text_))
    iso = len(_DATE_ISO_RE.findall(text_))
    named = len(_DATE_NAMED_RE.findall(text_))
    per1k = lambda x: 1000.0 * x / max(1, n_words)
    return per1k(urls), per1k(iso), urls, iso, named


def has_glossary(doc):
    for seg in doc.segments:
        for ln in seg.text.split("\n"):
            if _GLOSSARY_HEADING_RE.match(ln.strip()):
                return True
    return False


def voice_presence(text_, n_words):
    kami = len(_VOICE_KAMI_RE.findall(text_))
    penulis = len(_VOICE_PENULIS_RE.findall(text_))
    stance = len(_VOICE_STANCE_RE.findall(text_))
    per1k = lambda x: 1000.0 * x / max(1, n_words)
    return per1k(kami), per1k(penulis), per1k(stance), kami, penulis


# ---------------------------------------------------------------------------
# GAYA-AHLI-1005 S14 (putusan t_dbb77bfe f3_putusan-mekanisasi.md): helper
# C-26 (M-01), C-27 (M-02), C-28 (M-10), C-33 (M-15), penanda [R-n] C-18
# (M-13), dan penghitung gabungan sapaan C-20 (M-06/M-16, DATA dulu - vonis
# kenaikan ditunda ke naskah final langkah 11). Semua bekerja pada LAPIS PROSA
# SCANNER dengan pemecah kanon sentences_of (syarat kalibrasi putusan;
# pelajaran I-3 - jangan menyalin angka lapis ekstrak).
# ---------------------------------------------------------------------------
_CLAUSE_MIN_WORDS = 4


def clause_delim_stats(paras):
    """(kata, jumlah pemisah klausa) per kalimat prosa bernilai (M-01)."""
    out = []
    for ps in paras:
        for s in sentences_of(ps):
            w = len(words_of(s))
            if w >= _CLAUSE_MIN_WORDS and _dup_prose(s) and not _is_enumeration(s):
                out.append((w, s.count(",") + s.count(";")))
    return out


def clause_summary(stats):
    """(rata-rata pemisah/kalimat, %% kalimat berantai >=4, jumlah kalimat)."""
    if not stats:
        return 0.0, 0.0, 0
    ds = [d for _, d in stats]
    mean_c = sum(ds) / float(len(ds))
    chain = 100.0 * sum(1 for d in ds if d >= 4) / len(ds)
    return mean_c, chain, len(ds)


# Daftar tertutup C-28 (M-10): tiap kata dapat diaudit terhadap kasus positif
# palsu; deviasi sadar dari daftar lajur G3: 'ia'/'run'/'diff'/'audit' dilepas
# (ambigu sebagai kata umum Indonesia/istilah sah), 'gsp' dipasang (aktor
# institusi = manusia dalam register dinas).
_DEC_TOOL_NOUNS = ("mesin", "parser", "scanner", "alat", "skrip", "register",
    "dokumen", "laporan", "tabel", "rekam", "inventaris", "gerbang", "aturan",
    "korpus", "berkas", "sistem", "pipeline", "pemindai", "penghitung", "modul",
    "kompilator", "validator", "verifier", "controller", "orkestrator", "agen",
    "bot", "model", "script", "tools", "probe", "metode")
_DEC_HUMAN_NOUNS = ("kami", "saya", "tim", "engineer", "direktur", "klien",
    "pemilik", "beliau", "mereka", "anda", "kamu", "bapak", "ibu", "penyusun",
    "pembaca", "kontraktor", "vendor", "operator", "teknisi", "analis",
    "reviewer", "manusia", "staf", "divisi", "perusahaan", "gsp")
_DEC_VERBS = ("menetapkan", "menentukan", "memilih", "menolak", "memutuskan",
    "merekomendasikan", "mengusulkan", "menyimpulkan", "menghitung", "mengadopsi",
    "menyetujui", "membatalkan", "mengeluarkan", "menerbitkan", "mengesahkan",
    "menyalakan", "memasang", "menggunakan", "memakai", "menguji", "menegur",
    "memberi", "mengirim", "mengunci", "membuka", "menutup", "menambah",
    "mengubah")
_RX_DEC_TOOL = [re.compile(r"(?<![\w])" + w + r"(?![\w])", re.IGNORECASE)
                for w in _DEC_TOOL_NOUNS]
_RX_DEC_HUMAN = [re.compile(r"(?<![\w])" + w + r"(?![\w])", re.IGNORECASE)
                 for w in _DEC_HUMAN_NOUNS]
_RX_DEC_VERB = [re.compile(r"(?<![\w])" + w + r"(?![\w])", re.IGNORECASE)
                for w in _DEC_VERBS]


def decision_subject_counts(sents):
    """(alat, manusia, netral) atas kalimat berverba keputusan (M-10)."""
    alat = manusia = netral = 0
    for s in sents:
        if not any(rx.search(s) for rx in _RX_DEC_VERB):
            continue
        hm = any(rx.search(s) for rx in _RX_DEC_TOOL)
        hh = any(rx.search(s) for rx in _RX_DEC_HUMAN)
        if hm and not hh:
            alat += 1
        elif hh:
            manusia += 1
        else:
            netral += 1
    return alat, manusia, netral


# C-33 (M-15): pembanding bekerja pada KELAS VARIAN (rentang nilai), bukan token
# mentah - 'Rp 1.500.000' vs '1,5 juta rupiah' tidak dibandingkan sebagai dua
# ejaan satu kelas; yang dibandingkan: tempel-vs-spasi, simbol-vs-kata,
# ISO-vs-nama-vs-EN, skala-kata-vs-digit-penuh.
_NUMERIC_GROUPS = (
    ("rupiah", (
        ("tempel 'Rp500.000'", re.compile(r"(?<![A-Za-z0-9])Rp\.?\d")),
        ("ber-spasi 'Rp 500.000'", re.compile(r"(?<![A-Za-z0-9])Rp\.?\s\d")))),
    ("persen", (
        ("simbol '45%'", re.compile(r"\d\s*%")),
        ("kata '45 persen'", re.compile(r"\d\s+persen(?![\w])", re.IGNORECASE)))),
    ("tanggal", (
        ("ISO '2026-10-05'", re.compile(r"(?<![\d/])\d{4}-\d{2}-\d{2}(?![\d])")),
        ("bernama ID '5 Oktober 2026'", re.compile(
            r"\b\d{1,2}\s+(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|"
            r"September|Oktober|November|Desember)\s+\d{4}\b", re.IGNORECASE)),
        ("gaya EN 'October 5, 2026'", re.compile(
            r"\b(?:January|February|March|April|May|June|July|August|September|"
            r"October|November|December)\s+\d{1,2},?\s+\d{4}\b",
            re.IGNORECASE)))),
    ("skala-angka", (
        ("skala kata '1,5 juta'", re.compile(
            r"\b\d+(?:[.,]\d+)?\s+(?:juta|miliar|ribu)(?![\w])", re.IGNORECASE)),
        ("digit penuh '1.500.000'", re.compile(r"\b\d{1,3}(?:\.\d{3})+\b")))),
)
_NUMERIC_MIX_MIN = 2


def numeric_variant_mixes(text_):
    """Daftar string '<grup> campur: varian=n, ...' untuk kelas yang bercampur."""
    out = []
    for grp, variants in _NUMERIC_GROUPS:
        counts = [(label, len(rx.findall(text_))) for label, rx in variants]
        present = [(label, n) for label, n in counts if n >= _NUMERIC_MIX_MIN]
        if len(present) >= 2:
            out.append("%s campur: %s" % (grp, ", ".join(
                "%s=%d" % (l, n) for l, n in present)))
    return out


# Perluasan C-18 (M-13, C-31 diserap): densitas penanda provenans inline PER
# KALIMAT (>1 penanda per 20 kata), bukan agregat dokumen - yang mengganggu
# pembaca adalah kalimat yang berubah jadi kaki nota. Remedinya memindahkan
# mark ke baris tabel, bukan menghapusnya (selaras SPK-002).
_RMARK_RE = re.compile(r"\[R-?\d[^\]]*\]")


def rmark_dense_count(paras):
    n = 0
    for ps in paras:
        for s in sentences_of(ps):
            k = len(_RMARK_RE.findall(s))
            if k >= 2 and len(words_of(s)) < 20 * k:
                n += 1
    return n


# Penghitung gabungan sapaan K2 (M-16 diserap ke M-06; DATA dulu, vonis ikut
# keputusan naskah final langkah 11). Nol alamat lama: grep v1.8.x atas
# kamu/Yth./Bapak/Ibu/Saudara = kosong, jadi dibangun dari nol (catatan
# putusan M-16).
_SAPAAN_K2 = (
    ("kamu", re.compile(r"(?<![\w])kamu(?![\w])", re.IGNORECASE)),
    ("Yth.", re.compile(r"\bYth\.?", re.IGNORECASE)),
    ("Bapak", re.compile(r"(?<![\w])bapak(?![\w])", re.IGNORECASE)),
    ("Ibu", re.compile(r"(?<![\w])ibu(?![\w])", re.IGNORECASE)),
    ("Saudara", re.compile(r"(?<![\w])saudara(?![\w])", re.IGNORECASE)),
)


def sapaan_k2_counts(text_):
    return [(label, len(rx.findall(text_))) for label, rx in _SAPAAN_K2]


# ---------------------------------------------------------------------------
# NAT-GATE-R3 (30-09, putaran ketiga user): LENGKUNG NARASI.
# Koreksi user atas C-20: densitas sapaan mengukur KEHADIRAN suara, bukan GERAK
# cerita. Yang ditagih sekarang: (a) dokumen runut dari latar ke tujuan,
# (b) tiap bab punya sambungan dari/ke bab tetangga, (c) ada momen pembalik
# (klimaks) yang sadar ditempatkan, (d) bab tidak jadi katalog. Aturan tinggal
# di Module H.3.5; blok ini alat ukurnya. C-24 menagih langsung (biner, risiko
# positif palsu rendah); C-22/C-23/C-25 mode pantauan dulu sesuai disiplin
# kalibrasi yang sama dipakai untuk C-13/C-17.
# ---------------------------------------------------------------------------
_CHAP_SPLIT_RE = re.compile(
    r"(?m)^[ \t]*(?:#{1,4}[ \t]*)?(?:BAB|BAGIAN|KAPITEL|PART)[ \t]+[0-9IVXLC]+[^\n]*$")
_CHAP_H_RE = re.compile(r"(?m)^#{1,2}[ \t]+(\S[^\n]*)$")
_ARC_START_RE = re.compile(
    r"(?i)\b(PENDAHULUAN|LATAR\s+BELAKANG|PENGANTAR|KONTEKS|BACKGROUND|MEMULAI|"
    r"SEBELUM\s+MULAI|MENGAPA|CARA\s+MEMAKAI|PETA\s+(?:PERJALANAN|BAB))\b")
_ARC_END_RE = re.compile(
    r"(?i)\b(KESIMPULAN|PENUTUP|REKOMENDASI|LANGKAH\s+BERIKUTNYA|EPILOG|TUJUAN|"
    r"GOALS?\b|SAATNYA|AKHIR|RINGKASAN\s+AKHIR)\b")
_NAR_BACK_RE = re.compile(
    r"(?i)\b(sebelumnya|bab\s+sebelumnya|bagian\s+sebelumnya|pada\s+bab|"
    r"seperti\s+(?:telah|sudah|kita|di)|telah\s+kita|sudah\s+kita|"
    r"setelah\s+(?:itu|kita|membaca|menyelesaikan)|berangkat\s+dari|"
    r"mengacu\s+pada|lanjutan\s+dari|dari\s+hasil\s+atas)\b")
_NAR_FWD_RE = re.compile(
    r"(?i)\b(berikutnya|akan\s+datang|nantinya|masih\s+ada|"
    r"pertanyaan\s+(?:yang\s+)?(?:tersisa|berikutnya|lain)|selanjutnya\s+kita|"
    r"menuju|bab\s+berikut|langkah\s+berikut|esok|besok)\b")
_NAR_TURN_RE = re.compile(
    r"(?i)(?:\b(?:ternyata|mengejutkan|kunci(?:nya)?|yang\s+membedakan|"
    r"titik\s+balik|klimaks|temuan\s+(?:terbesar|penting|kunci)|"
    r"masalah(?:nya| utama)|justru\s+karena|padahal|sayangnya|di\s+sinilah)\b|"
    r"\bbukan\s+[\w\s]{1,40}?\s+melainkan\b)")
_STRUCT_LINE_RE = re.compile(
    r"^\s*(?:\||#|[-*+]\s)|TERPAKAI|DIBUANG|\bt_[0-9a-f]{6,}")


def chapters_from_text(text_):
    """Potong teks per bab. None bila struktur bab tidak terdeteksi (<4)."""
    pts = [(m.start(), m.group(0).strip()) for m in _CHAP_SPLIT_RE.finditer(text_)]
    if len(pts) < 4:
        pts = [(m.start(), m.group(1).strip())
               for m in _CHAP_H_RE.finditer(text_)]
    if len(pts) < 4:
        return None
    chaps = []
    for i, (pos, title) in enumerate(pts):
        end = pts[i + 1][0] if i + 1 < len(pts) else len(text_)
        chaps.append((title, text_[pos:end]))
    return chaps


def _split_paras(body):
    """Pecah badan bab jadi paragraf, toleran terhadap lapisan gabungan.

    Cacat ditemukan kalibrasi 30-09: readable_text() menggabungkan segmen dengan
    satu baris baru, sehingga satu bab utuh menjadi SATU blok dan narrative_share
    membaca 0% prosa pada bab yang aslinya 50%. Pemecah ikut memecah sebelum
    heading (baris '#'), bukan hanya paragraf kosong.
    """
    return re.split(r"\n\s*\n|\n(?=#{1,6}[ \t])", body)


def _edge_sentences(body, head=True, n=2):
    ps = [p for p in _split_paras(body) if len(words_of(p)) >= 4]
    txt = " ".join(ps[:2] if head else ps[-2:])
    ss = sentences_of(txt)
    return " ".join(ss[:n] if head else ss[-n:])


def narrative_share(body):
    """Porsi kata prosa naratif terhadap seluruh kata bab (anti-katalog)."""
    total = nar = 0
    for blk in _split_paras(body):
        w = len(words_of(blk))
        if not w:
            continue
        lines = [l for l in blk.split("\n") if l.strip()]
        struct = sum(1 for l in lines if _STRUCT_LINE_RE.search(l))
        total += w
        if struct * 2 <= len(lines) and len(sentences_of(blk)) >= 2:
            nar += w
    return (nar / float(total)) if total else 1.0, total


def spine_titles(text_):
    """Tulang punggung dokumen: semua heading level 1/2, untuk uji lengkung.

    Kalibrasi 30-09: pemotong bab hanya melihat penanda BAB/BAGIAN sehingga
    pembukaan buku (CARA MEMAKAI, PETA PERJALANAN, SUDUT PANDANG) tidak ikut
    dinilai ujung awal lengkungnya. Lengkung adalah soal urutan bagian utuh,
    jadi tulang punggungnya semua heading atas - bukan hanya bab bernomor.
    """
    out = []
    for m in re.finditer(r"(?m)^#{1,2}[ \t]+(\S[^\n]*)$", text_):
        out.append(m.group(1).strip())
    return out


def arc_positions(titles):
    start_i = next((i for i, t in enumerate(titles) if _ARC_START_RE.search(t)), None)
    end_i = next((i for i in range(len(titles) - 1, -1, -1)
                  if _ARC_END_RE.search(titles[i])), None)
    return start_i, end_i


# ---------------------------------------------------------------------------
# Mesin check per kanal
# ---------------------------------------------------------------------------
def evaluate(doc, channel, opts):
    res = Result()
    readable = doc.readable_text()          # semua lapisan terbaca (judul/tabel/meta)
    prose_src = doc.prose_text(opts.scan_code)   # hanya prosa -> metrik panjang H.2-H.6
    raw = doc.raw                            # lapisan mentah -> hitung C-1/C-2
    n_words = len(words_of(prose_src))
    short = channel in SHORT_CHANNELS
    sosmed = channel == "sosmed"
    # K7 kanal kitab (PUTUSAN t_77fd88c3): register naskah panjang gaya kitab.
    # Bukan kanal pendek; hanya kelas metrik yang terdaftar yang berubah arah.
    kitab = channel == "kitab"
    # K8 kanal standar (PUTUSAN t_eec55819, kartu t_334c0a44): naskah standar
    # normatif rumah. Aditif terhadap doc: delta HANYA pada C-7 (ambang rasio)
    # dan C-8 (residu setelah pengecualian vocab label S-2). Cabang lama tidak
    # disentuh; dokumen tanpa kanal ini berperilaku identik.
    standar = channel == "standar"
    d16 = doc.d16_exempt()
    c = count_forms(raw)
    triggered = []
    # Penanda blok terkendali kebijakan (gate-options seksi 8): hanya metrik yang
    # terdaftar di POLICY_EXEMPT_CODES yang menilai lapisan di LUAR blok sah.
    # C-1/C-2/C-3/C-5/C-10/A5 tetap memakai lapisan penuh (mutlak, putusan butir 1).
    pol_flags, pol_invalid = policy_block_flags(doc)
    pol_on = any(pol_flags)
    # D18 lapis dua (GAYA-AHLI-1005 S14, putusan M-03): blok kutipan EKSTERNAL
    # dengan rujukan sumber sah ikut dikecualikan dari daftar hitam A4/A5/A6/A7/
    # C-4 dan dari SEMUA metrik gaya (I-5: prosa surat/vendor bukan karya penulis
    # GSP). Flag kutipan DIGABUNG ke flag kebijakan sebelum lapisan evaluasi
    # dihitung: dokumen tanpa penanda kutipan -> s14_flags identik pol_flags ->
    # perilaku check lama byte-identik (jaminan regresi kartu berikutnya).
    # C-1/C-2/C-3/C-5/A1-A3 tetap memakai lapisan mentah/penuh (mutlak).
    quote_flags, quote_invalid = quote_block_flags(doc)
    qd_on = any(quote_flags)
    s14_flags = [a or b for a, b in zip(pol_flags, quote_flags)]
    s14_on = any(s14_flags)
    pol_origins = (ORIGIN_PROSE, ORIGIN_CODE) if opts.scan_code else (ORIGIN_PROSE,)
    prose_eval = (outside_policy_text(doc, s14_flags, pol_origins)
                  if s14_on else prose_src)
    triggered_all = []

    def emit(status, nama, detail=""):
        res.add(status, nama, detail)

    def absolut(status, nama, detail):
        # D-TA-08: A1/A2 tetap mutlak di SEMUA register, termasuk override & media sosial.
        emit(status, nama, detail)

    # --- C-1 / A1 : em dash -------------------------------------------------
    # Mutlak: penanda blok kebijakan TIDAK menekan vonis C-1/C-2 (gate-options
    # 8.3; putusan butir 1). Saat ada blok sah, rincian lapisan terbaca di luar
    # blok dilaporkan sebagai INFO supaya jejak "0 di luar blok" terlihat.
    em_total = c["em_lit"] + c["em_esc"]
    if em_total == 0:
        absolut("PASS", "C-1 jumlah U+2014 (literal + escape + entity) = 0", "0 temuan")
    else:
        absolut("FAIL", "C-1 jumlah U+2014 (literal + escape + entity) = 0",
                "%d temuan (literal %d, escape/entity %d)"
                % (em_total, c["em_lit"], c["em_esc"]))
    # --- C-2 / A2 : middle dot ---------------------------------------------
    md_total = c["md_lit"] + c["md_esc"]
    if md_total == 0:
        absolut("PASS", "C-2 jumlah U+00B7 di luar blok berpenanda D16 = 0", "0 temuan")
    elif d16:
        absolut("PASS", "C-2 jumlah U+00B7 di luar blok berpenanda D16 = 0",
                "%d kemunculan DIKECUALIKAN: berkas memuat penanda D16 (blok terkendali,"
                " skop per berkas, preseden gsp-ds-set-*)" % md_total)
    else:
        absolut("FAIL", "C-2 jumlah U+00B7 di luar blok berpenanda D16 = 0",
                "%d temuan tanpa penanda D16" % md_total)
    if pol_on and (em_total or md_total):
        out_read = "\n".join(seg.text for seg, fl in zip(doc.segments, pol_flags)
                             if not fl)
        co = count_forms(out_read)
        emit("INFO", "rincian blok kebijakan untuk C-1/C-2 (vonis tetap mutlak)",
             "lapisan terbaca di luar blok: U+2014 %d temuan (literal %d, escape/entity %d),"
             " U+00B7 %d temuan; total lapisan mentah: U+2014 %d, U+00B7 %d"
             % (co["em_lit"] + co["em_esc"], co["em_lit"], co["em_esc"],
                co["md_lit"] + co["md_esc"], em_total, md_total))
    # D18 lapis satu (S14, putusan M-03): berkas berpenanda D16 dengan temuan
    # U+2014/U+00B7 wajib melaporkan rincian aparatus vs prosa. Vonis C-1/C-2
    # TETAP mutlak atas total mentah (gate-options 8.3 tidak dilanggar); baris
    # ini hanya membuat vonis dapat dibaca: token aparatus daftar tertutup
    # (kop/provenans/klasifikasi) dipisahkan dari temuan prosa biasa.
    if d16 and (em_total or md_total):
        _ap_em = _ap_md = 0
        for _ln in raw.split("\n"):
            if _apparatus_line(_ln):
                _cf = count_forms(_ln)
                _ap_em += _cf["em_lit"] + _cf["em_esc"]
                _ap_md += _cf["md_lit"] + _cf["md_esc"]
        emit("INFO", "rincian aparatus D18 lapis satu untuk C-1/C-2 (vonis tetap mutlak)",
             "%d dari %d temuan U+2014 dan %d dari %d temuan U+00B7 duduk di baris "
             "aparatus daftar tertutup (kop/provenans/klasifikasi); sisanya prosa "
             "biasa - pembebasan bukan opsi, lihat gate-options 8.3"
             % (_ap_em, em_total, _ap_md, md_total))

    # --- INFO : en dash (D-TA-04, bukan pelanggaran) ------------------------
    if c["en_all"]:
        outside = c["en_all"] - min(c["en_all"], c["en_range"])
        emit("INFO", "en dash U+2013 dilaporkan sebagai informasi (D-TA-04)",
             "%d kemunculan; %d dalam pola rentang angka (?<=digit)(?=digit); %d di luar"
             " pola - dilaporkan, tidak dihitung sebagai pelanggaran"
             % (c["en_all"], min(c["en_all"], c["en_range"]), outside))

    # --- C-3 / A3 : emoji ---------------------------------------------------
    emo = emoji_count(readable)
    if sosmed:
        emit("INFO", "C-3 emoji di kanal formal = 0",
             "%d emoji; media sosial mengikuti brief kampanye (D-TA-08)" % emo)
    elif emo == 0:
        absolut("PASS", "C-3 emoji di kanal formal = 0", "0 temuan")
    else:
        absolut("FAIL", "C-3 emoji di kanal formal = 0", "%d emoji" % emo)

    # --- C-4 : frasa daftar hitam A4 / A6 / A7 ------------------------------
    # Sumber aturan (RT 3.2): lapisan KODE tidak diuji pola prosa - daftar hitam
    # scanner sendiri tinggal sebagai data, dan menandainya = positif palsu.
    # C-4 adalah baris agregat (RT 5.2); baris A4/A6/A7 di bawah menambahkan kode
    # per-pelanggaran agar corpus merah-hijau (NAT-S10) bisa membuktikan SETIAP kode
    # memicu FAIL lewat pencarian baris, bukan lewat pembacaan detail.
    h4 = frasa_hits(prose_eval, BLACKLIST_A4)
    h6 = frasa_hits(prose_eval, BLACKLIST_A6)
    h7 = frasa_hits(prose_eval, BLACKLIST_A7)
    h4f = frasa_hits(prose_src, BLACKLIST_A4)
    h6f = frasa_hits(prose_src, BLACKLIST_A6)
    h7f = frasa_hits(prose_src, BLACKLIST_A7)
    n4 = len(h4) + len(h6) + len(h7)
    n4f = len(h4f) + len(h6f) + len(h7f)
    for code, hits, hits_full, label in (
            ("A4", h4, h4f, "jejak kolaboratif/percakapan agen"),
            ("A6", h6, h6f, "penutup datar generik"),
            ("A7", h7, h7f, "pembuka generik")):
        if not hits:
            absolut("PASS", "%s %s = 0" % (code, label), "0 temuan")
        elif sosmed:
            emit("INFO", "%s %s = 0" % (code, label),
                 "%d temuan; media sosial ikut brief (D-TA-08)" % len(hits))
        else:
            absolut("FAIL", "%s %s = 0" % (code, label),
                    "%d temuan: %s" % (len(hits), "; ".join(hits[:5])))
        if len(hits) < len(hits_full):
            emit("INFO", "%s DIKECUALIKAN blok berpenanda kebijakan" % code,
                 "%d temuan DIKECUALIKAN: berada dalam blok berpenanda kebijakan "
                 "(skop per-blok, gate-options seksi 8)" % (len(hits_full) - len(hits)))
    if n4 == 0:
        absolut("PASS", "C-4 frasa daftar hitam A4/A6/A7 = 0", "0 temuan")
    elif sosmed:
        emit("INFO", "C-4 frasa daftar hitam A4/A6/A7 = 0",
             "%d temuan (%s); media sosial ikut brief (D-TA-08)"
             % (n4, ", ".join((h4 + h6 + h7)[:4])))
    else:
        absolut("FAIL", "C-4 frasa daftar hitam A4/A6/A7 = 0",
                "%d temuan: %s" % (n4, "; ".join((h4 + h6 + h7)[:6])))
    if n4 < n4f:
        emit("INFO", "C-4 DIKECUALIKAN blok berpenanda kebijakan",
             "%d temuan DIKECUALIKAN: berada dalam blok berpenanda kebijakan "
             "(%d dari %d temuan lapisan penuh)" % (n4f - n4, n4f - n4, n4f))

    # --- C-5 / B3 : italic istilah EN ---------------------------------------
    italics = italic_terms(prose_src)
    prod_std = sorted(set(t for t in italics if is_product_or_standard(t)))
    c5_ok = (len(prod_std) == 0 and len(italics) <= 2)
    c5_detail = "%d istilah di-italic (%d kategori produk/standar): %s" % (
        len(italics), len(prod_std), "; ".join(sorted(set(italics))[:5]) or "-")
    if sosmed:
        emit("INFO", "C-5 istilah EN di-italic <= 2 dan 0 untuk produk/standar",
             c5_detail + "; media sosial ikut brief (D-TA-08)")
    else:
        emit("PASS" if c5_ok else "FAIL",
             "C-5 istilah EN di-italic <= 2 dan 0 untuk produk/standar", c5_detail)
        if not c5_ok:
            triggered.append("B3")

    # --- A5 : label ruang kerja / fungsi internal ---------------------------
    # A5 (S14/M-03 lapis dua): hanya flag KUTIPAN yang digabung di sini - blok
    # kebijakan biasa TIDAK pernah mengecualikan A5 (daftar mutlak gate-options
    # 8.3). Tanpa penanda kutipan sah, sumber identik prose_src (regresi nol).
    a5_src = (outside_policy_text(doc, quote_flags, (ORIGIN_PROSE,))
              if qd_on else prose_src)
    h5 = frasa_hits(a5_src, BLACKLIST_A5) + frasa_hits(a5_src, _A5_CODE_NAMES)
    h5 = sorted(set(h5))
    if not h5:
        absolut("PASS", "A5 label ruang kerja / fungsi internal bocor ke narasi = 0",
                "0 temuan")
    elif sosmed:
        emit("INFO", "A5 label ruang kerja / fungsi internal bocor ke narasi = 0",
             "%d temuan (%s); media sosial ikut brief (D-TA-08)" % (len(h5), ", ".join(h5)))
    else:
        absolut("FAIL", "A5 label ruang kerja / fungsi internal bocor ke narasi = 0",
                "%d temuan: %s" % (len(h5), "; ".join(h5[:5])))

    # --- indikator berat B (metrik prosa) -----------------------------------
    # Seluruh metrik B terdaftar sebagai kode yang boleh dikecualikan (gate-options
    # 8.3): saat ada blok berpenanda sah, metrik menilai lapisan di luar blok dan
    # selisihnya dilaporkan sebagai baris INFO (gate-options 8.4). Tanpa penanda,
    # lapisan evaluasi identik dengan lapisan penuh -> perilaku lama tak berubah.
    paras_full = prose_paragraphs(doc, opts.scan_code)
    paras = (outside_paragraphs(doc, s14_flags, opts.scan_code)
             if s14_on else paras_full)

    def _sent_stats(ps):
        ss = []
        for p in ps:
            ss.extend(sentences_of(p))
        avg = ((sum(len(words_of(s)) for s in ss) / float(len(ss)))
               if ss else 0.0)
        return ss, avg

    sents, avg_words = _sent_stats(paras)
    sents_full, avg_full = _sent_stats(paras_full)
    nw_eval = len(words_of(prose_eval)) if s14_on else n_words
    prose_ok = doc.supports_prose and n_words > 0

    def b_metric(code, name, enabled, fn, na_reason, fn_full=None):
        if not enabled:
            emit("N/A", name, na_reason)
            return
        ok, detail = fn()
        if sosmed and not ok:
            # D-TA-08: di media sosial hanya A1/A2 yang mutlak; indikator berat
            # dilaporkan mengikuti brief kampanye, bukan sebagai pelanggaran gerbang.
            emit("INFO", name, detail + "; media sosial ikut brief (D-TA-08)")
            return
        if kitab and not ok and code in KITAB_DEMOTE_CODES:
            # K7 (PUTUSAN t_77fd88c3 butir 5+8): kelas kepadatan gaya runtuh jadi
            # INFO pada kanal kitab; alasan eksplisit wajib tercetak dan indikator
            # TIDAK masuk triggered[] -> tidak dihitung agregasi D-TA-09.
            emit("INFO", name, detail + "; DIRUNTUHKAN menjadi INFO karena kanal"
                 " kitab (genre buku pelajaran; putusan gerbang t_77fd88c3)")
            return
        emit("PASS" if ok else "FAIL", name, detail)
        if not ok:
            triggered.append(code)
        if fn_full is not None:
            okf, _df = fn_full()
            if ok and not okf:
                triggered_all.append(code)
                emit("INFO", "%s DIKECUALIKAN blok berpenanda kebijakan" % _code_of(name),
                     "indikator terpicu pada lapisan penuh tetapi tidak di luar "
                     "blok berpenanda kebijakan -> dikecualikan (gate-options "
                     "seksi 8, skop per-blok)")

    na_short = "tidak berlaku di kanal pendek '%s' (D-TA-05)" % channel
    na_format = "format '%s' tidak menyediakan prosa berkalimat (matriks sweep)" % doc.fmt

    # NAT-HIL-E2 (kartu t_c79b5f6d): C-6/C-7 positif palsu sistematis pada
    # cuplikan pendek lintas kanal (kontrol juri NAT-S22: 12 dari 18 sisi
    # manusiawi FAIL; C-6 menyumbang 303 dari sekitar 350 sampel berat
    # pasca-gerbang; contoh S-11 11,5 kata/kalimat dari 2 kalimat). Metrik
    # panjang kalimat dan kerapatan paragraf tidak punya daya pisah di bawah
    # 3 kalimat atau 40 kata pada lapisan yang dinilai -> N/A eksplisit,
    # bukan PASS (tetap dilaporkan, lolos senyap dilarang).
    e2_short = prose_ok and (len(sents) < 3 or nw_eval < 40)
    na_e2 = ("cuplikan pendek: %d kalimat / %d kata di bawah ambang penilaian "
             "metrik panjang (NAT-HIL-E2)" % (len(sents), nw_eval))

    # NAT-GATE-R1 (30-09-2026): ambang C-6 turun 25 -> 18 kata per kalimat (70%
    # ambang lama) mengikuti revisi Module H.2.1. Alasan: ambang lama memaksa
    # penulis materi pendek mengulur kalimat sampai isinya berulang. Lantai
    # dilonggarkan; langit-langit (maks 80 kata) dan guard cuplikan pendek
    # NAT-HIL-E2 tetap. Daya pisah yang hilang dari C-6 diambil alih C-13/C-14.
    # K7 kanal kitab (PUTUSAN t_77fd88c3 butir 3): arah DIBALIK menjadi plafon
    # atas - FAIL hanya bila rata-rata > 20,0 kata/kalimat (plafon P1a misi yang
    # terkunci). Nama baris menyebut plafon; kanal lain tidak tersentuh.
    c6_name = ("C-6 rata-rata kata per kalimat <= %.1f plafon P1a kanal kitab"
               " (indikator B1)" % _KITAB_AVG_CEILING) if kitab else \
              "C-6 rata-rata kata per kalimat >= 18 (indikator B1)"

    def _c6_kitab():
        return (avg_words <= _KITAB_AVG_CEILING,
                "%.1f kata/kalimat dari %d kalimat; plafon kanal kitab %.1f"
                % (avg_words, len(sents), _KITAB_AVG_CEILING))

    b_metric("B1", c6_name,
             (not short) and prose_ok and not e2_short,
             _c6_kitab if kitab else (lambda: (
                 avg_words >= 18.0,
                 "%.1f kata/kalimat dari %d kalimat" % (avg_words, len(sents)))),
             na_short if short else (na_e2 if e2_short else na_format),
             (lambda: (avg_full <= _KITAB_AVG_CEILING, "")) if kitab
             else (lambda: (avg_full >= 18.0, "")))

    def _b2(ps):
        def f():
            # Ambang gerbang C-7: paragraf pendek = < 3 kalimat (PUTUSAN USER 27-09-2026,
            # revisi NAT-C7: semula < 4 mengikuti target gaya H.3.1; H.3.1 tetap acuan
            # gaya penulisan, gerbang enforcer memakai 3). Maksimal 1 paragraf pendek.
            few = [p for p in ps if len(sentences_of(p)) < 3]
            return (len(few) <= 1,
                    "%d paragraf < 3 kalimat dari %d paragraf" % (len(few), len(ps)))
        return f

    def _b2_standar(ps):
        # K8 kanal standar (PUTUSAN t_eec55819 seksi 2(a) butir 3): aparatus
        # navigasi naskah normatif (indeks aturan, catatan cakupan, kepala lapis)
        # sah pendek-pendek; ambang absolut <=1 diganti rasio <= 20% total
        # paragraf sehingga mengikuti ukuran dokumen. Di atas rasio tetap FAIL
        # dan B2 tetap terpicu - kelonggaran terukur, bukan karpet.
        def f():
            few = [p for p in ps if len(sentences_of(p)) < 3]
            ratio = (len(few) / float(len(ps))) if ps else 0.0
            return (ratio <= STANDAR_SHORT_RATIO,
                    "%d paragraf < 3 kalimat dari %d paragraf (%.1f%%, ambang "
                    "rasio kanal standar %.0f%%)"
                    % (len(few), len(ps), 100.0 * ratio,
                       100.0 * STANDAR_SHORT_RATIO))
        return f

    b2_name = ("C-7 paragraf < 3 kalimat <= 1 per dokumen (indikator B2)"
               if not standar else
               "C-7 paragraf < 3 kalimat <= %.0f%% total paragraf (indikator B2)"
               " (kanal standar: aparatus navigasi)"
               % (100.0 * STANDAR_SHORT_RATIO))
    b_metric("B2", b2_name,
             (not short) and prose_ok and not e2_short,
             _b2_standar(paras) if standar else _b2(paras),
             na_short if short else (na_e2 if e2_short else na_format),
             _b2_standar(paras_full) if standar else _b2(paras_full))

    def _b4(text_, nw):
        def f():
            hits = frasa_hits(text_, BLACKLIST_B4)
            r = rate_per_1000(len(hits), nw)
            return (r <= 1.0, "%.1f per 1.000 kata (%d temuan): %s"
                    % (r, len(hits), "; ".join(hits[:5]) or "-"))
        return f

    b_metric("B4", "C-9a kosakata AI-typical ID/EN <= 1 per 1.000 kata (indikator B4)",
             prose_ok, _b4(prose_eval, nw_eval), na_format,
             _b4(prose_src, n_words))

    def _b5(text_):
        def f():
            low = text_.lower()
            totals = {}
            for grp in sorted(TRANSITION_GROUPS):
                # hitung per-kata: substring biasa membuat "maka" tertangkap dalam
                # "memakai"/"mengatakan" dan menghasilkan positif palsu pada teks wajar.
                totals[grp] = sum(
                    len(re.findall(r"(?<![\w])" + re.escape(p) + r"(?![\w])", low))
                    for p in TRANSITION_GROUPS[grp])
            tot = sum(totals.values())
            if tot < 4:
                return (True, "transisi terlalu sedikit untuk dinilai (%d)" % tot)
            top = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))[0]
            share = 100.0 * top[1] / tot
            return (share <= 60.0, "kategori dominan '%s' %.0f%% dari %d transisi"
                    % (top[0], share, tot))
        return f

    b_metric("B5", "C-9b transisi monoton <= 60% satu jenis (indikator B5)",
             prose_ok, _b5(prose_eval), na_format, _b5(prose_src))

    def _b6(text_, nw, ps):
        def f():
            bolds = len(re.findall(r"\*\*[^*\n]+\*\*", text_))
            r = rate_per_1000(bolds, nw)
            runs = vertical_bold_runs(ps)
            return (r <= 6.0 and runs <= 2,
                    "%.1f tebal per 1.000 kata (%d), daftar vertikal beruntun %d item"
                    % (r, bolds, runs))
        return f

    def _b6_standar(text_, nw, ps):
        # K8 kanal standar (PUTUSAN t_eec55819 seksi 2(a) butir 3): tebal yang
        # PERSIS sama dengan salah satu dari enam label bidang skema S-2 (vocab
        # tertutup di konstanta scanner, TIDAK dibaca dari dokumen - tanpa celah
        # swa-deklarasi) adalah tipografi struktur, bukan emfasis; dikeluarkan
        # dari pembilang. Ambang 6/1000 kata berlaku atas RESIDU dan B6 tetap
        # bisa terpicu. Dokumen bervocab lain butuh perluasan konstanta lewat
        # jalur M-6, bukan penanda mandiri.
        def f():
            kept = excluded = 0
            for m in re.finditer(r"\*\*([^*\n]+)\*\*", text_):
                if m.group(1).strip().rstrip(".:") in STANDAR_FIELD_LABELS:
                    excluded += 1
                else:
                    kept += 1
            r = rate_per_1000(kept, nw)
            runs = vertical_bold_runs(ps)
            return (r <= 6.0 and runs <= 2,
                    "%.1f tebal residu per 1.000 kata (%d), daftar vertikal "
                    "beruntun %d item; %d kepala bidang skema dikecualikan "
                    "(vocab tertutup S-2)" % (r, kept, runs, excluded))
        return f

    b6_name = ("C-8 tebal/inline-header-list <= 6 per 1.000 kata (indikator B6)"
               if not standar else
               "C-8 tebal residu/inline-header-list <= 6 per 1.000 kata"
               " (indikator B6) (kanal standar: kepala bidang S-2 dikecualikan)")
    b_metric("B6", b6_name,
             prose_ok,
             _b6_standar(prose_eval, nw_eval, paras) if standar
             else _b6(prose_eval, nw_eval, paras), na_format,
             _b6_standar(prose_src, n_words, paras_full) if standar
             else _b6(prose_src, n_words, paras_full))

    def _b7(text_, nw, ss):
        def f():
            unhedged = 0
            for s in ss:
                if re.search(r"\d", s):
                    continue
                low = s.lower()
                unhedged += sum(len(re.findall(r"(?<![\w])" + re.escape(h) + r"(?![\w])", low))
                                for h in HEDGE_WORDS)
            r = rate_per_1000(unhedged, nw)
            return (r <= 3.0, "%.1f hedging tanpa kuantifikasi per 1.000 kata (%d)" % (r, unhedged))
        return f

    b_metric("B7", "C-9 hedging tanpa kuantifikasi <= 3 per 1.000 kata (indikator B7)",
             prose_ok, _b7(prose_eval, nw_eval, sents), na_format,
             _b7(prose_src, n_words, sents_full))

    def _b8(text_):
        def f():
            missing = []
            if not re.search(r"\d", text_):
                missing.append("tanpa angka spesifik")
            if not any(w in text_.lower() for w in LIMITATION_WORDS):
                missing.append("tanpa pengakuan batasan")
            return (not missing, "OK" if not missing else "; ".join(missing))
        return f

    # NAT-GATE-R1: ambang keberlakuan uji dokumen analitis turun 80 -> 56 kata
    # (70% ambang lama) agar laporan pendek ikut dinilai tanpa dipanjangkan paksa.
    b_metric("B8", "C-8b ada angka spesifik dan pengakuan batasan (indikator B8)",
             (not short) and prose_ok and n_words >= 56, _b8(prose_eval),
             na_short if short else "prosa < 56 kata: uji dokumen analitis tidak berlaku",
             _b8(prose_src))

    # NAT-HIL-E1 (kartu t_c79b5f6d): indikator berat baru C-12/B10 gaya catatan
    # cepat. FAIL hanya bila >=2 sinyal BERBEDA terpicu sekaligus (panah ASCII
    # pengganti kata, rantai titik-koma perangkai fragmen tanpa predikat,
    # singkatan chat tak baku). Satu sinyal tunggal dilaporkan INFO agar jejak
    # tetap terlihat tanpa menaikkan agregasi D-TA-09 sendirian.
    def _b10(text_):
        def f():
            sig = note_style_signals(text_)
            return (len(sig) < 2,
                    "%d sinyal: %s" % (len(sig), "; ".join(sig)) if sig else "0 sinyal")
        return f

    b_metric("B10", "C-12 gaya catatan cepat <= 1 sinyal (indikator B10)",
             prose_ok, _b10(prose_eval), na_format, _b10(prose_src))
    _sig_eval = note_style_signals(prose_eval)
    if len(_sig_eval) == 1 and prose_ok:
        emit("INFO", "C-12 sinyal tunggal gaya catatan cepat",
             "%s - di bawah ambang dua sinyal, tidak menghitung agregasi" % _sig_eval[0])

    # --- NAT-GATE-R1 C-13 / B11 : kode mesin tanpa label manusia ------------
    # FAIL hanya pada KELAS KERAS (id kartu, status mentah, hash, nama kolom) >= 3
    # temuan berbeda. Kelas kebijakan/standar dilaporkan INFO sampai kalibrasi
    # selesai (lihat catatan di blok konstanta): pada laporan nyata kodenya sering
    # menjadi objek pembicaraan yang sah.
    CODE_MIN_FAIL = 3
    if not prose_ok:
        emit("N/A", "C-13 kode mesin tanpa label manusia <= 2 (indikator B11)",
             na_format)
    else:
        _gloss = glossary_codes(doc)
        # PUTUSAN-HEUR-1009 butir 3 (kartu t_d9d918a6): run docx berfont monospace
        # diperlakukan setara backtick markdown untuk penilaian C-13 SAJA - token
        # di dalamnya RUJUKAN ke bentuk, bukan pemakaian (preseden C-12/C-10).
        # Lapisan terkupas dipakai hanya di sini; check lain memakai lapisan utuh
        # (regresi byte-identik wajib) dan ambang CODE_MIN_FAIL tidak diubah.
        _pm = getattr(doc, "prose_mono", [])
        _mi = [i for i, e in enumerate(_pm) if e]
        if _mi:
            def _strip_mono(i, txt, _pm=_pm):
                e = _pm[i] if i < len(_pm) else None
                return txt if e is None else e[0]
            prose_eval_c13 = (outside_policy_text(doc, s14_flags, pol_origins,
                                                  strip_fn=_strip_mono)
                              if s14_on else
                              doc.prose_text(opts.scan_code, strip_fn=_strip_mono))
            prose_src_c13 = doc.prose_text(opts.scan_code, strip_fn=_strip_mono)
        else:
            prose_eval_c13 = prose_eval
            prose_src_c13 = prose_src
        # K7 kanal kitab (PUTUSAN t_77fd88c3 butir 5): komentar HTML baris
        # provenansi (mis. `<!-- kartu t_xxx | basis pin <hash> -->`) BUKAN
        # identifier keras pada kanal ini - ia jejak mesin untuk agen, bukan
        # teks baca. Pengupasan hanya untuk C-13 kanal kitab; kanal lain dan
        # metrik lain memakai lapisan utuh (regresi byte-identik).
        mc_src = _HTML_COMMENT_RE.sub(" ", prose_eval_c13) if kitab else prose_eval_c13
        mc_all_src = (_HTML_COMMENT_RE.sub(" ", prose_src_c13) if kitab else prose_src_c13)
        mc = machine_code_findings(mc_src, _gloss)
        mc_all = machine_code_findings(mc_all_src, _gloss)
        hard = [f for f in mc if f[0] in _CODE_HARD_CLASSES]
        soft = [f for f in mc if f[0] not in _CODE_HARD_CLASSES]
        name13 = "C-13 kode mesin tanpa label manusia <= 2 (indikator B11)"

        def _fmt(fs):
            return ", ".join("%s=%s" % (k, t) for k, t in fs[:6])

        # Visibilitas pengecualian tipografis (preseden pengupasan komentar HTML
        # kanal kitab): identifier yang keluar dari penilaian dilaporkan INFO.
        if _mi:
            _mono_found = machine_code_findings(
                "\n".join(_pm[i][1] for i in _mi), _gloss)
            _mono_hard = [f for f in _mono_found if f[0] in _CODE_HARD_CLASSES]
            emit("INFO", "C-13 identifier monospace dikecualikan (tipografi docx)",
                 "%d paragraf memuat run monospace; %d identifier keras hasil "
                 "sapuan lapisan monospace tidak dihitung keras (setara backtick, "
                 "PUTUSAN-HEUR-1009): %s"
                 % (len(_mi), len(_mono_hard), _fmt(_mono_hard)))

        if len(hard) >= CODE_MIN_FAIL:
            if kitab:
                emit("INFO", name13, "%d identifier keras: %s" % (len(hard), _fmt(hard))
                     + ("; %d kode kebijakan INFO: %s" % (len(soft), _fmt(soft)) if soft else "")
                     + "; DIRUNTUHKAN menjadi INFO karena kanal kitab (identifier API"
                     " = materi buku pemrograman; komentar HTML provenansi tidak"
                     " dihitung keras; putusan gerbang t_77fd88c3)")
            else:
                emit("FAIL", name13, "%d identifier keras: %s" % (len(hard), _fmt(hard))
                     + ("; %d kode kebijakan INFO: %s" % (len(soft), _fmt(soft)) if soft else ""))
                triggered.append("B11")
        elif hard:
            emit("INFO", name13, "%d identifier keras: %s - di bawah ambang tiga temuan"
                 % (len(hard), _fmt(hard))
                 + ("; %d kode kebijakan INFO: %s" % (len(soft), _fmt(soft)) if soft else ""))
        elif soft:
            emit("INFO", name13, "0 identifier keras; %d kode kebijakan/standar "
                 "dipantau (INFO, belum menagih): %s" % (len(soft), _fmt(soft)))
        else:
            emit("PASS", name13, "0 temuan")
        hard_all = [f for f in mc_all if f[0] in _CODE_HARD_CLASSES]
        if len(hard) < CODE_MIN_FAIL <= len(hard_all):
            triggered_all.append("B11")
            emit("INFO", "C-13 DIKECUALIKAN blok berpenanda kebijakan",
                 "%d identifier keras pada lapisan penuh tetapi di luar blok "
                 "kebijakan -> dikecualikan (gate-options seksi 8)" % len(hard_all))
        # Perluasan M-12 (S14): kelas enum-status/camel-API = lembut permanen
        # putaran ini - dilaporkan INFO terpisah agar visibilitas baru tidak
        # pernah menyentuh jalur FAIL maupun ambang CODE_MIN_FAIL kelas lama.
        _newc = [f for f in soft if f[0] in _CODE_SOFT_NEW_CLASSES]
        if _newc:
            emit("INFO", "perluasan C-13 M-12 identifier kelas baru dipantau",
                 "%d identifier enum status/API pihak ketiga dilaporkan INFO, "
                 "tidak menagih dan tidak dihitung keras: %s"
                 % (len(_newc), _fmt(_newc)))

    # --- NAT-GATE-R1 C-14 / B12 : gagasan ditulis ulang ----------------------
    # Ambang: >= 2 SALINAN BERLEBIH = FAIL; 1 salinan = INFO (di bawah ambang,
    # tetap terlihat di jejak). Diukur pada lapisan di luar blok kebijakan.
    DUP_MIN_EXTRAS = 2
    if not prose_ok or e2_short:
        emit("N/A", "C-14 gagasan ditulis ulang <= 1 salinan (indikator B12)",
             na_short if short else (na_e2 if e2_short else na_format))
    else:
        def _dup_ps(ps):
            groups, extras = repeated_idea_groups(ps)
            label = "%d salinan berlebih dari %d kelompok: %s" % (
                extras, len(groups),
                "; ".join("%dx '%s...'" % (len(g), g[0][:36]) for g in groups[:3]))
            return extras, label
        extras, label = _dup_ps(paras)
        extras_all, _ = _dup_ps(paras_full)
        name14 = "C-14 gagasan ditulis ulang <= 1 salinan (indikator B12)"
        if extras >= DUP_MIN_EXTRAS:
            emit("FAIL", name14, label)
            triggered.append("B12")
        elif extras == 1:
            emit("INFO", name14, label + " - satu salinan, di bawah ambang dua")
        else:
            emit("PASS", name14, "0 salinan berlebih dari %d kalimat prosa bernilai" % len(
                [s for ps in paras for s in sentences_of(ps)
                 if len(words_of(s)) >= _DUP_MIN_WORDS and _dup_prose(s)]))
        if extras < DUP_MIN_EXTRAS <= extras_all:
            triggered_all.append("B12")
            emit("INFO", "C-14 DIKECUALIKAN blok berpenanda kebijakan",
                 "%d salinan berlebih pada lapisan penuh tetapi di luar blok "
                 "kebijakan -> dikecualikan (gate-options seksi 8)" % extras_all)

    # --- NAT-GATE-R2 C-15 / B13 : ekor kalimat ------------------------------
    # Rata-rata lulus bukan jaminan: p90 dan maksimum yang bikin pembaca jenuh.
    # Menagih agregasi (cacat terbukti nyata pada korpus).
    # K7 kanal kitab (PUTUSAN t_77fd88c3 butir 5): vonis panjang kalimat jadi
    # milik gerbang misi P1d (alat R4, lebih ketat + punya register pengecualian)
    # -> FAIL runtuh menjadi INFO, tidak masuk triggered[].
    if not prose_ok or e2_short:
        emit("N/A", "C-15 ekor kalimat p90 <= 60 dan maks <= 80 (indikator B13)",
             na_short if short else (na_e2 if e2_short else na_format))
    else:
        widths = _prose_sentences(paras)
        p90, mx = sentence_tail_stats(widths)
        name15 = "C-15 ekor kalimat p90 <= 60 dan maks <= 80 (indikator B13)"
        n_over = sum(1 for w in widths if w > _SENT_MAX_GATE)
        if mx > _SENT_MAX_GATE * 2 or n_over >= 10:
            if kitab:
                emit("INFO", name15,
                     "p90=%.0f, maks=%d kata; %d kalimat melewati langit-langit 80 "
                     "(H.2.1); DIRUNTUHKAN menjadi INFO karena kanal kitab (vonis "
                     "panjang milik gerbang misi P1d alat R4; putusan gerbang "
                     "t_77fd88c3)" % (p90, mx, n_over))
            else:
                emit("FAIL", name15,
                     "p90=%.0f, maks=%d kata; %d kalimat melewati langit-langit 80 "
                     "(H.2.1)" % (p90, mx, n_over))
                triggered.append("B13")
        elif n_over:
            emit("INFO", name15,
                 "p90=%.0f, maks=%d kata; %d kalimat melewati langit-langit 80 - "
                 "di bawah ambang sepuluh" % (p90, mx, n_over))
        else:
            emit("PASS", name15, "p90=%.0f, maks=%d kata dari %d kalimat prosa"
                 % (p90, mx, len(widths)))

    # --- NAT-GATE-R2 C-16 / B14 : seksi terburuk -----------------------------
    # Vonis per-dokumen menutup bab yang menyimpang jauh; pengalaman baca adalah
    # per-bab, jadi unit ukur harus menyamai unit pengalaman. Menagih agregasi.
    # K7 kanal kitab (PUTUSAN t_77fd88c3 butir 4): arah dibalik - FAIL hanya bila
    # seksi TERBURUK > 20,0 kata/kalimat (plafon P1a); populasi kecil tetap N/A.
    if not prose_ok or e2_short:
        emit("N/A", "C-16 rata-rata seksi terburuk >= 14 kata/kalimat (indikator B14)",
             na_short if short else (na_e2 if e2_short else na_format))
    else:
        worst = worst_section(paras)
        name16 = ("C-16 rata-rata seksi terburuk <= %.1f plafon P1a kanal kitab"
                  " (indikator B14)" % _KITAB_AVG_CEILING) if kitab else \
                 "C-16 rata-rata seksi terburuk >= 14 kata/kalimat (indikator B14)"
        if worst is None:
            emit("N/A", name16, "tidak ada seksi dengan >= %d kalimat prosa"
                 % _SECT_MIN_SENTS)
        elif kitab and worst[0] > _KITAB_AVG_CEILING:
            emit("FAIL", name16,
                 "seksi terburuk %.1f kata/kalimat (%d kalimat) melewati plafon"
                 " kanal kitab %.1f" % (worst[0], worst[1], _KITAB_AVG_CEILING))
            triggered.append("B14")
        elif (not kitab) and worst[0] < _SECT_AVG_GATE:
            emit("FAIL", name16,
                 "seksi terburuk %.1f kata/kalimat (%d kalimat): '%s...'"
                 % (worst[0], worst[1], worst[2]))
            triggered.append("B14")
        else:
            emit("PASS", name16,
                 "seksi terburuk %.1f kata/kalimat (%d kalimat)%s"
                 % (worst[0], worst[1],
                    (" ; di bawah plafon kanal kitab %.1f" % _KITAB_AVG_CEILING)
                    if kitab else ""))

    # --- NAT-GATE-R2 C-17 / B15 : kerangka entri seragam (INFO dulu) ---------
    if not prose_ok or e2_short:
        emit("N/A", "C-17 kerangka label seragam < 80% entri berseri (indikator B15)",
             na_short if short else (na_e2 if e2_short else na_format))
    else:
        sq = scaffold_sequences(paras)
        name17 = "C-17 kerangka label seragam < 80% entri berseri (indikator B15)"
        if sq is None:
            emit("N/A", name17, "entri berseri >=3 label kurang dari 5 - tidak dinilai")
        else:
            total, top_seq, cnt = sq
            share = 100.0 * cnt / total
            detail = "%d/%d entri (%.0f%%) memakai urutan '%s'" % (
                cnt, total, share, " > ".join(top_seq))
            # STATUS PANTAUAN (kalibrasi korpus belum terkumpul; ambang vonis akan
            # dinaikkan ke FAIL pada versi setelah 20 deliverable etalase terukur).
            emit("INFO", name17, detail + (" - share >= 80%%, layak direvisi "
                 "(masih mode pantauan)" if share >= 80 else " - di bawah share 80%"))

    # --- NAT-GATE-R2 C-18 / B16a : kepadatan rujukan visual (INFO dulu) ------
    if not prose_ok or e2_short:
        emit("N/A", "C-18 kepadatan rujukan URL/tanggal ISO (indikator B16)",
             na_short if short else (na_e2 if e2_short else na_format))
    else:
        u1k, i1k, nu, ni, nd = citation_density(prose_eval, max(1, nw_eval))
        # Perluasan M-13 (S14, C-31 diserap): penanda provenans inline [R-n]
        # dihitung PER KALIMAT (>1 penanda per 20 kata), bukan agregat dokumen.
        rn_dense = rmark_dense_count(paras)
        name18 = "C-18 kepadatan rujukan URL/tanggal ISO (indikator B16)"
        detail = ("URL mentah %.1f/1.000 kata (%d), tanggal ISO %.1f/1.000 (%d), "
                  "tanggal bernama %d; kalimat padat penanda [R-n] %d (>1 penanda "
                  "per 20 kata, perluasan M-13; remedinya pindahkan mark ke baris "
                  "tabel, jangan hapus rujukan)"
                  % (u1k, nu, i1k, ni, nd, rn_dense))
        # STATUS PANTAUAN: ambang vonis ditetapkan setelah kalibrasi korpus.
        emit("INFO", name18, detail + " - mode pantauan, belum menagih")

    # --- NAT-GATE-R2 C-19 / B16b : daftar istilah (tanpa ambang panjang) -----
    # PUTUSAN USER 30-09: ambang 'dokumen panjang >= 6.000 kata' DICABUT -
    # kehadiran daftar istilah dinilai pada semua berkas berprosa kanal panjang,
    # tanpa menunggu dokumen mencapai ukuran tertentu.
    if not prose_ok:
        emit("N/A", "C-19 daftar istilah hadir (indikator B16)", na_format)
    elif short:
        emit("N/A", "C-19 daftar istilah hadir (indikator B16)",
             "tidak berlaku di kanal pendek '%s' (D-TA-05)" % channel)
    elif has_glossary(doc):
        emit("PASS", "C-19 daftar istilah hadir (indikator B16)",
             "bagian daftar istilah/glosarium ditemukan")
    else:
        # STATUS PANTAUAN dulu: menaikkan ke FAIL akan menghukum banyak artefak
        # terbit; jalur ini sekaligus mengaktifkan pengecualian glosarium C-13.
        emit("INFO", "C-19 daftar istilah hadir (indikator B16)",
             "tidak ada bagian daftar istilah/glosarium "
             "(H.4.1 mewajibkan pada dokumen panjang; mode pantauan)")

    # --- NAT-GATE-R2 C-20 / B16c : suara penulis (INFO dulu) ------------------
    if not prose_ok or e2_short:
        emit("N/A", "C-20 suara penulis: Kami/stance vs 'penulis' (indikator B16)",
             na_short if short else (na_e2 if e2_short else na_format))
    else:
        k1k, p1k, s1k, nk, np_ = voice_presence(prose_eval, max(1, nw_eval))
        # Data gabungan sapaan K2 (S14, M-16 diserap ke M-06): dibangun dari nol
        # (v1.8.x nol alamat untuk kamu/Yth./Bapak/Ibu/Saudara). DATA dulu -
        # vonis kenaikan predikat ikut keputusan naskah final langkah 11.
        _sap = dict(sapaan_k2_counts(prose_eval))
        sap_str = ", ".join("%s=%d" % (l, _sap[l])
                            for l in ("kamu", "Yth.", "Bapak", "Ibu", "Saudara"))
        name20 = "C-20 suara penulis: Kami/stance vs 'penulis' (indikator B16)"
        detail = ("Kami %.1f/1.000 kata (%d), klausa sikap %.1f/1.000, "
                 "'penulis' %d kemunculan; sapaan K2 [%s] (data, belum menagih)"
                 % (k1k, nk, s1k, np_, sap_str))
        if nk == 0 and np_ >= 2:
            # pola LAPORAN-ADINT: tanpa suara institusional, rujukan diri 'penulis'
            emit("INFO", name20, detail + " - TANPA sapaan Kami; suara penulis "
                 "hilang (H.1.2; mode pantauan)")
        else:
            emit("INFO", name20, detail + " - mode pantauan, belum menagih")

    # --- NAT-GATE-R2 C-21 : manifest visual docx/pptx (kepala vs objek) ------
    # Bukti (user 30-09): RAFIF-MOBILE 385 halaman = 0 gambar tertanam di docx
    # maupun pdf; kebutuhan diagram dilarapkan ke tabel. Yang bisa dihitung
    # deterministik: kepala 'Gambar k.n' yang menyatakan objek tetapi objeknya
    # tidak tertanam (artefak janji visual kosong).
    if doc.fmt in ("docx", "pptx") and doc.media_count is not None:
        n_media = doc.media_count
        caps = len(re.findall(r"\b[Gg]ambar\s+\d+(?:\.\d+)?\b", prose_src))
        name21 = "C-21 manifest visual: kepala Gambar vs objek tertanam"
        if caps and n_media == 0:
            emit("FAIL", name21,
                 "%d kepala 'Gambar k.n' dinyatakan tetapi 0 gambar tertanam - "
                 "visual piatu (jalur baku: /create-image-gsp, Module I.11)" % caps)
        elif caps and n_media < caps // 3:
            emit("INFO", name21,
                 "%d kepala vs %d objek tertanam - rasio rendah, periksa (mode "
                 "pantauan)" % (caps, n_media))
        else:
            emit("PASS", name21, "%d kepala, %d objek tertanam" % (caps, n_media))
    else:
        emit("N/A", "C-21 manifest visual: kepala Gambar vs objek tertanam",
             "hitung objek hanya untuk docx/pptx yang paketnya terbaca")

    # --- NAT-GATE-R2 guard ekstraksi PDF --------------------------------------
    # Bukti (30-09): ekstraksi baris PDF memecah kalimat - RAFIF-MOBILE terbaca
    # 5,8 kata/kalimat padahal sumber aslinya 29,5. Metrik panjang pada pdf TIDAK
    # bisa dipercaya penuh; laporkan NEEDS_REVIEW, jangan PASS/FAIL senyap.
    if doc.fmt == "pdf" and prose_ok and not short:
        emit("INFO", "guard ekstraksi PDF",
             "metrik panjang (C-6/C-7/C-15/C-16/C-14) dihitung dari teks berpotongan "
             "baris - vonisnya NEEDS_REVIEW, bandingkan dengan sumber markdown/docx "
             "sebelum dieksekusi (preseden ukur 30-09: 5,8 vs asli 29,5 kata/kalimat)")

    # --- NAT-GATE-R3 C-22 / B17 : lengkung latar-ke-tujuan (INFO dulu) -------
    # Struktur bab dipotong SEKALI untuk keempat detektor R3 (dokumen nyata 1,2 MB).
    chaps_r3 = (chapters_from_text(doc.readable_text())
                if (prose_ok and not short) else None)
    if not prose_ok or short:
        emit("N/A", "C-22 lengkung latar-ke-tujuan pada kerangka bab (indikator B17)",
             na_short if short else na_format)
    else:
        chaps = chaps_r3
        name22 = "C-22 lengkung latar-ke-tujuan pada kerangka bab (indikator B17)"
        spine = spine_titles(doc.readable_text())
        if len(spine) < 4:
            emit("N/A", name22,
                 "struktur bab tidak terdeteksi (<4 penanda BAB/heading) - "
                 "lengkung tidak dinilai")
        else:
            start_i, end_i = arc_positions(spine)
            n = len(spine)
            detail = "%d bab; awal=%s; tujuan=%s" % (
                n,
                ("bab %d" % (start_i + 1)) if start_i is not None else "TIDAK ADA",
                ("bab %d" % (end_i + 1)) if end_i is not None else "TIDAK ADA")
            ok = (start_i is not None and end_i is not None
                  and end_i > start_i and end_i >= n - max(2, n // 4))
            if ok:
                emit("PASS", name22, detail + " - runtut latar ke tujuan")
            else:
                emit("INFO", name22, detail + " - lengkung tidak lengkap "
                     "(mode pantauan; tinjau urutan bab, Module H.3.5)")

    # --- NAT-GATE-R3 C-23 / B18 : sambungan antar bab (INFO dulu) ------------
    if not prose_ok or short:
        emit("N/A", "C-23 sambungan naratif antar bab >= 60% (indikator B18)",
             na_short if short else na_format)
    else:
        chaps = chaps_r3
        name23 = "C-23 sambungan naratif antar bab >= 60% (indikator B18)"
        if chaps is None or len(chaps) < 4:
            emit("N/A", name23, "struktur bab tidak terdeteksi - tidak dinilai")
        else:
            joined = 0
            for ti, body in chaps:
                edge = _edge_sentences(body, True) + " " + _edge_sentences(body, False)
                if _NAR_BACK_RE.search(edge) or _NAR_FWD_RE.search(edge):
                    joined += 1
            share = 100.0 * joined / len(chaps)
            detail = "%d/%d bab membuka atau menutup dengan sambungan (%.0f%%)" % (
                joined, len(chaps), share)
            if share < 60:
                emit("INFO", name23, detail + " - banyak bab berdiri sendiri "
                     "(mode pantauan; Module H.3.5 butir 2)")
            else:
                emit("PASS", name23, detail)

    # --- NAT-GATE-R3 C-24 / B19 : momen pembalik ada (MENAGIH, biner) --------
    if not prose_ok or short:
        emit("N/A", "C-24 momen pembalik hadir di badan dokumen (indikator B19)",
             na_short if short else na_format)
    else:
        chaps = chaps_r3
        name24 = "C-24 momen pembalik hadir di badan dokumen (indikator B19)"
        if chaps is None or len(chaps) < 4:
            emit("N/A", name24, "struktur bab tidak terdeteksi - tidak dinilai")
        else:
            n = len(chaps)
            lo, hi = n // 4, n - max(1, n // 4)   # 'badan' = bukan pembuka/penutup
            hits = []
            for i in range(lo, max(lo + 1, hi)):
                ti, body = chaps[i]
                m = _NAR_TURN_RE.search(body)
                if m:
                    hits.append((i + 1, ti[:36], m.group(0)[:24]))
            if hits:
                emit("PASS", name24,
                     "%d bab memuat momen pembalik; pertama: bab %d '%s' "
                     "(penanda '%s')" % (len(hits), hits[0][0], hits[0][1],
                                         hits[0][2]))
            else:
                emit("FAIL", name24,
                     "0 momen pembalik di %d bab badan (%d-%d): dokumen berjalan "
                     "datar tanpa titik yang membalik pemahaman pembaca "
                     "(Module H.3.5 butir 3)" % (hi - lo, lo + 1, hi))
                triggered.append("B19")

    # --- NAT-GATE-R3 C-25 / B20 : bab-katalog (INFO dulu) --------------------
    if not prose_ok or short:
        emit("N/A", "C-25 porsi prosa naratif per bab >= 30% (indikator B20)",
             na_short if short else na_format)
    else:
        chaps = chaps_r3
        name25 = "C-25 porsi prosa naratif per bab >= 30% (indikator B20)"
        if chaps is None or len(chaps) < 4:
            emit("N/A", name25, "struktur bab tidak terdeteksi - tidak dinilai")
        else:
            catalogs = []
            for i, (ti, body) in enumerate(chaps):
                share, total = narrative_share(body)
                if total >= 200 and share < 0.30:
                    catalogs.append((i + 1, ti[:32], share))
            if catalogs:
                worst = min(catalogs, key=lambda x: x[2])
                emit("INFO", name25,
                     "%d/%d bab di bawah 30%% prosa; terburuk bab %d '%s' "
                     "(%.0f%%) - mode pantauan (Module H.3.5 butir 4)"
                     % (len(catalogs), len(chaps), worst[0], worst[1],
                        100 * worst[2]))
            else:
                emit("PASS", name25,
                     "%d bab semuanya di atas porsi prosa 30%%" % len(chaps))

    # --- GAYA-AHLI-1005 S14 (putusan t_dbb77bfe): C-26/C-27/C-28/C-33 + INFO
    # pembuka M-09. PREDIKAT: seluruhnya INFO dulu (syarat putusan - naik ke
    # FAIL hanya setelah retrofit korpus mencatat nol positif palsu). Sadar
    # akan temuan Seksi 0 putusan: FAIL di nomor > C-25 tidak otomatis
    # memblokir karena VERDICT dirakit dari absolut() + HIGH_INDICATORS; saat
    # predikat naik, pemblokir WAJIB ditambahkan lewat salah satu jalur itu
    # secara eksplisit - bukan sebagai efek samping emit("FAIL"). Semua bekerja
    # pada LAPIS PROSA SCANNER dengan pemecah kanon sentences_of, populasi
    # bernilai identik kalibrasi (>=4 kata, prosa, non-enumerasi), pada lapisan
    # yang sudah menghormati blok kutipan D18 (paras/prose_eval gabungan).
    sents_val = []
    for _ps in paras:
        for _s in sentences_of(_ps):
            if (len(words_of(_s)) >= 4 and _dup_prose(_s)
                    and not _is_enumeration(_s)):
                sents_val.append(_s)
    nw_val = sum(len(words_of(s)) for s in sents_val)
    s14_na = (na_short if short else
              na_e2 if (e2_short or len(sents_val) < 3 or nw_val < 40) else na_format)
    s14_ok = prose_ok and not short and len(sents_val) >= 3 and nw_val >= 40

    # C-26 (M-01): plafon kepadatan klausa. Ambang 2,2 / 20% dibekukan putusan;
    # kanal kitab runtuh INFO mengikuti preseden C-15/C-16 (PUTUSAN t_77fd88c3).
    if not s14_ok:
        emit("N/A", "C-26 kepadatan klausa rata-rata <= 2,2 dan rantai >=4 <= 20%"
             " (mode pantauan)", s14_na)
    else:
        mc_s14, ch_s14, ns_s14 = clause_summary(clause_delim_stats(paras))
        name26 = ("C-26 kepadatan klausa rata-rata <= 2,2 dan rantai >=4 <= 20%"
                  " (mode pantauan)")
        det26 = ("%.2f pemisah klausa/kalimat, %.1f%% kalimat berantai >=4 dari %d "
                 "kalimat bernilai" % (mc_s14, ch_s14, ns_s14))
        if kitab:
            emit("INFO", name26, det26 + " - kanal kitab: vonis panjang milik "
                 "gerbang misi P1d, runtuh INFO (preseden t_77fd88c3)")
        elif mc_s14 > 2.2 or ch_s14 > 20.0:
            emit("INFO", name26, det26 + " - DI ATAS ambang 2,2/20% (INFO dulu "
                 "sampai retrofit nol positif palsu; syarat putusan M-01)")
        else:
            emit("PASS", name26, det26)

    # C-27 (M-02): plafon rata-rata kata/kalimat. Objek ukur = avg_words lapis
    # prosa scanner (revisi putusan: BUKAN angka lapis ekstrak r3_metrics_docx).
    # Plafon 32,0 = tepi atas target K2 21-32; koordinat C-16 (seksi terburuk)
    # tidak diubah. Kanal kitab memakai plafon P1a yang sudah ada di C-6.
    if not s14_ok:
        emit("N/A", "C-27 rata-rata kata per kalimat <= 32 plafon K2 (mode pantauan)",
             s14_na)
    else:
        avg_s14 = (sum(len(words_of(s)) for s in sents_val) / float(len(sents_val)))
        name27 = "C-27 rata-rata kata per kalimat <= 32 plafon K2 (mode pantauan)"
        det27 = ("%.1f kata/kalimat dari %d kalimat bernilai; plafon 32,0 "
                 "(target K2 21-32)" % (avg_s14, len(sents_val)))
        if kitab:
            emit("INFO", name27, det27 + " - kanal kitab: plafon P1a ditegakkan "
                 "C-6, tidak diduplikasi (preseden t_77fd88c3)")
        elif avg_s14 > 32.0:
            emit("INFO", name27, det27 + " - DI ATAS plafon (INFO dulu sampai "
                 "retrofit nol positif palsu; syarat putusan M-02)")
        else:
            emit("PASS", name27, det27)

    # C-28 (M-10): subjek verba keputusan = artefak pipa data, tanpa pelaku
    # manusia. Daftar tertutup di konstanta (audit per kata). Ambang putusan
    # ">2/1000" terbukti TERLALU LONGGAR di lapis scanner (kalibrasi S14:
    # DATUM 2,19 DEMS 2,41 REKAP 1,48 RAFIF-AI 1,33 vs manusia ED2 0,00 KAK
    # 0,28) - dipakai INFO 1,0/1000 sambil menunggu vonis controller.
    if not s14_ok:
        emit("N/A", "C-28 subjek verba keputusan bukan artefak alat <= 1,0/1.000 kata"
             " (mode pantauan)", s14_na)
    else:
        alat28, manus28, netral28 = decision_subject_counts(sents_val)
        r28 = 1000.0 * alat28 / max(1, nw_val)
        name28 = ("C-28 subjek verba keputusan bukan artefak alat <= 1,0/1.000 kata"
                  " (mode pantauan)")
        det28 = ("subjek alat %.2f/1.000 kata (%d), subjek manusia %d, netral %d; "
                 "ambang INFO 1,0/1.000 hasil kalibrasi lapis scanner (putusan "
                 "usulkan >2 - terlalu longgar di lapis ini)"
                 % (r28, alat28, manus28, netral28))
        if r28 > 1.0:
            emit("INFO", name28, det28 + " - DI ATAS ambang (INFO dulu; syarat "
                 "putusan M-10)")
        else:
            emit("PASS", name28, det28)

    # C-33 (M-15): konsistensi konvensi numerik DALAM satu dokumen. Pembanding
    # bekerja pada kelas varian (rentang nilai), bukan token mentah; varian dari
    # blok kutipan sudah keluar lewat prose_eval gabungan (syarat M-15).
    if not prose_ok or short:
        emit("N/A", "C-33 konsistensi konvensi numerik dalam dokumen (mode pantauan)",
             na_short if short else na_format)
    else:
        mixes33 = numeric_variant_mixes(prose_eval)
        name33 = "C-33 konsistensi konvensi numerik dalam dokumen (mode pantauan)"
        if mixes33:
            emit("INFO", name33,
                 "%d kelas varian bercampur: %s - INFO dulu; naik ke FAIL hanya "
                 "bila satu varian berpopulasi kecil vs pasangannya (syarat "
                 "putusan M-15)" % (len(mixes33), "; ".join(mixes33)))
        else:
            emit("PASS", name33, "tidak ada kelas varian numerik bercampur")

    # M-09 (rasio pembuka, tanpa nomor C - pantauan murni): aktif HANYA di atas
    # 2.000 kalimat (syarat putusan; definisi pembuka dibekukan: kata pertama
    # setelah normalisasi case + strip tanda baca, lihat impl-notes).
    if not s14_ok or len(sents_val) <= 2000:
        emit("N/A", "rasio pembuka kalimat berbeda >= 0,20 (INFO M-09, >2.000 "
             "kalimat saja)",
             "aktif hanya pada dokumen > 2.000 kalimat (syarat putusan M-09); "
             "terhitung %d kalimat bernilai" % len(sents_val))
    else:
        # Definisi pembuka DIBEKUKAN sesuai syarat putusan M-09: kata pertama
        # setelah strip karakter pembuka (tanda kutip/kurung/braket/spasi) lalu
        # normalisasi case lalu strip tanda baca. Disusun dengan chr() agar
        # berkas sumber tetap bebas tanda kutip ganda dalam literal regex.
        _lead_re = re.compile("^[" + chr(34) + chr(39) + "(\[\s]+")
        _strip_ch = ".,;:!?" + chr(34) + chr(39) + "()[]"
        openers9 = []
        for s in sents_val:
            w0 = _lead_re.sub("", s).lower().strip(_strip_ch)
            openers9.append(w0.split()[0] if w0.split() else "")
        ratio9 = len(set(openers9)) / float(len(openers9))
        name9 = ("rasio pembuka kalimat berbeda >= 0,20 (INFO M-09, >2.000 "
                 "kalimat saja)")
        if ratio9 < 0.20:
            emit("INFO", name9, "%.3f dari %d kalimat - di bawah 0,20 (pantauan, "
                 "bukan tagihan)" % (ratio9, len(openers9)))
        else:
            emit("PASS", name9, "%.3f dari %d kalimat" % (ratio9, len(openers9)))


    emit("N/A", "C-11 kesimpulan datar tanpa implikasi (indikator B9)",
         "penilaian juri manusia (RT 5.3), di luar cakupan scanner deterministik")

    # --- C-10 : marker naturalisasi -----------------------------------------
    if short:
        emit("N/A", "C-10 marker naturalisasi pada deliverable",
             "tidak berlaku di kanal pendek '%s' (D-TA-05)" % channel)
    elif channel == "kanban":
        emit("N/A", "C-10 marker naturalisasi pada deliverable",
             "summary/komentar kanban bukan berkas deliverable (D-TA-07)")
    else:
        # C-10 hanya mengakui marker pada posisi sah (lihat MARKER_LINE_RE):
        # kalimat yang menjelaskan format marker, contoh di blok kode, sel
        # tengah tabel, dan placeholder sudut <...> BUKAN marker (kartu
        # t_19e648d4; positif palsu gate-options seksi 3 butir K-2).
        pos = find_naturalization_marker(doc)
        if pos:
            emit("PASS", "C-10 marker naturalisasi pada deliverable",
                 "marker ditemukan (%s)" % pos)
        elif opts.require_marker:
            emit("FAIL", "C-10 marker naturalisasi pada deliverable",
                 "marker 'naturalisasi: PASS (<skrip>, <tanggal>)' tidak ditemukan "
                 "pada posisi sah (frontmatter atau baris mandiri kaki berkas)")
        else:
            emit("N/A", "C-10 marker naturalisasi pada deliverable",
                 "marker belum ada; aktifkan --require-marker untuk gate pra-terbit")

    # --- agregasi D-TA-09 ----------------------------------------------------
    trig = sorted(set(triggered))
    high = [t for t in trig if t in HIGH_INDICATORS]
    agg_name = "D-TA-09 agregasi indikator berat (>=2 berat atau 3+ HIGH)"
    if short or not prose_ok:
        emit("N/A", agg_name,
             "metrik berat tidak berlaku di kanal '%s' / format '%s'" % (channel, doc.fmt))
    elif len(trig) >= 2 or len(high) >= 3:
        emit("FAIL", agg_name,
             "%d indikator berat terpicu [%s]; HIGH %d -> wajib revisi sebelum distribusi"
             % (len(trig), ", ".join(trig), len(high)))
    else:
        emit("PASS", agg_name,
             "%d indikator berat terpicu%s" % (len(trig), (" [%s]" % ", ".join(trig)) if trig else ""))
    if triggered_all:
        emit("INFO", "D-TA-09 DIKECUALIKAN blok berpenanda kebijakan",
             "%d indikator berat terpicu pada lapisan penuh tetapi dikecualikan oleh "
             "blok berpenanda kebijakan [%s] (gate-options seksi 8)"
             % (len(set(triggered_all)), ", ".join(sorted(set(triggered_all)))))
    for reason in pol_invalid:
        emit("INFO", "penanda kebijakan tanpa rujukan kartu DITOLAK",
             "alasan '%s' tidak memuat rujukan kartu t_xxxxxxxx -> blok tidak sah, "
             "seluruh check tetap jalan (gate-options 8.1)" % reason)
    for reason in quote_invalid:
        emit("INFO", "penanda Blok Kutipan tanpa rujukan sumber DITOLAK",
             "alasan '%s' tidak memuat rujukan sumber (kartu t_xxxxxxxx, kata "
             "sumber/from/pengirim/dari, arsip/verbatim, nama berkas, atau akun @)"
             " -> blok tidak sah, seluruh check tetap jalan (D18 lapis dua, "
             "putusan M-03)" % reason)
    if qd_on:
        _qt = "\n".join(seg.text for seg, fl in zip(doc.segments, quote_flags)
                        if fl)
        nq = (len(frasa_hits(_qt, BLACKLIST_A4)) + len(frasa_hits(_qt, BLACKLIST_A6))
              + len(frasa_hits(_qt, BLACKLIST_A7))
              + len(frasa_hits(_qt, BLACKLIST_A5))
              + len(frasa_hits(_qt, _A5_CODE_NAMES)))
        if nq:
            emit("INFO", "A4/A5/A6/A7 DIKECUALIKAN blok kutipan D18",
                 "%d temuan daftar hitam duduk dalam blok kutipan berpenanda sah "
                 "dan dikecualikan dari vonis (I-5: prosa surat/vendor bukan karya "
                 "penulis GSP); C-1/C-2/C-3/C-5 tetap mutlak" % nq)

    for note in doc.notes:
        emit("INFO", "catatan ekstraksi", note)
    return res


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
def render(rows):
    lines = []
    for i, (status, nama, detail) in enumerate(rows, 1):
        line = "CHECK %d: %s - %s" % (i, status, nama)
        if detail:
            line += " | %s" % detail
        lines.append(line)
    fails = sum(1 for s, _, _ in rows if s == "FAIL")
    lines.append("VERDICT: %s" % ("FAIL" if fails else "PASS"))
    return lines, fails


# ---------------------------------------------------------------------------
# Selftest (membangun artefak sementara, menjalankan pipeline nyata)
# ---------------------------------------------------------------------------
def _want_fail(label, rows, code):
    got = sorted(set(s for s, n, d in rows if n.startswith(code)))
    ok = "FAIL" in got
    return [("PASS" if ok else "FAIL", "selftest %s memicu FAIL pada %s" % (label, code),
             "status aktual: " + "/".join(got) if not ok else "")]


def _want_status(label, rows, code, want):
    got = sorted(set(s for s, n, d in rows if n.startswith(code)))
    ok = want in got
    return [("PASS" if ok else "FAIL", "selftest %s -> %s %s" % (label, code, want),
             "status aktual: " + "/".join(got) if not ok else "")]


def _want_no_fail(label, rows):
    bad = sorted(set(n for s, n, d in rows if s == "FAIL"))
    return [("PASS" if not bad else "FAIL", "selftest %s" % label,
             "" if not bad else "FAIL tak terduga: " + "; ".join(bad[:3]))]


def _want_na_all(label, rows, codes):
    got = tuple(sorted(c for c in codes
                       if any(s == "N/A" and n.startswith(c) for s, n, d in rows)))
    ok = got == tuple(sorted(codes))
    return [("PASS" if ok else "FAIL", "selftest %s" % label,
             "N/A pada " + ",".join(got) if ok else "N/A tidak lengkap: " + ",".join(got))]


def selftest(opts):
    rows = []
    tmp = tempfile.mkdtemp(prefix="scanfp-selftest-")
    try:
        em, md, en = EM_DASH, MID_DOT, EN_DASH

        def write(name, content):
            p = os.path.join(tmp, name)
            payload = content.encode("utf-8") if isinstance(content, str) else content
            with open(p, "wb") as fh:
                fh.write(payload)
            return p

        def run(path, channel="doc"):
            return evaluate(scan_one(path, opts), channel, opts).rows

        # 1 em dash literal pada .md -> C-1 FAIL
        r = run(write("t1.md", "Laporan audit lapangan %s 12 temuan kritis.\n" % em))
        rows += _want_fail("em dash literal (md)", r, "C-1")

        # 2 em dash lewat escape di snippet emitter .py -> C-1 FAIL
        r = run(write("t2.py", "FOOTER = 'Halaman 4' + '" + _BS + "u2014' + 'Mei'\n"))
        rows += _want_fail("em dash escape (py, kasus emitter)", r, "C-1")

        # 3 em dash lewat entity HTML desimal + heksadesimal -> C-1 FAIL
        r = run(write("t3.html", "<p>Audit " + _AMP + "#8212; selesai</p>"
                                 "<p>B " + _AMP + "#x2014; tutup</p>\n"))
        rows += _want_fail("em dash entity (html)", r, "C-1")

        # 4 middle dot tanpa penanda D16 -> C-2 FAIL
        r = run(write("t4.md", "Ringkasan Eksekutif %s Triwulan III\n" % md))
        rows += _want_fail("middle dot tanpa D16", r, "C-2")

        # 5 middle dot dengan penanda D16 -> dikecualikan (PASS)
        r = run(write("t5.md", "Header %s Subheader\n\n> Penanda D16: kutipan verbatim "
                               "master design, blok terkendali.\n" % md))
        rows += _want_status("middle dot dengan penanda D16", r, "C-2", "PASS")

        # 6 en dash dalam rentang angka -> INFO, bukan FAIL (D-TA-04)
        r = run(write("t6.md", "Masa kontrak 2026%s2028 sudah ditandatangani hari ini "
                               "oleh kami dan pihak kontraktor.\n" % en), "chat")
        rows += _want_no_fail("en dash rentang angka bukan pelanggaran (D-TA-04)", r)
        rows.append(("PASS" if any(s == "INFO" and n.startswith("en dash") for s, n, d in r)
                     else "FAIL", "selftest en dash dilaporkan sebagai INFO", ""))

        # 7 frasa A4/A6/A7 -> C-4 FAIL
        r = run(write("t7.md", "Di era digital yang berkembang pesat, sistem kami bekerja. "
                               "Semoga membantu dan jangan ragu bertanya. Demikianlah "
                               "pembahasan di atas kami susun.\n"))
        rows += _want_fail("frasa A4/A6/A7", r, "C-4")

        # 8 emoji di kanal formal -> C-3 FAIL
        r = run(write("t8.md", "Deploy selesai %s sukses total\n" % chr(0x1F680)))
        rows += _want_fail("emoji di kanal formal", r, "C-3")

        # 9 label ruang kerja bocor -> A5 FAIL
        r = run(write("t9.md", "Saya memanggil kanban" + "_complete dulu lalu menutup "
                               "scratchpad sebelum laporan resmi ini kami serahkan.\n"))
        rows += _want_fail("label ruang kerja bocor ke narasi", r, "A5")

        # 10-11 kanal chat/notif: C-6/C-7/C-10 tidak berlaku (D-TA-05)
        p_clean = write("t10.txt", "Deploy selesai.\n")
        rc = run(p_clean, "chat")
        rows += _want_na_all("chat mematikan C-6/C-7/C-10 (D-TA-05)", rc,
                             ("C-6", "C-7", "C-10"))
        rn = run(p_clean, "notif")
        rows += _want_na_all("notif mematikan C-6/C-7/C-10 (D-TA-05)", rn,
                             ("C-6", "C-7", "C-10"))
        rows += _want_no_fail("chat pendek bersih -> VERDICT PASS", rc)

        # 12 json: nilai kunci mesin dikecualikan dari prosa, em dash tetap dihitung
        r = run(write("t12.json", json.dumps(
            {"metadata": {"sha256": "abc"}, "ringkasan": "Audit %s selesai" % em},
            ensure_ascii=False)))
        rows += _want_fail("em dash di nilai json tetap dihitung", r, "C-1")

        # 13 frontmatter YAML: dikecualikan dari metrik prosa, dihitung untuk C-1
        r = run(write("t13.md", "---\ntitle: Laporan %s\nnaturalisasi: PASS\n---\n\n"
                      "Isi laporan.\n" % em))
        rows += _want_fail("frontmatter ikut dihitung untuk U+2014", r, "C-1")

        # 14 agregasi D-TA-09: dokumen pendek berulang -> minimal 2 indikator
        #    (NAT-HIL-SC1: diperpanjang sampai >=40 kata agar tidak kena guard
        #    cuplikan pendek NAT-HIL-E2; maksud uji tetap agregasi)
        r = run(write("t14.md", "Sistem ini dapat bekerja dengan baik pada modul lama. "
                                "Sistem itu mungkin stabil bila beban rendah. "
                                "Hasilnya bisa dilihat pada log mingguan tim lapangan. "
                                "Modul baru berpotensi menyumbang selisih kecil saat "
                                "uji beban puncak berlangsung malam hari di gudang "
                                "produksi aktif maupun di simpul cadangan.\n"))
        rows += _want_fail("agregasi D-TA-09", r, "D-TA-09")

        # 15 artefak dokumen bersih -> tidak ada FAIL (kalimat >=25 kata, ada angka
        #    spesifik + pengakuan batasan, sesuai ambang H.2.1/H.5.3-5.4)
        r = run(write("t15.md", "# Laporan anggaran 2027\n\n"
                                "Kami menyusun pagu tahun anggaran 2027 sebesar 4,5 miliar "
                                "rupiah untuk tiga gudang produksi aktif dengan asumsi kurs "
                                "dolar tetap dan tanpa penambahan pegawai baru sepanjang "
                                "tahun berjalan. Angka tersebut mengacu pada realisasi "
                                "belanja tahun 2026 sebesar 3,9 miliar rupiah serta kontrak "
                                "perawatan berkala yang masih berjalan sampai triwulan "
                                "pertama tahun berikutnya. Perlu ditegaskan bahwa pagu itu "
                                "belum memasukkan biaya penggantian unit genset cadangan yang "
                                "baru akan diuji bebannya pada semester kedua, sehingga sisa "
                                "ruang fiskal kami tahan sebagai pos tak terduga. Karena itu "
                                "kami mengusulkan penjadwalan ulang belanja modal pada "
                                "triwulan kedua agar posisi kas tetap aman dan tidak "
                                "mengganggu pembayaran kontrak jasa keamanan yang berjalan "
                                "sejak 2024.\n"))
        rows += _want_no_fail("artefak dokumen bersih -> tidak ada FAIL", r)

        # 16 determinisme: dua run menghasilkan baris identik
        a = render(run(p_clean, "chat"))[0]
        b = render(run(p_clean, "chat"))[0]
        rows.append(("PASS" if a == b else "FAIL",
                     "selftest determinisme dua run byte-identik", ""))

        # 17 kontrol merah: berkas cacat WAJIB menghasilkan FAIL (gerbang tidak mati)
        r = run(write("t17.md", "Di era digital ini kami hadir %s dengan layanan.\n" % em))
        rows.append(("PASS" if any(s == "FAIL" for s, _, _ in r) else "FAIL",
                     "selftest berkas cacat menghasilkan FAIL (kontrol merah)", ""))

        # 18-20 format Office bila pustaka tersedia
        try:
            import docx
            d = docx.Document()
            d.add_paragraph("Rekap mingguan %s tiga proyek aktif." % em)
            buf = io.BytesIO()
            d.save(buf)
            r = run(write("t18.docx", buf.getvalue()))
            rows += _want_fail("docx em dash terdeteksi", r, "C-1")
        except Exception as exc:
            rows.append(("N/A", "selftest docx dilewati", type(exc).__name__))
        try:
            import openpyxl
            wb = openpyxl.Workbook()
            wb.active["A1"] = "Anggaran 2027"
            buf = io.BytesIO()
            wb.save(buf)
            r = run(write("t19.xlsx", buf.getvalue()), "etalase")
            rows += _want_no_fail("xlsx bersih -> tidak ada FAIL", r)
        except Exception as exc:
            rows.append(("N/A", "selftest xlsx dilewati", type(exc).__name__))
        try:
            import pptx
            prs = pptx.Presentation()
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            slide.shapes.title.text = "Deck %s bersih" % em
            buf = io.BytesIO()
            prs.save(buf)
            r = run(write("t20.pptx", buf.getvalue()), "deck")
            rows += _want_fail("pptx em dash terdeteksi", r, "C-1")
        except Exception as exc:
            rows.append(("N/A", "selftest pptx dilewati", type(exc).__name__))

        # 21 berkas biner tak dikenal -> tidak crash, tanpa FAIL
        r = run(write("t21.bin", b"\x89PNG\r\n\x1a\n\x00\x01\x02"), "etalase")
        rows += _want_no_fail("biner tak dikenal tidak crash", r)

        # --- penanda blok terkendali kebijakan (gate-options seksi 8, kartu
        # t_ec8bfdab): kontrol merah-hijau eksplisit, fixture cacat FAIL sebelum
        # penanda dipasang dan PASS sesudahnya; tanpa penanda tetap FAIL.
        frasa_cacat = ("Semoga membantu dan jangan ragu bertanya. Demikianlah "
                       "pembahasan di atas kami susun.\n")
        # 22a kontrol merah: fixture cacat TANPA penanda -> C-4 tetap FAIL
        r = run(write("t22a.md", frasa_cacat))
        rows += _want_fail("frasa cacat tanpa penanda kebijakan", r, "C-4")
        # 22b kontrol hijau: fixture cacat yang SAMA di dalam blok sah -> C-4 PASS
        r = run(write("t22b.md", "> Penanda Kebijakan: contoh aturan internal "
                                "berkas kebijakan, t_test01\n\n" + frasa_cacat))
        rows += _want_status("frasa cacat dalam blok berpenanda sah", r, "C-4", "PASS")
        rows.append(("PASS" if any(s == "INFO" and "DIKECUALIKAN" in n
                                   for s, n, d in r) else "FAIL",
                     "selftest pengecualian C-4 muncul sebagai baris INFO", ""))
        # 23 penanda TANPA rujukan kartu ditolak -> C-4 tetap FAIL + INFO ditolak
        r = run(write("t23.md", "> Penanda Kebijakan: contoh tanpa rujukan resmi\n\n"
                                + frasa_cacat))
        rows += _want_fail("penanda kebijakan tanpa rujukan kartu", r, "C-4")
        rows.append(("PASS" if any(s == "INFO" and "DITOLAK" in n
                                   for s, n, d in r) else "FAIL",
                     "selftest penanda tanpa rujukan dilaporkan INFO DITOLAK", ""))
        # 24 penanda TIDAK menyentuh C-1/C-2/C-3 (mutlak, putusan butir 1)
        r = run(write("t24.md", "> Penanda Kebijakan: contoh mutlak, t_test01\n\n"
                                "Laporan lapangan %s selesai %s tutup.\n" % (em, md)))
        rows += _want_fail("penanda kebijakan tidak menekan C-1", r, "C-1")
        rows += _want_fail("penanda kebijakan tidak menekan C-2", r, "C-2")
        # 25 blok tertutup oleh heading berikutnya: frasa setelah heading tetap FAIL
        r = run(write("t25.md", "> Penanda Kebijakan: contoh skop blok, t_test01\n\n"
                                + frasa_cacat +
                                "\n## Bagian lanjutan\n\n" + frasa_cacat))
        rows += _want_fail("blok kebijakan tertutup heading berikutnya", r, "C-4")
        # 26 metrik gaya (C-7) ikut lapisan luar blok: tiga paragraf pendek di
        #    dalam blok dipisah baris tabel (baris kosong bukan pemisah paragraf
        #    di mesin ini; heading menutup blok) -> lapisan penuh FAIL C-7, luar
        #    blok PASS C-7, baris INFO wajib muncul
        para_pendek = "Kalimat satu. Kalimat dua.\n"
        prosa_luar = ("Kami menyusun laporan panjang dengan angka 2027 dan mencatat "
                      "batasan pengukuran di dalamnya. Tim verifikasi mengulang "
                      "sapuan dua kali pada berkas yang sama. Hasil kedua run "
                      "scanner identik tanpa selisih satu baris pun. Ruang lingkup "
                      "dokumen ini terbatas pada berkas yang disebut eksplisit.\n")
        r = run(write("t26.md", "> Penanda Kebijakan: contoh gaya dokumen, t_test01\n"
                                "| a | b |\n" + para_pendek +
                                "| c | d |\n" + para_pendek +
                                "| e | f |\n" + para_pendek +
                                "\n## Bagian luar blok\n\n" + prosa_luar))
        rows += _want_status("C-7 menilai lapisan di luar blok berpenanda", r, "C-7", "PASS")
        rows.append(("PASS" if any(s == "INFO" and n.startswith("C-7 DIKECUALIKAN")
                                   for s, n, d in r) else "FAIL",
                     "selftest pengecualian C-7 muncul sebagai baris INFO", ""))
        # 27 varian heading '# Kebijakan:' juga dikenali (bentuk D16 kedua)
        r = run(write("t27.md", "# Kebijakan: contoh varian heading, t_test01\n\n"
                                + frasa_cacat))
        rows += _want_status("penanda kebijakan varian heading", r, "C-4", "PASS")

        # --- C-10 posisi marker sah (kartu t_19e648d4): teks yang MENJELASKAN
        # format marker tidak boleh dihitung sebagai marker. Opsi khusus dengan
        # require_marker aktif agar cabang C-10 menilai penuh pada kanal etalase.
        opts_rm = argparse.Namespace(**vars(opts))
        opts_rm.require_marker = True

        def run_rm(path, channel="etalase"):
            return evaluate(scan_one(path, opts_rm), channel, opts_rm).rows

        # 28 kalimat prosa yang menyebut format marker utuh -> C-10 FAIL
        # (positif palsu lama: regex seluruh lapisan terbaca)
        r = run_rm(write("t28.md", "Setiap deliverable wajib membawa marker "
                                  "naturalisasi: PASS (scan_ai_footprint.py, "
                                  "2026-09-02) di kaki berkas sesuai kebijakan "
                                  "yang berlaku.\n"))
        rows += _want_status("deskripsi format marker di prosa bukan marker",
                             r, "C-10", "FAIL")
        # 29 marker sungguhan sebagai baris footer mandiri -> C-10 PASS
        r = run_rm(write("t29.md", "Isi laporan dengan angka 2026 dan catatan "
                                  "batasan yang diakui.\n\nnaturalisasi: PASS "
                                  "(scan_ai_footprint.py, 2026-09-02)\n"))
        rows += _want_status("marker footer mandiri diakui", r, "C-10", "PASS")
        # 30 marker bentuk baris tabel (bentuk baku corpus hijau) -> C-10 PASS
        r = run_rm(write("t30.md", "Isi laporan dengan angka 2026 dan catatan "
                                  "batasan yang diakui.\n\n| naturalisasi: PASS "
                                  "| scan_ai_footprint.py | 2026-09-02 |\n"))
        rows += _want_status("marker baris tabel kaki diakui", r, "C-10", "PASS")
        # 31 marker di sel tengah tabel penjelasan (bentuk baris 20
        # kebijakan-naturalisasi.md) -> C-10 FAIL
        r = run_rm(write("t31.md", "| Kanal | Aturan | Cek |\n"
                                  "|---|---|---|\n"
                                  "| K6 Etalase | deliverable membawa marker "
                                  "naturalisasi: PASS (<skrip>, <tanggal>) | "
                                  "C-1..C-10 |\n"))
        rows += _want_status("marker dalam sel tengah tabel penjelasan",
                             r, "C-10", "FAIL")
        # 32 frontmatter YAML -> C-10 PASS (lapisan frontmatter tidak ikut
        # lapisan terbaca, jadi cabang lama justru negatif palsu di sini)
        r = run_rm(write("t32.md", "---\ntitle: Laporan 2026\nnaturalisasi: PASS\n"
                           "---\n\nIsi laporan dengan angka 2026 dan batasan.\n"))
        rows += _want_status("marker frontmatter YAML diakui", r, "C-10", "PASS")
        # 33 contoh marker di dalam blok kode berpagar -> C-10 FAIL
        # (blok kode = contoh pemakaian, bukan marker deliverable)
        r = run_rm(write("t33.md", "# Prosedur\n\nGunakan bentuk berikut:\n\n"
                                  "```\nnaturalisasi: PASS (scan_ai_footprint.py, "
                                  "2026-09-02)\n```\n\nTaruh di kaki berkas.\n"))
        rows += _want_status("contoh marker dalam blok kode berpagar",
                             r, "C-10", "FAIL")
        # 34 baris mandiri berisi placeholder sudut <skrip>, <tanggal> -> FAIL
        # (placeholder dokumentasi bukan nilai marker sungguhan)
        r = run_rm(write("t34.md", "Catatan format:\n\nnaturalisasi: PASS "
                                  "(<skrip>, <tanggal>)\n"))
        rows += _want_status("baris placeholder sudut bukan marker",
                             r, "C-10", "FAIL")

        # --- NAT-HIL-SC1 (kartu t_c79b5f6d): regresi backtracking id=292,
        # guard cuplikan pendek NAT-HIL-E2, indikator gaya catatan cepat
        # NAT-HIL-E1 (C-12/B10). ---
        # 35 regresi backtracking: fixture potongan nyata pesan gsp-custodian
        #    id=292 (baris pemisah 64 minus) WAJIB selesai < 15 detik. Bug
        #    v1.2.0: D16_MARKER_RE backtrack eksponensial, scanner membekukan
        #    sapuan penuh (verify-chat-sweep.md seksi 6). Dijalankan di utas
        #    daemon agar regresi terdeteksi sebagai FAIL, bukan gantung abadi.
        import threading as _th
        fx = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "fixtures", "regresi-id292.txt")
        if not os.path.exists(fx):
            rows.append(("FAIL", "selftest fixture regresi id=292 ada",
                         "berkas hilang: " + fx))
        else:
            box = {}

            def _scan_fx():
                try:
                    box["rows"] = run(fx, "kanban")
                except Exception as exc:               # pragma: no cover
                    box["err"] = exc
            th = _th.Thread(target=_scan_fx, daemon=True)
            th.start()
            th.join(15)
            if th.is_alive():
                rows.append(("FAIL", "selftest regresi id=292 selesai < 15 dtk",
                             "scanner masih backtrack tanpa selesai pada fixture"))
            elif "err" in box:
                rows.append(("FAIL", "selftest regresi id=292 selesai < 15 dtk",
                             "%s: %s" % (type(box["err"]).__name__, box["err"])))
            else:
                rows.append(("PASS", "selftest regresi id=292 selesai < 15 dtk", ""))
                # fixture memuat literal U+2014 verbatim dari sumber -> C-1
                # wajib tetap FAIL (kontrol bahwa scan nyata, bukan skip senyap)
                rows += _want_fail("fixture regresi id=292 memicu C-1",
                                   box["rows"], "C-1")

        # 36 guard NAT-HIL-E2: cuplikan pendek kanal doc (2 kalimat, < 40
        #    kata; contoh nyata S-11 sisi manusiawi) -> C-6/C-7 N/A, bukan
        #    FAIL positif palsu maupun PASS senyap.
        r = run(write("t36.md", "Video tidak melintasi firewall. Beban lintas "
                                "zona riil berada di bawah 100 Mbps terhadap "
                                "kapasitas minimal 1 Gbps, sehingga marginnya "
                                "sepuluh kali lipat.\n"), "doc")
        rows += _want_status("cuplikan pendek -> C-6 N/A (NAT-HIL-E2)",
                             r, "C-6", "N/A")
        rows += _want_status("cuplikan pendek -> C-7 N/A (NAT-HIL-E2)",
                             r, "C-7", "N/A")
        # 37 guard tidak melumpuhkan dokumen panjang: lapisan >=3 kalimat dan
        #    >=40 kata dengan rata-rata >=25 kata/kalimat tetap menilai C-6
        #    (regresi balik kontrol merah-hijau; guard hanya untuk cuplikan).
        r = run(write("t37.md", "# Uji\n\n"
                              "Kami menyusun laporan evaluasi gudang triwulan "
                              "ketiga dengan angka 2027 dan mencatat seluruh "
                              "batasan pengukuran pada lampiran terpisah agar "
                              "pembaca dapat menelusuri setiap keputusan yang "
                              "kami ambil sepanjang periode berjalan. Tim "
                              "verifikasi mengulang sapuan dua kali pada berkas "
                              "yang sama dan memastikan kedua hasil scanner "
                              "identik tanpa selisih satu baris pun sehingga "
                              "determinisme alat ukur tetap terjaga. Ruang "
                              "lingkup dokumen ini terbatas pada berkas yang "
                              "disebut eksplisit di daftar isi dan tidak "
                              "meliputi arsip lama yang belum dimigrasikan ke "
                              "registry fleet tahun ini.\n"))
        rows += _want_status("prosa panjang -> C-6 tetap dinilai",
                             r, "C-6", "PASS")
        # 38 indikator NAT-HIL-E1 merah: cuplikan gaya catatan cepat nyata
        #    (sisi mesin S-09: panah ASCII + rantai titik-koma fragmen) ->
        #    C-12 FAIL padahal v1.2.0 lolos total (juri memilih lawannya 2/2).
        r = run(write("t38.md", "gsp-master: 237->3 SKILL.md (trio controller); "
                                ".lean-policy + .no-bundled-skills tertulis; "
                                "backup zip tersimpan; check ok:true "
                                "skillCount:3; probe chat: indeks skill = 3 "
                                "entri trio.\n"), "kanban")
        rows += _want_fail("gaya catatan cepat memicu C-12 (NAT-HIL-E1)",
                           r, "C-12")
        # 39 NAT-HIL-E1 hijau: sisi manusiawi pasangan S-09 (narasi utuh,
        #    tanpa panah/rantai/singkatan) -> C-12 PASS.
        r = run(write("t39.md", "Rampasan profil menurunkan jumlah SKILL.md "
                                "dari 237 menjadi 3 berkas trio controller. "
                                "Marker kebijakan sudah tertulis dan cadangan "
                                "zip tersimpan di folder cadangan workspace. "
                                "Pemeriksaan kelengkapan melaporkan ok dengan "
                                "tiga skill, sementara uji chat menghasilkan "
                                "indeks skill berisi tiga entri trio.\n"),
                    "kanban")
        rows += _want_status("narasi formal -> C-12 PASS", r, "C-12", "PASS")
        # 40 sinyal tunggal (hanya panah teknis) tidak menaikkan vonis:
        #    C-12 PASS + baris INFO sinyal tunggal wajib muncul.
        r = run(write("t40.md", "Alur kerja: unduh berkas lalu jalankan "
                                "pemeriksaan harian rutin oleh tim lapangan "
                                "terlebih dahulu sebelum serah terima. Hasil "
                                "pemeriksaan dicatat pada lembar kendali "
                                "milik unit terkait. Konversi format dilakukan "
                                "lewat alat baku (mode luring -> mode daring) "
                                "sesuai prosedur tetap yang berlaku.\n"))
        rows += _want_status("sinyal tunggal -> C-12 PASS", r, "C-12", "PASS")
        rows.append(("PASS" if any(s == "INFO" and n.startswith("C-12 sinyal tunggal")
                                   for s, n, d in r) else "FAIL",
                     "selftest sinyal tunggal C-12 muncul sebagai INFO", ""))
        # 41 rujukan bentuk di dalam kode sebaris BUKAN pemakaian: berkas
        #    kebijakan yang mendokumentasikan daftar hitam (`masing2`, `yg`)
        #    dengan satu panah teknis tidak boleh divonis C-12 (kelas bug sama
        #    dengan positif palsu marker C-10 / CHECK 9: alat ukur buta
        #    deskripsi inline).
        r = run(write("t41.md", "Gaya catatan cepat memakai singkatan tak baku "
                                "seperti `masing2`, `yg`, dan `dgn` pada catatan "
                                "internal agen. Daftar ini dipelihara bersama "
                                "aturan lain di berkas kebijakan naturalisasi "
                                "fleet. Konversi dilakukan lewat alat baku "
                                "(mode luring -> mode daring) sesuai prosedur "
                                "tetap yang berlaku.\n"))
        rows += _want_status("rujukan backtick bukan pemakaian -> C-12 PASS",
                             r, "C-12", "PASS")
        # 42-45 regresi DEFECT-SENTSPLIT-C7 (kartu t_91146669, kontrak
        #    docs/2026-09-29_defect-scanner-sentsplit-c7): blok CEK DIRI
        #    bernomor "(1) ... (2) ... (3) ..." wajib terhitung >= 3 kalimat;
        #    bug v1.4.0 menggabungkannya jadi satu kalimat raksasa sehingga
        #    paragraf terlihat pendek dan menjatuhkan vonis palsu C-7/B2.
        blok_cekdiri = ("CEK DIRI. (1) Apa fungsi utama gerbang naturalisasi "
                        "dalam pipeline dokumen ini? (2) Mengapa vonis palsu "
                        "pada blok bernomor berbahaya bagi penulis bab lain? "
                        "(3) Bagaimana cara memperluas lookahead pemecah "
                        "kalimat agar mencakup penanda nomor?")
        n_blok = len(sentences_of(blok_cekdiri))
        rows.append(("PASS" if n_blok >= 3 else "FAIL",
                     "selftest blok (N) terhitung >= 3 kalimat",
                     "" if n_blok >= 3 else "terhitung %d kalimat" % n_blok))
        # 43 dua blok bernomor sebagai paragraf mandiri (heading memisahkan
        #    paragraf di mesin ini): basal menghitung tiap blok 2 kalimat ->
        #    2 paragraf pendek melebihi toleransi 1 -> C-7 FAIL palsu;
        #    tambalan bedah wajib melihat C-7 PASS.
        para_cek2 = ("LATIHAN. (1) Sebutkan tiga kanal yang mematikan C-6 "
                     "sesuai D-TA-05? (2) Mengapa kanal kanban dikecualikan "
                     "dari gerbang naturalisasi? (3) Kapan override register "
                     "boleh dipakai oleh penulis dokumen?")
        para_penutup = ("Paragraf penutup ini dibuat panjang dengan tiga "
                        "kalimat lengkap agar metrik lain tidak ikut terpicu "
                        "dan berkas uji tetap dinilai penuh oleh scanner. "
                        "Kalimat kedua membawa angka 2026 supaya uji berjalan "
                        "pada kanal dokumen yang menilai gaya. Kalimat ketiga "
                        "menutup blok tanpa menambah paragraf pendek baru.")
        r = run(write("t42.md", "# Uji satu" + chr(10) * 2 + blok_cekdiri
                      + chr(10) * 2 + "# Uji dua" + chr(10) * 2 + para_cek2
                      + chr(10) * 2 + "# Penutup" + chr(10) * 2 + para_penutup
                      + chr(10)))
        rows += _want_status("blok bernomor tidak memicu C-7 FAIL", r, "C-7", "PASS")
        # 44 fixture regresi permanen scripts/fixtures/regresi-sentsplit-c7.md:
        #    wajib ada dan C-7 tidak boleh vonis salah padanya.
        fx2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "fixtures", "regresi-sentsplit-c7.md")
        if not os.path.exists(fx2):
            rows.append(("FAIL", "selftest fixture regresi sentsplit ada",
                         "berkas hilang: " + fx2))
        else:
            rows += _want_status("fixture regresi sentsplit tidak divonis C-7",
                                 run(fx2), "C-7", "PASS")
        # 45 guard varian luas DITOLAK: angka biasa di awal kalimat tanpa
        #    kurung TIDAK boleh terpecah (regresi C-6 w08 bila dilonggarkan).
        digit_polos = "Ada 5 orang. 10 lainnya pergi meninggalkan tempat."
        n_digit = len(sentences_of(digit_polos))
        rows.append(("PASS" if n_digit == 1 else "FAIL",
                     "selftest digit awal tanpa kurung tidak terpecah",
                     "terhitung %d kalimat" % n_digit))

        # 90+ GAYA-AHLI-1005 S14 (putusan t_dbb77bfe): merah-hijau memakai kasus
        # positif-palsu TERDOKUMENTASI papan lintas-misi (CH02/CH05/CH06/CH08/
        # CH17), bukan fixture karangan baru (syarat tutup Seksi 8 putusan).
        # 90 M-05 hijau CH17: 'such as an aisle name' BUKAN 'as an ai' (kasus
        #    nyata RAFIF-ED2 divonis A4 oleh substring murni).
        r = run(write("t90.md", "Papan nama lorong di gudang utama zona B sudah "
              "mengikuti standar penandaan yang kami tetapkan bersama vendor pada "
              "Maret 2026 dengan tinggi pemasangan 2,20 meter dari lantai. Contoh "
              "bentuk penandaan yang sah adalah such as an aisle name pada rak zona "
              "B sepanjang 40 meter. Tim K3 memverifikasi 42 papan terpasang kokoh "
              "dan terbaca jelas dari jarak 5 meter saat inspeksi pagi, dengan "
              "keterbatasan jarak baca pada lorong sempit yang kami catat terpisah."))
        rows += _want_no_fail("selftest CH17 'such as an aisle' tidak divonis A4", r)
        # 91 M-05 merah: pemakaian asli 'as an ai' tetap FAIL (dua arah).
        r = run(write("t91.md", "Sebagai model bahasa, as an ai, saya menyusun "
                                "lapangan ini dengan hati-hati dan kami periksa ulang."))
        rows += _want_fail("selftest 'as an ai' asli memicu FAIL A4", r, "A4")
        # 92 M-05 merah: entri multi-kata bertanda seru 'sure! here' utuh.
        r = run(write("t92.md", "Balasan asisten: Sure! here the summary you asked "
                                "for, lengkap dengan tabel dan kami arsipkan."))
        rows += _want_fail("selftest 'sure! here' memicu FAIL A4", r, "A4")
        # 93 M-12 hijau CH06: nama entitas 'Hoober' tidak tersandung pola generik.
        r = run(write("t93.md", "Menurut Hoober (peneliti interaksi manusia dan "
              "mesin, edisi kedua), antarmuka yang baik menjelaskan konsekuensi "
              "sebelum pengguna menekan tombol, dan prinsip itu kami jadikan acuan "
              "desain formulir layanan pada 2026."))
        rows += _want_no_fail("selftest CH06 'Hoober' tidak divonis identifier", r)
        # 94 M-12 CH08: 'RigidbodyType2D' = identifier API pihak ketiga, KELAS
        #    LEMBUT: muncul INFO, tidak pernah FAIL walau sendirian.
        r = run(write("t94.md", "Objek permainan diberi RigidbodyType2D lalu disetel "
              "nilainya pada inspector sehingga fisika dua dimensi bekerja sesuai "
              "gravitasi yang kami pilih sendiri, dan catatan setelan kami arsipkan "
              "bersama berkas proyek versi 3 ini."))
        rows += _want_no_fail("selftest CH08 'RigidbodyType2D' tidak menjatuhkan FAIL", r)
        rows.append(("PASS" if any(s == "INFO" and n.startswith("perluasan C-13")
                                   and "RigidbodyType2D" in d for s, n, d in r)
                     else "FAIL",
                     "selftest CH08 'RigidbodyType2D' dilaporkan INFO kelas baru", ""))
        # 95 M-12: enum status ALLCAPS bergaris-bawah = INFO kelas baru.
        r = run(write("t95.md", "Status tiket berubah menjadi READY_FOR_REVIEW setelah "
              "verifikasi selesai, dan kami catat pergantian itu di log harian tim "
              "dokumentasi pada 5 Oktober 2026 bersama bukti tanda terima kerja."))
        rows += _want_no_fail("selftest enum READY_FOR_REVIEW tidak menjatuhkan FAIL", r)
        rows.append(("PASS" if any(s == "INFO" and n.startswith("perluasan C-13")
                                   and "READY_FOR_REVIEW" in d for s, n, d in r)
                     else "FAIL",
                     "selftest enum READY_FOR_REVIEW dilaporkan INFO", ""))
        # 96 M-04 hijau: boilerplate tanda tangan berulang sah tidak dihitung C-14.
        sig = "Hormat kami, Tim Rekayasa GSP. " * 3
        r = run(write("t96.md", "Berdasarkan hasil pemeriksaan lapangan selama tiga "
              "hari berturut-turut kami menemukan dua belas deviasi kecil pada panel "
              "distribusi utama dan mencatat seluruhnya dalam berita acara resmi "
              "yang ditandatangani kedua pihak. " + sig))
        rows += _want_status("selftest M-04 boilerplate berulang tidak FAIL C-14",
                             r, "C-14", "PASS")
        # 97 M-04 merah: gagasan narasi ditulis ulang dua kali tetap FAIL C-14.
        dup = ("Panel distribusi utama mengalami lonjakan suhu pada jam beban puncak "
               "sehingga tim melakukan pengukuran ulang arus dan tegangan di lokasi. ")
        r = run(write("t97.md", "Laporan ini disusun oleh tim rekayasa lapangan. " * 2
                                + dup + dup))
        rows += _want_fail("selftest M-04 narasi dobel memicu FAIL C-14", r, "C-14")
        # 98 M-03 lapis dua hijau: blok kutipan ber-rujuk sumber mengecualikan
        #    prosa surat vendor dari A4/C-4 (kasus I-5 paket VENDOR-V18/V19).
        r = run(write("t98.md", "Berikut lampiran surat masuk dari mitra kami beserta "
           "tindak lanjut internal yang telah kami sepakati bersama pada rapat "
           "minggu lalu di kantor pusat.\n\n"
           "> Blok Kutipan: sumber surat vendor PT Alpha, arsip email 2026-09-12\n"
           "> Semoga membantu dan jangan ragu bertanya jika ada bagian yang perlu "
           "dijelaskan lebih lanjut oleh tim kami.\n"))
        rows += _want_status("selftest M-03 blok kutipan ber-sumber mengecualikan A4",
                             r, "A4", "PASS")
        # 99 M-03 lapis dua merah: penanda TANPA rujukan sumber ditolak -> A4 FAIL.
        r = run(write("t99.md", "Berikut lampiran surat masuk dari mitra kami beserta "
           "tindak lanjut internal yang telah kami sepakati bersama pada rapat "
           "minggu lalu di kantor pusat.\n\n"
           "> Blok Kutipan: catatan penting belaka\n"
           "> Semoga membantu dan jangan ragu bertanya jika ada bagian yang perlu "
           "dijelaskan lebih lanjut oleh tim kami.\n"))
        rows += _want_fail("selftest M-03 blok kutipan tanpa sumber DITOLAK (A4 FAIL)",
                           r, "A4")
        # 100 M-03 lapis satu: berkas berpenanda D16 dengan em dash di baris
        #     provenans -> baris INFO aparatus hadir; vonis C-1 TETAP FAIL (mutlak).
        r = run(write("t100.md", "# Standar Rumah\n\nProvenans: salinan baku%sversi 3"
                              "\n\n> Penanda D16: aparatus rumah terkendali.\n"
                              % em))
        rows += _want_fail("selftest M-03 lapis satu: C-1 tetap mutlak FAIL", r, "C-1")
        rows.append(("PASS" if any(s == "INFO" and n.startswith("rincian aparatus")
                                   for s, n, d in r) else "FAIL",
                     "selftest M-03 lapis satu: INFO rincian aparatus hadir", ""))
        # 101 M-01 C-26 merah: kalimat rapat klausa (rantai >=4 koma) -> INFO.
        cl = ("Tim lapangan memeriksa panel, mencatat suhu, mengukur arus, "
              "memotret nameplate, lalu menyusun berita acara. ") * 4
        r = run(write("t101.md", cl))
        rows += _want_status("selftest M-01 C-26 rantai klausa memicu INFO",
                             r, "C-26", "INFO")
        # 102 M-01 C-26 hijau: prosa kendur di bawah ambang -> PASS.
        r = run(write("t102.md", "Kami memeriksa panel distribusi utama pagi ini "
              "bersama petugas jaga malam. Hasilnya sesuai spesifikasi pabrikan yang "
              "berlaku saat ini. Tidak ada deviasi yang ditemukan di lokasi "
              "pemeriksaan hari ini. Berita acara hasil pemeriksaan kami tandatangani "
              "bersama di ruang operasi sebelum shift berakhir sore nanti. Dokumen "
              "arsip kami simpan di lemari besi lantai dua selama sepuluh tahun."))
        rows += _want_status("selftest M-01 C-26 prosa kendur PASS", r, "C-26", "PASS")
        # 103 M-02 C-27 merah: rata-rata di atas plafon 32 -> INFO.
        long_sent = ("Ketika beban puncak meningkat tajam pada kuartal ketiga maka "
                     "tim operasi wajib melakukan pengukuran ulang pada setiap panel "
                     "distribusi yang melayani zona produksi agar risiko gangguan "
                     "berantai dapat ditekan sedini mungkin sebelum berdampak luas. ") * 3
        r = run(write("t103.md", long_sent))
        rows += _want_status("selftest M-02 C-27 rata-rata tinggi memicu INFO",
                             r, "C-27", "INFO")
        # 104 M-10 C-28 merah: subjek alat pada verba keputusan -> INFO.
        ds = ("Scanner menetapkan batas ambang lalu menolak berkas yang tidak "
              "lengkap sebelum laporan diedarkan ke ruang arsip. ") * 4
        r = run(write("t104.md", ds))
        rows += _want_status("selftest M-10 C-28 subjek alat memicu INFO",
                             r, "C-28", "INFO")
        # 105 M-10 C-28 hijau: subjek manusia -> PASS.
        r = run(write("t105.md", "Kami menetapkan batas ambang sendiri setelah rapat "
              "internal pagi tadi. Tim kami memilih metode manual yang lebih murah "
              "biayanya. Kami menolak usulan otomasi penuh karena biaya perangkatnya "
              "belum sepadan. Keputusan ini berlaku untuk seluruh unit kerja mulai "
              "kuartal depan. Kami akan meninjau ulang angka anggarannya pada akhir "
              "tahun bersama bagian perencanaan."))
        rows += _want_status("selftest M-10 C-28 subjek manusia PASS", r, "C-28", "PASS")
        # 106 M-15 C-33 merah: dua varian rupiah sama-sama berpopulasi -> INFO.
        r = run(write("t106.md", "Anggaran tahap satu Rp 500.000 dan tahap dua "
              "Rp 750.000 dicairkan bertahap. Kontraktor mengajukan penyesuaian "
              "menjadi Rp500.000 flat lalu Rp625.000 untuk pekerjaan tambahan."))
        rows += _want_status("selftest M-15 C-33 varian rupiah campur memicu INFO",
                             r, "C-33", "INFO")
        # 107 M-15 C-33 hijau: satu varian konsisten -> PASS.
        r = run(write("t107.md", "Anggaran tahap satu Rp 500.000 dan tahap dua "
              "Rp 750.000 dicairkan bertahap sesuai kontrak induk yang sudah "
              "ditandatangani bersama di kantor pusat minggu lalu."))
        rows += _want_status("selftest M-15 C-33 varian konsisten PASS", r, "C-33", "PASS")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 56-59 NAT-GATE-R1 (30-09-2026): C-13 kode mesin tanpa label + C-14 gagasan
    #    ditulis ulang. Merah = artefak cacat wajib FAIL; hijau = bentuk sah wajib
    #    PASS, agar pelonggaran ambang panjang tidak meloloskan dua cacat asal.
    try:
        tmp2 = tempfile.mkdtemp(prefix="natr1_")

        def write2(name, body):
            p = os.path.join(tmp2, name)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(body)
            return p

        def run2(path, channel="doc"):
            return evaluate(scan_one(path, opts), channel, opts).rows

        # 56 merah C-13: tiga identifier internal tanpa penjelasan -> FAIL
        r = run2(write2("r56.md",
                        "Revisi selesai pada kartu t_91146669 dan kolom finished_at "
                        "sudah terisi. Status needs-review masih menempel pada berkas "
                        "induk sehingga agregasi D-TA-09 ikut terpicu saat pemeriksaan "
                        "berkala dijalankan ulang oleh petugas. Kami mencatat angka "
                        "revisi sebanyak 14 berkas dengan keterbatasan pada sampel "
                        "yang belum lengkap."))
        rows += _want_fail("kode mesin tanpa label memicu C-13 (NAT-GATE-R1)",
                           r, "C-13")

        # 57 hijau C-13: identifier yang sama, masing-masing berlabel penjelas
        r = run2(write2("r57.md",
                        "Revisi selesai pada kartu t_91146669 (laporan perbaikan "
                        "pemecah kalimat) dan kolom finished_at (waktu penyerahan "
                        "hasil) sudah terisi. Status needs-review (perlu ditinjau "
                        "pimpinan) masih menempel pada berkas induk sehingga aturan "
                        "agregasi indikator berat ikut terpicu saat pemeriksaan "
                        "berkala dijalankan ulang oleh petugas. Kami mencatat angka "
                        "revisi sebanyak 14 berkas dengan keterbatasan pada sampel "
                        "yang belum lengkap."))
        rows += _want_status("identifier berlabel bukan pelanggaran -> C-13 PASS",
                             r, "C-13", "PASS")

        # 58 merah C-14: gagasan yang sama ditulis ulang tiga kali -> FAIL
        r = run2(write2("r58.md",
                        "Gerbang naturalisasi memeriksa setiap dokumen sebelum "
                        "diserahkan kepada pembaca manusia. Gerbang naturalisasi "
                        "memeriksa setiap dokumen sebelum diserahkan kepada pembaca "
                        "manusia lebih dulu. Setiap dokumen diperiksa oleh gerbang "
                        "naturalisasi sebelum diserahkan kepada pembaca manusia. "
                        "Angka temuan 21 berkas dan batasan sampel ikut dicatat di "
                        "sini agar pembaca memahami cakupan kerja kami."))
        rows += _want_fail("gagasan ditulis ulang memicu C-14 (NAT-GATE-R1)",
                           r, "C-14")

        # 59 hijau C-14: tiga gagasan yang benar-benar terpisah (bukan parafrase)
        r = run2(write2("r59.md",
                        "Gerbang naturalisasi memeriksa setiap dokumen sebelum "
                        "diserahkan kepada pembaca manusia. Tim lapangan memasang "
                        "48 sensor thermal pada cincin deteksi terluar gudang timur. "
                        "Anggaran operasional triwulan berikutnya naik 12 persen "
                        "karena harga suku cadang impor, dan kami mengakui "
                        "keterbatasan ruang gudang pada pos penyimpanan tersebut."))
        rows += _want_status("tiga gagasan berbeda -> C-14 PASS", r, "C-14", "PASS")

        # 60-66 NAT-GATE-R2 (30-09): ekor kalimat, seksi terburuk, kerangka
        #    seragam, kepadatan rujukan, daftar istilah, suara penulis, manifest
        #    visual. Merah wajib menagih; hijau wajib tidak mengganggu.
        def rep(s, n):
            return " ".join([s] * n)

        # 60 merah C-15: satu kalimat raksasa >160 kata + 2 kalimat normal
        #    (3 kalimat agar tidak kena guard cuplikan pendek NAT-HIL-E2)
        r = run2(write2("r60.md",
                        rep("kerangka evaluasi ini membandingkan biaya operasional "
                            "listrik genset dan baterai pada beban puncak gudang "
                            "sebelum keputusan diambil oleh pimpinan proyek bersama "
                            "konsultan teknis yang ditunjuk resmi awal bulan lalu ",
                            7) + "\n\n" +
                        "Angka konsumsi 41 ribu kWh kami uraikan di bagian ini. "
                        "Batasan pencatatan meter tua kami akui secara terbuka."))
        rows += _want_fail("kalimat raksasa memicu C-15 (NAT-GATE-R2)", r, "C-15")

        # 61 hijau C-15: prosa bervariasi wajar
        r = run2(write2("r61.md",
                        "Kami meninjau 41 ribu kWh konsumsi triwulan ini. Beban "
                            "puncak terjadi pada Agustus, saat pendingin berjalan "
                            "tanpa henti sepanjang hari produksi. Genset cadangan "
                            "menyala empat kali dan biayanya tercatat rapi. "
                            "Kami mengakui batasannya: satu meter lama tidak "
                            "terkalibrasi sehingga angkanya kami buang."))
        rows += _want_status("prosa wajar -> C-15 PASS", r, "C-15", "PASS")

        # 62 merah C-17: 6 entri berkerangka identik -> share 100% INFO (pantauan)
        entri = "\n\n".join(
            "**T-%02d judul entri** Intinya: klaim ringkas nomor %d. Asalnya: studi "
            "lapangan tahun 2025. Untuk proyekmu: jalankan uji kecil sebelum skala."
            % (i, i) for i in range(1, 7))
        r = run2(write2("r62.md", entri + "\n"))
        rows.append(("PASS" if any(s == "INFO" and n.startswith("C-17") and
                                   "share >= 80" in d for s, n, d in r)
                     else "FAIL",
                     "selftest kerangka seragam dilaporkan INFO C-17 (NAT-GATE-R2)", ""))

        # 63 merah C-21: docx dengan kepala Gambar tanpa objek tertanam -> FAIL
        import docx as _docx
        buf = io.BytesIO()
        dd = _docx.Document()
        dd.add_paragraph("Gambar 3.1 arsitektur sistem pendingin gudang timur.")
        dd.add_paragraph("Tabel 3.1 daftar sensor terpasang lengkap hari ini.")
        dd.add_paragraph("Angka biaya 12,5 miliar dan risiko rantai pasok kami "
                         "catat pada lampiran resmi proyek berjalan.")
        dd.save(buf)
        p = os.path.join(tmp2, "r63.docx")
        open(p, "wb").write(buf.getvalue())
        r = run2(p, "etalase")
        rows += _want_fail("kepala Gambar tanpa objek memicu C-21 (NAT-GATE-R2)",
                           r, "C-21")

        # 64 hijau C-20: laporan institusional bersuara Kami -> INFO normal
        #    (>=40 kata agar tidak kena guard cuplikan pendek NAT-HIL-E2)
        r = run2(write2("r64.md",
                        "Kami menyampaikan hasil audit 14 gudang triwulan ketiga "
                        "kepada pimpinan sebagai bahan keputusan rapat besok pagi. "
                        "Kami rekomendasikan peremajaan pada 4 unit lebih dulu "
                        "karena biaya listriknya tertinggi di antara semua lokasi. "
                        "Kami sampaikan secara jujur bahwa dua gudang belum "
                        "terpasang meter baru, sehingga angkanya masih estimasi "
                        "internal kami dan belum bisa dibandingkan antar wilayah."))
        rows.append(("PASS" if any(s == "INFO" and n.startswith("C-20") and
                                   "TANPA sapaan" not in d for s, n, d in r)
                     else "FAIL",
                     "selftest suara Kami tidak divonis hilang -> C-20 INFO bersih", ""))

        # 65 merah C-20: pola LAPORAN-ADINT (Kami=0, penulis>=2) -> INFO TANPA
        r = run2(write2("r65.md",
                        "Hasil ekstraksi dihitung ulang oleh penulis bagian ini "
                        "dengan algoritma yang sama. Menurut penulis angka itu sah. "
                        "Oleh penulis, tabel disusun per genre agar mudah dicek. "
                        "Tidak ada angka spesifik lain dan batasan pun tidak "
                        "diakui di bagian ini sehingga pembaca menelan mentah."))
        rows.append(("PASS" if any(s == "INFO" and n.startswith("C-20") and
                                   "TANPA sapaan" in d for s, n, d in r)
                     else "FAIL",
                     "selftest tanpa-Kami dengan 'penulis' dilaporkan INFO C-20", ""))

        # 66 merah C-19: berkas berprosa tanpa glosarium -> INFO pantauan
        #    (PUTUSAN USER 30-09: ambang panjang 6.000 kata DICABUT)
        para = ("Tim survei mencatat kondisi lapangan pada titik penyimpanan "
                "barat dan melaporkan selisih suhu ke pos kendali setiap enam jam "
                "sampai perbaikan selesai dikerjakan kontraktor setempat. ")
        r = run2(write2("r66.md", para * 5))
        rows.append(("PASS" if any(s == "INFO" and n.startswith("C-19") and
                                   "tidak ada bagian" in d for s, n, d in r)
                     else "FAIL",
                     "selftest berkas tanpa glosarium -> INFO C-19", ""))

        # 67-70 NAT-GATE-R3 (30-09 putaran user ketiga): lengkung narasi.
        def mk_bab(specs):
            # specs: list of (title, body)
            return "\n\n".join("## %s\n\n%s" % (ti, bd) for ti, bd in specs)

        nar_body = ("Banyak orang mengira hasil ini datang dari keberuntungan "
                    "semata. Ternyata data lapangan membalik dugaan itu: yang "
                    "menentukan justru kedisiplinan pencatatan selama dua tahun. "
                    "Dari temuan sebelumnya kita berangkat ke pengukuran kedua, "
                    "dan pertanyaan yang tersisa akan dijawab pada bab berikutnya.")
        plain_body = ("Daftar kondisi lapangan dicatat lengkap. Suhu tercatat "
                      "dua puluh delapan derajat. Kelembapan tercatat enam puluh "
                      "persen. Arus tercatat empat belas ampere. Tegangan tercatat "
                      "tiga ratus delapan puluh volt. Semua angka masuk lembar.")
        # 67 hijau R3: dokumen berlengkung lengkap (pendahuluan -> ... -> kesimpulan,
        #    sambungan antar bab, momen pembalik di badan)
        r = run2(write2("r67.md", mk_bab([
            ("BAB 1 PENDAHULUAN", plain_body + " " + nar_body),
            ("BAB 2 KONDISI LAPANGAN", nar_body + " " + plain_body),
            ("BAB 3 PENGUKURAN", plain_body + " " + nar_body),
            ("BAB 4 ANALISIS", nar_body),
            ("BAB 5 TEMUAN LANJUTAN", plain_body + " " + nar_body),
            ("BAB 6 VERIFIKASI", nar_body + " " + plain_body),
            ("BAB 7 REKOMENDASI", plain_body),
            ("BAB 8 KESIMPULAN", nar_body)])))
        rows += _want_status("dokumen berlengkung -> C-24 PASS", r, "C-24", "PASS")

        # 68 merah C-24: 8 bab katalog tanpa satu pun momen pembalik -> FAIL
        r = run2(write2("r68.md", mk_bab([
            ("BAB %d DATA" % i, plain_body + " " + plain_body)
            for i in range(1, 9)])))
        rows += _want_fail("tanpa momen pembalik memicu C-24 (NAT-GATE-R3)",
                           r, "C-24")

        # 69 INFO C-22: bab tanpa penanda latar/tujuan -> lengkung tidak lengkap
        r = run2(write2("r69.md", mk_bab([
            ("BAB 1 OPERANDI", plain_body),
            ("BAB 2 OPERASI", plain_body),
            ("BAB 3 PEMELIHARAAN", plain_body),
            ("BAB 4 ANGGARAN", plain_body)])))
        rows.append(("PASS" if any(s == "INFO" and n.startswith("C-22") and
                                   "TIDAK ADA" in d for s, n, d in r)
                     else "FAIL",
                     "selftest tanpa ujung lengkung -> INFO C-22", ""))

        # 70 INFO C-25: bab isinya tabel semua (katalog murni) -> dilaporkan
        #    (perlu >=200 kata agar layak dinilai: 80 baris tabel ~240 kata)
        tab = "\n".join("| %d | angka %d |" % (i, i) for i in range(1, 81))
        prose_min = "Catatan singkat atas tabel di atas ada pada baris sumber."
        r = run2(write2("r70.md", mk_bab([
            ("BAB 1 PENDAHULUAN", prose_min),
            ("BAB 2 REGISTER A", tab + "\n\n" + prose_min),
            ("BAB 3 REGISTER B", tab + "\n\n" + prose_min),
            ("BAB 4 REGISTER C", tab + "\n\n" + prose_min),
            ("BAB 5 KESIMPULAN", prose_min)])))
        rows.append(("PASS" if any(s == "INFO" and n.startswith("C-25") and
                                   "di bawah 30%" in d for s, n, d in r)
                     else "FAIL",
                     "selftest bab katalog -> INFO C-25", ""))

        # === K7 kanal kitab (PUTUSAN t_77fd88c3, 30-09-2026) ================
        # Fixture KA: gaya kitab remaja (ASL rendah, paragraf pendek, tebal
        # penanda istilah, panah ASCII, identifier API, komentar HTML baris 1
        # provenansi). Kanal kitab harus PASS penuh; kanal doc harus tetap
        # menjatuhkan vonis lama (C-6/C-7/C-13) sebagai kontrol regresi.
        ka = ("<!-- kartu t_866b868b | RAFIF-POLISH-0930 | basis pin "
              "8439358fbb7b baris 1136 -->\n\n"
              "### BAB 1 - ANGKA ACAK\n\n"
              "**Bilangan acak** muncul di banyak permainan. Fungsi "
              "random_number_generation memakainya tiap kali. Pemain menekan "
              "tombol lalu hasil muncul.\n\n"
              "Gunakan from_angle untuk arah awal sesuai panah tujuan: panas -> "
              "bergerak -> dingin. Catatan singkat yg dibuat dgn tergesa.\n\n"
              "Fungsi look_at mengarahkan kamera. Mata pembaca ikut arah itu. "
              "Batasan materinya ada di halaman depan. Angka 5 contoh sudah "
              "cukup jelas.\n\n"
              "Latihan singkat ada di akhir bab. Kerjakan satu per satu "
              "dengan tenang.\n")
        # Fixture KB: melanggar plafon P1a (rata-rata > 20 kata/kalimat) dan
        # memuat satu kalimat raksasa > 160 kata agar C-15/B13 ikut terpicu.
        kb_ribuan = ("Pada pagi itu ibu membeli ikan segar di pasar yang ramai "
                     "sambil memeluk keranjang bambu cokelat dan ayah memeriksa "
                     "ban sepeda tua di halaman depan sementara kakak menyusun "
                     "tumpukan buku pelajaran di meja belajarnya dan adik kecil "
                     "mengejar ayam yang berlari keliling pekarangan dengan "
                     "tertawa keras sedangkan nenek duduk di kursi rotan mengupas "
                     "jagung kuning untuk stok makan siang dan koki di dapur "
                     "belakang mengaduk sayur santan yang mengepul harum sementara "
                     "paman menambal jaring ikan di bawah pohon mangga dan bibi "
                     "menjemur kain batik di tali rafia antara dua tiang bambu dan "
                     "beberapa tetangga mampir meminjam tangga kayu sambil "
                     "bercerita tentang panen padi musim kemarin yang melimpah "
                     "meski hujan sering turun tanpa henti sepanjang minggu "
                     "terakhir masa tanam sehingga semua orang di keluarga besar "
                     "kami sibuk menyiapkan keperluan hari raya dengan gembira "
                     "tanpa mengeluh sedikit pun meskipun biaya persiapan tahun "
                     "ini terasa lebih berat daripada tahun sebelumnya karena "
                     "harga bahan pokok naik cukup tajam di pasar induk kota "
                     "beserta desa-desa tetangga yang dilalui jalur distribusi "
                     "barang kebutuhan harian warga.")
        kb = ("### BAB 1 - PLAFON\n\n"
              "Paragraf ini disusun dengan kalimat yang sangat panjang karena "
              "memang demikian cara menguji bahwa plafon dua puluh kata per "
              "kalimat benar-benar menagih penulis yang mengulur kalimat tanpa "
              "perlu dan tanpa jeda yang cukup bagi pembaca muda. Kalimat "
              "kedua juga panjang dengan cara yang sama supaya rata-rata "
              "seluruh dokumen melewati batas plafon yang sudah ditetapkan "
              "oleh keputusan misi yang terkunci rapat. Kalimat ketiga menutup "
              "dengan rincian panjang yang serupa agar rata-rata terukur jelas "
              "di atas dua puluh kata per kalimat dengan margin yang aman. "
              + kb_ribuan + " "
              "Batasan contoh ini hanya alat uji dan angka 3 kalimat sengaja "
              "dibuat panjang.\n")
        r_ka_doc = run2(write2("ka-doc.md", ka))
        r_ka = run2(write2("ka-kitab.md", ka), channel="kitab")
        r_kb = run2(write2("kb-kitab.md", kb), channel="kitab")
        r_kb_doc = run2(write2("kb-doc.md", kb))

        # 71 registrasi kanal: kitab dikenal + alias k7 + bukan kanal pendek
        rows.append(("PASS" if ("kitab" in CHANNELS
                                and CHANNEL_ALIASES.get("k7") == "kitab"
                                and "kitab" not in SHORT_CHANNELS)
                     else "FAIL",
                     "selftest kanal kitab terdaftar (K7, alias k7, non-pendek)",
                     "" if "kitab" in CHANNELS else "CHANNELS tanpa 'kitab'"))

        # 72-77 vonis kelas konflik runtuh pada kanal kitab. Ambang peruntuhan
        # sengaja dilanggar fixture: C-7 (2 paragraf <3 kalimat), C-8 (tebal
        # >6/1000), C-12 (panah + singkatan chat), C-13 (3 identifier keras),
        # C-15 (kalimat raksasa di r_kb).
        rows += _want_status("kitab ASL rendah -> C-6 PASS (plafon)", r_ka, "C-6", "PASS")
        rows += _want_status("kitab -> C-7 vonis runtuh INFO", r_ka, "C-7", "INFO")
        rows += _want_status("kitab -> C-8 vonis runtuh INFO", r_ka, "C-8", "INFO")
        rows += _want_status("kitab -> C-12 vonis runtuh INFO", r_ka, "C-12", "INFO")
        rows += _want_status("kitab -> C-13 vonis runtuh INFO", r_ka, "C-13", "INFO")
        rows += _want_status("kitab -> C-15 vonis runtuh INFO", r_kb, "C-15", "INFO")
        rows += _want_status("kitab seksi kecil -> C-16 N/A", r_ka, "C-16", "N/A")

        # 78 komentar HTML provenansi tidak dihitung identifier keras di kitab
        c13_rows = [(s, d) for s, n, d in r_ka if n.startswith("C-13")]
        ok78 = bool(c13_rows) and all(
            "t_866b868b" not in d and "8439358fbb7b" not in d and "id kartu" not in d
            for s, d in c13_rows)
        rows.append(("PASS" if ok78 else "FAIL",
                     "selftest komentar HTML provenansi bukan identifier keras (kitab)",
                     "" if ok78 else "detail C-13 masih memuat id kartu/hash: "
                     + (c13_rows[0][1][:120] if c13_rows else "-")))

        # 79 setiap peruntuhan menyebut 'kanal kitab' secara eksplisit
        dem_names = ("C-7", "C-8 ", "C-12", "C-13", "C-15")
        missing = [nm for nm in dem_names
                   if not any(n.startswith(nm) and s == "INFO" and "kanal kitab" in d
                              for s, n, d in (r_ka + r_kb))]
        rows.append(("PASS" if not missing else "FAIL",
                     "selftest peruntuhan INFO menyebut alasan 'kanal kitab'",
                     "" if not missing else "tanpa alasan eksplisit: " + ",".join(missing)))

        # 80 agregat kitab: D-TA-09 PASS dan VERDICT tanpa FAIL
        rows += _want_status("kitab -> D-TA-09 PASS", r_ka, "D-TA-09", "PASS")
        rows += _want_no_fail("kitab naskah patuh-plafon -> tanpa FAIL", r_ka)

        # 81 kontrol regresi kanal doc: vonis lama pada fixture yang sama utuh
        rows += _want_fail("doc ASL rendah tetap FAIL C-6 (lantai 18 utuh)",
                           r_ka_doc, "C-6")
        rows += _want_fail("doc paragraf pendek tetap FAIL C-7", r_ka_doc, "C-7")
        rows += _want_fail("doc identifier keras tetap FAIL C-13", r_ka_doc, "C-13")

        # 82 balik arah plafon: > 20 kata/kalimat FAIL di kitab, PASS di doc
        rows += _want_fail("kitab ASL > plafon 20 -> C-6 FAIL", r_kb, "C-6")
        rows += _want_status("doc ASL tinggi tetap PASS C-6 (tak berubah)",
                             r_kb_doc, "C-6", "PASS")

        # === K8 kanal standar (PUTUSAN t_eec55819, kartu t_334c0a44) ========
        # Fixture HIJAU ST-A: naskah standar minimal - dua aturan berbadan enam
        # bidang S-2 (tebal kepala 12x), aparatus navigasi pendek 2 dari 11
        # paragraf (18,2% <= 20%), satu tebal emfatis residu (1,6/1000w).
        # Kanal standar harus PASS penuh; kanal doc pada berkas yang sama tetap
        # vonis lama (kontrol regresi). Parser menggabungkan baris prosa tanpa
        # pemisah - aparatus dipisah lewat heading/tabel, meniru manual asli.
        _st_r1 = ("**Pernyataan.** Aturan A-01 mengikat seluruh naskah normatif rumah "
                  "yang diterbitkan fleet beserta turunannya tanpa kecuali sejak "
                  "tanggal promosi. Turunan langsung ikut terikat pada hari yang "
                  "sama. **Fungsi bagi pembaca.** Pembaca menemukan batas mutu "
                  "register yang diuji sebelum naskah terbit tanpa perlu menebak "
                  "dari gaya isi dokumen. Batas mutu itu tercetak lengkap pada "
                  "register kanal. **Bukti manusia.** Contoh sah diambil dari arsip "
                  "proyek tahun 2026 sebanyak lima berkas. Pustakawan memverifikasi "
                  "silang kelimanya sebelum dipromosikan. **Kontras fleet.** "
                  "Cuplikan cacat lama dikutip verbatim sebagai pembanding resmi. "
                  "Kutipan itu menjadi peringatan awal bagi penyusun baru. "
                  "**Instrumen penegak.** Scanner gerbang menjalankan seluruh check "
                  "terdaftar pada register kanal rumah. Cetakan hijau menjadi syarat "
                  "promosi naskah. **Predikat verifikasi.** Lulus berarti semua "
                  "gerbang hijau pada cetakan resmi. Gagal berarti satu saja memerah "
                  "dan naskah dikembalikan utuh.")
        _st_r2 = ("**Pernyataan.** Aturan A-02 mengatur tata cara penomoran referensi "
                  "silang di dalam badan naskah agar rujukan antarbagian tetap "
                  "tertelusur pembaca. Nomor rujukan wajib bertemu pasangan resminya "
                  "saat audit. **Fungsi bagi pembaca.** Pembaca mengikuti alur argumen "
                  "tanpa tersesat di antara lampiran dan catatan kaki. Alur itu dijaga "
                  "oleh penanda bernomor konsisten. **Bukti manusia.** Sepuluh naskah "
                  "tahun 2025 diperiksa manual dan sembilan patuh pada konvensi ini. "
                  "**Kontras fleet.** Naskah lama memakai penanda bebas yang terbukti "
                  "membingungkan saat audit susulan berlangsung. **Instrumen penegak.** "
                  "Gerbang promosi menolak naskah dengan penomoran menggantung lebih "
                  "dari satu butir. **Predikat verifikasi.** Lulus bila seluruh "
                  "rujukan internal bertemu pasangan resminya pada register.")
        _st_tab = ("| ID | Lapis | Ringkas |\n"
                   "|----|-------|---------|\n"
                   "| A-01 | L1 | Register inti |\n"
                   "| A-02 | L1 | Register turunan |\n")
        st_a = ("# STD-UJI-K8\n\n"
                "Tim kelistrikan kami menyelesaikan pemeriksaan panel distribusi utama "
                "pada minggu kedua Maret 2026 setelah menerima surat tugas resmi dari "
                "bagian perencanaan dua hari sebelumnya. Sebanyak 12 feeder diukur arus "
                "beban puncaknya dan hasilnya dicocokkan dengan catatan pemeliharaan "
                "tahunan yang disimpan di lemari arsip lantai dua gedung operasional. "
                "Keterbatasan pengukuran ini adalah hanya 4 dari 12 feeder yang "
                "terpantau terus menerus selama jendela pemeliharaan berlangsung "
                "sehingga sisanya kami periksa secara berkala.\n\n"
                "## Bagian A - Register\n\n"
                "Bagian register memuat aturan bertingkat dengan badan enam bidang "
                "wajib untuk setiap aturan yang terdaftar pada naskah ini. Enam bidang "
                "tersebut ditulis seragam agar pembaca memindai cepat tanpa kehilangan "
                "konteks normatif masing-masing aturan. Struktur seragam inilah yang "
                "melahirkan tebal kepala bidang pada setiap aturan dan menjadi sasaran "
                "pengecualian kanal standar.\n\n"
                + _st_tab + "\n"
                "Indeks aturan memuat 4 butir aktif beserta seluruh turunannya.\n\n"
                "### Aturan A-01\n\n" + _st_r1 + "\n\n"
                + _st_tab + "\n"
                "Catatan cakupan: uji instrumen ini terbatas dua delta perilaku saja.\n\n"
                "### Aturan A-02\n\n" + _st_r2 + "\n\n"
                "## Bagian B - Penegakan\n\n"
                "Penegakan berjalan lewat gerbang penerbitan yang menolak naskah cacat "
                "sebelum promosi fleet dan hasil sapuan dibukukan bersama cetakan "
                "instrumen sebagai jejak audit resmi. Register kanal mencatat **K8** "
                "sebagai kanal baru pada dokumen uji ini beserta alias resminya. "
                "Verifikasi akhir menempel pada cetakan hijau dua kali jalan "
                "deterministik supaya audit susulan merekonstruksi vonis tanpa "
                "menebak-nebak.\n\n"
                "### Residu\n\n"
                "Residu emfatis dijaga rendah dengan menandai hanya istilah penting "
                "memakai tebal sementara sisanya ditulis polos mengikuti gaya prosa "
                "register panjang rumah. Ambang residu enam per seribu kata menjadi "
                "penahan utama jalur ini agar kelonggaran tidak berubah menjadi "
                "karpet. Perluasan kosakata label hanya sah lewat jalur M-6 yang "
                "tercatat dan dokumen bervocab lain dilarang memakai penanda mandiri "
                "di dalam badan naskahnya.\n\n"
                "### Bukti cetakan\n\n"
                "Sapuan ulang atas objek hidup akan dibukukan sebagai dasar koreksi "
                "rekaman vonis lepas pada lembar kendali misi gaya ahli. Setiap "
                "cetakan instrumen menyimpan nomor check, status, dan detail angka "
                "sehingga pembaca audit tidak bergantung pada ingatan pekerja. "
                "Rekaman semacam itu menjadi milik bersama fleet dan ikut diperiksa "
                "oleh verifier independen pada giliran verifikasi.\n\n"
                "### Eligibilitas\n\n"
                "Dokumen sejenis yang belum menegakkan standar lain tetap masuk kanal "
                "dokumen biasa karena eligibilitas kanal standar dipegang controller "
                "sebelum sapuan berlangsung. Norma itu mencegah pintu darurat universal "
                "sekaligus menjaga cetakan pertama menyebut kanal terpilih secara "
                "terbuka bagi auditor. Pelanggaran eligibilitas dicatat sebagai temuan "
                "audit, bukan kegagalan scanner di lapangan.\n\n"
                "### Rantai putusan\n\n"
                "Rekan pustaka menautkan setiap keputusan perluasan kosakata ke kartu "
                "putusan induknya supaya rantai asal-usul tetap utuh dibaca lintas "
                "generasi agen. Penambahan label bidang baru tanpa kartu induk dianggap "
                "percobaan celah swa-deklarasi dan dikembalikan utuh ke pengusulnya "
                "untuk ditimbang ulang. Kebijakan itu sudah berjalan sejak register "
                "kanal pertama dibuka.\n")
        r_st_a = run2(write2("st-a.md", st_a), channel="standar")
        r_st_a_doc = run2(write2("st-a-doc.md", st_a))
        # 83 registrasi kanal: standar dikenal + alias k8/normatif + non-pendek
        rows.append(("PASS" if ("standar" in CHANNELS
                                and CHANNEL_ALIASES.get("k8") == "standar"
                                and CHANNEL_ALIASES.get("normatif") == "standar"
                                and "standar" not in SHORT_CHANNELS)
                     else "FAIL",
                     "selftest kanal standar terdaftar (K8, alias k8/normatif, non-pendek)",
                     "" if "standar" in CHANNELS else "CHANNELS tanpa 'standar'"))
        # 84 fixture HIJAU: kanal standar PASS penuh tanpa FAIL
        rows += _want_status("standar naskah minimal -> C-7 PASS (rasio)",
                             r_st_a, "C-7", "PASS")
        rows += _want_status("standar naskah minimal -> C-8 PASS (residu)",
                             r_st_a, "C-8", "PASS")
        rows += _want_status("standar -> D-TA-09 PASS", r_st_a, "D-TA-09", "PASS")
        rows += _want_no_fail("standar naskah patuh -> tanpa FAIL", r_st_a)
        # 85 nama check mencetak penanda kanal eksplisit (di NAMA, bukan detail)
        rows.append(("PASS" if any(n.startswith("C-7")
                                   and "(kanal standar: aparatus navigasi)" in n
                                   for s, n, d in r_st_a) else "FAIL",
                     "selftest nama C-7 kanal standar memuat '(kanal standar: aparatus navigasi)'",
                     ""))
        rows.append(("PASS" if any(n.startswith("C-8 ") or (n.startswith("C-8") and not n.startswith("C-8b"))
                                   for s, n, d in r_st_a
                                   if "kanal standar" in n) else "FAIL",
                     "selftest nama C-8 kanal standar menyebut pengecualian kepala bidang",
                     ""))
        # 86 detail C-8 mencetak jumlah dikecualikan (vocab tertutup S-2)
        rows.append(("PASS" if any(n.startswith("C-8") and "dikecualikan" in d
                                   and "vocab tertutup S-2" in d
                                   for s, n, d in r_st_a) else "FAIL",
                     "selftest detail C-8 standar mencetak jumlah kepala bidang dikecualikan",
                     ""))
        # 87 kontrol regresi doc: berkas sama di kanal doc vonis lama utuh
        #    (13 tebal / 20,5 per 1000 kata -> FAIL B6; 2 paragraf pendek > 1 -> FAIL B2)
        rows += _want_fail("doc berkas sama tetap FAIL C-7 (ambang absolut utuh)",
                           r_st_a_doc, "C-7")
        rows += _want_fail("doc berkas sama tetap FAIL C-8 (label tetap dihitung)",
                           r_st_a_doc, "C-8")
        # 88 merah (a): frasa hitam A4 di prosa TETAP FAIL di kanal standar
        st_b = st_a.replace(
            "Penegakan berjalan lewat gerbang penerbitan yang menolak naskah cacat ",
            "Penegakan berjalan lewat gerbang penerbitan yang hope this helps "
            "menolak naskah cacat ")
        r_st_b = run2(write2("st-b.md", st_b), channel="standar")
        rows += _want_fail("standar frasa hitam A4 -> tetap FAIL (kanal bukan penyembunyi)",
                           r_st_b, "A4")
        # 89 merah (b): tebal emfatis non-label > 6/1000 kata -> FAIL B6
        st_c = st_a + ("\n### Uji residu\n\n"
                       + " ".join("**residu%d**" % i for i in range(1, 31))
                       + " Daftar residu emfatis ini sengaja melewati ambang enam per "
                       "seribu kata agar jalur FAIL B6 terbukti hidup pada kanal "
                       "standar dan tidak jadi karpet pelonggaran.\n")
        r_st_c = run2(write2("st-c.md", st_c), channel="standar")
        rows += _want_fail("standar residu emfatis > ambang -> FAIL C-8", r_st_c, "C-8")
        # 90 merah (c): paragraf pendek > 20% total -> FAIL B2
        st_d = st_a + "".join("\n### Catatan %d\n\nCatatan pendek %d.\n\n" % (i, i)
                              for i in range(1, 9))
        r_st_d = run2(write2("st-d.md", st_d), channel="standar")
        rows += _want_fail("standar paragraf pendek > 20% -> FAIL C-7", r_st_d, "C-7")
        # 91 C-6 tidak tersentuh: plafon hanya milik kitab; standar mewarisi
        #    floor doc >= 18 (fixture ASL rendah kitab FAIL C-6 juga di standar)
        r_st_ka = run2(write2("ka-std.md", ka), channel="standar")
        rows += _want_fail("standar ASL rendah -> C-6 floor doc utuh (tanpa plafon)",
                           r_st_ka, "C-6")
        # 92 tidak ada demosi ala kitab: C-12/C-13 vonis penuh di kanal standar
        #    (fixture ka memicu keduanya; di kitab runtuh INFO, di standar FAIL)
        rows += _want_fail("standar -> C-13 identifier keras tetap FAIL (tanpa demosi)",
                           r_st_ka, "C-13")
        rows += _want_fail("standar -> C-12 gaya catatan tetap FAIL (tanpa demosi)",
                           r_st_ka, "C-12")
        # 93 konstanta vocab tertutup tepat enam label S-2
        rows.append(("PASS" if len(STANDAR_FIELD_LABELS) == 6 and
                     "Pernyataan" in STANDAR_FIELD_LABELS and
                     "Predikat verifikasi" in STANDAR_FIELD_LABELS
                     else "FAIL",
                     "selftest STANDAR_FIELD_LABELS = enam label S-2 tertutup",
                     ""))

        # 88-89 NAT-GATE-R4 (05-10-2026): lapisan CSS/JS bukan prosa (temuan kalibrasi
        #     artefak rekap - vonis palsu C-6 15,7 dari prosa asli 26 kata/kalimat)
        html_uji = ("<!DOCTYPE html><html><head><style>\n"
                    "body { font-family: Segoe UI; margin: 0; padding: 0; background: #F0F0F0; }\n"
                    "h1 { color: #1a1a2e; font-size: 32px; letter-spacing: 1px; }\n"
                    "p { line-height: 1.6; }\n"
                    "</style></head><body>\n"
                    "<h1>Standar Naturalisasi dan Dokumen Fleet</h1>\n"
                    "<p>Dokumen ini kami susun sebagai bahan tinjauan bersama yang "
                    "rapi dan mudah dibaca oleh semua pihak yang berkepentingan pada "
                    "fleet. Setiap bagian membawa angka terukur dari pengujian nyata "
                    "yang dikerjakan hari ini juga. Kami menyadari sepenuhnya adanya "
                    "keterbatasan sampel pada beberapa deteksi yang masih berstatus "
                    "pantauan kalibrasi sebelum menagih vonis. Karena itu kami "
                    "menyusun kalimat panjang yang wajar agar metrik panjang dapat "
                    "dinilai dengan benar oleh scanner.</p>"
                    "</body></html>")
        r = run2(write2("r88.html", html_uji))
        rows += _want_status("isi style tidak dihitung kalimat -> C-6 PASS",
                             r, "C-6", "PASS")
        # 89 merah kendali: tanpa pembuangan, blok CSS panjang saja tetap bukan
        #    prosa - dokumen HANYA CSS tidak menghasilkan vonis panjang senyap
        html_kosong = ("<html><head><style>" +
                       "body { margin: 0; } " * 30 +
                       "</style></head><body></body></html>")
        r = run2(write2("r89.html", html_kosong))
        rows.append(("PASS" if any(n.startswith("C-6") and s in ("N/A", "PASS")
                                   for s, n, d in r) else "FAIL",
                     "selftest html hanya-CSS -> C-6 tidak menagih", ""))

        # 94-98 PUTUSAN-HEUR-1009 butir 3 (kartu t_d9d918a6): pengecualian
        #     tipografis run monospace docx untuk C-13 + perbaikan aditif
        #     glosarium-heading-docx (temuan pendamping putusan).
        try:
            import docx as _docx_st

            def docx_mk(items):
                """items = daftar (teks, font_atau_None, gaya_atau_None)."""
                dd = _docx_st.Document()
                for txt, fnt, sty in items:
                    pp = dd.add_paragraph(txt)
                    if fnt:
                        for rr in pp.runs:
                            rr.font.name = fnt
                    if sty:
                        pp.style = dd.styles[sty]
                buf2 = io.BytesIO()
                dd.save(buf2)
                return buf2.getvalue()

            def writeb(name, payload):
                p = os.path.join(tmp2, name)
                with open(p, "wb") as fh:
                    fh.write(payload)
                return p

            c13p = ("Revisi selesai pada kartu t_91146669 dan kolom finished_at "
                    "sudah terisi. Status needs-review masih menempel pada berkas "
                    "induk sehingga agregasi D-TA-09 ikut terpicu saat pemeriksaan "
                    "berkala dijalankan ulang oleh petugas. Kami mencatat angka "
                    "revisi sebanyak 14 berkas dengan keterbatasan pada sampel "
                    "yang belum lengkap.")
            # 94 merah: tiga identifier keras dalam prosa non-monospace -> FAIL
            r = run(writeb("r94.docx", docx_mk([(c13p, None, None)])))
            rows += _want_fail("docx identifier keras prosa biasa FAIL C-13",
                               r, "C-13")
            # 95 hijau: identifier yang sama seluruhnya dalam run monospace ->
            #    vonis utama bukan FAIL + baris INFO visibilitas tercetak
            r = run(writeb("r95.docx", docx_mk([(c13p, "IBM Plex Mono", None)])))
            c13m = sorted(set(s for s, n, d in r if n.startswith("C-13 kode mesin")))
            rows.append(("PASS" if c13m and "FAIL" not in c13m else "FAIL",
                         "selftest docx identifier dalam run monospace bukan FAIL",
                         "status aktual: " + "/".join(c13m)))
            rows.append(("PASS" if any(n.startswith("C-13 identifier monospace")
                                       and s == "INFO" for s, n, d in r) else "FAIL",
                         "selftest INFO 'identifier monospace dikecualikan' tercetak",
                         ""))
            # 96 merah campuran: paragraf serif mendampingi paragraf mono ->
            #    ambang tiga tetap jatuh pada lapisan serif
            r = run(writeb("r96.docx", docx_mk([(c13p, "IBM Plex Mono", None),
                                               (c13p, None, None)])))
            rows += _want_fail("docx campuran mono+serif: serif tetap FAIL C-13",
                               r, "C-13")
            # 97 hijau glosarium-docx: heading gaya 'Heading 1' membuka blok ->
            #    kode terdaftar dikecualikan -> C-13 PASS (temuan pendamping)
            gl_body = ("Register memuat baris build_std dan gate_check beserta "
                       "evidence_source tanpa penjelasan tambahan di badan naskah "
                       "sehingga pembaca awam kebingungan mengikuti alur laporan "
                       "yang disusun ulang tiga kali pekan ini oleh petugas jaga.")
            gl_items = [(gl_body, None, None),
                        ("DAFTAR SINGKATAN", None, "Heading 1"),
                        ("build_std adalah fungsi pembangun standar.", None, None),
                        ("gate_check adalah gerbang pemeriksaan akhir.", None, None),
                        ("evidence_source adalah kolom sumber bukti.", None, None)]
            r = run(writeb("r97.docx", docx_mk(gl_items)))
            rows += _want_status("docx glosarium gaya-heading mengecualikan kode "
                                 "-> C-13 PASS", r, "C-13", "PASS")
            # 98 merah kontrol: teks glosarium TANPA gaya heading tidak membuka
            #    blok -> C-13 tetap FAIL (tanpa lolos senyap)
            r = run(writeb("r98.docx", docx_mk([(t, f, None) for t, f, _ in gl_items])))
            rows += _want_fail("docx teks glosarium tanpa gaya heading tetap FAIL",
                               r, "C-13")
        except ImportError:
            rows.append(("N/A", "selftest docx monospace/glosarium dilewati",
                         "python-docx tidak tersedia"))
    finally:
        shutil.rmtree(tmp2, ignore_errors=True)

    lines, fails = render(rows)
    return lines, fails


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def collect_inputs(paths, self_exclude=True):
    """Kumpulkan berkas. Pengecualian-diri HANYA berlaku untuk hasil jalan-jalan
    direktori: berkas yang disebut operator secara eksplisit selalu dipindai
    (sapuan diri = kontrol bahwa gerbang tidak mati)."""
    explicit = []
    walked = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs.sort()
                for n in sorted(names):
                    walked.append(os.path.join(root, n))
        elif os.path.exists(p):
            explicit.append(p)
    files = explicit
    if self_exclude:
        here = os.path.abspath(__file__)
        files += [f for f in walked if os.path.abspath(f) != here]
    else:
        files += walked
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="scan_ai_footprint.py",
        description="Scanner deterministik jejak AI (A1-A7 / B1-B9 / C-1..C-10) untuk "
                    "gerbang naturalisasi keluaran GSP.")
    ap.add_argument("inputs", nargs="*", help="berkas atau direktori yang dipindai")
    ap.add_argument("--text", action="append", default=[],
                    help="cuplikan teks langsung (boleh lebih dari satu)")
    ap.add_argument("--channel", default="doc",
                    help="kanal: " + "|".join(sorted(CHANNELS)) + " (alias k1..k8 diterima)")
    ap.add_argument("--selftest", action="store_true",
                    help="jalankan uji mandiri bawaan (exit 0 wajib)")
    ap.add_argument("--scan-code", action="store_true",
                    help="ikutkan lapisan kode/komentar sebagai prosa (default: dikecualikan"
                         " per RT 3.2; literal dan escape tetap dihitung)")
    ap.add_argument("--require-marker", action="store_true",
                    help="jadikan C-10 wajib FAIL bila marker naturalisasi absen")
    ap.add_argument("--no-self-exclude", action="store_true",
                    help="jangan kecualikan berkas scanner sendiri dari sapuan direktori")
    ap.add_argument("--list-checks", action="store_true",
                    help="daftar kanal yang dikenal lalu keluar")
    ap.add_argument("--version", action="store_true", help="tampilkan versi skrip")
    opts = ap.parse_args(argv)

    if opts.version:
        sys.stdout.write("scan_ai_footprint.py %s\n" % __version__)
        return 0

    if opts.list_checks:
        for ch in sorted(CHANNELS):
            sys.stdout.write("%s: %s\n" % (ch, CHANNELS[ch]))
        return 0

    if opts.selftest:
        lines, fails = selftest(opts)
        sys.stdout.write("\n".join(lines) + "\n")
        return 0 if fails == 0 else 1

    channel = CHANNEL_ALIASES.get(opts.channel.lower(), opts.channel.lower())
    if channel not in CHANNELS:
        sys.stdout.write("CHECK 1: FAIL - kanal tidak dikenal '%s' (pilihan: %s)\n"
                         % (opts.channel, "|".join(sorted(CHANNELS))))
        sys.stdout.write("VERDICT: FAIL\n")
        return 1

    files = collect_inputs(opts.inputs, self_exclude=not opts.no_self_exclude)
    if not files and not opts.text:
        sys.stdout.write("CHECK 1: FAIL - tidak ada masukan terbaca (berkas/teks kosong)\n")
        sys.stdout.write("VERDICT: FAIL\n")
        return 1

    all_rows = []
    for p in files:
        try:
            doc = scan_one(p, opts)
        except Exception as exc:
            all_rows.append(("FAIL", "baca berkas %s" % os.path.basename(p),
                             "%s: %s" % (type(exc).__name__, exc)))
            continue
        all_rows.append(("INFO", "berkas", "%s [%s] kanal=%s" % (p, doc.fmt, channel)))
        all_rows.extend(evaluate(doc, channel, opts).rows)

    for i, snippet in enumerate(sorted(opts.text), 1):
        doc = extract_plain("teks-%d.md" % i, snippet)
        all_rows.append(("INFO", "berkas", "teks-%d [md] kanal=%s" % (i, channel)))
        all_rows.extend(evaluate(doc, channel, opts).rows)

    lines, fails = render(all_rows)
    sys.stdout.write("\n".join(lines) + "\n")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
