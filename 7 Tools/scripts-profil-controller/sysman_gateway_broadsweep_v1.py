#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sapuan LEBAR read-only: SEMUA proses (nama apa pun) yang command line-nya memuat
'gateway' + 'run', plus varian pola lain yang mungkin lolos filter monitor v1
(monitor hanya melihat hermes|python|pythonw.exe). Tujuan: membuktikan tidak ada
buta-titik pada buru hantu. Tidak mengubah apa pun."""
import json
import pathlib
import re
import sys

import psutil

REG = pathlib.Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json")
PROF_RE = re.compile(r"(?:--profile|-p)\s+(\S+)")

d = json.loads(REG.read_text(encoding="utf-8"))
live = set(d["hidup"])
must = set(d["gateway_wajib_hidup"])

hits = []
for p in psutil.process_iter(["pid", "name"]):
    try:
        cmd = " ".join(p.cmdline())
    except Exception:
        continue
    low = cmd.lower()
    if "gateway" not in low:
        continue
    if "monitor" in low or "audit" in low or "grep" in low:
        continue  # alat ukur, bukan gateway
    hits.append((p.info["pid"], p.info.get("name"), cmd))

print(f"proses ber-'gateway' (semua nama, alat ukur dikecualikan): {len(hits)}")
by_prof = {}
for pid, name, cmd in hits:
    if "gateway run" not in cmd.lower() and "gateway" not in cmd.lower():
        continue
    m = PROF_RE.search(cmd)
    prof = m.group(1) if m else ("default" if "hermes" in cmd.lower() else "?")
    by_prof.setdefault(prof, []).append((pid, name, cmd))

print(f"profil terdeteksi: {sorted(by_prof)}")
luar = [p for p in by_prof if p not in live]
print("DI LUAR REGISTRI HIDUP:", luar if luar else "(kosong)")
for prof in sorted(by_prof):
    if prof not in live:
        for pid, name, cmd in by_prof[prof]:
            print(f"  HANTU-KANDIDAT {prof} pid={pid} name={name}\n    {cmd[:300]}")
print("wajib ada:", {m: len(by_prof.get(m, [])) for m in sorted(must)})
print("VERDICT SAPUAN:", "TANPA-BUTA-TITIK" if not luar else "ADA-DI-LUAR-DAFTAR")
