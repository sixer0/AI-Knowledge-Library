#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sensus proses via psutil (tanpa WMI) - ronde cron 14-10b.
Cari sisa proses dari giliran monitor yang waktu-habis: powershell yatim,
python monitor, uv. Read-only: hanya mencetak, tidak membunuh."""
import psutil, time, datetime

now = time.time()
rows = []
for p in psutil.process_iter(['pid', 'ppid', 'name', 'cmdline', 'create_time']):
    try:
        name = (p.info['name'] or '').lower()
        cmd = ' '.join(p.info['cmdline'] or [])
        if name in ('powershell.exe', 'python.exe', 'pythonw.exe', 'hermes.exe', 'uv.exe', 'conhost.exe'):
            low = cmd.lower()
            if any(t in low for t in ('gateway', 'monitor', 'ciminstance', 'get-cim', 'win32_process', 'audit')):
                age_min = (now - (p.info['create_time'] or now)) / 60.0
                rows.append((p.info['pid'], p.info['ppid'], p.info['name'], age_min, cmd[:220]))
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

print(f"sensus {datetime.datetime.now().isoformat(timespec='seconds')} | baris={len(rows)}")
for pid, ppid, name, age, cmd in sorted(rows, key=lambda r: -r[3]):
    print(f"  pid={pid:<7} ppid={ppid:<7} {name:<14} umur={age:7.1f}mnt  {cmd}")
