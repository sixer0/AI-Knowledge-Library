#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 15-10 ronde g: bukti kesegaran worker gateway (read-only).
Cek: umur proses root, mtime+ukuran gateway.log per profil wajib, baris log terakhir,
dan age of newest file di logs/ tiap profil."""
import os, subprocess, time, pathlib, datetime

HOME = pathlib.Path(os.environ['LOCALAPPDATA']) / 'hermes'
PROFS = ['gsp-thinker', 'gsp-worker', 'gsp-worker-fast']
ROOTS = {'gsp-thinker': [15072], 'gsp-worker': [18684], 'gsp-worker-fast': [10552]}

def ps(cmd, timeout=150):
    r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', cmd],
                       capture_output=True, text=True, timeout=timeout)
    return r.stdout

now = time.time()
print(f"=== FRESHNESS CHECK {datetime.datetime.now().isoformat(timespec='seconds')} ===")

# 1) umur proses root (filter PID server-side, murah)
pids = [p for v in ROOTS.values() for p in v]
flt = ' -or '.join(f'ProcessId={p}' for p in pids)
out = ps(f"Get-CimInstance Win32_Process -Filter '{flt}' | ForEach-Object {{ \"{{0}}|{{1}}\" -f $_.ProcessId, $_.CreationDate }}".replace('{{','{').replace('}}','}'))
for line in out.splitlines():
    if '|' in line:
        pid, created = line.split('|', 1)
        try:
            ct = datetime.datetime.fromisoformat(created.strip())
            age_h = (datetime.datetime.now() - ct).total_seconds()/3600
            print(f"proses pid={pid.strip()} lahir={created.strip()} umur={age_h:.1f} jam")
        except ValueError:
            print(f"proses pid={pid.strip()} lahir={created.strip()} (parse gagal)")

# 2) log per profil wajib
for prof in PROFS:
    logd = HOME / 'profiles' / prof / 'logs'
    gw = logd / 'gateway.log'
    if not gw.exists():
        print(f"{prof}: gateway.log TIDAK ADA")
        continue
    mt = gw.stat().st_mtime
    age_min = (now - mt)/60
    lines = gw.read_text(encoding='utf-8', errors='replace').splitlines()
    last = lines[-1][:160] if lines else '(kosong)'
    newest = max(((f.stat().st_mtime, f.name) for f in logd.glob('*.log')), default=(0,'-'))
    print(f"{prof}: gateway.log umur={age_min:.0f} mnt ukuran={gw.stat().st_size}B baris_terakhir='{last}'")
    print(f"    berkas terbaru di logs/: {newest[1]} umur={(now-newest[0])/60:.0f} mnt")
