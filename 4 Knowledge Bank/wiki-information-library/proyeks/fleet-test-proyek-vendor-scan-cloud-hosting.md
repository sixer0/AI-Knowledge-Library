---
id: fleet-test-proyek-vendor-scan-cloud-hosting
type: proyek
title: "Vendor scan plan - penyedia cloud hosting (profil target + template scan)"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-vendor-crawler-specialist/vendor_scan_plan.md
halaman: hal. 2-5 (Profil Vendor Target; Template Scan; Compliance Gate; Asumsi)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: corporate
writer: gsp-librarian
tags: [vendor, cloud-hosting, scan, template, corporate, procurement]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-proyek-vendor-scan-cloud-hosting.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Vendor scan plan - penyedia cloud hosting (profil target + template scan)


Vendor scan plan untuk penyedia cloud hosting (persiapan Stage 1-2 pipeline intelijen vendor; tanpa fetch) [sumber — vendor_scan_plan.md hal. 2-5]:
Goals format G-5: kuantitatif — vendor memenuhi kriteria minimum >= 5; rentang harga publik per tier VPS/VM (bukan "price on request"); SLA uptime >= 99.9% tertulis. Kualitatif — lokasi data center publik (preferensi Indonesia/Singapura); kanal dukungan + SLA respons tertulis; sertifikasi ISO 27001/SOC 2 bila ada.

Field kontrak per record: vendor[] (vendor_id, name_en, name_local, website_url, country, lang, source_url, source_type, fetched_at, data_quality_flag); product[] (kategori VPS/Dedicated/Managed/Cloud PaaS); product_enrichment[] (price_min/max, currency ISO 4217, sla_uptime, dc_locations, support_channels, qualifications, price_not_public).

Template scan (hierarki authority 4 kategori): official vendor site -> halaman pricing (/pricing, /plans) -> review/comparison aggregator -> SLA/trust center (/sla, /trust-center, /legal).

Compliance gate (D.1-D.6): robots.txt pre-request (RFC 9309, cache <= 24 jam), hormati Disallow + Crawl-delay; rate limit 1 req/10-15 s per domain + backoff 429/503; UA deskriptif bertanda bot + kontak; skip-if-forbidden (login wall, CAPTCHA, ToS larang); PII vs business data (kontak person = PII, lawful basis EDPB 03/2026); source citation per record (source_url + source_type + fetched_at).

Asumsi ber-flag `assumption`: region default SEA + global (EN kanonik, name_local untuk versi lokal); kedalaman enrichment standard; seed list generik (belum diverifikasi — verifikasi cross-source minimal 2 sumber di Stage 3).

Kelas bukti: sekunder (persiapan tanpa eksekusi fetch; seluruh field fetched_at diisi saat pipeline dijalankan).
