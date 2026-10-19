# Full comment bodies for the two WAKE cards (read-only).
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
for tid in ("t_26d8e0dc", "t_2da2d99f", "t_c5da3e33", "t_4004a170"):
    print("=" * 72)
    print(tid)
    for c in con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)).fetchall():
        print(f"--- [{round((now-c['created_at'])/60,1)}m ago] {c['author']}:")
        print(c["body"])
con.close()
