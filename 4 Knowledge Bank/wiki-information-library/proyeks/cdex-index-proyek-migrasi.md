---
id: cdex-index-proyek-migrasi
type: proyek
title: "China Defence Expo Crawler — index proyek & rekaman migrasi"
status: active
sumber: docs/2026-08-24_china-defence-expo-crawler/README.md
halaman: Ringkasan baris 12-19
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: china-defence-expo-crawler
domain: defense-intel
writer: gsp-librarian
tags: [china-defence-expo-crawler, migrasi, proyek, defense-intel, documentation-contract]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/china-defence-expo-crawler/2026-08-25_cdex-index-proyek-migrasi.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# China Defence Expo Crawler — index proyek & rekaman migrasi

## Ringkasan
Proyek China Defence Expo Crawler adalah proyek intelijen (gsp-data-collector) pemetaan
vendor & produk dari 7 ekspo pertahanan/OSINT China (CIDEX, Security China, PT Expo China,
Airshow China, Big Data Expo, CRSAE, Shanghai Cybersecurity Expo) di 4 region China,
menargetkan pasar Indonesia. Artefak ini adalah rekaman task migrasi (Documentation Contract)
yang membaca MIGRATION_BRIEF.md, knowledge_map.md (bagian china-defence-expo-crawler),
manifest.json, dan 8 artefak kunci proyek.

## Struktur korpus terverifikasi (task migrasi)
- 743 file; struktur outputs/ + folder "07082026 0925" sebagai deliverable utama.
- Pola duplikat suffix: 375 file ber-akhiran (1)/(2)/(3); hash membuktikan beberapa salinan identik.

## Status
- README (artefak migrasi): STATUS complete, tidak ada blocker.
- Catatan verifikasi: README mengklaim 4 objek vault dibuat di `vault/china-defence-expo/`
  (index proyek, north-china-findings, synthesis-framework, deliverable-final), namun folder
  `vault/china-defence-expo/` KOSONG (2026-08-25) — objek aktual berada di perkara
  `vault/china-defence-expo-crawler/` (129 objek, analisa RAW 2026-08-25). Proposa ini
  mengisi index proyek yang diklaim namun tidak ada.

## Bukti
- Sumber: docs/2026-08-24_china-defence-expo-crawler/README.md (Ringkasan, baris 12-19;
  GAP utama baris 30-38; Blocker baris 39-40).
- Kelas bukti: sekunder (README adalah ringkasan turunan dari laporan RAW).
- Asumsi: angka detail korpus (161/62, 1360/337, 643+/299+) dipisahkan ke KU terpisah.
