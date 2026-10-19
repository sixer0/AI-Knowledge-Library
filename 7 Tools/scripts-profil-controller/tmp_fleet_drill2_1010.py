# -*- coding: utf-8 -*-
import sqlite3, os, pathlib, time
HOME = pathlib.Path(os.environ.get('LOCALAPPDATA',''))/'hermes'
con = sqlite3.connect(HOME/'kanban.db'); cur = con.cursor()
cols = [c[1] for c in cur.execute("PRAGMA table_info(tasks)")]
print("tasks cols:", cols)
timecol = 'updated_at' if 'updated_at' in cols else ('updatedAt' if 'updatedAt' in cols else 'created_at')
sel = "id,substr(title,1,70),assignee"
print("--- blocked ---")
for r in cur.execute(f"SELECT {sel},{timecol} FROM tasks WHERE status='blocked' ORDER BY {timecol}"):
    print("BLK", r)
print("--- running tertua ---")
for r in cur.execute(f"SELECT {sel},{timecol} FROM tasks WHERE status='running' ORDER BY {timecol} LIMIT 8"):
    print("RUN", r)
con.close()
