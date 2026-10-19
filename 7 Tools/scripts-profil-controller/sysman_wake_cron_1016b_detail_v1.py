# Detail butir nyata 16-10b: isi penuh kartu S22 + C22-PLURAL + cek langganan wake
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\","/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

for tid in ("t_44382333","t_65fb51b1"):
    r = con.execute("SELECT id,title,body,result,status,completed_at,assignee,created_by,goal_mode FROM tasks WHERE id=?",(tid,)).fetchone()
    print("#"*72)
    print(r["id"], "|", r["title"])
    print("status:", r["status"], "| assignee:", r["assignee"], "| created_by:", r["created_by"], "| goal_mode:", r["goal_mode"])
    print("completed age_min:", (now - r["completed_at"])//60)
    print("-- BODY --"); print((r["body"] or "")[:1200])
    print("-- RESULT --"); print((r["result"] or "")[:1500])
    print("-- KOMENTAR PENUH (kronologis) --")
    for c in con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at",(tid,)).fetchall():
        print(f"[{c['author']} {(now-c['created_at'])//60}m]\n{c['body'][:1400]}\n")
    subs = con.execute("SELECT * FROM kanban_notify_subs WHERE task_id=?",(tid,)).fetchall()
    print("-- wake subs:", len(subs), [dict(s) for s in subs][:3])
