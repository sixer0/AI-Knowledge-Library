# Read-only eval: heartbeat/events for 2 running LAPOR nodes + tenant census KORPUS-LANJUTAN-1011
import sqlite3, time, os, json

db = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(db)
con.row_factory = sqlite3.Row
now = time.time()

ids = ["t_ed4b57fd", "t_4b4069db"]
for tid in ids:
    r = con.execute("SELECT id,status,assignee,last_heartbeat_at,started_at,current_run_id FROM tasks WHERE id=?", (tid,)).fetchone()
    hb = r["last_heartbeat_at"]
    hb_age = (now - hb) / 60 if hb else -1
    print(f"[{tid}] status={r['status']} assignee={r['assignee']} heartbeat_age_min={'%.1f' % hb_age if hb else 'NONE'}")
    evs = con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)).fetchall()
    for e in evs:
        print(f"   event {e['kind']} age_min=%.1f" % ((now - e["created_at"]) / 60))
    cmts = con.execute("SELECT author,substr(body,1,40) b,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)).fetchall()
    for c in cmts:
        print(f"   comment {c['author']} age_min=%.1f :: %s" % ((now - c["created_at"]) / 60, c["b"].replace(chr(10), " ")))

print("--- tenant census KORPUS-LANJUTAN-1011 ---")
rows = con.execute("SELECT status,COUNT(*) n FROM tasks WHERE tenant='KORPUS-LANJUTAN-1011' GROUP BY status").fetchall()
for r in rows:
    print(f"   {r['status']} = {r['n']}")
open_cards = con.execute("SELECT id,status,title FROM tasks WHERE tenant='KORPUS-LANJUTAN-1011' AND status IN ('todo','blocked','running') ORDER BY created_at").fetchall()
for r in open_cards:
    print(f"   OPEN [{r['id']}] {r['status']} :: {r['title'][:70]}")

# ACK presence check: any RANTAI-ACK comment by author != LAPOR author on the two nodes
for tid in ids:
    ack = con.execute("SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at", (tid,)).fetchall()
    print(f"[{tid}] RANTAI-ACK count = {len(ack)}")
con.close()
