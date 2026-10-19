---
id: cdec-pipeline-repeatable-sumber
type: standar
title: "Pipeline repeatable China Defence Expo Crawler — sumber data & pustaka kueri"
status: active
links: cdex-inventori-sumber-ekspo
created: 2026-08-25
writer: gsp-librarian
domain: library
sumber: legacy-archive/china-defence-expo-crawler-20260824T085128Z-1-001/china-defence-expo-crawler/outputs/07082026 0925/report.md
halaman: bagian 7
tanggal_akses: 2026-08-25
kelas_bukti: sintesis
sensitif: tidak
perkara: china-defence-expo-crawler
tags: [library, china-defence-expo-crawler, standar, pipeline, sumber, kueri]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/china-defence-expo-crawler/2026-08-25_cdec-pipeline-repeatable-sumber.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Pipeline repeatable China Defence Expo Crawler — sumber data & pustaka kueri

# Pipeline repeatable China Defence Expo Crawler — sumber data & pustaka kueri

## Ringkasan
Arsitektur pipeline terdokumentasi untuk re-eksekusi musim ekspo berikutnya: update source inventory → regional discovery (Wave 1) → enrichment (Wave 2) → synthesis (Wave 4) → build database (Wave 5) → verify (Wave 6).

## Sumber data utama (gratis)
- Situs resmi ekspo: cidexshow.com, securitychina.com.cn, ptexpo.com.cn, airshow.com.cn, bigdata-expo.cn, crsae.cn, sins-expo.com.
- Bahasa lokal: Baidu, Baidu Baike, Qichacha (free), Tianyancha (free), gsxt.gov.cn (registry korporat resmi), shifair/jufair/emagecompany (direktori exhibitor), c114.com.cn, cnetsec.com.
- OSINT: BIS Entity List, Pentagon CMCL (1260H), EU Dual-Use, OFAC, OpenSanctions.
- Konteks industri: SIPRI Open Data, IISS, forum pertahanan Tiongkok, white papers.

## Pustaka kueri (contoh, per region)
- CIDEX: `"CIDEX" "exhibitor" OR "参展商"`, `"中国国际国防电子展览会" 参展商名录`.
- Airshow: `"珠海航展" 参展商名录`, `"airshow.com.cn" Category_1377`.
- Enrichment: `"[vendor]" site:qichacha.com`, `"[vendor]" "BIS Entity List"`, `"[vendor]" "GJB" OR "国军标"`.

## Otomasi
- build_database.py (openpyxl, 133KB) → XLSX; generate_report.py (python-docx, 83KB) → DOCX synthesis; enrich_vendors.py → enrichment; generate_briefing_batch03.py, generate_narrative_batch*.py → briefing/narasi DOCX; fix_xlsx_merge.py → perbaikan kolom enrichment; verify_enrichment.py → verifikasi.
- Semua skrip tersedia di folder outputs (37 file .py; duplikat salinan (1)/(2)/(3) dianggap satu).

## Bukti
- Sumber: report.md bagian 7, daftar file skrip di folder outputs (dibaca 2026-08-25).
