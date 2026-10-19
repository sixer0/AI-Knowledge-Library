# -*- coding: utf-8 -*-
"""Saksi kesegaran gateway non-WMI (read-only), ronde cron 17-10.
Baca state/gateway.heartbeat per profil hidup dari registri; default home = ROOT hermes.
Deteksi ulang tiap ronde, tanpa PID di-pin (pitfall 15-10)."""
import json, os, pathlib, datetime as dt

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path('C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

d = json.loads(REG.read_text(encoding='utf-8'))
live = d['hidup']
must = set(d['gateway_wajib_hidup'])
now = dt.datetime.now(dt.timezone.utc)
print(f"registri: {len(live)} hidup, wajib={sorted(must)}")
for prof in live:
    p = HOME / 'profiles' / prof / 'state' / 'gateway.heartbeat'
    if not p.exists() and prof == 'default':
        p = HOME / 'state' / 'gateway.heartbeat'
    tag = 'WAJIB' if prof in must else '     '
    if not p.exists():
        print(f"[{tag}] {prof}: TIDAK-ADA-BERKAS")
        continue
    try:
        rec = json.loads(p.read_text(encoding='utf-8'))
        ts = dt.datetime.fromisoformat(rec['updated_at'])
        age = max(0.0, (now - ts).total_seconds())
        print(f"[{tag}] {prof}: pid={rec.get('pid')} umur={int(age)}dtk ({int(age/60)}mnt)")
    except Exception as e:
        print(f"[{tag}] {prof}: GALAT baca {e}")
