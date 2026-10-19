#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnostik ronde cron 14-10b: kenapa monitor v1 menggantung >300 dtk.
Ukur durasi SATU query CIM via powershell subprocess (pola identik monitor),
lalu sensus sisa proses powershell/python warisan giliran sebelumnya.
Read-only terhadap gateway: tidak start/kill apa pun."""
import subprocess, sys, time

def timed_ps(cmd, timeout):
    t0 = time.time()
    try:
        r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', cmd],
                           capture_output=True, text=True, timeout=timeout)
        dt = time.time() - t0
        return dt, r.returncode, r.stdout[:400], r.stderr[:200]
    except subprocess.TimeoutExpired as e:
        dt = time.time() - t0
        return dt, 'TIMEOUT', (e.stdout or b'')[:200] if isinstance(e.stdout, bytes) else str(e.stdout)[:200], 'TIMEOUT'

Q = r"""
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(hermes|python|pythonw)\.exe$' -and $_.CommandLine -match 'gateway run' } | ForEach-Object { "{0}|{1}" -f $_.ProcessId, ($_.CommandLine -replace '\s+',' ') }
"""

dt, rc, out, err = timed_ps(Q, 60)
print(f"CIM_QUERY duration={dt:.1f}s rc={rc}")
print("stdout_lines=", len(out.splitlines()) if isinstance(out, str) else out)
if err:
    print("stderr=", err)

# Sensus proses powershell & python monitor warisan (read-only, tidak membunuh)
Q2 = r"""
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(powershell\.exe)$' } | ForEach-Object { "{0}|{1}" -f $_.ProcessId, ($_.CommandLine -replace '\s+',' ') }
"""
dt2, rc2, out2, err2 = timed_ps(Q2, 60)
print(f"\nPOWERSHELL_SENSUS duration={dt2:.1f}s rc={rc2}")
for line in (out2 or '').splitlines():
    print("  ", line[:160])
