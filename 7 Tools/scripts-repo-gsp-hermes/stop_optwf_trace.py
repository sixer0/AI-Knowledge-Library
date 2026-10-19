#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stop_optwf_trace.py — hentikan daemon WorkerTrace secara terverifikasi.

Baca optwf_worker_trace.pid, pastikan PID itu benar-benar proses
optwf_worker_trace.py (cek baris perintah via wmic), baru hentikan.
Usage: python stop_optwf_trace.py [--pid N]
"""
import os
import signal
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PID_FILE = os.path.join(HERE, "optwf_worker_trace.pid")


def cmdline_of(pid):
    """Baris perintah proses via PowerShell (wmic dihapus dari Win11 24H2+)."""
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"(Get-CimInstance Win32_Process -Filter 'ProcessId={pid}').CommandLine"],
            capture_output=True, text=True, timeout=30).stdout
        return out
    except Exception:
        return ""


def main():
    if "--pid" in sys.argv:
        pid = int(sys.argv[sys.argv.index("--pid") + 1])
    else:
        pid = int(open(PID_FILE, encoding="ascii").read().strip())
    cl = cmdline_of(pid)
    if "optwf_worker_trace.py" not in cl:
        print(f"REFUSE: pid {pid} bukan daemon optwf_worker_trace "
              f"(cmdline: {cl.strip()[:120] or 'tidak ditemukan'})")
        return 2
    os.kill(pid, signal.SIGTERM)
    print(f"stopped pid={pid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
