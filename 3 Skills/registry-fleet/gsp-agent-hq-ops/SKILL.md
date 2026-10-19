---
name: gsp-agent-hq-ops
version: 1.1.0
description: >-
  Use when fixing GSP Agent HQ/Brahma WebUI RBAC flows.
license: MIT
metadata:
  hermes:
    tags: [gsp, hq, brahma, rbac, webui, nextjs, information-library]
    category: gsp
---

# GSP Agent HQ & Brahma WebUI Operations

Runbook untuk memperbaiki/mengoperasikan dua aplikasi inti GSP:

| App | Repo | Port | Runtime | Cara jalan |
|---|---|---|---|---|
| **Agent HQ** | `C:/Users/TRIAL/gsp-datacenter` (Next.js 16) | 9011 | **produksi**: `node hq-server.mjs` (NODE_ENV=production, bind 127.0.0.1+IP Tailscale, HTTPS self-signed) — sejak fix SEC-001 30-08 | Autostart: `gsp-ecosystem-start.sh` + watchdog cron; middleware auth AKTIF (dev bypass tidak berlaku) |
| **Brahma WebUI** | `C:/Users/TRIAL/gsp-brahma` (Python server.py) | 9012 | daemon `./ctl.sh` | `./ctl.sh restart` |

## Login terpadu HQ (fix 30-08-2026)

- `/login` HQ = **form username/password**, verifikasi terhadap tabel `WebUiUser`
  (AKUN SAMA dengan WebUI Brahma) via `verifyPassword()` shared di
  `src/lib/webui-rbac.ts`. Endpoint: `POST /api/auth/login` (throttle 10x/15m per IP),
  `POST /api/auth/logout`, `GET /api/auth/me`.
- Sesi: cookie `gsp_hq_session` = HMAC-SHA256 (secret `NEXTAUTH_SECRET`), payload
  `{u,r,p,exp}`, TTL 24 jam, stateless (logout = hapus cookie, tidak dicabut
  server-side). Modul: `src/lib/hq-session.ts` (node crypto, server-only).
- `src/middleware.ts` menerima 3 identitas: NextAuth Google (butuh env OAuth —
  saat ini kosong), cookie sesi HQ (validasi HMAC **Web Crypto** — `node:crypto`
  TIDAK tersedia di runtime edge, nama cookie didefinisikan ulang di middleware),
  dan `x-internal-secret`.
- **`/api/brahma/rbac/*` WAJIB lolos pre-session** — handler menjaga diri via
  `x-rbac-token`; kalau middleware memblokirnya, login WebUI Brahma mati 401
  (regression nyata SEC-001 30-08, sudah difix).
- Role ADMIN/USER belum membatasi halaman HQ (keputusan user 30-08: semua yang
  login = akses penuh). Kontrak: `docs/2026-08-30-login-terpadu-hq/contract.md`.
- **Restart HQ produksi**: `powershell Stop-Process -Id <pid> -Force` lalu
  `node hq-server.mjs` dari `gsp-datacenter` (background). `taskkill //PID` lewat
  git-bash RUSAK (arg parsing) — pakai PowerShell. Setelah ubah kode: `npx next build`
  (prisma generate gagal EPERM saat server hidup — skip, client tidak berubah).

Keduanya saling terhubung via RBAC: WebUI memanggil HQ `/api/brahma/rbac/*`
dengan header `x-rbac-token`. Detail arsitektur & kontrak endpoint ada di
[`references/architecture-and-endpoints.md`](references/architecture-and-endpoints.md).

## Aturan emas

1. **Token RBAC harus sama di kedua .env**: `HERMES_WEBUI_RBAC_TOKEN`
   (gsp-brahma/.env) == `WEBUI_RBAC_TOKEN` (gsp-datacenter/.env). Beda → login/
   signup WebUI dapat 401. Setelah ubah, RESTART HQ agar terbaca.
2. **Bandingkan token dengan Python, bukan bash** — `grep|cut` pada file .env
   ber-CRLF menyisakan `\r` → false mismatch (kejadian nyata 24-08-2026).
   Pakai Python: `strip().strip('"').strip("'")` lalu bandingkan md5.
3. **Signup WebUI off by default** — aktif via `HERMES_WEBUI_RBAC_SIGNUP=1` di
   gsp-brahma/.env. Jika diaktifkan, siapa pun yang menjangkau port 9012 bisa
   buat akun USER (panel terbatas, bukan ADMIN) — konfirmasi ke user bila ragu.
4. **Akun pengguna baru yang siap digunakan = punya profil Hermes LENGKAP**. Jalur resmi:
   WebUI signup (auto-clone profil dari `default`) ATAU HQ user-access — sejak
   27-08-2026 kedua jalur memakai provisioning guard: nama profil divalidasi
   (`[a-z0-9][a-z0-9_-]{0,63}`, USER tidak boleh bind `default`), profil USER
   yang belum ada di disk di-auto-clone LENGKAP (SOUL+skills+memory), profil
   ADMIN yang belum ada DITOLAK (400, provision manual dulu). Sebelum guard
   ini, HQ `POST /api/user-access` hanya insert baris DB — akun bisa terikat
   ke profil yang tidak ada (kasus nyata: `GSP-1`) atau setengah jadi.
   `hermesProfile` hanya boleh terikat 1 user (409). PATCH `/api/user-access/<id>`
   kini menerima `hermesProfile` untuk re-bind (validator sama).
5. **/api/status itu ADMIN-only** — USER login dapat 403 di sana itu NORMAL,
   bukan bug profil. Uji panel USER: `/api/models`, `/api/sessions`, `/api/rbac/status`.
6. **.env perubahan butuh restart** — Next.js dev membaca .env saat boot; jangan
   andalkan hot-reload untuk variabel env.

## Alur kerja perbaikan (sudah teruji)

1. **Diagnosis dulu** (jangan tebak):
   - `curl -sk https://localhost:9012/api/rbac/status` → cek `enabled`/`signup_enabled`.
   - Uji endpoint langsung: `POST /api/auth/signup`, `POST /api/auth/login`,
     `POST /api/user-access`, `POST /api/brahma/rbac/signup` (dengan token).
   - Lihat log HQ (`gsp-datacenter/hq-dev.out.log`) untuk pola 4xx/5xx —
     mis. banyak `POST /api/user-access 400` = dinding validasi UI.
2. **Perbaiki di level chokepoint**: validasi client harus mencerminkan aturan
   server (username regex `^[a-z0-9][a-z0-9_-]{0,31}$`, password ≥8, profil wajib),
   dengan pesan bahasa yang jelas — jangan biarkan user mentok 400.
3. **Verifikasi end-to-end dengan probe user** lalu BERSIHKAN:
   - signup probe → cek profil di disk → login → akses panel USER → hapus
     (DELETE `/api/user-access/<id>`) + `rm -rf` profil.
   - Pitfall: ID dari command substitution sering menempel `\r` → `tr -d '\r'`
     dulu, atau curl dapat HTTP 000.
4. **Verifikasi UI Next.js tanpa browser**: lihat [`scripts/verify_nextjs_bundle.py`](scripts/verify_nextjs_bundle.py).

## Restart

- **WebUI**: `cd /c/Users/TRIAL/gsp-brahma && ./ctl.sh restart` (PID/log:
  `$HERMES_HOME/webui.{pid,log}` = `C:/Users/TRIAL/AppData/Local/hermes/`).
- **HQ**: kill process tree — parent `node .../next dev` + child
  `start-server.js` (cek via PowerShell `Get-CimInstance Win32_Process`),
  lalu relaunch command persisnya (ada di references) dengan
  `>> hq-dev.out.log 2>> hq-dev.err.log` sebagai background process.
  Catat PID listener baru via `netstat -ano | grep 9011`.

## Autostart & bind 0.0.0.0 (fix 26-08-2026)

- **Autostart ekosistem**: `C:/Users/TRIAL/gsp-ecosystem/gsp-ecosystem-start.sh`
  dipicu Startup VBS `gsp-ecosystem-autostart.vbs` (logon, hidden, tanpa admin);
  urutan Postgres → bridge → gateway → dashboard(9010) → webui(9012) → hq(9011).
  Skrip idempoten (health OR port oracle).
- **TIGA launcher WAJIB sinkron** (jangan ubah satu saja — yang lain akan
  regresi ke 127.0.0.1):
  1. `gsp-ecosystem-start.sh` (autostart logon)
  2. `gsp-ecosystem/watchdog-webui-hq.sh` (cadangan manual)
  3. `~/.hermes/scripts/watchdog-webui-hq.py` — **yang benar-benar dipakai cron**
     no_agent `19ae9f96d588` (tiap 3 jam); `.sh` hanyalah versi manual.
  WebUI: `bootstrap.py --host 0.0.0.0 9012` (`.env` sudah
  `HERMES_WEBUI_HOST=0.0.0.0`; jangan override ke 127.0.0.1).
  HQ: `next dev -H 0.0.0.0` eksplisit.
- **Akses remote (Tailscale)**: bind 0.0.0.0 SAJA TIDAK CUKUP — butuh rule
  firewall scoped interface: `GSP Agent HQ 9011 (Tailscale)` &
  `GSP Brahma WebUI 9012 (Tailscale)` (dibuat via
  `gsp-ecosystem/fw-tailscale.ps1` elevated/UAC, idempoten).
  Adapter = `Tailscale`, IP 100.102.23.27.
- **Cert HQ** SAN sekarang `DNS:localhost, IP:127.0.0.1, IP:100.102.23.27`
  (regen 26-08, backup `certs/hq-*.pem.bak-20260826`). WebUI cert sudah
  termasuk IP tailnet sejak 24-08.
- **Pitfall idempotensi gateway**: `hermes gateway status` outputnya
  `Gateway process running (PID n)` — grep `Gateway is running` tidak pernah
  cocok → spawn duplikat tiap run autostart (lihat windows-service-ops).

## Information Library (UI filter)

- API: `/api/information-library?scope=all|wiki|workspace|vault&q=&type=&status=`
  — `scope=all` = wiki+workspace, vault TIDAK ikut (staging terpisah).
- `typeCounts`/`statusCounts` dihitung dari daftar TERFILTER (progressive
  filtering): saat satu filter dipilih, chip saudaranya hilang — selalu sediakan
  chip "All" agar bisa reset.
- **Chip status vault harus bisa diklik** (API sudah dukung `status=` untuk
  vault; UI dulu menampilkan chip inert — fix 24-08-2026).
- Pola komponen: satu `FilterChip` (label+count+tone+active) untuk type DAN
  status, + tone map untuk status vault (usulan=warn, ditinjau=accent,
  terkurasi/terbit=up, ditolak/arsip=down).
- Toggle Active/All hanya untuk scope non-vault; di vault ganti chip status.
- `SHARED_WORKSPACE` di .env HQ WAJIB menunjuk path Windows
  (`C:/Users/TRIAL/workspace/gsp-hermes/workspace`) — default di code masih path Mac.

## Support files

- [`references/architecture-and-endpoints.md`](references/architecture-and-endpoints.md) — peta arsitektur, kontrak endpoint
  RBAC/user-access/IL, prosedur restart HQ lengkap, log fix 24-08-2026.
- [`scripts/verify_nextjs_bundle.py`](scripts/verify_nextjs_bundle.py) — verifikasi perubahan UI Next.js dev
  dengan grep string baru di chunk terkompilasi (saat browser tak tersedia).

## Provisioning guard profil RBAC (fix 27-08-2026)

- **Cek kesehatan profil akun**: `node C:/Users/TRIAL/gsp-datacenter/scripts/ensure-profile-complete.mjs check <profil>...`
  → JSON {exists, config, env, soulIdentity: BRAHMA|STOCK|custom, skillCount}.
- **Repair/provision manual**: `node ... ensure <profil>... [--force]` — merge
  skills dari default (root `AppData\Local\hermes`, 141 leaf skill), ganti SOUL
  hanya jika STOCK ("You are Hermes Agent…"), copy config/.env hanya jika
  absen, memory hanya jika absen. Idempoten.
- Root "default" = root Hermes home `C:/Users/TRIAL/AppData/Local/hermes`
  (BUKAN folder profiles/, dan BUKAN `C:/Users/TRIAL/.hermes` — folder itu
  sisa, isinya cuma gateway-logs + kanban.db tanpa profiles/).
- Akun↔profil binding diproteksi di `POST /api/user-access` (HQ); WebUI
  `/api/auth/signup` punya verifikasi pasca-clone (`ensure_profile_complete`
  di api/profiles.py) yang me-rollback profil parsial. WebUI HARUS direstart
  (proses pythonw server.py; watchdog respawn otomatis jika mati) agar
  patch routes.py aktif.
