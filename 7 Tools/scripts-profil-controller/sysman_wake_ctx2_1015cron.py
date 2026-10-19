# Probe: unblock activity + blocked reasons for VBCB (read-only).
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
q = lambda sql, a=(): [dict(r) for r in con.execute(sql, a).fetchall()]

cols = [c["name"] for c in q("PRAGMA table_info(tasks)")]
print("task cols:", cols)

ub = q("""SELECT e.task_id, e.created_at FROM task_events e JOIN tasks t ON t.id=e.task_id
          WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='unblocked' AND e.created_at >= ?
          ORDER BY e.created_at DESC LIMIT 20""", (now-6*3600,))
print("unblocked events last6h:", len(ub), [(u["task_id"], round((now-u["created_at"])/60)) for u in ub])

# blocked cards: last event age + last comment snippet
bl = q("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' ORDER BY created_at")
print("blocked count:", len(bl))
for b in bl[:6]:
    ev = q("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (b["id"],))
    lc = q("SELECT author,substr(body,1,100) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (b["id"],))
    print("BLK", b["id"], b["title"][:55], "| ev", [(e["kind"], round((now-e["created_at"])/60)) for e in ev], "| cmt", [(c["author"], c["b"].replace(chr(10),' ')[:80]) for c in lc])
