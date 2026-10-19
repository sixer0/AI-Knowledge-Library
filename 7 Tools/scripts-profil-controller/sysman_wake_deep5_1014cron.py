# Round 5: t_4edfcf3a LAPOR comments + ACK check (blind-spot on running node).
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def d(sql, args=()):
    cur = con.cursor()
    cur.execute(sql, args)
    return cur.fetchall()

for c in d("SELECT author, body, created_at FROM task_comments WHERE task_id='t_4edfcf3a' ORDER BY created_at DESC LIMIT 8"):
    print(f"[{round((now-c['created_at'])/60)}m] {c['author']}: {(c['body'] or '')[:400]}")
    print("---")
