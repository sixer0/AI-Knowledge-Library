# Read-only: umur selesai kartu done VBCB vs jendela scan (ronde 14-10-a ronde 3).
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
cur = con.cursor()
print("now=%d" % now)
for r in cur.execute("SELECT id,status,completed_at,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' ORDER BY completed_at"):
    ca = r["completed_at"]
    age_min = round((now-ca)/60) if ca else None
    ack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    mk = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()["c"]
    print("%s [%-7s] completed_age=%s min ack=%d marker=%d :: %s" % (r["id"], r["status"], age_min, ack, mk, r["title"][:55]))
con.close()
