---
id: rafif-c3-store-economy-compliance-2026-10
type: fakta
title: Ekonomi dan Kepatuhan Toko Aplikasi (Google Play / Apple) per Oktober 2026
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-11
catatan_verifikasi: "Verdict: terverifikasi || Alasan: 7 dimensi lolos terukur - 18/18 angka tertelusur per baris ke L2 U-1/U-2/U-9/U-12 + matriks B-29..B-34 + freshness baris 8-10 (pin byte-identik), kelengkapan 17/17 butir proposa termasuk URL kanonis target-sdk, tabel tarif STALE-FIELD l7 ditolak dengan benar, X-2 tidak dikutip sebagai angka, dedup wiki/vault 0 hit, YAML utuh. Catatan INFO non-pemblokir: kualifikasi '(kebijakan minimum)' pada closed testing tidak punya padanan kata di korpus beku (angka 12 tester x 14 hari bersumber B-34/U-12), dan 'dibatasi bertahap' adalah parafrasa dari 'limited only...rollout in 2027'. || Rekomendasi: saat promosi, hapus atau beri sumber khusus untuk '(kebijakan minimum)'; angka time-sensitive (tarif, tanggal, target API) tunduk prosedur DELTA salinan beku sebelum dikutip di dokumen rilis."
sumber: docs/2026-10-10_rafif-gameskill-guide/research/lanes/L2_domain_map.md (+ss. rujukan penuh di body; salinan beku vault/rafif-gameskill-1010/sources/)
halaman: ss.1 U-1,U-2,U-9,U-12; ss.3 butir 2/6
tanggal_akses: 2026-10-11
kelas_bukti: primer
sensitif: tidak
perkara: rafif-gameskill-1010
tags: [google-play, app-store, tarif, target-api, kepatuhan-toko, rafif-gameskill-1010]
links: [docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md, vault/rafif-gameskill-1010/sources/L2_domain_map.md]
penulis: gsp-librarian
diajukan: 2026-10-11
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-11
dipromosikan-ke: faktas/rafif-c3-store-economy-compliance-2026-10.md
catatan_keputusan: "dipromosikan: RG21b t_98725c99: gate biasa, custodian terverifikasi 2026-10-11, proposa 99 cc2cf2e093641ecf"
---

# Ekonomi dan Kepatuhan Toko Aplikasi (Google Play / Apple) per Oktober 2026

Objek baseline Information Library dari misi RAFIF-GAMESKILL-1010 (kandidat RAFIF-C3, lajur riset L2). Kelas bukti PRIMER (jawaban resmi per-sel halaman bantuan toko). Semua angka terukur ulang pada giliran promosi 2026-10-11 pukul 10:12-10:19 WIB (probe P-3, P-7, P-8) terhadap artefak riset beku ber-pin. Tanggal akses seragam 2026-10-11.

## 1. Tarif layanan Google Play (tabel per sel, jawaban resmi support.google.com answer/112622)

- Langganan: 10% + 5% (fee administrasi) untuk first $1M maupun standard. [R-3 U-1; R-1 B-29; R-7 P-7]
- Transaksi lain (non-langganan) NEW INSTALL: 20% + 5% standar. [R-3 U-1; R-1 B-29; R-7 P-7 token 20%]
- Transaksi lain EXISTING user: 25% + 5%, atau 20% bila memakai external web links. [R-3 U-1; R-1 B-29]
- Program Level Up / Apps Experience: new 15% + 5%; existing 20% + 5% atau 15% external. [R-3 U-1; R-1 B-29; R-7 P-7 token 15%]
- Pasar lain (di luar EEA/UK/US/AU/JP): 15% untuk first $1M / 30% di atasnya; langganan 15% flat. [R-3 U-1; R-1 B-29]
- Rollout wilayah: 30-Jun-2026 EEA/UK/US; Australia + Jepang efektif 30-Sep-2026. [R-3 U-1; R-1 B-29; R-7 P-7 token 'Australia' x4, 'Japan' x2]

## 2. Target API dan kewajiban tayang Android

- Mulai 31-Agu-2026 aplikasi baru dan update wajib target Android 16 (API level 36); Wear OS & Automotive API 35; TV & XR API 34; aplikasi existing minimal API 35; extension dapat diajukan s/d 1-Nov-2026. Footer halaman resmi 'Last updated 2026-10-01 UTC'. [R-3 U-2; R-1 B-30; R-5 baris 8; R-7 P-3 token 'Android 16 (API level 36)' + 'November 1, 2026']
- URL kanonis: developer.android.com/google/play/requirements/target-sdk (URL lama korpus 'google-play/requirements/target-sdk' mati 404; angka identik, URL berubah). [R-5 U-14 baris 8]
- Developer verification: enforcement mulai 30-Sep-2026 (dibatasi bertahap), rollout penuh 2027. [R-3 U-12; R-1 B-31]
- Registrasi developer Play: US$25 one-time; usia minimal 18 tahun. [R-3 U-12; R-1 B-32]

## 3. Apple (biaya program)

- Apple Developer Program US$99/tahun; Enterprise US$299/tahun. [R-3 U-9; R-1 B-33; R-7 P-8 token '$99' x1, '$299' x1]
- Small Business Program: komisi 15% dengan syarat pendapatan <= US$1 juta/tahun. [R-3 U-9; R-1 B-33]

## 4. Kuota jalur uji

- Play internal testing: 100 tester undangan. Closed testing: 12 tester x 14 hari (kebijakan minimum). [R-3 U-12; R-1 B-34]
- TestFlight: 10.000 penguji eksternal, uji berlaku 90 hari. [R-3 U-12; R-1 B-34]
- Firebase Test Lab: kuota gratis 30/60 menit tergantung paket (Spark/Blaze). [R-3 U-12; R-1 B-34]

## 5. BATAS dan prospektif

- Tarif adalah persentase per struktur sel; memakai satu angka tunggal 'potongan Play 30%' untuk Okt-2026 = salah terhadap primer (vonis STALE-FIELD atas tabel korpus lama l7). [R-5 baris 9, U-15]
- Batas panjang judul aplikasi Play dari rujukan korpus lama TIDAK diadopsi di objek ini (halaman jawaban resmi mati 404 tanpa arsip pada jendela uji; lihat register terlarang X-2 pada proposa sumber; angka tidak dikutip agar tidak terpropagasi).
- Angka time-sensitive (tarif, tanggal enforcement, target API) wajib dicek ulang terhadap primer sebelum dikutip dalam dokumen rilis setelah kuartal ini; prosedur DELTA memakai salinan beku folder sumber.

## 6. Register rujukan

- [R-1] `vault/rafif-gameskill-1010/sources/06_evidence_matrix.md` (53.891 B, sha256[:16] 69b125e91103ccaa) ss.7 baris B-29..B-34; ss.5 K-13.
- [R-3] `vault/rafif-gameskill-1010/sources/L2_domain_map.md` (22.482 B, sha256[:16] 8086e5da4844a1f9) ss.1 U-1, U-2, U-9, U-12.
- [R-5] `vault/rafif-gameskill-1010/sources/02_freshness_test.md` (24.736 B, sha256[:16] 8c1702cf52c56016) ss.2 baris 8-10; U-14..U-18.
- [R-7] Probe hidup giliran librarian 2026-10-11 10:12-10:19 WIB: P-3 target-sdk 200; P-7 answer/112622 200 1.628.692 B identik hulu (Australia x4, Japan x2, token 20%/15%/10%); P-8 developer.apple.com/programs 200 ($99 x1, $299 x1). Tabel 2.2 `docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md` (sha256[:16] cc2cf2e093641ecf).
