# -*- coding: utf-8 -*-
# Cek marker existing utk 3 simpul LAPOR (t_99bb85a4, t_b10a1e32, t_ad5d8e6f) sebelum vonis.
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None
for tid in ["t_99bb85a4","t_b10a1e32","t_ad5d8e6f"]:
    t = con.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()
    mk = con.execute("SELECT created_at, substr(body,1,60) b FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%' ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    print(tid, "status=", t["status"], "ack=", ack, "| marker=", (age(mk["created_at"]), "m lalu:", mk["b"]) if mk else "TIDAK ADA")
