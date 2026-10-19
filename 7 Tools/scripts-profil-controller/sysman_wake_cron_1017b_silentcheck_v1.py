# Ronde senyap 17-10: vonis scan() kanonis + penilaian 44 kartu blocked
import importlib.util, sqlite3, time, os, json

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")

# 1) panggil scan() kanonis (importlib), tangkap nilai kembaliannya (list tuple)
spec = importlib.util.spec_from_file_location(
    "wake_scan", os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
findings = mod.scan(DB, int(time.time()), authors)
print("SCAN findings =", len(findings))
for f in findings:
    print("  ROW:", f)

# 2) sensus kartu blocked: status, umur event terakhir, komentar terakhir, marker
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
rows = cur.execute("""
  SELECT id, title, status, tenant, created_at, block_kind
  FROM tasks WHERE status='blocked' ORDER BY created_at DESC
""").fetchall()
ids = [r["id"] for r in rows]
print("BLOCKED count =", len(ids))
now = time.time()
for r in rows:
    tid = r["id"]
    ev = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    cm = cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    age_ev = round((now - ev)/60.0, 1) if ev else None
    last = ""
    if cm:
        body = (cm["body"] or "").replace("\n", " ")[:110]
        last = f"[{cm['author']}] {body}"
    else:
        last = "(no comment)"
    print(f"BLOCKED {tid} | {r['title'][:52]} | tenant={r['tenant']} | ev_age_min={age_ev} | bk={r['block_kind']} | last: {last}")
con.close()
