# Final state check of the two blind-spot nodes before handoff.
import sqlite3, os, time
ROOT = r"C:/Users/TRIAL/AppData/Local/hermes"
con = sqlite3.connect(os.path.join(ROOT, "kanban.db"))
con.row_factory = sqlite3.Row
cur = con.cursor()
now = time.time()
for cid in ("t_e5746787", "t_fb685c56"):
    r = cur.execute("SELECT id,status,completed_at,last_heartbeat_at FROM tasks WHERE id=?", (cid,)).fetchone()
    d = dict(r)
    cs = cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (cid,)).fetchall()
    acks = [c for c in cs if 'RANTAI-ACK' in c['body']]
    prints = [c for c in cs if 'PARKED' in c['body']]
    print(f"{cid} status={d['status']} completed={d['completed_at']} hb_age={int(now-d['last_heartbeat_at'])//60 if d['last_heartbeat_at'] else None}m "
          f"acks={[(c['author'], int(now-c['created_at'])//60) for c in acks]} parked={len(prints)} last_comment={cs[-1]['author']}/{int(now-cs[-1]['created_at'])//60}m:{cs[-1]['body'][:80]}")
