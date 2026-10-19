# Membuat profil gsp-* baru secara batch (resep 24-08-2026, EKAS specialists)

Contoh teruji: 7 profil (`gsp-engineering-analyst`, `gsp-vss-specialist`,
`gsp-fiber-specialist`, `gsp-power-specialist`, `gsp-grounding-specialist`,
`gsp-security-specialist`, `gsp-infra-specialist`) dibuat 24-08-2026 dari 12 skill EKAS.
Skrip idempoten tersimpan: `C:/Users/TRIAL/workspace/gsp-hermes/scripts/create_ekas_specialists.py`
(adaptasi daftar profil per kebutuhan).

## Langkah pembuatan tiap profil

1. **Create**: `hermes profile create <profil> --no-skills --no-alias --description "<desc>"`
   - `--no-skills` = opt out bundled skill sync (marker `.no-bundled-skills`).
   - `--no-alias` = tanpa wrapper script.
2. **config.yaml** — TULIS ULANG dengan template fleet (jangan andalkan default):
   `model.default: deepseek/deepseek-v4-flash-0731`, `provider: kilocode`,
   `base_url: https://api.kilo.ai/api/gateway`, auxiliary vision `qwen/qwen3.7-flash`,
   `agent.max_turns: 150`, `terminal.cwd: C:/Users/TRIAL/workspace/gsp-hermes/workspace`,
   `platform_toolsets.cli: [file, terminal, skills, session_search, todo, web]`,
   `security.allow_private_urls: true`, `browser.allow_private_urls: true`,
   `web.search_backend: searxng`.
3. **.env** — salin dari profil existing (mis. gsp-librarian): variabel identik
   (SEARXNG_URL, KILOCODE_API_KEY, GITHUB_TOKEN, dst.) — jangan tulis manual.
4. **skills/** — `copytree` tiap skill yang dibutuhkan dari sumber (registry default
   `$LOCALAPPDATA/hermes/skills/gsp/<skill>` — FLAT di bawah `gsp/`, atau profil yang
   sudah punya) lalu `rmtree`+re-copy
   agar idempoten. Wajib ikut: `gsp-verification-before-completion`.
5. **SOUL.md** — template fleet:
   - Identitas (profil/peran/model) · Persona spesialis GSP
   - `## Aturan Khusus Peran` — 3-5 butir domain (ambil dari skill inti; sertakan
     batas "tidak ada di rak" yang relevan)
   - `## Skill — ALWAYS LOAD`: skill inti domain + gsp-verification-before-completion
   - `## Skill — ON DEMAND`: skill penunjang (pustaka-teknis, excel-master,
     webstack, skill lintas-domain)
   - `## Memori & Dokumentasi Bersama` (shared ws, Documentation Contract, Memory 6 langkah)
   - `## Aturan Kerja` — akhiri: "Akhiri respons dispatch dengan STATUS:
     complete|needs-review|blocked|failed".

## Kebijakan ALWAYS LOAD vs ON DEMAND (konvensi fleet)

- **ALWAYS LOAD** = skill yang dipakai di hampir setiap sesi peran itu (inti domain +
  verification) — jumlah kecil, jangan membebani konteks.
- **ON DEMAND** = skill situasional (penunjang lintas domain, webstack).
- `excel-master` (workbook) on demand di semua peran yang menyentuh perhitungan.
- Jangan pernah auto-load skill berat ke semua profil — hanya per profil sesuai peran.

## Registrasi ROSTER HQ (Windows — manual, add_hq_roster.py TIDAK ada)

Patch `C:/Users/TRIAL/gsp-datacenter/src/app/api/agents/route.ts`:
- Pola entri: `{ id, profile, name, emoji, role, model: "deepseek-v4-flash-0731", level: 3, group: <analysis|execution|verification|...> }`.
- Sisipkan sebelum baris komentar `// Level 3 — ...` yang sesuai, lalu **update komentar
  jumlah** di atas array (`// ── GSP AI Team roster — N static profiles ...`).
- Verifikasi: `curl -sk https://127.0.0.1:9011/api/agents` (Next dev hot-reload).

## Smoke-test profil baru (tanpa dashboard)

`hermes -p <profil> -z "...jawab singkat... akhiri STATUS: complete"` — WAJIB export
kredensial kilocode dari `~/.hermes/.env` ke env shell dulu (dispatch dari terminal gagal
"No usable credentials kilocode" tanpa itu):
`export KILOCODE_API_KEY="$(grep -E '^KILOCODE_API_KEY=' ~/.hermes/.env | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'")"`

Prompt panjang memicu blocklist hardline → simpan ke file dulu atau `bash <file>.sh`.

## Setelah buat profil

- Jalankan `bash gsp_gateway_watchdog.sh --restart` sekali (lihat
  `references/windows-fleet-watchdog.md`) agar profil baru mendapat proses serve + .pid.
- Update memori profil count + AGENTS.md shared ws bila menambah grup profil.
- GERBANG AUDIT-BEFORE-CLAIM (preseden PROF-MERGE-1010 PM-2, 10-10): profil yang
  "sudah terbangun" oleh sesi builder tetap WAJIB diaudit vs kontrak sebelum kartu
  ditutup — temuan nyata saat itu: (a) `platform_toolsets.cli` kehilangan `terminal`
  di TIGA profil sekaligus (template builder menyimpang dari resep langkah 2; worker
  tanpa terminal tidak bisa jalankan mekanik build), (b) skill fisik pembaca artefak
  belum terpasang meski kartu mensyaratkannya. Resep tambal aman: tulis-ulang YAML
  sequensial (bukan `config set` paralel) dengan gerbang diff terstruktur — muat YAML,
  ubah hanya kunci sasaran, simpan ulang (pertahankan CRLF + urutan kunci), re-parse
  dan buktikan SATU-SATUNYA perubahan adalah list yang ditarget; simpan backup `.orig`
  sebelum sentuh. Sensus gateway cukup via fungsi kanonik
  `gsp_fleet_gateway_check.active_profiles()` (dinamis per folder profil — profil baru
  otomatis terjaring tanpa edit watchdog).
- PITFALL SMOKE DARI SESI KANBAN (kejadian nyata 10-10, PM-2 t_07645289): smoke
  `hermes -p <p> -z` yang dijalankan dari sesi worker kanban MEWARISI
  `HERMES_KANBAN_TASK`/`HERMES_KANBAN_WORKSPACE`, jadi agen smoke ikut lifecycle kartu
  induk dan bisa menutup kartu itu lewat kanban_complete (satu run smoke bahkan
  berhasil complete; run berikutnya ditolak kernel 'already terminal' + meninggalkan
  komentar). Dampak: klaim penutupan berasal dari agen yang tidak diaudit untuk itu.
  Mitigasi: jalankan smoke dari sesi tanpa env kartu, atau `env -u HERMES_KANBAN_TASK
  -u HERMES_KANBAN_WORKSPACE hermes -p ... -z ...`; vonis penutupan tetap wajib
  diulang controller dengan pengukuran independen.