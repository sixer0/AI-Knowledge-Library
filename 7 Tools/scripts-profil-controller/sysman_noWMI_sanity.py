#!/usr/bin/env python3
"""Sanity probe noWMI: buktikan scanner bisa baca cmdline (bukan buta)."""
import importlib.util, sys, pathlib

spec = importlib.util.spec_from_file_location("audit", r'C:/Users/TRIAL/AppData/Local/hermes/scripts/sysman_audit_noWMI_v1.py')
m = importlib.util.module_from_spec(spec)
# matikan eksekusi main: modul tidak punya guard __main__, jadi jalankan penuh lalu baca fungsi
sys.modules['audit'] = m
spec.loader.exec_module(m)

procs = m.list_processes()
py = [(pid, ppid, img) for pid, ppid, img in procs if img in ('python.exe','pythonw.exe','hermes.exe')]
print(f"total proses python/hermes terlihat: {len(py)}")
shown = 0
for pid, ppid, img in py:
    cl = m.cmdline_for_pid(pid) or ''
    print(f"  pid={pid} ppid={ppid} img={img} cmdline={cl[:100]}")
    shown += 1
    if shown >= 15:
        break
if not py:
    print("BUTA: tidak ada python/hermes terlihat sama sekali")
elif all(not (m.cmdline_for_pid(pid) or '') for pid,_,_ in py[:5]):
    print("BUTA-PARSIAL: proses terlihat tapi cmdline kosong semua")
else:
    print("SANITY OK: scanner bisa baca cmdline")
