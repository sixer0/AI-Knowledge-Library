---
id: fleet-test-proyek-pipeline-monitor-harga
type: proyek
title: "Desain pipeline monitor harga produk kompetitor (2 tahap)"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-crawler-orchestrator/pipeline_plan.md
halaman: hal. 1-2 (Ringkasan Pipeline; Tahap 1-2; Daftar Delegasi)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: digital
writer: gsp-librarian
tags: [crawler, pipeline, harga, kompetitor, orkestrasi, proyek]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-proyek-pipeline-monitor-harga.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Desain pipeline monitor harga produk kompetitor (2 tahap)


Desain pipeline monitor harga produk kompetitor (DESAIN SAJA; eksekusi crawl tidak dijalankan) [sumber — pipeline_plan.md hal. 1-2]:
STAGE 1 — KOLEKSI (delegasi paralel, output isolation): PRICE_COLLECT_COMPETITOR (gsp-vendor-crawler-specialist; crawl situs/e-commerce; compliance respectful crawling, rate limit 1 req/10-15 s, UA deskriptif) + PRICE_COLLECT_SOCIAL (gsp-social-media-crawler; jalur gratis searxng/firecrawl lokal). Output per unit: items.jsonl + manifest.
STAGE 2 — ANALISIS (single-writer merge): PRICE_SYNTHESIS (social-media-analyst/vendor synthesis) — merge seri + idempotent upsert, dedup via hierarki authority, sintesis min/max/median per produk; output price_report.md + citation_manifest.json.

Aturan orkestrasi: single allocator (tanpa overlap natural key per kompetitor); konkurensi N=3 default, domain-aware, throttle agregat <= 1 req/10-15 s per domain + backoff 429/503; status unit PRICE_UNIT_STARTED/COMPLETE/PARTIAL/FAILED/DEFERRED; data tidak ditemukan -> data_quality_flag=partial + tercatat, BUKAN difabrikasi; outlier ditandai asumsi.

Dependensi DAG: unit 1 & 2 paralel (independen) -> unit 3 setelah keduanya COMPLETE.

Kelas bukti: sekunder (dokumen desain; tanpa eksekusi fetch).
