#!/usr/bin/env python3
"""gsp_fleet_gateway_check.py — headless & DINAMIS (cron no_agent). v2 29-08.

Alur (permintaan user 29-08-2026):
  1. GET daftar profil   -> scan folder profiles/ + profil 'default' (OTOMATIS
                            ikut profil baru, TERMASUK yang tanpa prefix gsp-)
  2. GET profil aktif    -> 1x PowerShell enumerasi semua proses `serve`;
                            query gagal -> ABORT (JANGAN mass-restart!)
  3. Loop restart        -> spawn serve per profil yang tidak aktif (headless),
                            lalu verifikasi ulang.

PELAJARAN 29-08, DIKOREKSI 29-09 (kartu t_cd3fa1f4, preseden t_ea363bcb):
- CREATE_NO_WINDOW + DETACHED_PROCESS = kombinasi INVALID di Windows (error
  CreateProcess). Tapi asumsi lama "CREATE_NEW_PROCESS_GROUP|DETACHED_PROCESS
  terbukti tanpa jendela" SALAH untuk konteks sesi agen (git-bash/ConPTY):
  DETACHED_PROCESS saja TETAP memunculkan jendela WindowsTerminal terlihat,
  dan jendela itu tali-hidup konsol gateway (WM_CLOSE jendela membunuh
  gateway; ledger mencatat exited UNCLEANLY).
- Resep bersih terbukti 29-09: CREATE_NO_WINDOW(0x08000000)|
  CREATE_NEW_PROCESS_GROUP TANPA DETACHED_PROCESS -> 0 jendela, rantai yatim
  dari shell, gateway stabil (ticker segar, state running). NO_WINDOW saja +
  NEW_GROUP sah dan perlu; NO_WINDOW+DETACHED invalid.
- Query status gagal tidak boleh dianggap "semua down" (pernah mass-spawn 47
  serve dobel). Fail-safe: cetak error, exit 2, tanpa spawn.
"""
import datetime
import os
import re
import subprocess
import sys

HERMES_BIN = r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe"
PROFILES_DIR = r"C:\Users\TRIAL\AppData\Local\hermes\profiles"
LOG_DIR = r"C:\Users\TRIAL\.hermes\gateway-logs"
GSP_WS = r"C:\Users\TRIAL\workspace\gsp-hermes\workspace"
os.makedirs(LOG_DIR, exist_ok=True)

CREATE_NO_WINDOW = 0x08000000  # subprocess.run pendek (powershell) DAN spawn gateway
# TAMBAL 29-09 (t_cd3fa1f4): NO_WINDOW|NEW_GROUP, TANPA DETACHED_PROCESS.
# DETACHED saja dari sesi agen (git-bash/ConPTY) memunculkan jendela WT yang
# jadi tali-hidup gateway; NO_WINDOW+DETACHED invalid (CreateProcess error).
SPAWN_FLAGS = CREATE_NO_WINDOW | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

RE_PROFILE = re.compile(r"(?i)(?:-p|--profile)\s+([A-Za-z0-9_\-]+)")


def list_profiles():
    """1) GET daftar profil — dinamis: semua folder profiles/ + 'default'.

    'default' tidak punya folder (HERMES_HOME global) tapi punya serve sendiri.
    """
    names = {d for d in os.listdir(PROFILES_DIR)
             if os.path.isdir(os.path.join(PROFILES_DIR, d)) and not d.startswith(".")}
    names.add("default")
    return sorted(names)


def active_profiles():
    """2) GET profil aktif — 1 query utk semua proses serve.

    Return (set_aktif, ok). ok=False jika query gagal (stderr/timeout) —
    pemanggil WAJIB abort, bukan menganggap semuanya down.
    Profil serve TANPA -p/--profile dianggap milik 'default'.
    """
    ps = ("Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -like '*serve*' "
          "-or $_.CommandLine -like '*gateway run*') "
          "-and ($_.Name -like 'hermes*' -or $_.Name -eq 'python.exe') } | "
          "ForEach-Object { "
          "  if ($_.CommandLine -match '(?:-p|--)profile\\s+([^\\s\\\"]+)') { $Matches[1] } "
          "  elseif ($_.CommandLine -match '(?i)(^|\\s)-p\\s+([^\\s\\\"]+)') { $Matches[2] } "
          "  else { 'default' } }")
    try:
        r = subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps],
                           capture_output=True, text=True, timeout=90,
                           creationflags=CREATE_NO_WINDOW)
    except Exception as e:
        return set(), False
    if r.returncode != 0 or (r.stderr or "").strip():
        return set(), False
    names = set()
    for s in (r.stdout or "").splitlines():
        s = s.strip().strip("'\"")
        if s:
            names.add(s)
    return names, True


def start_serve(profile: str) -> int:
    """3) Spawn gateway satu profil — headless (CREATE_NO_WINDOW|NEW_GROUP,
    TANPA DETACHED_PROCESS; tambal 29-09 t_cd3fa1f4).

    KOREKSI 03-09-2026: yang di-spawn adalah `gateway run` (dispatcher kartu
    kanban hidup di gateway), BUKAN `serve` (backend dashboard saja). Pola
    env meniru Hermes_Gateway_<p>.vbs resmi: HERMES_HOME per profil +
    HERMES_GATEWAY_DETACHED=1.
    """
    home = os.path.join(PROFILES_DIR, profile) if profile != "default" else r"C:\Users\TRIAL\AppData\Local\hermes"
    logf = open(os.path.join(LOG_DIR, f"{profile}.log"), "ab")
    env = dict(os.environ)
    env["HERMES_HOME"] = home
    env["PYTHONIOENCODING"] = "utf-8"
    env["HERMES_GATEWAY_DETACHED"] = "1"
    env["VIRTUAL_ENV"] = r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent\venv"
    pp = env.get("PYTHONPATH")
    env["PYTHONPATH"] = r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent" + ((os.pathsep + pp) if pp else "")
    args = [HERMES_BIN] + ([] if profile == "default" else ["-p", profile]) + ["gateway", "run"]
    p = subprocess.Popen(args, cwd=home, env=env, stdout=logf, stderr=logf,
                         creationflags=SPAWN_FLAGS, close_fds=True)
    try:
        with open(os.path.join(LOG_DIR, f"{profile}.pid"), "w", encoding="utf-8") as f:
            f.write(str(p.pid))
    except OSError:
        pass
    return p.pid


def main():
    profiles = list_profiles()                     # 1) daftar dinamis (semua profil)
    active, ok = active_profiles()                 # 2) status aktif (1 query)
    if not ok:
        print(f"GSP Fleet Gateway Check {datetime.datetime.now():%F %T}: "
              f"FAIL query status proses — ABORT tanpa restart (fail-safe anti mass-spawn).")
        return 2
    downs = [p for p in profiles if p not in active]
    if not downs:
        return 0                                   # sehat: diam total
    started, failed = [], []
    for p in downs:                                # 3) restart yang tidak aktif
        try:
            start_serve(p)
            started.append(p)
        except Exception as e:
            failed.append(f"{p}({e})")
    # verifikasi ulang setelah grace period
    import time
    time.sleep(25)
    active2, ok2 = active_profiles()
    still = [p for p in downs if p not in active2] if ok2 else []
    print(f"GSP Fleet Gateway Check {datetime.datetime.now():%F %T}: "
          f"{len(downs)}/{len(profiles)} profil down -> start {len(started)}")
    if failed:
        print(f"  GAGAL start: {', '.join(failed)}")
    if ok2 and still:
        print(f"  BELUM AKTIF pasca-start: {', '.join(still[:12])}"
              + (f" (+{len(still)-12} lain)" if len(still) > 12 else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
