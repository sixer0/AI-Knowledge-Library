# Ronde cron 15-10 (malam): scan kanonis + sanity papan hidup + blind spot running
import sqlite3, time, importlib.util, os

HERMES = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HERMES, "kanban.db")
SCAN = os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py")

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")

fn = getattr(mod, "scan", None)
findings = None
if fn:
    try:
        findings = fn(DB, now, authors)
    except TypeError:
        try:
            findings = fn(DB, now)
        except Exception as e:
            print("SCAN_ERR:", e)

print("=== SCAN KANONIS (nilai kembali) ===")
if findings is None:
    print("(scan() tidak tersedia/berubah - fallback CLI di langkah lain)")
else:
    print("N_TEMUAN =", len(findings))
    for row in findings:
        print("WAKE:", row)

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

print("=== SANITY PAPAN HIDUP ===")
r = cur.execute("SELECT COUNT(*) n FROM tasks").fetchone()
print("tasks =", r["n"])
r = cur.execute("SELECT COUNT(*) n FROM task_events").fetchone()
print("events =", r["n"])
try:
    r = cur.execute("SELECT COUNT(*) n FROM task_comments").fetchone()
    print("comments =", r["n"])
except Exception as e:
    print("comments ERR:", e)
r = cur.execute("SELECT MAX(created_at) mx FROM task_events").fetchone()
age = (now - int(r["mx"])) / 60.0 if r["mx"] else -1
print("umur_event_terakhir_menit = %.1f" % age)

print("=== SENSUS STATUS ===")
for row in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"{row['status']} = {row['n']}")

print("=== BLIND SPOT: running >60mnt tanpa event baru ===")
ids = [row["id"] for row in cur.execute(
    "SELECT id FROM tasks WHERE status='running' ORDER BY created_at")]
for tid in ids:
    e = cur.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (tid,)).fetchone()["mx"]
    c = cur.execute("SELECT MAX(created_at) mc FROM task_comments WHERE task_id=?", (tid,)).fetchone()["mc"]
    last = max([x for x in (e, c) if x] or [0])
    age_min = (now - int(last)) / 60.0
    lap = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELE%'", (tid,)).fetchone()["n"]
    ack = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    title = cur.execute("SELECT title FROM tasks WHERE id=?", (tid,)).fetchone()["title"]
    flag = ""
    if lap > 0 and ack == 0:
        flag = " <-- LAPOR tanpa ACK"
    if age_min > 120:
        flag += " <-- UMUR >2J"
    if flag:
        print(f"{tid} | {title[:60]} | last={age_min:.0f}m lap={lap} ack={ack}{flag}")

con.close()
