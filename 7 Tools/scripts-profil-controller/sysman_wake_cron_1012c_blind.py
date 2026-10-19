# Blind sweep ronde 12-10: terminal events <=6h tanpa syarat tenant + census todo terbuka
import sqlite3, time, os
db = os.path.join(os.environ.get("LOCALAPPDATA","C:/Users/TRIAL/AppData/Local/hermes"), "hermes", "kanban.db")
con = sqlite3.connect(db); con.row_factory = sqlite3.Row
now = int(time.time())
print("-- terminal events <=6h (tanpa syarat tenant) --")
q = """SELECT t.id, substr(t.title,1,48) title, t.status, t.tenant, e.kind,
       round((?1 - e.created_at)/60.0,1) age_min
FROM task_events e JOIN tasks t ON t.id=e.task_id
WHERE e.kind IN ('completed','blocked','parked') AND e.created_at >= ?1 - 6*3600
ORDER BY e.created_at DESC LIMIT 40"""
for r in con.execute(q,(now,)):
    print(dict(r))
print("-- todo terbuka (umur, parent status) --")
q2 = """SELECT t.id, substr(t.title,1,48) title, round((?1-t.created_at)/60.0,1) age_min,
       (SELECT group_concat(p2.status,',') FROM task_links l JOIN tasks p2 ON p2.id=l.parent_id WHERE l.child_id=t.id) parents
FROM tasks t WHERE t.status='todo' ORDER BY t.created_at DESC LIMIT 10"""
for r in con.execute(q2,(now,)):
    print(dict(r))
print("-- running dengan LAPOR tanpa ACK (blind) --")
q3 = """SELECT t.id, substr(t.title,1,48) title, t.last_heartbeat_at,
       (SELECT count(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%LAPOR%SELESA%') lapor,
       (SELECT count(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%') acks
FROM tasks t WHERE t.status='running'"""
rows=list(con.execute(q3))
print("running_count =", len(rows))
for r in rows: print(dict(r))
