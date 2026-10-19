# Read-only: detail nodes running ber-LAPOR tanpa ACK (heartbeat age, tenant, ACK census).
import sqlite3, os, time, json, sys

DB = os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = time.time()

ids = sys.argv[1:] or ["t_2d7495cc", "t_0416c049"]
for tid in ids:
    t = con.execute("SELECT id,title,status,assignee,tenant,created_by,started_at,completed_at,last_heartbeat_at,current_run_id,max_runtime_seconds FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(f"[{tid}] NOT FOUND")
        continue
    hb = t["last_heartbeat_at"]
    hb_age = (now - hb) / 60.0 if hb else None
    print(f"[{tid}] status={t['status']} assignee={t['assignee']} tenant={t['tenant']!r} by={t['created_by']}")
    print(f"  title={t['title'][:80]}")
    print(f"  hb_age_min={hb_age:.1f}" if hb_age is not None else "  hb=None")
    print(f"  max_runtime_s={t['max_runtime_seconds']} run={t['current_run_id']}")
    rows = con.execute("SELECT author,substr(body,1,110) b,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 12", (tid,)).fetchall()
    lap = ack = 0
    for r in rows:
        age = (now - r["created_at"]) / 60.0
        if "LAPOR-SELESAI" in r["b"]:
            lap += 1
        if "RANTAI-ACK" in r["b"]:
            ack += 1
        print(f"  c{age:6.1f}m {r['author']}: {r['b'][:100]}")
    print(f"  totals: LAPOR={lap} ACK={ack}")
    evs = con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)).fetchall()
    for e in evs:
        print(f"  e{(now - e['created_at'])/60.0:6.1f}m {e['kind']}")
    print("")
con.close()
