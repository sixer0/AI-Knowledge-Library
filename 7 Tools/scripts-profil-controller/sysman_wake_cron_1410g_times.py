import sqlite3, time
con = sqlite3.connect("file:C:/Users/TRIAL/AppData/Local/hermes/kanban.db?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())
def q(s):
    return con.execute(s).fetchone()
u = q("SELECT MAX(created_at) m FROM task_comments WHERE task_id='t_4edfcf3a' AND body LIKE '%UNBLOCK%'")
r = q("SELECT MIN(started_at) m FROM task_runs WHERE task_id='t_4edfcf3a' AND status='running'")
h = q("SELECT MAX(last_heartbeat_at) m FROM task_runs WHERE task_id='t_4edfcf3a' AND status='running'")
b = q("SELECT MAX(created_at) m FROM task_events WHERE kind='blocked' AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')")
e = q("SELECT MAX(created_at) m FROM task_events")
print("UNBLOCK age_min=", round((now - u["m"]) / 60, 1))
print("replacement-run age_min=", round((now - r["m"]) / 60, 1), "| hb age_min=", round((now - h["m"]) / 60, 1))
print("latest-blocked-event age_min=", round((now - b["m"]) / 60, 1))
print("board last event age_min=", round((now - e["m"]) / 60, 1))
