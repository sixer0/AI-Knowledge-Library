# Final checks: gave_up census per blocked card, scheduled card due, re-scan via module scan().
import sqlite3, time, importlib.util, sys

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = int(time.time())

blocked = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'")]
ng = 0
for i in blocked:
    n = con.execute("SELECT COUNT(*) c FROM task_events WHERE task_id=? AND kind='gave_up'", (i,)).fetchone()["c"]
    ng += (n > 0)
print("blocked cards:", len(blocked), "with gave_up event:", ng)

nto = con.execute("SELECT COUNT(DISTINCT task_id) c FROM task_events WHERE kind='timed_out' AND task_id IN (%s)" % ",".join("?" * len(blocked)), blocked).fetchone()["c"]
print("blocked cards with >=1 timed_out:", nto)

r = con.execute("SELECT id, title, body, created_at FROM tasks WHERE id='t_689662c9'").fetchone()
print("\nscheduled card:", r["id"], "| created:", time.strftime("%m-%d %H:%M", time.localtime(r["created_at"])))
print("body head:", (r["body"] or "")[:400].replace("\n", " | "))

# any runs for scheduled card?
nrun = con.execute("SELECT COUNT(*) c FROM task_runs WHERE task_id='t_689662c9'").fetchone()["c"]
print("runs for scheduled card:", nrun)

# re-scan canonical
spec = importlib.util.spec_from_file_location("wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
res = m.scan(DB, int(time.time()), ["default", "sysmanager-cleaner", "mission-wake"])
lines = res if isinstance(res, list) else res[0] if isinstance(res, tuple) else res
cnt = collections = None
if isinstance(lines, list):
    print("\nre-scan rows:", len(lines))
    import collections as C
    cls = C.Counter((x[1] if isinstance(x, (list, tuple)) and len(x) > 1 else str(x)) for x in lines)
    print(dict(cls))
    du = [x for x in lines if isinstance(x, (list, tuple)) and "done-unacked" in str(x)]
    print("done-unacked rows:", du if du else "NONE")
else:
    print("\nre-scan raw return:", repr(res)[:2000])
