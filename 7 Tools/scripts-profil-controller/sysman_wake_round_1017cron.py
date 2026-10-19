# Ronde senyap 17-10: sanity papan hidup + replika scan() kanonis + sensus kartu terbuka
import sqlite3, time, os, importlib.util, sys

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
SCAN = r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py"

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

now = int(time.time())

# 1) Sensus status seluruh kartu
print("== SENSUS STATUS ==")
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  {r['status']}: {r['n']}")

# 2) Kesegaran papan: MAX event (BUKAN MIN - preseden 14-10b)
r = cur.execute("SELECT MAX(created_at) mx, COUNT(*) n FROM task_events").fetchone()
age_min = (now - r["mx"]) / 60.0 if r["mx"] else None
print(f"== KESegARAN == event_max_age_min={age_min:.1f} total_events={r['n']}")
for t in ("tasks", "task_comments"):
    n = cur.execute(f"SELECT COUNT(*) c FROM {t}").fetchone()["c"]
    print(f"  {t}={n}")

# 3) Kartu terbuka non-done/archived per status dgn umur event terakhir
print("== KARTU TERBUKA (tidak done/archived) ==")
rows = cur.execute("""
  SELECT t.id, t.status, t.title, t.tenant, t.created_by,
         (SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id) last_ev
  FROM tasks t
  WHERE t.status NOT IN ('done','archived')
  ORDER BY last_ev DESC
""").fetchall()
print(f"  jumlah={len(rows)}")
for r in rows[:40]:
    age = (now - r["last_ev"]) / 60.0 if r["last_ev"] else -1
    print(f"  {r['id']} | {r['status']} | ev_age={age:.0f}m | tenant={r['tenant']} | by={r['created_by']} | {r['title'][:60]}")

# 4) Blind spot: kartu running dengan LAPOR-SELESAI tanpa ACK
run_ids = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE status='running'").fetchall()]
print(f"== BLINDSPOT running={len(run_ids)} ==")
for tid in run_ids:
    c2 = con.cursor()
    lap = c2.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELE%'", (tid,)).fetchone()["c"]
    ack = c2.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    if lap and not ack:
        hb = c2.execute("SELECT last_heartbeat_at FROM tasks WHERE id=?", (tid,)).fetchone()
        hba = (now - hb["last_heartbeat_at"]) / 60.0 if hb and hb["last_heartbeat_at"] else -1
        print(f"  CANDIDATE {tid} lap={lap} ack={ack} hb_age={hba:.1f}m")

# 5) Replika kanonis: panggil scan() modul pemindai (nilai kembali, BUKAN stdout)
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
findings = mod.scan(DB, now, authors)
print(f"== SCAN() KANONIS == temuan={len(findings)}")
for f in findings:
    print("  ", tuple(f) if not isinstance(f, tuple) else f)
con.close()
