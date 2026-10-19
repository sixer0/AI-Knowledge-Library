#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe fungsional gateway worker: status CLI + port listen + umur log. Read-only."""
import subprocess, re, os, time, glob, pathlib

PY = r'C:/Users/TRIAL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe'
HOME = pathlib.Path(r'C:/Users/TRIAL/AppData/Local/hermes')
WORKERS = ['gsp-thinker', 'gsp-worker', 'gsp-worker-fast']

for prof in WORKERS:
    print('===', prof, '===')
    # 1) status via modul CLI (bukan wrapper .cmd agar bebas PATH)
    try:
        r = subprocess.run([PY, '-m', 'hermes_cli.main', '--profile', prof, 'gateway', 'status'],
                           capture_output=True, text=True, timeout=90,
                           cwd=str(HOME / 'profiles' / prof))
        out = (r.stdout + r.stderr).strip().replace('\n', ' | ')
        print('  status:', out[:300])
    except Exception as e:
        print('  status ERROR:', repr(e)[:200])
    # 2) umur berkas log gateway terakhir (indikator aktivitas)
    logs = sorted(glob.glob(str(HOME / 'profiles' / prof / 'logs' / '*gateway*')),
                  key=os.path.getmtime) or sorted(
                  glob.glob(str(HOME / 'gateway-logs' / f'*{prof}*')), key=os.path.getmtime)
    if logs:
        f = logs[-1]
        age = (time.time() - os.path.getmtime(f)) / 60.0
        print(f'  log terbaru: {os.path.basename(f)} umur={age:.0f} menit ukuran={os.path.getsize(f)} B')
    else:
        print('  log gateway: tidak ditemukan di profil/logs maupun gateway-logs')

# 3) port listen milik proses gateway (bukti servis benar-benar menyimak)
Q = r"""
$conns = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(python|pythonw|hermes)\.exe$' -and $_.CommandLine -match 'gateway run' } | ForEach-Object {
  $p=$_.ProcessId
  $ports = ($conns | Where-Object { $_.OwningProcess -eq $p } | ForEach-Object { $_.LocalPort }) -join ','
  $prof = 'default'
  if ($_.CommandLine -match '--profile\s+(\S+)') { $prof=$matches[1] } elseif ($_.CommandLine -match '-p\s+(\S+)') { $prof=$matches[1] }
  "{0}|{1}|{2}" -f $prof, $p, $ports
}
"""
r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', Q],
                   capture_output=True, text=True, timeout=150)
print('=== port LISTEN per proses gateway ===')
seen = set()
for line in r.stdout.splitlines():
    if line.count('|') == 2 and line not in seen:
        seen.add(line)
        prof, pid, ports = line.split('|')
        print(f'  {prof:<20} pid={pid:<6} ports=[{ports}]')
