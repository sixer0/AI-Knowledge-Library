#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSP Registry Freshness Guard v1 (PROF-MERGE-1010). Mingguan, no_agent, diam-saat-sehat.

Bandingkan PROFILE-REGISTRY.json vs kenyataan:
  1) akun WebUiUser (pg via node) -> hermesProfile wajib ada di registri hidup
  2) folder profil di disk: gsp-* yang hidup tapi TIDAK di registri = kandidat arsip terlupakan
  3) entri registri yang foldernya sudah hilang dari disk
Laporkan drift; TIDAK mengubah apa pun (keputusan promosi/arsip = wewenang user/controller).
"""
import json, os, re, subprocess, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')
DC = r'C:/Users/TRIAL/gsp-datacenter'

def main():
    d = json.loads(REG.read_text(encoding='utf-8'))
    live = set(d['hidup'])
    drift = []
    # 1) RBAC vs registri
    jsf = pathlib.Path(DC) / 'tmp_gsp_rbac_rows.cjs'
    jsf.write_text("""const{Client}=require('pg');
const u=require('fs').readFileSync('.env','utf8').match(/DATABASE_URL="([^"]+)"/)[1];
const c=new Client({connectionString:u});
c.connect().then(()=>c.query('SELECT username, role, \\"hermesProfile\\" FROM \\"WebUiUser\\"'))
 .then(r=>{console.log(JSON.stringify(r.rows));return c.end()})
 .catch(e=>{console.log('[]');return c.end()});
""", encoding='utf-8')
    try:
        r = subprocess.run(['node', str(jsf)], cwd=DC, capture_output=True, text=True, timeout=30)
        rows = json.loads(r.stdout.strip().splitlines()[-1])
        for row in rows:
            hp = row.get('hermesProfile')
            if hp and hp not in live:
                drift.append(f"akun RBAC {row['username']} menunjuk profil '{hp}' DI LUAR registri")
    except Exception as e:
        drift.append(f"HQ/pg tak terbaca: {str(e)[:60]} (periksa manual)")
    # 2) folder gsp-* di luar registri yang masih punya gateway-service terpasang
    profs = {p.name for p in (HOME / 'profiles').iterdir() if p.is_dir()}
    stray = sorted(p for p in profs if p.startswith('gsp-') and p not in live)
    if stray:
        drift.append(f"folder profil gsp-* di luar registri: {','.join(stray)}")
    # 3) registri menunjuk folder hilang
    gone = sorted(p for p in live if p != 'default' and not (HOME / 'profiles' / p).is_dir())
    if gone:
        drift.append(f"entri registri tanpa folder: {','.join(gone)}")
    if drift:
        print("REGISTRY-DRIFT v1:\n- " + "\n- ".join(drift))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
