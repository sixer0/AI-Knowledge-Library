# Ronde senyap 17-10b: sanity papan hidup + census terbuka + blind-spot rute-4b + scan() kanonis
import importlib.util, json, os, sqlite3, sys, time

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()

now = int(time.time())
print("NOW_EPOCH", now)

# 1. Sanity: papan hidup (MAX event age, BUKAN MIN)
r = cur.execute("SELECT COUNT(*) n, MAX(created_at) mx FROM task_events").fetchone()
print("EVENTS count=%s max_age_min=%.1f" % (r["n"], (now - (r["mx"] or 0)) / 60.0))
for t in ("tasks", "task_comments"):
    r = cur.execute(f"SELECT COUNT(*) n FROM {t}").fetchone()
    print(f"{t} count={r['n']}")
r = cur.execute("SELECT MAX(created_at) mx FROM task_comments").fetchone()
print("comment_max_age_min=%.1f" % ((now - (r["mx"] or 0)) / 60.0))

# 2. Census status
print("--- STATUS CENSUS ---")
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print("%s=%s" % (r["status"], r["n"]))

# 3. Kartu terbuka non-done/non-archived dengan umur event terakhir
print("--- OPEN CARDS (non done/archived) ---")
ids = [x["id"] for x in cur.execute(
    "SELECT id FROM tasks WHERE status NOT IN ('done','archived')")]
open_rows = []
for cid in ids:
    e = cur.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (cid,)).fetchone()["mx"]
    c = cur.execute("SELECT MAX(created_at) mx FROM task_comments WHERE task_id=?", (cid,)).fetchone()["mx"]
    last = max([v for v in (e, c) if v] or [0])
    row = cur.execute("SELECT id,title,status,tenant,assignee,created_by,last_heartbeat_at,current_run_id FROM tasks WHERE id=?", (cid,)).fetchone()
    open_rows.append((row, last))
open_rows.sort(key=lambda x: x[1])
for row, last in open_rows:
    hb = row["last_heartbeat_at"]
    hb_age = ((now - hb) / 60.0) if hb else None
    print("%s | %s | %s | tenant=%s | assignee=%s | ev_age=%.0fm | hb_age=%s" % (
        row["id"], row["status"], (row["title"] or "")[:48], row["tenant"],
        row["assignee"], (now - last) / 60.0,
        ("%.0fm" % hb_age) if hb_age is not None else "-"))

# 4. Blind-spot: kartu running ber-LAPOR tanpa ACK
print("--- BLINDSPOT running LAPOR vs ACK ---")
run_ids = [x["id"] for x in cur.execute("SELECT id FROM tasks WHERE status='running'")]
for cid in run_ids:
    lap = cur.execute(
        "SELECT COUNT(*) n, MAX(created_at) mx FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESEI%' OR body LIKE '%LAPOR-SELESAI%')",
        (cid,)).fetchone()
    ack = cur.execute(
        "SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
        (cid,)).fetchone()
    hb = cur.execute("SELECT last_heartbeat_at, title FROM tasks WHERE id=?", (cid,)).fetchone()
    print("%s | lap=%s ack=%s | hb_age=%s | %s" % (
        cid, lap["n"], ack["n"],
        ("%.0fm" % ((now - hb["last_heartbeat_at"]) / 60.0)) if hb["last_heartbeat_at"] else "-",
        (hb["title"] or "")[:44]))

# 5. Scan() kanonis sebagai vonis tunggal
print("--- SCAN() KANONIS ---")
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
fn = getattr(mod, "scan", None)
if fn is None:
    print("NO scan() ATTR")
else:
    da = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
    authors = da.split(",") if isinstance(da, str) else list(da)
    res = fn(DB, int(time.time()), authors)
    print("scan findings =", len(res))
    for item in res:
        print("  ", tuple(item) if not isinstance(item, tuple) else item)
con.close()
