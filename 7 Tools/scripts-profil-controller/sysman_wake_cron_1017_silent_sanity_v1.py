# Ronde senyap 17-10: sanity papan hidup + replika scan() + sensus kartu terbuka
import sqlite3, time, os, importlib.util, sys
from collections import Counter

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
SCAN = r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py"

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

now = int(time.time())

# 1) Kesegaran papan: MAX(created_at) events (BUKAN MIN), jumlah baris
ev = cur.execute("SELECT MAX(created_at) m, COUNT(*) n FROM task_events").fetchone()
tk = cur.execute("SELECT COUNT(*) n FROM tasks").fetchone()
cm = cur.execute("SELECT COUNT(*) n FROM task_comments").fetchone()
print(f"events_max_age_min={(now - ev['m'])/60:.1f} events_total={ev['n']} tasks_total={tk['n']} comments_total={cm['n']}")

# 2) Sensus status terbuka
rows = cur.execute("SELECT status, COUNT(*) n FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status").fetchall()
print("open_census=", dict(Counter({r['status']: r['n'] for r in rows})))

# 3) Kartu running (blind spot rute-4b): umur heartbeat + LAPOR tanpa ACK
run = cur.execute("SELECT id, tenant, last_heartbeat_at, current_run_id FROM tasks WHERE status='running'").fetchall()
print("running_count=", len(run))
for r in run:
    hb = r['last_heartbeat_at']
    hb_age = (now - hb)/60.0 if hb else -1
    cs = cur.execute("SELECT body, author FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 30", (r['id'],)).fetchall()
    bodies = [c['body'] for c in cs]
    lap = any('LAPOR-SELESAI' in b or 'LAPOR SELESAI' in b for b in bodies)
    ack = any('RANTAI-ACK' in b for b in bodies)
    print(f"running id={r['id']} tenant={r['tenant']} hb_age_min={hb_age:.1f} lapor={lap} ack={ack}")

# 4) Re-scan deterministik via importlib scan() (kanonis)
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
sys.modules["wake_scan"] = mod
spec.loader.exec_module(mod)
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(',')
findings = mod.scan(DB, now, authors)
print("scan_findings=", len(findings))
for f in findings:
    print("  FINDING:", tuple(f) if not isinstance(f, tuple) else f)

con.close()
