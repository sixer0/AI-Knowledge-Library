#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit independen gateway fleet (sysman). Tidak mengubah apa pun - hanya ukur.
Bandingkan hasil vs gsp_gateway_monitor_v1.py: dua pengamat, satu kebenaran."""
import json, os, re, sys, pathlib
try:
    import psutil
except ImportError:
    print("PSUTIL MISSING"); sys.exit(2)

REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')
d = json.loads(REG.read_text(encoding='utf-8'))
live = set(d['hidup']); must = set(d['gateway_wajib_hidup'])

prof_pat = re.compile(r'--profile\s+(\S+)|\s-p\s+(\S+)')
found = {}
for p in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        name = (p.info['name'] or '').lower()
        cl = p.info['cmdline'] or []
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
    if name not in ('hermes.exe', 'python.exe', 'pythonw.exe'):
        continue
    joined = ' '.join(cl)
    if 'gateway' not in joined.lower() or 'run' not in [c.lower() for c in cl]:
        continue
    if not any(c.lower() == 'gateway' for c in cl):
        continue
    m = prof_pat.search(joined)
    prof = (m.group(1) or m.group(2)) if m else 'default'
    found.setdefault(prof, []).append(p.info['pid'])

print("REGISTRI hidup=%d wajib=%d" % (len(live), len(must)))
print("GATEWAY TERDETEKSI:")
for prof in sorted(found):
    tag = 'OK' if prof in live else 'HANTU'
    print("  %-24s pids=%s [%s]" % (prof, found[prof], tag))
missing = sorted(must - set(found))
print("WAJIB MATI:", missing if missing else "(tidak ada)")
ghosts = sorted(set(found) - live)
print("HANTU:", ghosts if ghosts else "(tidak ada)")
stray = sorted((set(found) & live) - must)
print("LAIN-HIDUP-BER-GATEWAY (tidak ditagih):", stray if stray else "(tidak ada)")
