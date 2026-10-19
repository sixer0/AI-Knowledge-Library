import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
t = con.execute("SELECT id,title,status,tenant,completed_at FROM tasks WHERE id='t_fa568361'").fetchone()
print(dict(t), "umur_selesai_mnt=", int((now - t["completed_at"]) / 60) if t["completed_at"] else None)
for c in con.execute("SELECT author, substr(body,1,120) b, created_at FROM task_comments WHERE task_id='t_fa568361' ORDER BY created_at"):
    print(f"  {c['author']} {int((now-c['created_at'])/60)}m :: {c['b']}")
