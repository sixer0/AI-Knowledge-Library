#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 16-10 zg: tutup CATATAN audit (PID dgn 'gateway' tanpa 'gateway run') + saksi heartbeat."""
import json, os, subprocess, time, datetime, pathlib

PROFILES = pathlib.Path(r'C:/Users/TRIAL/AppData/Local/hermes/profiles')
WATCH = ["gsp-thinker", "gsp-worker", "gsp-worker-fast"]

CMD = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'\" | "
       "ForEach-Object { if ($_.CommandLine -match 'gateway' -and $_.CommandLine -notmatch 'gateway run') { "
       "$_.ProcessId.ToString() + '|' + $_.CreationDate.ToString('yyyy-MM-dd HH:mm:ss') + '|' + $_.CommandLine } }")

t0 = time.time()
try:
    r = subprocess.run(["powershell", "-NoProfile", "-Command", CMD],
                       capture_output=True, text=True, timeout=150)
    rows = [ln for ln in r.stdout.splitlines() if ln.strip()]
    print(f"CIM rc={r.returncode} durasi={time.time()-t0:.0f}s baris_anomali={len(rows)}")
    mine = {os.getpid()}
    for ln in rows:
        pid, created, cmd = ln.split('|', 2)
        tag = "DIRI-SENDIRI" if int(pid) in mine else "LAIN"
        print(f"  pid={pid} lahir={created} [{tag}] cmd={cmd[:160]}")
except Exception as e:
    print("CIM GAGAL:", type(e).__name__, e)

print("--- saksi heartbeat (non-WMI) ---")
now = datetime.datetime.now(datetime.timezone.utc)
for p in WATCH:
    f = PROFILES / p / "state" / "gateway.heartbeat"
    if not f.exists():
        print(f"  {p:16s} TIDAK-ADA-BERKAS")
        continue
    d = json.loads(f.read_text(encoding="utf-8"))
    upd = datetime.datetime.fromisoformat(d["updated_at"].replace("Z", "+00:00"))
    age = (now - upd).total_seconds()
    live = "SEHAT" if age < 180 else "BASI"
    print(f"  {p:16s} pid={d['pid']:>6} umur_hb={age:5.0f}s -> {live}")
