import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
def q(sql, args=()):
    c = con.cursor(); c.execute(sql, args); return c.fetchall()
t = q("SELECT status FROM tasks WHERE id='t_4edfcf3a'")[0]["status"]
evs = q("SELECT kind,created_at FROM task_events WHERE task_id='t_4edfcf3a' ORDER BY created_at DESC LIMIT 6")
print("pilot t_4edfcf3a status:", t)
for e in evs:
    print(f"  {e['kind']} @{round((now-e['created_at'])/60)}m")
cs = q("SELECT author,created_at,body FROM task_comments WHERE task_id='t_4edfcf3a' ORDER BY created_at DESC LIMIT 2")
for c in cs:
    print(f"  cm [{c['author']}] @{round((now-c['created_at'])/60)}m :: {c['body'][:200]}")
