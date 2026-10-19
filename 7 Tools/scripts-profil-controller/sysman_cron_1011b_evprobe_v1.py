import sqlite3, time
db = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{db.replace(chr(92),'/')}?mode=ro", uri=True)
now = time.time()
for tbl, col in [("task_events","created_at"),("task_comments","created_at")]:
    mx = con.execute(f"SELECT MAX({col}) FROM {tbl}").fetchone()[0]
    print(f"{tbl}: max age_min = {(now-float(mx))/60.0:.1f}")
print("-- open statuses census --")
for row in con.execute("SELECT status, COUNT(*) FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status"):
    print(row)
print("-- last 5 events --")
for row in con.execute("SELECT task_id, kind, datetime(created_at,'unixepoch','+7 hours') FROM task_events ORDER BY created_at DESC LIMIT 5"):
    print(row)
print("-- WAKE=1 detail candidates vs canonical window: done_age min --")
import datetime
for tid in ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3"]:
    r = con.execute("SELECT completed_at, tenant, created_by FROM tasks WHERE id=?", (tid,)).fetchone()
    age_h = (now - float(r[0]))/3600.0
    print(f"{tid} done_age_h={age_h:.2f} tenant={r[1]!r} by={r[2]}")
