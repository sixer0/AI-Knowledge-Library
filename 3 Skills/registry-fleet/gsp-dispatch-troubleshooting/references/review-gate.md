# Review Gate dispatch — DONE hanya oleh asignor (fix 29-08-2026)

Session detail for SKILL.md recovery/verification flows. Kontrak ini mengubah cara
menafsirkan status dispatch: hasil kerja agent TIDAK PERNAH auto-`done`.

## Kontrak status (bridge.mjs 29-08-2026)
- `semanticStatus()`: oneshot/chat SELALU berakhir `needs-review` — marker
  `STATUS: complete` dari asignee diabaikan; `blocked`/`failed` tetap lewat.
  Hanya kind infra (`kanban`, `cron.*`, `memory.write`, `briefing.generate`) auto-`done`.
- `closeKanbanCard()`: `needs-review` → `kanban request-review <id> --summary ...`
  (kartu masuk status `review`), `done` → `complete`, `blocked|failed` → `block`.
- `recoverZombies()` dua lapis: AgentRequest `running` → failed, DAN
  OrchestrationRecord `running` yang parent-nya sudah terminal → failed
  (`WHERE status='running' AND EXISTS (SELECT 1 FROM "AgentRequest" r WHERE r.id=o."runId" AND r.status<>'running')`).

## Keputusan asignor — PATCH /api/brahma/requests/[id]
- `{"action":"force-done","note":"..."}` → status `done`, result diawali
  `[FORCE-DONE] <note>`, `decidedAt` terisi. SATU-SATUNYA jalan ke `done`.
- `{"action":"request-changes","feedback":"..."}` → kembali `queued`; feedback
  disisipkan ke akhir prompt (`[REVIEW FEEDBACK — changes requested]: ...`) = healing loop.
- Guard: `needs-review` hanya actionable via `force-done|request-changes`;
  `queued|awaiting_approval` via `approve|reject|edit`; lainnya 409.

## Alur kanban native (teruji 29-08)
`ready` → (assignee kerja) → `request-review` → `review` →
`request-changes` → `ready` (rework) → … → `complete` → `archive`.
Jangan `block` kartu yang hanya menunggu review; `block` untuk blocked/failed.

## Perbedaan dengan panduan pra-29-08
- "Reconcile failed-with-result ke done manual" → TIDAK lagi: reconcile ke
  `needs-review`, lalu assignor force-done.
- Kartu dispatch yang selesai TIDAK otomatis `complete` — ia menunggu `review`
  sampai assignor memutuskan.
- KPI dispatch kini observable: `GET /api/brahma/dispatch-kpi` (zombie edge =
  record `running` dengan parent tidak-running; halaman `/dispatch-kpi`).

## Insiden restart bridge (29-08)
- Patch baru hanya aktif setelah restart; pastikan antrean kosong dulu.
- `taskkill` via MSYS bisa gagal senyap → bridge lama tetap hidup, launcher
  menambah instans kedua = double-poll race. Verifikasi proses via PowerShell
  Win32_Process (`CommandLine like '*bridge.mjs*'`); wajib TEPAT SATU.
- Luncurkan bridge via terminal background (inline `&` ditolak parser);
  TANDA HIDUP: `swarm-bridge up · board=default · ...` di bridge.out.log.
