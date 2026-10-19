# Sapuan blind-spot: terminal-event <=6h tanpa syarat tenant + LAPOR tanpa ACK + re-scan final
import sqlite3, time, importlib.util, os

HERMES = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HERMES, "kanban.db")
SCAN = os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py")
now = int(time.time())

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

print("=== A. Event terminal <=6h (semua tenant, tanpa gerbang) ===")
rows = cur.execute("""
  SELECT t.id, t.status, t.tenant, t.title, MAX(e.created_at) last_ev
  FROM tasks t JOIN task_events e ON e.task_id=t.id
  WHERE e.kind IN ('completed','parked','blocked','timed_out','gave_up')
    AND e.created_at >= ?
  GROUP BY t.id ORDER BY last_ev DESC LIMIT 40
""", (now - 6*3600,)).fetchall()
print("n =", len(rows))
for r in rows:
    tid = r["id"]
    lap = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELE%'", (tid,)).fetchone()["n"]
    ack = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    mk  = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["n"]
    if r["status"] in ("done","blocked","parked") and lap > 0 and ack == 0 and mk == 0:
        print(f"KANDIDAT {tid} | {r['status']} | tenant={r['tenant']} | lap={lap} ack={ack} | {r['title'][:55]}")

print("=== B. Kartu running ber-LAPOR tanpa ACK (blind spot status running) ===")
ids = [r["id"] for r in cur.execute("SELECT id, title FROM tasks WHERE status='running'").fetchall()]
n_flag = 0
for tid in ids:
    lap = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELE%'", (tid,)).fetchone()["n"]
    ack = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    if lap > 0 and ack == 0:
        n_flag += 1
        t = cur.execute("SELECT title FROM tasks WHERE id=?", (tid,)).fetchone()["title"]
        print(f"RUNNING-LAPOR {tid} | {t[:60]}")
print("n_running_flag =", n_flag, "dari", len(ids), "running")

con.close()

print("=== C. Re-scan kanonis final ===")
spec = importlib.util.spec_from_file_location("wake_scan2", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = mod.DEFAULT_AUTHORS
if isinstance(authors, str):
    authors = authors.split(",")
res = mod.scan(DB, int(time.time()), authors)
print("N_TEMUAN_FINAL =", len(res))
for row in res:
    print("WAKE:", row)
