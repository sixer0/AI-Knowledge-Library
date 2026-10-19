# Read-only probe: two zero-ACK done cards vs route-4b gates (tenant blind spot check).
import sqlite3, os, time
DB = os.path.join(os.path.expandvars(r"C:/Users/TRIAL/AppData/Local/hermes"), "kanban.db")
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
now = time.time()
for tid in ["t_52521c3b", "t_c08057c4"]:
    t = con.execute("SELECT id,title,status,tenant,assignee,created_by,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    print(f"\n{tid} | {t['title'][:70]}")
    print(f"  status={t['status']} tenant={t['tenant']!r} assignee={t['assignee']} author={t['created_by']} done_age_m={round((now-float(t['completed_at']))/60,1) if t['completed_at'] else None}")
    for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)):
        print(f"  [{round((now-float(c['created_at']))/60,1)}m] {c['author']}: {c['body'][:130].replace(chr(10),' ')}")
# census: semua kartu done 24 jam terakhir tanpa komentar sama sekali
print("\n-- done 24j tanpa komentar --")
for r in con.execute("""SELECT t.id,t.title,t.tenant,t.completed_at FROM tasks t
  WHERE t.status='done' AND t.completed_at >= ? 
  AND NOT EXISTS (SELECT 1 FROM task_comments c WHERE c.task_id=t.id)
  ORDER BY t.completed_at DESC LIMIT 20""", (now-86400,)):
    print(f"  {r['id']} tenant={r['tenant']!r} age={round((now-float(r['completed_at']))/60,1)}m | {r['title'][:60]}")
con.close()
