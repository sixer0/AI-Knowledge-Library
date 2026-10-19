#!/usr/bin/env python3
"""start_missing_gateways_0903.py — nyalakan `gateway run` headless untuk profil
yang tidak punya gateway-service VBS (agentriset, firmanhidayat, gspuser01, gspuser02).
Pola sama dengan Hermes_Gateway_<p>.vbs resmi: HERMES_HOME per profil,
HERMES_GATEWAY_DETACHED=1, proses DETACHED (tidak terikat terminal pemanggil).
"""
import os, subprocess, sys

VENV = r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
PROFILES_DIR = r"C:\Users\TRIAL\AppData\Local\hermes\profiles"
TARGETS = ["agentriset", "firmanhidayat", "gspuser01", "gspuser02"]

for p in TARGETS:
    home = os.path.join(PROFILES_DIR, p)
    if not os.path.isdir(home):
        print(f"[skip] {p}: profil tidak ada"); continue
    env = dict(os.environ)
    env["HERMES_HOME"] = home
    env["PYTHONIOENCODING"] = "utf-8"
    env["HERMES_GATEWAY_DETACHED"] = "1"
    env["VIRTUAL_ENV"] = r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent\venv"
    pp = env.get("PYTHONPATH")
    env["PYTHONPATH"] = r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent" + (os.pathsep + pp if pp else "")
    flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    proc = subprocess.Popen(
        [VENV, "-m", "hermes_cli.main", "--profile", p, "gateway", "run"],
        cwd=home, env=env, creationflags=flags, close_fds=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"[start] {p} pid={proc.pid}")
print("done")
