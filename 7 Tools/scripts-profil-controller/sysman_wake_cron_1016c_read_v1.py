# Ambil komentar penuh LAPOR-SELESAI + PARKED kartu S13 untuk bahan vonis controller
import sqlite3
con = sqlite3.connect("file:C:/Users/TRIAL/AppData/Local/hermes/kanban.db?mode=ro", uri=True)
con.row_factory = sqlite3.Row
for c in con.execute("SELECT author, body FROM task_comments WHERE task_id='t_5b68a0be' AND body LIKE '%LAPOR-SELESAI%' ORDER BY created_at DESC LIMIT 1"):
    print(c["body"])
