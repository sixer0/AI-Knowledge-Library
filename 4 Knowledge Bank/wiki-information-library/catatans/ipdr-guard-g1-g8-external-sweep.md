---
id: ipdr-guard-g1-g8-external-sweep
type: catatan
title: Guard anti-positif-palsu G-1..G-8 versi sapuan eksternal IPDR
status: active
sumber: docs/2026-09-12-ipdr-global/reports/ARUS-BALIK-KEMHAN-v1.md
halaman: bagian 2b
tanggal_akses: 2026-09-13
kelas_bukti: primer
sensitif: tidak
perkara: ipdr-global-0912
tags: [ipdr, gsp-global-0912, traffic-intelligence, guard, anti-positif-palsu]
penulis: gsp-librarian
diajukan: 2026-09-12
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-13
dipromosikan-ke: catatans/ipdr-guard-g1-g8-external-sweep.md
catatan_keputusan: "dipromosikan: revisi VE5-B pin v8 b16d91aa880de478 (D-15; riwayat: promosi VE5 persetujuan user D-11a)"
---

# Guard anti-positif-palsu G-1..G-8 versi sapuan eksternal IPDR

Delapan guard penyaringan kandidat entitas IPDR yang diwarisi UTUH dari KEMHAN (rujukan `docs/2026-09-12-ipdr-global/identification/02_structured.md` baris 89) dan TERBUKA bekerja pada pencarian web lintas bahasa, bukan hanya penambangan korpus internal: seluruh 33 berkas ladder misi IPDR-GLOBAL-0912 mencatat penerapannya, dan 8 kelas positif-palsu baru tertangkap gerbang dengan nol lolos ke master. Kelas akses: internal nonsensitif.

## 1. Delapan guard

| ID | Guard |
|---|---|
| G-1 | Regex batas kata untuk token IPDR |
| G-2 | Token "DPI" berdiri sendiri DILARANG; hanya frasa "deep packet inspection" + padanan ID/CN |
| G-3 | Konteks drone-pencegat diecualikan dari makna intersepsi |
| G-4 | Frasa lengkap "interception" wajib; "intercept" telanjang tidak menaikkan baris |
| G-5 | Kata umum mediation/probe/recorder/tap/flow sah hanya ko-occur konteks jaringan/telekom |
| G-6 | Normalisasi case-fold + batas kata |
| G-7 | Setiap hit dibaca manusia dengan disposisi ACCEPT/REJECT/JUDGED-OUT (adjudikasi berakun) |
| G-8 | Direktori arsip `*-lama-*`/`*.bak-*` dikecualikan dari hitungan |

## 2. Delapan kelas positif-palsu baru yang tertangkap (nol lolos ke master)

1. Intersepsi fisik laut: tender UNODC/UNGM "Semi-Armored Patrol and Interception Vessels" (analog G-3/G-4; LADDER-GC8).
2. DPI endpoint-security: Trend Micro Deep Security, ko-occur bukan jaringan operator (G-5; LADDER-GC8).
3. Benturan merek pada identifier vendor sah: aerotel.com (ECG) vs Aerotel LI; reve.com vs REVE Systems; gamma-group.com vs gamma.ie; ips.it (LADDER-GC3/GC8). Pelajaran: token host saja tidak cukup; entity-match wajib uji isi/judul (SPK-002 butir 2).
4. Benturan akronim intra-ekosistem: "ATIS" = tiga badan berbeda (atisdigital.com vs atis-systems.com vs ATIS.cloud/CYDIS). Preseden: akronim pendek butuh pembeda host+judul.
5. Token di markup bukan teks terlihat: hit "data retention" beranda Telkom berasal dari atribut modal pencarian (LADDER-GC7). Aturan baca: kutipan bukti wajib dari judul/paragraf.
6. Positif-palsu drill Indonesia: dropdown bahasa, daftar negara form, substring kebetulan (LADDER-GC3-r2, LADDER-DRILL-ID). Jejak-INDONESIA=ADA hanya bila entitas + aktivitas Indonesia ko-occur pada teks terlihat.
7. Drift kategori produk: Riverbed "Deep Visibility" kini NPM/observability, bukan pembuat IPDR R1/R2 lagi (LADDER-GC1). Nama produk historis tidak boleh dipercaya dari ingatan.
8. Stub WAF HTTP 200 tanpa isi: thales.co.id 1041-1050 B tanpa token (M2b-GATE). 200 HTTP bukan bukti entitas bila body stub.

## 3. PROVENANS

- Sumber guard: blueprint `identification/02_structured.md` (sha16 `1c5a0062092996ab`) baris 89; aslinya KEMHAN `02_structured.md` baris 140-151.
- Bukti kerja lintas bahasa: 33 berkas `process/LADDER-*.md` (ukuran 8.411-62.154 B, terukur giliran promosi ini) + `reports/ARUS-BALIK-KEMHAN-v1.md` (sha16 `2e23f2dc6d4143d8`) bagian 2b.
- Registri beku definitif hasil: sha256(16) `b16d91aa880de478` (293 baris; riwayat pin gelombang-1 `e1940da5c400f70f`, 273 baris); rantai seed GB1..M4 + GC1-GAP..F1 `registri/SEED-LOG.txt` (sha16 `b7b5fdbf39a94ef2`, tumbuh dari `dba7cd3da2920cf0`).
- Kelas bukti primer: hasil ukur pipeline sendiri, dapat dijalankan ulang lewat skrip `process/` yang didaftarkan di ladder masing-masing lajur.

## REV-4 (2026-09-13, kartu t_384058a8, putusan controller D-15)

- Pin pembilang diganti: BEKU M4 sha256(16) `e1940da5c400f70f` (273 baris; riwayat pin gelombang-1, tetap rujukan sejarah, bukan sunting diam) -> BEKU definitif `registri/REGISTRI-ENTITAS-v8.csv` sha256(16) `b16d91aa880de478` (293 baris data; kapabilitas 262). Rantai beku utuh: e1940da5 -> v6 `75a76c5556f5e932` -> v7 `8c62d91b7fd4a00d` -> v8 `b16d91aa880de478` (deklarasi D-14; diverifikasi VD1-B3 CHECK 1 + countersign VD2-B2 SETUJU-RILIS `c9e42965c30ca200`).
- Angka turunan objek ini ditarik ulang dari v8 lewat `process/ve5b_measure.py` (seed `20260913-VE5B-SEED-V1`; cetakan `process/ve5b_measure.json`). Tabel perubahan lama->baru: `reports/PROMOSI-IL-LOG-v2.md`.
- Kelas akses tidak berubah; persetujuan user D-11a tetap berlaku untuk objek TERBATAS.
