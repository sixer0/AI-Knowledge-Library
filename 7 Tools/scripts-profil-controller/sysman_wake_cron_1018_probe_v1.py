# Rekonsiliasi kandidat blind-spot t_491531fd vs gerbang rute-4b
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
tid = "t_491531fd"
t = con.execute("SELECT id,title,status,tenant,assignee,created_by,completed_at,result FROM tasks WHERE id=?", (tid,)).fetchone()
print("id=%s status=%s tenant=%r assignee=%r created_by=%s" % (t["id"], t["status"], t["tenant"], t["assignee"], t["created_by"]))
print("title:", (t["title"] or "")[:90])
print("completed_at age_min =", round((now - t["completed_at"]) / 60.0, 1) if t["completed_at"] else None)
print("result:", ((t["result"] or "")[:200]).replace("\n", " "))
print("-- comments --")
for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)):
    print(f"[{round((now-c['created_at'])/60,1)}m] {c['author']}: {(c['body'] or '')[:120]}".replace("\n", " "))
print("-- events --")
for e in con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 8", (tid,)):
    print(f"{e['kind']} @ {round((now-e['created_at'])/60,1)}m")
