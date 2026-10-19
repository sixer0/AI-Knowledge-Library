# SearXNG self-hosted (Docker) — recipe + pitfalls

## Container recipe (Windows host, verified)
```
mkdir -p /c/Users/TRIAL/searxng
SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
printf 'use_default_settings: true\nserver:\n  limiter: false\n  public_instance: false\nsearch:\n  formats:\n    - html\n    - json\n' > /c/Users/TRIAL/searxng/settings.yml
docker run -d --name searxng -p 8080:8080 \
  -v /c/Users/TRIAL/searxng:/etc/searxng:rw \
  -e SEARXNG_BASE_URL=http://localhost:8080/ -e "SEARXNG_SECRET=$SECRET" \
  --restart unless-stopped searxng/searxng:latest
```
Note: port 8080 may be held on Windows by `tailscaled` bound to Tailscale IPs only (e.g. `100.x:8080`). Binding `127.0.0.1:8080` (or `8080:8080`) via Docker is fine after the WSL2 NAT fix — but if Docker's wildcard bind conflicts, publish a different host port (`-p 8088:8080`) and point `SEARXNG_URL` there.

## Crash-loop fix: `schema of /etc/searxng/limiter.toml is invalid!`
Symptom: container Restarting; logs show the limiter config validation failing on keys like `botdetection.ip_limit.count` / `window` / `filter` — keys that are NOT in the current schema.
Fix: replace the volume's `limiter.toml` with the package's own schema file (valid by definition):
```
docker run --rm --entrypoint cat searxng/searxng:latest /usr/local/searxng/searx/limiter.toml > /c/Users/TRIAL/searxng/limiter.toml
docker restart searxng
```
The schema lives at `searx/limiter.py`: `LIMITER_CFG_SCHEMA = Path(__file__).parent / "limiter.toml"` and `searx/botdetection/config.py` rejects unknown keys.

## Engine strategy (Indonesian IPs: Google/DDG/Brave often blocked)
From a home/ISP Indonesian IP, `google` → "Suspended: CAPTCHA", `duckduckgo` → timeout, `brave` → "too many requests", `startpage` → CAPTCHA. Wikipedia works.
Enable anti-CAPTCHA engines by extending settings.yml:
```yaml
use_default_settings: true
server:
  limiter: false
  public_instance: false
search:
  formats:
    - html
    - json
engines:
  - name: bing
    disabled: false
    weight: 2
  - name: mojeek
    disabled: false
  - name: qwant
    disabled: false
  - name: yep
    disabled: false
  - name: presearch
    disabled: false
```
Key fact: with `use_default_settings: true`, the `engines:` list **merges by name** — it toggles/adds engines, it does NOT replace the default engine set. Verify with `/config` (engine count + enabled flags):
```
curl -s http://localhost:8080/config | python -c "import json,sys; d=json.load(sys.stdin); print(len([e for e in d['engines'] if e.get('enabled')]), 'enabled')"
```

## Liveness test
```
curl -s -m 15 --noproxy '*' "http://localhost:8080/search?q=test&format=json" | python -c "import json,sys; d=json.load(sys.stdin); print('results:', len(d.get('results',[])))"
```
The JSON response also exposes `unresponsive_engines` — useful to see which engines are blocked without reading logs.
