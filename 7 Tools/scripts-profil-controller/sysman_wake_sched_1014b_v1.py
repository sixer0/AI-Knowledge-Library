import sqlite3, time
con = sqlite3.connect(r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db")
con.row_factory = sqlite3.Row
now = int(time.time())
for run in con.execute("SELECT id,status,outcome,started_at,ended_at,error FROM task_runs WHERE task_id='t_689662c9' ORDER BY rowid"):
    d = dict(run)
    for k in ("started_at","ended_at"):
        if d.get(k): d[k] = time.strftime("%m-%d %H:%M", time.localtime(d[k]))
    print(d)
for c in con.execute("SELECT author, substr(body,1,160) b, created_at FROM task_comments WHERE task_id='t_689662c9' ORDER BY created_at DESC LIMIT 4"):
    print("[", time.strftime("%m-%d %H:%M", time.localtime(c["created_at"])), "]", c["author"], ":", (c["b"] or "").replace("\n"," | ")[:150])
evs = con.execute("SELECT kind, MAX(created_at) m FROM task_events WHERE task_id='t_689662c9' GROUP BY kind ORDER BY m DESC").fetchall()
print("events:", [(e["kind"], time.strftime("%m-%d %H:%M", time.localtime(e["m"]))) for e in evs])
