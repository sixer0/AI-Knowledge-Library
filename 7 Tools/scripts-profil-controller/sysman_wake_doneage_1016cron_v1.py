# Why did the other 8 done-unacked cards not surface? completed age + marker presence.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
ids = ["t_8ded3fd6","t_7dbaae0b","t_6c0f26be","t_cabfb238","t_579d86f2",
       "t_5b68a0be","t_1837ce19","t_050e08e8","t_0a75080c"]
for i in ids:
    r = con.execute("SELECT id,completed_at FROM tasks WHERE id=?", (i,)).fetchone()
    mk = con.execute(
        "SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'",
        (i,)).fetchone()["n"]
    wk = con.execute(
        "SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
        (i,)).fetchone()["n"]
    ca = r["completed_at"]
    print(f"{i} done_age_h={round((now-ca)/3600,1)} wake_markers={mk} ack={wk}")
con.close()
