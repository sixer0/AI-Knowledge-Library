# sysman ronde-c bagian 3: baca komentar lengkap t_7f6e0fbb + konteks STA13
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

r = con.execute("SELECT id,title,status,tenant,started_at,last_heartbeat_at,max_runtime_seconds FROM tasks WHERE id='t_7f6e0fbb'").fetchone()
print("CARD", dict(r))
cs = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id='t_7f6e0fbb' ORDER BY created_at").fetchall()
for c in cs:
    print(f"\n--- {c['author']} @{int((now-c['created_at'])/60)}m ---\n{c['body'][:1200]}")

# sibling STA13 cards
print("\n=== STA13-1013 census ===")
for s in con.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant='STA13-1013' GROUP BY status"):
    print(s["status"], s["n"])
for k in con.execute("SELECT id,status,title,completed_at FROM tasks WHERE tenant='STA13-1013' ORDER BY created_at DESC LIMIT 12"):
    print(f"  {k['id']} {k['status']} {k['title'][:70]}")
