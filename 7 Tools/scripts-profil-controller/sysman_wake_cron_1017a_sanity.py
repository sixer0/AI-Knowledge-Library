# Ronde wake 17-10: sanity papan hidup + rekonsiliasi scan() kanonis + sensus terbuka
import sqlite3, time, os, importlib.util, sys, json

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

now = int(time.time())

# 1) Sensus status
print("== SENSUS STATUS ==")
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"{r['status']}: {r['n']}")

# 2) Kesegaran: MAX event (BUKAN MIN)
print("== KESGARAN ==")
for tbl, col in (("task_events","created_at"),("task_comments","created_at"),("tasks","created_at")):
    row = cur.execute(f"SELECT MAX({col}) m, COUNT(*) c FROM {tbl}").fetchone()
    age_min = (now - row["m"]) / 60.0 if row["m"] else -1
    print(f"{tbl}: rows={row['c']} newest_age_min={age_min:.1f}")

# 3) Rekonsiliasi scan() kanonis
print("== SCAN() KANONIS ==")
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = mod.DEFAULT_AUTHORS
if isinstance(authors, str):
    authors = authors.split(",")
findings = mod.scan(DB, now, authors)
print(f"temuan={len(findings)}")
for f in findings:
    print("ROW:", f)

# 4) Sensus kartu terbuka non-done/archived: id, status, tenant, block_kind, umur event terakhir, marker koreksi
print("== TERBUKA (non done/archived) ==")
rows = cur.execute("""
  SELECT id, status, tenant, block_kind, title, created_at
  FROM tasks
  WHERE status NOT IN ('done','archived')
  ORDER BY tenant, status
""").fetchall()
ids = [r["id"] for r in rows]
for r in rows:
    cid = r["id"]
    ev = con.cursor().execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()["m"]
    cm = con.cursor().execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id=?", (cid,)).fetchone()["m"]
    last = max([x for x in (ev, cm, r["created_at"]) if x] or [0])
    fixer = con.cursor().execute(
        "SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%[SYSMAN-CLEANER%' OR body LIKE '%RANTAI-WAKE%')",
        (cid,)).fetchone()["n"]
    age_h = (now - last)/3600.0
    print(f"{cid} | {r['status']} | tenant={r['tenant']} | bk={r['block_kind']} | last_ev_age_h={age_h:.1f} | fixmark={fixer} | {r['title'][:60]}")

# 5) Blind spot rute-4b: kartu running dengan LAPOR-SELESAI tanpa ACK author lain
print("== BLINDSPOT RUNNING ==")
run = cur.execute("SELECT id, title, tenant, last_heartbeat_at FROM tasks WHERE status='running'").fetchall()
print(f"running_count={len(run)}")
for r in run:
    cid = r["id"]
    hb_age = (now - r["last_heartbeat_at"])/60.0 if r["last_heartbeat_at"] else -1
    lap = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%')", (cid,)).fetchone()["n"]
    ack = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (cid,)).fetchone()["n"]
    print(f"{cid} | hb_age_min={hb_age:.1f} | lap={lap} ack={ack} | tenant={r['tenant']} | {r['title'][:60]}")
con.close()
