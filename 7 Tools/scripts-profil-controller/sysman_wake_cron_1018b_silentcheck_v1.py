# Ronde senyap 18-10b: scan() kanonis + sensus blocked + blind-spot running/todo
import sqlite3, sys, time, importlib.util
from pathlib import Path

HOME = Path("C:/Users/TRIAL/AppData/Local/hermes")
DB = HOME / "kanban.db"
SCAN = HOME / "scripts" / "gsp_mission_wake_scan.py"

# 1) scan() kanonis via importlib — TANGKAP nilai kembaliannya (list), bukan stdout
spec = importlib.util.spec_from_file_location("gsp_mission_wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
findings = mod.scan(str(DB), int(time.time()), authors)
print("SCAN_FINDINGS =", len(findings))
for f in findings:
    print("  ROW:", tuple(f))

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

# 2) sensus status terbuka
print("-- open status census --")
for r in con.execute("SELECT status, COUNT(*) c FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status ORDER BY c DESC"):
    print(f"  {r['status']} = {r['c']}")

# 3) blocked: apakah koreksi terakhir sudah tertempel? (tasks tidak punya updated_at)
print("-- blocked marker census --")
unfixed = []
for r in con.execute("SELECT id, title, created_at FROM tasks WHERE status='blocked' ORDER BY created_at DESC"):
    cid = r["id"]
    # komentar terakhir (ASC -> ambil yang paling akhir via list)
    coms = con.execute(
        "SELECT body, author FROM task_comments WHERE task_id=? ORDER BY created_at ASC", (cid,)
    ).fetchall()
    last = coms[-1]["body"] if coms else ""
    has_cleaner = "[SYSMAN-CLEANER" in last
    has_replaced = any((c["body"].startswith("Digantikan ") and c["author"] not in ("sysmanager-cleaner",)) for c in coms)
    if not has_cleaner:
        unfixed.append((cid, r["title"][:60], has_replaced, last[:80].replace("\n", " ")))
print("  blocked_total tanpa koreksi di komentar terakhir =", len(unfixed))
for u in unfixed:
    print("   UNFIXED:", u)

# 4) blind spot: kartu running dengan LAPOR tanpa ACK
print("-- blind spot running --")
run_rows = con.execute("SELECT id, title, last_heartbeat_at FROM tasks WHERE status='running'").fetchall()
print("  running_count =", len(run_rows))
for r in run_rows:
    cid = r["id"]
    lap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR%')", (cid,)).fetchone()["c"]
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (cid,)).fetchone()["c"]
    hb_age = (time.time() - (r["last_heartbeat_at"] or 0)) / 60
    print(f"  {cid} lap={lap} ack={ack} hb_age_min={hb_age:.0f} :: {r['title'][:60]}")

# 5) umur event terbaru (MAX, bukan MIN)
mx = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
print("last_task_event age_min =", round((time.time() - mx) / 60, 1))
con.close()
