# -*- coding: utf-8 -*-
# Ukur rentang umur selesai 33 kartu M4 done VBCB (lengkap, bukan 15 teratas).
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
rows = con.execute("""SELECT completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013'
 AND status='done' AND title LIKE '%(resume)%'""").fetchall()
ages = sorted(round((NOW - r[0]) / 60.0) for r in rows if r[0])
print("n=", len(ages), "| min=", ages[0], "mnt | max=", ages[-1], "mnt")
