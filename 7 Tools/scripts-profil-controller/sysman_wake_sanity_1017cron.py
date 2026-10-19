# Read-only sanity for mission-wake cron (silent-round protocol, 17-10)
import sqlite3, time, os, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()

print("== STATUS CENSUS ==")
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"{r['status']}: {r['n']}")

print("== TABLE COUNTS ==")
for t in ("tasks", "task_events", "task_comments"):
    try:
        n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t}: {n}")
    except Exception as e:
        print(f"{t}: ERR {e}")

print("== FRESHNESS (MAX created_at) ==")
for t in ("task_events", "task_comments"):
    try:
        mx = cur.execute(f"SELECT MAX(created_at) FROM {t}").fetchone()[0]
        if mx:
            print(f"{t}: newest {int((now - mx)/60)} min ago")
        else:
            print(f"{t}: EMPTY")
    except Exception as e:
        print(f"{t}: ERR {e}")

print("== OPEN CARDS NOT done/archived (detail) ==")
rows = [dict(r) for r in cur.execute(
    "SELECT id, status, title, tenant, created_by FROM tasks "
    "WHERE status NOT IN ('done','archived') ORDER BY status, id")]
print(f"count={len(rows)}")
for r in rows[:60]:
    print(json.dumps(r, ensure_ascii=False))

print("== RUNNING CARDS (blind-spot route-4b check) ==")
run = [dict(r) for r in cur.execute(
    "SELECT id, title, tenant, last_heartbeat_at, current_run_id FROM tasks WHERE status='running'")]
print(f"running={len(run)}")
for r in run:
    hb = r["last_heartbeat_at"]
    age = f"{int((now-hb)/60)} min" if hb else "None"
    cid = r["id"]
    lap = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (cid,)).fetchone()[0]
    ack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (cid,)).fetchone()[0]
    print(f"{cid} hb={age} LAPOR={lap} ACK={ack} tenant={r['tenant']} title={str(r['title'])[:60]}")
con.close()
