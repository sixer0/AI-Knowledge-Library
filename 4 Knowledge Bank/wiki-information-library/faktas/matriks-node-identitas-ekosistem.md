---
id: matriks-node-identitas-ekosistem
type: fakta
title: Matriks Node & Identitas Ekosistem GSP
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 3.3
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: digital
writer: gsp-librarian
tags: [ekosistem-brahma, node, arsitektur]
links: [arsitektur-ekosistem-brahma-5-lapisan]
penulis: dashboard
diajukan: 2026-08-25
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Riwayat: Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1. Status kembali usulan untuk verifikasi ulang custodian.. Verdict: terverifikasi || Alasan: Tabel identik kajian §3.3 baris 131-142 (10 node); versi WebUI v0.51.792 dan Firecrawl v2.11.162 cocok tabel yang sama; RAW kedua contract doc mengonfirmasi path node (gsp-brahma 9012, gsp-datacenter 9011, Postgres 5433). Batas (path spesifik mesin) jujur. || Rekomendasi: Non-blocking: baris komponen adjacent sudah merujuk §10.6 - cukup."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/matriks-node-identitas-ekosistem.md
---

# Matriks Node & Identitas Ekosistem GSP

Matriks node & identitas utama ekosistem GSP (kajian §3.3):

| Node | Lokasi | Fungsi |
|---|---|---|
| Brahma | profil `default` (AppData/Local/hermes) | Orkestrator utama; gateway running |
| Agent Headquarter | `C:/Users/TRIAL/gsp-datacenter` | Dashboard Next.js 16 + API + Prisma |
| WebUI Brahma | `C:/Users/TRIAL/gsp-brahma` | Fork Hermes WebUI v0.51.792; RBAC multi-user |
| Bridge | `C:/Users/TRIAL/gsp-datacenter/hermes-bridge` | Penghubung bus DB ↔ CLI hermes |
| Ekosistem launcher | `C:/Users/TRIAL/gsp-ecosystem` | Autostart, watchdog, log, PID |
| Fleet workspace | `C:/Users/TRIAL/workspace/gsp-hermes` | Kanonik scripts + skills + workspace |
| EKAS | `C:/Users/TRIAL/gsp-ekas` | Korpus pengetahuan teknik |
| Firecrawl source | `C:/Users/TRIAL/firecrawl-src` | Compose self-hosted v2.11.162 |
| SearXNG | `C:/Users/TRIAL/searxng` | settings.yml + volume |
| Komponen adjacent | n8n-data, open-webui, crawler-admin, ops, cloudflared.exe | Proyek/utilitas lain di host (§10.6) |

Sumber: `kajian_ekosistem_brahma.md` bab 3.3 (tabel Node & Identitas).

# Bukti

- WebUI Brahma adalah fork Hermes WebUI v0.51.792 (kajian §3.3, §5.x).
- Firecrawl compose v2.11.162 (kajian §3.3, §10.3).

# Batas

- Path lokal spesifik mesin audit (mesin Windows ini); jangan diasumsikan
  identik di mesin lain.
