# Round 15-10 cron step3: deterministic re-scan via canonical scan() (importlib) to confirm row set stability
import importlib.util, time, sys

spec = importlib.util.spec_from_file_location("wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True
spec.loader.exec_module(m)

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
authors = m.DEFAULT_AUTHORS
if isinstance(authors, str):
    authors = authors.split(",")
rows = m.scan(DB, int(time.time()), authors)
print("ROWS:", len(rows))
for r in rows:
    print(r)
