#!/usr/bin/env python3
"""gsp_orchestration_distribution_audit.py — audit deterministik distribusi
sistem orkestrasi era PMODE-1010 ke seluruh profil hidup + akun RBAC.

Cakupan (semua读数 dari disk/DB pada giliran jalan; nol ingatan):
  A. PROFILE-REGISTRY hidup vs direktori profil di disk (dua arah).
  B. Akun RBAC HQ (WebUiUser) -> profil target: ada? hidup?
  C. SOUL tiap profil hidup: marker PMODE-1010; blok lane yang benar
     (controller -> 'cabang MODE'/GATE ENFORCEMENT controller; pekerja ->
     LAN-PEKERJA + GERBANG-ACK + FAST-VERIF).
  D. Trio skill orkestrasi: hash sha256[:16] kanonik-ws vs registry-fleet
     vs mirror-repo vs salinan fisik profil (bila ada); visibilitas
     per profil via jalur registry (katalog skills/gsp).
  E. Berkas peran RT/TA + guard LOCK + wake-scan + deleg-watch hadir dan
     hash-nya tercatat.

Exit 0 = VERDICT PASS (nol defect); 1 = VERDICT FAIL; 2 = salah pakai.
Read-only total: tidak menulis papan, tidak mengubah berkas.
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys

HOME = r'C:/Users/TRIAL/AppData/Local/hermes'
WS = r'C:/Users/TRIAL/workspace/gsp-hermes/workspace'
PROF_DIR = f'{HOME}/profiles'
REGISTRY = f'{HOME}/skills/gsp'
CANON_WS = r'C:/Users/TRIAL/workspace/gsp-hermes/skills'
REPO_MIRROR = r'C:/Users/TRIAL/gsp-agent/hermes-home/skills/gsp'
SKILLS = ['gsp-orchestrator-worker', 'gsp-orchestration-execution',
          'gsp-task-architect-templates']
WORKER_TRIO = ('gsp-thinker', 'gsp-worker', 'gsp-worker-fast')
PEKERJA_EXTRA = ('gsp-librarian', 'gsp-custodian')


def sha16(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


def read(path):
    try:
        with open(path, encoding='utf-8', errors='ignore') as fh:
            return fh.read()
    except OSError:
        return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--registry-json',
                    default=f'{WS}/fleet/PROFILE-REGISTRY.json')
    ap.add_argument('--env-file', default=r'C:/Users/TRIAL/gsp-datacenter/.env')
    args = ap.parse_args()

    defects = []
    notes = []

    # A. registry vs disk
    reg = json.load(open(args.registry_json, encoding='utf-8'))
    living = list(reg['hidup'])
    disk = sorted(d for d in os.listdir(PROF_DIR)
                  if os.path.isdir(os.path.join(PROF_DIR, d)))
    only_reg = [p for p in living if p != 'default' and p not in disk]
    only_disk = [p for p in disk if p not in living]
    for p in only_reg:
        defects.append(f'A: profil di registry tapi tak ada di disk: {p}')
    for p in only_disk:
        defects.append(f'A: profil di disk tapi tak terdaftar hidup: {p}')
    notes.append(f'A: hidup={len(living)} disk={len(disk)} '
                 f'selisih={len(only_reg)+len(only_disk)}')

    # B. RBAC accounts
    try:
        import psycopg2
        envf = read(args.env_file)
        m = re.search(r'^(?:export )?DATABASE_URL="?([^"\n]+)"?', envf, re.M)
        conn = psycopg2.connect(m.group(1))
        cur = conn.cursor()
        cur.execute('SELECT username, role, "hermesProfile" FROM "WebUiUser"')
        accounts = cur.fetchall()
        conn.close()
        for user, role, prof in accounts:
            if prof not in living:
                defects.append(f'B: akun RBAC {user} ({role}) -> profil '
                               f'tidak hidup/tak terdaftar: {prof}')
        notes.append(f'B: akun RBAC={len(accounts)} semua->profil hidup '
                     f'={all(p in living for _, _, p in accounts)}')
    except Exception as exc:  # noqa: BLE001
        defects.append(f'B: probe RBAC gagal: {exc}')

    # C. SOUL per profil hidup
    for prof in living:
        sp = (f'{HOME}/SOUL.md' if prof == 'default'
              else f'{PROF_DIR}/{prof}/SOUL.md')
        t = read(sp)
        if not t:
            defects.append(f'C: SOUL hilang: {prof}')
            continue
        if 'PMODE-1010' not in t:
            defects.append(f'C: SOUL {prof} tanpa marker PMODE-1010')
        if prof in WORKER_TRIO or prof in PEKERJA_EXTRA:
            for tok, label in (('LANE PEKERJA', 'lane-pekerja'),
                               ('GERBANG-ACK', 'ack-dua-arah'),
                               ('FAST-VERIF', 'fast-verif')):
                if tok not in t:
                    defects.append(f'C: SOUL pekerja {prof} tanpa {label}')
            if 'Mikro-VERIF subagen' not in t and 'Mikro-VERIF' not in t:
                defects.append(f'C: SOUL pekerja {prof} tanpa mikro-verif')
        else:  # controller lane
            if not re.search(r'cabang MODE|Cabang MODE|MODE: DIRECT', t):
                defects.append(f'C: SOUL controller {prof} tanpa blok MODE')

    # D. trio skill: hash kanal + visibilitas
    for s in SKILLS:
        cw = f'{CANON_WS}/{s}/SKILL.md'
        rf = f'{REGISTRY}/{s}/SKILL.md'
        rm = f'{REPO_MIRROR}/{s}/SKILL.md'
        hs = {}
        for label, path in (('kanonik', cw), ('registry', rf), ('repo', rm)):
            if os.path.isfile(path):
                hs[label] = sha16(path)
            else:
                defects.append(f'D: {s} hilang di kanal {label}')
        uniq = set(hs.values())
        if len(uniq) > 1:
            defects.append(f'D: {s} beda-hash antar kanal: {hs}')
        # salinan orphan di tier repo mirror (jalur lama apa pun di bawah hermes-home/skills)
        for root, dirs, files in os.walk(r'C:/Users/TRIAL/gsp-agent/hermes-home/skills'):
            if 'SKILL.md' in files and os.path.basename(root) == s:
                cand = os.path.join(root, 'SKILL.md').replace('\\', '/')
                if '/skills/gsp/' not in cand:
                    h = sha16(cand)
                    if hs.get('kanonik') and h != hs['kanonik']:
                        defects.append(f'D: orphan repo {cand} basi ({h} != {hs["kanonik"]})')
        # salinan fisik profil (bukan registry bersama)
        for prof in living:
            base = (f'{HOME}/skills' if prof == 'default'
                    else f'{PROF_DIR}/{prof}/skills')
            for cand in (f'{base}/{s}/SKILL.md', f'{base}/gsp/{s}/SKILL.md'):
                if os.path.isfile(cand) and 'skills/gsp/' not in cand.replace('\\', '/'):
                    h = sha16(cand)
                    if hs.get('kanonik') and h != hs['kanonik']:
                        defects.append(f'D: salinan {prof} {s} basi '
                                       f'({h} != {hs["kanonik"]})')
        notes.append(f'D: {s} ' + ' '.join(f'{k}={v[:8]}' for k, v in hs.items()))

    # F. visibilitas trio per profil hidup via CLI resmi (bukti enabled nyata,
    #    bukan asumsi registry; preseden BAKU-DIST FAIL-2 10-10: env HERMES_PROFILE
    #    tidak dihormati `hermes skills list` -> wajib flag -p)
    import subprocess as _sp
    hb = r'C:/Users/TRIAL/AppData/Local/hermes/hermes-agent/venv/Scripts/hermes.exe'
    if os.environ.get('AUDIT_SKIP_CLI'):
        notes.append('F: dilewati (AUDIT_SKIP_CLI=1)')
    else:
        for prof in living:
            cmd = [hb] + ([] if prof == 'default' else ['-p', prof]) + \
                  ['skills', 'list', '--enabled-only']
            try:
                rr = _sp.run(cmd, capture_output=True, text=True, timeout=60,
                             env={**os.environ, 'COLUMNS': '300'})
                out = rr.stdout or ''
                miss = [s for s in SKILLS if s not in out]
                for s in miss:
                    defects.append(f'F: {prof} tidak enabled utk {s}')
            except Exception as exc:  # noqa: BLE001
                defects.append(f'F: probe CLI {prof} gagal: {exc}')
        notes.append('F: probe CLI enabled-only per profil hidup selesai')

    # E. instrumen + berkas peran
    for label, path in (
            ('peran-RT', f'{WS}/roles/gsp-request-translator.md'),
            ('peran-TA', f'{WS}/roles/gsp-task-architect.md'),
            ('guard-LOCK', f'{HOME}/scripts/gsp_wave_lock_guard.py'),
            ('wake-scan', f'{HOME}/scripts/gsp_mission_wake_scan.py'),
            ('deleg-watch', f'{HOME}/scripts/gsp_deleg_watch.py')):
        if os.path.isfile(path):
            notes.append(f'E: {label} sha16={sha16(path)} '
                         f'bytes={os.path.getsize(path)}')
        else:
            defects.append(f'E: instrumen hilang: {label} @ {path}')

    print('NOTES:')
    for n in notes:
        print('  ', n)
    if defects:
        print(f'DEFECTS ({len(defects)}):')
        for d in defects:
            print('  -', d)
        print('VERDICT: FAIL')
        return 1
    print('DEFECTS: 0')
    print('VERDICT: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
