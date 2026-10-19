# Blind sweep: terminal events <=6h TANPA syarat tenant + census 7 kartu blocked
import sqlite3, time, os
db = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect(db)
cur = con.cursor()
now = int(time.time())
print("-- terminal events <= 6h (tanpa syarat tenant) --")
rows = cur.execute("""
 SELECT t.id, t.status, t.tenant, e.kind, e.created_at,
        CAST((? - e.created_at)/60 AS INT) AS age_min
 FROM task_events e JOIN tasks t ON t.id = e.task_id
 WHERE e.created_at >= ? - 6*3600
   AND e.kind IN ('completed','blocked','parked','failed','done')
 ORDER BY e.created_at DESC LIMIT 30
""", (now, now)).fetchall()
if not rows:
    print("(kosong: tidak ada event terminal dalam 6 jam)")
for r in rows:
    print(r)
print("-- census 7 kartu blocked --")
rows = cur.execute("""
 SELECT id, substr(title,1,70), tenant, CAST((? - created_at)/60 AS INT) AS age_min_created
 FROM tasks WHERE status='blocked' ORDER BY created_at DESC
""", (now,)).fetchall()
for r in rows:
    print(r)
print("-- komentar terakhir per kartu blocked --")
for r in rows:
    c = cur.execute("""
      SELECT author, substr(body,1,110), CAST((? - created_at)/60 AS INT)
      FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1
    """, (now, r[0])).fetchone()
    print(r[0], "|", c)
con.close()
