---
id: gate-threshold-t1-t12
type: fakta
title: "12 threshold rules klasifikasi (T1-T12): 5 small, 6 orchestration, 1 ambiguous"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/02_small_task_criteria.md
halaman: 02_small_task_criteria.md §Threshold Rules (baris 20-44); 01_enforcement_rules.md §2.3 (baris 122-145)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, classification, threshold, t1-t12]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gate-threshold-t1-t12.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# 12 threshold rules klasifikasi (T1-T12): 5 small, 6 orchestration, 1 ambiguous

Kriteria testable untuk bypass: **T1-T5 SMALL** — steps ≤ 3 AND scope ∈ {single_file (T1), config_update (T2), restart/refresh (T3), simple_query (T4), quick_lookup (T5)}; **T6-T11 ORCHESTRATION** — steps > 3 (T6) atau steps ≤ 3 AND scope ∈ {multi_file (T7), new_feature (T8), architecture (T9), db_migration (T10), security (T11)}; **T12 AMBIGUOUS** — scope ambiguous/borderline (any steps) → orchestration konservatif. Setiap rule punya rationale eksplisit. Formula keputusan: SMALL hanya jika steps ≤ 3 DAN scope di set 5 kategori kecil; selain itu orchestration required tanpa konfirmasi. [R — 02_small_task_criteria.md §Threshold Rules, baris 20-44]
