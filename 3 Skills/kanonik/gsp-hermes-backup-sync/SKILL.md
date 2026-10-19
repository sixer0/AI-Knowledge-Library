---
name: gsp-hermes-backup-sync
description: >-
  Use when backing up/syncing GSP Hermes env repos to GitHub.
license: MIT
metadata:
  hermes:
    tags: [gsp, backup, sync, git, hermes-home, engine]
    category: gsp
---

# GSP Hermes Backup & Repo Sync

Runbook untuk backup/sinkronisasi state environment Hermes GSP ke repo GitHub.
Pemicu: "update repo dengan state hermes", "backup hermes", "sinkronkan
repo", "cek struktur repo gsp-*".

## Peta ekosistem repo (semua PRIVATE di GitHub sixer0)

| Repo | Isi | Lokal |
|---|---|---|
| `gsp-agent` | docs-backup/ + engine/ (salinan hermes-agent) + hermes-home/ (HERMES_HOME) | `C:/Users/TRIAL/gsp-agent` (clone 26-08; asal org gemilang-perkasa) |
| `gsp-brahma` | WebUI Brahma (Python server.py, port 9012) | `C:/Users/TRIAL/gsp-brahma` |
| `gsp-datacenter` | Agent HQ (Next.js, port 9011) | `C:/Users/TRIAL/gsp-datacenter` |
| `gsp-orchestrator-agent` | (terkait fleet, belum di-clone) | — |

Repo private → API publik GitHub mengembalikan **HTTP 404 = NORMAL**, bukan
kegagalan. Verifikasi read-back pakai `git ls-remote` == `git rev-parse HEAD`,
atau API dengan GITHUB_TOKEN dari `$LOCALAPPDATA/hermes/.env` (bandingkan token
dengan Python — file .env ber-CRLF, grep bisa false-mismatch). Lihat skill
`github-credential-ops` untuk audit akun/popup GCM/fix username per-host.

## Prosedur backup gsp-agent

1. **Clone** bila belum ada: `git clone https://github.com/sixer0/gsp-agent.git`
   (credential store menangani auth; username per-host sudah dipatok).
2. **Jalankan script sync** (sudah teruji, hardened):
   `python C:/Users/TRIAL/sync_gsp_agent.py` — atau salinan di
   `scripts/sync_gsp_agent.py` skill ini. Engine = mirror penuh lokal
   (copy + hapus file yang sudah tidak ada di lokal); hermes-home = copy
   konfigurasi & pengetahuan saja.
3. **Stage & cek** di `C:/Users/TRIAL/gsp-agent`:
   - `git add -A`
   - Cek secret/runtime ter-stage:
     `git diff --cached --name-only | grep -iE 'ticker|executions\.db|state\.db|kanban\.db|gateway_state|spawn-ledger|processes\.json|verification_evidence|models_dev_cache|provider_models_cache|ollama_cloud|channel_directory|\.usage\.json|skills_prompt_snapshot'` → harus kosong.
   - Cek file raksasa SEBELUM push (limit GitHub 100 MB):
     `git ls-tree -r -l HEAD | sort -k4 -rn | head`.
4. **Commit** conventional (`chore: backup GSP Hermes (YYYY-MM-DD) — ...`),
   **push**, **verifikasi** `git ls-remote origin refs/heads/main` == HEAD.

## Exclude wajib hermes-home (lean backup, tanpa secret/runtime)

- **Secret**: `.env`, `auth.json`, `*.pem`, `*.key` — JANGAN pernah di-track.
- **Runtime state**: state.db, kanban.db, gateway_state.json, spawn-ledger.json,
  processes.json, projects.db, verification_evidence.db, models_dev_cache*,
  provider/ollama caches, context_length_cache, channel_directory.json,
  install_id, .update*, .hermes_history, ticker_heartbeat/last_success,
  cron/executions.db, cron/notepad.db, cron/usage_audit.jsonl,
  .skills_prompt_snapshot, .usage.json, .last_used, .bundled_manifest,
  .curator_backups/, *.db-shm/*.db-wal/*.lock/*.pid.
- **Log/attachment**: `*.log` (mis. webui/bootstrap-9012.log), webui/attachments/.
  `.gitignore` repo sudah memuat `hermes-home/**/*.log` + `webui/attachments/`.

## Pitfall (semua kejadian nyata 26-08)

1. **Separator path Windows** — `os.walk` menghasilkan `cron\ticker_...`
   (backslash). Filter `startswith('cron/ticker_')` TIDAK match → runtime lolos
   ter-stage (127+168 file). SELALU normalisasi `rel.replace('\\','/')` di awal
   fungsi filter apa pun yang mencocokkan path.
2. **GitHub 100 MB limit** — log webui 183 MB sempat memblokir push (pre-receive
   hook). Cek `git ls-tree -r -l HEAD` sebelum push; `git rm --cached` + hapus
   file + amend (commit belum ter-push → amend aman).
3. **File runtime tracked dari backup lama** — setelah dihapus muncul sebagai
   `D` di status; pastikan semuanya runtime (filter `git status --short`), lalu
   commit penghapusan agar repo lean.
4. **Backup = snapshot state LOKAL** — carried commits GSP tetap ada; commit
   upstream yang belum di-`hermes update` tidak ikut. Jalankan `hermes update`
   dulu bila ingin engine merekam upstream terbaru.
5. **engine/ mirror = hapus file usang** — file only-in-repo (docs/agents/*
   pindah upstream, tests/stress/* dihapus, artefak default.tar.gz/log.txt)
   dihapus — itu benar, bukan kesalahan.

## Support files

- `scripts/sync_gsp_agent.py` — script sync hardened (jalankan, lalu stage/cek/commit/push).
- `references/backup-sync-gsp-agent-2026-08-26.md` — detail insiden sesi 26-08
  (angka diff, urutan fix, verifikasi akhir).

Untuk masalah kredensial/popup GCM/push gagal auth: lihat skill
`github-credential-ops`.
