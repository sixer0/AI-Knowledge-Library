# Read-only: heartbeat umur simpul running + sensus tenant VIBE-BIBLE-1013 (ronde 14-10-a).
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
cur = con.cursor()

for cid in ["t_68f547bd", "t_87aa2f1f"]:
    t = cur.execute("SELECT id,status,title FROM tasks WHERE id=?", (cid,)).fetchone()
    hb = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=? AND kind='heartbeat'", (cid,)).fetchone()["m"]
    lastev = cur.execute("SELECT kind, MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()
    lap = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (cid,)).fetchone()["c"]
    ack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (cid,)).fetchone()["c"]
    print("%s [%s] %s" % (cid, t["status"], t["title"][:60]))
    print("   heartbeat_age=%s min | LAPOR=%d ACK=%d" % (round((now-hb)/60) if hb else None, lap, ack))

print("\n-- sensus tenant VIBE-BIBLE-1013 --")
tot = 0
for r in cur.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    print("  %-10s %d" % (r["status"], r["c"])); tot += r["c"]
print("  TOTAL %d" % tot)
for r in cur.execute("SELECT id,status,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status IN ('running','todo','blocked','in_progress') ORDER BY status"):
    print("   open: %s [%s] %s" % (r["id"], r["status"], r["title"][:70]))
con.close()
