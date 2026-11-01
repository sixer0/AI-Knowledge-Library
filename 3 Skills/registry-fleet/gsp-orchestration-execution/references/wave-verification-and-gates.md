# Wave verification, cap rotation, dan gerbang deterministik controller

Dipakai penuh di HDKCOMP-0929 (12 gelombang verifikasi V01-V12 atas 48 perusahaan) dan pola
timeout-triase berulang di misi mobile 28-09 (C1, V03, V07). Semua terverifikasi berjalan.

## 1. Instantiate gelombang dari peta (bukan dari perkiraan)
- Tahap merge/analyst menulis `WAVE-MAP.md` + `batch-NN.csv` (populasi dipartisi tetap, mis 4 perusahaan/gelombang, `n = ceil(U/4)`).
- Controller membaca WAVE-MAP dengan parser, lalu membuat kartu V per baris peta (assignee PERSIS dari peta; jangan tukar tipe profil sendiri).
- Body kartu wajib menempel: skema kolom target, syarat jejak (tabel VERIFIKASI-AKURASI per field + LADDER per rung), larangan percaya CSV hulu apa adanya, dan FLAG register dari merge yang harus diuji eksplisit.

## 2. Cap rotasi (puncak running + per tipe profil)
- Saat instantiate serentak, langsung block ekor antrean dengan pesan berisi ALASAN + KRITERIA unblock ("saat ada V terminal"). Notifikasi block dari kartu ini = GEMA putusan sendiri: cek papan, laporkan 'tidak ada aksi sah', jangan unblock dini.
- Tiap gelombang terminal: buka SATU antrean tipe yang slotnya kosong; jaga maks 2 paralel per tipe profil dan puncak <=5. Bila antrean terakhir bertipe sama dengan slot penuh, TAHAN walau puncak masih longgar (kasus V11 crawler ditahan saat slot crawler penuh dua).
- Dispatcher kadang melepas semua ready serentak melewati cap — biarkan berjalan satu giliran bila modal sehat (jangan potong kerja hidup), lalu tegakkan cap untuk gelombang berikutnya.

## 3. Triase timeout kartu verifikasi/gelombang
Urutan tetap: UKUR DISK dulu, jangan re-dispatch buta, jangan pecah kartu pada timeout pertama.
- `ls verification/` + baca komentar pekerja. Modal = CSV hasil sudah ada tapi laporan/jejak VERIFIKASI belum -> DIAMKAN, dispatcher retry akan memanen (terbukti: V03 run-2, V07 run-2, C1 run-2 — ketiganya complete tanpa aksi controller; ukuran md naik setelah retry = bukti run-2 menambah jejak, bukan asal tutup).
- Ambang pecah kartu = timeout KEDUA tanpa artefak apa pun (preseden W12: beban baca desain kartu, akar di body bukan worker).

## 4. Gerbang deterministik dijalankan controller SEBELUM kartu hilir
- **Agregat V:** parser seragam atas seluruh `hasil-V*.csv` (total baris == populasi register, nama unik == populasi, cocok dua arah dengan komposisi kelas merge). Terima variasi nama jejak (`hasil-Vnn.md`, `hasil-Vnn-VERIFIKASI.md`, `VERIFIKASI-Vnn.md`) — pola glob, bukan satu nama kaku.
- **Linkcheck:** v1 naif memvonis 10 'mati' PALSU karena sel multi-URL ('a ; b') dibaca satu string (InvalidURL). Resep benar: pisahkan per `;`, probe PER-URL, vonis sel MATI hanya bila SEMUA URL sel gagal; simpan cetakan per-URL (`LINKCHECK.json`). 403 terhadap UA datacenter (pro.sony) bukan mati substansi bila jalur regional/arsip sudah memverifikasi — laporkan dengan catatan metode.
- Kartu hilir (SYN/laporan) baru DIBUAT setelah angka agregat + linkcheck nyata; body SYN menempel angka gerbang hasil ukur, putusan controller (Q-nn), dan syarat scanner keluaran.

## 5. Pitfall alat ukur controller (terjadi & tertangkap sendiri)
- awk `-F','` atas CSV berkoma-dalam-kutipan => false positive 'URL-MATI'. Wajib `csv.DictReader`.
- Kunci kolom status heuristik bisa meleset (`verification_status` tak ada; nyata di `last_verified`) — cetak daftar kolom dulu, lalu hitung.
- Angka laporan pihak lain = klaim sampai diukur ulang (aturan terkait butir 9). Uji tandingan Section A pasca-SYN menemukan 47 vs 48 = entri barred terdisklosi (bukan cacat) — rekonsiliasi semacam ini wajib dijelaskan ke user, bukan dianggap salah-hitung atau dilewat.

## 6. Mirror repo pasca-misi (kebijakan standing user)
- Salin folder misi ke `hermes-home/workspace/docs/<misi>` dengan eksklusi cache mentah: direktori `raw/`, `_*probe*`, `__pycache__`, file >2MB (apk). Preseden misi panduan GEN-2.
- `git add -f` log kunci yang dibutuhkan bukti (mis. UTILISASI pass, log dua-run identik-byte) karena gitignore repo menolak `*.log`; sisakan yang lain.
- Sisip CHANGELOG via skrip byte-level CRLF-safe (baris setelah header `|------|`), bukan patch teks (raw repo CRLF). Scan staged diff terhadap pola secret (api[_-]?key|ghp_|sk-|AKIA) — harus 0. Push lalu verifikasi `git ls-remote origin HEAD` == `rev-parse HEAD`.
- Jangan pernah mengandalkan pipeline `| tail` untuk exit code git (exit melapor status tail).
