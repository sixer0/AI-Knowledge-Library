#!/usr/bin/env python
"""Deterministic fleet credential + provider audit (Hermes on Windows).

Scans every profile under HERMES_HOME/profiles:
  - model.provider / model.default (regex on raw yaml, no PyYAML needed)
  - GSP-AI custom_providers registration (+ stale model entries)
  - fallback_providers presence
  - custom-provider API key fingerprint vs the global .env key (never prints keys)
Optionally probes the gateway to enumerate the key's REAL authorized models
(sends a bogus model name; the 403 message carries the authoritative list).

Usage:
  uv run --python 3.11 python audit_provider_credentials.py [HERMES_HOME] [--probe] [--out FILE.json]

Default HERMES_HOME: C:/Users/TRIAL/AppData/Local/hermes
Exit 0 always; judge by the printed summary.
"""
import hashlib, json, os, re, sys, urllib.request

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
KEY_ENV = "HERMES_CUSTOM_10_83_81_246_11400_API_KEY"
STALE_RX = re.compile(r"auto-worker:|auto-auxilary:")
args = [a for a in sys.argv[1:]]
probe = "--probe" in args
args = [a for a in args if not a.startswith("--")]
if "--out" in args:
    i = args.index("--out"); out = args[i+1]; args = args[:i] + args[i+2:]
else:
    out = None
if args:
    HOME = args[0]

fp = lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]

gkey = ""
env_path = os.path.join(HOME, ".env")
if os.path.exists(env_path):
    for line in open(env_path, encoding="utf-8", errors="replace"):
        if line.startswith(KEY_ENV + "="):
            gkey = line.split("=", 1)[1].strip(); break
gfp = fp(gkey) if gkey else None

allowed_models = None
base_url = None
if probe and gkey:
    # read base_url from the first profile config that has one
    prof_dir = os.path.join(HOME, "profiles")
    for n in sorted(os.listdir(prof_dir)):
        cfg = os.path.join(prof_dir, n, "config.yaml")
        if os.path.exists(cfg):
            m = re.search(r"base_url:\s*(\S+)", open(cfg, encoding="utf-8", errors="replace").read())
            if m and m.group(1).startswith("http"):
                base_url = m.group(1); break
    if base_url:
        req = urllib.request.Request(
            base_url.rstrip("/") + "/chat/completions",
            data=json.dumps({"model": "__bogus_probe__",
                             "messages": [{"role": "user", "content": "x"}]}).encode(),
            headers={"Authorization": "Bearer " + gkey, "Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=20)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            m = re.search(r"can only access models=\[([^\]]+)\]", body)
            if m:
                allowed_models = [x.strip().strip("'\"") for x in m.group(1).split(",")]
        except Exception as e:
            allowed_models = ["PROBE_FAILED:" + type(e).__name__]

rows = []
prof_dir = os.path.join(HOME, "profiles")
for n in sorted(os.listdir(prof_dir)) if os.path.isdir(prof_dir) else []:
    pdir = os.path.join(prof_dir, n)
    if not os.path.isdir(pdir):
        continue
    row = {"profile": n}
    cfg = os.path.join(pdir, "config.yaml")
    if not os.path.exists(cfg):
        row["no_config"] = True; rows.append(row); continue
    txt = open(cfg, encoding="utf-8", errors="replace").read()
    m = re.search(r"^model:\s*\n((?:[ \t]+.*\n)+)", txt, re.M)
    if m:
        blk = m.group(1)
        mp = re.search(r"^\s+provider:\s*(\S+)", blk, re.M)
        md = re.search(r"^\s+default:\s*(\S+)", blk, re.M)
        row["model_provider"] = (mp.group(1) if mp else "").strip("\"'")
        row["model_default"] = (md.group(1) if md else "").strip("\"'")
    row["provider_registered"] = "GSP-AI" in txt
    row["has_fallback_providers"] = bool(re.search(r"^fallback_providers:", txt, re.M))
    row["stale_model_entries"] = bool(STALE_RX.search(txt))
    kfp = "no_env"
    envf = os.path.join(pdir, ".env")
    if os.path.exists(envf):
        kv = cnt = 0 and None
        cnt = 0; kv = None
        for line in open(envf, encoding="utf-8", errors="replace"):
            if line.startswith(KEY_ENV + "="):
                cnt += 1; kv = line.split("=", 1)[1].strip()
        if kv:
            kfp = ("same" if fp(kv) == gfp else "DIFF") + f"(x{cnt})"
        else:
            kfp = "missing"
    row["key_match_global"] = kfp
    rows.append(row)

summary = {
    "hermes_home": HOME, "key_env": KEY_ENV,
    "global_key_present": bool(gkey),
    "total_profiles": len(rows),
    "registered": sum(1 for r in rows if r.get("provider_registered")),
    "key_same": sum(1 for r in rows if str(r.get("key_match_global", "")).startswith("same")),
    "key_problems": [r["profile"] for r in rows
                     if not str(r.get("key_match_global", "")).startswith("same")],
    "with_fallback": sum(1 for r in rows if r.get("has_fallback_providers")),
    "stale_model_entries": sum(1 for r in rows if r.get("stale_model_entries")),
    "gateway_allowed_models": allowed_models,
    "model_default_dist": {},
}
for r in rows:
    k = r.get("model_default") or "?"
    summary["model_default_dist"][k] = summary["model_default_dist"].get(k, 0) + 1

res = {"summary": summary, "profiles": rows}
text = json.dumps(res, indent=1)
if out:
    open(out, "w", encoding="utf-8").write(text)
print(text[:4000])
