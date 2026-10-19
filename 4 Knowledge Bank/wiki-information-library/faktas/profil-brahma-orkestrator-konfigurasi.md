---
id: profil-brahma-orkestrator-konfigurasi
type: fakta
title: Brahma Orkestrator — Identitas, Konfigurasi & Memori
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 4.1-4.3
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: digital
writer: gsp-librarian
tags: [brahma, orkestrator, konfigurasi]
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
catatan_verifikasi: "Riwayat: Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1. Status kembali usulan untuk verifikasi ulang custodian.. Verdict: terverifikasi || Alasan: Identitas/model/versi (v0.20.5 2026.8.19, upstream 057dcdf2, commit lokal 50e6507e patch ddgs _rescue_search) dan SELURUH nilai konfigurasi §4.2 (max_turns 500, reasoning medium, terminal local 180s, searxng/firecrawl, allow_private_urls, review_dispatch, delegation 250, memory 15.000+2.500, compression 0.5/0.2/20, telemetry false) cocok kajian baris 150-167; RAW kedua contract doc independen mencatat versi+commit yang sama; isi memori §4.3 cocok baris 171. Batas snapshot jujur. || Rekomendasi: Non-blocking: tidak ada."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/profil-brahma-orkestrator-konfigurasi.md
---

# Brahma Orkestrator — Identitas, Konfigurasi & Memori

Profil Brahma (orkestrator inti, profil `default`) — identitas & konfigurasi
(kajian §4.1–4.3):

- **Nama/Peran:** Brahma, AI Orchestrator GSP, mission-control Agent
  Headquarter. **Model:** `deepseek/deepseek-v4-flash-0731`, provider
  kilocode, base URL `https://api.kilo.ai/api/gateway`.
- **Vision auxiliary:** qwen3.7-flash (kilocode) untuk analisis gambar saat
  model utama tidak vision-native.
- **Versi Hermes:** v0.20.5 (2026.8.19); upstream `057dcdf2` + 2 commit lokal
  (`50e6507e` = patch fallback ddgs di web_tools.py `_rescue_search`).
- **Konfigurasi utama (§4.2):** `agent.max_turns: 500`, `reasoning_effort:
  medium`; `terminal.backend: local` (cwd `.`, timeout 180 s);
  `web.search_backend: searxng`, `web.extract_backend: firecrawl`;
  `browser.allow_private_urls: true`; `security.allow_private_urls: true`; `kanban.review_dispatch: true`;
  `delegation.max_iterations: 250`; `memory.memory_enabled: true` (limit 15.000
  char memori + 2.500 char profil user); `compression.enabled: true` (threshold
  0.5, target 0.2, protect last 20); `telemetry.shared_metrics.enabled: false`.
- **Memori persisten (§4.3):** 15.000 char memuat seluruh peta ekosistem
  (identitas user & repo GitHub, routing skill, fleet gateway watchdog, WebUI
  Brahma 9012, webstack lokal, konvensi fleet 34→40 profil, shared workspace,
  Agent Headquarter & Information Library, roster statis, prinsip "penulis
  adalah verifikator terlemah", dispatch pola HQ, RBAC, pipeline librarian,
  EKAS, mandat orkestrasi wajib 24-08-2026).

Sumber: `kajian_ekosistem_brahma.md` bab 4.1–4.3.

# Bukti

- SOUL: `~/.hermes/SOUL.md` — identitas GSP, gaya komunikasi, prinsip
  orkestrasi (kajian §4.1).
- Konfigurasi dibaca langsung dari config.yaml default (kajian §2 metode).

# Batas

- Nilai konfigurasi snapshot audit; perubahan config setelah audit tidak
  tercakup.
