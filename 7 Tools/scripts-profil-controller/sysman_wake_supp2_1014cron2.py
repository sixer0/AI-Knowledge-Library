# Read-only: detail on newly-surfaced done-unacked cards + t_ed9976be children weight.
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

for tid in ("t_b10a1e32", "t_eb458a5e", "t_4edfcf3a"):
    c = con.cursor()
    t = c.execute("SELECT id,title,status,tenant,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    print(f"{tid} | {t['status']} | tenant={t['tenant']} | completed_age={round((NOW-t['completed_at'])/60) if t['completed_at'] else '-'}m")
    print(f"   title: {t['title'][:90]}")
    for row in c.execute("SELECT author,SUBSTR(body,1,110) b,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)):
        print(f"   @{round((NOW-row['created_at'])/60)}m {row['author']}: {row['b'].replace(chr(10),' ')}")

# children of t_ed9976be (running blind spot) - transitive open descendants
print("== descendants t_ed9976be ==")
c = con.cursor()
seen = set(); frontier = ["t_ed9976be"]; depth = 0
while frontier and depth < 6:
    nxt = []
    for p in frontier:
        for row in c.execute("SELECT child_id FROM task_links WHERE parent_id=?", (p,)):
            if row['child_id'] in seen: continue
            seen.add(row['child_id'])
            ct = c.execute("SELECT status,title FROM tasks WHERE id=?", (row['child_id'],)).fetchone()
            nxt.append(row['child_id'])
    frontier = nxt; depth += 1
open_desc = [d for d in seen if c.execute("SELECT status FROM tasks WHERE id=?", (d,)).fetchone()['status'] in ('todo','ready','blocked','running')]
print(f"descendants_total={len(seen)} open={len(open_desc)}")
