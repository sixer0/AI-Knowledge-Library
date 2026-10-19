#!/usr/bin/env python3
"""Accurate inventory: per-profile ALWAYS LOAD / ON DEMAND (all names per line),
phantom classification, redundant vs orphan physical skills."""
import os, re, json

LOCALAPPDATA = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
PROFILES_DIR = os.path.join(LOCALAPPDATA, "hermes", "profiles")
FLEET_REG = os.path.join(LOCALAPPDATA, "hermes", "skills", "gsp")
GLOBAL_SKILLS = os.path.join(LOCALAPPDATA, "hermes", "skills")
KANONIK = os.path.join(os.path.expanduser("~"), "workspace", "gsp-hermes", "skills")

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

def list_registry_names(root):
    names = {}
    if not os.path.isdir(root):
        return names
    for entry in os.listdir(root):
        full = os.path.join(root, entry)
        if os.path.isdir(full):
            for c in [os.path.join(full, entry, "SKILL.md"), os.path.join(full, "SKILL.md")]:
                if os.path.isfile(c):
                    names[entry] = c
                    break
    return names

# Global registry: all categories under $LOCALAPPDATA/hermes/skills/<cat>/<name>
global_all = {}
if os.path.isdir(GLOBAL_SKILLS):
    for cat in os.listdir(GLOBAL_SKILLS):
        cf = os.path.join(GLOBAL_SKILLS, cat)
        if os.path.isdir(cf):
            for nm, path in list_registry_names(cf).items():
                global_all[nm] = path

fleet = list_registry_names(FLEET_REG)
kanonik = list_registry_names(KANONIK)

profiles = []
for p in sorted(os.listdir(PROFILES_DIR)):
    if p.startswith("gsp-"):
        soul_path = os.path.join(PROFILES_DIR, p, "SOUL.md")
        soul = read(soul_path)
        phys = list_registry_names(os.path.join(PROFILES_DIR, p, "skills"))
        profiles.append({
            "profile": p,
            "always": extract_sections(soul)["always"] if soul else [],
            "ondemand": extract_sections(soul)["ondemand"] if soul else [],
            "physical": list(phys.keys()),
        })

# Classification helpers
def in_reg(name):
    return name in fleet or name in kanonik or name in global_all

# Phantom referenced in SOUL but absent from all registries
phantom_refs = {}
for prof in profiles:
    ph = [sk for sk in prof["always"] + prof["ondemand"] if not in_reg(sk)]
    if ph:
        phantom_refs[prof["profile"]] = ph

# Phantom-but-physical: referenced in SOUL, absent from registries, but physically present in >=1 profile
phantom_physical = {}
for prof in profiles:
    ph = [sk for sk in prof["always"] + prof["ondemand"]
          if not in_reg(sk) and sk in prof["physical"]
          and sk not in phantom_physical]
    if ph:
        phantom_physical[prof["profile"]] = ph

# Orphan physical skills: physically in profile, absent from all registries
orphan_by_profile = {}
for prof in profiles:
    orph = [sk for sk in prof["physical"] if not in_reg(sk)]
    if orph:
        orphan_by_profile[prof["profile"]] = orph

# Redundant physical: physically in profile AND present in fleet/global registry
redundant_by_profile = {}
for prof in profiles:
    red = [sk for sk in prof["physical"] if in_reg(sk)]
    if red:
        redundant_by_profile[prof["profile"]] = red

report = {
    "profile_count": len(profiles),
    "phantom_refs": phantom_refs,
    "phantom_physical": phantom_physical,
    "orphan_by_profile": orphan_by_profile,
    "redundant_by_profile": redundant_by_profile,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_inventory_acc.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=1)

print("Profiles:", len(profiles))
print("\n=== PHANTOM referenced in SOUL but absent from ALL registries (unique names) ===")
uniq = {}
for p, lst in phantom_refs.items():
    for s in lst:
        uniq[s] = uniq.get(s, 0) + 1
for s, n in sorted(uniq.items(), key=lambda x: -x[1]):
    print(f"{s}  ({n} profil)")
print("\n=== PHANTOM-BUT-PHYSICAL (referenced in SOUL, physically present, absent from registry) ===")
uniq2 = {}
for p, lst in phantom_physical.items():
    for s in lst:
        uniq2[s] = uniq2.get(s, 0) + 1
for s, n in sorted(uniq2.items(), key=lambda x: -x[1]):
    print(f"{s}  ({n} profil)")
print("\n=== ORPHAN physical skills (absent from all registries) — unique names & count ===")
orphan_uniq = {}
for p, lst in orphan_by_profile.items():
    for s in lst:
        orphan_uniq[s] = orphan_uniq.get(s, 0) + 1
for s, n in sorted(orphan_uniq.items(), key=lambda x: -x[1]):
    print(f"{s}  ({n} profil)")
print("\n=== REDUNDANT physical skills (present in fleet/global) — total copies ===")
red_total = sum(len(lst) for lst in redundant_by_profile.values())
print("Total redundant copies:", red_total)
