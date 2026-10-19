---
id: gate-response-handling
type: fakta
title: "Penanganan respons bypass prompt: APPROVE_SET, DECLINE_SET, timeout, ambiguous, explanation mode"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/01a_gate_prompt_design.md
halaman: 01a_gate_prompt_design.md §3-4 (baris 279-435)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, response-handling, prompt]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gate-response-handling.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Penanganan respons bypass prompt: APPROVE_SET, DECLINE_SET, timeout, ambiguous, explanation mode

Matching case-insensitive: **APPROVE_SET** = {y, yes, yeah, yep, ya, iya, oke, ok, skip, go, lanjut, langsung} → bypass approval / direct execution; **DECLINE_SET** = {n, no, nope, tidak, tdk, nggak, full, orchestrate, orchestration, workflow} → full orchestration; kosong / timeout 30s → default full orchestration (tanpa re-prompt); teks tak dikenali (maybe, ?) → diperlakukan sebagai decline (konservatif). Jika user bertanya (kenapa/what/explain) → explanation mode (template penjelasan klasifikasi + perbedaan direct vs orchestration), lalu re-prompt HANYA sekali; respons kedua masih ambigu → decline. Algoritma: normalize → cek APPROVE → cek DECLINE → cek question words → else decline. [R — 01a_gate_prompt_design.md §3-4, baris 279-435]
