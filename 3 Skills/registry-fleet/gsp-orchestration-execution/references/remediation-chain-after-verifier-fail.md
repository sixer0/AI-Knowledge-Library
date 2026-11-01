# Rantai remediasi pasca-verifier FAIL (preseden misi panduan, 25-09)

Trigger: kartu verifikasi (VS) memvonis FAIL atas artefak sintesis sementara DAG
pre-built sudah memasang kartu hilir (mis. build DOCX, gerbang tampil). Yang
diuji di sini: menutup rantai TANPA menghapus gerbang, TANPA kerja terlarang,
TANPA menambal butir yang menunggu putusan user.

## Langkah controller (urut)
1. **Uji vonis sendiri dulu** (spot-check, bukan re-verifikasi penuh): baca
   VERIFICATION-REPORT.md + instrumen di `verification/`, verifikasi ulang 1-2
   temuan kunci dengan curl/grep sendiri. Vonis diterima hanya bila cocok disk.
2. **Ruling lewat komentar kartu**, bukan hanya chat: komentar pada kartu hilir
   (DX) dan countersign (CS) adalah jejak kanonik; salin ringkasannya ke
   Decision Log kontrak misi.
3. **Kartu build hilir: hormati gerbang kontraknya sendiri.** Bila kontrak kartu
   berbunyi 'build hanya dari artefak lolos VS' dan worker sudah memblokir diri
   dengan alasan itu (blocked + laporan, nol artefak terlarang — cek `ls *.docx`
   = kosong), itu GERBANG SEHAT, bukan kegagalan yang perlu ditolong. Biarkan
   blocked.
4. **Relink DAG, bukan stop naratif:**
   `hermes kanban --board default unlink <vs-lama> <build>` lalu
   `link <vs-ulang> <build>`. Parent kartu build menjadi kartu verifikasi-ulang
   sehingga dispatcher menegakkan gerbang lewat graf, bukan lewat ingatan.
5. **Kartu FIX berlingkup sempit** (via lad_card.py, parents = kartu VS + CS):
   daftar suntingan satu-per-satu dengan lokasi presisi (baris/bab), daftar
   DILARANG eksplisit (butir pending-user, berkas hulu), dan gerandang diri
   sebelum serah (grep cacat = 0, curl URL baru = 200, label muncul di baris
   yang sama, em dash = 0, wc dilaporkan).
6. **Kartu VS-R2** (gsp-verifier, parents = FIX): jalankan ULANG instrumen yang
   sama (sha tercatat), vonis per CHECK, tabel delta run-lama→R2. Butir
   pending-user dicatat `pending-user`, dilarang divonis FAIL.
7. **Countersign boleh lanjut dengan lingkaran dipersempit**: agree/disagree per
   set terhadap vonis FAIL + WAJIB mengulang fetch baris jaringan yang flaky
   dengan jeda antar-probe. Kenaikan predikat (NEEDS_REVIEW→PASS) sah hanya bila
   tidak bersandar pada baris flaky dan mengikuti aturan verifier yang tertulis;
   koreksi pembukuan dicatat countersigner.
8. **Ganti watchdog setelah topologi berubah**: watchdog rantai lama dimatikan,
   watchdog baru memantau rantai remediasi (FIX→VS-R2→build→gerbang-tampil).

## Pitfalls kelas ini
- **Sumber mati pasca-panen:** URL 200 saat kolektor membuka halaman, 404 saat
  diverifikasi hari kemudian (host menghapus halaman; CDX bisa nol snapshot).
  Ini BUKAN fabrikasi pekerja — provenance lajur jujur. Remediasi: ganti URL
  saudara yang hidup dan memuat klaim yang sama (verifikasi 200 + isi), catat di
  ruling. Jangan vonis pekerja berdasar kematian tautan hulu tanpa cek CDX.
- **Flaky alat verifier sendiri:** probe burst memicu timeout CDX + 429
  self-throttle → baris sampling jadi NEEDS_REVIEW, bukan FAIL. Jeda antar-probe;
  rerun bisa pulih (snapshot arsip ikut pulih). Bedakan tegas 'cacat artefak' vs
  'cacat alat ukur' di laporan.
- **Konflik definisi antar-kartu** (kartu VS vs kontrak desain TA, mis. '90 hari'
  = 12-13 minggu vs 9x7x3 jam): naikkan sebagai putusan user dengan opsi
  berangka + condong controller beralasan (permintaan mentah user = bobot
  tertinggi). Jangan controller sahkan deviasinya sendiri (rule kontrak desain
  anti-drift), dan jangan biarkan FIX menyentuh butir itu sampai putusan turun.
  Cacat teks nyata di sekitarnya (mis. 'minggu ke-13' di playbook 9 minggu) tetap
  jalan apa pun putusan.
- **Timeout serentak pada fan-out lajur** (semua lajur berangkat bersamaan
  menabrak RUN_TIMEOUT_MS 1800s): cek `raw/<lajur>/` sebelum memutuskan nasib —
  run pertama sering mati tepat sebelum menulis berkas lajur padahal cache sumber
  matang; retry biasanya cukup. Intervensi kartu tulis-dari-raw hanya bila retry
  kedua timeout tanpa artefak. Run verifikasi yang timeout pun kerap meninggalkan
  INSTRUMEN matang (skrip check + probe) yang tinggal dijalankan ulang.
