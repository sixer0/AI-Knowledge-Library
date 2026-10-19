#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Klasifikasi proses gateway: apakah n>1 per profil = rantai parent/child (normal)
atau instans independen (masalah: rebutan port/konsumen pesan ganda). Read-only."""
import re, subprocess, collections

Q = r"""
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(hermes|python|pythonw)\.exe$' -and $_.CommandLine -match 'gateway run' } | ForEach-Object { "{0}|{1}|{2}|{3}" -f $_.ProcessId, $_.ParentProcessId, ($_.CreationDate | Get-Date -Format 'HH:mm:ss'), ($_.CommandLine -replace '\s+',' ') }
"""
r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', Q],
                   capture_output=True, text=True, timeout=150)
rows = []
for line in r.stdout.splitlines():
    p = line.split('|', 3)
    if len(p) == 4:
        rows.append(p)

by = collections.defaultdict(list)
for pid, ppid, created, cmd in rows:
    m = re.search(r'--profile\s+(\S+)', cmd) or re.search(r'-p\s+(\S+)', cmd)
    prof = m.group(1) if m else 'default'
    by[prof].append((int(pid), int(ppid), created, cmd[:110]))

pids = {int(a[0]) for a in rows}
print("profil | pid | ppid | lahir | ppid-adalah-proses-gateway? | peran")
for prof in sorted(by):
    for pid, ppid, created, cmd in sorted(by[prof], key=lambda x: x[0]):
        chain = "YA (anak gateway)" if ppid in pids else ("ppid=%d di luar himpunan" % ppid)
        root = "ROOT" if ppid not in pids else "CHILD"
        print(f"{prof:<20} {pid:<6} {ppid:<6} {created} {chain:<34} {root}")
    # vonis per profil: jumlah ROOT = jumlah instans independen
    roots = [pid for pid, ppid, _, _ in by[prof] if ppid not in pids]
    print(f"{prof:<20} => INSTANS INDEPENDEN (root) = {len(roots)} {roots}")
