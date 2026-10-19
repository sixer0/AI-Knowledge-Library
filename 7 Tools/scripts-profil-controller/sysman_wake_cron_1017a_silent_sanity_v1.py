# Ronde senyap 17-10: sanity papan hidup + replika scan() + sensus terbuka + blind-spot running
import sqlite3, time, os, importlib.util, json, sys

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

now = int(time.time())

print("=== SENSUS STATUS ===")
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"{r['status']}: {r['n']}")

print("=== VOLUME BARIS ===")
for t in ("tasks", "task_events", "task_comments", "task_runs"):
    try:
        n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t}: {n}")
    except Exception as e:
        print(f"{t}: ERR {e}")

print("=== KESEGARAN (MAX created_at) ===")
for t, col in (("task_events", "created_at"), ("task_comments", "created_at")):
    try:
        mx = cur.execute(f"SELECT MAX({col}) FROM {t}").fetchone()[0]
        print(f"{t} terbaru: {round((now - mx)/60.0, 1)} menit lalu" if mx else f"{t}: KOSONG")
    except Exception as e:
        print(f"{t}: ERR {e}")

# heartbeat terbaru pada kartu running
try:
    hb = cur.execute("SELECT MAX(last_heartbeat_at) FROM tasks WHERE status='running'").fetchone()[0]
    print(f"heartbeat running terbaru: {round((now - hb)/60.0, 1)} menit lalu" if hb else "heartbeat running: tidak ada kartu running")
except Exception as e:
    print(f"heartbeat: ERR {e}")

print("=== SCAN() KANONIS (importlib) ===")
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
findings = mod.scan(DB, now, authors)
print(f"temuan scan(): {len(findings)}")
for f in findings:
    print("  FINDING:", tuple(f) if not isinstance(f, tuple) else f)

print("=== KARTU TERBUKA (bukan done/archived) per status, umur event terakhir ===")
rows = [dict(r) for r in cur.execute("""
    SELECT t.id, t.status, t.title, t.tenant,
           (SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id) last_ev
    FROM tasks t WHERE t.status NOT IN ('done','archived')
    ORDER BY t.status, last_ev DESC""")]
print("total terbuka:", len(rows))
for r in rows[:60]:
    age = round((now - r["last_ev"]) / 60.0, 1) if r["last_ev"] else None
    print(f"{r['status']:8s} {r['id']} ev={age}m tenant={r['tenant']} :: {(r['title'] or '')[:70]}")

print("=== BLIND SPOT: running dengan LAPOR tanpa ACK ===")
run_rows = [dict(r) for r in cur.execute("SELECT id, title, tenant, last_heartbeat_at FROM tasks WHERE status='running'")]
for r in run_rows:
    cid = r["id"]
    lap = cur.execute("SELECT COUNT(*), MAX(created_at) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (cid,)).fetchone()
    ack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (cid,)).fetchone()[0]
    if lap[0] and ack == 0:
        print(f"CANDIDATE {cid} lap={lap[0]} ack=0 hb={round((now-(r['last_heartbeat_at'] or 0))/60.0,1)}m :: {(r['title'] or '')[:60]}")
if not run_rows:
    print("(nol kartu running)")

con.close()
