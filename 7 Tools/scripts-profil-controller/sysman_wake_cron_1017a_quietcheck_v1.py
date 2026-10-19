# Ronde senyap 17-10: replika scan() kanonis + sensus blocked + cek marker
import importlib.util, sqlite3, time, os, sys

HERMES = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HERMES, "kanban.db")
SCAN = os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py")

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")

rows = mod.scan(DB, int(time.time()), authors)
print("SCAN findings =", len(rows))
for r in rows:
    print("  ", tuple(r))

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("\n-- census blocked (44) --")
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='blocked' ORDER BY created_at")]
triaged = 0
untouched = []
for tid in ids:
    c = con.cursor()
    last = c.execute(
        "SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",
        (tid,)
    ).fetchone()
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    age_min = (time.time() - ev) / 60.0 if ev else -1
    body = (last["body"] if last else "") or ""
    t = con.execute("SELECT title, tenant FROM tasks WHERE id=?", (tid,)).fetchone()
    marker = ("SYSMAN-CLEANER" in body) or ("RANTAI-WAKE" in body) or ("Digantikan" in body)
    if marker:
        triaged += 1
    else:
        untouched.append((tid, t["title"][:60], t["tenant"], round(age_min), (last["author"] if last else "-"), body[:70].replace("\n", " ")))
print("blocked total =", len(ids), "| marker-last-comment =", triaged, "| tanpa-marker =", len(untouched))
for u in untouched:
    print("  UNTOUCHED:", u)

print("\n-- todo/in_progress/in_review counts --")
for st in ("todo", "in_progress", "in_review", "pending"):
    n = con.execute("SELECT COUNT(*) FROM tasks WHERE status=?", (st,)).fetchone()[0]
    print(f"  {st} = {n}")

print("\n-- done 24h tanpa ACK (cek rute-4b manual) --")
cutoff = time.time() - 86400
cands = con.execute(
    "SELECT id, title, tenant, completed_at FROM tasks WHERE status='done' AND completed_at > ? ORDER BY completed_at DESC",
    (cutoff,)
).fetchall()
print("done-24h =", len(cands))
for c in cands:
    acks = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (c["id"],)).fetchone()[0]
    marks = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (c["id"],)).fetchone()[0]
    if acks == 0 and marks == 0:
        print("  NOACK-NOMARK:", c["id"], (c["tenant"] or "-"), c["title"][:60])

print("\n-- heartbeat running check (should be empty since running=0) --")
hb = con.execute("SELECT COUNT(*) FROM tasks WHERE status='running'").fetchone()[0]
print("running =", hb)
con.close()
