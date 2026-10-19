#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 11-10 ronde-b: triangulasi independen CIM -> profil gateway,
plus cek eksistensi folder profil vs registri (read-only, tidak mutasi)."""
import json, re, subprocess, os, pathlib

REG = pathlib.Path('C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')
HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'

q = """
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(hermes|python|pythonw)\\.exe$' -and $_.CommandLine -match 'gateway run' } | ForEach-Object { "{0}|{1}" -f $_.ProcessId, ($_.CommandLine -replace '\\s+',' ') }
"""
r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', q],
                   capture_output=True, text=True, timeout=120)
rows = {}
for line in r.stdout.splitlines():
    if '|' not in line:
        continue
    pid, cmd = line.split('|', 1)
    m = re.search(r'--profile\s+(\S+)', cmd) or re.search(r'-p\s+(\S+)', cmd)
    prof = m.group(1) if m else 'default'
    rows.setdefault(prof, []).append(int(pid))

d = json.loads(REG.read_text(encoding='utf-8'))
live, must = set(d['hidup']), set(d['gateway_wajib_hidup'])
print('registri hidup:', len(live), '| wajib:', sorted(must))
for p in sorted(set(list(rows) + list(must))):
    n = len(rows.get(p, []))
    tag = 'WAJIB' if p in must else ('hidup' if p in live else '>>> DI LUAR REGISTRI')
    on_disk = (HOME / 'profiles' / p).exists()
    print(f"  {p:22s} proses={n} folder={'ada' if on_disk else 'TIDAK'} [{tag}]")
hantu = [p for p in rows if p not in live]
mati = [p for p in must if len(rows.get(p, [])) == 0]
print('VONIS-CIM: wajib_mati=%s hantu=%s' % (mati or 'none', hantu or 'none'))
