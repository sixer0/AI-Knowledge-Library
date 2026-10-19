# Ronde cron 17-10: rekonsiliasi stdout kosong vs kandidat alat longgar
import sqlite3, time, importlib.util, os

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())

# 1) Vonis kanonis via scan() importlib
spec = importlib.util.spec_from_file_location("wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
authors = getattr(m, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
try:
    findings = m.scan(DB, now, authors)
except TypeError:
    findings = m.scan(DB, now)
print("CANONICAL scan() findings =", len(findings))
for f in findings:
    print("  ", f)

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# 2) Census kartu terbuka non-blocked (todo/running/in_progress dsb.)
print("\n-- open non-blocked status census --")
for r in con.execute("SELECT status, COUNT(*) c FROM tasks WHERE status NOT IN ('done','archived','blocked') GROUP BY status"):
    print(f"  {r['status']} = {r['c']}")

print("\n-- todo cards detail --")
for r in con.execute("SELECT id, title, tenant, created_at FROM tasks WHERE status='todo' ORDER BY created_at DESC LIMIT 10"):
    age = (now - r["created_at"]) / 60.0
    print(f"  {r['id']} age={age:.0f}m tenant={r['tenant']} | {r['title'][:60]}")

# 3) Marker check utk kandidat done terbaru (apakah sudah ber-marker ronde lalu)
print("\n-- recent done (<=12h) marker/ACK census --")
# id-list dulu, baru query per id (hindari nested cursor)
ids = [row["id"] for row in con.execute("SELECT id, title, completed_at, tenant FROM tasks WHERE status='done' AND completed_at >= ? ORDER BY completed_at DESC", (now - 12*3600,))]
titles = {row["id"]: (row["title"], row["tenant"], row["completed_at"]) for row in con.execute("SELECT id, title, completed_at, tenant FROM tasks WHERE status='done' AND completed_at >= ?", (now - 12*3600,))}
for tid in ids:
    mk = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()[0]
    ack = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
    lap = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESAI%')", (tid,)).fetchone()[0]
    ttl, ten, comp = titles[tid]
    age = (now - comp) / 60.0
    print(f"  {tid} age={age:.0f}m tenant={ten} marker={mk} ack={ack} lap={lap} | {ttl[:55]}")

# 4) Umur event terakhir (sanity hidup, MAX bukan MIN)
mx = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
print(f"\nlast_event_age_min = {(now-mx)/60.0:.1f}")
con.close()
