import sqlite3, os, time, json
db = os.path.join(os.path.join(os.environ.get("LOCALAPPDATA","C:/Users/TRIAL/AppData/Local"),"hermes","kanban.db"))
con = sqlite3.connect(db); con.row_factory = sqlite3.Row
now = time.time()
rows = con.execute("SELECT id,title,status,assignee,created_by,tenant,block_kind,created_at,completed_at,last_heartbeat_at FROM tasks WHERE status='blocked' ORDER BY created_at").fetchall()
for r in rows:
    cid = r["id"]
    comments = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (cid,)).fetchall()
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?",(cid,)).fetchone()["m"]
    print(f"CARD {cid} | {r['title'][:70]} | tenant={r['tenant']} | assignee={r['assignee']} | by={r['created_by']} | block_kind={r['block_kind']}")
    print(f"   last_event_age_min={round((now-(ev or 0))/60,1)}")
    for c in comments:
        print(f"   CMT[{c['author']}]: {c['body'][:160].replace(chr(10),' / ')}")
print("TOTAL_BLOCKED=", len(rows))
