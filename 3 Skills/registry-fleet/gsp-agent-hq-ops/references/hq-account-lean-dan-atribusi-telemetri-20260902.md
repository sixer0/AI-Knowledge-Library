# HQ: akun lean sejak lahir + atribusi inisiator telemetri (misi 2026-09-02)

Kontrak: `docs/2026-09-02-fix-hq-rbac-telemetry/contract.md`. Kartu done:
t_75df2e4f t_7afd5557 t_84bbbe59 t_11e4f653 t_dcf950a9 t_c263d45b.
Commit: gsp-datacenter `500bbdb` `f56decd` `ca09c52` · gsp-brahma `7f2da1f` `7322cba` · gsp-agent `437de48` `7fcbd3f`.

## Atribusi inisiator (temuan #4)

- `AgentRequest.requestedBy TEXT` = id inisiator: `user:<username>` utk login browser,
  id profil utk pemanggil mesin, NULL = data lama (fallback telemetri `brahma`).
- Bridge: `const fromAgent = r.requestedBy || "brahma"` (sebelumnya hardcode `brahma`,
  penyebab 260/260 edge satu sumber). Claim lane memakai `RETURNING *` sehingga kolom
  baru mengalir tanpa mengubah SELECT.
- Rute `POST /api/brahma/dispatch`: `getRequester(req, b.agentId)` — cookie sesi →
  `user:<u>`; selain itu pakai field body `agentId` (WAJIB utk pemanggil mesin karena
  tidak punya cookie). Helper `hq_dispatch.cjs` / `hq_dispatch_card.cjs`
  (workspace/gsp-hermes/scripts): arg `[agentId]` > env `HERMES_DISPATCH_AGENT` >
  infer `HERMES_HOME` (parent == `profiles` → nama profil aktif) > `brahma`.
- Backfill jujur (tanpa menebak username):
  `UPDATE "AgentRequest" SET "requestedBy"='brahma' WHERE origin IN ('brahma-controller','orchestrator-swarm','hermes') AND "requestedBy" IS NULL;`
  `UPDATE "AgentRequest" SET "requestedBy"='user:web' WHERE origin='web' AND "requestedBy" IS NULL;`
  lalu `UPDATE "OrchestrationRecord" o SET "fromAgent"='user:web' FROM "AgentRequest" r WHERE r.id=o."runId" AND r.origin='web' AND o."fromAgent"='brahma';`
  (hasil nyata: 130 / 151 / 143 baris).
- Graf `/orchestration` butuh node di kedua ujung edge: inisiator login dibuat node
  virtual sisi klien (`user:*` → grup `user`, baris layout sendiri). Tanpa itu edge
  `user:*` hilang senyap dari graf walau datanya ada.
- Normatif skill: `gsp-orchestration-telemetry` §"Atribusi inisiator" v1.1.0 dan
  `gsp-orchestration-execution` non-negotiable 3 v1.3.0.

## Provisioning akun lean (temuan #2 dan #3)

- HQ `scripts/ensure-profile-complete.mjs` → `provisionLeanProfile(name,{lane})`:
  config/.env/SOUL root hanya bila absen, skill fisik = lane (controller: trio
  orkestrasi + verif + LAD; worker: verif saja), marker ganda `.lean-policy` +
  `.no-bundled-skills`, purge `.bundled_manifest` dan `.skills_prompt_snapshot.json`.
- WebUI signup: `api/profiles.py.leanify_new_profile()` dipanggil handler
  `/api/auth/signup` SESUDAH audit clone (non-fatal kalau gagal).
- `inspectOnDisk` di kedua rute user-access WAJIB mengecualikan profil ber-marker
  lean — ambang lama `>=80% skill root` menolak semua akun lean.
- ADMINISTRATOR dengan profil belum ada kini ikut jalur lean (dulu 400
  "Provision it first"). Field profil di form boleh kosong → `hermesProfile`
  default = username.

## Resep deploy tambah kolom Prisma saat server produksi hidup

1. ALTER langsung lewat `pg` dari `hermes-bridge/node_modules` (bukan `migrate dev`):
   `ALTER TABLE "AgentRequest" ADD COLUMN IF NOT EXISTS "requestedBy" TEXT`.
2. `npx prisma generate` bisa balas `EPERM ... query_engine-windows.dll.node` karena
   server memegang DLL. JANGAN panik: cek dulu
   `grep -c requestedBy node_modules/.prisma/client/index.d.ts` — kalau field sudah
   masuk, client ter-update dan build akan compile.
3. `npx next build` → `node scripts/hq_restart.mjs` (kill listener 9011, respawn
   detached, health check). Restart HQ = wewenang user; jalankan hanya dengan approval.
4. Restart bridge WAJIB lewat `hermes-bridge/launch-bridge.sh` (git-bash absolut).
   Menjalankan `node bridge.mjs` telanjang keluar dengan
   `DATABASE_URL is required (use the direct postgres:// URL...)`.
5. Sebelum restart bridge, cek antrean: `AgentRequest` `status='running'` atau
   `'queued'` harus 0, supaya tidak memotong eksekusi worker.

## Verifikasi end-to-end

- `gsp-datacenter/scripts/verify_hq_fixes_20260902.py` — 15 check: akun USER+ADMIN
  via API → profil lean (skills<=5 + marker + gate SOUL) → login HQ 200 ber-cookie →
  dispatch ber-sesi → `requestedBy=user:<probe>` + edge `from` sama → grep chunk build
  (`NEXT_PUBLIC_OWNER_NAME` nol, `/api/auth/me` hadir). PASS 15/15.
- `gsp-datacenter/scripts/verify_attrib_agentid_20260902.py` — 6 check jalur mesin:
  dispatch tanpa cookie dengan `agentId` → `requestedBy=gsp-master`, tertahan
  `awaiting_approval` (sideEffecting=true supaya bridge tidak mengeksekusi probe),
  cleanup request+edge, sisa 0. PASS 6/6.
- Kedua skrip membuat akun/profil uji sendiri dan menghapusnya. Jejak DB yang
  pembersihannya terkena gate persetujuan tertinggal 1 request + 1 edge label probe
  (menunggu persetujuan user) — jangan dianggap kegagalan verifikasi.

## Identitas dashboard (temuan #1)

- Header `src/app/page.tsx` dulu membaca `process.env.NEXT_PUBLIC_OWNER_NAME`
  (bernilai nama pemilik di `.env`). Kini fetch `/api/auth/me` dan menampilkan
  `displayName || username` sesi dengan fallback netral "Command Center".
  `GET /api/auth/me` ikut mengembalikan `displayName` dari `WebUiUser`.
- Baris `NEXT_PUBLIC_OWNER_NAME` dihapus dari `.env`; jangan pernah memasukkan
  identitas personal ke env publik lagi.

## Pitfall mekanik yang muncul di misi ini

- `skill_manage(action=patch)` pada skill gsp-* menulis ke salinan **registry fleet**
  (`%LOCALAPPDATA%/hermes/skills/gsp/<skill>/SKILL.md`), bukan kanonik
  `workspace/gsp-hermes/skills/<skill>/`. Setelah setiap patch: sync-back kanonik dan
  bandingkan sha256 (pitfall sync-back `gsp-skill-distribution` berlaku dua arah).
- Distribusi salinan SKILL.md (kanonik + registry + repo snapshot + profil hidup)
  paling aman lewat skrip Python yang menulis byte-identik lalu memverifikasi sha256
  seragam; loop shell inline dengan glob `*/skills/**` bisa kena blocklist parser
  payload.
- Pipe `| python -c` di git-bash jatuh ke alias Store (buntu). Pakai
  `uv run --python 3.11 python`.
- `taskkill //PID` lewat git-bash rusak (arg parsing); pakai
  `powershell.exe -NoProfile -Command "Stop-Process -Id <pid> -Force"`.
- POST mutatif ber-guard W2.2 (user-access, orchestration, dispatch) bisa dipakai
  dari skrip verifikasi lewat header `x-internal-secret` — jalur mesin sah, bukan
  pelonggaran auth.
