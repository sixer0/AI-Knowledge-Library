---
id: gsp-orchestration-naming-convention
type: fakta
title: "Naming convention direktori skill GSP: prefix gsp- di-drop, phase-*/sub-*, gsp-agent-catalog tetap"
status: active
domain: digital
writer: gsp-librarian
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-17_gsp_orchestration_skill_report/99_implementation_report.md
halaman: §5.1 (baris 332-346)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: gsp-orchestration
tags: [orchestration, skills, naming-convention, gsp, ai-systems]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-orchestration/2026-08-25_gsp-orchestration-naming-convention.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Naming convention direktori skill GSP: prefix gsp- di-drop, phase-*/sub-*, gsp-agent-catalog tetap

Sistem skill Hermes menerapkan konvensi penamaan direktori yang sistematis (99_implementation_report.md §5.1 baris 332-346; 01_explore.md §4 baris 191-205):
- `gsp-` di-drop dari nama direktori: `gsp-orchestrator` → `orchestrator/`, `gsp-documentation-contract` → `documentation-contract/`, dst.
- `gsp-phase-*` (6 skill) → `phase-*`.
- `gsp-sub-*` (24 skill: S1-S13, T1-T9, U1-U2) → `sub-*`.
- `gsp-agent-catalog` → `gsp-agent-catalog/` (satu-satunya yang mempertahankan prefix penuh).

Field `name` di frontmatter YAML tetap menyimpan nama lengkap (mis. `name: gsp-sub-explore`) (01_explore.md §4 baris 205). Konvensi 100% konsisten (02_collection.md Naming Convention Audit baris 196-206); tidak ada penyimpangan yang dilaporkan.
