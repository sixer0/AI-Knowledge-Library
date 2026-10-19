---
id: ipdr-leksikon-baru-v2
type: fakta
title: Leksikon baru terbukti dari sapuan eksternal IPDR (usulan LEKSIKON v2)
status: active
sumber: docs/2026-09-12-ipdr-global/reports/ARUS-BALIK-KEMHAN-v1.md
halaman: bagian 1c+2a
tanggal_akses: 2026-09-13
kelas_bukti: primer
sensitif: tidak
perkara: ipdr-global-0912
tags: [ipdr, gsp-global-0912, traffic-intelligence, leksikon, term]
penulis: gsp-librarian
diajukan: 2026-09-12
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-13
dipromosikan-ke: faktas/ipdr-leksikon-baru-v2.md
catatan_keputusan: "dipromosikan: revisi VE5-B pin v8 b16d91aa880de478 (D-15; riwayat: promosi VE5 persetujuan user D-11a)"
---

# Leksikon baru terbukti dari sapuan eksternal IPDR (usulan LEKSIKON v2)

Tujuh term yang lolos adjudikasi guard G-7 dan terbukti produktif di sapuan web eksternal (satu-satunya frasa payung yang menangkap penawaran, atau varian literal yang tak tertangkap regex dasar). Diusulkan masuk revisi v2 LEKSIKON-IPDR-v1 (beku TA-D-01; perluasan lewat revisi tercatat, bukan improvisasi). Kelas akses: internal nonsensitif.

## 1. Tujuh term (tabel R-6 bagian 2a, cocok dengan hitungan atas berkas sumber)

| Term | Lapis | Bukti produksi | Rujukan |
|---|---|---|---|
| lawful surveillance | R4/R6 | judul halaman retensi Subsentio (satu-satunya frasa payung penangkap retention+LI sekaligus) | GENT-00027 |
| records production | R4/R3 | "Records production Subscriber records, CDRs, preservation" | GENT-00027 |
| legal disclosure | R4/R6 | frasa payung homepage Group 2000 berdampingan "data retention" | GENT-00141 |
| ipdr streaming protocol / IPDR/SP | R3 | penamaan protokol produk OpenVault (varian literal yang memastikan arah protokol) | GENT-00020 |
| ipdr collection | R3 | frasa produk ATS (arah collector broadband) | GENT-00017 |
| cgnat sebagai ko-occur pembangkit IPDR | R3 | cgnat x5 ko-occur ipdr x20 (Heksagon); cgnat x4-5 (Sandvine); halaman thunder-cgn (A10) | GENT-00016, GENT-00008, ENT-14290 |
| network forensics + retention (ko-occur) | R4 | modul "Network Forensics ... Unlimited Retention" Vehere | GENT-00023 |

Semua term tunduk guard ko-occur G-5 saat dipakai; tidak ada yang boleh berdiri sendiri sebagai pemicu.

## 2. Penanda literal IPDR

Token literal IPDR hadir di 7 baris master registri beku (hitung `ve5b_measure.py` atas kolom nama/bukti/URL, terukur ulang giliran revisi ini; tetap 7 baris pada v8), termasuk dua vendor Indonesia (Heksagon GENT-00016, PT. Artha Inti Prima GENT-00100). Ini menjawab gap literal U-1 KEMHAN (literal "IPDR" = 0 hasil di korpus RevC).

## 3. PROVENANS

- Sumber utama: `docs/2026-09-12-ipdr-global/reports/ARUS-BALIK-KEMHAN-v1.md` (sha16 `2e23f2dc6d4143d8`) bagian 1c dan 2a.
- Registri beku definitif: sha256(16) `b16d91aa880de478` (293 baris), diukur ulang giliran revisi ini (riwayat pin gelombang-1 `e1940da5c400f70f`, 273 baris); tiap baris rujukan membawa bukti-sumber + URL-bukti ber-timestamp.
- Rantai seed GB1..M4 + GC1-GAP..F1 (`registri/SEED-LOG.txt` sha16 `b7b5fdbf39a94ef2`, tumbuh dari `dba7cd3da2920cf0`); ladder terkait: LADDER-GC2*, LADDER-GC7*, LADDER-GC8* (dari 33 berkas `process/LADDER-*.md`).
- Kelas bukti primer: frasa dikutip dari fetch sendiri ber-akun timestamp di kolom bukti-sumber registri.

## REV-4 (2026-09-13, kartu t_384058a8, putusan controller D-15)

- Pin pembilang diganti: BEKU M4 sha256(16) `e1940da5c400f70f` (273 baris; riwayat pin gelombang-1, tetap rujukan sejarah, bukan sunting diam) -> BEKU definitif `registri/REGISTRI-ENTITAS-v8.csv` sha256(16) `b16d91aa880de478` (293 baris data; kapabilitas 262). Rantai beku utuh: e1940da5 -> v6 `75a76c5556f5e932` -> v7 `8c62d91b7fd4a00d` -> v8 `b16d91aa880de478` (deklarasi D-14; diverifikasi VD1-B3 CHECK 1 + countersign VD2-B2 SETUJU-RILIS `c9e42965c30ca200`).
- Angka turunan objek ini ditarik ulang dari v8 lewat `process/ve5b_measure.py` (seed `20260913-VE5B-SEED-V1`; cetakan `process/ve5b_measure.json`). Tabel perubahan lama->baru: `reports/PROMOSI-IL-LOG-v2.md`.
- Kelas akses tidak berubah; persetujuan user D-11a tetap berlaku untuk objek TERBATAS.
