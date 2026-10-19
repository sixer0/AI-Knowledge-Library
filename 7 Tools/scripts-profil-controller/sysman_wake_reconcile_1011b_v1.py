# Read-only reconciliation: canonical scan() vs detail_v2 WAKE=1 candidates.
import importlib.util, json, sqlite3, os, time

HERMES = os.path.expandvars(r"C:/Users/TRIAL/AppData/Local/hermes")
DB = os.path.join(HERMES, "kanban.db")
SCAN = os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py")

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

rows = None
for name in ("scan", "main", "run"):
    fn = getattr(mod, name, None)
    if callable(fn):
        try:
            r = fn()
            if isinstance(r, list):
                rows = r
                print(f"[canonical] {name}() -> {len(r)} rows")
                for x in r:
                    print("  ", x)
                break
        except TypeError:
            continue
if rows is None:
    print("[canonical] scan() tidak mengembalikan list; cek fungsi tersedia:",
          [n for n in dir(mod) if not n.startswith("_")][:30])

ids = ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3"]
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = time.time()
print("\n-- kandidat detail_v2 (replik longgar) vs fakta papan --")
for tid in ids:
    t = con.execute("SELECT id,title,status,tenant,assignee,created_by,completed_at,last_heartbeat_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(f"{tid}: TIDAK ADA di tasks"); continue
    comments = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)).fetchall()
    ev_last = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    def age(s):
        return round((now - float(s))/60.0, 1) if s else None
    print(f"\n{tid} | {t['title'][:60]}")
    print(f"  status={t['status']} tenant={t['tenant']!r} assignee={t['assignee']} author={t['created_by']} done_age_m={age(t['completed_at'])} hb_age_m={age(t['last_heartbeat_at'])} ev_age_m={age(ev_last)}")
    for c in comments[-6:]:
        print(f"  [{round((now-float(c['created_at']))/60,1)}m] {c['author']}: {c['body'][:110].replace(chr(10),' ')}")
con.close()
