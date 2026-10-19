---
id: ipdr-global-market-snapshot-2026
type: fakta
title: Snapshot pasar solusi IPDR global 2026 (registri beku IPDR-GLOBAL)
status: active
sumber: docs/2026-09-12-ipdr-global/registri/REGISTRI-ENTITAS-v8.csv
halaman: 293 baris data (kolom agregat)
tanggal_akses: 2026-09-13
kelas_bukti: sintesis
sensitif: ya
perkara: ipdr-global-0912
tags: [ipdr, gsp-global-0912, traffic-intelligence, pasar, registri-beku]
penulis: gsp-librarian
diajukan: 2026-09-12
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-13
dipromosikan-ke: faktas/ipdr-global-market-snapshot-2026.md
persetujuan-ref: user-webui-2026-09-12T22:3x-D-11a-kartu-t_fbfc624b
catatan_keputusan: "dipromosikan: revisi VE5-B pin v8 b16d91aa880de478 (D-15; riwayat: promosi VE5 persetujuan user D-11a)"
---

# Snapshot pasar solusi IPDR global 2026 (registri beku IPDR-GLOBAL)

Ringkasan populasi registri entitas misi IPDR-GLOBAL-0912, sumber pembilang tunggal `docs/2026-09-12-ipdr-global/registri/REGISTRI-ENTITAS-v8.csv`. Objek berisi ringkasan agregat + rujukan berkas beku, BUKAN salinan 293 baris. Kelas akses: internal-TERBATAS (memuat profil aparat dan kanal jual-aparat), mengikuti label sumber.

## 1. Populasi beku definitif v8 (terukur ulang giliran revisi ini, `process/ve5b_measure.py`)

- Baris: 293; kapabilitas: 262; non-kapabilitas: 31 (SDO-REGULATOR 22 + APARAT-STUDI-KASUS 6 + PENERBIT-PASAR 3).
- Tipe entitas: VENDOR 181, OSS-PROYEK 56, SDO-REGULATOR 22, INTEGRATOR 10, APARAT-STUDI-KASUS 6, MITRA-RESELLER 13, PENERBIT-PASAR 3, ISV 2.
- Jenjang bukti: VERIFIED-L2 58, VERIFIED-L1 191, PARTIAL 44, UNVERIFIED 0 terbit.
- Kanal jual: APARAT-DIREKT 41, DUA-KANAL 36, TELKO-HULU 33, TIDAK-DIKETAHUI 183.
- Jalur tata kelola: PASIF 165, LINTAS 81, AKTIF 47 (fungsi AKTIF wajib tertambat baris register risiko kepatuhan per SKEMA kolom 11).
- Ekspor-kontrol (kanonis REV 1): berawalan BELUM-DIKAJI 292 (persis 274 + varian berpenanda kurung 18); predikat nyata 1 (GENT-00180 Meiya Pico / SDIC Intelligence, US Entity List 2019-10-09, 84 FR 54002 BIS).

## 2. Batas pemakaian

- Daftar ini adalah peta pasar tingkat produk/kepatuhan, BUKAN panduan operasional intersepsi (batas etika D-04).
- Baris TELKO-HULU murni (33) dilarang dibaca sebagai "solusi aparat" tanpa bukti penawaran ke aparat (TA-D-11).
- UNVERIFIED tidak pernah naik ke kolom terbit (TA-D-09).

## 3. PROVENANS

- Pin registri beku definitif: sha256(16) `b16d91aa880de478`, 356.251 B, 293 baris; diukur ulang pada giliran revisi ini (ts+seed cetak `process/ve5b_measure.json`). Riwayat pin gelombang-1: `e1940da5c400f70f` (273 baris) - lihat seksi REVISI.
- Rantai seed merge: `20260912-GB1-SEED-V1` -> M1 -> M2 -> M2b -> M3 -> M3c -> `20260912-M4-SEED-V1` (beku gelombang-1); verifier memakai seed berbeda: VD1 `20260912-VD1-V1` + sampel `20260912-VD1-SAMPLE-V1`, V-SUSUN `20260912-VS3-SEED-V1` lalu `20260912-VS3R-SEED-V2`.
- Path ladder akuisisi: 33 berkas `docs/2026-09-12-ipdr-global/process/LADDER-*.md` (lajur G-C1..G-C8 r1-r4 + GC1GAP r1-r4/c1-c2 + DRILL-ID-A/B), tiap rung memuat URL/aksi, status HTTP + timestamp, hasil, keputusan lanjut.
- Laporan verifikasi: VD1 `reports/VERIFIKASI-AKURASI-v1.md` (sha16 `03f7a0598c92d456`, 26 CHECK PASS, SALAH-TARGET 0 atas 273 fetch mandiri); VD2 `reports/COUNTERSIGN-v1.md` (sha16 `f0dd9dc7c4ae021e`, SETUJU-RILIS); V-SUSUN v2 `reports/V-SUSUN-003-v2.md` (sha16 `158e35f710443e11`, VERDICT PASS 20 CHECK); VD3 `reports/VERIFIKASI-AKURASI-v3.md` (sha16 `a10d8acb87019a8f`), VD4 `reports/VERIFIKASI-AKURASI-v4.md` (sha16 `b0843be81117384c`), countersign VD2-B2 `reports/COUNTERSIGN-v3.md` (sha16 `c9e42965c30ca200`, VERDICT SETUJU-RILIS, sumber definitif v8).
- Dokumen turunan: `output/dasar_pengetahuan_003-GSP-IPD-IX-2026_TERBATAS.md` REV 1 (sha16 `1fc1b425507304fd`, 78.520 B); `output/workbook_matriks_004-GSP-IPD-IX-2026_TERBATAS.xlsx` (sha16 `0249702f80b6e5f9`).
- Persetujuan promosi: user via WebUI 2026-09-12 22:3x verbatim "1. Masukkan ke Information Library" (kontrak misi D-11a, kartu t_fbfc624b).

## REV-4 (2026-09-13, kartu t_384058a8, putusan controller D-15)

- Pin pembilang diganti: BEKU M4 sha256(16) `e1940da5c400f70f` (273 baris; riwayat pin gelombang-1, tetap rujukan sejarah, bukan sunting diam) -> BEKU definitif `registri/REGISTRI-ENTITAS-v8.csv` sha256(16) `b16d91aa880de478` (293 baris data; kapabilitas 262). Rantai beku utuh: e1940da5 -> v6 `75a76c5556f5e932` -> v7 `8c62d91b7fd4a00d` -> v8 `b16d91aa880de478` (deklarasi D-14; diverifikasi VD1-B3 CHECK 1 + countersign VD2-B2 SETUJU-RILIS `c9e42965c30ca200`).
- Angka turunan objek ini ditarik ulang dari v8 lewat `process/ve5b_measure.py` (seed `20260913-VE5B-SEED-V1`; cetakan `process/ve5b_measure.json`). Tabel perubahan lama->baru: `reports/PROMOSI-IL-LOG-v2.md`.
- Kelas akses tidak berubah; persetujuan user D-11a tetap berlaku untuk objek TERBATAS.
