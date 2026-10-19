# Ronde cron 15-10: cek done 12 jam tanpa RANTAI-ACK (sapuan blind-spot, read-only)
import sqlite3, time, os
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = int(time.time())
cutoff = now - 12*3600
cur = con.cursor()
rows = cur.execute(
    "SELECT id,title,status,completed_at,tenant FROM tasks "
    "WHERE status='done' AND completed_at >= ? ORDER BY completed_at DESC", (cutoff,)
).fetchall()
print("done_last_12h =", len(rows))
for r in rows:
    c2 = con.cursor()
    ack = c2.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    lap = c2.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (r["id"],)).fetchone()[0]
    mk = c2.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()[0]
    age_h = (now - r["completed_at"]) / 3600.0
    print(f"{r['id']} age={age_h:.1f}h ack={ack} lap={lap} marker={mk} tenant={r['tenant']} | {r['title'][:60]}")
con.close()
