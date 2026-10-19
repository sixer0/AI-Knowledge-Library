#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Saksi kesegaran gateway TANPA WMI (ronde cron 15-10-2026 malam).

Baca profiles/<p>/state/gateway.heartbeat per profil wajib + daftar hidup registri.
Tidak menyentuh CIM sama sekali, jadi kebal terhadap kelas kegagalan WMI lambat/wedged.
Vonis akar tetap milik gsp_gateway_audit_v1.py; alat ini hanya membuktikan gateway
menulis denyutnya sendiri (pid + updated_at UTC) dan tidak mem-PID apa pun.
"""
import json, os, pathlib, datetime as dt, sys

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path('C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')


def hb(prof):
    p = HOME / 'profiles' / prof / 'state' / 'gateway.heartbeat'
    if not p.exists() and prof == 'default':
        p = HOME / 'state' / 'gateway.heartbeat'
    if not p.exists():
        return None, None, str(p)
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
        ts = dt.datetime.fromisoformat(d['updated_at'])
        age = max(0.0, (dt.datetime.now(dt.timezone.utc) - ts).total_seconds())
        return age, d.get('pid'), str(p)
    except Exception as e:
        return None, f'PARSE-ERR {e}', str(p)


def main():
    d = json.loads(REG.read_text(encoding='utf-8'))
    live, must = set(d['hidup']), list(d['gateway_wajib_hidup'])
    print(f"registri: {len(live)} profil hidup, wajib gateway = {must}")
    bad = 0
    for p in sorted(set(must)):
        age, pid, path = hb(p)
        if age is None:
            print(f"  {p:<16} HEARTBEAT TIDAK ADA/BACA GAGAL ({pid}) -> {path}")
            bad += 1
            continue
        flag = 'SEGAR' if age < 180 else ('LAMA' if age < 3600 else 'BASI')
        if flag != 'SEGAR':
            bad += 1
        print(f"  {p:<16} umur={int(age):>6} dtk pid={pid} {flag}")
    # sensus heartbeat semua profil hidup di luar wajib (informasi, bukan vonis)
    others = sorted(live - set(must))
    any_other = [p for p in others if hb(p)[0] is not None]
    print(f"  profil hidup non-wajib ber-heartbeat: {len(any_other)} {any_other}")
    print("HASIL: " + ("SEMUA WAJIB SEGAR" if bad == 0 else f"{bad} PROFIL WAJIB TIDAK SEGAR"))
    return 0


if __name__ == '__main__':
    sys.exit(main())
