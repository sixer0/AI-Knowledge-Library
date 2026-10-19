# Deadlock kartu kembar, probe rentan-substring, dan koreksi-diri pengawas (06-10/11-2026, RAFIFUNITY/PROMANUAL/GAYA-AHLI)

Tiga pola baru terverifikasi saat pengawasan tiga papan semalam. Semua dari pengukuran disk, bukan laporan.

## 1. Deadlock siklus konsolidasi kartu kembar (kasus ke-5, pertama berakhir deadlock)

Kronologi nyata (rantai FIX-ZIP-CLAIM, 21:45–21:48): dua board-mover create kartu kembar sekaligus (t_0519c9ab + t_d2171469, cakupan sama); controller komentar di kartu B "kanonis = A, BERHENTI"; 60 detik kemudian controller PUTUSAN di kartu A "superseded oleh B" -> A archived -> B tetap blocked menunjuk A yang barusan diarsipkan. **Dua arah saling menunjuk = tidak ada kartu hidup yang memegang kerja (scope yatim).** Papan mencatat 0 running pada cakupan yang masih dibutuhkan sementara gerbang final berjalan di jalur lain.

Deteksi pengawas: setelah notifikasi blocked/superseded, cetak `kanban list` dan tanya **"kartu HIDUP mana yang kini memegang cakupan ini?"** Kalau jawabannya nol (semua kandidat blocked/done-superseded/archived), itu deadlock - bukan konsolidasi bersih. Kontras kasus benar: FIX-BM blocked dengan cakupan sungguh diserap kartu RUNNING (satu arah) = sehat, arsip tinggal formalitas.

Resolusi yang terbukti (D-76): controller create KANONIS BARU satu kali dengan parent sah + body "pemulihan scope yatim" + aset beku siap-pakai; lebih bersih daripada unblock salah satu kembar.

Tiga aturan fleet hasil traceroot (dukung proposal watchdog S14; bukti lintas papan: CH08/09, GEL3-B, S14-simetris, FIX-ZIP-CLAIM-B):
1. **Gerbang-create**: board-mover WAJIB grep `kanban list` untuk kartu setara SEBELUM create (bukan imbauan pasca-kejadian).
2. Komentar konsolidasi wajib menyebut status TERKINI lawan - cek ulang dalam 60 detik terakhir; jangan pernah merujuk kartu yang kauarsipkan sendiri.
3. Saat pencabutan digantikan putusan baru, **koreksi pointer wajib dipasang sebagai komentar di kartu tercabut** - pembaca hilir (F8/G-FINAL/reviewer) membaca kartu mati sebelum menemukan kanonis. Vonis kerja boleh superseded, jejak pointer tidak boleh menyesatkan.

## 2. Probe rentan-substring: sensor naif menghasilkan positif-palsu dua papan

Tiga tangkapan dalam satu sesi, pola sama - pencocokan substring tanpa batas:
- Probe pengawas `'.git' in zip.namelist()` = True padahal hanya `.gitignore` yang cocok; entri pustaka `.git/` sungguhan = 0. Sensor dibetulkan (prefix segmen path) SEBELUM vonis.
- Scanner fleet v1.8.x: frasa blacklist `"as an ai" in text` menvonis A4 pada prosa sah **"such as an aisle name"** (RAFIFUNITY ch17, akar kgali byte-per-byte; kemudian PROMANUAL STD-GAYA-AHLI-001 memuat fixture yang sama). Patch v1.9.0 = regex berbatas kata dengan selftest dua arah (aisle->PASS, pemakaian asli->FAIL) - pola red-green fixture kasus nyata.
- Sensus caption sidecar-vs-naskah mencetak 65/0/23 "beda" padahal pekerja melapor 87/0/1: akar = caption naskah memakai **NBSP (U+00A0)** setelah "Figure" sehingga regex spasi-biasa melewatkan 22 baris. Setelah normalisasi `\xa0 -> ' '`, dua instrumen menyatu. **Angka pekerja ternyata benar; sensor pengawas yang buta.**

Aturan turunannya: SEMUA probe pencocokan (pengawas maupun instrumen) wajib (a) batas kata `\b` untuk frasa, (b) kesamaan segmen path untuk nama berkas, (c) normalisasi NBSP sebelum perbandingan teks, dan (d) kalau hasil probe MENYANGKAL angka pekerja, curigai probe dulu - format nyata artefak diuji sebelum vonis beda. Kasus keenam kalinya disiplin ini dipakai, pertama kali terhadap sensor pengawas sendiri di depan angka pekerja.

## 3. Mention vs use pada blok meta (glif-zone dan residu scanner baru)

Naskah angkut (carry) boleh memuat blok meta yang MENDAFTARKAN mutasi - mis. catatan "em-dash → hyphen" yang sendiri memuat em-dash, atau ch17 L402 yang mengutip frasa terlarang "as an ai" dalam kutipan saat mendokumentasikan defect positif-palsunya. Sensor wajib sadar zona: hitung glif/jejak hanya pada LAPIS BUKU (sebelum penanda CATATAN GERBANG/DIFF-KD), dan laporkan hitungan meta secara terpisah. Vonis penuh atas blok meta = salah sasaran (blok dibuang perakit F8). Kelas tiket scanner iterasi berikut: mode mention (kutipan ter-delimit) / skip-blok-meta untuk detektor frasa.

## 4. Byte-identity vs pergeseran mtime

Re-render idempoten menghasilkan mtime baru dengan BYTE SAMA (fig_14-3.png 20:22 -> 21:07, sha identik). Jangan vonis "objek berubah" dari mtime saja, dan jangan vonis "objek belum diuji" dari mtime lama saja - **yang mengikat vonis adalah hash**. Vision QA yang menempel byte tetap sah lintas pergeseran mtime selama sha256 cocok register (doktrin vonis-menempel-byte, dipakai dua arah: menahan uji sia-sia DAN mewarisi vonis sah).

## 5. Koreksi-diri juga tunduk Iron Law angka=cetakan-alat

Rantai nyata satu sesi: countersign memuat angka peta -> koreksi-kedua ditulis TANPA ukur ulang -> ternyata keliru -> koreksi-ketiga-final mengukurnya segar. Dan pada countersign S14, klaim "CJK/C-15 terbukti ikut terlayani" **dibetulkan sebelum dikirim** oleh kucek lanjutan terhadap daftar butir. Aturan: setiap komentar koreksi/pembaruan diukur dulu seperti vonis biasa; jangan kirim koreksi dari ingatan. Lebih baik koreksi pra-kirim (replace di berkas temp) daripada koreksi pasca-kirim; keduanya sah, yang dilarang adalah koreksi yang tidak diukur.

## 6. Resep vision-tandingan buta untuk pengawas non-vision-sesi

Saat memverifikasi vonis mismatch vision pekerja: panggil vision_analyze dengan pertanyaan BUTA (tidak menyebut target/vonis) + satu konfirmasian negatif ("apakah identifier X masih muncul?"). Dua arah tertangkap dalam satu sesi: 14-3 (kata dobel "Instance" terkonfirmasi + EventLog.I absen) dan 9-4 (penanda terhitung 2, ③ hilang). Pertanyaan harus meminta KUTIPAN TEKS PERSIS, bukan ya/tidak atas cacat.
