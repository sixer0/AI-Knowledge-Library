# Read-only: schema + board sanity census for mission-wake round 14-10b
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
cur = con.cursor()

print("== SCHEMA ==")
for t in ("tasks", "task_events", "task_comments", "task_links"):
    try:
        cols = [r[1] for r in cur.execute(f"PRAGMA table_info({t})")]
        print(t, "->", cols)
    except Exception as e:
        print(t, "ERR", e)

now = int(time.time())
print("\n== SANITY ==")
n_tasks = cur.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
n_ev = cur.execute("SELECT COUNT(*) FROM task_events").fetchone()[0]
n_cm = cur.execute("SELECT COUNT(*) FROM task_comments").fetchone()[0]
max_ev = cur.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
max_cm = cur.execute("SELECT MAX(created_at) FROM task_comments").fetchone()[0]
print("tasks=%d events=%d comments=%d" % (n_tasks, n_ev, n_cm))
print("last event age_min=%.1f" % ((now - (max_ev or 0)) / 60.0))
print("last comment age_min=%.1f" % ((now - (max_cm or 0)) / 60.0))

print("\n== STATUS CENSUS (all boards) ==")
for st, c in cur.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status ORDER BY 2 DESC"):
    print(f"{st}: {c}")

print("\n== OPEN TASKS BY TENANT (todo/running/blocked/in_progress/parked) ==")
for tn, c in cur.execute(
    "SELECT COALESCE(NULLIF(tenant,''),'(null)'), COUNT(*) FROM tasks "
    "WHERE status IN ('todo','running','blocked','in_progress','parked','ready') "
    "GROUP BY 1 ORDER BY 2 DESC LIMIT 40"
):
    print(f"{tn}: {c}")

print("\n== EVENT KINDS LAST 12H ==")
for k, c in cur.execute(
    "SELECT kind, COUNT(*) FROM task_events WHERE created_at >= ? GROUP BY kind ORDER BY 2 DESC",
    (now - 12 * 3600,),
):
    print(f"{k}: {c}")
con.close()
