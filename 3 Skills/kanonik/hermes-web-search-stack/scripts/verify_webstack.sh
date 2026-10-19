#!/usr/bin/env bash
# Liveness check for the self-hosted Hermes web stack (SearXNG + Firecrawl).
# Usage: SEARXNG_URL=http://localhost:8080 FIRECRAWL_URL=http://localhost:3002 ./verify_webstack.sh
set -u
SEARXNG_URL="${SEARXNG_URL:-http://localhost:8080}"
FIRECRAWL_URL="${FIRECRAWL_URL:-http://localhost:3002}"

echo "== SearXNG ($SEARXNG_URL) =="
curl -s -m 20 --noproxy '*' "$SEARXNG_URL/search?q=test&format=json" \
  | python -c "import json,sys; d=json.load(sys.stdin); rs=d.get('results',[]); print('results:', len(rs)); [print('-', r.get('title','')[:60], '|', r.get('url','')[:60]) for r in rs[:5]]" \
  || echo "SearXNG FAILED"

echo "== Firecrawl ($FIRECRAWL_URL) =="
curl -s -m 90 --noproxy '*' -X POST "$FIRECRAWL_URL/v2/scrape" \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","formats":["markdown"]}' \
  | python -c "import json,sys; d=json.load(sys.stdin); print('success:', d.get('success'), '| markdown len:', len(d.get('data',{}).get('markdown','')))" \
  || echo "Firecrawl FAILED"

echo "== Hermes integration (no LLM) =="
HERMES_HOME="${HERMES_HOME:-$LOCALAPPDATA/hermes}"
cd "$HERMES_HOME/hermes-agent" 2>/dev/null || { echo "hermes-agent dir not found"; exit 0; }
HERMES_HOME="$HERMES_HOME" ./venv/Scripts/python -c "
from tools.web_tools import web_search_tool
r = web_search_tool('openai', 3)
import json
d = json.loads(r)
print('search success:', d.get('success'), '| results:', len(d.get('data',{}).get('web',[])))
if d.get('data',{}).get('rescued_from'):
    print('NOTE: rescued_from', d['data']['rescued_from'], '-', d['data'].get('backend_error','')[:80])
" 2>&1 | tail -3
