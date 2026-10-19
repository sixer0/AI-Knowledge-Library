#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 18-10 ronde a: cek kesegaran job monitor gateway + heartbeat state profil wajib."""
import json, io, os, time, datetime, pathlib

CRON = pathlib.Path(r'C:/Users/TRIAL/AppData/Local/hermes/cron/jobs.json')
HB = pathlib.Path(r'C:/Users/TRIAL/AppData/Local/hermes/profiles')

d = json.loads(CRON.read_text(encoding='utf-8'))
jobs = d.get('jobs', d) if isinstance(d, dict) else d
print("=== job cron terkait gateway/sysman ===")
for j in jobs:
    n = (j.get('name') or '')
    if 'gateway' in n.lower() or 'sysman' in str(j.get('id', '')).lower():
        print(f"  {j.get('id')} | {n} | sched={j.get('schedule') or j.get('cron')} | "
              f"enabled={j.get('enabled')} | last_run={j.get('last_run_at')} | next={j.get('next_run_at')} | "
              f"last_status={j.get('last_status') or j.get('last_result') or ''}")

print("=== heartbeat gateway per profil wajib (state/gateway.heartbeat) ===")
now = time.time()
for p in ('gsp-thinker', 'gsp-worker', 'gsp-worker-fast'):
    f = HB / p / 'state' / 'gateway.heartbeat'
    if not f.exists():
        print(f"  {p:<16} TIDAK-ADA-BERKAS")
        continue
    raw = f.read_text(encoding='utf-8', errors='replace').strip()
    age = now - f.stat().st_mtime
    print(f"  {p:<16} umur={age:.0f} dtk | {raw[:120]}")
