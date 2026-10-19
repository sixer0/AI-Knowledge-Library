#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSP Gateway Monitor v1 (PROF-MERGE-1010, 10-10-2026).

Menggantikan gsp_fleet_gateway_check.py + gsp_gateway_watchdog.py era 52-profil.
Sumber kebenaran: fleet/PROFILE-REGISTRY.json di shared workspace (daftar hidup).
Tugas:
  1) JAGA: gateway wajib (3 worker peran-via-berkas) harus hidup; start detached bila mati.
  2) BURU: gateway 'hermes gateway run' milik profil DI LUAR daftar hidup = hantu -> hentikan.
  3) DIAM saat sehat (stdout kosong = tidak ada delivery); cetak laporan hanya bila ada aksi.
Pitfall Windows yang ditambal: MSYS pgrep buta proses native (pakai CIM), Start-Process
redirect hang pada daemon (pakai Popen DETACHED), stub python Store (jalankan via interpreter nyata).
"""
import json, os, re, subprocess, sys, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')
HERMES_VENV_PY = HOME / 'hermes-agent' / 'venv' / 'Scripts' / 'python.exe'

def registry():
    d = json.loads(REG.read_text(encoding='utf-8'))
    return set(d['hidup']), set(d['gateway_wajib_hidup'])

def ps(cmd, timeout=150):
    # TAMBALAN sysman 14-10 malam: enumerasi CIM Win32_Process bisa >90 dtk saat WMI
    # dingin/beban tinggi (ukur 14-10: 42 dtk dingin, lalu 8-20 dtk; monitor v1 mati
    # TimeoutExpired mentah dua ronde beruntun = penjaga buta sebelum menindak).
    # Plafon dinaikkan ke 150 dtk (setara audit v1.1) + satu retry; vonis tetap sama.
    last = None
    for attempt in range(2):
        try:
            r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', cmd],
                               capture_output=True, text=True, timeout=timeout)
            # TAMBALAN sysman 15-10 siang (docs/2026-10-15_gateway-monitor-blind-pass/):
            # rc!=0 dulu dianggap hasil kosong -> vonis 'semua mati' palsu. Galat PowerShell
            # kini dihitung sebagai kegagalan lintasan (retry 1x, lalu RuntimeError eksplisit).
            if r.returncode != 0:
                last = RuntimeError(f"CIM rc={r.returncode} stderr={(r.stderr or '').strip()[:200]}")
                time.sleep(3)
                continue
            return r.stdout
        except subprocess.TimeoutExpired as e:
            last = e
            time.sleep(3)
    raise RuntimeError(f"GATEWAY-MONITOR ERROR: CIM timeout 2x{timeout}s — WMI tidak responsif") from last

def heartbeat_age_s(prof):
    """Umur (detik) heartbeat gateway profil, atau None bila berkas tidak ada.
    Gateway hidup menulis state/gateway.heartbeat tiap ~30 dtk (DEFAULT_HEARTBEAT_INTERVAL_S
    di hermes-agent/gateway/shutdown_watchdog.py, terukur 15-10). Sinyal kesegaran ini TIDAK
    bergantung WMI, jadi cocok sebagai saksi kedua saat lintasan CIM mencurigai mati."""
    p = HOME / 'profiles' / prof / 'state' / 'gateway.heartbeat'
    if not p.exists() and prof == 'default':
        p = HOME / 'state' / 'gateway.heartbeat'
    if not p.exists():
        return None
    try:
        import datetime as _dt
        d = json.loads(p.read_text(encoding='utf-8'))
        ts = _dt.datetime.fromisoformat(d['updated_at'])
        return max(0.0, (_dt.datetime.now(_dt.timezone.utc) - ts).total_seconds())
    except Exception:
        return None


def live_gateways():
    # TAMBALAN sysman 14-10 malam: filter nama di sisi CIM (server-side) memangkas
    # beban enumerasi saat WMI lambat; hasil setara (terukur 8 dtk vs >150 dtk).
    q = r"""
Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'" | Where-Object { $_.CommandLine -match 'gateway run' } | ForEach-Object { "{0}|{1}" -f $_.ProcessId, ($_.CommandLine -replace '\s+',' ') }
"""
    out = {}
    for line in ps(q).splitlines():
        if '|' not in line:
            continue
        pid, cmd = line.split('|', 1)
        m = re.search(r'--profile\s+(\S+)', cmd) or re.search(r'-p\s+(\S+)', cmd)
        prof = m.group(1) if m else 'default'
        out.setdefault(prof, []).append(int(pid))
    return out

def start_gateway(prof):
    logd = HOME / 'profiles' / prof / 'logs'
    logd.mkdir(parents=True, exist_ok=True)
    logf = open(logd / 'gateway-monitor-start.log', 'ab')
    flags = getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0) | getattr(subprocess, 'DETACHED_PROCESS', 0)
    subprocess.Popen([str(HERMES_VENV_PY), '-m', 'hermes_cli.main', '--profile', prof, 'gateway', 'run'],
                     cwd=str(HOME / 'profiles' / prof), stdout=logf, stderr=logf,
                     creationflags=flags, close_fds=True)
    pid_dir = HOME / 'gateway-logs'
    pid_dir.mkdir(exist_ok=True)

def kill_pids(pids):
    if not pids:
        return
    flt = ' -or '.join(f'$_.ProcessId -eq {p}' for p in pids)
    ps('$ErrorActionPreference="SilentlyContinue"; Get-CimInstance Win32_Process | Where-Object { '
       + flt + ' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }')

def main():
    if not REG.exists():
        print(f"GATEWAY-MONITOR ERROR: registri tidak ada di {REG}")
        return 1
    live, must = registry()
    acts = []
    notes = []
    gw = live_gateways()
    # 1) jaga yang wajib
    # TAMBALAN sysman 15-10 siang (docs/2026-10-15_gateway-monitor-blind-pass/): sebelum
    # menyalakan, mintakan saksi kedua yang tidak bergantung WMI. Ronde 13:03 vonis '0 proses'
    # untuk TIGA profil serentak padahal ketiganya hidup 26 jam (heartbeat berumur <2 dtk):
    # satu lintasan CIM buta-parsial menghasilkan peta kosong, dan start_gateway hanya
    # ditahan oleh gembok instance milik profil sendiri. Tanpa saksi ini penjaga bisa
    # menyalakan ulang gateway yang sebenarnya sehat (restart massal palsu).
    for prof in sorted(must):
        n = len(gw.get(prof, []))
        if n == 0:
            hb = heartbeat_age_s(prof)
            if hb is not None and hb < 180:
                notes.append(f"SKIP {prof}: CIM melapor 0 proses tapi heartbeat {int(hb)} dtk "
                             f"-> buta-parsial, tanpa aksi")
                continue
            start_gateway(prof)
            acts.append(f"START gateway wajib {prof} (0 proses + heartbeat mati -> spawn detached)")
    # TAMBALAN sysman 15-10 pagi (docs/2026-10-15_gateway-monitor-single-pass/):
    # ukur-ulang HANYA bila ada aksi START. Sebelumnya main() SELALU memanggil
    # live_gateways() dua kali walau sehat nol aksi; dua lintasan CIM saat WMI
    # lambat (ukur 15-10: 125-278 dtk/lintasan, retry ikut termakan) = plafon
    # ronde cron tergerus dua kali lipat tanpa nilai tambah — deteksi hantu dari
    # pengukuran pertama tetap sah karena keadaan sehat berarti tidak ada proses
    # baru yang kita lahirkan. Jalur beraksi mempertahankan semantik lama utuh.
    if acts:
        time.sleep(6)
        gw = live_gateways()
    # 2) buru hantu: profil ber-gateway yang tidak ada di daftar hidup
    # TAMBALAN sysman 10-10: aturan murni registri (p not in live), tanpa filter
    # prefix — menutup blind spot profil non-prefiks pensiun (agentriset,
    # firmanhidayat, gspuser01/02 dsb). 'default' aman: ada di registri hidup.
    ghosts = {p: pids for p, pids in gw.items() if p not in live}
    if ghosts:
        allp = [pid for pids in ghosts.values() for pid in pids]
        kill_pids(allp)
        acts.append("BUNUH gateway hantu: " + ", ".join(f"{p}({len(v)})" for p, v in sorted(ghosts.items())))
    # 3) laporan hanya bila ada aksi (pola watchdog: diam = sehat)
    # Catatan SKIP ikut dicetak: penjaga yang buta-parsial BUKAN keadaan sehat — pemilik
    # harus melihatnya (instruksi ronde: jangan biarkan buta).
    if acts or notes:
        if acts:
            print("GATEWAY-MONITOR AKSI:", "; ".join(acts))
        if notes:
            print("GATEWAY-MONITOR CATATAN:", "; ".join(notes))
        gw2 = live_gateways()
        status = {m: len(gw2.get(m, [])) for m in sorted(must)}
        print("status wajib setelah aksi:", status)
    return 0

if __name__ == '__main__':
    sys.exit(main())
