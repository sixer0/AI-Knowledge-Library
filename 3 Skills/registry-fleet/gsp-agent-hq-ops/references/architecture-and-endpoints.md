# GSP Agent HQ & Brahma WebUI — Arsitektur & Kontrak Endpoint

Logfix 24-08-2026: signup WebUI + create account HQ User Access + filter IL.

## Peta arsitektur

- **Agent HQ** = `C:/Users/TRIAL/gsp-datacenter` (Next.js 16.1.6, Turbopack).
  - Port **9011**, HTTPS self-signed (`--experimental-https`).
  - Dijalankan MANUAL (tidak ada launcher script). Command persisnya:
    ```
    cd /c/Users/TRIAL/gsp-datacenter && node node_modules/next/dist/bin/next dev \
      -p 9011 --experimental-https --experimental-https-key certs/hq-key.pem \
      --experimental-https-cert certs/hq-cert.pem >> hq-dev.out.log 2>> hq-dev.err.log
    ```
  - Proses: parent `node .../next dev` + child `start-server.js`.
  - Log: `hq-dev.out.log` / `hq-dev.err.log` di root repo.
  - Middleware (src/middleware.ts): di dev mode (NODE_ENV=development) SEMUA
    request diizinkan (`NextResponse.next()`); di build prod baru NextAuth
    berlaku. Jadi jangan asumsikan proteksi saat testing dev.
- **Brahma WebUI** = `C:/Users/TRIAL/gsp-brahma` (Python `server.py`).
  - Port **9012**, HTTPS self-signed (TLS cert `certs/webui-cert.pem`).
  - Daemon: `cd gsp-brahma && ./ctl.sh restart`. PID/log:
    `C:/Users/TRIAL/AppData/Local/hermes/webui.{pid,log}` +
    `webui/bootstrap-9012.log`.
  - RBAC via env: `HERMES_WEBUI_RBAC=1`, `HERMES_WEBUI_RBAC_API_URL`,
    `HERMES_WEBUI_RBAC_TOKEN`, `HERMES_WEBUI_RBAC_SIGNUP=1` (open signup),
    `HERMES_WEBUI_RBAC_CLONE_FROM` (default "default").

## Token RBAC (wajib sama)

- WebUI mengirim `x-rbac-token: <HERMES_WEBUI_RBAC_TOKEN>` ke HQ.
- HQ memvalidasi dengan `process.env.WEBUI_RBAC_TOKEN` (lib/webui-rbac.ts,
  `rbacTokenOk()` — constant-time compare).
- **Pitfall verifikasi**: ekstraksi bash `grep -E '^KEY=' .env | cut -d= -f2-`
  pada file CRLF menyisakan `\r` di nilai → md5 beda padahal token sama.
  Bandingkan dengan Python:
  ```python
  def read_env(p, key):
      for line in open(p, encoding='utf-8'):
          line = line.strip()
          if line.startswith(key + '='):
              return line.split('=', 1)[1].strip().strip('"').strip("'")
  ```
- Rekonsiliasi: tulis ulang .env HQ `WEBUI_RBAC_TOKEN` = nilai brahma
  (pertahankan baris lain; newline='\n').

## Endpoint RBAC (WebUI ⇄ HQ)

| Endpoint HQ | Method | Guard | Fungsi |
|---|---|---|---|
| `/api/brahma/rbac` | GET/POST | x-rbac-token | list / create user langsung |
| `/api/brahma/rbac/signup` | POST | x-rbac-token | create USER (dari WebUI signup) |
| `/api/brahma/rbac/login` | POST | x-rbac-token | verifikasi kredensial |

Payload signup: `{username, password, displayName?, hermesProfile}` → 201
`{ok, user}`; 409 kalau username/hermesProfile sudah dipakai; 400 validasi.

Endpoint browser HQ (tanpa token, dev posture):
- `/api/user-access` GET/POST — list/create WebUiUser
- `/api/user-access/[id]` PATCH/DELETE — role/displayName/password, hapus
  (admin terakhir dilindungi 409).

DB: Postgres via Prisma, tabel `WebUiUser` (username, passwordHash
`scryptSync` salt:hash, role USER/ADMINISTRATOR, hermesProfile).

## Alur signup WebUI (/api/auth/signup)

1. Gate: `_rbac_configured() && signup_allowed()` → selain itu **404
   "Signup is not enabled"** (penyebab utama "signup tidak bisa create akun").
2. Rate limit per IP (`_check_login_rate`).
3. Validasi: username regex `^[a-z0-9][a-z0-9_-]{0,31}$` (bukan "default"),
   password ≥8.
4. `create_profile_api(username, clone_from='default', clone_config=True)`
   → clone profil Hermes dari root home (bukan folder `profiles/default` —
   "default" = root HERMES_HOME, ditangani `_is_root_profile`).
5. `hq_signup(...)` → kalau bukan 201, rollback `delete_profile_api`.
6. Auto-login: create_session(auth_type="rbac", bound_profile=username,
   role="USER") + set cookie sesi & profil.

Alur login RBAC: `hq_login` → create_session(bound_profile=hermesProfile).
**Tidak mengecek profil ada di disk** — akun dengan profil hilang tetap bisa
login & pakai panel USER (chat/models/sessions); hanya folder profil yang
tidak tersedia. `/api/status` khusus ADMIN → 403 untuk USER itu normal.

## User creation paths (dua jalur)

1. **WebUI signup** → otomatis clone profil (profil = username) → akun penuh.
2. **HQ /user-access form** → hanya row DB; `hermesProfile` HARUS sudah ada
   (atau user tak bisa pakai WebUI). UI menampilkan datalist profil existing.
   - 400 wall: username format / password <8 / profil kosong — fix 24-08-2026:
     validasi client berbahasa Indonesia + lowercase username sebelum submit.
   - 409: profil sudah terikat user lain.

## Information Library

- Halaman: `src/app/information-library/page.tsx`; API:
  `src/app/api/information-library/route.ts`.
- `SHARED_WORKSPACE` env di .env HQ → `C:/Users/TRIAL/workspace/gsp-hermes/workspace`
  (default di code masih path Mac `/Users/mbp/...` — WAJIB override di Windows).
- GET params: `scope=all|wiki|workspace|vault`, `q`, `type`, `status`.
  - `all` = wiki (DB HermesMemory, max 300) + workspace (scan FS, md/markdown/mdx
    + folder docs/ dengan file non-md → type project + files[]).
  - `vault` = workspace/vault (staging, frontmatter YAML `---\nkey: value\n---`,
    status lifecycle: usulan/menunggu_verifikasi/menunggu_persetujuan/
    menunggu_upload_user/ditolak/terkurasi/terbit).
  - `typeCounts`/`statusCounts` dihitung dari daftar TERFILTER (progressive
    filtering).
- Standar filter (fix 24-08-2026):
  - Satu komponen `FilterChip` (label+count+tone+active) untuk type & status.
  - Chip status vault BISA DIKLIK (toggle; klik lagi → "all"); selalu ada chip
    "All".
  - Toggle Active/All hanya untuk scope non-vault (vault pakai chip status),
    dengan count (Active n / All n).
  - `resetFilters()` satu fungsi: q, type, scope, statusAll, vaultStatus.
  - Toolbar `flex-wrap` responsif.
  - Tone map status vault: usulan/proposal/pending=warn, tinjau/review=accent,
    kurasi/terbit/publish/approved/active=up, tolak/reject/archiv/superseded=down.

## Catatan verifikasi sesi 24-08-2026

- Signup probe `zzsig1`: 200, profil diclone, login 200, muncul di
  `/api/user-access`. Bersihkan: DELETE user + `rm -rf profiles/<name>`.
- Create HQ probe `e2ehq` (profil gsp-explore): 201, login 200, panel USER 200,
  endpoint admin ditolak 403 → RBAC aman.
- DELETE dengan ID dari command substitution butuh `tr -d '\r'` — tanpa itu
  curl HTTP 000 (URL rusak).
- curl ke HQ via http:// → HTTP 000 (empty reply); HQ hanya HTTPS.
- Browser (browser_exec) bisa hang di halaman HTTPS self-signed — verifikasi
  UI via bundle grep (scripts/verify_nextjs_bundle.py) + uji API langsung.
