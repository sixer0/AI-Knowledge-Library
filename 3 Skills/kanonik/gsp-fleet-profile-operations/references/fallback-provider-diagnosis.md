# Diagnosing "agents keep falling back to the fallback provider" (validated 2026-09-01)

Symptom: user reports fleet work "terlempar ke fallback" (e.g. kilocode) even though the
primary provider (GSP-AI custom) is configured everywhere.

## The 4-layer check ladder (run in order; each layer has a cheap deterministic probe)

1. **Credential distribution** — usually NOT the cause once `register_gsp_ai_fleet.py`
   has run. Use `scripts/audit_provider_credentials.py` (fingerprint-compare per-profile
   key vs global .env, never prints keys). All-same ⇒ move on.
2. **Gateway health at IDLE** — `GET /v1/models` (200 + model list) and a few sequential
   chat completions with timing (`curl -w "%{http_code} %{time_total}"`). Fast 200s at
   idle prove the key+endpoint are fine; degradation is load-dependent, so idle probes
   passing does NOT exonerate the gateway.
3. **Runtime evidence in agent logs** — `$HERMES_HOME/logs/agent.log{,.1,.2}` is the
   ground truth. Parse with regex over lines (do NOT trust memory):
   - success mix: `API call #\d+: model=(\S+) provider=(\S+)` → count custom vs kilocode
     (fallback ratio = kilocode / total).
   - failures: lines matching `API call failed.*provider=(\w+)`; classify by
     `Request timed out.` / `APIConnectionError` / `Error code: \d+`.
   - fallback events: `Fallback activated: X → Y (provider)` (chat_completion_helpers)
     and `trying fallback` / `main fallback chain` (auxiliary_client).
   - **stickiness**: fallback persists for the rest of a session — compute run-length of
     provider per session id from the success lines to show it (e.g. custom×65 →
     kilocode×28 → custom×12).
   - correlate failure bursts with heavy fan-out missions (per-hour counter).
4. **Fallback chain itself** — the classic compound failure: primary degrades under
   load → fallback fires → fallback is ALSO dead → session dies. Check:
   - root + per-profile `auth.json` `credential_pool.kilocode[].last_status`
     (`exhausted`, code 429 = upstream rate limit, 402 = low credit). Read via
     `uv run --python 3.11 python` (bare `python` may hit the MS Store alias).
   - log line `API call failed after 3 retries ... provider=kilocode` = session death.

## Authoritative model-access probe (no doc needed)

Send a chat completion with a deliberately bogus model name using the real key. The
gateway's 403 `key_model_access_denied` message contains the authoritative
`This key can only access models=[...]` list. Compare against each profile's
`custom_providers[].models` block — stale entries (e.g. `auto-worker`,
`auto-auxilary` after a key re-scope) are a latent 403 bomb even when nothing is
failing today.

## Pitfalls hit during this audit

- `hermes_cli` is NOT importable as a module from arbitrary venvs; find source at
  `C:/Users/TRIAL/gsp-agent/engine/hermes_cli/` if code reading is needed.
- Session→profile resolution: query each `profiles/*/state.db` (and root `state.db`)
  for tables containing `session`, match `id LIKE '<prefix>%'`; unresolved ids are
  usually the global/default profile.
- Fleet gateway processes run in PAIRS (venv python + uv python per profile) — don't
  count them as duplicates/double-spawn.
- Bridge `No usable credentials for provider 'kilocode'` in old bridge.out.log may be
  historical (pre fix_fleet_env); check the timestamp before blaming current config.
- Report the fallback RATIO (e.g. 31% of calls on fallback over ~10 days) and the
  number of affected sessions — that's what makes "kebanyakan terlempar" quantified
  rather than vibes.
