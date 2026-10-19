# Full text of recent comments on the two fase-stalled cards + ACK check on t_87b1a40e.
import sqlite3
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
for tid in ("t_6359bba5", "t_bb725705", "t_87b1a40e"):
    print(f"\n========== {tid} ==========")
    for c in con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)):
        print(f"\n--- [{c['created_at']}] {c['author']} ---")
        print(c["body"][:1800])
    acks = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
    marks = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()[0]
    print(f"\nACK_COUNT={acks} MARKER_COUNT={marks}")
