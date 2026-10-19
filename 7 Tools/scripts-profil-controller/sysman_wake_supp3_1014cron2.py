# Read-only: why t_b10a1e32 surfaced as done-unacked (blocked status) - comments + events + route-4b gate check.
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
tid = "t_b10a1e32"
c = con.cursor()
t = c.execute("SELECT id,status,tenant,block_kind,completed_at,started_at FROM tasks WHERE id=?", (tid,)).fetchone()
print(dict(t) if t else "none")
print("-- all comments --")
for row in c.execute("SELECT id,author,SUBSTR(body,1,160) b,created_at FROM task_comments WHERE task_id=? ORDER BY created_at ASC", (tid,)):
    print(f"@{round((NOW-row['created_at'])/60)}m {row['author']}: {row['b'].replace(chr(10),' ')}")
print("-- events --")
for row in c.execute("SELECT kind,run_id,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 12", (tid,)):
    print(f"@{round((NOW-row['created_at'])/60)}m {row['kind']} run={row['run_id']}")
