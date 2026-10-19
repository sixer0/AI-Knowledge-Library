# Firecrawl self-host (Docker Compose) — recipe

Official guidance: https://docs.firecrawl.dev/contributing/self-host and the repo's `SELF_HOST.md`.

## Steps (verified on Windows, tag v2.11.162)
```
cd /c/Users/TRIAL
git clone --depth 1 --branch v2.11.162 https://github.com/firecrawl/firecrawl.git firecrawl-src
```
Write `.env` in the repo root (minimal, from SELF_HOST.md):
```
PORT=3002
HOST=0.0.0.0
USE_DB_AUTHENTICATION=false
BULL_AUTH_KEY=<random hex>
NUM_WORKERS_PER_QUEUE=1
CRAWL_CONCURRENT_REQUESTS=2
MAX_CONCURRENT_JOBS=2
BROWSER_POOL_SIZE=2
```
Build and start — **name the services to skip foundationdb** (queue is Postgres via NUQ_BACKEND default; foundationdb images are otherwise pulled and run for nothing):
```
cd firecrawl-src
docker compose build api playwright-service nuq-postgres
docker compose up -d api playwright-service redis rabbitmq nuq-postgres
```
The `api` service runs `node dist/src/harness.js --start-docker` (API + workers). Build is heavy (node + playwright Chromium + custom postgres image) — run in background.

## Auto-start on Docker Desktop boot
Compose file has no restart policy; add a `docker-compose.override.yml`:
```yaml
services:
  api:                 { restart: unless-stopped }
  playwright-service:  { restart: unless-stopped }
  redis:               { restart: unless-stopped }
  rabbitmq:            { restart: unless-stopped }
  nuq-postgres:        { restart: unless-stopped }
```
Then `docker compose up -d` again to apply.

## Verify
```
curl -s -m 90 -X POST http://localhost:3002/v2/scrape \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","formats":["markdown"]}'
# expect success:true, data.markdown present
```
Root `GET http://localhost:3002/` → 200 once the harness is up (takes ~10-30s after containers start).

## Notes
- Self-hosted API key is optional; Hermes uses `FIRECRAWL_API_URL` and no key.
- If the first scrape right after `compose up` hiccups, re-test — workers re-initialize.
- Resource limits in the compose are generous (api 4 CPU/8G, playwright 2 CPU/4G); tune `NUM_WORKERS_PER_QUEUE` down for a home box.
