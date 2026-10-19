"""GAYA-AHLI-1005 S15 - generator fixture merah-hijau untuk scanner jejak AI v1.9.0.

Menulis berkas fixture statis (UTF-8, LF) + f3_manifest.json ke --outdir.
Deterministik: konten dibangun dari konstanta di berkas ini, tanpa waktu dan
tanpa rawak, sehingga dua kali jalan menghasilkan byte yang persis sama.

Sumber kasus: docs/2026-10-05-gaya-bahasa-forensik/work/f3_putusan-mekanisasi.md
(syarat tutup Seksi 8: kasus positif-palsu TERDOKUMENTASI papan lintas-misi,
bukan fixture karangan baru) dan f3_impl-notes.md (daftar check S14).

Semantik ekspektasi (dibaca runner f3_run_fixtures.py):
  mode "all"  : SEMUA baris yang cocok kunci harus memenuhi want/want_not/detail
  mode "any"  : CUKUP satu baris yang cocok memenuhinya (pakai bila scanner
                mencetak baris utama + baris "DIKECUALIKAN blok" untuk kunci sama)
  check "exit": kode keluar scanner yang diharapkan
  known_defect: deviasi dilaporkan NEEDS_REVIEW (bukan FAIL) dengan bukti;
                dipakai untuk temuan kartu ini yang butuh putusan controller.
"""
import argparse, hashlib, json, os, sys

EM = chr(0x2014)   # em dash U+2014 - lewat chr() agar berkas sumber ini sendiri
#                      bebas literal glif (gerbang naturalisasi A1/A2 nol).

# ---------------------------------------------------------------------------
# BASE = paragraf bersih terverifikasi: 3 kalimat satu paragraf, rata-rata
# >= 18 kata, ada angka spesifik, ada kata batasan, tanpa verba hedging, tanpa
# frasa daftar hitam, rantai klausa rendah, subjek manusia. Sapuan pada v1.9.0
# kanal doc = exit 0 nol FAIL (dibuktikan probe kartu ini). Fixture HIJAU
# dibangun DI ATAS basis ini supaya "hijau" berarti bersih sungguhan.
# ---------------------------------------------------------------------------
BASE = (
    "Tim kelistrikan kami menyelesaikan pemeriksaan panel distribusi utama pada minggu "
    "kedua Maret 2026 setelah menerima surat tugas resmi dari bagian perencanaan dua hari "
    "sebelumnya. Sebanyak 12 feeder diukur arus beban puncaknya dan hasilnya dicocokkan "
    "dengan catatan pemeliharaan tahunan yang disimpan di lemari arsip lantai dua gedung "
    "operasional. Keterbatasan pengukuran ini adalah hanya 4 dari 12 feeder yang dapat "
    "dipantau terus menerus selama jendela pemeliharaan berlangsung sehingga sisanya kami "
    "periksa secara berkala.\n")

FIXTURES = {}


def fx(name, channel, text, checks, note, arah=None):
    """arah: MERAH = masukan yang HARUS tertangkap; HIJAU = masukan sah yang
    TIDAK boleh tertangkap (positif-palsu). Default diambil dari sufiks nama
    berkas; fixture yang namanya tidak memuat arah diberi argumen eksplisit."""
    if arah is None:
        arah = "MERAH" if name.endswith("-red.md") else "HIJAU"
    FIXTURES[name] = {"channel": channel, "text": text, "checks": checks,
                      "note": note, "arah": arah}


# ---------------------------------------------------------------------------
# M-05 (BUG batas kata frasa_hits) - kasus bernama CH17 'such as an aisle'
# ---------------------------------------------------------------------------
fx("f3-m05-aisle-green.md", "doc",
   "Papan nama lorong di gudang utama zona B mengikuti standar penandaan yang kami tetapkan "
   "bersama vendor pada Maret 2026 dengan tinggi pemasangan 2,20 meter dari lantai. Contoh "
   "bentuk penandaan yang sah adalah such as an aisle name pada rak zona B sepanjang 40 meter. "
   "Sebanyak 42 papan diverifikasi terpasang kokoh dan terbaca jelas dari jarak 5 meter saat "
   "inspeksi pagi. Keterbatasan penilaian ini adalah 3 papan tertutup barang dagangan sehingga "
   "kami nilai ulang pada inspeksi berikutnya.\n",
   [{"check": "A4", "want": "PASS"}, {"check": "C-4", "want": "PASS"},
    {"check": "exit", "want": 0}],
   "CH17: substring 'as an ai' di dalam 'such as an aisle name' tidak boleh tertangkap (fix M-05)")
fx("f3-m05-asanai-red.md", "doc",
   "Sebagai model bahasa, as an ai, saya menyusun laporan inspeksi panel distribusi utama ini "
   "dengan hati-hati lalu kami periksa ulang isinya bersama tim kelistrikan sebelum berkas "
   "diedarkan ke bagian perencanaan pada minggu yang sama. Keterbatasan laporan ini adalah "
   "hanya 4 dari 12 feeder yang dipantau terus menerus selama jendela pemeliharaan berjalan.",
   [{"check": "A4", "want": "FAIL"}, {"check": "C-4", "want": "FAIL"},
    {"check": "exit", "want": 1}],
   "pemakaian asli 'as an ai' tetap tertangkap - arah merah dijaga")

# ---------------------------------------------------------------------------
# M-01 C-26 plafon kepadatan klausa (mode pantauan / INFO dulu)
# ---------------------------------------------------------------------------
fx("f3-m01-clause-red.md", "doc",
   ("Tim lapangan memeriksa panel, mencatat suhu, mengukur arus, memotret nameplate, lalu "
    "menyusun berita acara resmi yang ditandatangani bersama oleh kedua belah pihak. ") * 6,
   [{"check": "C-26", "want": "INFO", "detail": "DI ATAS ambang"},
    {"check": "exit", "want": 1}],
   "rantai >=4 pemisah klausa menagih mode pantauan C-26")
fx("f3-m01-clause-green.md", "doc", BASE,
   [{"check": "C-26", "want": "PASS"}, {"check": "exit", "want": 0}],
   "prosa kendur di bawah ambang 2,2/20% harus PASS")

# Syarat putusan M-01 butir 1: baris turunan, formula, sitasi, dan sel tabel WAJIB
# keluar dari hitungan; kalau tidak, butir ini mengulang cacat I-3.
_TBL = ["| Rumus | Bentuk | Hasil |", "|---|---|---|"]
for _i in range(12):
    _TBL.append("| Daya terpasang panel %d | P = V x I x cos phi | %d kW |" % (_i + 1, 10 + _i))
fx("f3-m01-tablesel-green.md", "doc",
   BASE + "\n" + "\n".join(_TBL) + "\n\nSebanyak 12 baris hasil pada tabel di atas kami serahkan "
   "ke bagian pemeliharaan untuk ditindaklanjuti bersama pada pekan depan sesuai jadwal yang "
   "sudah disepakati kedua belah pihak minggu ini.\n",
   [{"check": "C-26", "want": "PASS"}, {"check": "C-27", "want": "PASS"},
    {"check": "exit", "want": 0}],
   "sel tabel/formula padat koma tidak menaikkan metrik klausa (syarat M-01 butir 1)")

# ---------------------------------------------------------------------------
# M-02 C-27 plafon rata-rata kata per kalimat
# ---------------------------------------------------------------------------
fx("f3-m02-longavg-red.md", "doc",
   ("Ketika beban puncak meningkat tajam pada kuartal ketiga maka tim operasi wajib melakukan "
    "pengukuran ulang pada setiap panel distribusi yang melayani zona produksi agar risiko "
    "gangguan berantai dapat ditekan sedini mungkin sebelum berdampak luas pada aktivitas "
    "pelanggan industri yang berlangganan daya besar di kawasan tersebut. ") * 3,
   [{"check": "C-27", "want": "INFO", "detail": "DI ATAS plafon"}, {"check": "exit", "want": 1}],
   "rata-rata lapis prosa di atas plafon 32 memicu mode pantauan C-27")
fx("f3-m02-longavg-green.md", "doc", BASE,
   [{"check": "C-27", "want": "PASS"}, {"check": "exit", "want": 0}],
   "rata-rata dalam rentang target K2 21-32 harus PASS")

# ---------------------------------------------------------------------------
# M-10 C-28 subjek verba keputusan bukan artefak alat
# ---------------------------------------------------------------------------
fx("f3-m10-toolsubj-red.md", "doc",
   ("Scanner menetapkan batas ambang lalu menolak berkas yang tidak lengkap sebelum laporan "
    "diedarkan ke ruang arsip. Parser menghitung ulang jumlah baris kemudian validator "
    "menerbitkan daftar temuan yang baru. ") * 3,
   [{"check": "C-28", "want": "INFO", "detail": "DI ATAS ambang"}, {"check": "exit", "want": 1}],
   "subjek artefak alat pada verba keputusan memicu mode pantauan C-28")
fx("f3-m10-humansubj-green.md", "doc",
   "Kami menetapkan batas ambang sendiri setelah rapat internal pagi tadi di ruang sidang lantai "
   "dua. Tim kami memilih metode manual yang lebih murah biayanya dibanding otomasi penuh yang "
   "diusulkan kontraktor pada pertemuan minggu sebelumnya. Kami menolak usulan otomasi penuh itu "
   "karena biaya perangkatnya belum sepadan dengan manfaatnya sekarang. Keputusan ini berlaku "
   "untuk seluruh 12 unit kerja mulai kuartal depan setelah anggaran penunjang disahkan manajemen, "
   "dengan keterbatasan bahwa 3 unit masih menunggu persetujuan tertulis.\n",
   [{"check": "C-28", "want": "PASS"}, {"check": "exit", "want": 0}],
   "subjek manusia pada verba keputusan harus PASS")

# ---------------------------------------------------------------------------
# M-15 C-33 konsistensi konvensi numerik dalam dokumen
# ---------------------------------------------------------------------------
fx("f3-m15-rupiah-red.md", "doc",
   "Anggaran tahap satu Rp 500.000 dan tahap dua Rp 750.000 dicairkan bertahap sesuai jadwal "
   "kontrak induk yang sudah disepakati kedua pihak pada rapat perencanaan awal tahun. Kontraktor "
   "mengajukan penyesuaian menjadi Rp500.000 flat lalu Rp625.000 untuk pekerjaan tambahan di "
   "gedung operasional lantai tiga. Keterbatasan catatan ini adalah 2 pos pekerjaan tambahan "
   "belum diverifikasi lapangan sehingga angkanya dapat berubah.\n",
   [{"check": "C-33", "want": "INFO", "detail": "rupiah campur"}, {"check": "exit", "want": 0}],
   "varian rupiah tempel vs ber-spasi sama-sama berpopulasi memicu mode pantauan C-33")
fx("f3-m15-rupiah-green.md", "doc",
   "Anggaran tahap satu Rp 500.000 dan tahap dua Rp 750.000 dicairkan bertahap sesuai kontrak "
   "induk yang sudah ditandatangani kedua pihak pada rapat sebelumnya. Sisa anggaran tahap tiga "
   "Rp 900.000 dijadwalkan cair pada kuartal berikutnya setelah berita acara pemeriksaan pertama "
   "terbit dan diverifikasi bagian keuangan. Keterbatasan jadwal ini adalah 1 pos menunggu "
   "keputusan manajemen puncak sehingga tanggalnya belum tetap.\n",
   [{"check": "C-33", "want": "PASS"}, {"check": "exit", "want": 0}],
   "satu varian rupiah konsisten harus PASS")

# ---------------------------------------------------------------------------
# M-09 rasio pembuka kalimat - gerbang aktivasi >2.000 kalimat bernilai.
# Pasangan STRES: tujuannya menguji gerbang aktivasi + arah vonis, bukan mutu
# dokumen. Ambang 2.000 kalimat memaksa berkas raksasa yang pasti menjatuhkan
# metrik gaya lain (C-6/C-14/C-16), jadi fixture ini TIDAK menuntut exit 0 -
# runner hanya memvonis baris M-09. Dinyatakan di f3_fixture-notes.md.
# Kosakata pembuka diturunkan dari korpus misi (first-word DATUM-MANUAL,
# DATUM-HOUSE-000, DEMS-SPPT) supaya bahasanya Indonesia nyata, bukan karangan.
# ---------------------------------------------------------------------------
_M09_PRED = [
    "memperlihatkan hasil pengukuran harian di lokasi",
    "menyimpang dari batas yang disepakati kedua pihak",
    "sesuai spesifikasi pabrikan terbaru tahun ini",
    "menuntut pemeriksaan ulang oleh petugas jaga",
    "tercatat dalam lembar kerja lapangan minggu ini",
    "dikirim ke ruang arsip digital kemarin sore",
    "dibahas dalam rapat tinjauan manajemen pagi",
    "disetujui kedua belah pihak pekan lalu",
    "masih menunggu verifikasi independen tim lain",
    "dicatat sebagai temuan minor oleh inspektur",
]
_M09_POOL = [ "abbreviations", "aborts", "about", "above", "abridged", "absan", "absen",
    "absolut", "absolute", "abstrak", "abstraksi", "acak", "accent", "accented", "accept",
    "acceptance", "access", "accessible", "accompanies", "accountability", "accuristech",
    "across", "acts", "actual", "actually", "actuator", "acuan", "adalah", "adanya",
    "adaptasi", "added", "adding", "address", "addressed", "adds", "aditif", "administrasi",
    "administratif", "administration", "admiralty", "adopsi", "adopsinya", "advan",
    "advokat", "after", "again", "against", "agar", "agen", "agree", "agrees", "agregat",
    "ahsp", "airflow", "ajukan", "akal", "akan", "akar", "akhir", "akibat", "akibatnya",
    "akreditasi", "aksen", "akses", "aksi", "aktif", "aktivitas", "aktor", "aktuator",
    "aktuatornya", "akumulasi", "akun", "akurasi", "akurat", "akustik", "alamat", "alami",
    "alarm", "alasan", "alasannya", "alat", "alatnya", "alert", "alias", "aliases",
    "aligned", "alignment", "aliran", "allocated", "allowed", "alluvial", "almost",
    "alokasi", "alone", "already", "also", "alternatif", "alur", "always", "aman", "ambang",
    "amber", "ambigu", "ambil", "ampere", "ampiran", "amplifier", "amplop", "anak",
    "analisis", "analysis", "anatomi", "anatomy", "ancaman", "anchor", "anchors", "anda",
    "andal", "anduril", "andy", "anggaran", "anggarannya", "anggota", "angka", "angkanya",
    "angles", "animasi", "animations", "anjuran", "annex", "annexes", "annotation",
    "announces", "annually", "anomali", "anotasi", "another", "anri", "ansi", "answer",
    "antar", "antara", "antaranya", "antarmuka", "antarskill", "antrean", "anyone",
    "anything", "anywhere", "apakah", "aparatus", "aparatusnya", "apart", "aplikasi",
    "apparatus", "appear", "appears", "append", "appliance", "applies", "aptos", "arah",
    "arahan", "arbitrer", "arch", "archimate", "architecture", "archive", "area", "argumen",
    "argument", "arguments", "arial", "arithmetic", "aritmetika", "around", "arrester",
    "arrives", "arrow", "arrows", "arsenal", "arsip", "arsipnya", "arsir", "arsiran",
    "arsitektur", "artefact", "artefacts", "artefak", "arti", "artikel", "artinya", "arus",
    "asal", "asalnya", "aset", "aside", "asignasi", "asimetri", "asing", "asked", "asks",
    "asli", "aslinya", "asme", "aspect", "aspek", "assembly", "asserts", "assessed",
    "assessments", "assets", "assigned", "assumed", "assumption", "assumptions", "asumsi",
    "atas", "atasnya", "atau", "atestasi", "atribusi", "atribut", "attaches", "attest",
    "attestation", "attribute", "aturan", "aturannya", "audiens", "audiensnya", "audio",
    "audit", "auditor", "audits", "august", "autentikasi", "autentisitas", "author",
    "authority", "authors", "autokorelasi", "auxiliary", "avoid", "awal", "awalnya", "awam",
    "axis", "ayat", "azure", "baca", "bacaan", "back", "backplane", "badan", "bagaimana",
    "bagi", "bagian", "bagus", "bahan", "bahasa", "bahkan", "bahwa", "baik", "baku",
    "bakunya", "balance", "balik", "baliknya", "band", "banding", "bands", "bangka",
    "bangun", "bangunan", "banned", "banner", "bantahan", "bantu", "banyak", "barang",
    "bare", "bareskrim", "baris", "barisnya", "barrier", "bars", "baru", "basah", "basal",
    "base", "basefont", "baseline", "basi", "basic", "basis", "basisnya", "batas",
    "batasnya", "baterai", "battery", "bawah", "bawahnya", "bayangan", "bdxl", "beban",
    "bebas", "beberapa", "because", "become", "becomes", "beda", "been", "before", "begin",
    "begitu", "behalf", "behaviour", "behind", "bekerja", "beku", "belakang", "belakangan",
    "belas", "beliau", "believed", "belong", "below", "belum", "benang", "benar", "bendera",
    "benderanya", "beneath", "bentuk", "bentuknya", "berada", "berakhir", "berakhiran",
    "beraksi", "beralamat", "beralasan", "beralert", "berangka", "berangkat", "berani",
    "berantai", "berapa", "berarti", "berasal", "berat", "berawalan", "berbagi",
    "berbahasa", "berbahaya", "berband", "berbar", "berbasis", "berbeda", "berbendera",
    "berbentuk", "berbicara", "berbohong", "berborder", "berbunyi", "bercabang",
    "berchecklist", "berdampingan", "berdasar", "berdata", "berdaulat", "berderajat",
    "berdiri", "berdokumen", "beredar", "berestimasi", "berevolusi", "berfield", "berfill",
    "berformat", "berformula", "berformulir", "berfungsi", "bergantung", "bergaris",
    "bergaya", "bergerak", "bergeser", "berguna", "berhak", "berharga", "berhenti",
    "berhyphen", "berikut", "berikutnya", "berimbang", "berinstrumen", "berisi", "berjalan",
    "berjalur", "berjejak", "berjenjang", "berjumlah", "berkapasitas", "berkas",
    "berkasnya", "berkedudukan", "berkelakuan", "berkelas", "berkoma", "berkotak",
    "berkunci", "berlabel", "berlaku", "berlapis", "berlensa", "bermakna", "bermark",
    "bermerek", "bermesin", "bermodal", "bermuara", "bernama", "bernilai", "bernomor",
    "berpagar", "berpangkalan", "berpasangan", "berpemilik", "berpemisah", "berpengaruh",
    "berperingatan", "berpikir", "berpindah", "berpola", "berpredikat", "berprefiks",
    "berprioritas", "berrentang", "bersama", "bersamaan", "bersangkutan", "bersatuan",
    "berseri", "bersidik", "bersifat", "bersih", "bersinggungan", "bersitasi", "berskrip",
    "berstatus", "berstruktur", "bersudut", "bersumber", "bersyarat", "bertabrakan",
    "bertahan", "bertahap", "bertambah", "bertanda", "bertanggal", "bertanya", "bertemu",
    "bertentangan", "bertitik", "bertransformasi", "bertumpu", "berubah", "berukuran",
    "berulang", "berumah", "berumur", "berupa", "berurutan", "berwaktu", "berwarna",
    "berwenang", "besar", "besaran", "besarnya", "beserta", "beside", "between", "biasa",
    "biasanya", "biaya", "biayanya", "biayaumum", "bicsi", "bidang", "bila", "bilangan",
    "bill", "bind", "binding", "binds", "biner", "bingkai", "bintang", "bipm", "bisa",
    "bisnis", "black", "block", "blocks", "blok", "blokir", "blokirnya", "blueprint",
    "bmkg", "bnpt", "bobot", "bocor", "body", "bohong", "bola", "bold", "boleh", "bolong",
    "border", "borders", "borrowed", "both", "bound", "boundaries", "boundary", "boxed",
    "boxes", "boya", "bpmn", "bracket", "brackets", "branches", "breach", "breached",
    "break", "breaker", "breaks", "brief", "briefs", "buatan", "bubble", "budget", "build",
    "builder", "building", "builds", "built", "buka", "bukan", "bukti", "buktinya", "buku",
    "bulan", "bulat", "bullet", "buntu", "bunyi", "buruk", "buruknya", "busbar", "busy",
    "buta", "butir", "butirnya", "butuh", "buys", "byte", "cabang", "cacah", "cacat",
    "cacatnya", "cadangan", "cakram", "cakupan", "calculated", "calculation", "calibration",
    "calibri", "call", "caller", "callout", "calls", "camera", "campur", "campuran",
    "cannot", "cantik", "cantumkan", "capabilities", "capability", "capacity", "capaian",
    "capital", "capitals", "caps", "caption", "captions", "cara", "care", ]


def _m09_text(n, opener_repeat):
    """n kalimat; pembuka ke-i diambil dari pool[(i // opener_repeat)]."""
    return " ".join(
        "%s %s." % (_M09_POOL[(i // opener_repeat) % len(_M09_POOL)].capitalize(),
                    _M09_PRED[i % len(_M09_PRED)]) for i in range(n)) + "\n"


fx("f3-m09-lowopener-red.md", "doc", _m09_text(2100, 40),
   [{"check": "rasio pembuka", "want": "INFO"}],
   "pasangan stres gerbang >2.000 kalimat: rasio pembuka di bawah 0,20 -> INFO")
fx("f3-m09-diverse-green.md", "doc", _m09_text(2100, 1),
   [{"check": "rasio pembuka", "want": "PASS"}],
   "pasangan stres gerbang >2.000 kalimat: rasio pembuka di atas 0,20 -> PASS")

# ---------------------------------------------------------------------------
# M-03 D18 lapis satu (rincian aparatus) + lapis dua (blok kutipan)
# ---------------------------------------------------------------------------
fx("f3-m03-aparatus-d16.md", "doc",
   "# Standar Rumah%sAlat Ukur\n\nProvenans: salinan baku%sversi 3\n\n"
   "> Penanda D16: aparatus rumah terkendali.\n" % (EM, EM),
   [{"check": "rincian aparatus", "want": "INFO"}, {"check": "C-1", "want": "FAIL"}],
   "lapis satu: berkas berpenanda D16 dapat rincian aparatus, vonis C-1 TETAP mutlak FAIL",
   arah="MERAH")
fx("f3-m03-aparatus-nod16-green.md", "doc",
   "# Standar Rumah%sAlat Ukur\n\nProvenans: salinan baku%sversi 3\n\n"
   "Berkas ini tanpa penanda D16 sehingga rinciannya tidak boleh muncul.\n" % (EM, EM),
   [{"check": "rincian aparatus", "want_not": "INFO"}, {"check": "C-1", "want": "FAIL"}],
   "lapis satu dua arah: tanpa penanda D16 tidak ada baris rincian aparatus, C-1 tetap mutlak")
_QBODY = ("> Semoga membantu dan jangan ragu bertanya jika ada bagian yang perlu dijelaskan "
          "lebih lanjut oleh tim kami.\n> Please let me know if you need anything else from our "
          "side, we are glad to help.\n")
fx("f3-m03-quote-marked-green.md", "doc",
   BASE + "\n> Blok Kutipan: sumber surat vendor PT Alpha, arsip email 2026-09-12\n" + _QBODY,
   [{"check": "A4", "want": "PASS", "mode": "any"}, {"check": "C-4", "want": "PASS", "mode": "any"},
    {"check": "DIKECUALIKAN blok", "want": "INFO"}, {"check": "exit", "want": 0}],
   "D18 lapis dua: kutipan vendor BER-RUJUKAN mengecualikan prosa surat dari A4/C-4 (kasus I-5)")
fx("f3-m03-quote-unmarked-red.md", "doc",
   BASE + "\n> Blok Kutipan: catatan penting belaka\n" + _QBODY,
   [{"check": "A4", "want": "FAIL"}, {"check": "tanpa rujukan", "want": "INFO"},
    {"check": "exit", "want": 1}],
   "penanda Blok Kutipan tanpa rujukan sumber DITOLAK -> prosa surat kembali divonis A4")

# ---------------------------------------------------------------------------
# M-04 whitelist struktural C-14 (boilerplate wajib-seragam)
# ---------------------------------------------------------------------------
_SIG_ID = ("Hormat kami, Benny Wijaya Manajer Hubungan Internasional PT Gemilang Satria "
           "Perkasa yang beralamat di kantor pusat lantai dua dan dihubungi melalui "
           "surat resmi bagian sekretariat pada jam kerja hari kerja.")
_SIG_EN = ("Kind regards, Benny International Relations Staff PT Gemilang Satria Perkasa "
           "yang berkantor di lantai dua dan dihubungi melalui surat resmi sekretariat "
           "pada jam kerja hari kerja.")
_DUPNAR = ("Panel distribusi utama mengalami lonjakan suhu pada jam beban puncak sehingga tim "
           "melakukan pengukuran ulang arus dan tegangan di lokasi kejadian.")
fx("f3-m04-boilerplate-green.md", "doc",
   BASE + "\n" + "\n\n".join([_SIG_ID] * 4) + "\n",
   [{"check": "C-14", "want": "PASS"}, {"check": "exit", "want": 0}],
   "blok tanda tangan ID berulang (whitelist tertutup _DUP_BOILER_RE) tidak dihitung salinan")
fx("f3-m04-narrative-red.md", "doc",
   BASE + "\n" + "\n\n".join([_DUPNAR] * 4) + "\n",
   [{"check": "C-14", "want": "FAIL"}, {"check": "exit", "want": 1}],
   "gagasan narasi ditulis ulang 4x TETAP FAIL - whitelist bukan penghapusan pemeriksaan")
# Kasus bernama register I-6 (surat vendor V18/V19): blok tanda tangan berbahasa
# Inggris. PUTUSAN Seksi 2 M-04 + R3 3.6 menuntut bentuk ini PASS; daftar tertutup
# _DUP_BOILER_RE hanya mengenal 'dengan hormat|hormat kami' sehingga idiom EN
# 'Kind regards' tidak termasuk -> fixture ini MENAGIH tambalan (DEFECT-1).
fx("f3-m04-kindregards-green.md", "doc",
   BASE + "\n" + "\n\n".join([_SIG_EN] * 4) + "\n",
   [{"check": "C-14", "want": "PASS"}, {"check": "exit", "want": 0}],
   "DEFECT-1: blok tanda tangan EN berulang sah - whitelist belum mengenal idiom EN",
   )
FIXTURES["f3-m04-kindregards-green.md"]["known_defect"] = (
    "DEFECT-1: PUTUSAN M-04 + R3 seksi 3.6 menyebut blok tanda tangan 'Kind regards' sebagai "
    "boilerplate sah yang wajib PASS C-14, tetapi _DUP_BOILER_RE hanya memuat padanan Indonesia "
    "('dengan hormat|hormat kami'). Bentuk nyata korpus VENDOR-V19 (baris pendek berpisah, "
    "dijadikan fixture f3-m04-sigblock-real-green.md) lolos karena tiap baris di bawah ambang "
    "6 kata, jadi positif-palsu tidak muncul di korpus hari ini; namun begitu surat diratakan "
    "menjadi satu kalimat panjang (ekstraktor docx/teks biasa) gerbang salah vonis pada kedua "
    "scanner. Putusan yang dibutuhkan: tambahkan idiom EN ke daftar tertutup atau cabut "
    "kasusnya dari register.")
# Bentuk nyata blok tanda tangan VENDOR-V19: lolos pada v1.8.1 DAN v1.9.0 karena
# tiap baris di bawah ambang 6 kata - dibukukan agar DEFECT-1 tidak terbaca
# sebagai 'korpus nyata pernah salah vonis'.
_SIGBLOCK = ("Kind regards,\nBenny\nInternational Relations Staff\n"
             "PT Gemilang Satria Perkasa (GSP)")
fx("f3-m04-sigblock-real-green.md", "doc",
   BASE + "\n" + "\n\n".join([_SIGBLOCK] * 9) + "\n",
   [{"check": "C-14", "want": "PASS"}, {"check": "exit", "want": 0}],
   "bentuk nyata blok tanda tangan EN (baris pendek) PASS pada v1.8.1 dan v1.9.0")

# ---------------------------------------------------------------------------
# M-12 perluasan C-13 identifier kelas baru (INFO permanen putaran ini)
# ---------------------------------------------------------------------------
fx("f3-m12-newclass-red.md", "doc",
   BASE + " Status tiket berubah menjadi READY_FOR_REVIEW setelah verifikasi selesai, dan kami "
   "catat pergantian itu di log harian tim dokumentasi pada 5 Oktober 2026 bersama bukti tanda "
   "terima pekerjaan lapangan hari itu.\n",
   [{"check": "perluasan C-13", "want": "INFO", "detail": "READY_FOR_REVIEW"},
    {"check": "C-13", "want_not": "FAIL"}, {"check": "exit", "want": 0}],
   "enum ALLCAPS bergaris-bawah dilaporkan INFO kelas baru, tidak pernah menjatuhkan FAIL")
fx("f3-m12-whitelist-green.md", "doc",
   BASE + " Kami menjalankan perintah git config core.autocrlf true sebelum menyeragamkan akhir "
   "baris pada repositori dokumen internal tim agar berkas seragam lintas platform kerja kami.\n",
   [{"check": "C-13", "want": "PASS"},
    {"check": "perluasan C-13", "want_not": "INFO"}, {"check": "exit", "want": 0}],
   "CH02: stem konfigurasi alat git-config tidak tersandung identifier kelas baru")

# ---------------------------------------------------------------------------
# M-13 perluasan C-18 penghitung kalimat padat penanda [R-n]
# ---------------------------------------------------------------------------
fx("f3-m13-rmark-red.md", "doc",
   BASE + "\n" + ("Panel feeder satu mengalami lonjakan suhu [R-1][R-2][R-3] sementara panel "
   "feeder dua tetap normal menurut catatan operator jaga malam hari itu juga di ruang kontrol "
   "utama. ") * 3 + "\n",
   [{"check": "C-18", "want": "INFO", "detail": r"kalimat padat penanda \[R-n\] [1-9]"}],
   "satu kalimat memuat >1 penanda rujukan pada <20 kata per penanda dihitung penghitung M-13")
fx("f3-m13-rmark-green.md", "doc",
   BASE + "\nSuhu puncak panel feeder satu tercatat lebih tinggi dibanding feeder dua menurut "
   "catatan operator jaga malam di ruang kontrol utama [R-1].\n",
   [{"check": "C-18", "want": "INFO", "detail": r"kalimat padat penanda \[R-n\] 0 "}],
   "satu penanda [R-n] per kalimat tidak dihitung padat oleh penghitung M-13")

# ---------------------------------------------------------------------------
# M-16 data sapaan institusional K2 pada C-20 (DATA, belum menagih)
# ---------------------------------------------------------------------------
fx("f3-m16-sapaan-data.md", "doc",
   BASE + "\nKami menyampaikan laporan ini kepada Bapak Direktur Operasional. Ibu Manajer "
   "Pemeliharaan meminta data tambahan dan Saudara Kepala Seksi menyetujuinya hari itu juga.\n",
   [{"check": "C-20", "want": "INFO",
     "detail": r"sapaan K2 \[kamu=0, Yth\.=0, Bapak=1, Ibu=1, Saudara=1\]"}],
   "penghitung sapaan K2 menempel sebagai data pada detail C-20, vonis tidak berubah",
   arah="MERAH")
fx("f3-m16-sapaan-absent-green.md", "doc", BASE,
   [{"check": "C-20", "want": "INFO",
     "detail": r"sapaan K2 \[kamu=0, Yth\.=0, Bapak=0, Ibu=0, Saudara=0\]"}],
   "arah dua sisi: dokumen tanpa sapaan mencatat nol pada semua label, bukan angka hantu")

# ---------------------------------------------------------------------------
# C-8b keterangan LIMITATION berbahasa Inggris = MENAGIH (ekor putusan Seksi 8)
# ---------------------------------------------------------------------------
_C8B = (
    "Laporan ini disusun oleh tim rekayasa lapangan untuk keperluan tinjauan internal manajemen "
    "puncak pada kuartal pertama tahun 2026. Sebanyak 12 hasil pengukuran telah kami bandingkan "
    "dengan spesifikasi pabrikan dan catatan pemeliharaan sebelumnya sehingga simpulan sanggup "
    "dipertanggungjawabkan di hadapan auditor eksternal. Kami juga meninjau ulang metode "
    "pengambilan contoh agar hasilnya mewakili kondisi peralatan di lokasi pengujian selama tiga "
    "pekan penuh. Seluruh berkas pendukung disimpan di lemari arsip lantai dua gedung "
    "operasional dan diminta kembali oleh bagian perencanaan bila diperlukan.")
fx("f3-c8b-limitation-red.md", "doc", _C8B + "\n",
   [{"check": "C-8b", "want": "FAIL", "detail": "tanpa pengakuan batasan"},
    {"check": "exit", "want": 1}],
   "dokumen analitis tanpa pengakuan batasan apa pun menagih C-8b (perilaku tak berubah S14)")
fx("f3-c8b-limitation-green.md", "doc", _C8B + (
    " The measurement campaign carries one important limitation: only 2 of 12 feeder bays were "
    "instrumented during the maintenance window, so results for the remaining bays stay "
    "unverified until the next planned outage. Rincian beban puncak tercatat pada tabel lampiran "
    "sebagai rujukan resmi tim.\n"),
   [{"check": "C-8b", "want": "PASS"}, {"check": "exit", "want": 0}],
   "kata 'limitation' berbahasa Inggris diakui LIMITATION_WORDS -> C-8b PASS (tagihan P1)")

# ---------------------------------------------------------------------------
# Kanal kitab (K7) + C-24 momen pembalik
# ---------------------------------------------------------------------------
fx("f3-kitab-clause.md", "kitab",
   ("Tim lapangan memeriksa panel, mencatat suhu, mengukur arus, memotret nameplate, lalu "
    "menyusun berita acara resmi yang ditandatangani bersama oleh kedua belah pihak. ") * 6,
   [{"check": "C-26", "want": "INFO", "detail": "kanal kitab"},
    {"check": "C-27", "want": "INFO", "detail": "kanal kitab"},
    {"check": "C-6", "want": "FAIL"}],
   "kanal kitab: C-26/C-27 runtuh INFO dengan alasan eksplisit, plafon gaya milik C-6 (preseden t_77fd88c3)",
   arah="MERAH")

_C24_FLAT = "".join(
    "\n## BAB %d KONDISI LAPANGAN\n\nTim survei mencatat kondisi eksisting pada area %d dan "
    "menuliskan hasil pengamatan ke dalam lembar kerja lapangan yang ditandatangani pengawas "
    "proyek di lokasi masing masing pada hari yang sama.\n" % (i, i) for i in range(1, 9))
fx("f3-c24-flat-red.md", "doc", _C24_FLAT,
   [{"check": "C-24", "want": "FAIL"}],
   "8 bab katalog tanpa satu pun momen pembalik -> C-24 menagih FAIL (bukti REJECT butir M-07)")
fx("f3-c24-flat-kitab.md", "kitab", _C24_FLAT,
   [{"check": "C-24", "want": "FAIL"}],
   "kanal kitab TIDAK meruntuhkan C-24: vonisnya sudah diputus PUTUSAN t_77fd88c3, bukan dibuka lewat M-07",
   arah="MERAH")
_ARC = _C24_FLAT.replace(
    "\n## BAB 5 KONDISI LAPANGAN\n\n",
    "\n## BAB 5 KONDISI LAPANGAN\n\nHasil pengukuran justru membalik dugaan awal kami: panel "
    "yang semula dianggap paling sehat ternyata menyumbang lonjakan terbesar sehingga seluruh "
    "rencana perbaikan kami susun ulang dari awal.\n\n")
fx("f3-c24-arc-green.md", "doc", _ARC,
   [{"check": "C-24", "want": "PASS"}],
   "satu momen pembalik di badan dokumen cukup untuk C-24 PASS (arah hijau dua sisi)")


def build(outdir, check=False):
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    problems, entries = [], []
    for name in sorted(FIXTURES):
        meta = FIXTURES[name]
        payload = meta["text"].encode("utf-8")
        path = os.path.join(outdir, name)
        if check:
            if not os.path.exists(path):
                problems.append("HILANG " + name)
                continue
            if open(path, "rb").read() != payload:
                problems.append("BEDA   " + name)
        else:
            with open(path, "wb") as fh:
                fh.write(payload)
        e = {"file": name, "channel": meta["channel"], "bytes": len(payload),
             "sha256": hashlib.sha256(payload).hexdigest(), "arah": meta["arah"],
             "checks": meta["checks"], "note": meta["note"]}
        if meta.get("known_defect"):
            e["known_defect"] = meta["known_defect"]
        entries.append(e)
    man = {"generator": "f3_gen_fixtures.py", "mission": "GAYA-AHLI-1005 S15",
           "scanner_target": "v1.9.0 sha16 d61b996931e93dcd", "fixtures": entries}
    mp = os.path.join(outdir, "f3_manifest.json")
    if check:
        if os.path.exists(mp) and json.loads(open(mp, encoding="utf-8").read()) != man:
            problems.append("BEDA   f3_manifest.json")
        return problems
    with open(mp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(man, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
    return problems


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    probs = build(a.outdir, a.check)
    for p in probs:
        print(p)
    print("%s %d fixture -> %s" % ("CHECK" if a.check else "WROTE", len(FIXTURES), a.outdir))
    sys.exit(1 if probs else 0)
