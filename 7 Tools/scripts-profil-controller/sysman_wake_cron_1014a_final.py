# Final: canonical scan() re-run + parent runway check (started vs max_runtime_seconds, LAPOR presence).
import importlib.util, time, sqlite3, sys

spec = importlib.util.spec_from_file_location("mws", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mws)

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
authors = mws.DEFAULT_AUTHORS
if isinstance(authors, str):
    authors = authors.split(",")
now = int(time.time())
rows = mws.scan(DB, now, authors)
print("RESCAN_ROWS", len(rows))
for r in rows[:50]:
    print("  ", r)

con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
print("---- RUNWAY ----")
over = 0
for r in cur.execute("SELECT id,started_at,max_runtime_seconds,status,title FROM tasks WHERE status='running'"):
    run_min = (now - r["started_at"]) / 60 if r["started_at"] else 0
    cap_min = (r["max_runtime_seconds"] or 3600) / 60
    nlap = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()[0]
    if run_min > cap_min:
        over += 1
        print(f"OVER-CAP {r['id']} run={int(run_min)}m cap={int(cap_min)}m LAPOR={nlap} | {r['title'][:50]}")
print("RUNNING_TOTAL_OVER_CAP", over)
hb = cur.execute("SELECT MAX(last_heartbeat_at) FROM tasks WHERE status='running'").fetchone()[0]
print("FRESHEST_HB_MIN", int((now - hb)/60))
