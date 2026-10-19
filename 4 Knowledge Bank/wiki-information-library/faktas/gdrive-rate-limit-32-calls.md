---
id: gdrive-rate-limit-32-calls
type: fakta
title: "Beban API GDrive per-sub-agent: ~32 calls vs limit 75K/hari (0.04% kuota)"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/03_gdrive_integration_points.md
halaman: 03_gdrive_integration_points.md §Rate Limit Analysis (baris 77-119)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, gdrive, rate-limit, api]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gdrive-rate-limit-32-calls.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Beban API GDrive per-sub-agent: ~32 calls vs limit 75K/hari (0.04% kuota)

Google Drive API v3 limits (per May 2026): read 100.000 requests/user/day, write 75.000 requests/user/day, upload bandwidth 750 GB/user/day, per-file max 5 TB, resumable session expires setelah 1 jam. Estimasi per task tipikal GSP: ~16 sub-agents → ~16 uploads → ~32 API calls (upload + share) = **0,04% kuota harian**; bahkan 10 task konkuren (~320 calls) tetap diabaikan. `upload` memakai resumable MediaFileUpload (rate-limit friendly). Bottleneck potensial: tiap call gsp-drive-sync.py spawn subprocess baru ke google_api.py (~1-2s overhead) — untuk 16 sub-agents ≈ 16-32s total, diterima karena sub-agents selesai asinkron. [R — 03_gdrive_integration_points.md §Rate Limit Analysis, baris 77-119]
