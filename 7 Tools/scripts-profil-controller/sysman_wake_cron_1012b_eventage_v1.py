# Read-only: umur event papan + daftar kartu blocked + ACK census per kartu blocked
import sqlite3, time, os

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
c = con.cursor()

last_ev = c.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
print("last_task_event_age_min =", round((now - last_ev) / 60, 1) if last_ev else "NONE")

print("-- blocked cards --")
rows = c.execute("SELECT id,title,status,tenant,created_by,created_at,block_kind FROM tasks WHERE status='blocked' ORDER BY created_at DESC").fetchall()
for r in rows:
    age_h = (now - r["created_at"]) / 3600 if r["created_at"] else -1
    ncom = c.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=?", (r["id"],)).fetchone()[0]
    last_com = c.execute("SELECT MAX(created_at) FROM task_comments WHERE task_id=?", (r["id"],)).fetchone()[0]
    ack = c.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE 'RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    lap = c.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%')", (r["id"],)).fetchone()[0]
    ev_age = None
    e = c.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (r["id"],)).fetchone()[0]
    if e:
        ev_age = round((now - e) / 60, 1)
    print(f"{r['id']} | tenant={r['tenant']} | age_h={age_h:.1f} | comments={ncom} ack={ack} lapor={lap} | last_comment_age_min={'-' if not last_com else round((now-last_com)/60,1)} | last_event_age_min={ev_age}")
    print(f"   title: {r['title'][:110]}")
con.close()
