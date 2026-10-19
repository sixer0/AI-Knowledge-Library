"""Verifikasi deterministik OPENAI-IMG-3: sapuan config/env + fungsional provider per profil."""
import os, re, sys, hashlib, subprocess, json

PROF_ROOT = os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes\profiles")
BASE = os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes")
REPO = os.path.join(BASE, "hermes-agent")
FP = "1ab84207"
TARGETS = ["gsp-image-specialist", "gsp-image-prompt-specialist", "gsp-design-system-specialist",
           "gsp-document-writer", "gsp-pm-writer", "gspuser01", "gsp-master", "gsp-master01", "<BASE>"]

def home(p):
    return BASE if p == "<BASE>" else os.path.join(PROF_ROOT, p)

fails = []
def check(n, name, ok, detail=""):
    print(f"CHECK {n}: {'PASS' if ok else 'FAIL'} - {name} | {detail}")
    if not ok:
        fails.append(name)

# C1: env tepat 1 baris + fingerprint cocok
for i, p in enumerate(TARGETS, 1):
    lines = [l.strip() for l in open(os.path.join(home(p), ".env"), encoding="utf-8") if l.strip().startswith("OPENAI_API_KEY=")]
    ok = len(lines) == 1 and hashlib.sha256(lines[0].split("=", 1)[1].encode()).hexdigest().startswith(FP)
    check(i, f"env {p}", ok, f"n={len(lines)}")

# C2: config image_gen benar + model block utuh (anti korusi dotted key)
for i, p in enumerate(TARGETS, 7):
    txt = open(os.path.join(home(p), "config.yaml"), encoding="utf-8").read()
    ig = re.search(r"^image_gen:\n((?:[ \t]+.*\n?)+)", txt, re.M)
    body = ig.group(1) if ig else ""
    ok = "provider: openai" in body and "gpt-image-2-medium" in body
    model_ok = bool(re.search(r"^model:\n(?:[ \t]+.*\n?)+", txt, re.M))
    junk = bool(re.search(r"^provider:\s*openai\s*$", txt, re.M)) or bool(re.search(r"^base_url:\s*http", txt, re.M))
    check(i, f"cfg {p}", ok and model_ok and not junk, f"ig={ok},model_block={model_ok},junk={junk}")

# C3: toolset image_gen aktif di profil target baru
for i, p in enumerate(["gsp-image-prompt-specialist", "gsp-design-system-specialist", "gsp-document-writer", "gsp-pm-writer"], 16):
    txt = open(os.path.join(home(p), "config.yaml"), encoding="utf-8").read()
    m = re.search(r"^platform_toolsets:\n((?:[ \t]+.*\n?)+)", txt, re.M)
    seg = m.group(1) if m else ""
    check(i, f"toolset {p}", bool(re.search(r"-\s+image_gen\b", seg)))

# C4: fungsional - registry resolve ke openai + is_available, per profil (HERMES_HOME)
probe_code = r'''
import os, sys, json
sys.path.insert(0, os.environ["REPO"])
os.environ.setdefault("HERMES_HOME", os.environ["HH"])
from dotenv import load_dotenv
load_dotenv(os.path.join(os.environ["HH"], ".env"), override=True)
import hermes_cli.plugins as hp
try:
    hp.discover_plugins()
except Exception as e:
    pass
from agent.image_gen_registry import get_active_provider
p = get_active_provider()
out = {"provider": p.name if p else None, "available": bool(p and p.is_available())}
try:
    import importlib
    mod = importlib.import_module("plugins.image_gen.openai")
    out["model"] = mod._resolve_model()[0]
except Exception as e:
    out["model_err"] = str(e)[:80]
print(json.dumps(out))
'''
for i, p in enumerate(TARGETS, 20):
    env = dict(os.environ, HH=home(p), REPO=REPO, PYTHONPATH=REPO)
    r = subprocess.run([os.path.join(REPO, "venv", "Scripts", "python.exe"), "-c", probe_code],
                       capture_output=True, text=True, env=env, timeout=120)
    try:
        out = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        out = {"raw": (r.stdout + r.stderr)[-150:]}
    ok = out.get("provider") == "openai" and out.get("available") is True and out.get("model") == "gpt-image-2-medium"
    check(i, f"fungsional {p}", ok, json.dumps(out)[:140])

print(f"\nTOTAL: {len(TARGETS)*3+4} checks | FAIL: {len(fails)}")
print("VERDICT:", "PASS" if not fails else "FAIL " + "; ".join(fails))
