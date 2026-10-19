# Tenant census BLENDER-MCP-SKILL-1016 + ACK/marker check per card (read-only).
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def age(ts):
    return round((now - ts) / 60.0, 1) if ts else None

rows = con.execute("SELECT id,status,title,completed_at FROM tasks WHERE tenant=? ORDER BY created_at", ("BLENDER-MCP-SKILL-1016",)).fetchall()
print(f"TENANT CARDS: {len(rows)}")
for r in rows:
    ids = [r["id"]]
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    lap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["c"]
    mk  = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["c"]
    hb  = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    print(f"{r['id']:12} {r['status']:9} lap={lap} ack={ack} wake_marker={mk} last_ev={age(hb)}m  {r['title'][:60]!r}")
