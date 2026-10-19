#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Saksi kesegaran heartbeat gateway non-WMI (ronde cron 17-10 sysman).
Baca state/gateway.heartbeat per profil di daftar hidup registri. Read-only."""
import json, datetime, pathlib, os
HOME = pathlib.Path(os.environ['LOCALAPPDATA']) / 'hermes'
REG = pathlib.Path('C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')
reg = json.loads(REG.read_text(encoding='utf-8'))
live = reg['hidup']; must = reg['gateway_wajib_hidup']
now = datetime.datetime.now(datetime.timezone.utc)

def hb(prof):
    p = HOME / 'profiles' / prof / 'state' / 'gateway.heartbeat'
    if not p.exists() and prof == 'default':
        p = HOME / 'state' / 'gateway.heartbeat'
    if not p.exists():
        return None, None
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
        ts = datetime.datetime.fromisoformat(d['updated_at'])
        return max(0.0, (now - ts).total_seconds()), d.get('pid')
    except Exception as e:
        return f'ERR:{e}', None

print("=== SET WAJIB ===")
fresh = 0
for m in sorted(must):
    a, pid = hb(m)
    s = f"{a:.0f}s" if isinstance(a, float) else str(a)
    if isinstance(a, float) and a < 300:
        fresh += 1
    print(f"{m:22s} age={s} pid={pid}")
print(f"FRESH(<300s)={fresh}/{len(must)}")
print("=== SEMUA PROFIL HIDUP ===")
for m in sorted(live):
    a, pid = hb(m)
    s = f"{a:.0f}s" if isinstance(a, float) else str(a)
    print(f"{m:22s} age={s} pid={pid}")
