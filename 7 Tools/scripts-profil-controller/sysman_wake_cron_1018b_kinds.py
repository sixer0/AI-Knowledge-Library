import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
now = int(time.time())
print("-- event kinds 24j terakhir (seluruh papan) --")
for r in cur.execute("SELECT kind, COUNT(*) c, MAX(created_at) m FROM task_events WHERE created_at >= ? GROUP BY kind ORDER BY c DESC", (now-86400,)):
    print(f"  {r['kind']:<16} n={r['c']:<4} terbaru={round((now-r['m'])/60,1)}m")
print("-- event VBCB 24j: author/kind per jam terakhir --")
for r in cur.execute("SELECT e.kind, COUNT(*) c FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.created_at >= ? GROUP BY e.kind", (now-86400,)):
    print(f"  VBCB {r['kind']} = {r['c']}")
print("-- komentar baru (bukan alat cleaner) 6j terakhir --")
for r in cur.execute("SELECT task_id, author, substr(body,1,70) b, created_at FROM task_comments WHERE created_at >= ? AND author NOT IN ('sysmanager-cleaner','gsp-system-manager') ORDER BY created_at DESC LIMIT 15", (now-21600,)):
    print(f"  {round((now-r['created_at'])/60,1)}m {r['author']} @{r['task_id'][:10]} | {r['b'][:60]}")
