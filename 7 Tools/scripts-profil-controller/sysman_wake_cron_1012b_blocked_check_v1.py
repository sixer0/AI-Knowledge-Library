import sqlite3, time, os
db = os.path.join(os.environ.get("LOCALAPPDATA","C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())
rows = con.execute("SELECT id,title,status,tenant,assignee,created_by,completed_at FROM tasks WHERE status='blocked' ORDER BY created_at DESC").fetchall()
print(f"blocked={len(rows)} now={now}")
for r in rows:
    tid = r["id"]
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1",(tid,)).fetchone()
    cm = con.execute("SELECT author, substr(body,1,160) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3",(tid,)).fetchall()
    ev_age = round((now-ev["created_at"])/60,1) if ev else None
    print(f"- {tid} | {r['title'][:70]} | tenant={r['tenant']} | by={r['created_by']} | last_event={ev['kind'] if ev else '-'} age_min={ev_age}")
    for c in cm:
        print(f"    comment[{c['author']}]: {c['b'][:150]}")
