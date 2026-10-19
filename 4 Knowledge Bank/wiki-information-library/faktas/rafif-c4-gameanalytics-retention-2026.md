---
id: rafif-c4-gameanalytics-retention-2026
type: fakta
title: Benchmark Retensi dan Sesi Game Mobile 2026 (GameAnalytics) - LABEL VENDOR
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-11
catatan_verifikasi: "Verdict: terverifikasi || Alasan: 29/29 angka tertelusur ke L3 ss.1 U-8 + baris D1..D5 + matriks B-26..B-28 (pin byte-identik); LABEL VENDOR menempel pada 18/18 baris benchmark berdigit (8 baris berdigit tanpa VENDOR = seksi BATAS dan register rujukan, bukan angka benchmark); larangan peleburan populasi Admiral Media (K-11) hadir dan terverifikasi teks ke L3 ss.3 butir 4 ('200+ kampanye UA berbayar'); X-1 Newzoo hanya muncul sebagai LARANGAN; entity-match, populasi 16.000+ game dan ambang >=1.000 MAU CY2025 utuh; dedup 0; YAML utuh. || Rekomendasi: saat promosi tambahkan penanda U-8 pada baris region dan percentil sesi (Oceania 25,63/NA 23,28/EU 22,20/Afrika 18,52; P90 40-42; P75 ~5,2 dan ~8 dan >22; P75 5,3-5,7) karena detail itu hidup di register U-8 sementara baris tersebut mengutip D4/D5 saja; semua angka terverifikasi ada di sumber, nol fabrikasi, vonis tidak bergantung pada rapian ini."
sumber: docs/2026-10-10_rafif-gameskill-guide/research/lanes/L3_quality_bar.md (+ss. rujukan penuh di body; salinan beku vault/rafif-gameskill-1010/sources/)
halaman: ss.1 U-8; ss.2.1 D1..D5
tanggal_akses: 2026-10-11
kelas_bukti: sekunder
sensitif: tidak
perkara: rafif-gameskill-1010
tags: [retensi, benchmark, vendor-label, gameanalytics, rafif-gameskill-1010]
links: [docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md, vault/rafif-gameskill-1010/sources/L3_quality_bar.md]
penulis: gsp-librarian
diajukan: 2026-10-11
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-11
dipromosikan-ke: faktas/rafif-c4-gameanalytics-retention-2026.md
catatan_keputusan: "dipromosikan: RG21b t_98725c99: gate biasa, custodian terverifikasi 2026-10-11, proposa 99 cc2cf2e093641ecf"
---

# Benchmark Retensi dan Sesi Game Mobile 2026 (GameAnalytics) - LABEL VENDOR

Objek baseline Information Library dari misi RAFIF-GAMESKILL-1010 (kandidat RAFIF-C4, lajur riset L3). KELAS BUKTI: SEKUNDER - benchmark vendor, BUKAN ambang resmi platform. Setiap baris angka di objek ini berlabel VENDOR: nilainya adalah distribusi pasar sesungguhnya (median/persentil dari dataset vendor), bukan norma yang ditegakkan toko. Populasi: 16.000+ game mobile 9 region dengan ambang >= 1.000 MAU, tahun kalender 2025; halaman 'Last updated: August 24, 2026'. Entity-match PASS (judul '2026 Mobile & PC Gaming Benchmarks - GameAnalytics', penulis Tomas Hubka). [R-4 U-8; R-1 B-26; R-7 P-5]

## 1. Retensi global (semua angka = VENDOR)

- D1: P50 ~22%; P75 'tepat di atas 30%'; P90 ~40%; P99 64-68%. [R-4 D1, VENDOR; R-1 B-26; R-7 P-5 konteks '22%']
- D7: P50 < 4%; P75 6-7%; P90 11-12%; P99 > 25% (puncak > 28%). [R-4 D2, VENDOR; R-1 B-26; R-7 P-5 konteks 'D7 just under 4%']
- D30: P50 0,68-0,79%; P75 1,6-1,8%; P99 13-15%. [R-4 D3, VENDOR; R-1 B-26; R-7 P-5 konteks 'D30 at roughly 0']

## 2. Konteks region Asia / Indonesia (VENDOR)

- D1 P50 Asia 17,50% (di bawah median global 22%); Oceania 25,63%, NA 23,28%, EU 22,20%, Afrika 18,52%. [R-4 D4, VENDOR; R-1 B-27]
- D7 P50 Asia 2,68% (terendah bersama); Afrika/Oceania 5,60%, NA 4,97%, EU 4,06%. Implikasi bar lokal: standar retensi pasar Asia lebih rendah dari median global. Komentar analis di halaman (opini berlabel): 'value harus terasa di 10-15 menit pertama'. [R-4 D4, VENDOR; R-1 B-27]

## 3. Pola sesi (median, VENDOR)

- Playtime per hari P50 ~12 menit (P75 22-24; P90 40-42; P99 > 94). [R-4 D5, VENDOR; R-1 B-28]
- Panjang sesi P50 3,1-3,5 menit (P75 ~5,2; P90 ~8; P99 > 22). [R-4 D5, VENDOR; R-1 B-28]
- Frekuensi sesi P50 3,8-3,9 sesi/hari (P75 5,3-5,7; P99 > 12). [R-4 D5, VENDOR; R-1 B-28]
- PC (pelengkap): D1 median ~7%; DAU/MAU median 4-5%; top 1% > 50%. [R-4 U-8, VENDOR]

## 4. BATAS wajib pakai (anti-peleburan)

- Label VENDOR menempel pada SETIAP angka di objek ini: bukan ambang resmi Google Play/Apple (ambang resmi sisi Android ada di objek rafif-c2, kelas primer).
- DILARANG melebur dua populasi D7 berbeda: GameAnalytics (P50 < 4%, P75 6-7%; semua game terintegrasi GA) vs dataset Admiral Media (kuartil atas 25%+ dari 200+ kampanye UA berbayar). Setiap angka wajib menyebut sumbernya; tidak ada satu 'rata-rata industri'. [R-1 K-11; R-4 ss.3 butir 4]
- Angka Newzoo 2026 TIDAK termasuk objek ini (NEGATIF-BERAKUN; lihat register terlarang X-1 pada proposa sumber). Pengganti angka pasar = estimator berlabel (pocketgamer 2024 / mobilegamer H1-2025), bukan fakta absolut.
- Prospektif: benchmark vendor bergeser tiap tahun kalender; prosedur DELTA membandingkan hanya terhadap salinan beku `vault/rafif-gameskill-1010/sources/`.

## 5. Register rujukan

- [R-1] `vault/rafif-gameskill-1010/sources/06_evidence_matrix.md` (53.891 B, sha256[:16] 69b125e91103ccaa) ss.7 baris B-26..B-28; ss.5 K-8/K-11.
- [R-3] `vault/rafif-gameskill-1010/sources/L2_domain_map.md` (22.482 B, sha256[:16] 8086e5da4844a1f9) ss.1 U-7.
- [R-4] `vault/rafif-gameskill-1010/sources/L3_quality_bar.md` (31.665 B, sha256[:16] 32e41ac440292210) ss.1 U-8; ss.2.1 baris D1..D5.
- [R-5] `vault/rafif-gameskill-1010/sources/02_freshness_test.md` (24.736 B, sha256[:16] 8c1702cf52c56016) ss.2 baris 12.
- [R-7] Probe hidup giliran librarian 2026-10-11 WIB: P-5 gameanalytics.com/reports/2026-mobile-pc-gaming-benchmarks HTTP 200, 150.809 B; judul entity-match PASS; konteks '22%, D7 just under 4%, and D30 at roughly 0' hadir. Tabel 2.2 `docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md` (sha256[:16] cc2cf2e093641ecf).
