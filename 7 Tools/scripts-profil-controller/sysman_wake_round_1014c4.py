# sysman ronde-c bagian 4: cek ulang blind spot t_7f6e0fbb (ACK mendarat? kartu selesai?)
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
r = con.execute("SELECT id,status,completed_at,last_heartbeat_at FROM tasks WHERE id='t_7f6e0fbb'").fetchone()
print("STATUS", r["status"], "completed_age_min", int((now-r["completed_at"])/60) if r["completed_at"] else None, "hb_age", int((now-r["last_heartbeat_at"])/60) if r["last_heartbeat_at"] else None)
cs = con.execute("SELECT author, substr(replace(body,char(10),' '),1,110) b, created_at FROM task_comments WHERE task_id='t_7f6e0fbb' ORDER BY created_at DESC LIMIT 6").fetchall()
for c in cs:
    print(f"{int((now-c['created_at'])/60)}m {c['author']}: {c['b']}")
acks = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id='t_7f6e0fbb' AND body LIKE '%RANTAI-ACK%'").fetchone()["c"]
print("ACK_COUNT", acks)
evs = con.execute("SELECT kind, MAX(created_at) m FROM task_events WHERE task_id='t_7f6e0fbb' GROUP BY kind ORDER BY m DESC LIMIT 5").fetchall()
for e in evs:
    print("EV", e["kind"], int((now-e["m"])/60), "m")
