---
id: cdex-standar-skema-db-xlsx
type: standar
title: "China Defence Expo — skema database XLSX 21 kolom, 6 sheet, quality gates QG1-QG10"
status: active
sumber: legacy-archive/china-defence-expo-crawler-20260824T085128Z-1-001/china-defence-expo-crawler/outputs/01_synthesis_framework.md
halaman: Section 5-9 + verification Section 2
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: china-defence-expo-crawler
tags: [china, standar, database-schema, xlsx, quality-gates, defense-intel]
penulis: gsp-librarian
diajukan: 2026-08-25
created: 2026-08-25
writer: gsp-librarian
domain: defense-intel
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/china-defence-expo-crawler/2026-08-25_cdex-standar-skema-db-xlsx.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# China Defence Expo — skema database XLSX 21 kolom, 6 sheet, quality gates QG1-QG10

Skema database (01_synthesis_framework.md Section 5-7; kolom terverifikasi di 01_verification_report.md Section 2):
- 21 kolom Vendor_Master: vendor_id, name_en, name_cn, region, city, expo, business_type, dual_use_status, registration_date, registered_capital, ownership, subsidiaries, gjb_certifications, export_license, risk_flags, confidence_score, tier, composite_score, Website, Contact_Email, Source_URL.
- 6 sheet: Vendor_Master, Product_Master, Regional_Summary, Gap_Analysis, Vendor_Profiles, METADATA.
- 10 quality gates (QG1-QG10): unik vendor_id, integritas mapping vendor-produk, >=90% field P0, keseimbangan regional, confidence 0-100%, atribusi sumber >=80%, OSINT >=2 sumber 100%, konsistensi tier, konsistensi skor, kelengkapan gap Critical/High.
- Conditional formatting untuk status dual-use, ekspor, severity gap, coverage score.

[Sumber: legacy-archive/china-defence-expo-crawler-20260824T085128Z-1-001/china-defence-expo-crawler/outputs/01_synthesis_framework.md]
