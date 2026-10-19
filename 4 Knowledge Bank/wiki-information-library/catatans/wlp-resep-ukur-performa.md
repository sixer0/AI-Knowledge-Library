---
id: wlp-resep-ukur-performa
type: catatan
title: Resep ukur performa WebUI apples-to-apples (misi WLP)
status: active
sumber: docs/2026-09-05-webui-long-transcript-perf/checkpoints/CP-F23-rewalk.md
halaman: §2; CP-F15 §3; CP-F17 kepala; CP-F18 CHECK 2
tanggal_akses: 2026-09-07
kelas_bukti: primer
sensitif: tidak
perkara: wlp
tags: [webui, performa, protokol-ukur, playwright, wlp, brahma]
links: [wlp-angka-outline-window, wlp-pelajaran-blind-spot-instrumen, wlp-fakta-pendaratan-statik]
penulis: gsp-librarian
diajukan: 2026-09-07
revisi-oleh: gsp-librarian
revisi-pada: 2026-09-07
catatan_revisi: "Revisi sesuai vonis custody t_126d0f03 oleh giliran librarian berbeda (kartu t_898e0257): (1) butir 1.1 - dasar satuan keempat kelas sesi disebut eksplisit per kelas sesuai tabel CP-F3 par.2; XL pasca-jalur-bare 4894, stored 4893. (2) Butir 3.1 - n=7 kelas XL tercapai di F17 (retry-verified) dan dikonfirmasi ulang di F18. (3) Penomoran seksi body dirapatkan dari 4 menjadi 3. Non-hambatan: kolom enc di CP-F17 dijelaskan dan rujukan deklarasi identitas metode ditegaskan ke CP-F23 par.2. Status tetap perlu_revisi; kenaikan ke terverifikasi wewenang custodian pada kartu recheck."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-07
catatan_verifikasi: "Verdict: terverifikasi. Alasan spesifik: revisi librarian di kartu t_898e0257 sudah memperbaiki tiga butir vonis ronde-1 sesuai sumber primer yang saya cek sendiri: (1) A21 dasar angka XL SHORT 52 tersimpan tanpa bare; MEDIUM 1694, LONGP 2701, XL 4894 pasca-jalur-bare; XL stored = 4893 (CP-F3-base.md par.2 tabel kelas); (2) A22 waktu XL n=7 tercapai di F17 (retry-verified) dan dikonfirmasi ulang di F18 (CP-F17-smokebench.md par.2 + CP-F18-veraccept.md CHECK 2); (3) penomoran seksi body sekarang berurutan 1-2-3. Perbaikan non-hambatan juga terverifikasi: kolom `enc` dijelaskan sebagai `encodedBodySize` (CP-F17 tabel + CP-F23 par.2) dan klaim identitas metode dirujuk ke CP-F23 par.2. Uji regresi terhadap cakupan ronde-1 (protokol >=7 sampel, F15 7/7, F18 8/8, flag route-intercept + settings mtime, GET-only, gerbang md5, EOL blob LF 8a210d8f vs disk CRLF 4d396b43) tetap tersedia; tidak ada substansi sah yang hilang. Status diangkat menjadi terverifikasi; promosi ke wiki wewenang librarian."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-07
dipromosikan-ke: catatans/wlp-resep-ukur-performa.md
---

# Resep ukur performa WebUI apples-to-apples (misi WLP)

1. Isi resep

1.1 Protokol baseline: empat kelas sesi dengan satuan `S.messages.length` pasca-fetch jalur yang dilaporkan (definisi sumber CP-F3 par.2), dasar disebut eksplisit per kelas: SHORT 52 (semua pesan tersimpan, tanpa truncation; tidak ada jalur bare), MEDIUM 1694 dan LONGP 2701 serta XL 4894 (pasca-jalur-bare; stored/message_count XL = 4893). Diukur per arm dengan target minimal 7 sampel valid per sel (arm x kelas). Preseden: protokol par.9.8 minta >= 7 sampel/ukuran [R-1]; instrumen tertambal F15 mencapai 7/7 valid nol discard [R-2]; vonis acceptance F18 mencatat 8/8 sel att=7 valid=7, discard/error/contamination nol [R-3].

1.2 Alat ukur biaya transfer: resource-timing `encodedBodySize` browser (kolomnya dicetak sebagai `enc` di tabel CP-F17; nama field resminya dideklarasikan eksplisit di CP-F23 par.2), dijumlahkan per fase interaksi (enc_sum). Deklarasi identitas metode antar keadaan ada di CP-F23 par.2: metode yang sama persis dengan baseline OFF F17 dan angka cacat F19, sehingga delta antar keadaan apples-to-apples [R-4][R-5][R-6].

1.3 Arm ON/OFF tanpa menyentuh konfigurasi user: flag produk (`wlp_cv_rows`, `wlp_outline_window`) di-arm lewat route-intercept `/api/settings` per konteks browser (make_context flags), bukan lewat settings.json. Bukti kepatuhan lintas tiga giliran kartu: mtime `settings.json` tetap 2026-09-06 02:44:49 [R-4][R-5][R-6]. Semua permintaan alat adalah GET; nol POST/nol mutasi data sesi [R-5][R-6].

1.4 Gerbang buka sebelum mengukur (prasyarat validitas delta): `md5(body GET /static/outline.js) == md5(berkas DISK checkout serve)` dicetak segar oleh skrip prereq sebelum satu pun sampel diambil; baris sumber kunci (mis. 446) dibaca dari badan terserve, bukan dari repo [R-6][R-7]. Tanpa gerbang ini, delta bisa mengukur berkas yang salah (lihat objek pelajaran pendaratan statik).

1.5 Catatan pembanding EOL: dengan `core.autocrlf=true` + `.gitattributes * text=auto`, blob git tersimpan LF (md5 8a210d8f...) sedangkan berkas disk/terserve CRLF (md5 4d396b43...); pembanding yang benar selalu body terserve vs berkas DISK [R-7][R-8].

2. Register rujukan

- R-1: docs/2026-09-05-webui-long-transcript-perf/checkpoints/CP-F3-base.md, DEV-1 (par.9.8 >= 7 sampel/ukuran; tabel kelas §2).
- R-2: checkpoints/CP-F15-instr.md §3 (perintah --n-valid 7; hasil valid 7/7 attempt 7/7).
- R-3: checkpoints/CP-F18-veraccept.md CHECK 2 (8/8 sel att=7 valid=7).
- R-4: checkpoints/CP-F17-smokebench.md kepala dokumen (instrumen, flag ON via route-intercept, settings mtime; kolom `enc` pada tabel §1) dan checkpoints/CP-F23-rewalk.md par.2 (deklarasi eksplisit metode ukur identik dengan baseline OFF F17).
- R-5: checkpoints/CP-F19-walk.md §3 (metode probe; route-intercept; GET only) dan §5 (angka cacat).
- R-6: checkpoints/CP-F23-rewalk.md §2 (deklarasi eksplisit metode ukur identik dengan baseline OFF F17 dan keadaan cacat F19) dan §5 (kepatuhan).
- R-7: checkpoints/CP-F21-reverify.md §1 G1 dan §3 (gerbang md5 body==disk; EOL).
- R-8: checkpoints/CP-F22-cherrypick.md §3 (baris blob LF vs disk CRLF).

3. Batas berlaku

3.1 Resep ini terverifikasi pada WebUI Brahma serve :9012 dengan sesi beku kelas wlp_lib dan instrumen harness wlp-f6a/f15/f17/f23; angka slope/waktu render tidak ikut dipromosikan di objek ini karena n=7 untuk kelas cacat XL baru tercapai di F17 (retry-verified, CP-F17 §2) dan dikonfirmasi ulang di F18 [R-3], serta framing klaim E1 masih NEEDS_REVIEW (CP-F7 CHECK 6). Kelas sesi lain atau mesin lain wajib rekalibrasi ambang discard sebelum angka dipakai.
