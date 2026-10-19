# -*- coding: utf-8 -*-
# Isi komentar sebelum marker + reason block utk 9 kartu M4 blocked (stalled ~129m) + t_b10a1e32.
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
IDS = ["t_a66ce30a","t_ad5d8e6f","t_b2b82e31","t_c2180f14","t_ccfca3b8","t_de326482","t_de73c01d","t_deb670d0","t_ed8b0b54","t_b10a1e32"]
def age(ts): return round((NOW-ts)/60.0)
for tid in IDS:
    t = con.execute("SELECT title, status, assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    print("###", tid, "|", (t["title"] or "")[:60], "|", t["status"], "|", t["assignee"])
    rows = con.execute("SELECT author, created_at, substr(body,1,260) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)).fetchall()
    for r in rows:
        print("   -", r["author"], age(r["created_at"]), "m |", r["b"].replace("\n", " ")[:240])
    # blok reason dari event
    ev = con.execute("SELECT payload, created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    if ev: print("   BLOCK-EVENT", age(ev["created_at"]), "m |", str(ev["payload"])[:200])
    # apakah sudah pernah promote lagi setelah marker?
    print()
