#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sapuan bersih read-only ronde cron 18-10 (pola sysman_gateway_cron_1015i_sweep_v1).

Vonis hantu murni registri: SATU lintasan CIM berfilter nama yang sekaligus
mengeluarkan ProcessId, ParentProcessId, CommandLine; akar dideteksi ulang tiap
ronde (tanpa pin PID); self-exclude PID sendiri + orang tua + token alat sapuan.
Tidak mengubah apa pun.
"""
import json, os, re, subprocess, sys, time, pathlib, datetime

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

Q = r"""
Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'" | Where-Object { $_.CommandLine -match 'gateway run' } | ForEach-Object { "{0}|{1}|{2}" -f $_.ProcessId, $_.ParentProcessId, ($_.CommandLine -replace '\s+',' ') }
"""


def ps(cmd, timeout=150):
    last = None
    for _ in range(2):
        try:
            r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', cmd],
                               capture_output=True, text=True, timeout=timeout)
            if r.returncode != 0:
                last = RuntimeError(f"CIM rc={r.returncode} stderr={(r.stderr or '').strip()[:200]}")
                time.sleep(3)
                continue
            return r.stdout
        except subprocess.TimeoutExpired as e:
            last = e
            time.sleep(3)
    raise RuntimeError(f"SWEEP ERROR: CIM timeout 2x{timeout}s") from last


def hb_age(prof):
    p = HOME / 'profiles' / prof / 'state' / 'gateway.heartbeat'
    if not p.exists() and prof == 'default':
        p = HOME / 'state' / 'gateway.heartbeat'
    if not p.exists():
        return None
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
        ts = datetime.datetime.fromisoformat(d['updated_at'])
        return max(0.0, (datetime.datetime.now(datetime.timezone.utc) - ts).total_seconds())
    except Exception:
        return None


def main():
    d = json.loads(REG.read_text(encoding='utf-8'))
    live = set(d['hidup'])
    must = set(d['gateway_wajib_hidup'])
    self_pids = {os.getpid(), os.getppid()}
    SELF_TOKENS = ('sysman_gateway_cron_', 'gsp_gateway_audit_v1.py', 'gsp_gateway_monitor_v1.py',
                   'sysman_audit_noWMI_v1.py', 'gsp_gateway_tree_v1.py', 'gsp_gateway_probe_v1.py')
    t0 = time.time()
    rows = []
    for line in ps(Q).splitlines():
        parts = line.split('|', 2)
        if len(parts) != 3:
            continue
        pid, ppid, cmd = parts
        if int(pid) in self_pids or int(ppid) in self_pids:
            continue
        if any(tok in cmd for tok in SELF_TOKENS):
            continue
        if 'gateway run' not in cmd:
            continue
        m = re.search(r'--profile\s+(\S+)', cmd) or re.search(r'-p\s+(\S+)', cmd)
        rows.append((m.group(1) if m else 'default', int(pid), int(ppid)))
    allp = {p for _, p, _ in rows}
    by = {}
    for prof, pid, ppid in rows:
        by.setdefault(prof, []).append((pid, ppid))
    print(f"SWEEP BERSIH {datetime.datetime.now().isoformat(timespec='seconds')} "
          f"(lintasan {time.time()-t0:.0f} dtk, {len(rows)} proses 'gateway run')")
    ghosts = []
    for prof in sorted(by):
        roots = [p for p, pp in by[prof] if pp not in allp]
        tag = 'hidup-di-registri' if prof in live else 'HANTU-DI-LUAR-DAFTAR'
        if prof not in live:
            ghosts.append(prof)
        print(f"  {prof:<22} root={len(roots)} pids={[p for p,_ in sorted(by[prof])]} {tag}")
    print('--- saksi heartbeat (non-WMI) ---')
    for m in sorted(must):
        print(f"  {m:<22} heartbeat={hb_age(m)}")
    print('VONIS:', 'BERSIH (nol hantu)' if not ghosts else f'HANTU={ghosts}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
