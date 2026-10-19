#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Saksi kesegaran gateway non-WMI (ronde cron 17-10 malam).
Baca state/gateway.heartbeat per profil dari daftar hidup registri.
Deteksi ulang akar tiap ronde via satu lintasan CIM berfilter nama (tanpa pin PID)."""
import json, os, re, subprocess, datetime as dt, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path('C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

d = json.loads(REG.read_text(encoding='utf-8'))
live = d['hidup']
must = d['gateway_wajib_hidup']

q = """
Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'" | Where-Object { $_.CommandLine -match 'gateway run' } | ForEach-Object { "{0}|{1}" -f $_.ProcessId, ($_.CommandLine -replace '\\s+',' ') }
"""
r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', q],
                   capture_output=True, text=True, timeout=150)
print('cim rc=', r.returncode)
procs = {}
for line in r.stdout.splitlines():
    if '|' not in line:
        continue
    pid, cmd = line.split('|', 1)
    m = re.search(r'--profile\s+(\S+)', cmd) or re.search(r'-p\s+(\S+)', cmd)
    prof = m.group(1) if m else 'default'
    procs.setdefault(prof, []).append(int(pid))

now = dt.datetime.now(dt.timezone.utc)
print('--- umur heartbeat (dtk) vs proses CIM ---')
for p in live:
    hb = HOME / 'profiles' / p / 'state' / 'gateway.heartbeat'
    if not hb.exists() and p == 'default':
        hb = HOME / 'state' / 'gateway.heartbeat'
    if hb.exists():
        try:
            j = json.loads(hb.read_text(encoding='utf-8'))
            age = (now - dt.datetime.fromisoformat(j['updated_at'])).total_seconds()
            hbs = f"{age:8.0f}"
        except Exception as e:
            hbs = f"ERR {e}"
    else:
        hbs = 'TIDAK-ADA-BERKAS'
    n = len(procs.get(p, []))
    tag = 'WAJIB' if p in must else ''
    print(f"{p:22s} proc={n} hb={hbs} {tag}")

ghosts = {k: v for k, v in procs.items() if k not in live}
print('--- hantu di luar registri:', ghosts if ghosts else 'NOL')
