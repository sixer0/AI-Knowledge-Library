# Final-round probe: tenant/assignee + latest ACK comments for blind-spot candidates.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
ids = ["t_f4de0f1f", "t_5d087ab1"]
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
cur = con.cursor()
now = time.time()
for tid in ids:
    r = cur.execute(
        "SELECT id,status,assignee,tenant,created_by,completed_at,last_heartbeat_at FROM tasks WHERE id=?",
        (tid,),
    ).fetchone()
    print(r[0], "status=", r[1], "assignee=", r[2], "tenant=", repr(r[3]), "created_by=", r[4],
          "completed_at=", r[5], "hb_age_min=%.1f" % ((now - (r[6] or 0)) / 60))
    for c in cur.execute(
        "SELECT author,substr(body,1,160),created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 5",
        (tid,),
    ):
        print("   age=%.1fm %s: %s" % ((now - c[2]) / 60, c[0], c[1].replace("\n", " | ")[:150]))
con.close()
