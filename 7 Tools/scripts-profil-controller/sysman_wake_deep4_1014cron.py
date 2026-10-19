# Round 4: created_by of 24 JEDA cards + exact counts for report.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def d(sql, args=()):
    cur = con.cursor()
    cur.execute(sql, args)
    return cur.fetchall()

rows = d("""SELECT t.created_by, COUNT(*) n FROM tasks t
            WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked'
            GROUP BY t.created_by""")
print("blocked-by-creator:", [(r["created_by"], r["n"]) for r in rows])
rows2 = d("""SELECT t.created_by, COUNT(*) n FROM tasks t
             WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='todo' GROUP BY t.created_by""")
print("todo-by-creator:", [(r["created_by"], r["n"]) for r in rows2])
# blocked cards WITHOUT JEDA reason as last-blocked event (the other 33 blocked total?)
tot = d("SELECT COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'")[0]["n"]
jed = d("""SELECT COUNT(DISTINCT e.task_id) n FROM task_events e JOIN tasks t ON t.id=e.task_id
           WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' AND e.payload LIKE '%JEDA-GELOMBONG%'""")[0]["n"]
print(f"blocked total={tot} with-JEDA={jed}")
nonj = d("""SELECT t.id, substr(t.title,1,60) ti FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked'
            AND t.id NOT IN (SELECT e.task_id FROM task_events e WHERE e.payload LIKE '%JEDA-GELOMBONG%')""")
for r in nonj:
    hb = d("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],))[0]["m"]
    print(f"  non-JEDA blocked {r['id']} ev@{round((now-(hb or now))/60)}m :: {r['ti']}")
