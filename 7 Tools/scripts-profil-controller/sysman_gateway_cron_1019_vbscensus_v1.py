#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sensus autostart login vs registri hidup (ronde cron 19-10, read-only).

Menandingkan VBS gateway di folder Startup dengan daftar hidup registri.
VBS profil arsip harus berakhiran .disabled-<tanggal> (norma PROF-MERGE-1010).
"""
import json, pathlib, re

STARTUP = pathlib.Path('C:/Users/TRIAL/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup')
REG = pathlib.Path('C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

reg = json.loads(REG.read_text(encoding='utf-8'))
live = set(reg['hidup'])
must = set(reg['gateway_wajib_hidup'])

active, disabled = [], []
for p in sorted(STARTUP.glob('*.vbs*')):
    if '.disabled' in p.name:
        disabled.append(p.name)
        continue
    if not p.name.lower().startswith('hermes_gateway'):
        continue  # bukan VBS gateway hermes (docker-desktop, gsp-ecosystem, dll)
    m = re.match(r'Hermes_Gateway_(.+)\.vbs$', p.name, re.I)
    active.append(m.group(1) if m else p.name)

print(f"VBS_gateway_aktif={len(active)} vbs_disabled={len(disabled)}")
print("--- VBS gateway aktif vs registri ---")
for prof in active:
    tgt = 'WAJIB' if prof in must else ('hidup' if prof in live else '*** DI-LUAR-REGISTRI ***')
    print(f"  {prof:28s} {tgt}")
no_vbs = sorted(p for p in must if p not in active)
print(f"WAJIB_tanpa_VBS_autostart={no_vbs if no_vbs else 'NONE'}")
stray = sorted(p for p in active if p not in live)
print(f"VBS_aktif_di_luar_registri={stray if stray else 'NONE'}")
leftover = sorted(d for d in disabled if not re.search(r'\.disabled-\d{6,}', d))
print(f"disabled_tanpa_stempel_tanggal={leftover if leftover else 'NONE'}")
