import sqlite3, os, time
db = os.path.join(os.environ.get("LOCALAPPDATA","C:/Users/TRIAL/AppData/Local"),"hermes","kanban.db")
con = sqlite3.connect(db); con.row_factory = sqlite3.Row
now=time.time()
print("event_cols:", [c[1] for c in con.execute("PRAGMA table_info(task_events)")])
ids=["t_9bacb330","t_140e456c","t_5b7a8dd5","t_11db1218","t_10569fbe"]
for cid in ids:
    print(f"== {cid}")
    evs = con.execute("SELECT * FROM task_events WHERE task_id=? ORDER BY created_at",(cid,)).fetchall()
    for e in evs[-5:]:
        d=dict(e); age_h=round((now-d.get('created_at',0))/3600,1)
        d.pop('created_at',None)
        print("   EV", {k:(str(v)[:70]) for k,v in d.items()}, f"@{age_h}h")
    links = con.execute("SELECT parent_id,child_id FROM task_links WHERE parent_id=? OR child_id=?",(cid,cid)).fetchall()
    for l in links:
        p,c = l["parent_id"], l["child_id"]
        other = c if p==cid else p
        r = con.execute("SELECT id,title,status,assignee FROM tasks WHERE id=?",(other,)).fetchone()
        role = "PARENT" if p==cid else "CHILD"
        print(f"   {role} {r['id']} [{r['status']}] assignee={r['assignee']} :: {r['title'][:60]}")
