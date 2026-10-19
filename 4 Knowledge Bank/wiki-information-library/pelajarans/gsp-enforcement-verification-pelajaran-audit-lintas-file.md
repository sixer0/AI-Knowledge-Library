---
id: gsp-enforcement-verification-pelajaran-audit-lintas-file
type: pelajaran
title: "Pelajaran — audit lintas-file (per-rule, per-line) menangkap konflik perilaku antar skill file"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement-verification/audit_report.md
halaman: Key Findings (baris 201-212); Recommendations (baris 214-217)
tanggal_akses: 2026-08-25
kelas_bukti: sintesis
sensitif: tidak
perkara: gsp-enforcement-verification
domain: digital
writer: gsp-librarian
tags: [gsp, orchestration, enforcement, lesson, audit]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement-verification/2026-08-25_gsp-enforcement-verification-pelajaran-audit-lintas-file.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Pelajaran — audit lintas-file (per-rule, per-line) menangkap konflik perilaku antar skill file

Pelajaran dari sub-siklus verifikasi enforcement: **audit lintas-file (per-rule, per-line) diperlukan untuk menangkap konflik perilaku antar skill file** (audit_report.md Key Findings baris 201-212, Recommendations baris 214-217).

- Audit per-file yang terisolasi menghasilkan PASS; konflik BLOCKING vs NON-BLOCKING hanya terlihat saat check yang sama ditelusuri DI KEDUA file (orchestrator Step E13 vs documentation-contract Rule 13 / Sub-Agent Completion Gate).
- enforcement-audit-report.md (baris 236-241) menegaskan: "No rules found that are only documented without being embedded in workflow steps" namun tetap mencatat minor inconsistency antar file.
- Rekomendasi audit: (1) resolve conflict blocking vs non-blocking — samakan di kedua file; (2) tambahkan header eksplisit Rule 14-15 di documentation-contract (saat audit, aturan itu implicit).

Implikasi: verifikasi kepatuhan tidak cukup satu file per file — perlu lintas-file consistency check untuk aturan yang sama yang ter-kodifikasi di beberapa tempat.
