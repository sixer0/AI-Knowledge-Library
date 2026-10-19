#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ukur waktu query CIM gateway (read-only) untuk menambal monitor v1. Sysman 14-10 malam."""
import subprocess, time

Q_ALL = r"""
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(hermes|python|pythonw)\.exe$' -and $_.CommandLine -match 'gateway run' } | ForEach-Object { "{0}|{1}" -f $_.ProcessId, ($_.CommandLine -replace '\s+',' ') }
"""

Q_FILTER = r"""
Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'" | Where-Object { $_.CommandLine -match 'gateway run' } | ForEach-Object { "{0}|{1}" -f $_.ProcessId, ($_.CommandLine -replace '\s+',' ') }
"""

Q_TOTAL = 'Get-CimInstance Win32_Process | Measure-Object | Select-Object -ExpandProperty Count'


def run(cmd, timeout=300):
    t0 = time.time()
    try:
        r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', cmd],
                           capture_output=True, text=True, timeout=timeout)
        return time.time() - t0, len(r.stdout.splitlines()), r.stdout, r.stderr[:200]
    except subprocess.TimeoutExpired:
        return time.time() - t0, -1, '(TIMEOUT)', ''


for label, q in (('TOTAL-PROSES', Q_TOTAL), ('ALL-NOCIMFILTER', Q_ALL), ('CIMNAMEFILTER', Q_FILTER)):
    dur, nlines, out, err = run(q)
    print(f"{label}: dur={dur:.1f}s lines={nlines} err={err.strip()[:120]}")
    if label == 'CIMNAMEFILTER':
        for ln in out.splitlines():
            print('   ', ln[:150])
