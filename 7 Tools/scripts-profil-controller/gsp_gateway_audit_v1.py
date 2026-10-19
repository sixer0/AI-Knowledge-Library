#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSP Gateway AUDIT v1.1 (read-only, milik System Manager).

Bukan pengganti monitor: alat ukur INDEPENDEN untuk membuktikan vonis monitor.
Tidak mengubah apa pun.

v1.1 (sysman 10-10): vonis "GANDA" dihitung dari INSTANS INDEPENDEN (root = proses
yang parent-nya bukan proses gateway lain), BUKAN jumlah proses mentah. Alasan:
`hermes gateway run`spawn rantai anak (wrapper -> python -> worker) sehingga n>1
per profil itu NORMAL; yang berbahaya hanya >1 root (rebutan port/konsumen pesan).
Baris tanpa 'gateway run' pada command line dilaporkan terpisah sebagai catatan.
"""
import json, os, re, subprocess, sys, time, pathlib, datetime

REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

Q = r"""
Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'" | Where-Object { $_.CommandLine -match 'gateway' } | ForEach-Object { "{0}|{1}|{2}|{3}" -f $_.ProcessId, $_.ParentProcessId, $_.Name, ($_.CommandLine -replace '\s+',' ') }
"""


def ps(cmd, timeout=150):
    # TAMBALAN sysman 14-10 malam: enumerasi CIM TANPA filter nama menembus plafon
    # saat WMI lambat (terukur >150 dtk). Query kini berfilter nama (setara hasil,
    # terukur 8 dtk) + satu retry; kegagalan dua kali = pesan eksplisit, bukan
    # traceback mentah.
    last = None
    for attempt in range(2):
        try:
            r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', cmd],
                               capture_output=True, text=True, timeout=timeout)
            return r.stdout
        except subprocess.TimeoutExpired as e:
            last = e
            time.sleep(3)
    raise RuntimeError(f"AUDIT ERROR: CIM timeout 2x{timeout}s — WMI tidak responsif") from last


def main():
    if not REG.exists():
        print("AUDIT ERROR: registri tidak ada:", REG)
        return 1
    d = json.loads(REG.read_text(encoding='utf-8'))
    live = set(d['hidup'])
    must = set(d['gateway_wajib_hidup'])

    # TAMBALAN sysman 16-10 (ronde zg): alat ini SENDIRI mengandung token 'gateway'
    # pada path scriptnya dan tidak punya '--profile', sehingga masuk CATATAN sebagai
    # profil 'default' (vonis palsu; preseden kelas buru-hantu broadsweep 11-10).
    # Self-exclude: PID sendiri + orang tua langsung + token nama alat audit/sapuan.
    self_pids = {os.getpid(), os.getppid()}
    SELF_TOKENS = ('gsp_gateway_audit_v1.py', 'sysman_gateway_cron_', 'sysman_gateway_audit',
                   'gsp_gateway_monitor_v1.py', 'sysman_audit_noWMI_v1.py', 'gsp_gateway_tree_v1.py',
                   'gsp_gateway_probe_v1.py')

    runs, notes = [], []
    for line in ps(Q).splitlines():
        parts = line.split('|', 3)
        if len(parts) != 4:
            continue
        pid, ppid, name, cmd = parts
        if int(pid) in self_pids or int(ppid) in self_pids:
            continue
        if any(tok in cmd for tok in SELF_TOKENS):
            continue
        m = re.search(r'--profile\s+(\S+)', cmd) or re.search(r'-p\s+(\S+)', cmd)
        prof = m.group(1) if m else 'default'
        if 'gateway run' in cmd:
            runs.append((prof, int(pid), int(ppid)))
        else:
            notes.append((prof, int(pid), cmd[:120]))

    all_pids = {p for _, p, _ in runs}
    by_prof = {}
    for prof, pid, ppid in runs:
        by_prof.setdefault(prof, []).append((pid, ppid))

    print("=== AUDIT GATEWAY FLEET", datetime.datetime.now().isoformat(timespec='seconds'), "===")
    print(f"registri hidup: {len(live)} | wajib gateway: {sorted(must)}")
    print("--- proses 'gateway run' per profil (root = instans independen) ---")
    for prof in sorted(by_prof):
        roots = [p for p, pp in by_prof[prof] if pp not in all_pids]
        tag = "HIDUP" if prof in live else "DI-LUAR-DAFTAR-HIDUP"
        print(f"  {prof:<22} proses={len(by_prof[prof]):<2} root={len(roots)} pids={[p for p,_ in sorted(by_prof[prof])]} {tag}")
    if not by_prof:
        print("  (tidak ada proses 'gateway run' terdeteksi)")

    print("--- vonis ---")
    mati, hantu, ganda = [], [], []
    for m in sorted(must):
        roots = [p for p, pp in by_prof.get(m, []) if pp not in all_pids]
        if not roots:
            mati.append(m)
            print(f"  WAJIB {m:<20} root=0 -> MATI (monitor harus start)")
        elif len(roots) > 1:
            ganda.append((m, roots))
            print(f"  WAJIB {m:<20} root={len(roots)} {roots} -> GANDA (instans duplikat nyata)")
        else:
            print(f"  WAJIB {m:<20} root=1 -> OK")
    for prof in sorted(by_prof):
        if prof not in live:
            hantu.append(prof)
            print(f"  HANTU {prof:<20} pids={[p for p,_ in by_prof[prof]]} -> di luar daftar hidup, hentikan")
    for prof in sorted({p for p, _, _ in notes}):
        print(f"  CATATAN {prof:<18} proses ber-'gateway' tanpa 'gateway run' (bukan target buru): "
              f"{[(p, c[:60]) for pp, p, c in notes if pp == prof]}")

    ok = not mati and not hantu and not ganda
    print("VERDICT:", "SEHAT" if ok else
          f"PERLU-AKSI (wajib_mati={mati}, hantu={hantu}, ganda={[g[0] for g in ganda]})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
