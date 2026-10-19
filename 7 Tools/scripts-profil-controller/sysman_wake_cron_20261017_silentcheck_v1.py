# Ronde senyap 17-10: rekonsiliasi stdout kosong vs keadaan papan (read-only).
import sqlite3, time, sys, importlib.util
from datetime import datetime, timezone

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = HOME + "/kanban.db"
SCAN = HOME + "/scripts/gsp_mission_wake_scan.py"

# 1) panggil scan() kanonis, tangkap nilai kembaliannya (bukan stdout)
spec = importlib.util.spec_from_file_location("gsp_mission_wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
findings = mod.scan(DB, int(time.time()), authors)
print("scan() temuan =", len(findings))
for f in findings:
    print("  ROW:", tuple(f))

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = int(time.time())

# 2) umur event terakhir papan (MAX, bukan MIN)
for tbl, col in [("task_events", "created_at"), ("task_comments", "created_at")]:
    r = con.execute(f"SELECT MAX({col}) m FROM {tbl}").fetchone()
    age = (now - r["m"]) / 60.0 if r["m"] else None
    print(f"max {tbl} age_min =", round(age, 1) if age is not None else "NONE")

# 3) sensus kartu terbuka non-done/archived
rows = con.execute(
    "SELECT id,title,status,tenant,assignee,created_by,created_at,completed_at,"
    "block_kind,current_run_id,last_heartbeat_at FROM tasks "
    "WHERE status NOT IN ('done','archived') ORDER BY status, created_at DESC"
).fetchall()
print("open (non done/archived) =", len(rows))
by_status = {}
for r in rows:
    by_status.setdefault(r["status"], 0)
    by_status[r["status"]] += 1
print("by_status:", by_status)

# 4) untuk tiap blocked: umur event terakhir kartu + apakah komentar terakhirnya koreksi/marker
cur2 = con.cursor()  # cursor terpisah utk query dalam
for r in rows:
    if r["status"] != "blocked":
        continue
    ev = cur2.execute(
        "SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)
    ).fetchone()["m"]
    cm = cur2.execute(
        "SELECT author, body, created_at FROM task_comments WHERE task_id=? "
        "ORDER BY created_at DESC LIMIT 1", (r["id"],)
    ).fetchone()
    last_age = round((now - ev) / 60.0, 0) if ev else None
    tail = (cm["body"][:70].replace("\n", " ") if cm else "(tanpa komentar)")
    mark = ""
    if cm:
        b = cm["body"]
        for tok in ("[SYSMAN-CLEANER", "RANTAI-WAKE", "Digantikan", "ANCHOR-KONTRAK", "DITAHAN"):
            if tok in b:
                mark += "[" + tok + "]"
    print(f"BLK {r['id']} | {r['title'][:38]} | evt_age={last_age}m | blk={r['block_kind']} | last={mark or 'TANPA-TOKEN'} :: {tail}")

# 5) blind spot rute-4b: kartu done <=24j tanpa RANTAI-ACK dari author lain
cand = con.execute(
    "SELECT id,title,tenant,completed_at,created_by FROM tasks "
    "WHERE status='done' AND completed_at > ? ORDER BY completed_at DESC LIMIT 50",
    (now - 86400,),
).fetchall()
print("done-24j =", len(cand))
cur3 = con.cursor()
for r in cand:
    acks = cur3.execute(
        "SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
        (r["id"],),
    ).fetchall()
    if len(acks) == 0:
        print(f"  DONE-NOACK {r['id']} | {r['title'][:40]} | tenant={r['tenant']} | by={r['created_by']}")
