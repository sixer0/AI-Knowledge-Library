#!/usr/bin/env python3
"""Verifikasi provenans + dedup untuk kurasi vault (gsp-librarian)."""
import json, re, sys
from pathlib import Path

VAULT = Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/vault")
LEGACY = Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/legacy-archive")
WIKI = Path(r"C:/Users/TRIAL/AppData/Local/hermes/wiki")

SCOPE = {"adint-vendor-research","gsp-outputs-history","kemhan-bin","china-defence-expo",
         "arsenal-ids-barat-timur","arsenal-tahap-4","ransus-pengamanan-informasi",
         "riset-sistem-ai-gsp","forensic-nfl-2026","labinsen-tni-al","china-expo-toni",
         "catatan_keputusan"}  # catatan_keputusan berisi arsenal-dosir-keputusan (terkait scope arsenal)

def parse_fm(raw):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw, re.S)
    if not m: return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm

objs = []
for f in sorted(VAULT.rglob("*.md")):
    rel = f.relative_to(VAULT).as_posix()
    perkara = rel.split("/")[0]
    if perkara not in SCOPE:
        continue
    raw = f.read_text("utf-8")
    fm = parse_fm(raw)
    objs.append((rel, fm))

print(f"OBJEK SCOPE: {len(objs)}\n")

# --- 1. Provenans: cek keberadaan path sumber ---
print("=== PROVENANS (sumber) ===")
issues = []
for rel, fm in objs:
    src = fm.get("sumber", "")
    oid = fm.get("id", rel)
    if not src:
        issues.append((oid, rel, "TANPA sumber"))
        print(f"[{oid}] TANPA sumber — {rel}")
        continue
    # sumber bisa multi-path dipisah koma/; atau berisi knowledge_map.md/manifest.json (root archive)
    parts = [p.strip() for p in re.split(r"[;,]", src) if p.strip()]
    statuses = []
    for p in parts:
        p2 = p.replace("legacy-archive/", "", 1)
        full = LEGACY / p2
        if full.exists():
            statuses.append(f"OK:{p}")
        elif (LEGACY / p).exists():
            statuses.append(f"OK:{p}")
        else:
            statuses.append(f"MISS:{p}")
            issues.append((oid, rel, f"MISSING: {p}"))
    print(f"[{oid}] {' | '.join(statuses)}")

# --- 2. Dedup id: vs wiki + vs vault ---
print("\n=== DEDUP ===")
wiki_ids = {}
for f in WIKI.rglob("*.md"):
    raw = f.read_text("utf-8")
    fm = parse_fm(raw)
    if fm.get("id"):
        wiki_ids.setdefault(fm["id"], []).append(f.relative_to(WIKI).as_posix())
all_vault_ids = {}
for f in sorted(VAULT.rglob("*.md")):
    fm = parse_fm(f.read_text("utf-8"))
    if fm.get("id"):
        all_vault_ids.setdefault(fm["id"], []).append(f.relative_to(VAULT).as_posix())

seen = set()
for rel, fm in objs:
    oid = fm.get("id", "?")
    if oid in seen:
        print(f"[{oid}] DUPLIKAT id dalam vault scope (file lain juga pakai id ini)")
    seen.add(oid)
    if oid in wiki_ids:
        print(f"[{oid}] ADA DI WIKI: {wiki_ids[oid]} — OBJEK SUDAH DIPROMOSIKAN?")
for oid, locs in all_vault_ids.items():
    if len(locs) > 1 and oid in seen:
        print(f"[{oid}] id sama di vault beberapa lokasi: {locs}")

print("\n=== RINGKASAN ISSUES ===")
print(f"total issues: {len(issues)}")
for oid, rel, msg in issues:
    print(f"- {msg} ({rel})")
