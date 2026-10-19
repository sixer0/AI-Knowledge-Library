#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sapuan hantu gateway ronde cron 18-10 (read-only).

Bedanya dari gsp_gateway_audit_v1.py: filter CIM server-side pada CommandLine
(bukan pada nama proses), sehingga interpreter apa pun yang menjalankan
'gateway run' ikut terlihat. Self-exclude PID sendiri + token alat sapuan
(preseden buru-hantu broadsweep 11-10 dan CATATAN audit 16-10).
"""
import json, os, re, subprocess, sys, time, pathlib, datetime

REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

Q = r"""
Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%gateway%run%'" | ForEach-Object { "{0}|{1}|{2}|{3}" -f $_.ProcessId, $_.ParentProcessId, $_.Name, ($_.CommandLine -replace '\s+',' ') }
"""

SELF_TOKENS = ('sysman_gateway_cron_1018b_ghost_v1.py', 'gsp_gateway_audit_v1.py',
               'gsp_gateway_monitor_v1.py', 'sysman_gateway_cron_', 'broadsweep',
               'sysman_audit_noWMI_v1.py', 'gsp_gateway_tree_v1.py')


def ps(cmd, timeout=150):
    last = None
    for _ in range(2):
        try:
            r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', cmd],
                               capture_output=True, text=True, timeout=timeout)
            if r.returncode != 0:
                raise RuntimeError(f"CIM rc={r.returncode}: {r.stderr[:200]}")
            return r.stdout
        except (subprocess.TimeoutExpired, RuntimeError) as e:
            last = e
            time.sleep(3)
    raise RuntimeError(f"GHOST ERROR: lintasan CIM gagal 2x — {last}") from last


def main():
    d = json.loads(REG.read_text(encoding='utf-8'))
    live = set(d['hidup'])
    must = set(d['gateway_wajib_hidup'])
    self_pids = {os.getpid(), os.getppid()}

    t0 = time.time()
    out = ps(Q)
    rows = []
    for line in out.splitlines():
        parts = line.split('|', 3)
        if len(parts) != 4:
            continue
        pid, ppid, name, cmd = parts
        if int(pid) in self_pids or int(ppid) in self_pids:
            continue
        if any(tok in cmd for tok in SELF_TOKENS):
            continue
        if 'gateway run' not in cmd:
            continue
        m = re.search(r'--profile\s+(\S+)', cmd) or re.search(r'-p\s+(\S+)', cmd)
        prof = m.group(1) if m else 'default'
        rows.append((prof, int(pid), int(ppid), name))

    all_pids = {p for _, p, _, _ in rows}
    by = {}
    for prof, pid, ppid, name in rows:
        by.setdefault(prof, []).append((pid, ppid, name))

    print("=== SAPUAN HANTU GATEWAY", datetime.datetime.now().isoformat(timespec='seconds'),
          f"(lintasan {time.time()-t0:.0f} dtk, {len(rows)} proses 'gateway run') ===")
    hantu, ganda, mati = [], [], []
    for prof in sorted(by):
        roots = [p for p, pp, _ in by[prof] if pp not in all_pids]
        names = sorted({n for _, _, n in by[prof]})
        tag = "hidup" if prof in live else ">>> DI-LUAR-DAFTAR-HIDUP"
        print(f"  {prof:<22} proses={len(by[prof])} root={len(roots)} exe={names} {tag}")
        if prof not in live:
            hantu.append(prof)
        if len(roots) > 1:
            ganda.append((prof, roots))
    for m in sorted(must):
        roots = [p for p, pp, _ in by.get(m, []) if pp not in all_pids]
        if not roots:
            mati.append(m)
            print(f"  WAJIB {m:<20} root=0 -> MATI")
    print("VONIS:", "BERSIH (0 hantu, 0 ganda, 0 wajib mati)"
          if not (hantu or ganda or mati) else
          f"PERLU-AKSI hantu={hantu} ganda={[g[0] for g in ganda]} wajib_mati={mati}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
