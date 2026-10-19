---
id: gate-hil-a0-checklist
type: fakta
title: "GATE-A0 di HIL Gates Master Table + item baru Enforcement Checklist + struktur orchestrator"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/01_gate_insertion_point.md
halaman: 01_gate_insertion_point.md §4.3-4.4 (baris 160-192); 01_scope_assessment_gate.md §Enforcement Checklist & HIL (baris 338-390)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, hil-gate, checklist, gate-a0]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gate-hil-a0-checklist.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# GATE-A0 di HIL Gates Master Table + item baru Enforcement Checklist + struktur orchestrator

Tiga sisipan ke orchestrator/SKILL.md: (1) **GATE-A0** di HIL Gates Master Table — fase "A.0 (Pre-Phase A)", trigger "Every user request", skip rule "Never skip — always classify", default bila tanpa respons = full orchestration (konservatif); (2) satu item baru di Enforcement Checklist SEBELUM item "Apakah saya sudah call request-translator first?": "Apakah Scope Assessment Gate (Step A0) sudah dijalankan sebelum Phase A?" dengan cabang SMALL+approve → direct execution, selain itu → lanjut Step A1; (3) struktur orchestrator menempatkan Step A0 di depan A1-A5b (Phase A), B–J tidak berubah. [R — 01_gate_insertion_point.md §4.3-4.4, baris 160-192]
