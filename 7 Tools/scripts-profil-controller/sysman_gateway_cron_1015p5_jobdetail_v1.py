#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 15-10 ronde p5 (read-only): hanya job pemanggil monitor gateway + riwayat outputnya."""
import json, pathlib, datetime, os

HOME = pathlib.Path(r"C:/Users/TRIAL/AppData/Local/hermes")
paths = [HOME / 'cron' / 'jobs.json'] + sorted((HOME / 'profiles').glob('*/cron/jobs.json'))
for p in paths:
    if not p.exists():
        continue
    d = json.loads(p.read_text(encoding='utf-8'))
    jobs = d['jobs'] if isinstance(d, dict) and 'jobs' in d else d
    for j in jobs:
        blob = json.dumps(j, ensure_ascii=False)
        if 'gateway_monitor' in blob or 'Gateway Monitor' in blob or 'gateway monitor' in blob.lower():
            print(f"### {p}")
            print(json.dumps(j, ensure_ascii=False, indent=1)[:2500])
            prof = p.parts[-3]
            for od in (HOME / 'profiles' / prof / 'cron' / 'output' / str(j.get('id')),
                       HOME / 'cron' / 'output' / str(j.get('id'))):
                if od.exists():
                    fs = sorted(od.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True)[:8]
                    print(f"\n>>> output folder {od} ({len(fs)} terbaru)")
                    for f in fs:
                        ts = datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime('%m-%d %H:%M')
                        txt = f.read_text(encoding='utf-8', errors='replace')
                        print(f"  [{ts}] {f.name} ukuran={len(txt)} AKSI={'AKSI' in txt} START={'START' in txt}")
                        if 'AKSI' in txt or 'ERROR' in txt:
                            print('      ' + txt.strip().replace('\n', '\n      ')[:500])
