# Read-only census of blocked cards + last comments (cron round 12-10)
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = time.time()

rows = con.execute(
    "SELECT id, title, status, created_at, started_at, completed_at, assignee, tenant "
    "FROM tasks WHERE status NOT IN ('done','archived') ORDER BY created_at DESC"
).fetchall()
print("OPEN_CARDS =", len(rows))
for r in rows:
    print("-" * 70)
    print(f"id={r['id']} status={r['status']} tenant={r['tenant']!r} assignee={r['assignee']!r}")
    print(f"title={r['title'][:110]}")
    age_h = (now - (r['created_at'] or 0)) / 3600
    print(f"created_age_h={age_h:.1f}")
    ev = con.execute(
        "SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3",
        (r["id"],),
    ).fetchall()
    for e in ev:
        print(f"  event {e['kind']} age_min={(now - e['created_at'])/60:.0f}")
    cm = con.execute(
        "SELECT author, substr(body,1,160) b, created_at FROM task_comments "
        "WHERE task_id=? ORDER BY created_at DESC LIMIT 4",
        (r["id"],),
    ).fetchall()
    for c in cm:
        print(f"  comment[{c['author']}] age_min={(now - c['created_at'])/60:.0f} :: {c['b']!r}")
con.close()
