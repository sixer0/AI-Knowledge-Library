# Resolve blocked-count mismatch (status variants), inspect scheduled card, list all non-standard-status tasks.
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
now = time.time()
def age(ts): return int((now - ts)/60) if ts else None

print("STATUS VARIANTS (bracketed):")
for st, n in cur.execute("SELECT '['||status||']' s, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  {st} {n}")

print("TRIM-MATCH blocked:")
for r in cur.execute("SELECT id,status,title,tenant,created_at FROM tasks WHERE trim(status)='blocked' AND status<>'blocked'"):
    print(f"  {r['id']} | [{r['status']}] | tenant={r['tenant']} | created={age(r['created_at'])}m | {r['title'][:70]}")

print("SCHEDULED:")
for r in cur.execute("SELECT id,status,title,tenant,created_at,assignee FROM tasks WHERE trim(status)='scheduled'"):
    print(f"  {r['id']} | [{r['status']}] | tenant={r['tenant']} | created={age(r['created_at'])}m | assignee={r['assignee']} | {r['title'][:70]}")
