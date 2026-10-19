#!/usr/bin/env python3
"""Promote orphan skills (physical in profiles, absent from fleet registry) into fleet registry.
Copies the most complete SKILL.md folder found across profiles. Flat structure <name>/SKILL.md."""
import os, json, shutil

LOCALAPPDATA = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
PROFILES_DIR = os.path.join(LOCALAPPDATA, "hermes", "profiles")
FLEET_REG = os.path.join(LOCALAPPDATA, "hermes", "skills", "gsp")
ACC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_inventory_acc.json")

with open(ACC, encoding="utf-8") as f:
    acc = json.load(f)

orphan_by_profile = acc["orphan_by_profile"]

# Build unique orphan names + candidate sources (profile paths holding SKILL.md)
unique_orphans = {}
for p, lst in orphan_by_profile.items():
    for name in lst:
        if name not in unique_orphans:
            unique_orphans[name] = []
        unique_orphans[name].append(p)

def find_skill_folder(profile, name):
    """Find physical skill folder for name in a profile (nested or flat)."""
    sk = os.path.join(PROFILES_DIR, profile, "skills")
    candidates = [
        os.path.join(sk, name, name),
        os.path.join(sk, name),
    ]
    for c in candidates:
        if os.path.isdir(c) and os.path.isfile(os.path.join(c, "SKILL.md")):
            return c
    return None

def best_source(name):
    """Pick profile with the largest SKILL.md content for this orphan."""
    best = None
    best_len = 0
    for p in unique_orphans[name]:
        folder = find_skill_folder(p, name)
        if folder:
            sm = os.path.join(folder, "SKILL.md")
            try:
                len = os.path.getsize(sm)
            except Exception:
                len = 0
            if len > best_len:
                best = (p, folder)
                best_len = len
    return best

promoted = []
skipped_exists = []
missing = []

for name in sorted(unique_orphans.keys()):
    target = os.path.join(FLEET_REG, name)
    if os.path.isfile(os.path.join(target, "SKILL.md")):
        skipped_exists.append(name)
        continue
    src = best_source(name)
    if src is None:
        missing.append(name)
        continue
    src_profile, src_folder = src
    # copy whole folder flat
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.copytree(src_folder, target)
    promoted.append((name, src_profile))

print("=== PROMOTED to fleet registry ===")
for name, prof in promoted:
    print(name, "(from", prof)
print("Total promoted:", len(promoted))
print("\n=== Already existed in fleet (skip) ===")
print(len(skipped_exists), "->", skipped_exists[:10])
print("\n=== Missing (no physical source found) ===")
print(missing)

# Save report
report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_promoted.json")
with open(report_path, "w", encoding="utf-8") as f:
    json.dump({"promoted": [n for n, _ in promoted], "exists": skipped_exists, "missing": missing}, f, indent=1)
print("Report:", report_path)
