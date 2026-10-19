#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Saksi kesegaran gateway TANPA WMI (ronde cron 19-10).

Baca state/gateway.heartbeat per profil dari registri hidup. Heartbeat ditulis
gateway tiap ~30 dtk (DEFAULT_HEARTBEAT_INTERVAL_S, gateway/shutdown_watchdog.py).
Profil `default` ber-home di ROOT hermes -> fallback path (pitfall 15-10 malam).
Read-only; tidak menyalakan/mematikan apa pun.
"""
import json, pathlib, datetime as dt, os

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path('C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

def hb_path(prof):
    p = HOME / 'profiles' / prof / 'state' / 'gateway.heartbeat'
    if not p.exists() and prof == 'default':
        p = HOME / 'state' / 'gateway.heartbeat'
    return p

def main():
    reg = json.loads(REG.read_text(encoding='utf-8'))
    live = list(reg['hidup'])
    must = list(reg['gateway_wajib_hidup'])
    now = dt.datetime.now(dt.timezone.utc)
    print(f"WAKTU_UTC={now.isoformat()}")
    print(f"REGistri_hidup={len(live)} wajib={sorted(must)}")
    fresh = []
    for prof in live:
        p = hb_path(prof)
        if not p.exists():
            print(f"  {prof:24s} TIDAK-ADA-BERKAS")
            continue
        try:
            d = json.loads(p.read_text(encoding='utf-8'))
            ts = dt.datetime.fromisoformat(d['updated_at'])
            age = max(0.0, (now - ts).total_seconds())
        except Exception as e:
            print(f"  {prof:24s} GALAT-BACA {type(e).__name__}")
            continue
        tag = 'FRESH' if age < 300 else 'stale'
        if age < 300:
            fresh.append(prof)
        print(f"  {prof:24s} age={age/60:8.1f}m pid={d.get('pid','?')} {tag} wajib={prof in must}")
    print(f"HITUNG_FRESH_lt5m={len(fresh)} -> {sorted(fresh)}")
    print(f"WAJIB_FRESH={sorted([p for p in fresh if p in must])} "
          f"WAJIB_TIDAK_FRESH={sorted([p for p in must if p not in fresh])}")

if __name__ == '__main__':
    main()
