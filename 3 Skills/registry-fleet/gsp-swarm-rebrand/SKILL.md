---
name: gsp-swarm-rebrand
description: Use when touching GSP WebUI/HQ branding or adding new pages.
license: MIT
metadata:
  hermes:
    tags: [gsp, swarm, rebrand, branding]
    category: gsp
---

# GSP SWARM Rebrand (28-08-2026)

Semua output user-visible direbrand **Brahma/Hermes → Swarm**. Logo: attachment
`webui/attachments/c77aaa467ea2/screenshot-1787908800723.png` (hex emblem + wordmark SWARM).

## Yang sudah diubah
| Komponen | Perubahan |
|---|---|
| WebUI `gsp-brahma` | `<title>Swarm`, i18n.js 14 locale (~800 string), login/RBAC page (`Swarm — Sign in`), manifest.json, favicon/PWA icons (digenerate dari logo; skrip `~/workspace/swarm_rebrand/gen_icons.py`), fallback `bot_name` → 'Swarm' (config.py, onboarding.py, ui.js, boot.js, panels.js, routes.py), halaman "Swarm is restarting", `api/updates.py` label |
| Agent HQ `gsp-datacenter` | layout.tsx `GSP Swarm HQ` + description, sidebar logo 'S' + teks, roster `name: "Swarm"` (id tetap `brahma`), semua halaman (brahma/agents/tasks/user-access/IL/command-palette/approval-inbox/briefing/runs/dispatches), login page 'S' + `GSP Swarm HQ`, banner SVG, X-Title API articles/trends |
| Konektor | bridge.mjs BRIEF_PROMPT (netral "your memory wiki"); shim CLI `swarm` di `AppData/Local/hermes/bin/swarm` (exec hermes.exe) agar hint `swarm model`/`swarm auth` valid |
| Identitas | 48 SOUL.md (root + semua profil): Brahma→Swarm, GSP Agent Headquarter→GSP Swarm HQ; AGENTS.md shared workspace heading |

## Kontrak internal TIDAK diubah (jangan di-rebrand!)
- id roster `"brahma"`, map agent-chat `brahma: 'default'`
- Route `/api/brahma/*`, halaman `/brahma`, href `/brahma`
- DB Prisma `HermesTask`, `HermesMemory`, kolom `hermesTaskId`, store key `hermes-*`
- Env `HERMES_*` (termasuk `HERMES_WEBUI_PASSWORD` yang tampil di pesan — itu nama env asli), header `X-Hermes-CSRF-Token`, key i18n `status_hermes_home`, localStorage `hermes-*`
- Nama binary `hermes`, path `~/.hermes`, storage `hermes-lang`

## Sisa yang DISENGAJA
- Komentar kode berisi Brahma/Hermes (jejak audit) — tidak user-visible.
- Teks "(Hermes engine)" di AGENTS.md = referensi teknis mesin.

## Verifikasi cepat
```bash
curl -sk https://localhost:9011/ | grep -o "<title>[^<]*</title>"        # GSP Swarm HQ
curl -sk https://localhost:9011/api/agents | head -c 120                  # "name":"Swarm"
curl -sk https://localhost:9012/login | grep -iE "hermes|brahma"          # (kosong)
swarm -z "siapa kamu?"                                                    # jawab sebagai Swarm
```

## Pitfall
- `ctl.sh restart` bisa gagal bunuh proses lama (PID stale, watchdog men-spawn ulang) → cek PID listener `netstat -ano | grep 9012` sebelum klaim.
- i18n.js: locale non-EN punya genitif kabur (d'Hermes, Hermes\'e, Hermes-Dashboard) — pass terpisah per-pola; env var & key harus di-skip.
- JSX text node & triple-quoted string Python TIDAK kena regex quote → perlu pass manual per-baris.
- Perubahan kedua repo BELUM di-commit (git status menunjukkan M massal + untracked certs/ lama).
