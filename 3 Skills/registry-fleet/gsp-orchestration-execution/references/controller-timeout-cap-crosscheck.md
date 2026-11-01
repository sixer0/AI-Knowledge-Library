# Pola controller: triase timeout, rotasi cap, uji-tandingan agregat, pitfall parser audit
(Dirangkum dari misi mobile 0928, HDKCOMP-0929, misi visual 0929 — 29-09-2026)

## 1. Triase timeout: ukur modal sebelum memutuskan (jangan pernah re-dispatch buta)
Saat kartu timeout dan dispatcher retry naik, triase dulu state disk, lalu pilih salah satu dari tiga:
- **Modal nol artefak** (belum ada berkas keluaran sama sekali): biarkan retry jalan SATU kali; timeout kedua tanpa artefak = PECAH lingkup kartu (preseden W12 -> W12-C/D; akar sering beban baca body kartu, bukan kemalasan worker — cek apakah body memerintahkan buka banyak berkas besar).
- **Modal parsial** (artefak sebagian + scratch/cache persisten, mis. `hasil-V03.csv` yatim tanpa laporan): JANGAN sentuh — dispatcher retry akan take-over dan memanen (preseden C1, V03, V07, A1, A4: SEMUA menutup via run-2 tanpa aksi manual; run-2 tinggal verifikasi + closure, kadang menambah jejak ±600 B yang terukur).
- **Modal lengkap tapi kartu menggantung running** (pekerja mati pasca-menulis): unblock agar worker/penutup merapikan closure (preseden L9-B, REM-UTIL).
Ambang pecah-kartu = timeout KEDUA tanpa modal, bukan pertama. Timeout pertama dengan modal kaya = non-kejadian.

## 2. Cap rotasi (puncak ≤5, maks 2 paralel per tipe profil) — tafsir yang benar
- Cap adalah **rem pelepasan kartu baru, bukan kill-switch kerja berjalan**. Lane yang sudah running sehat di atas cap: biarkan jalan (memutus kerja sehat membakar modal); cukup jangan lepas gelombang berikutnya. Preseden L9/L17 + misi visual A1-A4.
- Saat dispatcher melepas N kartu `ready` serentak: block kelebihan dengan pesan berisi **pemicu unblock eksplisit** ("slot <tipe> penuh; menyusul saat <X> terminal"). Notifikasi block berikutnya = gema putusan sendiri; jawab dengan ukur papan, tanpa aksi.
- Rotasi: tiap lane terminal, buka kartu antrean yang cocok **tipe slot yang kosong** (bukan urutan nomor mentah) agar komposisi selang-seling terjaga; kalau satu tipe penuh dan antrean hanya berisi tipe itu, TAHAN meski puncak masih longgar (kasus V11 vs slot collector kosong).
- `hermes kanban block` hanya sah pada kartu ready/running; kartu todo tertahan rantai menolak block dan memang tidak perlu.

## 3. Uji-tandingan controller atas angka agregat (anti-halusinasi, pra-SYN)
Sebelum menerima laporan hasil merge/sintesis, hitung ulang dengan parser INDEPENDEN atas sumber mentah (bukan membaca angka kartu):
- Rekonsiliasi selisih populasi sampai ke entitasnya. Kasus nyata: laporan 47 vs register 48 = satu entri barred (nama legal tak tercetak di sumber resmi) yang DIDISKLOSIKAN eksplisit — sah; selisih tanpa disklosi = cacat.
- Selisih kelas kecil (Adjacent 6 vs 5) boleh teridentifikasi sebagai artefak hitung entri barred, asal sisi terbit (Section B/C) tidak terpengaruh.
- Kalau klaim worker menyebut angka berbeda dari body kartumu sendiri (68 vs 64 karena append antar-waktu), body-mu yang basi — koreksi diterima bila parser worker membukukan bijeksi.

## 4. Pitfall parser audit (terbukti berulang, semua salah controller, semua tertangkap)
- **Delimiter manifest tidak seragam antar-pekerja** meski nama kolom sama: A1/A2 pipe, A3 TAB. Deteksi per-berkas (`head -2` dulu), jangan warisi asumsi segmen sebelumnya.
- **awk -F',' pada CSV ber-kutipan = false positive** ('URL-MATI' palsu untuk Hikvision dkk karena koma dalam kutipan). Selalu `csv.DictReader`.
- **Sel multi-URL** ("a ; b" dalam satu sel) WAJIB di-split per `;` sebelum linkcheck; vonis mati hanya bila SEMUA URL dalam sel gagal. Versi naif menghasilkan 10 kematian palsu dari 48 sel (hasil sebenarnya 47/48 hidup).
- Grep pola error (`404`, `FAIL`) menangkap substring di dalam sha256 — anchor ke kolom, bukan whole-line.
- Temuan non-judul di hulu (baris katalog 'register-studio', 'daftar agregat Wikipedia', seller-mismatch alias penerbit sah) = cacat mutu yang lolos gerbang lama karena audit menghitung nama unik, bukan menguji tiap nama; nyatakan eksplisit ke verifier hilir, jangan tambal diam-diam.

## 5. Operasio repo (gsp-agent) saat mirror misi
- `.gitignore` menolak `hermes-home/**/*.log`: log kunci hasil (verifikasi dua-run, utilisasi) butuh `git add -f`; cache probe HTML per-gelombang (`_vNN_scripts/probe|pages`, `_probe*`) di-unstage via `git restore --staged --` + daftar berkas (non-destruktif) agar repo tidak membengkak 100 MB+.
- CHANGELOG repo ber-CRLF: `patch` tool bisa gagal match; resep andal = skrip python `raw.split(b'\r\n')`, sisip setelah baris `|------|` header tabel, tulis ulang join CRLF.
- Gerbang persetujuan menolak perintah destruktif (`find -exec rm -rf`) yang timeout tanpa respons user: JANGAN sirkumvensi; ubah tujuan jadi non-destruktif (unstage cukup; file mirror sisa tidak menghalangi commit).
- Substitusi inline kompleks `$(grep -n ...)` dalam terminal memicu hardline 'malformed payload': tulis helper python ke Temp lalu jalankan via uv — selalu jalur andal.
- Scan secret staged diff sebelum commit: pola `(api[_-]?key|ghp_|sk-[A-Za-z0-9]{20}|AKIA..)` di `git diff --cached`, vonis hanya pada literal, laporkan angkanya. Push lalu verifikasi `git ls-remote origin HEAD` == `git rev-parse HEAD`.

## 6. Etika jawaban notifikasi gema
Notifikasi block/timeout yang merujuk putusan controller sendiri dijawab dengan: ukur papan segar + konfirmasi 'keadaan persis desain' + nol aksi. Jangan pernah membuat kartu baru dari notifikasi status (instruksi otomatis eksplisit melarang re-dekomposisi).
