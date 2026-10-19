#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Saksi non-WMI ronde cron 18-10: umur berkas state/gateway.heartbeat SEMUA profil
di disk dibandingkan daftar hidup registri. Gateway mana pun (exe apa pun) menulis
heartbeat ini tiap ~30 dtk, jadi baris berumur < 180 dtk pada profil DI LUAR daftar
hidup = indikasi hantu yang lolos filter nama proses CIM. Read-only."""
import json, os, pathlib, datetime, sys

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path('C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

d = json.loads(REG.read_text(encoding='utf-8'))
live = set(d['hidup']); must = set(d['gateway_wajib_hidup'])
now = datetime.datetime.now(datetime.timezone.utc)

def age(p):
    try:
        ts = datetime.datetime.fromisoformat(json.loads(p.read_text(encoding='utf-8'))['updated_at'])
        return max(0.0, (now - ts).total_seconds())
    except Exception:
        return None

rows = []
p_default = HOME / 'state' / 'gateway.heartbeat'
if p_default.exists():
    rows.append(('default', age(p_default)))
for prof_dir in sorted((HOME / 'profiles').iterdir()):
    if not prof_dir.is_dir():
        continue
    hb = prof_dir / 'state' / 'gateway.heartbeat'
    if hb.exists():
        rows.append((prof_dir.name, age(hb)))

fresh_outside = []
print(f"{'profil':<24}{'heartbeat_dtk':>14}   status")
for prof, a in sorted(rows, key=lambda r: (r[1] is None, r[1])):
    tag = ('WAJIB' if prof in must else ('hidup-di-registri' if prof in live else 'DI-LUAR-DAFTAR'))
    if a is not None and a < 180 and prof not in live:
        fresh_outside.append(prof); tag = 'HANTU-FRESH'
    print(f"{prof:<24}{('%.0f' % a) if a is not None else 'N/A':>14}   {tag}")
print('---')
print('profil di disk tanpa berkas heartbeat:', len([p for p in (x.name for x in (HOME/'profiles').iterdir() if x.is_dir()) if p not in [r[0] for r in rows]]))
print('VONIS SAKSI:', 'BERSIH (nol gateway fresh di luar daftar hidup)' if not fresh_outside else f'HANTU={fresh_outside}')
sys.exit(0)
