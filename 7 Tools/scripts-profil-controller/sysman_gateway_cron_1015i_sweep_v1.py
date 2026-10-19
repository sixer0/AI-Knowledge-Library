#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron sysman 15-10 ronde i: sapuan gateway read-only (audit + akar + hantu), satu lintasan CIM.

Pola kanonis gabungan pelajaran ronde 14-10/15-10:
- SATU query Get-CimInstance berfilter nama server-side (python*/hermes.exe) -> tahan WMI lambat.
- Vonis berbasis AKAR (parent bukan 'gateway run'), bukan jumlah proses mentah (rantai anak normal).
- Deteksi ulang akar tiap ronde; TANPA PID di-hardcode dari ronde sebelumnya.
- Self-exclude PID sendiri + token alat sapuan; wajib literal 'gateway run'.
- Bandingkan terhadap registri penuh tanpa filter prefix (registri = sumber tunggal).
"""
import json, os, re, subprocess, sys, time, datetime, pathlib

REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')
PROF_RE = re.compile(r"(?:--profile|-p)\s+(\S+)")
CMD = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'\" | "
       "ForEach-Object { if ($_.CommandLine -match 'gateway run') { "
       "$_.ProcessId.ToString() + '|' + $_.ParentProcessId.ToString() + '|' + "
       "$_.CreationDate.ToString('yyyy-MM-dd HH:mm:ss') + '|' + $_.CommandLine } }")


def cim(timeout=150):
    last = None
    for _ in range(2):
        try:
            r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', CMD],
                               capture_output=True, text=True, timeout=timeout)
            return r.stdout
        except subprocess.TimeoutExpired as e:
            last = e
            time.sleep(3)
    raise RuntimeError(f"CIM timeout 2x{timeout}s - WMI tidak responsif") from last


def main():
    if not REG.exists():
        print("ERROR: registri tidak ada:", REG)
        return 1
    d = json.loads(REG.read_text(encoding='utf-8'))
    live = set(d['hidup'])
    must = set(d['gateway_wajib_hidup'])

    t0 = time.time()
    out = cim()
    rows = []
    for line in out.splitlines():
        parts = line.split('|', 3)
        if len(parts) != 4:
            continue
        pid, ppid, created, cmd = parts
        low = cmd.lower()
        # self-exclude + alat sapuan/penjaga lama agar tidak jadi hantu palsu
        if int(pid) == os.getpid():
            continue
        if any(tok in low for tok in ('broadsweep', 'rootage', 'sweep_v1', 'monitor_v1', 'audit_v1', 'ghostcheck')):
            continue
        if 'gateway run' not in low:
            continue
        rows.append((int(pid), int(ppid), created.strip(), cmd))
    print(f"CIM satu lintasan: {len(rows)} proses 'gateway run' dalam {time.time()-t0:.0f} dtk")
    by_pid = {p[0]: p for p in rows}

    now = datetime.datetime.now()
    roots = {}
    counts = {}
    for pid, ppid, created, cmd in rows:
        m = PROF_RE.search(cmd)
        prof = m.group(1) if m else 'default'
        counts.setdefault(prof, []).append(pid)
        is_root = not (ppid in by_pid and 'gateway run' in by_pid[ppid][3].lower())
        if is_root:
            try:
                ct = datetime.datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
                age_h = (now - ct).total_seconds() / 3600
            except ValueError:
                age_h = -1
            roots.setdefault(prof, []).append((pid, age_h))

    print("--- profil ber-gateway (n_proses / n_akar) vs registri ---")
    fail = 0
    for prof in sorted(counts):
        tag = "HIDUP" if prof in live else "DI-LUAR-DAFTAR"
        nr = len(roots.get(prof, []))
        ages = ", ".join(f"{a:.1f}j" for _, a in roots.get(prof, []))
        print(f"  {prof:<22} n={len(counts[prof]):<2} root={nr:<2} umur_akar=[{ages}] {tag}")

    print("--- vonis wajib ---")
    for mprof in sorted(must):
        nr = len(roots.get(mprof, []))
        v = "OK" if nr >= 1 else "MATI"
        if nr < 1:
            fail += 1
        print(f"  WAJIB {mprof:<18} root={nr} -> {v}")
    ghosts = sorted(p for p in counts if p not in live)
    dupes = sorted(p for p, r in roots.items() if len(r) > 1)
    for g in ghosts:
        print(f"  HANTU {g:<18} pids={counts[g]}")
    for p in dupes:
        print(f"  GANDA {p:<18} roots={roots[p]}")
    print("VERDICT:", "SEHAT" if fail == 0 and not ghosts else
          f"PERLU-AKSI (wajib_mati={fail}, hantu={len(ghosts)})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
