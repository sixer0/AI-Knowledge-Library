# Cek kartu completed <=6h: tenant, author LAPOR vs ACK, marker (rekonsiliasi buta-tutup rute-4b)
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

ids = [r["task_id"] for r in con.execute(
    "SELECT DISTINCT task_id FROM task_events WHERE kind='completed' AND created_at >= ?",
    (now - 6 * 3600,)).fetchall()]
print("completed_ids(<=6h) =", ids)
for cid in ids:
    t = con.execute("SELECT id,status,tenant,title,created_by,completed_at FROM tasks WHERE id=?", (cid,)).fetchone()
    print(f"\ncard={t['id']} status={t['status']} tenant={t['tenant']} by={t['created_by']}")
    print("title:", (t["title"] or "")[:80])
    cs = con.execute("SELECT author,substr(body,1,160) b,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (cid,)).fetchall()
    print("comments:", len(cs))
    for c in cs:
        print(f"  [{(now-c['created_at'])/60.0:.0f}m] {c['author']}: {c['b']!r}")
    r = con.execute("SELECT substr(result,1,300) res FROM tasks WHERE id=?", (cid,)).fetchone()
    print("result:", (r["res"] or "")[:300])
