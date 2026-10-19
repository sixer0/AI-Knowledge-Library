---
id: cdex-pelajaran-parser-rebuild-v21
type: pelajaran
title: "China Defence Expo — pelajaran: rebuild parser v2.1 mengembalikan 161->1.360 vendor, +114 flag OSINT"
status: active
sumber: legacy-archive/china-defence-expo-crawler-20260824T085128Z-1-001/china-defence-expo-crawler/outputs/07082026 0925/china_defence_expo_report_v2.md
halaman: Pendahuluan & Section 2
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: china-defence-expo-crawler
tags: [china, pelajaran, parser, rebuild, osint, defense-intel]
penulis: gsp-librarian
diajukan: 2026-08-25
created: 2026-08-25
writer: gsp-librarian
domain: defense-intel
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/china-defence-expo-crawler/2026-08-25_cdex-pelajaran-parser-rebuild-v21.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# China Defence Expo — pelajaran: rebuild parser v2.1 mengembalikan 161->1.360 vendor, +114 flag OSINT

Pelajaran dari rebuild v2.1 (china_defence_expo_report_v2.md): ekstrak v1.0 kehilangan data karena:
1. Tabel regional memakai 5 layout header discovery berbeda — parser v1.0 hanya menangani sebagian.
2. Matriks OSINT per-region (Vendor x BIS x Pentagon 1260H x OFAC x EU x UN) DIABAIKAN v1.0 — rebuild memulihkan +114 flag.
3. Enrichment memakai tabel nama split/single campuran; rebuild menggabungkan nama pendek ke record penuh via alias akronim (mis. CETC -> China Electronics Technology Group).

Hasil: 161 -> 1.360 vendor unik (~8x), 62 -> 337 produk (~5x), 75 flagged (vs ~64 estimasi awal), 83 GJB (vs 18). Pelajaran: format tabel yang beragam wajib dipetakan eksplisit; jangan pernah menganggap satu layout.

[Sumber: legacy-archive/china-defence-expo-crawler-20260824T085128Z-1-001/china-defence-expo-crawler/outputs/07082026 0925/china_defence_expo_report_v2.md]
