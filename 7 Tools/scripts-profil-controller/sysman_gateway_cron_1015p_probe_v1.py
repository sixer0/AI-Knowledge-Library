#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 15-10 ronde p (read-only diagnostik).

Monitor v1 ronde 13:03 mencetak AKSI START x3 padahal ketiga gateway wajib sudah hidup
26,3 jam (akar lahir 14-10 10:48:50) dan log start profil menulis 'Another gateway instance
is already running'. Hipotesis: lintasan CIM monitor mengembalikan stdout KOSONG/galat dan
ps() TIDAK memeriksa returncode -> keadaan 'semua mati' palsu. Skrip ini mengukur query
monitor apa adanya (rc, stderr, jumlah baris, durasi) dan memanggil live_gateways() modul
kanonis langsung, tanpa mengubah berkas penjaga.
"""
import importlib.util, re, subprocess, sys, time

MON = r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_gateway_monitor_v1.py"

Q = r"""
Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'" | Where-Object { $_.CommandLine -match 'gateway run' } | ForEach-Object { "{0}|{1}" -f $_.ProcessId, ($_.CommandLine -replace '\s+',' ') }
"""

for i in range(2):
    t0 = time.time()
    r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', Q],
                       capture_output=True, text=True, timeout=200)
    dt = time.time() - t0
    lines = [l for l in r.stdout.splitlines() if '|' in l]
    profs = {}
    for l in lines:
        pid, cmd = l.split('|', 1)
        m = re.search(r'--profile\s+(\S+)', cmd) or re.search(r'-p\s+(\S+)', cmd)
        profs.setdefault(m.group(1) if m else 'default', 0)
        profs[m.group(1) if m else 'default'] += 1
    print(f"[lintasan {i+1}] rc={r.returncode} durasi={dt:.0f}s baris={len(lines)}")
    print(f"  profil={sorted(profs.items())}")
    if r.stderr.strip():
        print("  STDERR:", r.stderr.strip()[:800])

spec = importlib.util.spec_from_file_location("mon", MON)
mon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mon)
t0 = time.time()
gw = mon.live_gateways()
print(f"[live_gateways modul] durasi={time.time()-t0:.0f}s -> " +
      ", ".join(f"{k}:{len(v)}" for k, v in sorted(gw.items())))
live, must = mon.registry()
print("must:", sorted(must), "| terlihat monitor:", {m: len(gw.get(m, [])) for m in sorted(must)})
print("hantu (di luar registri):", sorted(p for p in gw if p not in live))
