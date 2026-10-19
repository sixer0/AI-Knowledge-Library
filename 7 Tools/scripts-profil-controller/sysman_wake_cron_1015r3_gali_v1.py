# -*- coding: utf-8 -*-
# Ronde 1015r3: isi komentar terakhir 1 orang tua sampel + event blocked-nya (payload penuh),
# + cek apakah ronde r2 sudah menulis marker/comment apa pun di anak wake.
import sqlite3, time, json
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

pid = "t_64328060"  # orang tua dari t_002af121
print("== ORANG TUA SAMPLE", pid, "==")
t = con.execute("SELECT id,title,status,created_at,completed_at FROM tasks WHERE id=?", (pid,)).fetchone()
print(dict(t), "| created", age(t["created_at"]), "m")
for e in con.execute("SELECT kind,payload,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (pid,)).fetchall():
    print(f"  ev {age(e['created_at'])}m {e['kind']} :: {(e['payload'] or '')[:200]}")
for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (pid,)).fetchall():
    print(f"  cm {age(c['created_at'])}m [{c['author']}] {c['body'][:280]}")

print("\n== ANAK SAMPLE t_002af121 komentar ==")
for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id='t_002af121' ORDER BY created_at DESC LIMIT 3").fetchall():
    print(f"  cm {age(c['created_at'])}m [{c['author']}] {c['body'][:200]}")

print("\n== DONE M4 TANPA ACK: sample 3 kartu, komentar terakhir ==")
for r in con.execute("SELECT id,title,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done' ORDER BY completed_at DESC LIMIT 3").fetchall():
    print(f"  {r['id']} done {age(r['completed_at'])}m {(r['title'] or '')[:60]}")
    for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (r["id"],)).fetchall():
        print(f"    cm {age(c['created_at'])}m [{c['author']}] {c['body'][:160]}")
