# Sanity rekonsiliasi: umur event papan + blind spot kartu running (read-only).
import sqlite3, os, time
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()

print("== umur event papan (pencocokan pola query pemindai) ==")
q1 = cur.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
print("  MAX(created_at) events:", q1, "-> umur", round((now-q1)/60), "mnt")
q2 = cur.execute("SELECT created_at FROM task_events ORDER BY created_at DESC LIMIT 1").fetchone()
print("  ORDER BY DESC LIMIT 1 :", q2["created_at"], "-> umur", round((now-q2["created_at"])/60), "mnt")
q3 = cur.execute("SELECT MAX(created_at) m FROM tasks").fetchone()["m"]
print("  MAX(created_at) tasks :", q3, "-> umur", round((now-q3)/60), "mnt")
q4 = cur.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()["m"]
print("  MAX(created_at) coms  :", q4, "-> umur", round((now-q4)/60), "mnt")
print("  now_epoch:", now)

print("== BLIND SPOT: semua kartu running ==")
for r in cur.execute("SELECT id,title,status,tenant,assignee,created_at FROM tasks WHERE status='running'"):
    tid = r["id"]
    evs = cur.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)).fetchall()
    coms = cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (tid,)).fetchall()
    lapor = sum(1 for c in coms if "LAPOR" in (c["body"] or "").upper())
    ack = sum(1 for c in coms if "RANTAI-ACK" in (c["body"] or ""))
    print(f"  {tid} [{r['tenant']}] {r['title'][:60]}")
    print(f"    umur_kartu={round((now-r['created_at'])/60)}m lapor={lapor} ack={ack}")
    for e in evs: print(f"    ev {e['kind']}@{round((now-e['created_at'])/60)}m")
    for c in coms[:3]: print(f"    com {c['author']}@{round((now-c['created_at'])/60)}m: {(c['body'] or '')[:100]}".replace(chr(10),' '))

print("== cek DB alternatif boards/gsp ==")
alt = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "boards", "gsp", "kanban.db")
print("  ada di disk:", os.path.exists(alt))
