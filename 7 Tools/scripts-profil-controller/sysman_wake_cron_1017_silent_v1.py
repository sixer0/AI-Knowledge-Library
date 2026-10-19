# sysman cron 17-10: ronde senyap - replika scan() + sensus blocked
import importlib.util, sqlite3, time, os, sys

SCRIPTS = r"C:/Users/TRIAL/AppData/Local/hermes/scripts"
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"

spec = importlib.util.spec_from_file_location("wake_scan", os.path.join(SCRIPTS, "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
findings = mod.scan(DB, int(time.time()), authors)
print("SCAN findings =", len(findings))
for f in findings:
    print("  ROW:", tuple(f))

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# ambang hidup di skrip
for k in ("STALLED_MIN", "RUN_WINDOW_H", "FASE_STALL_MIN", "DONE_UNACKED_MIN"):
    print("AMBANG", k, "=", getattr(mod, k, "?"))

now = int(time.time())
print("\n-- census terbuka (bukan done/archived) --")
cur = con.cursor()
rows = cur.execute("SELECT id, status, tenant, created_by, title FROM tasks WHERE status NOT IN ('done','archived') ORDER BY status, id").fetchall()
print("total terbuka =", len(rows))
ids = [r["id"] for r in rows]
for r in rows:
    ev = con.cursor().execute("SELECT MAX(created_at) AS m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    cm = con.cursor().execute("SELECT MAX(created_at) AS m FROM task_comments WHERE task_id=?", (r["id"],)).fetchone()["m"]
    last = max([x for x in (ev, cm) if x] or [0])
    age = (now - last) / 60.0 if last else -1
    # komentar terakhir
    lc = con.cursor().execute("SELECT author, substr(body,1,90) AS b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    # marker cleaner?
    clean = con.cursor().execute("SELECT COUNT(*) AS c FROM task_comments WHERE task_id=? AND body LIKE '%[SYSMAN-CLEANER%'", (r["id"],)).fetchone()["c"]
    dig = con.cursor().execute("SELECT COUNT(*) AS c FROM task_comments WHERE task_id=? AND body LIKE '%Digantikan t_%'", (r["id"],)).fetchone()["c"]
    print(f"{r['id']} | {r['status']} | tenant={r['tenant']} | umur_event={age:.0f}m | cleaner={clean} diganti={dig}")
    print(f"    judul: {(r['title'] or '')[:80]}")
    if lc:
        print(f"    komentar_terakhir[{lc['author']}]: {lc['b']!r}")

# blind spot: kartu running dengan LAPOR tanpa ACK
print("\n-- blind spot running --")
run = cur.execute("SELECT id, title, last_heartbeat_at FROM tasks WHERE status='running'").fetchall()
print("running =", len(run))
for r in run:
    hb = (now - (r["last_heartbeat_at"] or 0)) / 60.0 if r["last_heartbeat_at"] else -1
    lap = con.cursor().execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["c"]
    ack = con.cursor().execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    print(f"  {r['id']} hb={hb:.0f}m lap={lap} ack={ack} :: {(r['title'] or '')[:60]}")

# papan kesegaran: event & komentar terbaru global
print("\n-- kesegaran global --")
me = cur.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
mc = cur.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()["m"]
mt = cur.execute("SELECT MAX(created_at) m FROM tasks").fetchone()["m"]
for name, v in (("events", me), ("comments", mc), ("tasks", mt)):
    print(f"  {name} terbaru umur = {(now-v)/60.0:.1f} mnt" if v else f"  {name} KOSONG")
con.close()
