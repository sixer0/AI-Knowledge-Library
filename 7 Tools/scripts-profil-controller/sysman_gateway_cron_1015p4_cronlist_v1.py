#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 15-10 ronde p4 (read-only): daftar SEMUA job cron di semua sumber + mana yang memanggil monitor."""
import json, pathlib, os

HOME = pathlib.Path(r"C:/Users/TRIAL/AppData/Local/hermes")
paths = [HOME / 'cron' / 'jobs.json'] + sorted((HOME / 'profiles').glob('*/cron/jobs.json'))
for p in paths:
    if not p.exists():
        continue
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"{p}: GALAT {e}")
        continue
    jobs = d['jobs'] if isinstance(d, dict) and 'jobs' in d else d
    print(f"\n### {p}  ({len(jobs)} job)")
    for j in jobs:
        blob = json.dumps(j, ensure_ascii=False)
        mark = ' <== MONITOR' if 'gateway_monitor' in blob or 'Gateway Monitor' in blob else ''
        print(f"  id={j.get('id')} name={j.get('name')!r} enabled={j.get('enabled')} "
              f"schedule={j.get('schedule') or j.get('cron') or j.get('interval')} "
              f"last_run={j.get('last_run_at')} last_status={j.get('last_status')}{mark}")
        if mark:
            print("    keys:", sorted(j.keys()))
            for k in ('script', 'command', 'prompt', 'message', 'payload', 'task', 'deliver', 'mode', 'agent'):
                if k in j:
                    print(f"    {k} = {str(j[k])[:300]}")
