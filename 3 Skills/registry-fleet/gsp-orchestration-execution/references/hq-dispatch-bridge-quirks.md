# HQ Dispatch & Kanban Bridge Quirks (terverifikasi 02-09, misi Asset Factory)

## Auth dispatch API
- `POST https://localhost:9011/api/brahma/dispatch` dengan header `x-internal-secret`.
- Nilai `INTERNAL_API_SECRET` di `gsp-datacenter/.env` TERBUNGKUS KUTIP. Cara ambil yang benar:
  `SECRET=$(grep -E "^INTERNAL_API_SECRET=" .env | cut -d= -f2- | tr -d '"\r')`
  Tanpa `tr -d '"'` respons selalu `{"error":"Unauthorized"}` (terjadi nyata 02-09).
- Body: `{kind:"oneshot", profile:"gsp-<nama-profil>", title, prompt, hermesTaskId:"<id kartu>", sideEffecting:false}`.
  `sideEffecting:true` masuk status `awaiting_approval`, bukan queued.
- `PATCH /api/brahma/requests/<id>` action `force-done` DITOLAK selama status `running`
  ("cannot force-done a running request"). Tunggu request jadi `done`/`failed` dulu.

## Auto-claim bridge (penting!)
- Bridge worker mengklaim DAN mengeksekusi setiap kartu kanban yang `--assignee`-nya
  profil gsp-*, TANPA perlu AgentRequest dispatch eksplisit. Bukti 02-09: kartu
  AF-R0-probe/schema/shelf/lane R selesai dikerjakan padahal controller hanya
  mendispatch RT, TA, dan librarian secara eksplisit.
- Konsekuensi: kartu dibuat tanpa edge `--depends` langsung jalan dan bisa mendahului
  upstream-nya. Kejadian berulang KEDUA (pertama: loop 20x 31-08). ATURAN:
  **setiap kartu untuk pekerjaan bridge WAJIB dibuat dengan `--depends <id>` sesuai
  DAG blueprint**; kalau terlanjur tanpa edge, mitigasi: instruksi kartu menuntut
  "lapor blocked jujur bila input belum ada" + re-dispatch sheet yang kekurangan bahan.

## Lifecycle kartu
- `complete` ditolak selama worker claim hidup: error menyebut
  "live worker claim (run N, pid P, heartbeat T)" -> polling status AgentRequest
  sampai `done`, baru tutup kartu.
- Kalau bridge sudah menutup kartu sendiri, `complete` membalas
  "unknown id or terminal state" - itu BUKAN error, cek `show <id>` (status `done`).
- Verifikasi hasil: artefak-first (file di path kontrak + byte > 0), bukan hanya status.
- Jangan pakai loop polling terminal >420s untuk menunggu request; pakai putaran
  pendek berulang (break saat status berubah) agar tidak kena timeout klien.

## Register aktor (preferensi user 02-09)
User bisa kapan saja meminta "daftar aktor masing2 fleet yang kamu dispatch".
Selalu rawai REGISTER di contract.md: `kartu | judul | assignee profil | status` per
gelombang (simpan juga cards.json hasil script pembuat kartu), dan siap render
sebagai tabel aktor+peran+status dalam satu jawaban tanpa penelusuran ulang.

## Cap 1MB stdout mematahkan loop mirror HQ (kejadian 02-09, misi EXPO-INTEL)
- `hermes()` di bridge.mjs membatasi stdout 1MB (SEC-007). Setelah board punya
  ~800 kartu, `kanban list --json` = 1,19MB -> terpotong -> JSON.parse gagal ->
  `mirrorKanban()` log "kanban list failed: Unterminated string" tiap tick.
- Efek: MIRROR HQ (visibilitas dashboard) basi; DISPATCH TIDAK terpengaruh
  (loop antrean terpisah, kartu tetap jalan - bukti G3 running normal).
- Deteksi cepat: grep "kanban list failed" bridge.out.log; ukur
  `hermes kanban --board default list --json | wc -c` vs 1048576.
- Perbaikan yang sah (wewenang user untuk restart): arsipkan kartu done lama
  (`hermes kanban archive`), atau naikkan MAX_OUT, atau mirror pakai `list
  --status !done`. Jangan restart bridge sendiri (kebijakan user).

## Gerbang force-done API mati senyap saat build HQ lebih tua dari sumber (triase 0907A, 07-09)
- `PATCH /api/brahma/requests/[id] action=force-done` pada request `blocked`/`failed` dibalas
  409 `cannot force-done a ... request` walau `src/app/api/brahma/requests/[id]/route.ts`
  sudah memuat TRG-0904G-FIX (yang mengizinkan aksi itu sejak 04-09).
- Diagnosis: bandingkan mtime `.next/server/app/api/brahma/requests/[id]/route.js` (build yang
  dijalankan proses HQ) vs berkas sumber. Build 04-09 09:55 < sumber 04-09 14:50 = fix belum live.
  Restart HQ = wewenang user; jangan restart sendiri.
- Jalur sah sementara: rekonsiliasi DB guarded per-id, satu transaksi,
  `UPDATE "AgentRequest" SET status='done', result=<note rujukan kartu terminal> ... WHERE id=$2
  AND status IN ('blocked','failed')` — preseden
  docs/2026-09-04-kanban-triage-c/scripts/reconcile_bridge_approval.cjs dan
  docs/2026-09-07-cron-kanban-triage-0907a/scripts/reconcile_triage_0907a.cjs.
  DATABASE_URL dibaca dari gsp-datacenter/.env lewat env var proses (dotenv tidak auto-load dari
  cwd hermes-bridge; `new Pool({connectionString: process.env.DATABASE_URL})` butuh
  `DATABASE_URL=... node script.cjs` atau require dotenv dengan path .env absolut).
- Query daftar non-done: `GET /api/brahma/requests?status=blocked,failed,running,queued,needs-review,awaiting_approval&take=200`
  (parameter `take`, BUKAN `limit`; `skip` diabaikan rute). Response `{requests, pending}`.
- `createdAt` AgentRequest = UTC ISO; umur WIB = calendar.timegm(...) lalu kurangi 7*3600,
  jangan time.mktime (meleset 7 jam).
