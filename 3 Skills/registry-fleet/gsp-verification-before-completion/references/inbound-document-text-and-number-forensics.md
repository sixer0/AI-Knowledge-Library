# Forensik Dokumen Masuk: Fidelity Teks + Uji Ulang Angka Turunan (tervalidasi 2026-10-07, studi satu dokumen masuk rev A, 35 hal)

Kelas tugas: pengguna menyodorkan SATU berkas laporan (PDF/DOCX) dan minta dipelajari/diaudit
detail, sering dengan "tanpa orkestrasi". Beda dari VERIF-GATE (itu menguji artefak yang KITA
rilis) dan dari `gsp-doc-layout-verification` (itu geometri halaman): di sini objeknya kebenaran
isi + keutuhan teks dokumen pihak lain/edisi kilat yang belum lolos gerbang.

## 0. Preferensi kerja saat user bilang "tanpa orkestrasi"
Eksekusi langsung: TIDAK dispatch RT/TA, TIDAK buat kartu kanban. Gerbang naturalisasi TETAP
berjalan pada jawaban yang dibaca user (draft -> scan -> serahkan dengan jejak VERDICT).
Bentuk keluaran yang diterima user: identitas berkas -> isi per bagian -> hasil uji ulang angka
(PASS/FAIL eksplisit) -> cacat tekstual TERBUKTI -> daftar tindakan -> jejak gerbang paling akhir.

## 1. Triangulasi ekstraktor SEBELUM vonis cacat teks (aturan paling mahal)
Satu ekstraktor TIDAK cukup untuk menvonis dokumen. Jalankan tiga: `pypdf`, `pdftotext`
(dua mode: `-layout` dan flow polos), `pymupdf`. Pola kegagalan yang terbukti:
- **Glyph hilang senyap.** Font subset Type0/Identity-H non-Latin (mis. MicrosoftJhengHei,
  MS Mincho) TIDAK terbaca `pdftotext` (WinAnsi/tanpa peta Unicode) sehingga kata lenyap dari
  ekstraksi padahal TERCIPTA di kertas. Di dokumen studi: "memperlebar 误差 geometri", "band 红外-termal".
  Resep: enumerate font via pypdf `page["/Resources"]["/Font"]` -> kalau ada Type0/Identity-H
  non-Latin, curigai kata bolong; lalu render halaman ke PNG ~150-170 dpi dan baca dengan vision.
  Vonis "kata hilang" hanya sah bila render/vision atau pymupdf mengonfirmasi.
- **Kata dobel artefak layout.** `-layout` bisa menduplikasi frasa saat teks menyambung antar
  baris/kolom. Buktikan dengan `pymupdf page.get_text("words")`: kelompokkan bbox per pita y,
  cek apakah dua kemunculan itu dua kata nyata pada dua baris berbeda. Kasus dokumen studi:
  "<harga> bid miliar bid request" NYATA (y=390 dan y=404, dua baris tercetak), sementara
  sebagian dobel lain cuma artefak. Jangan campur keduanya di laporan.
- **Deteksi tabel tidak bisa dipercaya untuk menghitung baris.** `pymupdf find_tables()`
  mengembalikan NOL pada PDF tabel tanpa garis ruling (kasus ini) meski tabel jelas ada.
  Untuk menghitung baris register/tabel: pola regex baris teks + verifikasi manual.
- `import fitz` sudah deprecated -> pakai `pymupdf`. Menggabungkan `page.get_text()` sefleet
  lalu split `\f` bisa menghasilkan SATU "halaman" -> iterasi halaman eksplisit, jangan split.

## 2. Baterai uji ulang angka turunan (yield tertinggi)
Ambil SEMUA entri berlabel turunan/DITURUNKAN, hitung ulang dari rumus DAN masukan yang ditulis
dokumen itu sendiri. Enam kelas cacat yang benar-benar muncul satu sesi:
1. Nilai BENAR, rumus pencatatan cacat — "piksel x 4 band x 16 bit / 2^30" tanpa /8 (bit->byte);
   hasil 8,29 GB sah, audit balik dari rumus menghasilkan 66,2 GB.
2. Faktor dua salah — pembanding "standar 2N" padahal 100 km2 x T = N.
3. Inkonsistensi model sendiri — P = 100(1-0,6^1,4) = 51,09% tapi terbit 50,6%; selesaikan
   balik n tersirat (n=1,38) untuk membuktikan bukan pembulatan.
4. Salah orde 1000x di prosa — "50 AOI = orde 19 GB/tahun, masih satu unit NAS kecil" vs
   50 x 48 x 8,29 GB = 19.868 GB (19,4 TB). Kelas paling berbahaya: mengubah kesimpulan
   arsitektur, dan lolos karena angkanya "kelihatan masuk akal".
5. Dua agregat tak bisa direkonsiliasi — narasi rentang A-B <satuan uang> vs tabel total C <satuan uang>, C jauh di luar rentang.
   Resep: coba SEMUA kombinasi sub-derivasi (D-01..D-04, per-AOI vs multi-AOI) dan laporkan
   yang terdekat plus asumsi yang hilang, jangan langsung tuduh mengarang.
6. KPI tidak tercapai oleh skenarionya sendiri — target "<T per konfirmasi" vs belanja
   F1 dokumen = B per kasus, B di atas T; kalau satuannya event dan dokumen tak menyebut event/kasus,
   vonisnya "tidak terukur", bukan "salah".
Selalu uji juga klaim struktur yang ditulis dokumen tentang dirinya: "memuat 130 baris data"
(hitung manual: cocok), "18 satelit" vs 20 baris tabel, urutan huruf lampiran (dua "Lampiran A",
huruf D tak pernah dipakai -> rujukan silang ambigu).
Pitfall label provenans: kaki tabel bisa tercetak STATIS (semua berbunyi "PROVENANS PEMASOK",
termasuk glosarium PUBLIK-UMUM dan KPI buatan penyusun), dan kolom Asal bisa salah kelas
(baseline internal sendiri dilabeli PEMASOK/ASUMSI). Label provenans bukan bukti asal.

## 3. Gerbang naturalisasi: pitfall path yang memakan satu giliran
- `scan_ai_footprint.py <path>` balas "CHECK 1: FAIL - tidak ada masukan terbaca (berkas/teks
  kosong)" untuk PATH YANG TIDAK ADA, bukan pesan file-not-found. Vonis pertama saat FAIL itu:
  salah direktori, bukan berkas kosong. `$LOCALAPPDATA/Temp` (terminal/MSYS) dan
  `$LOCALAPPDATA/hermes/Temp` (scratch Hermes) DIREKTORI BERBEDA -> selalu operasikan path
  `resolved_path` yang dikembalikan write_file, jangan bangun ulang dari ingatan.
- `vision_analyze` Windows: pakai forward-slash (`C:/Users/...`). Path backslash ganda
  (`C:\Users\...`) bisa balas "media file not found" untuk berkas yang benar-benar ada.
- Render PDF tanpa poppler: `uv run --with pymupdf python` -> `page.get_pixmap(dpi=150).save()`
  (pdftoppm tidak selalu ada; pdftotext biasanya ada di git-bash mingw64).

## 4. Cara melapor temuan
Pisahkan tegas: (a) cacat faktual/aritmetika yang menuntut koreksi edisi berikutnya,
(b) cacat tekstual/penyajian, (c) hal yang sudah baik. Sertakan penyeimbang — dokumen ini
jujur soal field kosong, menolak halaman 404 lembut sebagai bukti, dan register 130 barisnya
cocok klaim; melapor hanya yang buruk = vonis berat sebelah. Sebut angka hasil ukur sendiri,
bukan salinan angka laporan (anti-halusinasi, SPK-002 butir 9).
