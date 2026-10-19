# Tenant census DECK-HTMLPDF-1015: status per kartu, ACK, marker, event terakhir.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

rows = con.execute(
    "SELECT id,status,title,created_at,completed_at FROM tasks WHERE tenant=? ORDER BY created_at",
    ("DECK-HTMLPDF-1015",)).fetchall()
print(f"tenant DECK-HTMLPDF-1015: {len(rows)} kartu")
ids = [r["id"] for r in rows]  # id-list dulu, hindari nested-cursor pitfall
for r in rows:
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    mk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()["c"]
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    lap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%' OR body LIKE '%STATUS: partial-handoff%' OR body LIKE '%PARKED%')", (r["id"],)).fetchone()["c"]
    age = "-" if ev is None else f"{round((now-ev)/60,1)}m"
    print(f"{r['id']} {r['status']:9s} ack={ack} wake_mk={mk} lap={lap} last_ev={age:>7s}  {r['title'][:60]!r}")

# links within tenant
print("--- links ---")
for l in con.execute("SELECT parent_id, child_id FROM task_links WHERE parent_id IN (%s) OR child_id IN (%s)" % (",".join("?"*len(ids)), ",".join("?"*len(ids))), ids+ids).fetchall():
    print(f"  {l['parent_id']} -> {l['child_id']}")
con.close()
