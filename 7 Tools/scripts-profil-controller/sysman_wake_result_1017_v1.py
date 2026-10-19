import sqlite3
con = sqlite3.connect(r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db")
con.row_factory = sqlite3.Row
r = con.execute("SELECT result, body FROM tasks WHERE id='t_4a179fc3'").fetchone()
print("== RESULT FULL ==")
print(r["result"])
print("\n== BODY FULL ==")
print(r["body"])
