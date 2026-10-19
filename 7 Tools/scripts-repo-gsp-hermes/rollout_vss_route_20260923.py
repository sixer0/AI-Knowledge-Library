#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout baris rute korpus VSS ke MEMORY.md semua profil (VSSKB-0923, D-02).
Idempoten. Arsip verbatim pra-sunting ke memory/refs/<profil>/ sebelum sunting.
Cakupan: 53 profil di profiles/ + profil default (memori di root hermes home).
Pakai: python rollout_vss_route_20260923.py [--apply]   (tanpa --apply = dry-run)
"""
import sys, datetime, hashlib
from pathlib import Path

APPLY = "--apply" in sys.argv
PROFILES = Path(r"C:/Users/TRIAL/AppData/Local/hermes/profiles")
DEFAULT_MEM = Path(r"C:/Users/TRIAL/AppData/Local/hermes/memories/MEMORY.md")
REFS = Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/memory/refs")
MARK = "INDEX #vss-korpus"
ROW = ("INDEX #vss-korpus: topik cctv/kamera/surveilans/VMS/NVR/ONVIF/lensa/bitrate -> "
       "muat skill pustaka-teknis (+cctv-system-designer); baca "
       "ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/ shared ws + IL objek VSSKB-0923.")
assert len(ROW) <= 230, f"baris rute terlalu panjang: {len(ROW)}"

ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
stats = {"added": [], "skip_existing": [], "no_memory": [], "fail": []}


def inject(mem: Path, tag: str, refs_sub: str):
    """Tambahkan baris rute ke satu berkas memori dengan arsip verbatim dulu."""
    text = mem.read_text(encoding="utf-8", errors="replace")
    if MARK in text:
        stats["skip_existing"].append(tag)
        return
    if not APPLY:
        stats["added"].append(tag)
        return
    dest = REFS / refs_sub
    dest.mkdir(parents=True, exist_ok=True)
    arc = dest / "2026_09_23_arsip_memory_sebelum_rute_vss.md"
    if not arc.exists():
        arc.write_text(
            f"# Arsip verbatim MEMORY.md {tag} pra-rute VSS (VSSKB-0923)\n"
            f"# waktu: {ts} | sha256: {hashlib.sha256(text.encode('utf-8')).hexdigest()}\n\n"
            + text, encoding="utf-8")
    mem.write_text(text.rstrip("\n") + "\n\u00a7\n" + ROW + "\n", encoding="utf-8")
    if MARK in mem.read_text(encoding="utf-8", errors="replace"):
        stats["added"].append(tag)
    else:
        stats["fail"].append(tag)


for p in sorted(PROFILES.iterdir()):
    if not p.is_dir():
        continue
    mem = p / "memories" / "MEMORY.md"
    if not mem.exists():
        stats["no_memory"].append(p.name)
        continue
    inject(mem, p.name, p.name)

if DEFAULT_MEM.exists():
    inject(DEFAULT_MEM, "default(root)", "default-profile")

mode = "APPLY" if APPLY else "DRY-RUN"
print(f"[{mode}] target={len(stats['added'])} sudah_ada={len(stats['skip_existing'])} "
      f"tanpa_memory={len(stats['no_memory'])} gagal={len(stats['fail'])}")
print("tanpa_memory:", ", ".join(stats["no_memory"]) or "-")
print("gagal:", ", ".join(stats["fail"]) or "-")
if APPLY:
    rep = Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-23-vss-knowledge-register/rollout-mem-report.md")
    rep.write_text(f"# Laporan rollout rute VSS | {ts} | ROW_LEN={len(ROW)}\n"
                   f"- ditambah: {len(stats['added'])}\n- sudah_ada: {len(stats['skip_existing'])}\n"
                   f"- tanpa_memory: {stats['no_memory']}\n- gagal: {stats['fail'] or '[]'}\n"
                   f"- baris: `{ROW}`\n", encoding="utf-8")
    print("report:", rep)
