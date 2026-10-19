# sysman ronde-c bagian 5: turunan t_7f6e0fbb + umur flat VBCB + rekap final
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# turunan transitif t_7f6e0fbb
kids = con.execute("SELECT child_id FROM task_links WHERE parent_id='t_7f6e0fbb'").fetchall()
print("DIRECT_CHILDREN", [k["child_id"] for k in kids])
par = con.execute("SELECT parent_id FROM task_links WHERE child_id='t_7f6e0fbb'").fetchall()
print("PARENTS", [p["parent_id"] for p in par])

# umur event terakhir per kartu blocked VBCB (sebar flat?)
ages = con.execute("""
  SELECT MIN(mn) a, MAX(mn) b FROM (
    SELECT MAX(e.created_at) mn FROM task_events e JOIN tasks k ON e.task_id=k.id
    WHERE k.tenant='VIBE-BIBLE-1013' AND k.status='blocked' GROUP BY k.id)
""").fetchone()
print("BLOCKED_LAST_EV_AGE min_max_min", int((now-ages["b"])/60), int((now-ages["a"])/60))

# cek ulang status t_7f6e0fbb saat ini
r = con.execute("SELECT status, last_heartbeat_at FROM tasks WHERE id='t_7f6e0fbb'").fetchone()
print("STA13_FIX2 status", r["status"], "hb_age", int((now-r["last_heartbeat_at"])/60))
acks = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id='t_7f6e0fbb' AND body LIKE '%RANTAI-ACK%'").fetchone()["c"]
print("STA13_FIX2 ack", acks)
