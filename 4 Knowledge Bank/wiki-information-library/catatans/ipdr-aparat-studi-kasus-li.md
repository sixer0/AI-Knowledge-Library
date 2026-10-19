---
id: ipdr-aparat-studi-kasus-li
type: catatan
title: Studi kasus end user aparat + lingkup intersepsi sah terukur (IPDR-GLOBAL)
status: active
sumber: docs/2026-09-12-ipdr-global/registri/REGISTRI-ENTITAS-v8.csv
halaman: kolom tipe-ENTITAS/KANAL-JUAL/lapis-R (293 baris)
tanggal_akses: 2026-09-13
kelas_bukti: sintesis
sensitif: ya
perkara: ipdr-global-0912
tags: [ipdr, gsp-global-0912, traffic-intelligence, aparat, lawful-interception]
penulis: gsp-librarian
diajukan: 2026-09-12
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-13
dipromosikan-ke: catatans/ipdr-aparat-studi-kasus-li.md
persetujuan-ref: user-webui-2026-09-12T22:3x-D-11a-kartu-t_fbfc624b
catatan_keputusan: "dipromosikan: revisi VE5-B pin v8 b16d91aa880de478 (D-15; riwayat: promosi VE5 persetujuan user D-11a)"
---

# Studi kasus end user aparat + lingkup intersepsi sah terukur (IPDR-GLOBAL)

Enam entitas aparat studi kasus terverifikasi dan besaran lingkup lawful interception terukur dari registri beku definitif v8 IPDR-GLOBAL-0912, sebagai batas mutu promosi dan rujukan pasar. Kelas akses: internal-TERBATAS (identitas aparat + konteks intersepsi sah; klasifikasi sumber D-03). Bukan panduan operasional (batas etika D-04): tingkat produk/kepatuhan saja.

## 1. Entri APARAT-STUDI-KASUS (6 baris, nama institusi publik; risiko = konteks kapabilitas, bukan identitas rahasia)

| GENT-id | Institusi | Negara | STATUS-BUKTI |
|---|---|---|---|
| GENT-00109 | Kepolisian Negara Republik Indonesia (Polri) | Indonesia | VERIFIED-L1 |
| GENT-00110 | Home Team Science and Technology Agency (HTX) | Singapore | VERIFIED-L1 |
| GENT-00120 | Drug Enforcement Administration (DEA) | United States | VERIFIED-L2 |
| GENT-00121 | Federal Bureau of Investigation (FBI) | United States | VERIFIED-L2 |
| GENT-00122 | Bundeskriminalamt (BKA) | Germany | VERIFIED-L2 |
| GENT-00123 | National Crime Agency (NCA) | United Kingdom | VERIFIED-L2 |

L1 = halaman resmi/institusi; L2 = kontrak publik USAspending / laporan resmi (akun per baris di kolom bukti-sumber registri).

## 2. Lingkup LI terukur (batas mutu promosi)

- Kanal jual APARAT-DIREKT: 41 baris; DUA-KANAL: 36 baris.
- Lapis R6 terbukti (utama+sekunder): 57 baris.
- Fungsi jalur AKTIF: 47 baris, semuanya tertambat baris register risiko kepatuhan (aturan SKEMA kolom 11; dua baris AKTIF baru v8 GENT-00240/GENT-00241 membawa anchor eksplisit di catatan-risiko).
- Baris TELKO-HULU murni (33) dilarang naik sebagai "solusi aparat" tanpa bukti penawaran (TA-D-11).

## 3. PROVENANS

- Pembilang tunggal: `registri/REGISTRI-ENTITAS-v8.csv` sha256(16) `b16d91aa880de478`, diukur ulang giliran revisi ini (`process/ve5b_measure.py`: APARAT-DIREKT 41, DUA-KANAL 36, R6 terbukti 57, AKTIF 47, TELKO-HULU 33, aparat 6; roster aparat identik dengan gelombang-1). Riwayat pin: `e1940da5c400f70f` (273 baris).
- Narasi bab terkait: `output/dasar_pengetahuan_003-GSP-IPD-IX-2026_TERBATAS.md` REV 1 (sha16 `1fc1b425507304fd`) Bab 13.
- Ladder: `process/LADDER-GC8*.md` (r1-r4) untuk studi kasus aparat dan tender publik.
- Rantai seed GB1..M4 + GC1-GAP..F1 (`registri/SEED-LOG.txt` sha16 `b7b5fdbf39a94ef2`, tumbuh dari `dba7cd3da2920cf0`).
- Verifikasi: VD1 sha16 `03f7a0598c92d456` (SALAH-TARGET 0 dari 273 fetch mandiri), VD2 countersign sha16 `f0dd9dc7c4ae021e`, V-SUSUN v2 sha16 `158e35f710443e11` VERDICT PASS; VD3 `reports/VERIFIKASI-AKURASI-v3.md` (sha16 `a10d8acb87019a8f`), VD4 `reports/VERIFIKASI-AKURASI-v4.md` (sha16 `b0843be81117384c`), countersign VD2-B2 `reports/COUNTERSIGN-v3.md` (sha16 `c9e42965c30ca200`, VERDICT SETUJU-RILIS, sumber definitif v8).
- Persetujuan promosi: user via WebUI 2026-09-12 22:3x verbatim "1. Masukkan ke Information Library" (kontrak D-11a, kartu t_fbfc624b).

## REV-4 (2026-09-13, kartu t_384058a8, putusan controller D-15)

- Pin pembilang diganti: BEKU M4 sha256(16) `e1940da5c400f70f` (273 baris; riwayat pin gelombang-1, tetap rujukan sejarah, bukan sunting diam) -> BEKU definitif `registri/REGISTRI-ENTITAS-v8.csv` sha256(16) `b16d91aa880de478` (293 baris data; kapabilitas 262). Rantai beku utuh: e1940da5 -> v6 `75a76c5556f5e932` -> v7 `8c62d91b7fd4a00d` -> v8 `b16d91aa880de478` (deklarasi D-14; diverifikasi VD1-B3 CHECK 1 + countersign VD2-B2 SETUJU-RILIS `c9e42965c30ca200`).
- Angka turunan objek ini ditarik ulang dari v8 lewat `process/ve5b_measure.py` (seed `20260913-VE5B-SEED-V1`; cetakan `process/ve5b_measure.json`). Tabel perubahan lama->baru: `reports/PROMOSI-IL-LOG-v2.md`.
- Kelas akses tidak berubah; persetujuan user D-11a tetap berlaku untuk objek TERBATAS.
