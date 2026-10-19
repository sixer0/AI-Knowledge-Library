---
id: gdrive-error-s1-s10-4-kelas
type: fakta
title: "Error handling GDrive push: 10 skenario (S1-S10), 4 kelas error, retry logic, 7 fallback tiers"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/02a_gdrive_error_handling.md
halaman: 02a_gdrive_error_handling.md §1 (baris 23-43), §3 (baris 430-444), §4 (baris 447-519), §5 (baris 522-561)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, gdrive, error-handling, fallback]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gdrive-error-s1-s10-4-kelas.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Error handling GDrive push: 10 skenario (S1-S10), 4 kelas error, retry logic, 7 fallback tiers

Sepuluh skenario: S1 auth failure (PERMISSION, retry 1x refresh), S2 rate limit 429 (TRANSIENT, 3x exponential 2→4→8s), S3 network timeout (TRANSIENT, 1x + timeout 60s), S4 missing parent folder (LOGIC, 1x auto-create), S5 permission API fail (PERMISSION, 0x — file ter-upload, share manual), S6 quota exceeded (RESOURCE, 0x — skip semua sisa), S7 file conflict (LOGIC, 0x — GDrive versioning), S8 large file >10MB (RESOURCE, 1x resumable, kompres opsional), S9 google_api.py script error (LOGIC, 1x fix args), S10 subprocess hang (TRANSIENT, 1x kill+retry). Semua Block? = NO. Empat kelas: TRANSIENT / PERMISSION / LOGIC / RESOURCE dengan recovery strategy berbeda. Tujuh fallback tiers: Tier 0 normal → Tier 6 critical (script hilang, skip semua GDrive); semakin tinggi tier semakin banyak operasi di-skip, tapi orkestrasi tetap berjalan. [R — 02a_gdrive_error_handling.md §1,3,4,5, baris 23-561]
