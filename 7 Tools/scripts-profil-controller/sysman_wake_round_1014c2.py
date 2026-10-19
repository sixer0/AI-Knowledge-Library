# sysman cron 14-10 ronde-c bagian 2: census ACK done VBCB + kartu running + triase controller
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

TEN = "VIBE-BIBLE-1013"

print("=== DONE VBCB: ACK+marker census ===")
rows = con.execute("SELECT id,title,completed_at FROM tasks WHERE tenant=? AND status='done' ORDER BY completed_at", (TEN,)).fetchall()
for r in rows:
    acks = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    marks = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["c"]
    print(f"{r['id']} ack={acks} marker={marks} done_age={int((now-r['completed_at'])/60)}m {r['title'][:55]}")

print("\n=== GAVE_UP / timed_out census VBCB ===")
gu = con.execute("SELECT COUNT(DISTINCT task_id) n FROM task_events WHERE kind='gave_up' AND task_id IN (SELECT id FROM tasks WHERE tenant=?)", (TEN,)).fetchone()["n"]
to = con.execute("SELECT COUNT(DISTINCT task_id) n FROM task_events WHERE kind='timed_out' AND task_id IN (SELECT id FROM tasks WHERE tenant=?)", (TEN,)).fetchone()["n"]
print("gave_up_cards", gu, "timed_out_cards", to)
run = con.execute("SELECT COUNT(*) n FROM tasks WHERE tenant=? AND status='running'", (TEN,)).fetchone()["n"]
print("vbcb_running", run)

print("\n=== TRIASE controller pada kartu blocked VBCB (komentar author default/sysman setelah timeout) ===")
# timeout epoch terukur dari ronde sebelumnya: event timed_out max
mx = con.execute("SELECT MAX(created_at) m FROM task_events WHERE kind='timed_out' AND task_id IN (SELECT id FROM tasks WHERE tenant=?)", (TEN,)).fetchone()["m"]
tri = con.execute("SELECT task_id, author, substr(replace(body,char(10),' '),1,90) b, created_at FROM task_comments WHERE created_at>=? AND author IN ('default','gsp-system-manager','user','sysmanager-cleaner','mission-wake') AND task_id IN (SELECT id FROM tasks WHERE tenant=?) ORDER BY created_at DESC LIMIT 20", (mx, TEN)).fetchall()
print("controller_comments_after_timeout", len(tri))
for t in tri:
    print(f"  {t['task_id']} {t['author']}: {t['b']}")

print("\n=== KARTU RUNNING global (blind spot) ===")
runs = con.execute("SELECT id,title,tenant,last_heartbeat_at,started_at FROM tasks WHERE status='running'").fetchall()
for r in runs:
    hb = r["last_heartbeat_at"]
    lap = con.execute("SELECT MAX(created_at) m, COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (r["id"],)).fetchone()
    acks = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    print(f"{r['id']} tenant={r['tenant']} hb_age={int((now-hb)/60) if hb else None}m run_age={int((now-r['started_at'])/60) if r['started_at'] else None}m lapor_n={lap['c']} lapor_age={int((now-lap['m'])/60) if lap['m'] else None}m ack={acks} title={r['title'][:60]}")

print("\n=== BLOCKED non-VBCB (10 lainnya) - umur event + alasan singkat ===")
oth = con.execute("SELECT id,title,status FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant!=?) ", (TEN,)).fetchall()
for r in oth:
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    tn = con.execute("SELECT tenant FROM tasks WHERE id=?", (r["id"],)).fetchone()["tenant"]
    print(f"{r['id']} tenant={tn} last_ev={int((now-ev)/60) if ev else None}m {r['title'][:60]}")
