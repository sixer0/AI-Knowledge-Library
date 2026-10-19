---
id: dual-path-gsp-orchestrator
type: fakta
title: "Dual path gsp-orchestrator: dua lokasi instalasi skill, versi aktif dengan templates"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-17_gsp_orchestration_skill_report/99_implementation_report.md
halaman: 99_implementation_report.md §8 obs #2 (hal. 458); 01_specs.md §6 edge #3 (hal. 478)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: gsp-orchestration-skill-report
tags: [gsp, orchestration, duplicate, skill-path]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-orchestration-skill-report/2026-08-25_dual-path-gsp-orchestrator.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Dual path gsp-orchestrator: dua lokasi instalasi skill, versi aktif dengan templates

Skill `gsp-orchestrator` ada di **dua lokasi**: `~/.hermes/skills/gsp-orchestrator/` dan `~/.hermes/skills/gsp-orchestration/orchestrator/`. Laporan menggunakan versi `gsp-orchestration/orchestrator/` karena memiliki set lengkap 16 template. Kondisi dual-path berpotensi menyebabkan ambiguitas pemuatan skill dan harus dipantau saat maintenance. [R — 99_implementation_report.md §8 obs #2, hal. 458]
