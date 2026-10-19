#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSP Gateway AUDIT v2-psutil (read-only, ronde cron 14-10b).

Motif: WMI/CimInstance host sedang sangat lambat (query trivial 43 dtk, enumerasi
penuh >60 dtk) sehingga pola CIM pada gsp_gateway_audit_v1.py/monitor v1 tidak
lagi andal. Alat ini memakai psutil (tanpa WMI) dengan SEMANTIK VONIS IDENTIK
audit v1.1: root = proses 'gateway run' yang parent-nya bukan proses gateway run
lain; registri = sumber tunggal daftar hidup.
"""
import json, re, sys, time, datetime, pathlib
import psutil

REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')


def main():
    t0 = time.time()
    d = json.loads(REG.read_text(encoding='utf-8'))
    live, must = set(d['hidup']), set(d['gateway_wajib_hidup'])

    runs = []   # (prof, pid, ppid)
    for p in psutil.process_iter(['pid', 'ppid', 'name', 'cmdline']):
        try:
            name = (p.info['name'] or '').lower()
            if name not in ('hermes.exe', 'python.exe', 'pythonw.exe'):
                continue
            cmd = ' '.join(p.info['cmdline'] or [])
            if 'gateway run' not in cmd:
                continue
            m = re.search(r'--profile\s+(\S+)', cmd) or re.search(r'-p\s+(\S+)', cmd)
            prof = m.group(1) if m else 'default'
            runs.append((prof, p.info['pid'], p.info['ppid']))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    all_pids = {pid for _, pid, _ in runs}
    by_prof = {}
    for prof, pid, ppid in runs:
        by_prof.setdefault(prof, []).append((pid, ppid))

    print(f"=== AUDIT GATEWAY (psutil, tanpa WMI) {datetime.datetime.now().isoformat(timespec='seconds')} ===")
    print(f"registri hidup: {len(live)} | wajib gateway: {sorted(must)} | durasi_ukur={time.time()-t0:.1f}s")
    for prof in sorted(by_prof):
        roots = [p for p, pp in by_prof[prof] if pp not in all_pids]
        tag = "HIDUP" if prof in live else "DI-LUAR-DAFTAR-HIDUP"
        print(f"  {prof:<22} proses={len(by_prof[prof]):<2} root={len(roots)} pids={[p for p,_ in sorted(by_prof[prof])]} {tag}")

    mati, hantu, ganda = [], [], []
    print("--- vonis ---")
    for m_ in sorted(must):
        roots = [p for p, pp in by_prof.get(m_, []) if pp not in all_pids]
        if not roots:
            mati.append(m_)
            print(f"  WAJIB {m_:<20} root=0 -> MATI")
        elif len(roots) > 1:
            ganda.append((m_, roots))
            print(f"  WAJIB {m_:<20} root={len(roots)} -> GANDA")
        else:
            print(f"  WAJIB {m_:<20} root=1 -> OK")
    for prof in sorted(by_prof):
        if prof not in live:
            hantu.append(prof)
            print(f"  HANTU {prof:<20} pids={[p for p,_ in by_prof[prof]]}")
    ok = not mati and not hantu and not ganda
    print("VERDICT:", "SEHAT" if ok else f"PERLU-AKSI (mati={mati}, hantu={hantu}, ganda={[g[0] for g in ganda]})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
