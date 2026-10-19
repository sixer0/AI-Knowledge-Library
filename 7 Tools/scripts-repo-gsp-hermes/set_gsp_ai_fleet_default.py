#!/usr/bin/env python
"""Set GSP-AI (auto-efficient) as DEFAULT model + kilocode kilo-auto/free as
fallback #1 across ALL Hermes profiles — SEQUENTIAL ONLY.

WHY SEQUENTIAL: a concurrent batch (3 workers x many `hermes config set`) was
found to corrupt config.yaml — the dotted keys were written as TOP-LEVEL keys
(e.g. `model.default` became top-level `default:`) leaving the `model:` block
untouched. Single / sequential `hermes config set` calls write correctly.
This script therefore runs strictly one hermes process at a time.

Per profile (in order):
  1. ensure GSP-AI custom provider + API key are registered (idempotent)
  2. `hermes config unset` the four top-level junk keys the corrupted batch
     left behind (default, provider, base_url, api_key) — no-op if absent
  3. `hermes config set`:
       model.default        = auto-efficient
       model.provider       = GSP-AI
       model.base_url       = http://10.83.81.246:11400/v1
       model.api_key        = ${HERMES_CUSTOM_10_83_81_246_11400_API_KEY}
       fallback_providers   = [{"provider":"kilocode","model":"kilo-auto/free"}]
  4. verify by parsing config.yaml: model block matches target, no top-level
     junk keys remain, fallback_providers present.
"""
import json, os, re, subprocess, sys, time

PROFILES_ROOT = "C:/Users/TRIAL/AppData/Local/hermes/profiles"
GLOBAL_ENV = "C:/Users/TRIAL/AppData/Local/hermes/.env"
HERMES_BIN = "C:/Users/TRIAL/AppData/Local/hermes/hermes-agent/venv/Scripts/hermes.exe"
KEY_NAME = "HERMES_CUSTOM_10_83_81_246_11400_API_KEY"

TARGET_MODEL = {
    "default": "auto-efficient",
    "provider": "GSP-AI",
    "base_url": "http://10.83.81.246:11400/v1",
    "api_key": "${HERMES_CUSTOM_10_83_81_246_11400_API_KEY}",
}
TARGET_FALLBACK = [{"provider": "kilocode", "model": "kilo-auto/free"}]
TOPLEVEL_JUNK = ["default", "provider", "base_url", "api_key"]

GSP_AI_BLOCK = """custom_providers:
  - name: GSP-AI
    base_url: http://10.83.81.246:11400/v1
    key_env: HERMES_CUSTOM_10_83_81_246_11400_API_KEY
    model: auto-efficient
    models:
      auto-worker: {}
      auto-auxilary: {}
      auto-efficient: {}
      thinker: {}
    models_discovered: true
"""

import yaml

def read_key():
    for line in open(GLOBAL_ENV, encoding="utf-8"):
        if line.startswith(KEY_NAME + "="):
            return line.split("=", 1)[1].strip()
    raise SystemExit(f"FATAL: {KEY_NAME} not found in {GLOBAL_ENV}")

def load(name):
    p = os.path.join(PROFILES_ROOT, name, "config.yaml")
    try:
        return yaml.safe_load(open(p, encoding="utf-8")) or {}
    except Exception as e:
        return {"__error__": str(e)}

def gsp_registered(cfg):
    return any(isinstance(e, dict) and e.get("name") == "GSP-AI" for e in (cfg.get("custom_providers") or []))

def register_gsp(name, key):
    cfg_p = os.path.join(PROFILES_ROOT, name, "config.yaml")
    env_p = os.path.join(PROFILES_ROOT, name, ".env")
    cc = ec = False
    if os.path.exists(cfg_p):
        txt = open(cfg_p, encoding="utf-8").read()
        if not gsp_registered(load(name)):
            # Append the GSP-AI block. NOTE: do NOT shortcut on a bare
            # `custom_providers:` line — a profile may have a custom_providers
            # list holding OTHER providers (e.g. user01 had GSP-Server) with no
            # GSP-AI entry; that must be handled by a caller, not skipped here.
            if not re.search(r"^custom_providers:", txt, re.M):
                if txt and not txt.endswith("\n"):
                    txt += "\n"
                with open(cfg_p, "w", encoding="utf-8", newline="\n") as f:
                    f.write(txt + "\n" + GSP_AI_BLOCK)
                cc = True
            else:
                # A custom_providers list already exists but lacks GSP-AI —
                # merge via `hermes config set custom_providers '<json>'`.
                import subprocess, json as _json
                cfg = load(name)
                merged = list(cfg.get("custom_providers") or [])
                merged.append({"name": "GSP-AI",
                               "base_url": "http://10.83.81.246:11400/v1",
                               "key_env": KEY_NAME,
                               "model": "auto-efficient",
                               "models": {"auto-worker": {}, "auto-auxilary": {},
                                          "auto-efficient": {}, "thinker": {}},
                               "models_discovered": True})
                r = subprocess.run([HERMES_BIN, "-p", name, "config", "set",
                                    "custom_providers", _json.dumps(merged)],
                                   capture_output=True, text=True, timeout=120)
                cc = r.returncode == 0
    if os.path.exists(env_p):
        txt = open(env_p, encoding="utf-8").read()
        if not re.search(r"^" + re.escape(KEY_NAME) + r"=", txt, re.M):
            if txt and not txt.endswith("\n"):
                txt += "\n"
            with open(env_p, "w", encoding="utf-8", newline="\n") as f:
                f.write(txt + f"{KEY_NAME}={key}\n")
            ec = True
    else:
        with open(env_p, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"{KEY_NAME}={key}\n")
        ec = True
    return cc, ec

def hermes(name, *args):
    r = subprocess.run([HERMES_BIN, "-p", name] + list(args),
                       capture_output=True, text=True, timeout=120)
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode, out.splitlines()[0] if out else ""

def convert(name):
    key = GLOBAL_KEY
    res = {"name": name, "steps": [], "problems": [], "ok": False, "state": None}
    try:
        cc, ec = register_gsp(name, key)
        res["reg"] = {"cfg": cc, "env": ec}
        # 1) remove top-level junk keys
        for k in TOPLEVEL_JUNK:
            rc, msg = hermes(name, "config", "unset", k)
            res["steps"].append(("unset:" + k, rc == 0))
        # 2) set the target model block + fallback
        for k, v in TARGET_MODEL.items():
            rc, msg = hermes(name, "config", "set", "model." + k, v)
            res["steps"].append(("set:model." + k, rc == 0))
            if rc != 0:
                res["problems"].append(f"set model.{k} failed: {msg}")
        rc, msg = hermes(name, "config", "set", "fallback_providers", json.dumps(TARGET_FALLBACK))
        res["steps"].append(("set:fallback_providers", rc == 0))
        if rc != 0:
            res["problems"].append(f"set fallback_providers failed: {msg}")
        # 3) verify
        cfg = load(name)
        if "__error__" in cfg:
            res["problems"].append(f"YAML parse error: {cfg['__error__']}")
        else:
            m = cfg.get("model") or {}
            ok = True
            for k, v in TARGET_MODEL.items():
                if m.get(k) != v:
                    res["problems"].append(f"model.{k}={m.get(k)!r} != {v!r}")
                    ok = False
            if (cfg.get("fallback_providers") or []) != TARGET_FALLBACK:
                res["problems"].append(f"fallback_providers={cfg.get('fallback_providers')!r}")
                ok = False
            for k in TOPLEVEL_JUNK:
                if k in cfg:
                    res["problems"].append(f"top-level junk '{k}' still present")
                    ok = False
            if not gsp_registered(cfg):
                res["problems"].append("GSP-AI custom provider missing")
            res["state"] = {"default": m.get("default"), "provider": m.get("provider"),
                            "fallback": cfg.get("fallback_providers")}
            res["ok"] = ok and not res["problems"]
        res["ok"] = res["ok"] and not res["problems"]
    except Exception as e:
        res["problems"].append(f"exception: {e}")
    return res

def main():
    global GLOBAL_KEY
    GLOBAL_KEY = read_key()
    names = sorted(os.path.basename(d) for d in os.listdir(PROFILES_ROOT)
                   if os.path.isdir(os.path.join(PROFILES_ROOT, d)))
    print(f"Converting {len(names)} profiles SEQUENTIALLY (no concurrency)...", flush=True)
    results = []
    t0 = time.time()
    for name in names:                      # strictly sequential
        r = convert(name)
        results.append(r)
        tag = "OK " if r["ok"] else "ISSUE"
        detail = "; ".join(r["problems"]) if r["problems"] else f"default={r['state']['default']} provider={r['state']['provider']} fb={r['state']['fallback']}"
        print(f"[{tag}] {name:35} {detail}", flush=True)
    ok = sum(1 for r in results if r["ok"])
    print(f"\n=== SUMMARY: {ok}/{len(results)} profiles in target state ({time.time()-t0:.0f}s) ===")
    bad = [r for r in results if not r["ok"]]
    if bad:
        print("ISSUES:")
        for r in bad:
            print(f"  {r['name']}: {'; '.join(r['problems'])}")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsp_ai_default_report.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, default=str)
    print("Report -> gsp_ai_default_report.json")
    return 0 if ok == len(results) else 1

if __name__ == "__main__":
    sys.exit(main())
