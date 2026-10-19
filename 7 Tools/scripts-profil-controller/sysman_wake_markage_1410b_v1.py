# Umur penanda RANTAI-WAKE pada 11 kartu done + t_d3cc135a (read-only).
import sqlite3, os, time
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
for r in cur.execute("SELECT task_id, author, created_at, body FROM task_comments WHERE body LIKE '%RANTAI-WAKE%' AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013') ORDER BY created_at"):
    print(f"{r['task_id']} {r['author']}@{round((now-r['created_at'])/60)}m :: {(r['body'] or '')[:60]}".replace(chr(10),' '))
