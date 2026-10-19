#!/usr/bin/env python3
"""GSP Watchdog — Brahma WebUI (9012) & Agent HQ (9011).
Pola watchdog: DIAM saat sehat; hanya output/restart jika ada layanan mati.
Dijalankan cron no_agent tiap 3 jam (Python — tidak bergantung PATH/bash)."""
import datetime
import os
import socket
import ssl
import subprocess
import time
import urllib.request

ECODIR = r"C:\Users\TRIAL\gsp-ecosystem"
LOG = os.path.join(ECODIR, "watchdog.log")

# HEADLESS (29-08-2026): subprocess.run jangka pendek wajib CREATE_NO_WINDOW.
# PENTING (koreksi 29-08): JANGAN gabungkan DETACHED_PROCESS + CREATE_NO_WINDOW
# untuk Popen detached — kombinasi invalid di Windows 11, console tetap
# dialokasikan dan muncul sebagai panel Windows Terminal. Spawn latar cukup
# DETACHED_PROCESS (lihat SPAWN_FLAGS).
CREATE_NO_WINDOW = 0x08000000
QUERY_FLAGS = CREATE_NO_WINDOW
SPAWN_FLAGS = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def log(msg: str) -> None:
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now():%F %T}] {msg}\n")


def http_ok(url: str, timeout: int = 10) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout, context=SSL_CTX) as r:
            return 200 <= r.status < 400
    except Exception:
        return False


def port_alive(port: int) -> bool:
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect(("127.0.0.1", port))
        return True
    except Exception:
        return False
    finally:
        s.close()


def spawn(cmd: list, cwd: str, logfile: str):
    logf = open(logfile, "ab")
    flags = SPAWN_FLAGS  # DETACHED saja — DETACHED+NO_WINDOW invalid (panel muncul)
    return subprocess.Popen(cmd, cwd=cwd, stdout=logf, stderr=logf,
                            creationflags=flags, close_fds=True)


def wait_http(url: str, tries: int, delay: int) -> bool:
    for _ in range(tries):
        if http_ok(url, 5):
            return True
        time.sleep(delay)
    return False


def load_env(path: str) -> dict:
    env = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return env


started = []

# ── Brahma WebUI (9012, HTTPS self-signed) ─────────────────────────────────
if http_ok("https://127.0.0.1:9012/health"):
    log("webui OK")
elif port_alive(9012):
    log("webui: port hidup tapi health gagal (mungkin masih booting)")
else:
    log("webui DOWN -> restart")
    env = os.environ.copy()
    env.update(load_env(r"C:\Users\TRIAL\gsp-brahma\.env"))
    py = env.get("HERMES_WEBUI_PYTHON", r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe")
    logf = os.path.join(ECODIR, "webui.log")
    logf = open(logf, "ab")
    flags = SPAWN_FLAGS  # DETACHED saja — DETACHED+NO_WINDOW invalid (panel muncul)
    p = subprocess.Popen(
        [py, "bootstrap.py", "--no-browser", "--foreground", "--host", "0.0.0.0", "9012"],
        cwd=r"C:\Users\TRIAL\gsp-brahma", env=env, stdout=logf, stderr=logf,
        creationflags=flags, close_fds=True,
    )
    started.append(f"webui(pid {p.pid})")
    log("webui pulih" if wait_http("https://127.0.0.1:9012/health", 12, 5) else "webui belum pulih dalam 60s")

# ── Agent HQ (9011, HTTPS self-signed) ─────────────────────────────────────
if http_ok("https://localhost:9011/"):
    log("hq OK")
elif port_alive(9011):
    log("hq: port hidup tapi health gagal (mungkin masih booting)")
else:
    log("hq DOWN -> restart")
    node = r"C:\Program Files\nodejs\node.exe"
    logf = os.path.join(ECODIR, "hq.log")
    logf = open(logf, "ab")
    flags = SPAWN_FLAGS  # DETACHED saja — DETACHED+NO_WINDOW invalid (panel muncul)
    # SEC-001 fix (30-08): production server (auth aktif, bind loopback+tailscale) —
    # bukan lagi `next dev -H 0.0.0.0` yang mem-bypass middleware.
    p = subprocess.Popen(
        [node, "hq-server.mjs"],
        cwd=r"C:\Users\TRIAL\gsp-datacenter", stdout=logf, stderr=logf,
        creationflags=flags, close_fds=True,
    )
    started.append(f"hq(pid {p.pid})")
    log("hq pulih" if wait_http("https://localhost:9011/", 24, 5) else "hq belum pulih dalam 120s")

# ── Hermes Bridge (antrean dispatch AgentRequest) ──────────────────────────
# Insiden 28-08-2026: bridge mati Diam => dispatch HQ "running tanpa diproses".
# Bridge tidak listen port — deteksi via PowerShell CommandLine node.exe.
def bridge_running() -> bool:
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "@(Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | "
             "Where-Object { $_.CommandLine -like '*bridge.mjs*' }).Count"],
            capture_output=True, text=True, timeout=30,
            creationflags=CREATE_NO_WINDOW)
        lines = [l.strip() for l in out.stdout.splitlines() if l.strip()]
        n = int(lines[-1]) if lines else 0
        return n > 0
    except Exception:
        # Gagal deteksi => anggap hidup. Bridge dobel lebih buruk daripada
        # melewatkan satu siklus restart (dua bridge = antrean double-process).
        return True


if bridge_running():
    log("bridge OK")
else:
    log("bridge DOWN -> restart")
    env = os.environ.copy()
    denv = load_env(r"C:\Users\TRIAL\gsp-datacenter\.env")
    env["DATABASE_URL"] = denv.get("DATABASE_URL", "")
    env["HERMES_BOARD"] = denv.get("HERMES_BOARD", "default")
    env["HERMES_BIN"] = denv.get("HERMES_BIN", "hermes")
    env["HERMES_WIKI"] = denv.get("HERMES_WIKI", "")
    env["BRIDGE_RUN_TIMEOUT_MS"] = "1800000"
    kenv = load_env(r"C:\Users\TRIAL\AppData\Local\hermes\.env")
    if kenv.get("KILOCODE_API_KEY"):
        env["KILOCODE_API_KEY"] = kenv["KILOCODE_API_KEY"]
    node = r"C:\Program Files\nodejs\node.exe"
    logf = os.path.join(ECODIR, "bridge.log")
    p = subprocess.Popen(
        [node, "bridge.mjs"], cwd=r"C:\Users\TRIAL\gsp-datacenter\hermes-bridge",
        env=env, stdout=open(logf, "ab"), stderr=subprocess.STDOUT,
        creationflags=SPAWN_FLAGS,
        close_fds=True,
    )
    started.append(f"bridge(pid {p.pid})")
    log("bridge dipulihkan")

# Output HANYA jika ada aksi restart (diam saat sehat = cron tidak kirim apa-apa)
if started:
    print(f"GSP watchdog: layanan di-restart:{' '.join(started)} — {datetime.datetime.now():%F %T}")
