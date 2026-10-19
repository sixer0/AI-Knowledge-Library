---
id: bridge-hermes-arsitektur-dispatch-mirror
type: fakta
title: Bridge (hermes-bridge) — Arsitektur, Alur Dispatch & Mirror
status: active
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 6.1-6.3
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: digital
writer: gsp-librarian
tags: [bridge, hermes, message-bus, dispatch]
links: [temuan-audit-f1-f12]
penulis: dashboard
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: Semua konstanta dan alur terverifikasi verbatim terhadap kajian §6.1-6.4 (baris 243-267): dependensi tunggal pg ^8.13.1, launcher launch-bridge.sh + daftar env (DATABASE_URL, HERMES_BOARD, HERMES_BIN, HERMES_WIKI, BRIEF_HOUR) + KILOCODE_API_KEY dari .env home Hermes; POLL_MS=5000, MIRROR_MS=30000, RUN_TIMEOUT_MS=1800000 dengan riwayat override dari 240 s pasca insiden timeout crawl 21-08-2026; WIKI_DIR aktual C:/Users/TRIAL/AppData/Local/hermes/wiki; BRIEF_HOUR=8; lima langkah runRequest termasuk hasil max 8.000 char dan status semantik STATUS/KODE; empat mirror (kanban, cron, wiki, daily brief dengan guard persist hermes-briefing.generatedAt); bug ReferenceError kanbanCardId 24-08-2026 dan prinsip bookkeeping failure != agent failure. Tidak ada dimensi yang gagal. Satu-satunya perbedaan redaksional: body menulis syarat 'target profil != default' sedangkan sumber '!= default/brahma' - penyempitan ringan, tidak mengubah fakta. YAML valid, satu baris status, title==H1, links `temuan-audit-f1-f12` ada di folder vault yang sama. || Rekomendasi: Siap dipromosikan. Sunting status `terverifikasi` -> `ditinjau` sebelum promote (aturan I1). Bila ingin presisi penuh, tulis ulang syaratnya menjadi '!= default/brahma' sesuai sumber. || Riwayat: catatan_verifikasi sebelumnya (custodian 2026-08-25 perlu_revisi, direvisi librarian Wave B fix-h1) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/bridge-hermes-arsitektur-dispatch-mirror.md
catatan_keputusan: "dipromosikan: IL-INGEST-01 B1a pilot: verdict custodian terverifikasi (C-B1a-verdict.md), cek YAML kelas-I5 lulus, non-sensitif non-dosir"
---

# Bridge (hermes-bridge) — Arsitektur, Alur Dispatch & Mirror

Bridge (`hermes-bridge` / `bridge.mjs`) — penghubung bus PostgreSQL 5433 ke
CLI hermes (kajian §6.1–6.3):

- **Arsitektur:** Node.js ESM, dependensi tunggal `pg` (^8.13.1); launcher
  `launch-bridge.sh` membaca env dari `../.env` (DATABASE_URL, HERMES_BOARD,
  HERMES_BIN, HERMES_WIKI, BRIEF_HOUR) + `KILOCODE_API_KEY` dari Hermes home
  `.env` (wajib agar dispatch profil tidak gagal kredensial).
- **Konstanta:** `POLL_MS=5000`, `MIRROR_MS=30000`, `RUN_TIMEOUT_MS=1800000`
  (30 menit; di-override dari 240 s setelah insiden timeout crawl 21-08-2026),
  `WIKI_DIR` = `C:/Users/TRIAL/AppData/Local/hermes/wiki`, `BRIEF_HOUR=8`.
- **Alur dispatch (runRequest, §6.2):** update AgentRequest → running + event;
  jika target profil ≠ default → tulis OrchestrationRecord (kind=dispatch),
  set AgentState running, buat kartu kanban (assignee=profil), simpan
  hermesTaskId (tanpa duplikat kartu); eksekusi `hermes -p <profil> -z
  <prompt>` dengan timeout 30 mnt; update → done + result (max 8.000 char);
  status semantik respons (STATUS/KODE) menutup kartu kanban + OrchestrationRecord.
- **Mirror (§6.3):** kanban mirror (kartu → HermesTask), cron mirror (`hermes
  cron list --all` → DataStore), health mirror, wiki mirror (writeWikiEntry +
  git commit → HermesMemory), daily brief chief-of-staff (guard persist harian
  via DataStore `hermes-briefing.generatedAt`; memperbaiki bug brief ganda
  24-08-2026).
- **Bug historis (§6.4):** ReferenceError `kanbanCardId` (24-08-2026) →
  scope variabel diperbaiki; prinsip "bookkeeping failure ≠ agent failure"
  (AgentRequest failed tapi result terisi → rekonsiliasi ke done).

Sumber: `kajian_ekosistem_brahma.md` bab 6.1–6.4.

# Bukti

- Proses node bridge.mjs aktif saat audit (§3.2).
- Pitfall pelengkap: dispatch berat >4 menit → RUN_TIMEOUT_MS 30 mnt; sub-task
  fokus+sempit <15 mnt (§6.4).

# Batas

- Konstanta nilai dari source saat audit; bisa berubah di versi bridge lain.
