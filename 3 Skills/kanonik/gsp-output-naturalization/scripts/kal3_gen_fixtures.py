"""GAYA-AHLI-1005 KAL3 (kartu t_0d21feab) - generator fixture kanal 'standar'.

Menulis fixture merah-hijau kanal K8 (standar) + manifest ke --outdir dengan
skema yang sama persis dengan f3_gen_fixtures.py sehingga runner lama
f3_run_fixtures.py membacanya tanpa perubahan apa pun (manifest tetap bernama
f3_manifest.json di dalam direktori fixture).

Sumber spesifikasi: docs/2026-10-05-gaya-bahasa-forensik/work/
f4_putusan-kanal-standar.md Seksi 2(a) butir 5 (gerbang terima creator) dan
body kartu KAL3:
  HIJAU : naskah standar minimal (skema berlabel enam bidang, aparatus pendek
          >1 tapi <20%) PASS kanal standar;
  MERAH : (a) frasa hitam A4 dalam prosa kanal standar tetap FAIL;
          (b) tebal emfatis non-label >6/1000w FAIL B6;
          (c) paragraf pendek >20% FAIL B2;
          (d) BERKAS SAMA di kanal doc berperilaku aturan doc (label tetap
              dihitung, rasio absolut <=1 tetap berlaku) - diwujudkan sebagai
              entrik kedua yang menunjuk berkas hijau yang sama dengan
              channel=doc.

Deterministik: konten dibangun dari konstanta, tanpa waktu, tanpa rawak; dua
kali jalan menghasilkan byte yang persis sama. Glif A1/A2 nol (em dash dan
middle dot tidak pernah ditulis; tidak ada literalnya di berkas ini).
"""
import argparse, hashlib, json, os, sys

# ---------------------------------------------------------------------------
# Skema enam bidang S-2 (vocab tertutup STANDAR_FIELD_LABELA di scanner;
# ditulis lewat konstanta agar fixture dan scanner merujuk daftar yang sama).
# ---------------------------------------------------------------------------
LABELS = ("Pernyataan", "Fungsi bagi pembaca", "Bukti manusia",
          "Kontras fleet", "Instrumen penegak", "Predikat verifikasi")


def card(*fields):
    """Satu kartu aturan = SATU paragraf berisi enam bidang berlabel tebal.
    Tiap bidang satu atau beberapa kalimat; seluruh bidang duduk dalam satu
    paragraf (pola manual STD-GAYA-AHLI-001) sehingga tidak menambah hitungan
    paragraf pendek."""
    assert len(fields) == 6
    return " ".join("**%s.** %s" % (lab, txt) for lab, txt in zip(LABELS, fields)) + "\n"


INTRO = (
    "Dokumen miniatur ini adalah bahan uji gerbang kanal standar untuk instrumen "
    "pemeriksa jejak AI rumah dan disusun oleh tim verifikasi sebagai pengganti "
    "naskah normatif sungguhan pada fixture. Setiap aturan di bawah memakai skema "
    "enam bidang yang sama dengan kartu aturan manual gaya rumah sehingga "
    "pengecualian kepala bidang bisa diuji tanpa menyentuh dokumen hidup. "
    "Keterbatasan miniatur ini adalah isinya fiktif dan seluruh angkanya berasal "
    "dari contoh pengukuran panel distribusi yang dipakai sebagai basis bersih "
    "fixture lama sejak misi sebelumnya.\n")

APARATUS = (
    "Indeks miniatur memuat delapan aturan contoh bernomor berurutan.\n",
    "Catatan cakupan: lapis L9 tidak diuji pada berkas ini.\n",
)

RULES = (
    ("Penamaan berkas kerja", (
        "Setiap berkas kerja rumah memakai nama baku berisi kode lapis, nomor aturan, dan tahun terbit agar arsip bisa dicari tanpa membuka isinya. Nama bebas pilihan penyusun dilarang pada berkas yang naik ke rak bersama divisi.",
        "Pegawai baru menemukan berkas tujuan dalam satu ketikan pencarian tanpa bertanya kepada senior. Biaya penelusuran arsip turun tajam ketika seluruh rak mengikuti satu pola yang sama sepanjang tahun.",
        "Register arsip lantai dua mencatat 340 berkas lama berpindah tangan lebih lambat daripada 96 berkas berpola baku selama kuartal pertama 2026.",
        "Tiga profil fleet lama menyimpan laporan dengan akhiran tanggal yang berbeda-beda sehingga auditor kehilangan dua versi dokumen yang sama. Pola baku menghapus kelas kehilangan itu sampai akar namanya.",
        "Pemeriksa nama berkas otomatis berjalan pada gerbang promosi dokumen sebelum berkas masuk rak bersama divisi.",
        "Lulus saat nama berkas memuat kode lapis dan nomor urut sesuai daftar kendali rak. Gagal saat nama hanya berisi kata bebas tanpa kode yang bisa ditelusuri balik.",
    )),
    ("Urutan kepala seksi", (
        "Kepala seksi ditulis berjenjang mulai tingkat dua dan tidak pernah melompat level agar pembaca buta layar tetap memahami hierarki isi. Nomor kepala mengikuti urutan kemunculan, bukan urutan pentingnya gagasan.",
        "Struktur kepala yang rapi menjadi peta jalan bagi pembaca yang memindai dokumen dua ratus halaman. Tanpa peta itu pembaca menyerah di halaman kesepuluh dan isi penting tidak pernah terbaca.",
        "Uji pembaca internal atas enam dokumen panjang menunjukkan rata-rata 22 menit lebih cepat menemukan bagian target setelah jenjang kepala dirapikan.",
        "Dua laporan proyek fleet memakai kepala tebal tanpa jenjang sehingga daftar isi otomatis menghasilkan pohon dangkal. Jenjang markdown biasa sudah cukup memperbaiki daftar isi tanpa alat tambahan.",
        "Pemeriksa struktur kepala berjalan sebagai bagian gerbang bentuk sebelum naskah diserahkan ke reviewer manusia.",
        "Lulus saat seluruh kepala mengikuti jenjang bertingkat tanpa lompatan level. Gagal saat ditemukan kepala setingkat yang melompat lebih dari satu tingkatan.",
    )),
    ("Format angka desimal", (
        "Angka desimal memakai koma sebagai pemisah pecahan dan titik sebagai pemisah ribuan sesuai konvensi bahasa Indonesia yang berlaku di seluruh keluaran rumah. Campur kedua konvensi dalam satu tabel dianggap cacat bentuk.",
        "Pembaca lokal tidak perlu menerjemahkan ulang angka asing sebelum mengambil keputusan teknis. Konsistensi pemisah mencegah salah baca sebesar faktor seribu pada angka beban-rilis yang fatal.",
        "Audit hitungan taksiran menemukan 17 sel tabel terbalik pemisahannya dan tiga di antaranya mengubah keputusan pemilihan vendor secara material.",
        "Sebuah penawaran fleet lama menulis harga dalam format titik Amerika sehingga total tertukar antara pemasok dan pembeli saat rekonsiliasi. Satu aturan pemisah menggagalkan kelas sengketa itu lebih awal.",
        "Pemeriksa konvensi numerik mencetak varian yang bercampur sebagai sinyal pantauan pada sapuan dokumen panjang.",
        "Lulus saat satu konvensi pemisah dipakai konsisten di seluruh badan dokumen. Gagal saat dua konvensi bercampur pada populasi sel yang sama.",
    )),
    ("Rujukan silang antarbab", (
        "Setiap rujukan antarbab menyebut nomor bab dan judul singkat sasaran, bukan kata tunjuk umum seperti bagian sebelumnya yang kehilangan makna saat dokumen dicetak ulang. Penunjuk yang benar membuat salinan cetak setara dengan salinan layar.",
        "Pembaca yang melompat ke bab favoritnya tetap bisa menelusuri dependensi gagasan tanpa membaca linear dari halaman pertama. Rujukan yang tepat sasaran menghemat waktu telaah reviewer eksternal.",
        "Telaah penerbit eksternal atas draf panjang mengembalikan 9 komentar yang seluruhnya berakar pada kata tunjuk ambigu yang sama.",
        "Kitab latihan fleet memakai rujukan nomor halaman statis dan menjadi basi setiap kali tata letak berubah satu milimeter. Rujukan bab-judul bertahan terhadap perubahan tata letak maupun format keluaran.",
        "Pemeriksa pola rujukan mencatat kata tunjuk umum sebagai kandidat perbaikan pada laporan sapuan mingguan.",
        "Lulus saat setiap rujukan menyebut bab sasaran dengan nomor dan judul singkat. Gagal saat rujukan hanya menunjuk posisi relatif tanpa identitas sasaran.",
    )),
    ("Istilah asing pertama", (
        "Istilah asing ditulis sekali beserta padanan bahasa Indonesia pada kemunculan pertama, lalu padanan itu dipakai konsisten sampai akhir dokumen. Daftar istilah wajib memuat setiap pasangan yang diperkenalkan badan aturan.",
        "Pembaca nonspesialis memahami dokumen tanpa membuka kamus dan tetap terhubung dengan literatur asli lewat padanan yang diperkenalkan di awal. Kebiasaan ini menjaga dokumen dinas tetap terbaca lintas generasi pegawai.",
        "Panel pembaca gabungan sipil dan teknis menilai dokumen berpadanan lengkap rata-rata 4 dari 5 banding 2,6 untuk dokumen penuh istilah mentah.",
        "Laporan vendor asing setebal dua ratus halaman tanpa padanan hanya dibaca dua orang internal dan tidak pernah menjadi dasar keputusan. Kehadiran padanan menentukan siapa yang bisa memakai sebuah dokumen.",
        "Pemeriksa istilah mengumpulkan pasangan asing-padanan untuk kelengkapan daftar istilah pada gerbang bentuk.",
        "Lulus saat setiap istilah asing punya padanan terdaftar dan dipakai ulang secara konsisten. Gagal saat istilah mentah berulang tanpa padanan setelah kemunculan pertama.",
    )),
    ("Tanda tangan elektronik", (
        "Lembar pengesahan memuat nama terang, jabatan, dan metode pengesahan yang sah menurut peraturan rumah, dan gambar tanda tangan saja tidak cukup sebagai bukti pengesahan. Metadata pengesahan dicetak terbaca, bukan tersembunyi di properti berkas.",
        "Penerima dokumen bisa memastikan siapa penanggung jawab isi tanpa menghubungi penerbit, dan sengketa keaslian terselesaikan dari lembar itu sendiri. Kejelasan ini melindungi baik penerbit maupun penerima pada pemeriksaan mendadak.",
        "Pemeriksaan kepatuhan tahunan menolak 6 paket serah terima yang pengesahannya hanya berupa tempelan gambar tanpa identitas jabatan yang terbaca.",
        "Arsip fleet lama menyimpan persetujuan dalam tangkapan layar percakapan pribadi yang tidak bisa diaudit organisasi. Lembar pengesahan terbaca memindahkan persetujuan ke ruang yang bisa diperiksa publik internal.",
        "Pemeriksa kelengkapan lembar kendali menagih ketiga unsur pengesahan sebelum paket dinyatakan siap edar.",
        "Lulus saat nama, jabatan, dan metode pengesahan tercetak terbaca pada lembar pengesahan. Gagal saat salah satu unsur hilang atau hanya tersimpan sebagai properti berkas yang tidak terbaca mata.",
    )),
    ("Penyimpanan bukti ukur", (
        "Setiap angka yang terbit di dokumen wajib punya berkas cetakan alat di rumah angkanya masing-masing, dan salinan prosa tidak pernah menggantikan cetakan asli. Rumah angka berarti direktori kerja misi tempat cetakan diproduksi saat giliran pengukuran.",
        "Verifikator independen bisa mengulang pengukuran dari berkas yang sama tanpa mengandalkan ingatan penulis dokumen. Jejak yang utuh mengubah klaim menjadi temuan yang bisa disengketakan dengan bukti, bukan dengan nada bicara.",
        "Reproduksi acak atas 40 angka beban-rilis menemukan 3 selisih pembulatan yang semuanya terlacak ke cetakan yang tidak disimpan penulis aslinya.",
        "Sebuah rekap fleet mengutip angka dari ringkasan pesan sesaat dan gagal direproduksi saat audit karena cetakan alatnya sudah terhapus. Kebijakan rumah angka melarang rantai kutip tanpa sumber cetak.",
        "Pemeriksa register angka menagih pasangan berkas cetakan untuk setiap numeral beban-rilis pada dokumen panjang.",
        "Lulus saat setiap numeral beban-rilis menunjuk berkas cetakan yang ada di direktori kerja misi. Gagal saat angka terbit tanpa rumah angka yang bisa ditelusuri verifikator.",
    )),
    ("Penutup berisi aksi", (
        "Paragraf penutup dokumen kerja menyebut keputusan atau aksi yang diminta beserta penerima dan tenggatnya, bukan ringkasan isi yang mengulang halaman depan. Penutup seperti ini memindahkan tanggung jawab dari penulis ke pemegang wewenang dengan jelas.",
        "Pembaca eksekutif yang hanya membuka dua halaman terakhir tetap tahu apa yang harus ia putuskan dan sampai kapan. Ringkasan isi di posisi itu hanya menunda pertemuan tindak lanjut yang sebenarnya sudah matang.",
        "Rekap triwulan bagian perencanaan mencatat 11 dari 14 memo berpenutup aksi ditindaklanjuti tanpa rapat tambahan, dibanding 3 dari 12 memo berpenutup ringkasan.",
        "Nota internal fleet lama ditutup dengan simpulan umum dan mati di meja sekretariat tanpa satu pun keputusan lahir darinya. Tenggat dan nama penerima terbukti menjadi bahan bakar eksekusi memo.",
        "Pemeriksa struktur penutup membandingkan kalimat terakhir dengan daftar aksi terdaftar pada lembar kendali misi.",
        "Lulus saat penutup memuat aksi, penerima, dan tenggat yang saling cocok dengan lembar kendali. Gagal saat penutup hanya merangkum isi tanpa permintaan tindakan apa pun.",
    )),
)

# Paragraf tambahan untuk fixture MERAH B6: tebal emfatis NON-label yang harus
# tetap dihitung pada kanal standar (residu > 6 per 1.000 kata). Tiap paragraf
# tiga kalimat supaya tidak ikut menggeser rasio paragraf pendek C-7.
EMPHATIC_EXTRA = (
    "Tim verifikasi menekankan bahwa **nama berkas**, **kode lapis**, dan **nomor "
    "aturan** adalah **tiga unsur** yang tidak boleh ditawar pada rak bersama, "
    "sementara **tahun terbit** hanya pelengkap urutan arsip. Catatan lapangan "
    "menyebut **penamaan longgar** muncul paling sering pada **berkas sementara** "
    "milik pegawai yang belum menerima orientasi arsip rumah. Panitia bentuk "
    "menjadikan temuan itu bahan rapat rutin bulanan bersama bagian kearsipan.\n",
    "Kesimpulan sementara panitia menyebut **disiplin bentuk** lebih penting "
    "daripada **kecepatan edar** karena **satu berkas salah nama** memaksa "
    "**seluruh rak** diverifikasi ulang oleh petugas selama **tiga hari** kerja "
    "penuh tanpa jaminan temuan lengkap. Peristiwa pemborosan waktu itu tercatat "
    "pada log bagian perencanaan triwulan pertama tahun berjalan. Dua petugas "
    "senior diminta menyusun panduan singkat agar kejadian serupa tidak berulang "
    "pada rak berikutnya.\n",
)

# Paragraf pendek tambahan untuk fixture MERAH C-7 (rasio > 20%).
SHORT_EXTRA = (
    "Catatan retensi: berkas uji disimpan sampai kartu lanjutan terbit.\n",
    "Batas uji: dokumen hidup manual tidak disentuh fixture ini.\n",
    "Rujukan putusan: lihat lembar keputusan kanal di arsip misi.\n",
)


# Aparatus navigasi pendek: SATU baris di bawah heading sendiri karena pemisah
# paragraf scanner adalah segmen non-prosa (heading/tabel/kode), bukan baris
# kosong - baris kosong dibuang Doc.add dan tidak memotong grup (pitfall
# terukur KAL3 pada v1.10.0). Pola ini mengikuti aparatus indeks manual hidup.
APARATUS = (
    ("## Indeks Miniatur", "Indeks miniatur memuat delapan aturan contoh bernomor berurutan."),
    ("## Catatan Cakupan", "Catatan cakupan: lapis L9 tidak diuji pada berkas ini."),
)


def green_text():
    parts = ["# Standar miniatur aturan rumah K8\n\n", INTRO + "\n"]
    for head, line in APARATUS:
        parts.append(head + "\n\n" + line + "\n\n")
    for i, (title, fields) in enumerate(RULES, 1):
        parts.append("### ATU-K8-%02d %s\n\n" % (i, title))
        parts.append(card(*fields) + "\n")
    return "".join(parts)


def a4_red_text():
    # Cacat konten nyata kelas A4 di prosa: janji bantuan khas agen, dalam
    # kalimat penulis sendiri (bukan kutipan, bukan blok kebijakan).
    return green_text().replace(
        "fixture lama sejak misi sebelumnya.",
        "fixture lama sejak misi sebelumnya. Semoga membantu pembaca menelusuri "
        "setiap aturan dengan cepat.", 1)


def b6_red_text():
    return green_text().rstrip("\n") + "\n\n" + EMPHATIC_EXTRA[0] + "\n" + EMPHATIC_EXTRA[1]


SHORT_HEADS = ("### Catatan Retensi", "### Batas Uji", "### Rujukan Putusan")


def c7_red_text():
    parts = [green_text()]
    for head, line in zip(SHORT_HEADS, SHORT_EXTRA):
        parts.append("\n" + head + "\n\n" + line.strip() + "\n\n")
    return "".join(parts)


FIXTURES = {}


def fx(name, channel, text, checks, note, arah=None):
    """Kunci entrik = (nama berkas, kanal): dua entrik boleh menunjuk SATU
    berkas yang sama dengan kanal berbeda (kontrol arah (d) memakai trik ini)."""
    if arah is None:
        arah = "MERAH" if name.endswith("-red.md") else "HIJAU"
    FIXTURES[(name, channel)] = {"file": name, "channel": channel, "text": text,
                                 "checks": checks, "note": note, "arah": arah}


GREEN_CHECKS = [
    {"check": "C-1", "want": "PASS"},
    {"check": "A4", "want": "PASS"},
    {"check": "C-4", "want": "PASS"},
    {"check": "C-7", "want": "PASS", "mode": "any", "detail": "kanal standar"},
    {"check": "C-8", "want": "PASS", "mode": "any", "detail": "dikecualikan"},
    {"check": "D-TA-09", "want": "PASS"},
    {"check": "exit", "want": 0},
]

fx("k8-standar-green.md", "standar", green_text(), GREEN_CHECKS,
   "HIJAU KAL3: naskah standar minimal (skema enam bidang + aparatus pendek 2/11 "
   "= 18,2% < 20%) harus PASS penuh kanal standar (putusan t_eec55819 2(a).5)")

fx("k8-standar-green.md", "doc", green_text(), [
    {"check": "C-7", "want": "FAIL", "mode": "any"},
    {"check": "C-8", "want": "FAIL", "mode": "any"},
    {"check": "D-TA-09", "want": "FAIL"},
    {"check": "exit", "want": 1},
], "KONTROL arah (d): BERKAS SAMA di kanal doc tetap vonis aturan doc "
   "(C-7 absolut <=1 menagih 2 paragraf; C-8 menghitung 48 label tanpa "
   "pengecualian; agregasi B2+B6 memicu D-TA-09)")

fx("k8-a4-red.md", "standar", a4_red_text(), [
    {"check": "A4", "want": "FAIL", "mode": "any"},
    {"check": "C-4", "want": "FAIL", "mode": "any"},
    {"check": "C-7", "want": "PASS", "mode": "any"},
    {"check": "C-8", "want": "PASS", "mode": "any"},
    {"check": "exit", "want": 1},
], "MERAH arah (a): frasa hitam A4 dalam prosa penulis di kanal standar TETAP "
   "FAIL - kanal bukan penutup cacat konten (larangan eksplisit putusan)")

fx("k8-b6-red.md", "standar", b6_red_text(), [
    {"check": "C-8", "want": "FAIL", "mode": "any", "detail": "tebal residu"},
    {"check": "C-7", "want": "PASS", "mode": "any"},
    {"check": "D-TA-09", "want": "PASS"},
    {"check": "exit", "want": 1},
], "MERAH arah (b): tebal emfatis non-label di atas ambang -> residu C-8 FAIL "
   "dan B6 terpicu walau kepala bidang S-2 dikecualikan")

fx("k8-c7-red.md", "standar", c7_red_text(), [
    {"check": "C-7", "want": "FAIL", "mode": "any", "detail": "kanal standar"},
    {"check": "C-8", "want": "PASS", "mode": "any"},
    {"check": "D-TA-09", "want": "PASS"},
    {"check": "exit", "want": 1},
], "MERAH arah (c): aparatus pendek melampaui rasio 20% total paragraf -> "
   "C-7 FAIL dan B2 terpicu (kelonggaran terukur, bukan karpet)")


def build(outdir, check=False):
    problems = []
    entries = []
    # Berkas unik ditulis sekali (dua entrik boleh menunjuk berkas yang sama).
    seen = {}
    for key in sorted(FIXTURES):
        meta = FIXTURES[key]
        seen.setdefault(meta["file"], meta)
    for name in sorted(seen):
        meta = seen[name]
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
    for key in sorted(FIXTURES):
        meta = FIXTURES[key]
        payload = meta["text"].encode("utf-8")
        e = {"file": meta["file"], "channel": meta["channel"],
             "bytes": len(payload),
             "sha256": hashlib.sha256(payload).hexdigest(), "arah": meta["arah"],
             "checks": meta["checks"], "note": meta["note"]}
        entries.append(e)
    man = {"generator": "kal3_gen_fixtures.py", "mission": "GAYA-AHLI-1005 KAL3",
           "scanner_target": "v1.10.0 sha16 601a96db8f6adda7",
           "fixtures": entries}
    mp = os.path.join(outdir, "f3_manifest.json")
    if check:
        if os.path.exists(mp) and json.loads(open(mp, encoding="utf-8").read()) != man:
            problems.append("BEDA   f3_manifest.json")
        return problems
    os.makedirs(outdir, exist_ok=True)
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
    print("%s %d entri fixture (%d berkas unik) -> %s" % (
        "CHECK" if a.check else "WROTE", len(FIXTURES),
        len(set(k[0] for k in FIXTURES)), a.outdir))
    sys.exit(1 if probs else 0)
