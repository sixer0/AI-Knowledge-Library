#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 15-10 ronde p3 (read-only): riwayat job cron gateway-monitor + outputnya.

Mencari apakah vonis '0 proses' berulang tiap ronde (cacat sistematis) atau kejadian tunggal.
"""
import json, os, pathlib, datetime

HOME = pathlib.Path(r"C:/Users/TRIAL/AppData/Local/hermes")
d = json.loads((HOME / 'cron' / 'jobs.json').read_text(encoding='utf-8'))
jobs = d['jobs'] if isinstance(d, dict) and 'jobs' in d else d
for j in jobs:
    blob = json.dumps(j, ensure_ascii=False)
    if 'gateway' in blob.lower():
        keep = {k: j.get(k) for k in ('id', 'name', 'enabled', 'schedule', 'schedule_type',
                                      'provider', 'model', 'deliver', 'last_run_at',
                                      'next_run_at', 'last_status', 'script', 'command')
                if k in j}
        print(json.dumps(keep, ensure_ascii=False)[:1200])
        print('---')

print("\n=== output terbaru job gateway-monitor ===")
for j in jobs:
    if 'gateway' in json.dumps(j, ensure_ascii=False).lower():
        od = HOME / 'profiles' / 'gsp-system-manager' / 'cron' / 'output' / str(j.get('id'))
        if not od.exists():
            od = HOME / 'cron' / 'output' / str(j.get('id'))
        if not od.exists():
            print(f"job {j.get('id')}: folder output tidak ada")
            continue
        files = sorted(od.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True)[:6]
        print(f"job {j.get('id')} ({j.get('name')}): {len(files)} berkas terbaru")
        for f in files:
            ts = datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
            txt = f.read_text(encoding='utf-8', errors='replace')[:600]
            print(f"\n>>> {f.name} [{ts}] ukuran={f.stat().st_size}")
            print(txt)
