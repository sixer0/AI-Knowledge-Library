#!/usr/bin/env python3
"""Verify a Next.js dev page's compiled bundle contains expected strings.

Use when the browser daemon is unavailable/stuck (e.g. HTTPS self-signed
interstitial pages) and you need to confirm a UI edit actually shipped:
fetch the page HTML, extract /_next/static/chunks/*.js URLs, and grep each
chunk for the new strings. Also reports recent errors from the Next dev log.

Usage:
    python verify_nextjs_bundle.py <base_url> <page_path> [string1 string2 ...]

Example:
    python verify_nextjs_bundle.py https://localhost:9011 /information-library \
        "vaultStatus" "FilterChip" "Clear filters"

Notes:
- Skips TLS verification (self-signed local dev certs).
- Strings may be unicode-escaped in the bundle; prefer ASCII identifiers
  (state names, class names, attributes) over long prose when choosing needles.
- If a transient Fast Refresh error appears in hq-dev.err.log (e.g.
  "X is not defined" mid-patch), re-fetch the page once and confirm the error
  does NOT re-appear — that proves the transient state resolved.
"""
import re
import ssl
import subprocess
import sys
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://localhost:9011"
PAGE = sys.argv[2] if len(sys.argv) > 2 else "/information-library"
NEEDLES = sys.argv[3:] or ["FilterChip", "Clear filters"]
LOG = r"C:/Users/TRIAL/gsp-datacenter/hq-dev.err.log"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return r.read().decode("utf-8", "replace")


def main() -> int:
    try:
        html = get(BASE + PAGE)
    except Exception as e:  # noqa: BLE001
        print("PAGE FETCH FAILED:", repr(e))
        return 1
    chunks = sorted(set(re.findall(r"/_next/static/chunks/[^\"]+\.js", html)))
    print(f"page OK, {len(html)} bytes, {len(chunks)} chunks")

    hits = {n: False for n in NEEDLES}
    for n in NEEDLES:
        if n in html:
            hits[n] = True
    for c in chunks:
        try:
            body = get(BASE + c)
        except Exception as e:  # noqa: BLE001
            print("chunk fetch err:", c, e)
            continue
        for n in NEEDLES:
            if n in body and not hits[n]:
                hits[n] = True
                print("FOUND in", c.split("/")[-1][:40], "->", n)

    ok = True
    for n, found in hits.items():
        print(("OK  " if found else "MISS"), n)
        ok = ok and found

    # optional: tail dev error log for new errors mentioning the page
    try:
        out = subprocess.run(
            ["tail", "-20", LOG], capture_output=True, text=True, timeout=10
        ).stdout
        page_hits = [l for l in out.splitlines() if PAGE.split("/")[-1] in l and ("rror" in l or "ailed" in l)]
        if page_hits:
            print("!!! Recent errors in dev log:")
            print("\n".join(page_hits[-5:]))
    except Exception:  # noqa: BLE001
        pass

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
