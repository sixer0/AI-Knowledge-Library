# Verify run-timed_out class: task_runs records, heartbeat liveness, full scan classification, id diff vs parent set.
import importlib.util, time, sqlite3

spec = importlib.util.spec_from_file_location("mws", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mws = importlib.util.module_from_spec(spec); spec.loader.exec_module(mws)
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
authors = mws.DEFAULT_AUTHORS
if isinstance(authors, str): authors = authors.split(",")
now = int(time.time())
rows = mws.scan(DB, now, authors)
from collections import Counter
print("RESCAN_TOTAL", len(rows), Counter(r[1] for r in rows))

con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
cols = [r[1] for r in cur.execute("PRAGMA table_info(task_runs)")]
print("COLS task_runs:", ",".join(cols))

ids_run = sorted(r[0] for r in rows if r[1] == "run-timed_out")
ids_stall = sorted(r[0] for r in rows if r[1] == "stalled")
parents = sorted({p["parent_id"] for c in ids_stall for p in cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (c,))})
extra = [i for i in ids_run if i not in parents]
missing = [p for p in parents if p not in ids_run]
print("RUN_ROWS", len(ids_run), "PARENTS", len(parents), "EXTRA_NOT_PARENT", extra, "PARENT_NOT_IN_RUN", missing)

print("SAMPLE task_runs for 3 parents:")
for tid in ids_run[:3]:
    for rr in cur.execute("SELECT * FROM task_runs WHERE task_id=? ORDER BY rowid DESC LIMIT 3", (tid,)):
        d = dict(rr)
        print(f"  {tid}: " + " ".join(f"{k}={d[k]}" for k in cols if d.get(k) is not None))

print("HEARTBEAT LIVENESS (events kind=heartbeat last 10 min, per parent):")
live = 0
for tid in ids_run:
    n = cur.execute("SELECT COUNT(*) FROM task_events WHERE task_id=? AND kind='heartbeat' AND created_at>=?", (tid, now-600)).fetchone()[0]
    st = cur.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()["status"]
    if n: live += 1
    if n == 0:
        print(f"  NO-HB-10MIN {tid} status={st}")
print(f"  live_parents_with_hb_last10min = {live}/{len(ids_run)}")

print("STATUS NOW for run rows:", Counter(cur.execute("SELECT status FROM tasks WHERE id=?", (i,)).fetchone()["status"] for i in ids_run))
# LAPOR presence on run rows
nlap_any = sum(cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (i,)).fetchone()[0] for i in ids_run)
print("TOTAL_LAPOR_ON_RUN_ROWS", nlap_any)
# controller comments on run rows
nctrl = sum(cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND author IN ('default','gsp-master01','sysmanager-cleaner','mission-wake')", (i,)).fetchone()[0] for i in ids_run)
print("CTRL_COMMENTS_ON_RUN_ROWS", nctrl)
