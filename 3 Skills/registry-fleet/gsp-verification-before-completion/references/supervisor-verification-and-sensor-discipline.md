# Supervisor Verification & Sensor Discipline (class-level, distilled 06-12)

Presiden pola dari dua malam supervisi lintas-enam-papan (PROMANUAL, GAYA-AHLI, RAFIFUNITY, PROMANUAL-V2, EKASLAP, VISUAL). Semua vonis pengawas berasal dari CETAKAN ALAT pada giliran itu - tidak ada satu pun klaim dikutip dari laporan pekerja atau ingatan.

## A. Pola kerja countersign pengawas (ulang tiap kartu selesai)
1. JANGAN percaya status `completed` dari judul/notifikasi. Buka papan (`hermes kanban show <id>` lewat skrip python subprocess - bukan grep inline yang rawan petik), baca result penuh + event runs (durasi!) + komentar.
2. Ukur ARTEFAK dengan instrumen sendiri: sha256[:16] + byte + baris + glif (U+2014/U+00B7) + CR; untuk docx/zip: parser zipfile regex urutan-bebas; untuk PDF: PyMuPDF halaman/teks/links/URI terpotong; jalankan ulang scanner/gerbang kanonis dengan argumen posisi berkas (TANPA `--text <path>` - akar F-25-1: scanner mengukur string path, bukan isi).
3. Cocokkan silang dengan countersign GILIRAN SEBELUMNYA (rantai pin: naskah->docx->pdf->companion->bukti). Angka yang sama dari dua instrumen beda-algoritma = kokoh; beda = telusuri definisi sebelum vonis (mis. 487 bookmark vs 0 anchor = definisi berbeda, keduanya benar).
4. Kirim komentar dari BERKAS TEMP (apostrof/& merusak shell); guard `grep -c` pada teks unik SEBELUM dan SESUDAH kirim. Koreksi selalu komentar TERPISAH, jangan sunting komentar lama.
5. REDELIVER (notifikasi kartu yang sudah divonis): cek guard jejak `grep -c "Countersign pengawas"` pada show; jika =1, TANPA komentar baru, cukup nyatakan redeliver ke user.
6. Peta papan WAJIB dipetik dari sensus `hermes kanban list | awk ...` pada giliran kirim; tempel angka final ke draf SEBELUM tayang (pelajaran-ke-12). Bila peta berubah setelah kirim: komentar koreksi peta terpisah.
7. Tindakan penjagaan bukti aditif boleh (salin rekonstruksi byte-eksak ke `_arsip/`, probe read-only) - nyatakan eksplisit di laporan sebagai tindakan pengawas, nol mutasi artefak hidup.

## B. Taksonomi positif-palsu sensor (pelajaran-ke-11: sensus-sensor-dulu sebelum vonis artefak)
Semua pernah menipu sensor pengawas sendiri dan DIBETULKAN sebelum vonis tayang:
- **Path terpotong spasi**: regex `[A-Za-z]:/[^\s]+` memotong "James F. Kurose 7th.pdf" -> 'HILANG' palsu. Solusi: potong sampai pemisah struktural (`|`, backtick, newline), lalu os.path.exists.
- **Backtick penempel**: path dalam markdown code-span menyisakan '`' -> exists gagal. Strip backtick/whitespace sebelum uji.
- **Kolom salah di manifest JSON**: entri punya `path/sha256` kanon tapi kolom `png/sha256_png` hanya terisi sebagian -> '56 berkas hilang' palsu. Sensus pertama (kolom path) = 62/62 ADA. Baca kunci entri dulu (`sorted(items[0].keys())`).
- **Regex atribut XML berurutan**: `<w:hyperlink[^>]*w:anchor=` melewatkan elemen dengan atribut mendahului -> 496 vs aktual 722. Parser robust: ambil seluruh tag hyperlink lalu cari atribut di dalamnya.
- **`--out` diperlakukan DIREKTORI** oleh skrip target -> cmp file-vs-dir = PermissionError/'BEDA semua'. Baca struktur keluaran, bandingkan file-per-file.
- **CRLF vs LF**: byte disk mentah != klaim pasca-normalisasi (30.504 vs 30.329 = selisih CR); sha konten-LF + selisih byte == jumlah CR = koheren, catat dua konvensi.
- **Substring-grep tanpa anchor**: token '404' dalam sha256; DOI "terpotong" filter substring padahal href utuh (kurung nama penulis). Uji bentuk lengkap, bukan fragmen.
- **Interpreter subproses**: `sys.executable` di dalam runner uv = python dasar tanpa dependensi -> rc=2/ModuleNotFound palsu. Panggil dengan dependensi resmi perintah-jalan (baca LAPORAN/resep dulu - TKIT: `--with python-docx --with matplotlib --with pywin32`).
- **Sampler normalisasi teks** menyembunyikan keberadaan heading/table-cell -> probe terarah per sampel.
- **Terminal echo memotong baris panjang** -> jangan simpulkan 'isi terpotong' dari tampilan; baca berkas mentah dengan python.

## C. Koreksi diri & jejak (pelajaran-ke-9/10/12)
- Klaim hasil HANYA dari cetakan yang sudah dipetik; draf berisi kata PASS/FAIL yang belum diukur = cacat sebelum tayang (REVG: klaim hijau penuh ditulis sebelum ujian hidup selesai; tertangkap aturan angka=cetakan-alat).
- Koreksi jejak wajib disensor ke TEKS TAYANG (grep pada `kanban show`) - jangan koreksi draf yang ternyata tak pernah tayang.
- Countersign pengawas ATAS lembar juri: jangan memuat skor mentah per-dimensi bila juri lain masih berjalan (kanal bocor lintas-juri; preseden S12f buta-sebagian).
- Typo/label-salah di komentar tayang -> komentar koreksi terpisah ber-guard.

## D. Kelas cacat artefak yang berulang (untuk gerbang hilir)
- **OPC DOCX XML-langsung**: Id rel duplikat (carry+baru tabrakan `rId46`), Override [Content_Types] hantu menunjuk part absen, Word menolak buka padahal zipfile/python-docx toleran. Gerbang keras: keunikan Id + Override menunjuk part hadir + PROBE BUKA NYATA (Word COM ReadOnly ComputeStatistics). Preseden CHECK 11-14 build_ed3d = rujukan implementasi.
- **DOI/URL kurung**: `10.1002/(SICI)...` termakan parser URL -> rel terpotong 404 lolos SEMUA sensor lemah; tertangkap hanya di gerbang final. Validasi FORMAT rel Target + entity-match tidak cukup.
- **Anchor internal regresi**: rujukan prosa polos tanpa `w:hyperlink w:anchor=` vs pembanding-edisi (Ed2 1.217 anchor) - pembanding edisi = cara satu-satunya menangkap kelas ini.
- **Word regenerasi TOC membuang bookmark kustom** di paragraf sumber TOC (korelasi 487/487, round-trip permanen) -> GoTo PDF non-TOC=0; known-defect ber-register + klausul batas terbit di buku = jalur rilis sah (D-92 cabang B).
- **Builder dokumen besar**: python-docx add_* per-baris kuadratik; resep-B XML-per-bagian-sisip-sekali atau split+docxcompose. Kartu builder-berat-bentuk-satu mati di jendela bridge 1800dtk (instances 7x lintas-fleet) -> formulasi WAJIB rantai per-bab sejak awal; timeout kedua = pecah, bukan resep ketiga; partial-handoff AMBANG-B enam bidang > timeout bisu.
- **Pin-era vs artefak-hidup**: komentar/result mem-pin byte lalu objek disunting -> semua hilir mewarisi pin basi. Norma: pin sah = result kartu TERAKHIR; vonis menempel byte; objek antar-era wajib terarsip byte-eksak (`_arsip/` revA..revF; pelajaran revD hilang lalu diselamatkan rekonstruksi ber-assert).

## E. Transfer fleet yang terbukti sehat
- Alat vonis identik byte di SEMUA salinan profil (F-25-7: gsp-verifier mirror v1.9.1 basi -> resync; cek `cmp`/sha dua jalur sebelum memakai alat pihak-lain).
- Register allow-list ber-fixture (G-NAT-53) + kanal per-genre (KAL `standar`: C-7 rasio <=20%, C-8 vocab tertutup enam label bidang) - pelonggaran lewat putusan ber-angka, bukan ambang global; delta alat HANYA yang diputus + fixture merah-hijau + kontrol arah (kanal lama tetap diberlakukan).
- Penjurian: dua-juri buta-dari-awal (`ls` kosong direkam), SARING/LEPAS dua lapis, selisih>=2 -> adjudikator skor-terkunci-sebelum-baca, goalpost tidak bergeser (gagal substansial vs prosedur dibedakan), disclosure buta-sebagian dibukukan.
- Promosi library: verdict-first custodian-menolak + gatekeeper verifikasi-mandiri (ILPRO-2), status usulan->dipromosikan dengan riwayat-catatan di objek.
