---
id: arsitektur-ekosistem-brahma-5-lapisan
type: fakta
title: Arsitektur Ekosistem Brahma GSP — 5 Lapisan
status: active
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 1 & 3.1
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: digital
writer: gsp-librarian
tags: [ekosistem-brahma, arsitektur, gsp-fleet]
links: [gsp-subagent-model-map-pemetaan-subagent]
penulis: dashboard
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: Kelima lapisan cocok verbatim dengan kajian §1 baris 22-28 dan diagram §3.1 baris 67-112. Semua angka terverifikasi ulang dari sumber RAW: 42 agen roster API (41 statis + 1 dinamis, baris 31 dan 513), 128 SKILL.md registry 20 kategori + 12 kanonik EKAS (baris 32, §8.1 baris 373, 376), DB AgentRequest 42/HermesTask 43/HermesMemory 54/OrchestrationRecord 39/AgentEvent 95 (baris 33, tabel §5.4), EKAS 270 file teks + 430 file lengkap (§9.2 baris 398), Wiki 54 entri (§9.3 baris 405), IL 1.996 entri (§9.4 baris 411), kanban 47 kartu (§9.6 baris 426), port 9011/9012/9010/5433/8080/3002 (§3.2 baris 118-127), 5 agen crawl firecrawl (§7.6 baris 365). Tidak ada dimensi yang gagal. Provenans lengkap (sumber + rujukan bab), YAML valid, satu baris status, title==H1, kelas_bukti primer jujur (dokumen audit primer), grouping domain digital sesuai isi, links `gsp-subagent-model-map-pemetaan-subagent` terbukti ada di vault dan wiki. || Rekomendasi: Siap dipromosikan librarian. Saat promosi, sunting baris status `terverifikasi` menjadi `ditinjau` lebih dulu (aturan I1) dan salin rujukan silang ke objek port serta IL entri. Sensitif=tidak dan non-dosir, jadi tidak butuh gerbang manusia. || Riwayat: catatan_verifikasi sebelumnya (custodian 2026-08-25 perlu_revisi, direvisi librarian Wave B fix-h1) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/arsitektur-ekosistem-brahma-5-lapisan.md
catatan_keputusan: "dipromosikan: IL-INGEST-01 B1a pilot: verdict custodian terverifikasi (C-B1a-verdict.md), cek YAML kelas-I5 lulus, non-sensitif non-dosir"
---

# Arsitektur Ekosistem Brahma GSP — 5 Lapisan

Ekosistem GSP adalah sistem multi-agen AI self-hosted yang berpusat pada Brahma
(AI Orchestrator PT. Gemilang Satria Perkasa), dioperasikan dari GSP Agent
Headquarter. Terdiri dari **5 lapisan** (kajian §1, §3.1):

1. **Kokpit & Antarmuka** — Agent Headquarter (Next.js, port 9011, HTTPS),
   WebUI Brahma (fork Hermes WebUI, port 9012, HTTPS), Dashboard Hermes (9010).
2. **Bus Pesan & Bridge** — PostgreSQL 17 (port 5433) sebagai message bus +
   `hermes-bridge` (Node.js) menjembatani dashboard dengan CLI `hermes`.
3. **Fleet Agen** — 40 profil agen spesialis `gsp-*` (+ `default` = Brahma,
   + `user01` = user WebUI), masing-masing dengan SOUL.md, model
   (deepseek-v4-flash-0731 via kilocode; 4 profil vision qwen3.7-flash),
   toolset, dan skill sendiri.
4. **Webstack Riset** — SearXNG lokal (Docker, port 8080, backend pencarian)
   dan Firecrawl self-hosted (Docker, port 3002, backend ekstraksi); 5 agen
   crawl punya akses Firecrawl.
5. **Knowledge & Memory** — Shared workspace (Brahma Fleet), EKAS (270 file
   teks + 430 file lengkap), Wiki (54 entri), Information Library (1.996
   entri), Vault (staging librarian), kanban (47 kartu).

Skala terukur saat audit 24-08-2026: **42 agen** dalam roster API (41 statis +
1 dinamis WebUI); 128 SKILL.md di registry default (20 kategori) + 12 skill
rekayasa EKAS kanonik; DB AgentRequest 42, HermesTask 43, HermesMemory 54,
OrchestrationRecord 39, AgentEvent 95. Sumber: kajian bab 1 & 3.1 (dokumen
`kajian_ekosistem_brahma.md`), tabel §3.2–3.3.

# Bukti

- Diagram komponen lengkap di kajian §3.1 (layout layanan, bus, bridge, fleet,
  webstack, knowledge).
- Ringkasan eksekutif kajian §1: 40 profil + 1 default + 1 user = 42 agen.
- Skala: 128 SKILL.md registry; DB counts §5.4; IL 1.996 entri §9.4.

# Batas

- Angka di atas adalah snapshot audit 24-08-2026 — sumber berubah; cek
  `tanggal_akses` bila dipakai mengikat.
