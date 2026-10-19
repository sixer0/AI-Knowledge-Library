# -*- coding: utf-8 -*-
"""Saksi kesegaran gateway non-WMI: heartbeat per profil wajib + daftar hidup registri."""
import json, os, pathlib, datetime as dt

HOME = pathlib.Path(os.environ['LOCALAPPDATA']) / 'hermes'
REG = pathlib.Path('C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

d = json.loads(REG.read_text(encoding='utf-8'))
must = sorted(d['gateway_wajib_hidup'])
for prof in must:
    p = HOME / 'profiles' / prof / 'state' / 'gateway.heartbeat'
    if not p.exists():
        print(f"{prof}: TIDAK-ADA-BERKAS")
        continue
    try:
        hb = json.loads(p.read_text(encoding='utf-8'))
        ts = dt.datetime.fromisoformat(hb['updated_at'])
        age = max(0.0, (dt.datetime.now(dt.timezone.utc) - ts).total_seconds())
        print(f"{prof}: pid={hb.get('pid')} umur_heartbeat={int(age)}dtk")
    except Exception as e:
        print(f"{prof}: GALAT {e}")
