# Cek jejak eskalasi t_841f18dc (apakah butir SAH sudah pernah dilaporkan/di-marker)
import sqlite3, os, time
HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB)
cur = con.cursor()
tid = "t_841f18dc"
print("== comments (semua) ==")
for a,b,c in cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)):
    print(f"[{(now-float(c))/60.0:.0f}m] {a}: {b[:400]}")
print("== events ==")
for k,c in cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 12", (tid,)):
    print(f"[{(now-float(c))/60.0:.0f}m] {k}")
print("== marker RANTAI-WAKE lintas seluruh papan (14 hari terakhir) ==")
cut = now - 14*86400
for t,a,b,c in cur.execute("SELECT task_id, author, substr(body,1,60), created_at FROM task_comments WHERE body LIKE '%RANTAI-WAKE%' AND created_at>=? ORDER BY created_at DESC LIMIT 20", (cut,)):
    print(f"[{(now-float(c))/60.0:.0f}m] {t} {a}: {b}")
con.close()
