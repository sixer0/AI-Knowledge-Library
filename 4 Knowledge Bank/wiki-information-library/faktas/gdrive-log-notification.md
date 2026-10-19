---
id: gdrive-log-notification
type: fakta
title: "Format log GDrive BLOCKED:GDRIVE_* + severity + notifikasi user end-of-task + throttle 250ms"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/02a_gdrive_error_handling.md
halaman: 02a_gdrive_error_handling.md §6 (baris 605-678), §7.2 (baris 708-731)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, gdrive, logging, notification]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gdrive-log-notification.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Format log GDrive BLOCKED:GDRIVE_* + severity + notifikasi user end-of-task + throttle 250ms

Setiap error GDrive WAJIB di-log: `[BLOCKED:GDRIVE_<ERROR_CODE>] <phase>/<file> — <error_message> — attempt <N>/<max> — action: <action>` dengan kode seperti AUTH, RATE_LIMIT, TIMEOUT, NO_FOLDER, SHARE_PERMISSION, QUOTA_EXCEEDED, LARGE_FILE, SCRIPT_ERROR, SUBPROCESS_TIMEOUT. Severity: CRITICAL (script/dep hilang), ERROR (auth/quota/script), WARNING (transient/share/large/missing folder), INFO (conflict). Ditulis ke `status_tasks.md` (tabel GDrive Push Errors) dan `gdrive_sync_report.md` (Failed Uploads + summary). Notifikasi user TIDAK real-time — hanya di end-of-task summary (total artifacts, synced, local-only, share missing, quota). Preventif rate limit: throttle queue 250ms antar call (~4 calls/s) + respect Retry-After + dedup check + upload counter. [R — 02a_gdrive_error_handling.md §6-7.2, baris 605-731]
