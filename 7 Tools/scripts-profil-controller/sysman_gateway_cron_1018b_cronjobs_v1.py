#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 18-10 ronde b: dump struktur jobs.json + cari job monitor gateway."""
import json, pathlib

CRON = pathlib.Path(r'C:/Users/TRIAL/AppData/Local/hermes/cron/jobs.json')
d = json.loads(CRON.read_text(encoding='utf-8'))
print("top-level type:", type(d).__name__, "keys:", list(d)[:20] if isinstance(d, dict) else len(d))
jobs = d.get('jobs') if isinstance(d, dict) else d
if jobs is None:
    jobs = []
print("jumlah job:", len(jobs))
if jobs:
    print("contoh kunci job[0]:", sorted(jobs[0].keys()))
for j in jobs:
    blob = json.dumps(j, ensure_ascii=False).lower()
    name = str(j.get('name', ''))
    if 'gateway' in blob or 'monitor' in blob or 'sysman' in blob or 'ranta' in blob:
        print("---")
        for k in ('id', 'job_id', 'name', 'title', 'schedule', 'cron', 'expr', 'enabled',
                  'disabled', 'state', 'last_run_at', 'next_run_at', 'last_status', 'mode',
                  'deliver', 'script'):
            if k in j:
                print(f"  {k} = {j[k]}")
