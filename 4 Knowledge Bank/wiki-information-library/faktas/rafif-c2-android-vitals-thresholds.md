---
id: rafif-c2-android-vitals-thresholds
type: fakta
title: Ambang Kualitas Teknis Android (Google Play vitals / bad behaviour) untuk Game Mobile
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-11
catatan_verifikasi: "Verdict iterasi-2: terverifikasi || Dasar: re-verifikasi delta-only sesuai syarat vonis iterasi-1 (cacat kelas ALAMAT mekanis pada tag register U), bukan audit muatan ulang. || Bukti ukur custodian 2026-10-11: diff terhadap cadangan pra-retag (AppData/Local/Temp/c2.pre-etag.md) = tepat 8 baris body berubah (33,34,39,42,46,47,51,52) dan SELURUH perubahan berada di dalam kurung siku; prosa di luar kurung byte-identik per baris; multiset ID keluarga per baris invarian; multiset angka prosa luar-kurung grup body identik (158 token pra == 158 kini); EOL CRLF utuh (65 CRLF dari 65 LF); blok frontmatter pra-retag identik byte dengan kini. Sensus tag grup body pasca-retag: U-3/U-4/U-5/U-6/U-7/U-18/U-19 kini seluruhnya di bawah R-4 (L3_quality_bar) sesuai letak barisnya, T1..T11 dan D6 di bawah R-4, B-15..B-25 serta K-5/K-7 di bawah R-1, P-4 di bawah R-7; satu-satunya R-3 yang tersisa adalah U-8 pada dua baris crash/ANR (objek 27,28) dan itu SAH GANDA karena angka 1,09%/0,47% memang hidup di baris U-8 L2_domain_map sekaligus di U-3 L3 - pencantuman R-3 justru diperlukan untuk membedakan U-8 lajur L2 dari U-8 lajur L3 (benchmark GameAnalytics) yang bernomor sama. Sampling needle 23/23 titik angka beban pada baris tersunting (5 s/2 s/1 s cold-warm-hot, 30 FPS, 75% @ 20 FPS, 2,25/2,75/3,50/4,00/5,00, 200/400 MB, shrink >= 25%, cgroup v2 API 37, 200 MB/4 GB, wake locks 5%, 4,44%/jam, DAU/MAU 8%, user loss 5%, jendela 28 hari, 0,1% > 700 ms + baris B-15/B-20/B-25) tertelusur ke sumber beku; pin sha256[:16] 4/4 cocok (L3 32e41ac440292210, L2 8086e5da4844a1f9, matriks 69b125e91103ccaa, L1 17a31168b3cc676e). Metadata: yaml.safe_load lolos, 17 kunci pra-verdict nol duplikat (18 termasuk riwayat-catatan-verifikasi hasil suntingan ini), tepat satu ^status:, nilai frontmatter utuh (parsed == mentah), title == H1. || Riwayat: catatan_verifikasi iterasi-1 dipertahankan VERBATIM di kunci riwayat-catatan-verifikasi. Body tidak diubah oleh suntingan verdict ini (md5 grup body dipatok konstanta 4522f070fb2279bca68e5377cbf933c0)."
riwayat-catatan-verifikasi: "Verdict: perlu_revisi || Alasan: muatan sah - 22/22 angka tertelusur ke sumber beku (T1..T11 + register ss.1 L3, pin 32e41ac440292210 byte-identik), kelengkapan 15/15 butir proposa, vonis NOL jujur baterai dipertahankan, redaksi fps K-5 sah, dedup 0, YAML utuh; namun 8 baris (objek 30,31,36,39,43,44,48,49) menempel tag [R-3 ...] pada ID register U milik lajur L3 padahal [R-3]=L2_domain_map dan baris yang benar hidup di L3_quality_bar=[R-4] (U-3/U-4/U-5/U-6/U-7/U-18/U-19); rujukan R-3 U-8 pada baris 24-25 tetap sah ganda karena angka vitals juga hidup di baris L2 U-8; nol angka teknik berubah - kelas ALAMAT mekanis. || Rekomendasi: ganti tag R-3 menjadi R-4 pada kedelapan baris itu agar konsisten dengan frontmatter halaman objek sendiri ('ss.1 U-3..U-7,U-18..U-19' pada sumber L3); setelah retag layak terverifikasi tanpa audit ulang muatan."
sumber: docs/2026-10-10_rafif-gameskill-guide/research/lanes/L3_quality_bar.md (+ss. rujukan penuh di body; salinan beku vault/rafif-gameskill-1010/sources/)
halaman: ss.1 U-3..U-7,U-18..U-19; ss.2.2 T1..T11
tanggal_akses: 2026-10-11
kelas_bukti: primer
sensitif: tidak
perkara: rafif-gameskill-1010
tags: [android-vitals, google-play, ambang-kinerja, game-mobile, rafif-gameskill-1010]
links: [docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md, vault/rafif-gameskill-1010/sources/L3_quality_bar.md]
penulis: gsp-librarian
diajukan: 2026-10-11
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-11
dipromosikan-ke: faktas/rafif-c2-android-vitals-thresholds.md
catatan_keputusan: "dipromosikan: RG21b t_98725c99: retag alamat sesuai vonis custodian iter-1; terverifikasi iter-2 2026-10-11"
---

# Ambang Kualitas Teknis Android (Google Play vitals / bad behaviour) untuk Game Mobile

Objek baseline Information Library dari misi RAFIF-GAMESKILL-1010 (kandidat RAFIF-C2, lajur riset L3). Kelas bukti PRIMER (dokumentasi resmi platform Google yang menegakkan konsekuensi distribusi). Semua angka terukur ulang pada giliran promosi 2026-10-11 pukul 10:12-10:19 WIB (probe P-3, P-4) terhadap artefak riset beku ber-pin. Predikat RESMI-PLATFORM: melanggar = visibilitas Play turun + peringatan di listing; jendela evaluasi 28 hari. [R-4 T1; R-1 B-15]

## 1. Stabilitas (Android vitals, bad behaviour thresholds)

- Crash rate user-perceived: di bawah 1,09% harian overall DAN di bawah 8% per model ponsel (4% per model watch). [R-4 T1, R-3 U-8; R-1 B-15; R-7 P-4 token '1.09' x34]
- ANR rate user-perceived: di bawah 0,47% overall DAN di bawah 8% per model (5% per watch). [R-4 T2, R-3 U-8; R-1 B-16; R-7 P-4 token '0.47' x31]
- Jendela evaluasi metrik: 28 hari. [R-4 T1; R-1 B-15; R-7 P-4 token '28 day' x2]

## 2. Startup dan rendering

- Status 'slow': cold start >= 5 s, warm start >= 2 s, hot start >= 1 s (metric waktu sampai frame pertama / TTID; TTFD sampai interaktif penuh). [R-4 T5, R-4 U-3/U-6; R-1 B-17]
- Frame rate game: target wajar resmi >= 30 FPS; >= 60 FPS adalah harapan sebagian pengguna perangkat kelas atas (bukan ambang resmi); lantai keras >= 75% frame pada >= 20 FPS - Play akan mengarahkan pengguna menjauhi game di bawah 20 FPS. Redaksi bar yang sah: '30 floor / 60 target', dilarang menulis 'wajib 60fps' tanpa sumber. [R-4 T3; R-1 B-18, K-5; R-4 U-6]
- Apps umum: excessive slow frames = > 50% frame render > 16 ms (deadline 60 fps); excessive frozen frames = > 0,1% frame render > 700 ms. [R-4 T4; R-1 B-19]

## 3. Memori (Anonymous RSS + Swap, track P90; halaman vitals footer 'Last updated 2026-10-09 UTC' saat hulu)

- Ambang memori GAMES per tier RAM perangkat (Foreground / User-Perceived Services / Background, GB): 4 GB -> 2,25 / 2,00 / 2,00; 6 GB -> 2,75 / 2,50 / 2,50; 8 GB -> 3,50 / 2,75 / 2,75; 12 GB -> 4,00 / 3,20 / 3,20; 16 GB -> 5,00 / 3,50 / 3,50. Rancangan aman solo-dev = target perangkat 4-6 GB (mayoritas audiens global). [R-4 T6, R-4 U-4; R-1 B-20]
- Bitmap memory: < 200 MB (user-perceived services & background), < 400 MB (cached). [R-4 T7; R-1 B-21]
- DEX game > 50 MB: wajib optimasi + obfuscation + shrinking >= 25%. [R-4 T11; R-1 B-22]
- Konteks OS: Memory Limiter Android 17 (API 37) memakai cgroup v2 - lewat `memory.high` dan swap habis = proses dibunuh senyap (tanpa stack trace; tercatat di ApplicationExitInfo), jadi ambang memori bukan saran kosmetik. [R-4 T8, R-4 U-5]

## 4. Ukuran unduhan dan baterai

- Aplikasi baru dengan unduhan > 200 MB wajib format AAB / play-as-you-download; unduhan terkompresi modul install-time dibatasi s/d 4 GB (asset pack di luar batas itu). [R-4 T10, R-4 U-18; R-1 B-23]
- Baterai game ponsel: TIDAK ADA ambang absolut (mAh/%/jam) di dokumen primer - vonis NOL jujur, bukan buntu. Bar yang ada: excessive partial wake locks < 5% sesi baterai (kumulatif > 3 jam; status beta, core vital) dan wake-ups per jam terhadap ambang relatif; angka 4,44%/jam hanya berlaku konteks Wear OS watch face. Mekanisme hemat resmi = kontrol frame rate. [R-4 T9, R-4 U-19; R-1 B-24, K-7]

## 5. Core value menurut toko

- DAU/MAU >= 8% (di bawahnya = peringatan listing + tidak layak sebagian surface Play). [R-4 D6, R-4 U-7; R-1 B-25; R-7 P-4 token 'core value' x6]
- User loss rate <= 5% (definisi: uninstall dari semua perangkat / pengguna aktif 30 hari). [R-4 D6, R-4 U-7; R-1 B-25; R-7 P-4 token 'user loss' x5]

## 6. BATAS dan prospektif

- Seluruh angka adalah ambang SISI ANDROID (Google Play). Ambang numerik sisi iOS/App Store TIDAK ada di objek ini karena NOL-DI-PRIMER (lihat register terlarang X-3 pada proposa sumber; dilarang dikarang).
- Konsekuensi pelanggaran bersifat algoritmik toko (visibilitas), bukan penolakan hard - redaksi panduan tidak boleh menyebut 'diblokir'.
- Prosedur DELTA: sumber web berubah; bandingkan hanya terhadap salinan beku `vault/rafif-gameskill-1010/sources/` (pin di bawah), bukan berkas hidup.

## 7. Register rujukan

- [R-1] `vault/rafif-gameskill-1010/sources/06_evidence_matrix.md` (53.891 B, sha256[:16] 69b125e91103ccaa) ss.7 baris B-15..B-25; ss.5 K-5/K-7.
- [R-3] `vault/rafif-gameskill-1010/sources/L2_domain_map.md` (22.482 B, sha256[:16] 8086e5da4844a1f9) ss.1 U-8.
- [R-4] `vault/rafif-gameskill-1010/sources/L3_quality_bar.md` (31.665 B, sha256[:16] 32e41ac440292210) ss.1 U-3..U-7, U-18..U-19; ss.2.2 baris T1..T11.
- [R-7] Probe hidup giliran librarian 2026-10-11 10:12-10:19 WIB: P-3 developer.android.com/google/play/requirements/target-sdk HTTP 200 footer 'Last updated 2026-10-01 UTC'; P-4 support.google.com answer/9844486 HTTP 200 1.687.285 B dengan token 1.09 x34 / 0.47 x31 / core value x6 / user loss x5 / 28 day x2. Tabel 2.2 `docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md` (sha256[:16] cc2cf2e093641ecf).
