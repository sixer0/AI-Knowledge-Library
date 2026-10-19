#!/usr/bin/env python3
"""Cek koneksi VPN GSP -> inference server KAYTUS (10.83.81.246).

Dipakai cron agent mode "GSP VPN-Kaytus Morning Check" tiap 05:30.
Logika:
  1. Probe endpoint inference kaytus (HTTP apa pun = terjangkau).
  2. Terjangkau  -> STATUS: CONNECTED_OK, diam-diam lapor sehat.
  3. Tidak terjangkau:
     a. tunnel UP (adapter OpenVPN punya IP 10.255.x + proses openvpn hidup)
        tapi endpoint mati -> STATUS: VPN_UP_SERVER_DEAD (jangan reconnect buta).
     b. tunnel DOWN -> panggil OpenVPN GUI --connect "VPN GSP.ovpn"
        (kredensial tersimpan DPAPI di registry user; nointeract),
        tunggu hingga 120 dtk sambil re-probe tiap 10 dtk.
        Berhasil -> STATUS: RECONNECTED. Gagal -> STATUS: FAILED (+ekor log).

Flag uji:
  --probe-only        tidak pernah memicu koneksi (hanya ukur)
  --test-fail-branch  probe IP fiktif untuk uji jalur merah tanpa menyentuh VPN nyata

Exit code: 0 = sehat/berhasil reconnect; 2 = FAILED/VPN_UP_SERVER_DEAD; 3 = error skrip.
Panggil: uv run --python 3.11 --no-project python vpn_kaytus_check.py
"""
import argparse
import datetime
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

KAYTUS = "10.83.81.246"
ENDPOINTS = [
    f"http://{KAYTUS}:11400/v1/models",   # gateway GSP-AI (model provider fleet)
    f"http://{KAYTUS}:4000/health",       # endpoint inferensi alternatif
]
GUI = r"C:\Program Files\OpenVPN\bin\openvpn-gui.exe"
CONFIG = "VPN GSP.ovpn"
LOGFILE = r"C:\Users\TRIAL\OpenVPN\log\VPN GSP.log"
CREATE_NO_WINDOW = 0x08000000
DETACHED = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)


def now() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def probe(url: str, timeout: int = 8):
    """True bila server merespons HTTP apa pun (termasuk 401/404: bukti reachable)."""
    req = urllib.request.Request(url, headers={"User-Agent": "gsp-vpn-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return True, f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        return True, f"HTTP {e.code}"
    except Exception as e:
        return False, type(e).__name__


def tunnel_state():
    """(up, detail) dari adapter OpenVPN + proses openvpn."""
    up_ip = ""
    try:
        out = subprocess.run(["ipconfig"], capture_output=True, text=True,
                             creationflags=CREATE_NO_WINDOW, timeout=20).stdout
        blocks = re.split(r"\n[^\n]*adapter [^\n]*\n", "\n" + out)
        heads = re.findall(r"adapter ([^\n:]+):", out)
        for head, body in zip(heads, blocks[1:]):
            if "OpenVPN" in head:
                m = re.search(r"IPv4 Address[^\d]*(\d+\.\d+\.\d+\.\d+)", body)
                if m and m.group(1).startswith("10."):
                    up_ip = m.group(1)
    except Exception:
        pass
    proc = False
    try:
        out = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command",
             "(Get-Process openvpn -ErrorAction SilentlyContinue).Count"],
            capture_output=True, text=True, creationflags=CREATE_NO_WINDOW, timeout=30).stdout
        proc = out.strip().isdigit() and int(out.strip()) > 0
    except Exception:
        pass
    return (bool(up_ip) and proc), f"ip={up_ip or '-'} proses_openvpn={'ada' if proc else 'tidak'}"


def trigger_connect():
    if not os.path.exists(GUI):
        return False, f"GUI tidak ditemukan: {GUI}"
    subprocess.Popen([GUI, "--connect", CONFIG], creationflags=DETACHED)
    return True, f"dipanggil: openvpn-gui --connect '{CONFIG}'"


def log_tail(n: int = 12) -> str:
    try:
        with open(LOGFILE, "r", errors="replace") as f:
            lines = f.readlines()
        return "".join(lines[-n:]).strip()
    except Exception as e:
        return f"(log tidak terbaca: {e})"


def any_reachable():
    results = []
    ok = False
    for url in ENDPOINTS:
        r, detail = probe(url)
        results.append((url, r, detail))
        ok = ok or r
    return ok, results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe-only", action="store_true")
    ap.add_argument("--test-fail-branch", action="store_true")
    args = ap.parse_args()

    global ENDPOINTS
    if args.test_fail_branch:
        ENDPOINTS = ["http://240.0.0.1:59999/probe"]  # IP fiktif: selalu gagal

    print(f"[{now()}] cek awal konektivitas KAYTUS ({KAYTUS})")
    ok, results = any_reachable()
    for url, r, detail in results:
        print(f"  probe {'OK ' if r else 'BIO'} {url} -> {detail}")

    if ok:
        up, detail = tunnel_state()
        print(f"STATUS: CONNECTED_OK | tunnel: {detail} | inference kaytus terjangkau")
        return 0

    up, tdetail = tunnel_state()
    print(f"  kaytus tidak terjangkau; kondisi tunnel: {tdetail}")

    if up:
        print("STATUS: VPN_UP_SERVER_DEAD | tunnel VPN hidup tapi server kaytus tidak "
              "merespons - kemungkinan server mati/di hulu, reconnect tidak menolong")
        return 2

    if args.probe_only:
        print("STATUS: DISCONNECTED (probe-only, tidak memicu koneksi)")
        return 2

    print("  tunnel mati -> memicu koneksi via OpenVPN GUI")
    started, msg = trigger_connect()
    print(f"  {msg}")
    if not started:
        print("STATUS: FAILED | tidak bisa memicu koneksi")
        return 2

    deadline = time.time() + 120
    while time.time() < deadline:
        time.sleep(10)
        ok, results = any_reachable()
        if ok:
            up2, tdetail2 = tunnel_state()
            print(f"STATUS: RECONNECTED | reconnect berhasil dalam <=120 dtk | {tdetail2}")
            return 0
        print("  ... menunggu tunnel (re-probe)")

    print("STATUS: FAILED | 120 dtk setelah trigger, kaytus tetap tidak terjangkau")
    print("--- ekor log VPN ---")
    print(log_tail())
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"STATUS: ERROR | {type(e).__name__}: {e}")
        sys.exit(3)
