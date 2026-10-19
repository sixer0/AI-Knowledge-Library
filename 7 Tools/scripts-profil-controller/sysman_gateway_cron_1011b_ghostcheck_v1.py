#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sapuan hantu read-only (tambalan self-exclusion).

Pola sama dengan sysman_gateway_broadsweep_v1.py tetapi mengecualikan PID sendiri
dan nama berkas alat ukur, sehingga vonis 'DI LUAR DAFTAR' tidak lagi positif-palsu
oleh barisan proses sapuan itu sendiri (cacat terukur 11-10: broadsweep melaporkan
'?' = dirinya sendiri). Read-only, tidak mengubah apa pun.
"""
import json
import os
import pathlib
import re
import sys

import psutil

REG = pathlib.Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json")
PROF_RE = re.compile(r"(?:--profile|-p)\s+(\S+)")
SELF_PID = os.getpid()
INSTRUMENT_TOKENS = ("broadsweep", "monitor", "audit", "ghostcheck", "probe", "grep", "tree")

d = json.loads(REG.read_text(encoding="utf-8"))
live = set(d["hidup"])
must = set(d["gateway_wajib_hidup"])

hits = []
for p in psutil.process_iter(["pid", "name"]):
    try:
        if p.info["pid"] == SELF_PID:
            continue
        cmd = " ".join(p.cmdline())
    except Exception:
        continue
    low = cmd.lower()
    if "gateway" not in low:
        continue
    if any(tok in low for tok in INSTRUMENT_TOKENS):
        continue
    if "gateway run" not in low:
        continue
    hits.append((p.info["pid"], p.info.get("name"), cmd))

by_prof = {}
for pid, name, cmd in hits:
    m = PROF_RE.search(cmd)
    prof = m.group(1) if m else "default"
    by_prof.setdefault(prof, []).append(pid)

luar = sorted(p for p in by_prof if p not in live)
print(f"proses 'gateway run' (alat ukur + diri sendiri dikecualikan): {len(hits)}")
print(f"profil ber-gateway: {sorted(by_prof)}")
print("WAJIB:", {m: len(by_prof.get(m, [])) for m in sorted(must)})
print("DI LUAR DAFTAR HIDUP:", luar if luar else "(kosong)")
verdict = "SEHAT" if (not luar and all(len(by_prof.get(m, [])) >= 1 for m in must)) else "PERLU-AKSI"
print("VERDICT SAPUAN:", verdict)
sys.exit(0 if verdict == "SEHAT" else 1)
