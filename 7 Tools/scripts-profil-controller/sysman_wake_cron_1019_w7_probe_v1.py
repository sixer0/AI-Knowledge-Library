"""Cek jejak penanda/laporan ronde sebelumnya pada kartu t_841f18dc (W7 gate-close)."""
import os
import sqlite3
import time

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())

for tid in ("t_841f18dc",):
    print(f"== KOMENTAR {tid} (semua, ASC) ==")
    for r in cur.execute(
        "SELECT author, substr(replace(body, char(10), ' '),1,160) b, created_at"
        " FROM task_comments WHERE task_id=? ORDER BY created_at ASC",
        (tid,),
    ):
        print(f"  [{(now - int(r['created_at'])) / 60.0:.0f} mnt] {r['author']}: {r['b']}")
    print(f"== EVENT {tid} (terminal/terakhir) ==")
    for r in cur.execute(
        "SELECT kind, created_at FROM task_events WHERE task_id=?"
        " ORDER BY created_at DESC LIMIT 6",
        (tid,),
    ):
        print(f"  [{(now - int(r['created_at'])) / 60.0:.0f} mnt] {r['kind']}")
con.close()
