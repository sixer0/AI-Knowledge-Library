# Profile rename recipe (verified 2026-08-24)

Session-proven sequence for renaming a gsp-* profile on this Windows host.
Applied to `gsp-vendor-crawler-orchestrator` → `gsp-crawler-orchestrator`
(role broadened: orchestrates vendor AND social-media crawlers).

## 1. Stop the gateway
```bash
hermes -p <old> gateway stop
```

## 2. Kill orphaned `serve` processes (Windows file-lock)
`gateway stop` does NOT kill leftover `hermes … serve --host 127.0.0.1 --port 0`
processes. They hold the profile dir open → `mv` fails `Permission denied`.
```powershell
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*gsp-<old>*' } | Select-Object ProcessId,CommandLine | Format-List
Stop-Process -Id <pid> -Force
```
Re-check before renaming; also confirm the gateway python process is gone
(`Get-Process -Id <old gateway pid>`).

## 3. Rename the directory
```bash
mv "C:/Users/TRIAL/AppData/Local/hermes/profiles/<old>" "C:/Users/TRIAL/AppData/Local/hermes/profiles/<new>"
```

## 4. Rewrite SOUL.md (surgical, identity-guarded)
- `# SOUL — GSP <New Role>` title, `**Profil:** <new>`, `**Peran:**` broadened.
- Persona first line ("Sebagai <New Role>…").
- Add role-specific "Aturan Khusus" section(s); update ALWAYS LOAD / ON DEMAND
  skill lists (add the broadened-role skills).
- Preserve the "Memori & Dokumentasi Bersama" + "Aturan Kerja" blocks verbatim.
- After write: assert file starts with `# SOUL` and contains `<new>`.

## 5. Copy domain skills the broadened role needs
```bash
for s in gsp-social-media-collection-workflow gsp-social-media-data-standards; do
  cp -r "$HH/profiles/gsp-social-media-crawler/skills/$s" "$HH/profiles/<new>/skills/$s"
done
```

## 6. Update all references fleet-wide
```bash
python "C:/Users/TRIAL/workspace/gsp-hermes/scripts/rename_profile_refs.py"
```
- Replaces full name (`gsp-<old>`), short name (`<old>`), and title-case prose
  (`<Old Role>`), in order.
- Walks `profiles/`, `workspace/gsp-hermes`, default `memories/` and [`skills/`](../../).
- Skips `logs/`, `.git`, binaries (`.db/.sqlite/.jsonl/.log/.pid/.lock`),
  and gateway artifacts. Historical transcripts/logs keep the old name (correct).
- This also updates the default profile's `memories/MEMORY.md` and fleet skills,
  so no separate memory edit is needed for name consistency.

## 7. Clean stale gateway artifacts
```bash
rm "$HH/profiles/<new>/gateway.pid" "$HH/profiles/<new>/gateway.lock" "$HH/profiles/<new>/gateway_state.json"
rm "$HH/gateway-logs/<old>.pid" "$HH/gateway-logs/<old>.log"
```

## 8. Restart gateway with the new name
```bash
cd "C:/Users/TRIAL/workspace/gsp-hermes/workspace"
"$HH/hermes-agent/venv/Scripts/hermes" -p <new> gateway run   # background
```
Write the pid file from `profiles/<new>/gateway_state.json` (field `pid`) —
the bash background-wrapper PID is NOT the gateway PID.

## 9. Verify
- `hermes profile list | grep <new>` → present, running.
- `grep -rl "<old>" "$HH/profiles" workspace` → only logs/transcripts remain.
- `head -8 SOUL.md` → title + Profil + Peran correct.
- Config preserved: `hermes -p <new> config get web.search_backend` = searxng,
  `web.extract_backend` = firecrawl, `.env` has `SEARXNG_URL` + `FIRECRAWL_API_URL`.
- Functional: `HERMES_HOME=<new profile>` + `tools.web_tools.web_search_tool(...)`
  and `asyncio.run(web_extract_tool(['https://example.com']))`.

## Status-command nuance
`hermes -p X gateway status` prints the queried profile as
"✓ Gateway is running (PID: n)" and lists OTHER profiles in an
"Other profiles:" block below — the queried profile is NOT in that block, so
grep the whole output, not just the block.

## Watchdog note
`gsp_gateway_watchdog.sh` globs `hermes profile list | grep '^gsp-'`, so a
renamed profile is picked up automatically. Its default `HERMES_BIN` /
`GSP_WS` are still Mac-era paths on this host — override via env or fix.
