# Rekonsiliasi-2 1018b: daftar penulis ACK vs penulis LAPOR per kartu kandidat (gerbang author rute-4b)
import sqlite3

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
for tid in ["t_8358d01c", "t_d663f001", "t_63b993df", "t_491531fd"]:
    r = con.cursor().execute("SELECT id FROM tasks WHERE id LIKE ?", (tid + "%",)).fetchone()
    print("==", r["id"])
    rows = con.cursor().execute(
        "SELECT author, substr(body,1,70) b, created_at FROM task_comments "
        "WHERE task_id=? ORDER BY created_at ASC", (r["id"],)).fetchall()
    for c in rows:
        print(f"   [{c['author']}] {c['b'].replace(chr(10),' ')[:66]}")
con.close()
