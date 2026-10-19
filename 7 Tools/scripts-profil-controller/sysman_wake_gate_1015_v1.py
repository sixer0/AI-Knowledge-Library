# Confirm gating structure of the 33 todo verification cards — sysman cron 15-10 read-only
import sqlite3, time
from collections import Counter
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
def age(ts): return "%.0fm" % ((now-ts)/60) if ts else "-"

# A) event kinds seen on a sample blocked writer card
print("=== event kinds for blocked writers (sample 3) ===")
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' LIMIT 3")]
for cid in ids:
    ks = con.execute("SELECT kind, COUNT(*) c, MAX(created_at) mc FROM task_events WHERE task_id=? GROUP BY kind", (cid,)).fetchall()
    print(f"  {cid}: " + "; ".join(f"{r['kind']}x{r['c']}@{age(r['mc'])}" for r in ks))

# B) parent-status census for ALL todo cards in tenant
print("\n=== todo cards parent census ===")
pat = Counter()
for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo'"):
    ps = [p["status"] for p in con.execute("""SELECT t.status FROM task_links l JOIN tasks t ON t.id=l.parent_id WHERE l.child_id=?""", (r["id"],))]
    pat[tuple(sorted(ps))] += 1
for k, c in pat.most_common():
    print(f"  x{c}: parents={k}")

# C) Verifikasi census overall
rows = con.execute("SELECT status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%Verifikasi bab%'").fetchall()
print("\nVerifikasi bab census:", dict(Counter(r["status"] for r in rows)))

# D) M4 resume cards census
rows = con.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%(resume)%' GROUP BY status").fetchall()
print("M4 resume census:", {r["status"]: r["c"] for r in rows})

# E) blocked writers: consecutive_failures / last_failure_error sample + max_runtime
r = con.execute("""SELECT consecutive_failures, max_runtime_seconds, COUNT(*) c FROM tasks
WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' GROUP BY consecutive_failures, max_runtime_seconds""").fetchall()
for x in r: print(f"blocked group: consec_fail={x['consecutive_failures']} cap={x['max_runtime_seconds']} n={x['c']}")

# F) last dispatcher/controller comment on any blocked writer (triase trail?)
print("\n=== comments on blocked writers (last 5 across all) ===")
for c in con.execute("""SELECT tc.task_id, tc.author, tc.created_at, substr(tc.body,1,140) b
FROM task_comments tc JOIN tasks t ON t.id=tc.task_id
WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' ORDER BY tc.created_at DESC LIMIT 5"""):
    print(f"  {c['task_id']} [{age(c['created_at'])}] {c['author']}: {c['b'][:120].replace(chr(10),' | ')}")
