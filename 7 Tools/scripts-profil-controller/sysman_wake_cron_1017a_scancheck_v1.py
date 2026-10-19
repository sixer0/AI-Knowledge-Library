# Ronde cron 17-10: verifikasi deterministik scan() kanonis + sensus kartu terbuka
import importlib.util, time, sqlite3, os, sys

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")

spec = importlib.util.spec_from_file_location("gsp_mission_wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")

findings = mod.scan(DB, int(time.time()), authors)
print("SCAN_TEMUAN =", len(findings))
for f in findings:
    print("ROW:", f)

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
print("--- SENSUS STATUS ---")
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(r["status"], r["n"])
open_rows = [dict(r) for r in cur.execute(
    "SELECT id, title, status, tenant, created_by FROM tasks WHERE status NOT IN ('done','archived') ORDER BY status, id")]
print("KARTU_TERBUKA =", len(open_rows))
for r in open_rows:
    print("OPEN:", r["id"], "|", r["status"], "|", (r["tenant"] or "-"), "|", (r["title"] or "")[:70])
mx = cur.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
now = int(time.time())
print("EVENT_TERBARU_UMUR_MENIT =", round((now - (mx or 0)) / 60.0, 1))
for t in ("tasks", "task_events", "task_comments"):
    print(t, "=", cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
# blind spot: kartu running dengan LAPOR-SELESAI tanpa ACK
print("--- RUNNING+LAPOR tanpa ACK ---")
ids = [r[0] for r in cur.execute("SELECT id FROM tasks WHERE status='running'")]
for i in ids:
    lap = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (i,)).fetchone()[0]
    ack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (i,)).fetchone()[0]
    if lap and not ack:
        print("BLIND:", i)
con.close()
