# Sapuan buta-tutup ronde 11-10 (i): event terminal <=6j tanpa syarat tenant + census todo.
import sqlite3, os, time
HERMES = os.path.expandvars(r"C:/Users/TRIAL/AppData/Local/hermes")
DB = os.path.join(HERMES, "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB)
cur = con.cursor()

print("== EVENT TERMINAL <=6 JAM (tanpa syarat tenant) ==")
rows = cur.execute("""
SELECT e.task_id, e.kind, e.created_at, t.status, t.tenant, t.assignee, t.title
FROM task_events e JOIN tasks t ON t.id=e.task_id
WHERE e.created_at >= ? - 6*3600 AND e.kind IN ('completed','blocked','parked')
ORDER BY e.created_at DESC LIMIT 40
""", (now,)).fetchall()
for tid, kind, ts, status, tenant, assignee, title in rows:
    age = round((now-ts)/60.0, 1)
    acks = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
    marks = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()[0]
    print(f"{tid} {kind} age={age}m status={status} tenant={tenant!r} ack={acks} marker={marks} | {title[:55]}")

print("\n== CENSUS TODO (semua) ==")
for tid, title, tenant, created_by in cur.execute(
    "SELECT id,title,tenant,created_by FROM tasks WHERE status='todo' ORDER BY created_at"):
    ev = cur.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,)).fetchone()[0]
    parents = cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()
    pstat = []
    for (p,) in parents:
        s = cur.execute("SELECT status FROM tasks WHERE id=?", (p,)).fetchone()
        pstat.append(f"{p}:{s[0] if s else '?'}")
    print(f"{tid} lastev_age={(now-ev)/60.0:.0f}m parents={pstat} | {title[:60]}")

print("\n== UMUR EVENT TERAKHIR BOARD ==")
lastev = cur.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
lastc = cur.execute("SELECT MAX(created_at) FROM task_comments").fetchone()[0]
print(f"last_event_age_min={(now-lastev)/60.0:.1f} last_comment_age_min={(now-lastc)/60.0:.1f}")
con.close()
