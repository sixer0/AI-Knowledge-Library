#!/usr/bin/env python
"""Register the GSP-AI custom provider across all gsp-* fleet profiles.

Register-only (per user decision 27-08-2026): adds the provider entry + API key
to every profile WITHOUT touching model defaults or fallback chains. Idempotent —
safe to rerun.

Changes per profile:
  1. config.yaml: append a `custom_providers:` block (legacy list format) if absent.
  2. .env: append HERMES_CUSTOM_10_83_81_246_11400_API_KEY=<key> if absent
     (creating .env when missing).
Verification per profile: re-read both files, parse config.yaml, confirm the
entry exists and the key is present in .env.
"""
import glob, os, re, sys

PROFILES_ROOT = "C:/Users/TRIAL/AppData/Local/hermes/profiles"
GLOBAL_ENV = "C:/Users/TRIAL/AppData/Local/hermes/.env"
KEY_NAME = "HERMES_CUSTOM_10_83_81_246_11400_API_KEY"

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

def read_key():
    for line in open(GLOBAL_ENV, encoding="utf-8"):
        if line.startswith(KEY_NAME + "="):
            return line.split("=", 1)[1].strip()
    raise SystemExit(f"FATAL: {KEY_NAME} not found in {GLOBAL_ENV}")

def append_env(path, key_value):
    created = False
    if os.path.exists(path):
        txt = open(path, encoding="utf-8").read()
        if re.search(r"^" + re.escape(KEY_NAME) + "=", txt, re.M):
            return False, "already-present"
        if txt and not txt.endswith("\n"):
            txt += "\n"
        new = txt + f"{key_value}\n"
    else:
        new = f"{key_value}\n"
        created = True
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    return True, ("created+key" if created else "key-appended")

def append_config(path):
    """Append GSP-AI custom_providers block; returns (changed, note)."""
    if not os.path.exists(path):
        return False, "no-config"
    txt = open(path, encoding="utf-8").read()
    if "GSP-AI" in txt or re.search(r"^custom_providers:\s*$", txt, re.M):
        return False, "already-present"
    if txt and not txt.endswith("\n"):
        txt += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt + "\n" + GSP_AI_BLOCK)
    return True, "block-appended"

def verify(path_cfg, path_env, key):
    """Return list of problems (empty = OK)."""
    problems = []
    # config side
    if os.path.exists(path_cfg):
        try:
            import yaml
            cfg = yaml.safe_load(open(path_cfg, encoding="utf-8")) or {}
        except Exception as e:
            return [f"config parse error: {e}"]
        cp = cfg.get("custom_providers") or []
        entry = next((e for e in cp if isinstance(e, dict) and e.get("name") == "GSP-AI"), None)
        if entry is None:
            problems.append("GSP-AI entry missing in config.yaml")
        else:
            if entry.get("key_env") != KEY_NAME:
                problems.append(f"key_env wrong: {entry.get('key_env')}")
            if entry.get("base_url") != "http://10.83.81.246:11400/v1":
                problems.append(f"base_url wrong: {entry.get('base_url')}")
            if "auto-worker" not in (entry.get("models") or {}):
                problems.append("models list incomplete")
    else:
        problems.append("config.yaml absent")
    # env side
    if os.path.exists(path_env):
        txt = open(path_env, encoding="utf-8").read()
        m = re.search(r"^" + re.escape(KEY_NAME) + r"=(.*)$", txt, re.M)
        if not m:
            problems.append("key missing in .env")
        elif m.group(1).strip() != key:
            problems.append("key value mismatch in .env")
    else:
        problems.append(".env absent")
    return problems

def main():
    key = read_key()
    key_value = f"{KEY_NAME}={key}"
    dirs = sorted(glob.glob(os.path.join(PROFILES_ROOT, "gsp-*")))
    rows = []
    for d in dirs:
        name = os.path.basename(d)
        cfg_p = os.path.join(d, "config.yaml")
        env_p = os.path.join(d, ".env")
        c_changed, c_note = append_config(cfg_p)
        e_changed, e_note = append_env(env_p, key_value)
        problems = verify(cfg_p, env_p, key)
        status = "OK" if not problems else "ISSUE"
        rows.append((name, status, c_note, e_note, "; ".join(problems)))
        print(f"[{status}] {name}: config={c_note} env={e_note}" + (f" | {'; '.join(problems)}" if problems else ""))
    ok = sum(1 for r in rows if r[1] == "OK")
    print(f"\nTOTAL: {len(rows)} profiles, OK: {ok}, ISSUE: {len(rows)-ok}")
    return 0 if ok == len(rows) else 1

if __name__ == "__main__":
    sys.exit(main())
