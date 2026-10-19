# Ronde senyap 17-10 (cron mission-wake): rekonsiliasi stdout kosong.
# 1) MAX(created_at) lintas events/comments/runs/tasks (anti MIN-menipu)
# 2) vonis kanonis via importlib scan()
# 3) sensus kartu terbuka non-done: rem apa yang menempel di komentar terakhir
import importlib.util, json, os, sqlite3, time
from datetime import datetime, timezone

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row


def max_age(col, table, where=""):
    q = f"SELECT MAX({col}) AS m, COUNT(*) AS n FROM {table}" + ((" WHERE " + where) if where else "")
    r = con.execute(q).fetchone()
    if not r["m"]:
        return f"{table}: KOSONG (n=0)"
    try:
        ts = float(r["m"])
    except (TypeError, ValueError):
        ts = datetime.fromisoformat(str(r["m"]).replace("Z", "+00:00")).timestamp()
    age = (time.time() - ts) / 60.0
    return f"{table}: n={r['n']} max_age_min={age:.1f}"


print("-- kesegaran (MAX, bukan MIN) --")
for spec in (("created_at", "task_events"), ("created_at", "task_comments"),
             ("started_at", "task_runs"), ("created_at", "tasks")):
    print(max_age(*spec))

print("-- sensus status --")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"{r['status']} = {r['n']}")

print("-- kelas blind-spot (running/todo) --")
rows = con.execute("SELECT id,status,title FROM tasks WHERE status IN ('running','todo','in_progress')").fetchall()
print("jumlah =", len(rows))
for r in rows[:20]:
    print(" ", r["id"], r["status"], r["title"][:70])

print("-- vonis kanonis scan() --")
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
now = int(time.time())
fn = getattr(mod, "scan", None)
findings = None
if fn:
    try:
        findings = fn(DB, now, authors)
    except TypeError as e:
        print("TypeError signature:", e)
        findings = fn(DB, now)
print("temuan scan() =", 0 if findings is None else len(findings))
if findings:
    for f in findings:
        print("  FINDING", tuple(f) if not isinstance(f, (str, int, float)) else f)

print("-- 44 blocked: rem di komentar terakhir --")
open_rows = con.execute(
    "SELECT id, tenant, status, title, created_at FROM tasks "
    "WHERE status NOT IN ('done','archived') ORDER BY tenant NULLS LAST, id"
).fetchall()
print("kartu terbuka non-done/archived =", len(open_rows))
cc = con.cursor()
rem_counts = {}
detail = []
for r in open_rows:
    cs = cc.execute(
        "SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC",
        (r["id"],),
    ).fetchall()
    last = cs[0]["body"] if cs else ""
    allbody = "\n".join(c["body"] for c in cs)
    if "[SYSMAN-CLEANER" in allbody:
        rem = "SYSMAN-CLEANER"
    elif "RANTAI-WAKE" in allbody:
        rem = "RANTAI-WAKE"
    elif "Digantikan t_" in allbody:
        rem = "DIGANTIKAN"
    elif "[FASE]" in allbody:
        rem = "FASE"
    elif "ANCHOR-KONTRAK" in allbody or "ANCHOR" in last:
        rem = "ANCHOR"
    elif not cs:
        rem = "TANPA-KOMENTAR"
    else:
        rem = "TANPA-REM"
    rem_counts[rem] = rem_counts.get(rem, 0) + 1
    age_h = (time.time() - float(r["created_at"])) / 3600.0
    detail.append((rem, r["id"], r["tenant"], r["status"], round(age_h, 1), (last or "")[:90].replace("\n", " ")))
print("rekap rem:", json.dumps(rem_counts, ensure_ascii=False))
for d in detail:
    if d[0] in ("TANPA-REM", "TANPA-KOMENTAR"):
        print("  BUTIR?", d)
print("-- akhir --")
con.close()
