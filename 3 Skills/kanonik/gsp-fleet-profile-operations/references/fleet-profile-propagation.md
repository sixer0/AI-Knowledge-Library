# Fleet propagation — SearXNG/Firecrawl/ddgs across gsp-* profiles (Windows)

Verified 2026-08-24 on this Windows host. 33 gsp-* profiles live under
`C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-*`. The canonical fleet
generator (manifest.json / scripts / kanonik skills) did NOT migrate from the
Mac, so fleet changes are applied per-profile, directly.

## Target state
- ALL 33 profiles: `SEARXNG_URL=http://localhost:8080` in `.env`,
  `web.search_backend=searxng` in `config.yaml`, the `hermes-web-search-stack`
  skill in `skills/`, and the skill listed in SOUL.md "Skill — ON DEMAND".
- CRAWL-ONLY (5 agents): `gsp-vendor-crawler-specialist`,
  `gsp-crawler-orchestrator`, `gsp-data-collector`,
  `gsp-social-media-crawler`, `gsp-data-analyst` — additionally
  `FIRECRAWL_API_URL=http://localhost:3002` in `.env` and
  `web.extract_backend=firecrawl`.
- Non-crawl profiles: NO `FIRECRAWL_API_URL`. Their `web_extract` still
  functions but through the keyless ring (exa/parallel), NOT firecrawl —
  distinguishable by content length differing from firecrawl's output
  (verified: 165 chars vs firecrawl's 180 for example.com).

## Audit (read-only)
Scan each profile: `config.yaml` `web:` section (search_backend /
extract_backend), `.env` (SEARXNG_URL / FIRECRAWL_API_URL), `skills/` dirs
(hermes-web-search-stack, gsp-searxng, gsp-firecrawl), SOUL.md (mentions of
searxng/firecrawl/crawl). All 33 gsp-* profiles have the web toolset enabled.

## Apply pattern (idempotent)
1. `.env`: append `KEY=value` only if no line starts with `KEY=` (dedup).
   Create the file if missing.
2. Config: `hermes -p <profile> config set web.search_backend searxng` —
   the `-p` global flag targets a profile's own config.yaml/.env.
3. Skill: `shutil.copytree` from
   `C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/hermes-web-search-stack`
   to `<profile>/skills/hermes-web-search-stack` (skip if present).
4. SOUL.md ON DEMAND patch: replace `` `gsp-searxng` `` with
   `` `gsp-searxng`, `hermes-web-search-stack` `` (first occurrence only).
   GUARD (prevents the 2026-08-21 SOUL-prefix-loss incident): after the
   replace, assert the file still starts with `# SOUL` and still contains
   the profile identity string; abort otherwise.

## Idempotent tool
`C:/Users/TRIAL/workspace/gsp-hermes/scripts/fix_fleet_webstack.py` does all
of the above + a verification table (env/search/extract/skill/soul per
profile). Rerun-safe (dedup + presence checks).

## Verification
- Re-scan: every profile must show sx_env=Y, search=searxng, skill=Y,
  soul=Y; crawl agents additionally fc_env=Y + extract=firecrawl; non-crawl
  must NOT have FIRECRAWL_API_URL.
- Functional (no LLM cost): from the hermes-agent repo venv with
  `HERMES_HOME` set to the profile dir, call
  `tools.web_tools.web_search_tool('...')` for search and
  `asyncio.run(web_extract_tool(['https://example.com']))` for extract.
- SOUL integrity spot-check: `head -3 SOUL.md` (identity prefix) and the
  ON DEMAND line contains `hermes-web-search-stack`.
