import sqlite3
con = sqlite3.connect("file:C:/Users/TRIAL/AppData/Local/hermes/kanban.db?mode=ro", uri=True)
for r in con.execute("PRAGMA table_info(tasks)"):
    print(r[1], r[2])
