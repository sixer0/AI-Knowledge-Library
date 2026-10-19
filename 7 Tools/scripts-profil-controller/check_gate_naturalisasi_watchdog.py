# -*- coding: utf-8 -*-
"""Launcher cron (harus di bawah ~/.hermes/scripts/) untuk penjaga gerbang
naturalisasi NAT-S25. Sumber kebenaran skrip:
C:/Users/TRIAL/workspace/gsp-hermes/scripts/check_gate_naturalisasi.py

Keputusan D-TA-06: laporan saja, TANPA auto-block. Exit code verdict (1 saat
FAIL) sengaja dinormalkan ke 0 di sini supaya cron no_agent tetap MENGIRIM
stdout selisih (exit != 0 menandai job 'error' dan menahan pengiriman).
Verdict jujur tetap terbaca di baris VERDICT laporan di disk.
"""
import runpy

TARGET = "C:/Users/TRIAL/workspace/gsp-hermes/scripts/check_gate_naturalisasi.py"

try:
    runpy.run_path(TARGET, run_name="__main__")
except SystemExit:
    pass

raise SystemExit(0)
