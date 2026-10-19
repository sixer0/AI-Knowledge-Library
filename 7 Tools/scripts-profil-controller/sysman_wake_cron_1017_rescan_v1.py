# -*- coding: utf-8 -*-
"""Pembuktian kedua ronde 17-10: panggil scan() kanonis via importlib (bukan CLI)
dan tangkap NILAI KEMBALIAN (list temuan), bukan stdout - preseden 15-10."""
import importlib.util, os, sys, time

SCRIPT = r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py"
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"

spec = importlib.util.spec_from_file_location("wake_scan", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
print("CONTROLLER_AUTHORS =", authors)
for name in ("STALLED_MIN", "RUN_WINDOW_H", "FASE_STALL_MIN", "DONE_UNACKED_MIN"):
    print("AMBANG %-16s =" % name, getattr(mod, name, "(tidak ada)"))

res = mod.scan(DB, int(time.time()), authors)
print("TIPE =", type(res).__name__, "JUMLAH TEMUAN =", len(res))
for row in res:
    print("  TEMUAN:", row)
print("SCAN-DONE")
