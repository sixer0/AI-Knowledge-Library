# -*- coding: utf-8 -*-
# Cek penanda RANTAI-WAKE mendarat atau tidak (read-only).
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
for tid in ["t_1a9ca5ce", "t_ed9976be", "t_edb280b5"]:
    rows = con.execute("SELECT author, created_at, substr(body,1,80) b FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%' ORDER BY created_at DESC", (tid,)).fetchall()
    print(tid, "marker_n=", len(rows))
    for r in rows:
        print("   ", r["author"], round((NOW-r["created_at"])/60.0), "m |", r["b"])
