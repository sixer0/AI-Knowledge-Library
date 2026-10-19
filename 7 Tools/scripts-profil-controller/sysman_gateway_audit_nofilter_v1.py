#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit read-only gateway fleet vs PROFILE-REGISTRY — TANPA filter prefix.

Tambal blind spot monitor v1 (startswith(('gsp-','rafif'))): vonis hantu =
p not in live, murni dari registri. Read-only: tidak start/kill apa pun.
Pola buru hantu di monitor v1 juga melewatkan profil non-prefiks yang
dipensiunkan; skrip ini menutup celah itu untuk audit periodik.
"""
import json, re, subprocess, sys, pathlib

REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

def main():
    d = json.loads(REG.read_text(encoding='utf-8'))
    live = set(d['hidup'])
    must = set(d['gateway_wajib_hidup'])
    # NB: pakai raw triple-quote polos — escaping \" di dalam raw string
    # membuat PowerShell gagal parse dan mengembalikan nol baris (cacat v1.0).
    q = r"""
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(hermes|python|pythonw)\.exe$' -and $_.CommandLine -match 'gateway run' } | ForEach-Object { "{0}|{1}" -f $_.ProcessId, ($_.CommandLine -replace '\s+',' ') }
"""
    r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', q],
                       capture_output=True, text=True, timeout=120)
    procs = {}
    for line in r.stdout.splitlines():
        if '|' not in line:
            continue
        pid, cmd = line.split('|', 1)
        m = re.search(r'--profile\s+(\S+)', cmd) or re.search(r'-p\s+(\S+)', cmd)
        prof = m.group(1) if m else 'default'
        procs.setdefault(prof, []).append(int(pid))
    print('registri hidup :', len(live), '| wajib:', sorted(must))
    print('gateway terdeteksi (root+anak, mentah):')
    for p in sorted(procs):
        tag = 'OK' if p in live else 'DI-LUAR-REGISTRI'
        print(f'  {p:24s} n={len(procs[p]):2d} pids={procs[p]} [{tag}]')
    # vonis wajib: minimal 1 proses per profil wajib
    missing = sorted(m for m in must if m not in procs)
    ghosts = {p: v for p, v in procs.items() if p not in live}
    # duplikat root dicatat (audit v1 yang memvonis root; di sini sinyal mentah)
    multi = {p: v for p, v in procs.items() if p in live and len(v) > 3}
    print('WAJIB-MATI     :', missing if missing else 'none')
    print('HANTU(no-prefix):', {p: v for p, v in sorted(ghosts.items())} if ghosts else 'none')
    print('PROSES-TINGGI  :', multi if multi else 'none')
    return 0 if not missing and not ghosts else 2

if __name__ == '__main__':
    sys.exit(main())
