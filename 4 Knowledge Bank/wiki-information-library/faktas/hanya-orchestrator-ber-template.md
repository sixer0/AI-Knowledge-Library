---
id: hanya-orchestrator-ber-template
type: fakta
title: "Hanya gsp-orchestrator yang punya linked templates; tidak ada references/scripts/assets"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-17_gsp_orchestration_skill_report/01_explore.md
halaman: 01_explore.md §6 (hal. 270–282); 99_implementation_report.md §8 obs #8 (hal. 470)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: gsp-orchestration-skill-report
tags: [gsp, orchestration, templates, linked-files]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-orchestration-skill-report/2026-08-25_hanya-orchestrator-ber-template.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Hanya gsp-orchestrator yang punya linked templates; tidak ada references/scripts/assets

Dari 35 skill, **hanya `orchestrator/` yang memiliki subdirektori** — `templates/` berisi **16 file .md.tpl** (358 LOC) untuk setiap jenis artefak alur GSP (01_translated, 02_structured, 01_explore, 02_collection, 03_analysis, 01_specs, 02_plan, 99_implementation_report, 01_gate_report, 01_test_report, 01_verification, 02_security, report, decisions, status_tasks, delegation_progress_report). Tidak ada satupun skill yang menggunakan `references/`, `scripts/`, atau `assets/` — kapabilitas linked-files termanfaatkan minim. [R — 01_explore.md §6, hal. 270–282]
