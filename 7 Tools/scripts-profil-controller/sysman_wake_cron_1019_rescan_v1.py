"""Re-scan kanonis akhir giliran: panggil scan() modul pemindai wake, cetak jumlah temuan."""
import importlib.util
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "gsp_mission_wake_scan", os.path.join(HERE, "gsp_mission_wake_scan.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

db = os.path.join(os.path.dirname(HERE), "kanban.db")
authors = mod.DEFAULT_AUTHORS
authors = authors.split(",") if isinstance(authors, str) else list(authors)
rows = mod.scan(db, int(time.time()), authors)
print(f"SCAN temuan={len(rows)}")
for r in rows:
    print("  ", tuple(r))
