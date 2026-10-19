# Read-only sanity: MAX(created_at) on events/comments vs now, plus open-card census.
import sqlite3, time, os

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

def max_age(table, col="created_at"):
    r = cur.execute(f"SELECT MAX({col}) AS m, COUNT(*) AS n FROM {table}").fetchone()
    if r["m"] is None:
        return ("EMPTY", 0)
    return (round((now - int(r["m"])) / 60.0, 1), int(r["n"]))

for t in ("task_events", "task_comments"):
    age, n = max_age(t)
    print(f"{t}: rows={n} last_age_min={age}")
cols = [r[1] for r in cur.execute("PRAGMA table_info(task_runs)").fetchall()]
print("task_runs cols:", cols)

r = cur.execute("SELECT COUNT(*) AS n FROM tasks WHERE status NOT IN ('done','archived','cancelled')").fetchone()
print(f"open_tasks(non-done/archived)={r['n']}")
for row in cur.execute("SELECT status, COUNT(*) AS n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  {row['status']} = {row['n']}")

# blocked cards: age of last event per card, top 10 oldest
print("-- blocked cards, last-event age (min), top 10 --")
ids = [row["id"] for row in cur.execute("SELECT id FROM tasks WHERE status='blocked'")]
rows = []
for tid in ids:
    e = cur.execute("SELECT MAX(created_at) AS m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    c = cur.execute("SELECT MAX(created_at) AS m FROM task_comments WHERE task_id=?", (tid,)).fetchone()["m"]
    last = max([v for v in (e, c) if v], default=None)
    age = round((now - int(last)) / 60.0, 0) if last else None
    title = cur.execute("SELECT title FROM tasks WHERE id=?", (tid,)).fetchone()["title"]
    mk = cur.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["n"]
    rows.append((age if age is not None else 9e9, tid, title, mk))
rows.sort(reverse=True)
for age, tid, title, mk in rows[:10]:
    print(f"  {tid} age={age} marker={mk} :: {title[:70]}")
con.close()
