---
id: standar-kategori-scope
type: standar
title: "Standar kategori klasifikasi scope: 5 small + 5 orchestration + boundary rules"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/02_small_task_criteria.md
halaman: 02_small_task_criteria.md §Categories (baris 48-165), §Ambiguous Cases (baris 245-277)
tanggal_akses: 2026-08-25
kelas_bukti: sintesis
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, standard, classification, scope]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_standar-kategori-scope.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Standar kategori klasifikasi scope: 5 small + 5 orchestration + boundary rules

Taksonomi kategori scope task GSP dengan boundary rule per kategori: **Small (bypass eligible)** — single_file change (boundary: jika fix butuh 2+ file → bukan small), config update (boundary: multi config/service → bukan simple), restart/refresh (boundary: bagian deployment/migration → bukan simple), simple query (boundary: butuh analisis mendalam/cross-referencing → bukan simple), quick lookup (boundary: bagian investigasi/debugging besar → bukan simple). **Orchestration-required** — multi-file changes, new feature, architecture changes, database migrations, security-critical operations (masing-masing dengan contoh & rasional). Ambiguous default → orchestration konservatif, dengan 5 borderline indicators dan resolution strategy. Acceptance: ≥5 kategori small + 5 orchestration, boundary jelas, threshold testable. [R — 02_small_task_criteria.md §Categories, baris 48-165]
