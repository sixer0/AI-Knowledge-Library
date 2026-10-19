#!/usr/bin/env python3
"""gsp_gateway_watchdog.py — pastikan SEMUA profil gsp-* hidup & bisa di-dispatch (Windows).

Pola watchdog: DIAM saat sehat; hanya output jika ada aksi (restart).
MODE default : cek + start yang mati. --restart : stop semua lalu start ulang.

KOREKSI LAPISAN (03-09-2026, arahan user): lapisan delegasi yang benar adalah
`hermes -p <profil> gateway run` — dispatcher kartu kanban hidup di gateway
(kanban.dispatch_in_gateway default True, lock singleton machine-global).
Proses `serve` hanya backend JSON-RPC untuk dashboard desktop dan TIDAK
mengklaim kartu; pola lama serve-only terbukti menyalakan 150 proses tanpa
menaikkan throughput delegasi. Deteksi & spawn kini menyasar `gateway run`.
Spawn meniru Hermes_Gateway_<p>.vbs resmi: HERMES_HOME per profil +
HERMES_GATEWAY_DETACHED=1 + DETACHED_PROCESS (headless, tak terikat terminal).
"""
import json
import os
import re
import subprocess
import sys
import time

HERMES_BIN = r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe"
PYTHON_BIN = r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
PROFILES_DIR = r"C:\Users\TRIAL\AppData\Local\hermes\profiles"
HERMES_AGENT = r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent"
GSP_WS = r"C:\Users\TRIAL\workspace\gsp-hermes\workspace"
LOG_DIR = r"C:\Users\TRIAL\.hermes\gateway-logs"
os.makedirs(LOG_DIR, exist_ok=True)

RESTART = "--restart" in sys.argv
VERBOSE = "--verbose" in sys.argv

# CARA COCOK (03-09-2026): gateway diluncurkan `-p <profil> gateway run` (VBS)
# atau `-m hermes_cli.main --profile <profil> gateway run` (skrip ad-hoc).
PS_FILTER = ("Get-CimInstance Win32_Process | Where-Object {{ $_.CommandLine -match '(?i)(-p|--profile)\\s+{p}\\b' -and "
             "$_.CommandLine -like '*gateway run*' -and ($_.Name -like 'hermes*' -or $_.Name -eq 'python.exe') }} | "
             "Measure-Object | Select-Object -ExpandProperty Count")


def serve_count(profile: str) -> int:
    try:
        out = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", PS_FILTER.format(p=profile)],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        return int(out or 0)
    except Exception:
        return 0


def stop_serve_processes(profile: str) -> int:
    """Stop semua proses gateway untuk profil (mode --restart)."""
    ps = ("Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match '(?i)(-p|--profile)\\s+{p}\\b' -and "
          "$_.CommandLine -like '*gateway run*' -and ($_.Name -like 'hermes*' -or $_.Name -eq 'python.exe') } | "
          "ForEach-Object {{ Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }}")
    subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps.format(p=profile)],
                   capture_output=True, text=True, timeout=60)
    time.sleep(2)
    return serve_count(profile)


def start_serve(profile: str) -> int:
    """Spawn `gateway run` headless per profil (pola VBS resmi, detached)."""
    home = os.path.join(PROFILES_DIR, profile)
    env = dict(os.environ)
    env["HERMES_HOME"] = home
    env["PYTHONIOENCODING"] = "utf-8"
    env["HERMES_GATEWAY_DETACHED"] = "1"
    env["VIRTUAL_ENV"] = os.path.join(HERMES_AGENT, "venv")
    pp = env.get("PYTHONPATH")
    env["PYTHONPATH"] = HERMES_AGENT + (os.pathsep + pp if pp else "")
    logf = open(os.path.join(LOG_DIR, f"{profile}.log"), "ab")
    flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    p = subprocess.Popen(
        [PYTHON_BIN, "-m", "hermes_cli.main", "--profile", profile, "gateway", "run"],
        cwd=home, env=env, stdout=logf, stderr=logf, creationflags=flags, close_fds=True,
    )
    # Tulis PID ke file yang dibaca dashboard HQ (~/.hermes/gateway-logs/<profil>.pid)
    try:
        pidf = os.path.join(LOG_DIR, f"{profile}.pid")
        with open(pidf, "w", encoding="utf-8") as f:
            f.write(str(p.pid))
    except OSError:
        pass
    return p.pid



def main():
    profiles = sorted(d for d in os.listdir(PROFILES_DIR) if d.startswith("gsp-"))
    if not profiles:
        print("gsp_gateway_watchdog: tidak ada profil gsp-*")
        return 1
    actions = []
    if RESTART:
        for p in profiles:
            n = serve_count(p)
            if n > 0:
                stop_serve_processes(p)
                actions.append(f"[stop] {p} (was {n})")
        time.sleep(3)
    for p in profiles:
        n = serve_count(p)
        if n > 0:
            if VERBOSE:
                print(f"[ok] {p} ({n} serve)")
            continue
        pid = start_serve(p)
        actions.append(f"[start] {p} pid={pid}")
        time.sleep(1)
    if actions:
        print("GSP fleet watchdog:", " | ".join(actions))
    else:
        if VERBOSE:
            print(f"GSP fleet watchdog: semua {len(profiles)} profil sehat (diam)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
