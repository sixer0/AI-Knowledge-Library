# -*- coding: utf-8 -*-
# Ronde 1015r3: re-scan kanonis via import modul scan(db_path, now_int, authors_list).
import importlib.util, time, sys
spec = importlib.util.spec_from_file_location("ws", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = mod.DEFAULT_AUTHORS
if isinstance(authors, str): authors = authors.split(",")
rows = mod.scan(r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db", int(time.time()), authors)
print("JUMLAH BARIS:", len(rows))
for r in rows[:40]:
    print(r)
