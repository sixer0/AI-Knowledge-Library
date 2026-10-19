#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 15-10 ronde p2 (read-only): cmdline penuh gateway wajib + riwayat AKSI hantu.

Tujuan:
 A) Apakah proses 'gateway run' yang hidup mencantumkan '--profile <nama>' di cmdline?
    (monitor v1 mengelompokkan profil dari regex itu; tanpa flag = semua masuk 'default')
 B) Berapa sering monitor mencetak AKSI START dari waktu ke waktu (log start per profil).
"""
import glob, os, re, subprocess, time

CMD = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe'\" | "
       "ForEach-Object { if ($_.CommandLine -match 'gateway run') { "
       "$_.ProcessId.ToString() + '|' + $_.CreationDate.ToString('yyyy-MM-dd HH:mm:ss') + '|' + $_.CommandLine } }")
t0 = time.time()
r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', CMD], capture_output=True, text=True, timeout=200)
rows = [l.split('|', 2) for l in r.stdout.splitlines() if l.count('|') >= 2]
print(f"CIM rc={r.returncode} durasi={time.time()-t0:.0f}s baris={len(rows)}")
want = ('gsp-thinker', 'gsp-worker', 'gsp-worker-fast')
for parts in rows:
    pid, created, cmd = parts
    cmd = cmd.strip()
    if any(w in cmd for w in want):
        print(f"  pid={pid} lahir={created}\n    CMD: {cmd[:400]}")
print("--- baris tanpa token --profile/-p (kandidat masuk bucket 'default') ---")
n_noflag = 0
for parts in rows:
    pid, created, cmd = parts.strip() if False else parts
    cmd = cmd.strip()
    if not re.search(r'(?:--profile|-p)\s+\S+', cmd):
        n_noflag += 1
        print(f"  pid={pid} CMD: {cmd[:300]}")
print(f"total tanpa flag profil: {n_noflag} dari {len(rows)}")

print("\n--- riwayat 'Another gateway instance' / start gagal per profil ---")
base = r"C:/Users/TRIAL/AppData/Local/hermes/profiles"
for p in want:
    f = os.path.join(base, p, 'logs', 'gateway-monitor-start.log')
    if not os.path.exists(f):
        print(f"{p}: (tidak ada log)")
        continue
    txt = open(f, encoding='utf-8', errors='replace').read()
    n_busy = txt.count('Another gateway instance')
    print(f"{p}: ukuran={len(txt)}B  'Another gateway instance' x{n_busy}")
    for m in re.finditer(r'^(\d{4}-\d\d-\d\d[ T]\d\d:\d\d:\d\d[.,]?\d*).{0,120}$', txt, re.M):
        pass
