import sqlite3
con = sqlite3.connect("C:/Users/TRIAL/AppData/Local/hermes/kanban.db")
for tbl in ("tasks", "task_events", "task_comments", "task_links"):
    print(tbl, [r[1] for r in con.execute(f"PRAGMA table_info({tbl})")])
