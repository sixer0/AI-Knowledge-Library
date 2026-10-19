---
id: gate-edge-cases-ec1-ec7
type: fakta
title: "7 edge cases Scope Assessment Gate (EC1-EC7) dengan penanganan eksplisit"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/01_scope_assessment_gate.md
halaman: 01_scope_assessment_gate.md §Edge Cases (baris 394-509); 01_enforcement_rules.md §2.6 (baris 312-322)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, edge-cases, gate]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gate-edge-cases-ec1-ec7.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# 7 edge cases Scope Assessment Gate (EC1-EC7) dengan penanganan eksplisit

EC1 user minta orkestrasi untuk task kecil → honor, log `user_override: true`. EC2 user minta bypass untuk task orkestrasi → DENY + jelaskan, log `bypass_denied: true`. EC3 multi-part (sebagian kecil, sebagian penuh) → ANY part FULL = seluruh request FULL, silent. EC4 request terlalu pendek/tidak jelas ("fix it") → AMBIGUOUS → Phase A, request-translator menangani klarifikasi. EC5 false positive SMALL (kompleksitas > estimasi) → stop, notifikasi user, tawarkan switch ke orkestrasi (safety valve / escalation mid-execution). EC6 timeout prompt 30s → default orkestrasi, tanpa re-prompt. EC7 user bertanya tentang klasifikasi → penjelasan transparan dengan template. [R — 01_scope_assessment_gate.md §Edge Cases, baris 394-509]
