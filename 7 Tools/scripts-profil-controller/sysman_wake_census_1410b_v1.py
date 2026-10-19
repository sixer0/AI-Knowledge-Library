# Census tenant VIBE-BIBLE-1013 + board sanity (read-only).
import sqlite3, os, time, json
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()

print("== SENSUS STATUS tenant VIBE-BIBLE-1013 ==")
for r in cur.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    print(f"  {r['status']}: {r['c']}")
print("  total:", cur.execute("SELECT COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchone()["c"])

print("== kartu tenant di luar daftar WAKE (done/blocked tanpa wake) ==")
for r in cur.execute("SELECT id,status,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status NOT IN ('todo','blocked') LIMIT 20"):
    print(f"  {r['id']} [{r['status']}] {r['title'][:70]}")

print("== komentar controller-lain pada kartu blocked sejak 170m lalu ==")
n = 0
for r in cur.execute("""SELECT task_id, author, body, created_at FROM task_comments
    WHERE created_at > ? AND author NOT IN ('gsp-worker','gsp-worker-fast','dispatcher','user','gsp-worker-fast ') 
      AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')
    ORDER BY created_at DESC LIMIT 15""", (now-170*60,)):
    print(f"  {r['task_id']} {r['author']}@{round((now-r['created_at'])/60)}m: {r['body'][:90]}".replace(chr(10),' '))
    n += 1
if n == 0: print("  (tidak ada)")

print("== SANITY papan hidup ==")
e = cur.execute("SELECT MIN(created_at) m FROM task_events").fetchone()["m"]
print("  umur event terbaru papan:", round((now-e)/60), "menit")
print("  jumlah tasks:", cur.execute("SELECT COUNT(*) c FROM tasks").fetchone()["c"])
print("  jumlah events:", cur.execute("SELECT COUNT(*) c FROM task_events").fetchone()["c"])
print("  running saat ini (semua tenant):", cur.execute("SELECT COUNT(*) c FROM tasks WHERE status='running'").fetchone()["c"])
for r in cur.execute("SELECT id,title,tenant FROM tasks WHERE status='running' LIMIT 10"):
    print(f"    run: {r['id']} [{r['tenant']}] {r['title'][:60]}")
