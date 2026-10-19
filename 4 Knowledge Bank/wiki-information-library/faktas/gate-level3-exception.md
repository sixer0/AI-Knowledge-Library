---
id: gate-level3-exception
type: fakta
title: "Modifikasi LEVEL 3 rule: exception request-translator hanya untuk SMALL + persetujuan user"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/01_scope_assessment_gate.md
halaman: 01_scope_assessment_gate.md §LEVEL 3 Rule Modification (baris 322-336); 01_enforcement_rules.md §2.6 (baris 290-294)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, level3, request-translator]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gate-level3-exception.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Modifikasi LEVEL 3 rule: exception request-translator hanya untuk SMALL + persetujuan user

Aturan lama: `NEVER skip request-translator for any request`. Aturan baru: `NEVER skip request-translator for any request — EXCEPT when Scope Assessment Gate (Step A0) classifies task as SMALL AND user explicitly approves bypass via confirmation prompt`. Rasional: gate berjalan SEBELUM scope aturan ini berlaku; exception didefinisikan sempit — hanya SMALL + persetujuan eksplisit user. FULL dan AMBIGUOUS selalu melewati request-translator. Ini satu-satunya rule yang perlu dimodifikasi; semua aturan lain tetap utuh. [R — 01_scope_assessment_gate.md §LEVEL 3 Rule Modification, baris 322-336]
