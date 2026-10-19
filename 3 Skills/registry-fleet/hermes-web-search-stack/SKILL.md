---
name: hermes-web-search-stack
description: "Self-hosted SearXNG/Firecrawl/ddgs as Hermes web backends."
version: 1.1.0
tags: [hermes, searxng, firecrawl, ddgs, websearch, self-hosted, docker, windows, wsl2]
---

# Hermes self-hosted web search & extract stack (SearXNG + Firecrawl + ddgs)

## When to use
- User asks to install/integrate SearXNG, Firecrawl, or ddgs as Hermes web backends.
- Web search returns nothing, engines blocked, extract fails, or "fallback search" is requested.
- Windows symptom: a Docker container is Up but its published port is unreachable from localhost (curl HTTP 000 / "Empty reply").

## Hermes web config model (v0.20.x — verified from source)
- Config keys: `web.search_backend` (search per-capability), `web.extract_backend` (extract per-capability), `web.backend` (shared fallback), `web.keyless_rescue` (default on), `web.keyless_fallback` (default on).
- Env vars: `SEARXNG_URL` (search), `FIRECRAWL_API_URL` (self-host) or `FIRECRAWL_API_KEY` (cloud).
- **There is NO `web.search_fallback` key.** Native failure path = one-shot keyless rescue ring (`exa`, `parallel`, `tavily`, `firecrawl`, `keenable`), stateless per call. To make ddgs the fallback you must patch (see references/hermes-web-backends.md).
- Providers are plugins under `<hermes-agent>/plugins/web/{searxng,firecrawl,ddgs,...}/provider.py`. Availability: searxng needs `SEARXNG_URL` set; ddgs needs the `ddgs` package importable in the hermes venv.
- Set config with `hermes config set`, env in `$HERMES_HOME/.env` (URLs/secrets only).

## Setup summary (Windows path, verified 2026-08)
1. **SearXNG** — Docker container on 127.0.0.1:8080 with volume + settings.yml. See references/searxng-docker.md (includes limiter.toml crash-loop fix + anti-CAPTCHA engine strategy).
2. **Firecrawl** — clone repo at pinned tag, `.env`, `docker compose build`, `docker compose up -d <services>`. See references/firecrawl-selfhost.md.
3. **Hermes integration** — `hermes config set web.search_backend searxng`, `web.extract_backend firecrawl`; append `SEARXNG_URL` + `FIRECRAWL_API_URL` to `.env`.
4. **ddgs fallback** — `pip install ddgs` into the hermes venv; optional local patch for ddgs-first rescue (references/hermes-web-backends.md).
5. **Verify** — scripts/verify_webstack.sh for service liveness; direct Hermes tool calls for integration (no LLM cost).

## Critical Windows/WSL2 pitfall — Docker published ports unreachable
Symptom: container Up, `docker port` shows a mapping (or is empty), but curl from Windows to `localhost:PORT` → HTTP 000 / "Empty reply", while the same service answers from inside the container or inside the docker-desktop distro.
Root causes seen on this host: `.wslconfig networkingMode=mirrored` breaks Docker Desktop's Windows→WSL port forwarding; Hyper-V firewall `DefaultInboundAction=Block` can also block.
Fix ladder (in order):
1. Hyper-V firewall → Allow (needs UAC elevation): `Set-NetFirewallHyperVVMSetting -Name '{40E0AC32-46A5-438A-A0B2-2B479E8F2E90}' -DefaultInboundAction Allow`.
2. If still broken → switch `.wslconfig` to `networkingMode=default` (NAT), back up the original, `wsl --shutdown`, restart Docker Desktop. **NAT mode is what actually fixed it** (mirrored-mode relay accepts TCP but drops payloads).
Full diagnostic ladder + commands: references/windows-docker-wsl2-ports.md.

**Testing pitfall that wasted a session:** `curl` (and bash `/dev/tcp`) against a non-HTTP service (e.g. redis on a published port) reports misleading "Empty reply from server" / HTTP 000 even when the relay works fine. Always probe with the service's own protocol — redis: send `PING` and expect `+PONG` via a Python socket (bash /dev/tcp + head can silently return nothing in git-bash).

## Verification without LLM cost
From the hermes-agent repo with `HERMES_HOME` set, call the tool wrappers directly:
```
cd "$HERMES_HOME/hermes-agent" && HERMES_HOME="$HERMES_HOME" ./venv/Scripts/python -c "
from tools.web_tools import web_search_tool
print(web_search_tool('test query', 5)[:400])"
```
`web_extract_tool` is async — wrap in `asyncio.run()`. These exercise the exact plugin/backend resolution path the agent uses. Optionally finish with a real `hermes chat -q "…web_search… web_extract…"`.

## Verified API shapes & plugin known-limits (measured 2026-09-11, WF-CRAWL-0911)
- Valid Firecrawl shapes on this build: `POST /v2/scrape {url, formats, timeout}` -> 200 synchronous; `POST /v2/batch/scrape {urls, formats}` -> async job, poll `GET /v2/batch/scrape/<id>` until completed; `POST /v2/crawl {url, limit}` -> async, poll. Extra body keys `maxDepth`/`formats`/`depth` on `/v2/crawl` are REJECTED (HTTP 400 unrecognized_keys) - any recipe sending them is wrong.
- Plugin known-limit (searxng): Hermes `web_search` sends only q/format/pageno with a hardcoded 15s timeout and cannot pass `engines=`/`categories=` - engine fan-out needs direct HTTP `/search?...&engines=a,b,c` recipes (see skill `gsp-searxng`).
- Plugin known-limit (firecrawl): the provider exposes only `/v2/search` + `/v2/scrape`; `/v2/batch/scrape` and `/v2/crawl` are NOT native tools - bulk/parallel extraction recipes must go direct HTTP (see skill `gsp-firecrawl`).
- Fleet norm: collection / explorer / crawler workflow classes MUST run search=searxng + extract=firecrawl in parallel per skills `gsp-searxng` / `gsp-firecrawl` (authoritative recipes live there; reference, do not duplicate).

## Pitfalls
- SearXNG crash-loop `schema of /etc/searxng/limiter.toml is invalid` → the generated template has keys not in the schema; copy the package's own `/usr/local/searxng/searx/limiter.toml` into the volume (it IS the schema, so it validates).
- Google/DDG/Brave/Startpage frequently CAPTCHA/timeout from Indonesian IPs — enable bing/mojeek/qwant/yep/presearch via `use_default_settings: true` + `engines:` list (merges by name; it does NOT replace the default set).
- Firecrawl compose includes unused foundationdb services — skip them by naming services in `docker compose up -d`.
- Local Hermes installs here are git-based and already carry local commits; the ddgs rescue patch should be committed so it survives and is traceable.
- This machine is Windows; stack paths are `C:/Users/TRIAL/...` — Mac-era paths (`~/searxng`, `/Users/mbp/...`) in memory are historical.

## Support files
- references/searxng-docker.md — container recipe, limiter.toml fix, engine strategy, /config verification.
- references/firecrawl-selfhost.md — pinned-tag clone, .env, build/up, restart override, /v2/scrape test.
- references/hermes-web-backends.md — config resolution, keyless rescue details, ddgs-first patch recipe, direct-tool verification.
- references/windows-docker-wsl2-ports.md — full diagnosis ladder + NAT-mode fix + protocol-aware probing.
- scripts/verify_webstack.sh — liveness check for SearXNG + Firecrawl.
