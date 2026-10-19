---
name: gsp-fleet-profile-operations
description: "Use when auditing or changing GSP fleet profiles (gsp-*)."
version: 1.1.0
tags: [gsp, fleet, profiles, hermes, propagation, windows]
---

# GSP Fleet Profile Operations (Windows)

## When to use
- User asks to check/audit all gsp-* profiles, add/remove/change a profile, or propagate a setting (env var, config key, skill, SOUL change) across the fleet.
- Rolling out the self-hosted web stack (SearXNG/Firecrawl/ddgs) to profiles — load `hermes-web-search-stack` too (its references/fleet-profile-propagation.md has the full recipe).

## Fleet layout on this Windows host
- Profiles: `C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-*` (33 profiles + user01 = WebUI user).
- Each profile: `config.yaml` (settings), `.env` (URLs/secrets), [`skills/`](../../kanonik/) (copied per-profile), `SOUL.md` (persona + "Skill — ALWAYS LOAD" / "Skill — ON DEMAND" lists), shared cwd `C:/Users/TRIAL/workspace/gsp-hermes/workspace`.
- **Canonical generator did NOT migrate**: manifest.json / scripts / kanonik skills are absent on Windows (Mac-era `~/workspace/gsp-hermes/scripts/{generate_profiles,build_skills,validate_profiles}.py`). Fleet changes = direct per-profile edits. If the generator is ever restored, regenerate profiles first, then re-apply fleet-wide webstack settings.

## Safe per-profile edit rules
- Config: use `hermes -p <profile> config set KEY VALUE` (verified working; never hand-edit config.yaml).
- Env: append `KEY=value` only if no line starts with `KEY=` (dedup); create the file if missing.
- Skills: `shutil.copytree` from the source skill dir into `<profile>/skills/<name>` (skip if present).
- SOUL.md: surgical first-occurrence replace ONLY, then assert the file still starts with `# SOUL` AND still contains the profile identity string. (Prevents the 2026-08-21 incident where a rewrite script dropped identity prefixes from all 32 SOUL files.)

## Fleet webstack target state (verified 2026-08-24)
- ALL 33 profiles: `SEARXNG_URL=http://localhost:8080` in .env, `web.search_backend=searxng`, skill `hermes-web-search-stack` in skills/ + listed in SOUL ON DEMAND.

## GSP-AI provider registration (verified 2026-08-27)
- ALL 44 gsp-* profiles carry a `custom_providers:` block in config.yaml registering **GSP-AI** (self-hosted OpenAI-compatible gateway `http://10.83.81.246:11400/v1`, models: auto-worker / auto-auxilary / auto-efficient / thinker) + `HERMES_CUSTOM_10_83_81_246_11400_API_KEY` in each profile .env (same key as global). **DEFAULT MODEL (also 2026-08-27): ALL 47 configs (44 gsp-* + firmanhidayat + user01 + global default) now use provider `GSP-AI` / model `auto-efficient` with `fallback_providers: [{provider: kilocode, model: kilo-auto/free}]`.** Set via [`C:/Users/TRIAL/workspace/gsp-hermes/scripts/set_gsp_ai_fleet_default.py`](../../../7%20Tools/scripts-repo-gsp-hermes/set_gsp_ai_fleet_default.py) (SEQUENTIAL — never concurrent, see Pitfalls). user01's custom_providers holds GSP-Server (100.102.23.27:11434) + GSP-AI; both must be preserved when merging.
- Idempotent rollout script: [`C:/Users/TRIAL/workspace/gsp-hermes/scripts/register_gsp_ai_fleet.py`](../../../7%20Tools/scripts-repo-gsp-hermes/register_gsp_ai_fleet.py) (re-run safe; verifies entry+key per profile; created gsp-firman-custom/config.yaml which was absent).
- gsp-firman-custom was the only profile missing config.yaml (bare profile); gsp-budi & gsp-creative were missing .env entirely (created by the script).
- Crawl-only (5 agents): `gsp-vendor-crawler-specialist`, `gsp-crawler-orchestrator`, `gsp-data-collector`, `gsp-social-media-crawler`, `gsp-data-analyst` — additionally `FIRECRAWL_API_URL=http://localhost:3002` + `web.extract_backend=firecrawl`.
  - **SAPU PM-4 (10-10, PROF-MERGE-1010): daftar ini historis.** Empat dari lima sudah diarsipkan 10-10 ke `C:/Users/TRIAL/gsp-archive/hermes-profiles-2026-10-10/` (kandidat hidup tersisa: `gsp-social-media-crawler` pun TIDAK ada di disk). Daftar hidup kanonis = `workspace/fleet/PROFILE-REGISTRY.json` (17 profil); jangan dispatch ke nama di baris ini tanpa cek folder profil.
- Non-crawl: NO `FIRECRAWL_API_URL`; their `web_extract` still works via the keyless ring (exa/parallel), NOT firecrawl — intended restriction.

## Idempotent tool
[`C:/Users/TRIAL/workspace/gsp-hermes/scripts/fix_fleet_webstack.py`](../../../7%20Tools/scripts-repo-gsp-hermes/fix_fleet_webstack.py) — env dedup + config set + skill copy + SOUL patch with identity guard + per-profile verification table. Rerun-safe.

## Kilocode credential (verified 2026-08-28)
- ALL 47 profiles (44 gsp-* + firmanhidayat + user01 + novriandy) carry `KILOCODE_API_KEY` in .env, exactly 1 line each, identical to the global `.env` key (JWT ~268 chars). On 2026-08-28 the 5 profiles that lacked it (firmanhidayat, gsp-budi, gsp-creative, gsp-firman-custom, user01) were fixed by append-dedup of the global key; fix verified via re-read fingerprint + live API test (`https://api.kilo.ai/api/gateway/v1/models` → 200, 368 models; chat on kilo-auto/free and kilo-auto/efficient both 200).
- kilocode needs only `KILOCODE_API_KEY` (see `hermes_cli/auth.py` ProviderConfig + plugin provider); `KILOCODE_BASE_URL` is optional and unused. The credential pool in `auth.json` (`credential_pool.kilocode`) stores only a `secret_fingerprint` and re-seeds from the profile .env on every `load_pool()` — it never overrides a corrected env value.
- A pool entry with `last_status: exhausted / code 402` is an account-balance issue (kilo.ai "Low Credit Warning"), self-recovering after the 1-hour 402 cooldown TTL once credits are topped up; not a config defect.

## Verification
- Re-scan all profiles (env/config/skills/SOUL) — every profile: sx_env=Y, search=searxng, skill=Y, soul=Y; crawl agents: fc_env=Y, extract=firecrawl; non-crawl: no FIRECRAWL_API_URL.
- Functional spot-check (no LLM cost): from the hermes-agent repo venv with `HERMES_HOME=<profile dir>`, call `tools.web_tools.web_search_tool('...')` and `asyncio.run(web_extract_tool(['https://example.com']))`.
- SOUL integrity: `head -3 SOUL.md` (identity prefix intact) + ON DEMAND line contains the new skill name.

## Profile provisioning guard (27-08-2026)
- RBAC-bound profiles must equal the root default (SOUL Brahma + 141 leaf skills).
- Check: `node C:/Users/TRIAL/gsp-datacenter/scripts/ensure-profile-complete.mjs check <profile>...`
- Repair/provision: same script with `ensure <profile>... [--force]` (idempotent; replaces only STOCK SOUL, merges skills, never clobbers live config/curated memory).
- Note: `C:/Users/TRIAL/.hermes` is a stale stub (no profiles/) — base home is `%LOCALAPPDATA%\hermes`.

## Pitfalls

- **Deteksi proses watchdog HARUS cocok bentuk cmdline aktual** (insiden 30-08): gateway fleet
  hidup sebagai `python -m hermes_cli.main --profile <p> gateway run`, tapi
  `gsp_fleet_gateway_check.py` mendeteksi pola `*serve*` → false-negative 50/52 "down" →
  mass-spawn 50 `serve` tiap 07:00 (menumpuk 122 proses python, memicu storm timeout mirror
  bridge). Setelah mengubah cara agen dijalankan, audit semua script deteksi/restart.
  Guard anti-mass-spawn (abort saat query gagal) tidak melindungi dari false-negative deteksi.
- **Guard middleware Next.js tidak berlaku saat dev-bypass** (SEC-001, 30-08): penjaga auth
  yang hanya ada di middleware bisa di-bypass total oleh `NODE_ENV=development`; letakkan
  guard kritis di LEVEL ROUTE (getToken di route handler) agar tetap berlaku.

- **NEVER run `hermes config set` concurrently across profiles** (verified 2026-08-27): a 3-worker parallel batch corrupted config.yaml on ALL profiles — dotted keys were written as TOP-LEVEL keys (`model.default` → top-level `default:`), leaving the `model:` block untouched while hermes reported success. Single / strictly-sequential invocations write correctly. When scripting fleet-wide `config set`, run ONE hermes process at a time (no ThreadPool/concurrent subprocesses) and verify by re-parsing each config.yaml afterward. If a profile was corrupted: `hermes -p <p> config unset default provider base_url api_key` (top-level junk) then re-set the dotted keys.
- All gsp-* profiles have the web toolset enabled (no `tools.disabled` entry).
- Setting `web.search_backend` alone makes `web_extract` resolve to the "firecrawl" default (selection_exists) → non-crawl profiles land on keyless rescue; that is intended since they have no firecrawl credentials.
- When adding a NEW profile, apply the same webstack defaults: search for all; firecrawl only if the role collects web data.
- `hermes-web-search-stack` is the umbrella for the self-hosted SearXNG/Firecrawl/ddgs stack itself (install, integration, WSL2 port-forwarding pitfalls) — load it for anything about the stack, not just fleet rollout.
