# Board sanity + VBCB mission context (read-only).
import sqlite3, time, json
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
q = lambda sql, a=(): [dict(r) for r in con.execute(sql, a).fetchall()]

mx = q("SELECT MAX(created_at) m FROM task_events")[0]["m"]
print("BOARD last event age_min:", round((now - mx)/60))
print("counts tasks:", q("SELECT COUNT(*) c FROM tasks")[0]["c"], "events:", q("SELECT COUNT(*) c FROM task_events")[0]["c"])

# running card in VBCB
for r in q("SELECT id,title,assignee FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='running'"):
    ev = q("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (r["id"],))
    print("RUNNING", r["id"], r["title"][:80], r["assignee"], [(e["kind"], round((now-e["created_at"])/60)) for e in ev])

# controller ACK activity in tenant last 6h
acks = q("""SELECT c.task_id, c.author, c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id
            WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%RANTAI-ACK%' AND c.created_at >= ?""", (now-6*3600,))
print("ACK comments in tenant last 6h:", len(acks), sorted({a["author"] for a in acks}))
# last ACK ever in tenant
lastack = q("""SELECT c.author, c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id
               WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%RANTAI-ACK%' ORDER BY c.created_at DESC LIMIT 3""")
print("last ACKs ever:", [(a["author"], round((now-a["created_at"])/60)) for a in lastack])
# done cards total ack census today (completed last 12h)
dones = q("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done' AND completed_at >= ?", (now-12*3600,))
n_ack = 0
ids = [d["id"] for d in dones]
for i in ids:
    if q("SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' LIMIT 1", (i,)):
        n_ack += 1
print("done last12h:", len(ids), "with ACK:", n_ack)
# blocked sample reasons
bl = q("SELECT id,title,substr(COALESCE(blocked_reason,''),1,80) r FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' LIMIT 5")
for b in bl: print("BLOCKED", b["id"], b["title"][:60], "|", b["r"])
