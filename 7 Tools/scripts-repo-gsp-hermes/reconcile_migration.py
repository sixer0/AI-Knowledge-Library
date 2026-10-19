#!/usr/bin/env python3
"""
reconcile_migration.py — rekonsiliasi migrasi legacy-archive → Information Library.

Membandingkan: manifest sumber (semua file) vs objek vault vs entri wiki (IL).
Output: laporan per proyek — file terpreservasi (workspace scope), objek vault,
entri wiki, dan GAP (file penting tanpa representasi kurasi).

Usage: python reconcile_migration.py
"""
import json
from pathlib import Path

ROOT = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace/legacy-archive")
VAULT = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace/vault")
WIKI = Path("C:/Users/TRIAL/AppData/Local/hermes/wiki")

def main():
    files = json.loads((ROOT / "manifest.json").read_text("utf-8"))
    # grup per proyek top-level
    proj = {}
    for f in files:
        top = f["rel"].split("/", 1)[0]
        proj.setdefault(top, []).append(f)

    # objek vault (selain ekas yang sudah ada)
    vault_objs = []
    for p in sorted(VAULT.rglob("*.md")):
        rel = p.relative_to(VAULT).as_posix()
        if rel.startswith("ekas/"):
            continue
        vault_objs.append(rel)

    # entri wiki yang terkait legacy (tidak termasuk ekas)
    wiki_legacy = []
    for p in sorted(WIKI.rglob("*.md")):
        rel = p.relative_to(WIKI).as_posix()
        if rel.startswith("ekas"):
            continue
        wiki_legacy.append(rel)

    print(f"TOTAL FILE SUMBER: {len(files)}")
    print(f"OBJEK VAULT (non-ekas): {len(vault_objs)}")
    print(f"ENTRI WIKI (non-ekas): {len(wiki_legacy)}")
    print("\n=== PER PROYEK ===")
    total_penting = 0
    for top in sorted(proj, key=lambda t: -len(proj[t])):
        fl = proj[top]
        penting = [f for f in fl if f["kelas"] == "penting"]
        total_penting += len(penting)
        v = [o for o in vault_objs if o.split("/")[0] in VSLUG.get(top, [top])]
        w = [o for o in wiki_legacy if any(s in o for s in VSLUG.get(top, [top]))]
        print(f"\n[{top}] {len(fl)} file ({len(penting)} penting)")
        print(f"  vault objek: {len(v)}")
        for o in v: print(f"    - {o}")
        print(f"  wiki entry: {len(w)}")
        for o in w: print(f"    - {o}")
    print(f"\nTOTAL FILE PENTING: {total_penting}")

VSLUG = {
    "ADINT-20260824T085309Z-1-001": ["adint-vendor-research"],
    "outputs-20260824T085259Z-1-001": ["gsp-outputs-history"],
    "KEMHAN -20260824T085136Z-1-001": ["kemhan-bin"],
    "china-defence-expo-crawler-20260824T085128Z-1-001": ["china-defence-expo"],
    "ARSENAL-IDS-BARAT-TIMUR-20260824T085012Z-1-001": ["arsenal-ids-barat-timur"],
    "Arsenal Tahap 4-20260824T085411Z-1-001": ["arsenal-tahap-4"],
    "RANSUS-20260824T085403Z-1-001": ["ransus-pengamanan-informasi"],
    "Research Agentic Operating System-20260824T084946Z-1-001": ["riset-sistem-ai-gsp"],
    "RISET SISTEM OPERASI AI GSP DAN KAM-20260824T085358Z-1-001": ["riset-sistem-ai-gsp"],
    "FORENSIC-20260824T085317Z-1-001": ["forensic-nfl-2026"],
    "Labinsen TNI AL-20260824T085454Z-1-001": ["labinsen-tni-al"],
    "China Expo - Toni Research-20260824T085430Z-1-001": ["china-expo-toni"],
}

if __name__ == "__main__":
    main()
