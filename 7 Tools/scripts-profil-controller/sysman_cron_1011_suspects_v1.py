import sqlite3, os, time
db = os.path.join(os.environ.get("LOCALAPPDATA","C:/Users/TRIAL/AppData/Local"),"hermes","kanban.db")
con = sqlite3.connect(db); con.row_factory = sqlite3.Row
now = time.time()
ids = ["t_ef0a078e","t_9bacb330","t_140e456c","t_5b7a8dd5","t_11db1218","t_10569fbe","t_51ebfa26","t_bcbdbe04"]
for cid in ids:
    r = con.execute("SELECT id,title,status,tenant,assignee,created_by,completed_at FROM tasks WHERE id=?",(cid,)).fetchone()
    age_h = round((now-(r["completed_at"] or 0))/3600,1)
    print(f"== {cid} | {r['title'][:55]} | status={r['status']} | tenant={r['tenant']} | assignee={r['assignee']} | done_age_h={age_h}")
    cmts = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at",(cid,)).fetchall()
    for c in cmts[-4:]:
        ca = round((now-c["created_at"])/3600,1)
        print(f"   [{c['author']} @{ca}h] {c['body'][:130].replace(chr(10),' / ')}")
