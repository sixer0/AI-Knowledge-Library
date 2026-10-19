#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 15-10 ronde h (revisi): umur proses ROOT gateway wajib (read-only).

Pelajaran ronde h awal: psutil.process_iter + lookup cmdline induk per proses menggantung
>180 dtk saat WMI lambat. Ganti ke SATU query CIM berfilter nama server-side (Name=python*)
yang sudah mengembalikan ProcessId, ParentProcessId, CreationDate, CommandLine sekaligus;
akar = proses 'gateway run' yang induknya tidak ikut 'gateway run'. Nol loop psutil.
"""
import subprocess, datetime, re, time

PROFS = ['gsp-thinker', 'gsp-worker', 'gsp-worker-fast']
PROF_RE = re.compile(r"(?:--profile|-p)\s+(\S+)")

CMD = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe'\" | "
       "ForEach-Object { if ($_.CommandLine -match 'gateway run') { "
       "$_.ProcessId.ToString() + '|' + $_.ParentProcessId.ToString() + '|' + "
       "$_.CreationDate.ToString('yyyy-MM-dd HH:mm:ss') + '|' + $_.CommandLine } }")

t0 = time.time()
r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', CMD],
                   capture_output=True, text=True, timeout=150)
rows = []
for line in r.stdout.splitlines():
    parts = line.split('|', 3)
    if len(parts) == 4:
        rows.append(parts)
by_pid = {int(p[0]): p for p in rows}
print(f"CIM satu lintasan: {len(rows)} proses 'gateway run' dalam {time.time()-t0:.0f} dtk")
now = datetime.datetime.now()
for prof in PROFS:
    found = False
    for pid_s, ppid_s, created, cmd in rows:
        m = PROF_RE.search(cmd)
        if not m or m.group(1) != prof:
            continue
        ppid = int(ppid_s)
        parent_is_gw = ppid in by_pid and 'gateway run' in by_pid[ppid][3].lower()
        ct = datetime.datetime.strptime(created.strip(), '%Y-%m-%d %H:%M:%S')
        age_h = (now - ct).total_seconds() / 3600
        print(f"{prof}: pid={pid_s} root={not parent_is_gw} lahir={created} umur={age_h:.1f} jam")
        found = True
    if not found:
        print(f"{prof}: TIDAK ADA PROSES gateway run -> MATI")
