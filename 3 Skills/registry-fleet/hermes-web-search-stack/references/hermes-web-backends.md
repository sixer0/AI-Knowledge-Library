# Hermes web backend wiring + ddgs-first rescue patch

## Config resolution (from agent/web_search_registry.py + tools/web_tools.py)
Selection precedence:
1. `web.search_backend` / `web.extract_backend` (per-capability override; strict — no availability probe, a broken selection surfaces its own error)
2. `web.backend` (shared fallback)
3. Single registered+available provider, else legacy preference order: firecrawl → parallel → tavily → exa → searxng → brave-free → ddgs (filtered by availability)
4. Keyless free-tier walk (exa/parallel anonymous MCP) — strictly last; disable via `web.keyless_fallback: false`

There is **no `web.search_fallback` key** (grep of source confirms). The only native fallback on failure is the one-shot keyless rescue (`web.keyless_rescue`, default on) through `plugins/web/keyless_mcp.py` ring `_KEYLESS_RING = ("exa","parallel","tavily","firecrawl","keenable")` — stateless per call; next call retries the configured backend.

## ddgs-first rescue patch (local commit pattern)
Goal: when the configured search backend (e.g. searxng) fails, try ddgs BEFORE the keyless ring.
Location: `tools/web_tools.py`, function `_rescue_search(provider_name, original_error, query, limit)`.
Insert before `rescued = search_with_failover(...)`:
```python
    try:
        from agent.web_search_registry import get_provider as _rescue_get_provider
        ddgs_provider = _rescue_get_provider("ddgs")
        if (ddgs_provider is not None
                and ddgs_provider.supports_search()
                and ddgs_provider.is_available()):
            ddgs_result = ddgs_provider.search(query, limit)
            if ddgs_result.get("success"):
                data = ddgs_result.setdefault("data", {})
                data["rescued_from"] = provider_name
                data["backend_error"] = (
                    f"Configured backend '{provider_name}' failed this call "
                    f"({(original_error or 'unknown error')[:300]}); result served "
                    "by ddgs fallback. The next call will use "
                    f"'{provider_name}' again.")
                return ddgs_result
    except Exception as exc:  # noqa: BLE001
        logger.debug("ddgs rescue attempt failed: %s", exc)
```
Commit as a normal local commit (the install is git-based and already carries local commits):
```
cd "$HERMES_HOME/hermes-agent" && git add tools/web_tools.py && git commit -m "feat(web): try ddgs first in one-shot search rescue"
```

## ddgs facts
- Availability = `ddgs` package importable in the hermes venv: `"$HERMES_HOME/hermes-agent/venv/Scripts/python" -m pip install ddgs`.
- ddgs search runs in a disposable child process with a 30s wall-clock cap (GIL-safe isolation) — safe to call from the rescue path.
- Search-only provider (`supports_extract() == False`) — extract fallback remains the keyless ring.

## Direct verification without LLM cost
```
cd "$HERMES_HOME/hermes-agent"
HERMES_HOME="$HERMES_HOME" ./venv/Scripts/python -c "
from tools.web_tools import web_search_tool
print(web_search_tool('test query', 5)[:600])"
```
For extract (async):
```
import asyncio, json
from tools.web_tools import web_extract_tool
r = json.loads(asyncio.run(web_extract_tool(['https://example.com'])))
print(r['results'][0]['title'], r['results'][0]['error'])
```
Fallback proof: stop the backend (e.g. `docker stop searxng`), run web_search_tool → result carries `"rescued_from": "searxng"` and `backend_error` mentioning "ddgs fallback". Restart the backend after.
