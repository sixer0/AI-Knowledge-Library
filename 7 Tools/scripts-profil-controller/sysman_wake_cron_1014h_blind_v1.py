# Sapuan blind spot 14-10h: kartu running + blocked non-VBCB (read-only).
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("== KARTU RUNNING ==")
for r in con.execute("SELECT id,title,assignee,started_at,tenant FROM tasks WHERE status='running'"):
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    print(f"  {r['id']} tenant={r['tenant']} assignee={r['assignee']} start={(now-r['started_at'])//60 if r['started_at'] else -1}m ev={(now-ev)//60 if ev else -1}m :: {r['title'][:70]}")
    for c in con.execute("SELECT author, substr(replace(body,char(10),' '),1,120) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 3", (r["id"],)):
        print(f"    [{c['author']} {(now-c['created_at'])//60}m] {c['b']}")

print("\n== BLOCKED NON-VBCB ==")
for r in con.execute("SELECT id,title,status,tenant,assignee FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant!='VIBE-BIBLE-1013') ORDER BY created_at DESC"):
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    evage = int((now - ev) / 60) if ev else -1
    nmark = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI%'", (r["id"],)).fetchone()["c"]
    print(f"  {r['id']} tenant={r['tenant']} ev={evage}m rantai_kom={nmark} :: {r['title'][:60]}")
    last = con.execute("SELECT author, substr(replace(body,char(10),' '),1,100) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
    if last:
        print(f"    last[{last['author']} {(now-last['created_at'])//60}m] {last['b']}")
con.close()
