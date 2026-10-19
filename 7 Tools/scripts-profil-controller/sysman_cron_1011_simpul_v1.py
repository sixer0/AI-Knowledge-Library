import sqlite3, os, time
db = os.path.join(os.environ.get("LOCALAPPDATA","C:/Users/TRIAL/AppData/Local"),"hermes","kanban.db")
con = sqlite3.connect(db); con.row_factory = sqlite3.Row
now=time.time()
for cid in ["t_fb685c56"]:
    cmts = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at",(cid,)).fetchall()
    for c in cmts:
        print(f"[{c['author']} @{round((now-c['created_at'])/3600,1)}h] {c['body'][:200].replace(chr(10),' / ')}")
