# Ronde wake 16-10: cek kesegaran event + census kartu terbuka + marker coverage blocked
import sqlite3, time, os
DB = os.path.expandvars(r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())

for tbl, col in [("task_events", "created_at"), ("task_comments", "created_at")]:
    r = cur.execute(f"SELECT MAX({col}) m, COUNT(*) c FROM {tbl}").fetchone()
    print(f"{tbl}: max_age_min={round((now - r['m'])/60,1)} count={r['c']}")

print("-- status terbuka --")
for r in cur.execute("SELECT status, COUNT(*) c FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status ORDER BY c DESC"):
    print(f"{r['status']} = {r['c']}")

print("-- blocked: umur event terakhir + marker RANTAI-WAKE + [FASE] --")
ids = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE status='blocked' ORDER BY id")]
for tid in ids:
    ev = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    mk = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["c"]
    ph = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%[FASE]%'", (tid,)).fetchone()["c"]
    title = cur.execute("SELECT title FROM tasks WHERE id=?", (tid,)).fetchone()["title"]
    age = round((now - ev)/60) if ev else None
    print(f"{tid} ev_age={age}m marker={mk} fase={ph} :: {title[:60]}")

print("-- running dengan LAPOR tanpa ACK --")
run_ids = [r["id"] for r in cur.execute("SELECT id, title FROM tasks WHERE status='running'")]
print(f"running count={len(run_ids)}")
for tid in run_ids:
    lap = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%')", (tid,)).fetchone()["c"]
    ack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    hb = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    age = round((now - hb)/60) if hb else None
    if lap and not ack:
        print(f"CANDIDATE {tid} lap={lap} ack={ack} ev_age={age}m")
con.close()
