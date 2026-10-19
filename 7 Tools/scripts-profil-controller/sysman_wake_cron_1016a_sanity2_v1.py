"""Ronde wake 16-10: saksi kedua saat stdout kosong (umur event terminal + census terbuka)."""
import sqlite3, time, os

DB = os.path.join("C:/Users/TRIAL/AppData/Local/hermes", "kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = int(time.time())

ev = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
cm = con.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()["m"]
rn = con.execute("SELECT MAX(created_at) m FROM runs" if False else "SELECT MAX(started_at) m FROM task_runs").fetchone()["m"]
print("events_max_age_min = %.1f" % ((now - ev) / 60.0))
print("comments_max_age_min = %.1f" % ((now - cm) / 60.0))
if rn:
    print("runs_max_age_min = %.1f" % ((now - rn) / 60.0))

print("-- status terbuka --")
for r in con.execute("SELECT status, COUNT(*) c FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status ORDER BY c DESC"):
    print("%s = %d" % (r["status"], r["c"]))

print("-- running dengan LAPOR tanpa ACK (blind spot rute-4b) --")
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='running'")]
hits = 0
for tid in ids:
    lap = con.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELE'", (tid,)
    ).fetchone()["c"]
    ack = con.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)
    ).fetchone()["c"]
    if lap and not ack:
        hits += 1
        print("HIT %s lap=%s ack=%s" % (tid, lap, ack))
print("running_total=%d blind_hits=%d" % (len(ids), hits))

print("-- marker RANTAI-WAKE umur <= 12 jam --")
for r in con.execute(
    "SELECT task_id, MAX(created_at) m FROM task_comments WHERE body LIKE '%RANTAI-WAKE%' "
    "GROUP BY task_id HAVING m > ? ORDER BY m DESC LIMIT 15", (now - 12 * 3600,)
):
    print("%s age_min=%.0f" % (r["task_id"], (now - r["m"]) / 60.0))
con.close()
