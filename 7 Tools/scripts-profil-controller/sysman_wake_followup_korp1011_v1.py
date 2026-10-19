# Read-only follow-up: why t_df6a4a8a (done, ack=0) is not a WAKE row; comment ages on
# running cards t_e5746787 & t_fb685c56 (blind-spot check); cutoff & window checks.
import sqlite3, os, time

ROOT = r"C:/Users/TRIAL/AppData/Local/hermes"
con = sqlite3.connect(os.path.join(ROOT, "kanban.db"))
con.row_factory = sqlite3.Row
cur = con.cursor()
now = time.time()
CUTOFF = 1791630000

for cid in ("t_df6a4a8a", "t_931ae90a", "t_e5746787", "t_fb685c56"):
    r = cur.execute("SELECT id,status,tenant,assignee,created_by,created_at,completed_at,last_heartbeat_at,title FROM tasks WHERE id=?", (cid,)).fetchone()
    if not r:
        print(cid, "NOT FOUND"); continue
    d = dict(r)
    print(f"\n=== {cid} [{d['status']}] tenant={d['tenant']} assignee={d['assignee']} created_by={d['created_by']}")
    print(f"    created={d['created_at']} (>=cutoff? {bool(d['created_at'] and d['created_at']>=CUTOFF)}) completed={d['completed_at']} hb_age={int(now-d['last_heartbeat_at'])//60 if d['last_heartbeat_at'] else None}m")
    print("    title:", (d['title'] or '')[:90])
    cs = cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (cid,)).fetchall()
    for c in cs:
        age = int(now - c['created_at'])//60
        print(f"    comment age={age}m author={c['author']}: {c['body'][:130].replace(chr(10),' | ')}")
    # events after completion
    ev = cur.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (cid,)).fetchall()
    print("    events:", [(e['kind'], int(now-e['created_at'])//60) for e in ev])

# children of t_e034cb5e (who did the child get promoted by?)
print("\nCHILD LINKS of t_e034cb5e:")
try:
    lk = cur.execute("SELECT * FROM task_links WHERE parent_task_id='t_e034cb5e' OR child_task_id='t_e034cb5e'").fetchall()
    for l in lk:
        print("   ", dict(l))
except Exception as e:
    print("   link query err:", e)
ev = cur.execute("SELECT kind,author,payload,created_at FROM task_events WHERE task_id='t_e5746787' ORDER BY created_at LIMIT 6").fetchall()
print("t_e5746787 first events:", [(e['kind'], e['author'], int(now-e['created_at'])//60) for e in ev])
