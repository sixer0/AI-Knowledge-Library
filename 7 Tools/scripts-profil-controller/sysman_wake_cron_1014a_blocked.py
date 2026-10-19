# Full detail of all 10 blocked cards + 1 scheduled card: last events, comments (last 3), parents/children.
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
now = time.time()
def age(ts): return int((now - ts)/60) if ts else None

rows = list(cur.execute("SELECT * FROM tasks WHERE status IN ('blocked','scheduled')"))
print("COUNT", len(rows))
for r in rows:
    print("="*100)
    print(f"{r['id']} | [{r['status']}] block_kind={r['block_kind']} recur={r['block_recurrences']} | tenant={r['tenant']} | assignee={r['assignee']} | created={age(r['created_at'])}m")
    print(f"TITLE: {r['title'][:110]}")
    body = (r['body'] or '')[:400].replace('\n',' / ')
    print(f"BODY: {body}")
    lastevs = list(cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (r['id'],)))
    print("LAST_EVENTS:", [(e['kind'], age(e['created_at'])) for e in lastevs])
    cs = list(cur.execute("SELECT author, created_at, substr(body,1,140) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (r['id'],)))
    for c in cs:
        print(f"  C[{age(c['created_at'])}m] {c['author']}: {c['b']}")
    if not cs:
        print("  (no comments)")
    par = [p['parent_id'] for p in cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (r['id'],))]
    chi = [c['child_id'] for c in cur.execute("SELECT child_id FROM task_links WHERE parent_id=?", (r['id'],))]
    print("PARENTS:", par, "CHILDREN:", len(chi))
