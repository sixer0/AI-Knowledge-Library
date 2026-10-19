---
id: infrastruktur-autostart-watchdog-docker-tailscale
type: fakta
title: Infrastruktur Operasional — Autostart, Watchdog, Docker & Tailscale
status: active
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 10.1-10.5
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: operations
writer: gsp-librarian
tags: [infrastruktur, autostart, watchdog, docker, tailscale]
links: [inventaris-layanan-port-ekosistem]
penulis: dashboard
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: Seluruh butir terverifikasi terhadap kajian §10.1-10.6 (baris 433-473): urutan autostart dependency-first 1/6 PostgreSQL 5433 sampai 6/6 hq 9011 dengan idempotency health-check/port-listening; dua job cron dengan id 19ae9f96d588 (every 180m, ok) dan f6ffb5e61aa7 (tiap 3 jam :55, status error 22:55) beserta pitfall PID MSYS vs Windows; stack Docker Firecrawl (api 3002, playwright-service, redis, rabbitmq, nuq-postgres, foundationdb+init) dan konfigurasi SearXNG 8080 dengan engine bing weight 2, mojeek, qwant, yep, presearch serta google/ddg/brave/startpage diblokir IP; PostgreSQL 5433 bus gsp_agent_hq PG17, 5432 legacy, MySQL 3306; node tailscale desktop-br2dlt9 100.102.23.27 dengan akses remote https://100.102.23.27:9012 self-signed, WSL2 NAT + Hyper-V firewall; komponen adjacent n8n-data, open-webui, crawler-admin, ops autocrawl, cloudflared.exe, OpenVPN, add-rules.ps1, hermes-backup-before-gsp-20260824/, code/, ai-agent-messaging/. Tidak ada angka yang menyimpang. Renik non-blocking: frontmatter `halaman: bab 10.1-10.5` padahal body dan baris sumber menyebut §10.1-10.6 (isi §10.6 dipakai); body sudah menyebut rentang lengkapnya sehingga provenans tetap dapat dipulihkan. Kelas bukti primer sesuai (verifikasi live docker ps/netstat/tasklist/tailscale, kajian §2). || Rekomendasi: Siap dipromosikan. Sunting status `terverifikasi` -> `ditinjau` sebelum promote (aturan I1) dan perlebar `halaman` menjadi 'bab 10.1-10.6'. Catat untuk kurator: objek ini memuat alamat IP mesh dan id cron host - kebijakan korpus sudah menandai sensitif=tidak dan tidak ada nilai secret yang disalin (kajian §16.C hanya mendaftar nama kunci), tetapi keputusan sensitivitas tetap wewenang librarian/user. || Riwayat: catatan_verifikasi sebelumnya (custodian 2026-08-25 perlu_revisi, direvisi librarian Wave B fix-h1) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/infrastruktur-autostart-watchdog-docker-tailscale.md
catatan_keputusan: "dipromosikan: IL-INGEST-01 B1a pilot: verdict custodian terverifikasi (C-B1a-verdict.md), cek YAML kelas-I5 lulus, non-sensitif non-dosir"
---

# Infrastruktur Operasional — Autostart, Watchdog, Docker & Tailscale

Infrastruktur operasional ekosistem GSP — autostart, watchdog, Docker,
PostgreSQL, jaringan (kajian §10.1–10.6):

- **Autostart (§10.1):** Task Scheduler saat logon → `start-ecosystem.bat` →
  `gsp-ecosystem-start.sh`; urutan dependency-first 1/6 PostgreSQL (5433) →
  2/6 bridge → 3/6 gateway → 4/6 dashboard (9010) → 5/6 webui (9012) →
  6/6 hq (9011); idempotent (health check ATAU port-listening).
- **Watchdog & cron (2 job, §10.2):**
  - GSP Watchdog WebUI & HQ (`19ae9f96d588`, every 180m, script-only) — ok.
  - GSP Fleet Gateway Watchdog (`f6ffb5e61aa7`, tiap 3 jam :55, script-only)
    — **error** (22:55) saat audit.
  - Pitfall: PID MSYS vs Windows (fallback PowerShell di versi WebUI/HQ).
- **Docker (§10.3):** Firecrawl self-hosted (api 3002, playwright-service,
  redis, rabbitmq, nuq-postgres, foundationdb+init) — up 10 jam; SearXNG
  (8080): use_default_settings + json + limiter false; engine aktif bing
  (weight 2), mojeek, qwant, yep, presearch; google/ddg/brave/startpage
  diblokir IP.
- **PostgreSQL (§10.4):** 5433 = bus utama `gsp_agent_hq` (PG 17); 5432 =
  instance kedua (legacy/lain); MySQL 3306 listening juga.
- **Jaringan & Tailscale (§10.5):** node `desktop-br2dlt9` (100.102.23.27);
  WebUI diakses remote via `https://100.102.23.27:9012` (self-signed);
  WSL2 NAT + Hyper-V firewall allow untuk port Docker.
- **Komponen adjacent (§10.6):** n8n-data, open-webui, crawler-admin, ops/
  autocrawl watchdog, cloudflared.exe, OpenVPN, add-rules.ps1,
  hermes-backup-before-gsp-20260824/, code/, ai-agent-messaging/, dll.

Sumber: `kajian_ekosistem_brahma.md` bab 10.1–10.6.

# Bukti

- Semua service diverifikasi live saat audit (docker ps, netstat, tasklist,
  tailscale status — §2).

# Catatan

- Temuan terkait: F7 (PID MSYS tidak andal), F12 (adjacent tidak terkelola).
