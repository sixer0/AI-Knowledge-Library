# GSP Ecosystem — As-Built Inventory & Audit Checklist (2026-08-24)

Snapshot terverifikasi live 24-08-2026 oleh Brahma (audit read-only; deliverable
`Kajian_Ekosistem_Brahma_GSP_2026-08-24.docx` + `workspace/gsp-hermes/workspace/docs/2026_08_24_kajian_ekosistem/`).
Gunakan untuk refresh fakta layout fleet dan sebagai checklist audit ekosistem/kajian berikutnya.

## Paths (Windows, current)
- HQ dashboard: `C:/Users/TRIAL/gsp-datacenter` (Next.js 16 + Prisma + Tauri; codebase pindah dari `~/gsp-agent-headquarter`)
- WebUI Brahma: `C:/Users/TRIAL/gsp-brahma` (fork Hermes WebUI v0.51.792; daemon ctl.sh; RBAC `api/rbac.py`; 71 modul API)
- Bridge: `C:/Users/TRIAL/gsp-datacenter/hermes-bridge` (bridge.mjs, launch-bridge.sh; RUN_TIMEOUT_MS=1800000)
- Launcher/log: `C:/Users/TRIAL/gsp-ecosystem` (start-ecosystem.bat → gsp-ecosystem-start.sh; watchdog-*.sh; *.log *.pid)
- Kanonik scripts/skills: `C:/Users/TRIAL/workspace/gsp-hermes` (scripts/; skills/ = 12 skill EKAS)
- Shared workspace: `C:/Users/TRIAL/workspace/gsp-hermes/workspace` (AGENTS.md, MEMORY.md, memory/, docs/, vault/, ekas/, legacy-archive/)
- EKAS: `C:/Users/TRIAL/gsp-ekas` (model-lokal/ 270 teks; lengkap/ 430 file + 160 PDF)
- Firecrawl compose `C:/Users/TRIAL/firecrawl-src`; SearXNG `C:/Users/TRIAL/searxng`
- Wiki: `C:/Users/TRIAL/AppData/Local/hermes/wiki` (catatans/faktas/keputusans/pelajarans/proyeks/standars, 54 md)
- Kanban DB: `C:/Users/TRIAL/AppData/Local/hermes/kanban.db`

## Matriks layanan/port (saat audit)
| Service | Port | Proto | Catatan |
|---|---|---|---|
| HQ gsp-datacenter | 9011 | HTTPS self-signed | curl wajib `-k` |
| WebUI gsp-brahma | 9012 | HTTPS self-signed | pythonw bootstrap.py; butuh auth |
| Hermes Dashboard | 9010 | HTTP 127.0.0.1 | `hermes dashboard --port 9010 --host 127.0.0.1` |
| hermes-bridge | - | internal | node bridge.mjs; poll 5s |
| PostgreSQL 17 (bus HQ) | 5433 | TCP | `gsp_agent_hq`; pg_isready -p 5433 |
| PostgreSQL lain/legacy | 5432 | TCP | accepting |
| SearXNG (docker) | 8080 | HTTP | engine: bing/mojeek/qwant/yep/presearch |
| Firecrawl API (docker) | 3002 | HTTP | stack: api, playwright-service, redis, rabbitmq, nuq-postgres, foundationdb |
| Tailscale | 100.102.23.27 | WireGuard | node `desktop-br2dlt9` |

## Fakta fleet (40 gsp-* + default + user01)
- Semua: deepseek-v4-flash-0731 (kilocode), max_turns 150, cwd shared ws, search_backend=searxng.
- Vision (4, qwen3.7-flash): image-analyst, image-specialist, image-prompt-specialist, design-system-specialist. image-specialist punya image_gen; image-analyst/prompt-specialist/design-system TANPA terminal.
- Firecrawl extract (5): gsp-crawler-orchestrator, gsp-data-analyst, gsp-data-collector, gsp-social-media-crawler, gsp-vendor-crawler-specialist.
- Delegation: gsp-crawler-orchestrator (delegation+clarify); clarify: gsp-request-translator.
- ROSTER (src/app/api/agents/route.ts): 41 entri statis (komentar "43" STALE); groups core1/advisor2/controller1(+dinamis webui)/analysis9/execution19/verification7/utility2 → API 42 agen incl 1 dinamis.
- MISMATCH (masih terbuka): roster id `gsp-vendor-crawler-orchestrator` vs profil disk `gsp-crawler-orchestrator`.

## DB counts (psql gsp_agent_hq, 2026-08-24)
AgentRequest 42 (38 done/2 failed/1 rejected/1 running) · AgentState 33 · HermesTask 43 (41 done/2 blocked) · HermesMemory 54 · WebUiUser 2 · OrchestrationRecord 39 · AgentEvent 95 · DataStore 5 · Brief/Mission/User/Article 0

## Cron (2 watchdog, script-only no_agent)
- `19ae9f96d588` GSP Watchdog WebUI & HQ — every 180m — watchdog-webui-hq.py — last ok
- `f6ffb5e61aa7` GSP Fleet Gateway Watchdog — `55 1,4,7,10,13,16,19,22 * * *` — gsp_gateway_watchdog.sh — last error (22:55 24-08)

## Checklist perintah audit (terverifikasi)
```bash
hermes profile list                          # ~42 profil + state gateway
hermes --version                             # v0.20.5 + commit lokal
hermes kanban --board default list --json    # hitung kartu per status
curl -sk https://localhost:9011/api/agents
curl -sk https://localhost:9011/api/brahma/requests
curl -sk 'https://localhost:9011/api/information-library?scope=all'
docker ps; netstat -ano | grep LISTENING; tailscale status
# Hitungan DB: pakai FILE skrip tersimpan, JANGAN heredoc inline raksasa
# (parser terminal memblokir one-liner besar): bash <saved>.sh dengan
# DATABASE_URL diexport dari gsp-datacenter/.env
```

## Pitfall ditemukan saat audit
- HQ & WebUI HTTPS self-signed → curl butuh `-k`; probe http:// kosong/000.
- `hermes kanban complete <id> --result "..."` TIDAK menerima `--json` (hanya --result/--summary/--metadata). Cek `hermes kanban complete --help`.
- Heredoc psql inline besar → block parser; jalankan via file skrip tersimpan.
- PID file gateway (gsp-ecosystem/gateway-logs) adalah PID MSYS — tidak andal lintas proses; `hermes profile list` adalah sumber otoritatif state gateway.
- Status "online" di /api/agents bisa misleading (PID file stale → process.kill(pid,0) false positive).
- 2 kartu kanban blocked + 2 AgentRequest failed/rejected belum direkonsiliasi saat audit.

## Temuan (12) & rekomendasi (15) — ringkas
F1 roster mismatch (tinggi) · F2 gateway fleet down + cron watchdog error (tinggi) · F3 komentar roster stale · F4 kartu blocked · F5 request failed/rejected · F6 visibilitas user dinamis parsial · F7 PID/MSYS · F8 drift salinan skill (kanonik vs registry vs per-profil) · F9 firecrawl hanya 5 agen · F10 rantai EKAS PUTUS (GROUNDING/CYBERSECURITY/CIVIL) + R1 kosong · F11 wiki 3 sumber kebenaran · F12 infra adjacent tak terkelola (n8n/open-webui/crawler-admin/ops).
Recs: sinkron roster↔profil + gate validasi; restart fleet gateway (`bash gsp_gateway_watchdog.sh --restart`) + perbaiki cron; cek state gateway native; health-check harian terjadwal; rekonsiliasi blocked/failed; formalisasi RAW→VAULT→WIKI; sinkronisasi skill kanonik (hash); lengkapi rantai EKAS + R1; rollout firecrawl terkontrol; profil vision perlu terminal/read; agen observability; rotasi secret + TLS CA internal; audit RBAC & firewall.
