import sqlite3, time
con = sqlite3.connect(r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db")
con.row_factory = sqlite3.Row
now = int(time.time())
rows = con.execute("SELECT id, title, tenant, block_kind, created_at FROM tasks WHERE status='blocked'").fetchall()
for r in rows:
    last_c = con.execute("SELECT body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    b = (last_c["body"] or "") if last_c else ""
    if "[SYSMAN-CLEANER" not in b:
        mx = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (r["id"],)).fetchone()[0]
        print(f"NO-TOKEN {r['id']} ev_age={(now-mx)/60.0:.0f}m kind={r['block_kind']} tenant={r['tenant']}")
        print(f"  title: {r['title']}")
        print(f"  last comment ({((now-last_c['created_at'])/60.0 if last_c else -1):.0f}m): {b[:400]}")
