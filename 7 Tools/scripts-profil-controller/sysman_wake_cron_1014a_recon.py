# Reconcile blocked census + recheck done-unacked candidate t_009f2fdc marker/ACK state.
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
now = time.time()
def age(ts): return int((now - ts)/60) if ts else None

print("STATUS CENSUS NOW:")
for st, n in cur.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status"):
    print(" ", st, n)

print("BLOCKED DETAIL NOW:")
for r in cur.execute("SELECT id,title,status,tenant,created_at,assignee FROM tasks WHERE status='blocked'"):
    lastev = cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    ntri = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%[FASE]%' OR body LIKE '%TRIASE%' OR body LIKE '%DITAHAN%')", (r["id"],)).fetchone()[0]
    print(f"  {r['id']} | tenant={r['tenant']} | created={age(r['created_at'])}m lastev={(lastev['kind'], age(lastev['created_at'])) if lastev else None} TRIASE={ntri} | {r['title'][:70]}")

print("t_009f2fdc COMMENTS:")
for c in cur.execute("SELECT author, created_at, substr(body,1,110) b FROM task_comments WHERE task_id='t_009f2fdc' ORDER BY created_at"):
    print(f"  [{age(c['created_at'])}m] {c['author']}: {c['b']}")
