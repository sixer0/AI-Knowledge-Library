# Deep-dive VIBE-BIBLE-1013: blocked reasons, comments, run outcomes, tenant census.
import sqlite3, time, json, collections

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def d(sql, args=()):
    cur = con.cursor()
    cur.execute(sql, args)
    return cur.fetchall()

# 1. Tenant census full
cen = d("SELECT status, COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status")
print("CENSUS VIBE-BIBLE-1013:", {r["status"]: r["n"] for r in cen})

# 2. Blocked reason sample from task_events payload (one M4 card + distinct reasons across tenant)
evs = d("""SELECT e.task_id, e.kind, e.payload, e.created_at FROM task_events e
           JOIN tasks t ON t.id=e.task_id
           WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind IN ('blocked','timed_out','gave_up','promoted')
           ORDER BY e.created_at DESC LIMIT 12""")
for r in evs:
    p = (r["payload"] or "")[:300].replace("\n", " ")
    print(f"EVT {r['task_id']} {r['kind']} @{round((now-r['created_at'])/60)}m :: {p}")

print()
reasons = d("""SELECT substr(e.payload,1,200) pr, COUNT(*) n FROM task_events e
               JOIN tasks t ON t.id=e.task_id
               WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='blocked'
               GROUP BY pr ORDER BY n DESC LIMIT 8""")
for r in reasons:
    print(f"REASON x{r['n']}: {(r['pr'] or '')[:200]}")

# 3. Comments on 2 M4 blocked cards (latest 6 each)
for tid in ("t_0913266d", "t_896447e4"):
    print(f"\n--- comments {tid} ---")
    for c in d("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)):
        print(f"[{round((now-c['created_at'])/60)}m] {c['author']}: {(c['body'] or '')[:280]}")

# 4. Run outcomes for tenant (task_runs if exists)
tabs = [r["name"] for r in d("SELECT name FROM sqlite_master WHERE type='table'")]
if "task_runs" in tabs:
    ro = d("""SELECT r.status, COUNT(*) n, MAX(r.updated_at) mx FROM task_runs r
              JOIN tasks t ON t.id=r.task_id
              WHERE t.tenant='VIBE-BIBLE-1013' GROUP BY r.status""")
    print("\nRUNS:", [(r["status"], r["n"], round((now - (r["mx"] or now))/60)) for r in ro])

# 5. Outlier t_edb280b5 + its parent chain
for tid in ("t_edb280b5", "t_4edfcf3a"):
    t = d("SELECT id,title,status,created_at,assignee FROM tasks WHERE id=?", (tid,))
    if t:
        r = t[0]
        print(f"\nCARD {tid} [{r['status']}] created {round((now-r['created_at'])/60)}m assignee={r['assignee']} :: {(r['title'] or '')[:80]}")
        for c in d("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)):
            print(f"   [{round((now-c['created_at'])/60)}m] {c['author']}: {(c['body'] or '')[:200]}")
        for e in d("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)):
            print(f"   ev {e['kind']} @{round((now-e['created_at'])/60)}m")

# 6. Running parents count (W1 writers still running?)
rp = d("""SELECT COUNT(*) n FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='running'""")
print("\nrunning cards in tenant:", rp[0]["n"])
for r in d("SELECT id,title,created_at,assignee FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='running' ORDER BY created_at DESC LIMIT 15"):
    hb = d("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],))
    hbm = round((now - (hb[0]["m"] or now))/60) if hb else None
    print(f"  RUN {r['id']} hb@{hbm}m created {round((now-r['created_at'])/60)}m assignee={r['assignee']} :: {(r['title'] or '')[:70]}")
