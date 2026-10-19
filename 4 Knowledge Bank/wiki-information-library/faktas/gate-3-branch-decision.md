---
id: gate-3-branch-decision
type: fakta
title: "Klasifikasi 3 cabang Scope Assessment Gate: SMALL / FULL / AMBIGUOUS + formula inti"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/01_scope_assessment_gate.md
halaman: 01_scope_assessment_gate.md §Three Classification Outcomes (baris 82-88); 01_enforcement_rules.md §2.2 (baris 55-116)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, classification, decision-tree]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gate-3-branch-decision.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Klasifikasi 3 cabang Scope Assessment Gate: SMALL / FULL / AMBIGUOUS + formula inti

Gate menghasilkan tiga outcome: **SMALL** (steps ≤ 3 AND scope ∈ {single_file, config_update, restart, simple_query, quick_lookup} → bypass prompt `[Y/n]`, user putuskan direct exec atau orchestration), **FULL** (steps > 3 ATAU scope ∈ {multi_file, new_feature, architecture, db_migration, security} → silent, langsung Phase A), dan **AMBIGUOUS** (scope tidak jelas / borderline → silent, default konservatif ke orkestrasi). Formula inti: `IF steps ≤ 3 AND scope ∈ set-small → SMALL; ELSE → ORCHESTRATION REQUIRED`. Design principle: conservative default — ambiguous selalu orchestration, zero overhead untuk task penuh (prompt hanya untuk SMALL), user sovereignty (bisa override, dengan penjelasan). [R — 01_scope_assessment_gate.md §Three Classification Outcomes, baris 82-88]
