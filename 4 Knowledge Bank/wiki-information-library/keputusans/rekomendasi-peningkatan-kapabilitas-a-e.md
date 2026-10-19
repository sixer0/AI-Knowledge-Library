---
id: rekomendasi-peningkatan-kapabilitas-a-e
type: keputusan
title: Rekomendasi Peningkatan Kapabilitas Ekosistem GSP (A-E)
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 15
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: operations
writer: gsp-librarian
tags: [rekomendasi, peningkatan, roadmap]
links: [temuan-audit-f1-f12]
penulis: dashboard
diajukan: 2026-08-25
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Riwayat: Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1. Status kembali usulan untuk verifikasi ulang custodian.. Verdict: terverifikasi || Alasan: 15 rekomendasi dalam 5 kelompok (A2+B4+C3+D3+E3=15) cocok verbatim kajian §15 baris 538-561; RAW kedua tabel §14 baris 521-532 mengonfirmasi pasangan rekomendasi-temuan (F1-A1, F2-B3, F7-B4, F8-C8, F9-D10, F10-C9, E13-15 keamanan); catatan 'belum tentu dieksekusi' jujur. || Rekomendasi: Non-blocking: tidak ada."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: keputusans/rekomendasi-peningkatan-kapabilitas-a-e.md
---

# Rekomendasi Peningkatan Kapabilitas Ekosistem GSP (A-E)

Rekomendasi peningkatan kapabilitas ekosistem GSP (kajian §15, 15 rekomendasi
dalam 5 kelompok):

**A. Konsolidasi Identitas & Roster**
1. Sinkronkan ROSTER ↔ profil disk: rename/alias `gsp-crawler-orchestrator`;
   update komentar jumlah; tes idempoten `add_hq_roster.py`.
2. Validasi CI/script: setiap profil baru wajib masuk ROSTER + komentar jumlah.

**B. Keandalan Operasional**
3. Hidupkan ulang gateway fleet (`bash gsp_gateway_watchdog.sh --restart`);
   perbaiki penyebab status error cron.
4. Ganti mekanisme PID file dengan pengecekan port/state Hermes native
   (`hermes -p <p> gateway status`).
5. Otomasi health-check harian (9010/9011/9012/bridge/docker/gateway →
   kanban/DataStore).
6. Rekonsiliasi 2 kartu blocked + 2 AgentRequest failed/rejected dengan
   decision log.

**C. Knowledge & Skill Management**
7. Formalikan pipeline RAW→VAULT→WIKI; pemilik per vault project; otomasi
   proposal librarian.
8. Bangun sinkronisasi skill kanonik → per-profil (single source of truth +
   hash) untuk F8.
9. Lengkapi rantai jaminan EKAS yang PUTUS + isi R1 (regulasi Indonesia)
   berprovenans; verifikasi rutin rujukan eksternal (mis. ONVIF).

**D. Kapabilitas Fleet**
10. Evaluasi penambahan extract_backend=firecrawl ke profil riset lain
    (rate limit) atau formalisasi fallback ddgs.
11. Perkuat profil vision: toolset terminal/read; dokumentasikan batas
    halusinasi qwen3.7-flash.
12. Pertimbangkan agen observability khusus untuk telemetry lintas profil.

**E. Keamanan & Hardening**
13. Rotasi & minimalkan secret; pastikan .env tidak ter-commit; TLS internal CA.
14. Tinjau RBAC: batasi role USER dari endpoint admin HQ; reset `_rbac_user`.
15. Audit firewall & exposure: konfirmasi tidak ada service terbuka ke internet
    selain via Tailscale.

Sumber: `kajian_ekosistem_brahma.md` bab 15.

# Bukti

- Rekomendasi berpasangan dengan temuan F1-F12 (kajian §14).
- Status: rekomendasi, belum tentu dieksekusi penuh saat audit.

# Catatan

- Tracking eksekusi rekomendasi ada di kanban/decision log orkestrasi (di luar
  dokumen audit ini).
