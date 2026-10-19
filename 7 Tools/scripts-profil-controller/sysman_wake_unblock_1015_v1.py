# Which cards got unblocked events (tenant VBCB) — sysman cron 15-10 read-only
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
def age(ts): return "%.0fm" % ((now-ts)/60) if ts else "-"

print("=== unblocked events (tenant VBCB) ===")
for r in con.execute("""SELECT e.task_id, e.created_at, t.status, substr(t.title,1,50) ti
FROM task_events e JOIN tasks t ON t.id=e.task_id
WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='unblocked' ORDER BY e.created_at DESC"""):
    print(f"  {r['task_id']} unblock@{age(r['created_at'])} ago now_status={r['status']} :: {r['ti']}")

print("\n=== M4 resume cards: created_at distribution ===")
for r in con.execute("""SELECT substr(title,1,30) ti, status, created_at, completed_at FROM tasks
WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%(resume)%' ORDER BY created_at DESC LIMIT 6"""):
    print(f"  {r['status']} created={age(r['created_at'])} done={age(r['completed_at'])} :: {r['ti']}")

print("\n=== verification todo cards: any promoted recently? (status != todo among W1-W4 Verifikasi) ===")
rows = con.execute("""SELECT id,status,title FROM tasks WHERE tenant='VIBE-BIBLE-1013'
AND title LIKE '%Verifikasi bab%'""").fetchall()
from collections import Counter
print("  census:", dict(Counter(r['status'] for r in rows)))
