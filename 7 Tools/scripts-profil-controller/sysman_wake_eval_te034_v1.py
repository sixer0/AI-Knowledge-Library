# Read-only eval of card t_e034cb5e: comments, LAPOR-SELESAI vs RANTAI-ACK authors,
# plus canonical scan() reconciliation. Targeted per-id (not fixed-sample tools).
import sqlite3, os, json, sys, time, importlib.util

ROOT = r"C:/Users/TRIAL/AppData/Local/hermes"
CARD = sys.argv[1] if len(sys.argv) > 1 else "t_e034cb5e"

cands = [os.path.join(ROOT, "kanban.db"),
         os.path.join(ROOT, "boards", "default", "kanban.db"),
         os.path.join(ROOT, "boards", "gsp", "kanban.db")]
db = next((p for p in cands if os.path.exists(p)), None)
print("DB USED:", db)
con = sqlite3.connect(db)
con.row_factory = sqlite3.Row
cur = con.cursor()

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("TABLES:", tables)

def cols(t):
    try:
        return [r[1] for r in cur.execute(f"PRAGMA table_info({t})")]
    except Exception:
        return []

print("tasks cols:", cols("tasks"))
ctab = "comments" if "comments" in tables else ("task_comments" if "task_comments" in tables else None)
print("comment table:", ctab, "cols:", cols(ctab) if ctab else None)

row = cur.execute("SELECT * FROM tasks WHERE id=?", (CARD,)).fetchone()
if row:
    d = dict(row)
    print("CARD:", {k: d.get(k) for k in ("id","status","tenant","assignee","completed_at","created_at")})

now = time.time()
if ctab:
    rows = cur.execute(f"SELECT * FROM {ctab} WHERE task_id=? ORDER BY created_at", (CARD,)).fetchall()
    print(f"COMMENTS ({len(rows)}):")
    for r in rows:
        d = dict(r)
        body = (d.get("body") or d.get("comment") or d.get("text") or "")[:160].replace("\n"," | ")
        age = int(now - d.get("created_at", 0))
        print(f"  [{d.get('created_at')}] age={age//60}m author={d.get('author') or d.get('created_by')}: {body}")

# event kinds terminal
if "task_events" in tables:
    ev = cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 8", (CARD,)).fetchall()
    print("LAST EVENTS:", [(e['kind'], int(now-e['created_at'])//60) for e in ev])

# canonical scan() reconciliation
spec = importlib.util.spec_from_file_location("wake_scan", os.path.join(ROOT, "scripts", "gsp_mission_wake_scan.py"))
m = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(m)
    out = m.scan() if hasattr(m, "scan") else None
    print("SCAN OUTPUT:", repr(out))
except Exception as e:
    print("SCAN IMPORT FAIL:", e)
