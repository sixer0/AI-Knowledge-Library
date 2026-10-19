---
id: agen-headquarter-stack-api-model-data
type: fakta
title: "Agent Headquarter (gsp-datacenter): Stack, API Routes & Model Data"
status: active
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 5.1-5.5
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: digital
writer: gsp-librarian
tags: [agent-headquarter, stack, prisma, nextjs]
links: [bridge-hermes-arsitektur-dispatch-mirror]
penulis: dashboard
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian PUTARAN 2, 2026-09-03, re-challenge penuh 7 dimensi atas suntingan gsp-document-writer). Alasan: re-challenge PUTARAN 2: suntingan putaran 1 terverifikasi. '~60 route' diganti '36 endpoint dasar beserta varian sub-route (kajian 5.3)' - hitung ulang independen blok kode 5.3 menghasilkan tepat 36 endpoint dasar unik, cocok; frontmatter 'halaman' dilebarkan ke bab 5.1-5.5 sesuai rekomendasi; angka Prisma 5.4 tetap identik sumber (verifikasi putaran 1, tidak berubah). Mekanik: yaml.safe_load lulus, satu baris status, title==H1, nilai frontmatter utuh. || Rekomendasi: objek siap lanjut ke lane librarian - sunting status 'terverifikasi' menjadi 'ditinjau' sebelum memanggil vault_promote.py (aturan I1); cek YAML kelas I5 dan klasifikasi dosir manual tetap prosedurnya. Tidak ada perubahan lain yang diperlukan penulis. Sensitif: tidak; dosir: tidak ada tema perkara hukum (kompensasi klasifikasi manual lane librarian, temuan I2). || Riwayat PUTARAN 1 (custodian 2026-09-03, perlu_revisi): Verdict: perlu_revisi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: Angka Prisma §5.4 terverifikasi identik dengan kajian baris 220-230 (AgentRequest 42, AgentEvent 95, AgentState 33, HermesTask 43, HermesMemory 54, OrchestrationRecord 39, DataStore 5, WebUiUser 2, model content 0); §5.1 stack, §5.2 halaman, dan §5.5 alur cocok verbatim dengan kajian baris 177-183, 185-192, 232-237. Klaim '~60 route' yang diatribusikan ke §5.3 TIDAK ada di sumber: kajian §5.3 (baris 196-216) hanya mendaftar 36 endpoint dasar + 14 varian berkurung dan tidak menyatakan total apa pun; pencarian pola 'digit + route' di seluruh folder docs/2026_08_24_kajian_ekosistem menghasilkan nol. Angka tanpa rujukan = asumsi, bukan fakta (prinsip #3 standar library). Renik non-blocking: frontmatter `halaman: bab 5.1-5.4` padahal body juga memakai §5.5. || Rekomendasi: Ganti '~60 route' dengan angka yang dapat ditunjuk (mis. '36 endpoint dasar beserta varian sub-route, kajian §5.3') atau tandai eksplisit sebagai perkiraan; lebarkan `halaman` menjadi 'bab 5.1-5.5'. Tidak ada perubahan lain yang diperlukan. || Riwayat: catatan_verifikasi sebelumnya (custodian 2026-08-25 perlu_revisi, direvisi librarian Wave B fix-h1) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-putaran: 2
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-document-writer
direvisi-pada: 2026-09-03
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/agen-headquarter-stack-api-model-data.md
catatan_keputusan: "dipromosikan: subset lolos re-challenge RC-9 putaran 2 (9/9 terverifikasi); angka snapshot dibaca sebagai snapshot audit 24-08-2026 (objek terkait sudah membawa seksi Batas)"
---

# Agent Headquarter (gsp-datacenter): Stack, API Routes & Model Data

Agent Headquarter (`gsp-datacenter`), dashboard mission control GSP
(kajian §5):

- **Stack (§5.1):** Next.js 16 (App Router) + React 19 + TypeScript; UI
  Tailwind CSS v4, Recharts, react-dnd, lucide-react; DB PostgreSQL via Prisma
  ORM (`prisma db push`); auth NextAuth (Google OAuth, ALLOWED_EMAILS) + RBAC
  WebUI; desktop wrapper Tauri 2.
- **Halaman utama (§5.2):** Cockpit (⌘K command palette, daily brief),
  /brahma (dispatch one-shot & kanban, Approval Inbox, live activity),
  /information-library (scope All/Wiki/Workspace/Vault), Work & Content
  (Tasks, Ideas, Content OS, Longform, YouTube, Articles, Client Pulse, Agents
  roster, Garden, Watchlist Radar, X Analytics, Trends, scrape metrics),
  /orchestration (graf + timeline telemetry), /user-access (RBAC + pin profil).
- **API routes (§5.3):** 36 endpoint dasar yang terdaftar di kajian §5.3
  beserta varian sub-route (notasi berkurung), termasuk /api/brahma/dispatch,
  /api/brahma/health, /api/agents (GET roster + POST state),
  /api/information-library (+ file dengan proteksi path traversal),
  /api/orchestration, /api/user-access, /api/cron, /api/trends, dll.
- **Model data Prisma (§5.4):** AgentRequest 42 (status queued →
  awaiting_approval → approved → running → done/failed/rejected), AgentEvent
  95, AgentState 33, HermesTask 43 (mirror kanban), HermesMemory 54 (wiki),
  OrchestrationRecord 39 (telemetry), DataStore 5, WebUiUser 2; model fitur
  content (Article, Idea, Youtube*, ClientPulse*, Brief, Mission, User) = 0.
- **Alur komunikasi (§5.5):** Website → insert AgentRequest (aman → queued;
  side-effecting → awaiting_approval) → Bridge poll Postgres 5 detik → jalankan
  via CLI hermes → hasil ditulis kembali; bridge TIDAK pernah mengeksekusi
  awaiting_approval; setiap dispatch lintas profil menulis OrchestrationRecord
  (graf /orchestration).

Sumber: `kajian_ekosistem_brahma.md` bab 5.1–5.5.

# Bukti

- Inventaris API routes dari source (kajian §5.3); DB counts via psql (§2).
- UI /information-library menampilkan badge sumber workspace/wiki (§9.4).

# Batas

- Jumlah record DB = snapshot audit 24-08-2026.
