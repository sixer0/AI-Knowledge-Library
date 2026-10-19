# Cron ronde g 11-10: rekonsiliasi scan() kanonis + evaluasi per-kartu kandidat detail_v2
import importlib.util, sqlite3, time, json, os

HERMES = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HERMES, "kanban.db")
SCAN = os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py")

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# ambang dari sumber
for nm in ("STALLED_MIN","RUN_WINDOW_H","FASE_STALL_MIN","DONE_UNACKED_MIN"):
    print(nm, "=", getattr(mod, nm, "?"))
print("DEFAULT_AUTHORS =", getattr(mod, "DEFAULT_AUTHORS", "?"))
print("CUTOFF literal search:")
src = open(SCAN, encoding="utf-8").read()
import re
for m in re.finditer(r"1[78]\d{8}", src):
    print("  literal", m.group(0))

now = int(time.time())
auth = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
auth_list = auth.split(",") if isinstance(auth, str) else list(auth)
rows = mod.scan(DB, now, auth_list)
print("=== CANONICAL scan() rows:", len(rows))
for r in rows:
    print("WAKE", r)

cands = ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3",
         "t_c08057c4","t_52521c3b"]
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
print("=== PER-KARTU ===")
for cid in cands:
    t = con.execute("SELECT id,title,status,tenant,assignee,created_by,completed_at,last_heartbeat_at FROM tasks WHERE id=?", (cid,)).fetchone()
    if not t:
        print(cid, "NOT FOUND"); continue
    done_age = (now - t["completed_at"])/60 if t["completed_at"] else None
    print(f"\n--- {cid} | {t['title'][:60]} | status={t['status']} tenant={t['tenant']!r} assignee={t['assignee']} by={t['created_by']} done_age_min={done_age and round(done_age,1)}")
    cs = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (cid,)).fetchall()
    for c in cs:
        age = (now - c["created_at"])/60
        print(f"   [{age:7.1f}m] {c['author']}: {c['body'][:110].replace(chr(10),' | ')}")
con.close()
