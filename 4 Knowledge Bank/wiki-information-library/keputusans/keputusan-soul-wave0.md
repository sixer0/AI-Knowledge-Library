---
id: keputusan-soul-wave0
type: keputusan
title: "Keputusan: SOUL.md sebagai Primary Enforcement Layer (Wave 0) — file yang selalu di-load"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/report.md
halaman: report.md §SOUL.md Enforcement (baris 103-133); 03_integration_map.md §10 (baris 744-777)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, decision, soul-md, wave0]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_keputusan-soul-wave0.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Keputusan: SOUL.md sebagai Primary Enforcement Layer (Wave 0) — file yang selalu di-load

Setelah blueprint selesai ditemukan celah kritis: Hermes bisa me-bypass seluruh enforcement jika tidak auto-load orchestrator skill di session baru, tidak menjalankan Scope Assessment Gate, dan tidak push ke GDrive. Solusi: **SOUL.md (~/.hermes/SOUL.md)** sebagai primary enforcement layer karena file ini SELALU di-load di SETIAP session (satu-satunya yang tak bisa di-skip). Perubahan: identity "GSP Orchestrator — Master Controller" sebagai DEFAULT dan ONLY mode; MANDATORY auto-load `skill_view(name='gsp-orchestration/orchestrator')` di setiap session start; Rule 1 & Rule 2 inline penuh; LEVEL 3 exception; kewajiban GDrive push. Status: ALREADY IMPLEMENTED. Wave 0 dijalankan SEBELUM Wave 1-5 karena SOUL.md adalah entry point semua session. [R — report.md §SOUL.md, baris 103-133]
