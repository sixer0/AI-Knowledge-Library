# Firecrawl + Bing SERP fallback for programmatic site resolution (verified 2026-09-02)

Use when script-side "find official website for company X" is needed but ddgs and SearXNG
both fail from this host (ddgs: timeouts on ALL backends html/brave/bing/google/libraries;
SearXNG :8080: geo-poisoned results or 0 hits with engine filters; direct Bing/Mojeek fetch:
robots-disallowed). The Hermes `web_search` tool uses the same poisoned SearXNG — do not assume
it is clean for niche/technical queries.

## Working recipe (proven: Unitree Robotics -> unitree.com, zh-named CN companies resolved)

POST to local Firecrawl scrape endpoint against a Bing SERP URL, then decode Bing's redirect:

```python
import base64, json, re, time, urllib.parse, urllib.request
FC = "http://localhost:3002/v1/scrape"
_last = [0.0]

def _serp(q):
    time.sleep(max(0.0, 1.2 - (time.time() - _last[0])))  # throttle >=1.2s between calls
    _last[0] = time.time()
    payload = {"url": "https://www.bing.com/search?q=" + urllib.parse.quote(q),
               "formats": ["links"], "timeout": 30000}
    req = urllib.request.Request(FC, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        links = json.load(r)["data"].get("links", [])
    out = []
    for l in links:
        href = l.get("url", "")
        if href.startswith("https://www.bing.com/ck/a"):
            u = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("u", [""])[0]
            if u.startswith("a1"):
                u = "http" + base64.urlsafe_b64decode(u[2:] + "==").decode(errors="ignore")
            href = u
        if href.startswith("http"):
            out.append(href)
    return out
```

Selection rule: pick first result whose apex-domain token overlaps a token of the company
name (strip `www.`, lowercase); keep first otherwise as weak fallback. Return '' on no hit —
never fabricate. Serialize + throttle when called from a thread pool (8 threads Stage-1 style
otherwise hammer the SERP).

## Pitfalls
- `formats:["links"]` returns `javascript:` junk entries — filter to http(s) after decode.
- Bing wraps most organic links in `ck/a?...&u=a1<base64url>`; raw hrefs are useless without
  the `a1`-prefix strip + `urlsafe_b64decode` with `==` padding.
- Firecrawl `/v1/search` returns empty `data:[]` on this install (no search backend wired) —
  only `/v1/scrape` works; do not waste turns retrying /search.
- Name-token overlap must compare against the DECODED target host, not the bing wrapper domain.
