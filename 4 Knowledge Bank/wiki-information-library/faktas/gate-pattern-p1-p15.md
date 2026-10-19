---
id: gate-pattern-p1-p15
type: fakta
title: "15 pattern klasifikasi (P1-P15) + 3 heuristik estimasi step + aturan prioritas"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/01_scope_assessment_gate.md
halaman: 01_scope_assessment_gate.md §Pattern Matching (baris 153-192), §Step Count Estimation (baris 94-132); 01_enforcement_rules.md §2.3 (baris 147-205)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, classification, pattern, heuristic]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gate-pattern-p1-p15.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# 15 pattern klasifikasi (P1-P15) + 3 heuristik estimasi step + aturan prioritas

Pattern scope berbasis keyword/regex: **P1-P5 SMALL** (single_file, config_update, restart, simple_query, quick_lookup), **P6-P10 FULL** (multi_file, new_feature, architecture, db_migration, security), **P11-P15 AMBIGUOUS** (generic verb tanpa target, open-ended investigation, multi small task gabung, user-facing functionality, external dependency). Aturan prioritas: FULL > AMBIGUOUS > SMALL; FULL+AMBIGUOUS → FULL (lebih spesifik). Estimasi step memakai 3 heuristik:

- (1) indikator verb eksplisit — 1 verb = 1 step, 2 verb "lalu/setelah" = 2, 3+ verb / rantai "dan" = 3+/FULL, tanpa verb jelas = AMBIGUOUS;
- (2) kompleksitas implisit dari tipe task (read-only = 1, edit+verify = 2-3, multi-component = 4+/FULL, investigasi = AMBIGUOUS);
- (3) constraint eksplisit user ("langsung saja" = lower bound 1, "dengan test" = +2, "update docs" = +1, "step by step" = pref orkestrasi). [R — 01_scope_assessment_gate.md §Pattern Matching & §Step Count Estimation, baris 94-192]
