# Sanity akhir ronde 1014z: umur komentar terakhir papan, event 70m milik siapa, kartu scheduled, census ACK marker.
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

c = con.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()["m"]
print("last comment age min:", round((now - c) / 60, 1))
e = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
print("last event age min:", round((now - e) / 60, 1))
for r in con.execute("SELECT task_id, kind, created_at FROM task_events ORDER BY created_at DESC LIMIT 5"):
    print("  ev", r["task_id"], r["kind"], f"{(now-r['created_at'])/60:.0f}m")
for r in con.execute("SELECT task_id, author, substr(body,1,60) b, created_at FROM task_comments ORDER BY created_at DESC LIMIT 5"):
    print("  cm", r["task_id"], r["author"], f"{(now-r['created_at'])/60:.0f}m", repr(r["b"]))
print("\nscheduled card:")
for r in con.execute("SELECT id, title, tenant, created_at FROM tasks WHERE status='scheduled'"):
    print("  ", r["id"], repr(r["title"][:60]), r["tenant"], f"age={(now-r['created_at'])/3600:.1f}h")
print("\ngave_up per tenant:")
for r in con.execute("SELECT t.tenant, COUNT(*) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE e.kind='gave_up' GROUP BY t.tenant ORDER BY n DESC LIMIT 5"):
    print("  ", r["tenant"], r["n"])
print("\nVBCB gave_up distinct cards:", con.execute("SELECT COUNT(DISTINCT e.task_id) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE e.kind='gave_up' AND t.tenant='VIBE-BIBLE-1013'").fetchone()["n"])
print("VBCB blocked tanpa gave_up:", [r["id"] for r in con.execute("SELECT t.id FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' AND NOT EXISTS (SELECT 1 FROM task_events e WHERE e.task_id=t.id AND e.kind='gave_up')")])
