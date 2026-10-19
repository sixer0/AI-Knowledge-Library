# Operasional Misi Lajur Riset -> Buku (preseden PROMANUAL-1004, 04-10)

Pola teruji dari misi riset multi-lajur yang berlanjut produksi buku (dekomposisi RT/TA ->
12 sub-lajur akuisisi -> analisis/rekonsiliasi -> vonis verifier -> agregat -> sintesis ->
blueprint buku -> tulis berantai). Melapis `saturation-gate-sweep-lanes.md` (norma vonis) dan
`saturation-sweep-mission-frame.md` (kerangka misi); berkas ini hanya operasional mekanik.

## 1. Watcher latar: parser `show --json` dan ambang selesai

- Bentuk keluaran `hermes kanban show <id> --json`: `{task:{...}, parents:[], comments:[], ...}`.
  `status` ada di `["task"]["status"]`, `parents` di LEVEL ATAS. Parser yang membaca
  `json.load(...)["status"]` menghasilkan `?` SENYAP.
- Bahayanya (kejadian nyata 04-10): loop bash memperlakukan `?` sebagai "bukan ready/running"
  -> vonis "settled" PALSU dalam hitungan detik padahal kedua kartu masih jalan. Aturan:
  watcher WAJIB memvonis status TAK DIKENAL (`?`) sebagai AKTIF (lanjut menunggu), bukan selesai.
- Resep watcher sah: skrip python kecil di terminal(background=true, notify_on_complete=true),
  baca `["task"]["status"]`, bandingkan hanya terhadap himpunan aktif eksplisit
  {ready, running, todo}, cetak hanya saat keadaan berubah (hemat log), window 3-8 jam lalu
  re-spawn saat wake. Ini menggantikan polling manual berulang antar-giliran.

## 2. Builder kartu batch: guard `__main__` (akar tabrakan duplikat)

- Kejadian nyata 04-10 (D-11 kontrak): modul builder kartu (berisi loop `create(...)` di
  LEVEL MODUL) di-import dari giliran inline lain untuk memakai konstantanya -> SEMUA blok
  create tereksekusi ulang -> 4 kartu duplikat lahir saat set kanonik sudah done.
- Aturan: modul builder yang dipakai ulang (konstanta lingkup, perender body) WAJIB menaruh
  seluruh pemanggilan create di bawah `if __name__ == "__main__":`; pemakaian import-only
  tidak pernah menyentuh papan. Alternatif aman untuk 1-2 kartu: panggilan `lad_card.py`
  langsung via subprocess, tanpa modul perantara.
- Pemulihan duplikat (protokol sudah terbukti): set lebih dulu & lebih maju = kanonik;
  duplikat berstatus ready tanpa run diberi komentar jejak -> `archive`; akar + jejak id
  masuk Decision Log. Window anti-duplikat tetap <2 menit antara baca papan dan create.

## 3. Register beku dengan pembaca paralel: addendum + refreeze append-only

- Masalah: kartu fix (menutup GAP sintesis) butuh menambah klaim ke register beku yang
  SEMENTARA ITU dibaca serentak oleh kartu lain (sintesis, blueprint, penulis bab). Sunting
  langsung = tabrakan tulis + sha16 yang sudah dikutip berkas hilir jadi bohong.
- Protokol (putusan D-15, layak jadi norma kelas ini):
  1. Kartu fix TIDAK menyentuh `research/<L>/register-beku.md`. Klaim baru ditulis ke
     `research/FIX/<KARTU>/addendum-KL.md` (format baris kanonis + ladder + korpus).
  2. SATU kartu refreeze (assignee analyst) menggabungkan semua addendum sah secara
     append-only: validasi baris dulu (URL hidup, entity-match, tanda asal; baris cacat
     ditolak dengan alasan), nomor melanjutkan, kolom rujukan menyebut kartu fix asal.
  3. Terbitkan sha16 baru per lajur tersentuh + `REFREEZE-LOG.md` (tabel LAMA->BARU, ID
     baru, waktu) + backup `.pre-refreeze.bak`; verifikasi diri = diff nol-suntingan-lama.
  4. Berkas hilir (specs/blueprint) TIDAK disunting cetakan sha16 historisnya; cukup catatan
     menunjuk REFREEZE-LOG. Rantai tulis berawal dari kartu refreeze (edge parent), sehingga
     penulis bab otomatis membaca sha16 terbaru.

## 4. Kartu resume: SISA_KERJA dari komentar induk

- Enam bidang laporan partial-handoff tinggal di KOMENTAR kartu (`show --json` -> `comments`,
  cari bidang SISA_KERJA), bukan hanya di `result` yang terpotong. Body kartu resume wajib
  memerintahkan: `hermes kanban show <induk> --json` lalu baca komentar, DAN lanjut penomoran
  register dari berkas (cacah baris KL terakhir diukur, bukan dipercaya dari narasi).
- Mata-3 (rantai maksimum): fokus HANYA residu yang disebut mata-2; hasil penutupan sah =
  VONIS JENUH PENUH atau PARTIAL-CAPPED dengan ledger claim (permohonan putusan ke controller,
  preseden D21). Controller memvonis terima/tolak di Decision Log dengan alasan angka; residu
  lajur yang tumbuh diberi label PARTIAL + resweep terjadwal (norma S3), bukan mata-4 paksa.

## 5. Dispatch gelombang riset besar

- Buat SELURUH DAG sekaligus (norma gelombang N1: batch creation sah; kap menghitung RUNNING
  per misi), edge HANYA ke hulu data nyata. Rantai sengaja untuk menegakkan kap ditulis eksplisit
  di kontrak (mis. gelombang sensus menunggu gelombang teknik selesai = edge kap, bukan data -
  catat supaya audit tidak membacanya sebagai edge semu).
- Direktif lajur (`worker-offensive-logic.md`, `saturation-gate-sweep-lanes.md`, RULE
  PRESISI-HASIL) ditempel UTUH ke body kartu lewat skrip pembuat yang membaca berkas rujukan
  saat create - bukan diringkas, bukan sekadar menunjuk nama skill.
- Vonis verifier FAIL pertama pada suatu kelas jalur (mis. kelas-8 diklaim tanpa akun render)
  adalah bukti gerbang bekerja, bukan anomali: kartu remediasi memuat DUA jalur penutupan sah
  (jalankan jalur sungguhan ATAU sunting vonis jadi N/A ber-bukti - dan syaratkan minimal satu
  eksekusi nyata sebelum boleh memilih N/A), lalu re-vonis oleh verifier lain (penulis != verifier).
- Sinkron tabel kontrak: skrip idempoten regex per id kartu (`| \`t_x\` | ... | <status> |`)
  lebih tahan daripada patch manual, karena pengawas silang/bridge bisa menyunting CONTRACT.md
  di antara giliran (peringatan "modified since read" = normal; baca ulang sebelum tulis).
