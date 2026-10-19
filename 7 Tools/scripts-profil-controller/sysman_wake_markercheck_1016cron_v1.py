# Inspect marker class/timing vs completion for the two freshly-done cards.
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
for i in ("t_1837ce19", "t_050e08e8"):
    r = con.execute("SELECT id,status,title,completed_at FROM tasks WHERE id=?", (i,)).fetchone()
    print("=" * 60)
    print(f"{i} status={r['status']} completed_age_min={round((now-r['completed_at'])/60,1)}")
    print("title:", r["title"][:90])
    cs = con.execute(
        "SELECT author,created_at,body FROM task_comments WHERE task_id=? ORDER BY created_at",
        (i,)).fetchall()
    for c in cs:
        print(f"  [{round((now-c['created_at'])/60,1)}m] {c['author']}: {(c['body'] or '')[:150]!r}")
con.close()
