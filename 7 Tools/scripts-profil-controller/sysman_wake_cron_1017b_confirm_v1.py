# Konfirmasi vonis diam: scan() kanonis + census status terbuka
import sqlite3, time, importlib.util, sys

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
SCAN = "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py"

con = sqlite3.connect(DB)
rows = con.execute("SELECT status, COUNT(*) n FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status").fetchall()
print("-- open status --")
for s, n in rows:
    print(f"{s} = {n}")
mx = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()[0]
print(f"newest_task_event_age_min = {round((time.time()-mx)/60,1)}")
con.close()

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
sys.argv = [SCAN]
spec.loader.exec_module(mod)
authors = mod.DEFAULT_AUTHORS.split(",") if isinstance(mod.DEFAULT_AUTHORS, str) else list(mod.DEFAULT_AUTHORS)
findings = mod.scan(DB, int(time.time()), authors)
print(f"scan() findings = {len(findings)}")
for f in findings:
    print("  ", tuple(f) if not hasattr(f, '_asdict') else f)
