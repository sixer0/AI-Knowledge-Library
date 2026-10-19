#!/usr/bin/env python3
"""Extract per-profile: role_rules 'Muat X' lines + current ALWAYS (accurate) + physical skill count."""
import os, re, json

LOCALAPPDATA = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
PROFILES_DIR = os.path.join(LOCALAPPDATA, "hermes", "profiles")

def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None

def extract_sections(soul):
    al, od = [], []
    idx_al = soul.find("ALWAYS LOAD")
    idx_od = soul.find("ON DEMAND")
    idx_mem = soul.find("Memori & Dokumentasi")
    if idx_al >= 0:
        end = idx_od if idx_od > idx_al else (idx_mem if idx_mem > idx_al else len(soul))
        for line in soul[idx_al:end].splitlines():
            al += re.findall(r"`([a-zA-Z][a-zA-Z0-9_-]+)`", line)
    if idx_od >= 0:
        end = idx_mem if idx_mem > idx_od else len(soul)
        for line in soul[idx_od:end].splitlines():
            od += re.findall(r"`([a-zA-Z][a-zA-Z0-9_-]+)`", line)
    return {"always": al, "ondemand": od}

out = {}
for p in sorted(os.listdir(PROFILES_DIR)):
    if p.startswith("gsp-"):
        soul = read(os.path.join(PROFILES_DIR, p, "SOUL.md"))
        sec = extract_sections(soul)
        # role_rules section: between 'Aturan Khusus Peran' and 'Skill — ALWAYS LOAD'
        idx_role = soul.find("Aturan Khusus Peran")
        idx_sk = soul.find("Skill — ALWAYS LOAD")
        role_seg = soul[idx_role:idx_sk] if idx_role >= 0 and idx_sk > idx_role else ""
        muat_lines = []
        for line in role_seg.splitlines():
            if "Muat" in line or "muat" in line:
                muat_lines.append(line.strip())
        out[p] = {
            "always": sec["always"],
            "ondemand": sec["ondemand"],
            "role_muat": muat_lines,
        }

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_roles.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)

for p, d in out.items():
    print(p, "\n  AL:", d["always"], "\n  MUAT:", d["role_muat"])
