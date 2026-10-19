# Ronde senyap 17-10: sanity papan hidup + replika scan() kanonis + sapuan blind-spot rute-4b
import sqlite3, time, os, importlib.util, io, contextlib, json

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN_SCRIPT = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")
now = int(time.time())

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def age_min(ts):
    return round((now - ts) / 60.0, 1) if ts else None

print("== SENSUS STATUS ==")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  {r['status']}: {r['n']}")

print("== KEHIDUPAN PAPAN ==")
me = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
mc = con.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()["m"]
nt = con.execute("SELECT COUNT(*) n FROM tasks").fetchone()["n"]
ne = con.execute("SELECT COUNT(*) n FROM task_events").fetchone()["n"]
nc = con.execute("SELECT COUNT(*) n FROM task_comments").fetchone()["n"]
print(f"  tasks={nt} events={ne} comments={nc}")
print(f"  event terakhir umur={age_min(me)} mnt; komentar terakhir umur={age_min(mc)} mnt")

print("== SCAN() KANONIS ==")
spec = importlib.util.spec_from_file_location("mws", SCAN_SCRIPT)
mod = importlib.util.module_from_spec(spec)
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
    authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
    if isinstance(authors, str):
        authors = authors.split(",")
    findings = mod.scan(DB, now, authors)
    print(f"  temuan scan(): {len(findings)} -> {findings}")
except Exception as e:
    print(f"  GALAT scan(): {type(e).__name__}: {e}")
captured = buf.getvalue().strip()
if captured:
    print(f"  stdout saat scan: {captured[:500]}")

print("== BLIND SPOT: running ber-LAPOR tanpa ACK ==")
hits = 0
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='running'")]
for tid in ids:
    lap = con.execute(
        "SELECT COUNT(*) n, MAX(created_at) m FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%' OR body LIKE '%LAPOR-SELESAI%')",
        (tid,)).fetchone()
    if lap["n"]:
        ack = con.execute(
            "SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
            (tid,)).fetchone()["n"]
        hb = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
        title = con.execute("SELECT title FROM tasks WHERE id=?", (tid,)).fetchone()["title"]
        print(f"  {tid} '{title[:40]}' lap={lap['n']} ack={ack} lap_umur={age_min(lap['m'])}m evt_umur={age_min(hb)}m")
        hits += 1
if hits == 0:
    print("  (nol kartu running ber-LAPOR tanpa ACK; running total =", len(ids), ")")

print("== KARTU TERBUKA (todo/running/blocked) + umur event terakhir ==")
rows = con.execute("""SELECT t.id, t.status, t.title, t.tenant,
   (SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id) le
   FROM tasks t WHERE t.status IN ('todo','running','blocked','in_progress')
   ORDER BY t.status, le""").fetchall()
for r in rows:
    print(f"  [{r['status']}] {r['id']} tenant={r['tenant']} evt_umur={age_min(r['le'])}m :: {(r['title'] or '')[:60]}")
print("  total terbuka:", len(rows))
con.close()
