# ACK census ulang untuk 11 kartu done VIBE-BIBLE-1013 (read-only, eksplisit id).
import sqlite3, os, time
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
ids = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'")]
print("jumlah done:", len(ids))
for tid in ids:
    r = cur.execute("SELECT title, completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    ack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    lap = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND UPPER(body) LIKE '%LAPOR%'", (tid,)).fetchone()["c"]
    wake = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["c"]
    ca = r["completed_at"]
    age = round((now-ca)/60) if ca else "NULL"
    print(f"{tid} lapor={lap} ack={ack} wake_marker={wake} selesai={age}m :: {(r['title'] or '')[:55]}")
