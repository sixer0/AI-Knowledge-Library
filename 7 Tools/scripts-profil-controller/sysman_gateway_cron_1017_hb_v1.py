#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Saksi kesegaran gateway non-WMI untuk ronde cron sysman 17-10.
Baca state/gateway.heartbeat per profil dari daftar hidup registri (bukan PID di-pin)."""
import json, os, pathlib, datetime as dt

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

live = json.loads(REG.read_text(encoding='utf-8'))
must = set(live['gateway_wajib_hidup'])
now = dt.datetime.now(dt.timezone.utc)
print("registri hidup:", len(live['hidup']), "| wajib:", sorted(must))
for prof in sorted(live['hidup']):
    p = HOME / 'profiles' / prof / 'state' / 'gateway.heartbeat'
    if not p.exists() and prof == 'default':
        p = HOME / 'state' / 'gateway.heartbeat'
    if not p.exists():
        print(f"{'WAJIB ' if prof in must else '      '}{prof}: TIDAK-ADA-BERKAS")
        continue
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
        ts = dt.datetime.fromisoformat(d['updated_at'])
        age = max(0.0, (now - ts).total_seconds())
        flag = "SEGAR" if age < 180 else ("BASAH" if age < 3600 else "BASI")
        print(f"{'WAJIB ' if prof in must else '      '}{prof}: pid={d.get('pid')} umur={age:.0f}s [{flag}]")
    except Exception as e:
        print(f"{'WAJIB ' if prof in must else '      '}{prof}: GALAT {type(e).__name__} {e}")
