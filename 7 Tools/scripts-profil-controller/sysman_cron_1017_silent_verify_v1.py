# Ronde senyap 17-10: konfirmasi scan()=0 temuan + sensus komentar terakhir kartu non-done
import importlib.util, sqlite3, time, os, sys

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")

spec = importlib.util.spec_from_file_location("mws", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")

now = int(time.time())
findings = mod.scan(DB, now, authors)
print("SCAN findings =", len(findings))
for f in findings:
    print("  ROW:", tuple(f))

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

# census non-done/archived
rows = cur.execute(
    "SELECT id,title,status,tenant,created_at FROM tasks WHERE status NOT IN ('done','archived')"
).fetchall()
print("NON-DONE count =", len(rows), "| statuses:",
      {s: sum(1 for r in rows if r['status'] == s) for s in set(r['status'] for r in rows)})

# komentar terakhir per kartu non-done: ada penanda koreksi/vonis?
ids = [r["id"] for r in rows]
marker_tok = ("[SYSMAN-CLEANER", "RANTAI-WAKE", "Digantikan", "ANCHOR-KONTRAK",
              "DITAHAN", "WATCH-1011", "triase")
uncorrected = []
for tid in ids:
    c2 = con.cursor()
    c = c2.execute(
        "SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",
        (tid,)).fetchone()
    body = c["body"] if c else ""
    age_h = (now - c["created_at"]) / 3600.0 if c else None
    hit = any(tok.lower() in body.lower() for tok in marker_tok)
    if not hit:
        uncorrected.append((tid, age_h, body[:90].replace("\n", " ")))
print("UNCORRECTED (no triage/correction token in last comment) =", len(uncorrected))
for u in uncorrected[:20]:
    print("  UNC:", u)

# umur event terakhir papan (MAX, bukan MIN)
m = cur.execute("SELECT MAX(created_at) m FROM task_events").fetchone()
mc = cur.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()
print("last task_event age_min =", round((now - m["m"]) / 60.0, 1))
print("last comment   age_min =", round((now - mc["m"]) / 60.0, 1))
con.close()
