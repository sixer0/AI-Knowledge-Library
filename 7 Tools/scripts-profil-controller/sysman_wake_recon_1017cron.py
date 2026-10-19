# Reconciliation: canonical scan() + last-comment coverage on blocked pop (17-10 cron)
import importlib.util, sqlite3, time, sys

# 1) canonical scan() — signature (db_path, now_epoch_INT, controller_authors_LIST)
spec = importlib.util.spec_from_file_location("wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
db = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
authors = authors.split(",") if isinstance(authors, str) else list(authors)
findings = mod.scan(db, int(time.time()), authors)
print(f"SCAN findings={len(findings)}")
for f in findings:
    print("FINDING:", f)

# 2) blocked population: last comment token coverage
now = int(time.time())
con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()
ids = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE status='blocked' ORDER BY id")]
print(f"blocked={len(ids)}")
missing = []
for cid in ids:
    lc = cur.execute("SELECT body, author, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (cid,)).fetchone()
    ev = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()["m"]
    ev_age = int((now-ev)/60) if ev else -1
    body = (lc["body"] if lc else "") or ""
    tok = "CLEANER" if "SYSMAN-CLEANER" in body else ("RANTAI-WAKE" if "RANTAI-WAKE" in body else ("NONE" if not lc else "OTHER"))
    if tok in ("NONE", "OTHER"):
        missing.append((cid, tok, ev_age, body[:90].replace("\n"," ")))
print(f"without cleaner/wake marker: {len(missing)}")
for m in missing:
    print("MISS:", m)

# 3) last event age per blocked card (stale freeze signature)
ages = [int((now - cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()["m"])/60) for cid in ids]
if ages:
    print(f"blocked last-event age min={min(ages)} max={max(ages)}")
con.close()
