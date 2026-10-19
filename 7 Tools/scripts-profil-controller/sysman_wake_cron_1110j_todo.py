import sqlite3, time, os
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); cur = con.cursor()
now = int(time.time())
for tid, title, created_at, cb, tenant in cur.execute(
        "SELECT id,title,created_at,created_by,tenant FROM tasks WHERE status='todo' ORDER BY created_at"):
    parents = cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()
    pstat = []
    for (pid,) in parents:
        st = cur.execute("SELECT status FROM tasks WHERE id=?", (pid,)).fetchone()
        pstat.append(f"{pid}:{st[0] if st else '?'}")
    ev = cur.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,)).fetchone()[0]
    print(f"{tid} age_h={(now-(created_at or 0))/3600:.1f} lastev_age_h={(now-ev)/3600:.1f} if ev else 'None'" if ev else f"{tid} age_h={(now-(created_at or 0))/3600:.1f} lastev=None", "|", title[:48], "| parents:", pstat, "| tenant:", tenant, "| by:", cb)
con.close()
