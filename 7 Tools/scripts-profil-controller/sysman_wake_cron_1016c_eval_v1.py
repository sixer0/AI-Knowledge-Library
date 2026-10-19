# Ronde wake 16-10c: rekonsiliasi scan() kanonis vs kandidat longgar + marker + kesegaran papan
import sqlite3, time, importlib.util, os, json

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
spec = importlib.util.spec_from_file_location(
    "mws", os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py"))
mws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mws)

now = int(time.time())
authors = getattr(mws, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

findings = mws.scan(DB, now, authors)
print("== scan() kanonis:", len(findings), "temuan")
for f in findings:
    print("  ", tuple(f))

print("== kesegaran papan (MAX created_at) ==")
for tbl, col in (("task_events", "created_at"), ("task_comments", "created_at"), ("task_runs", "started_at")):
    try:
        r = con.execute(f"SELECT MAX({col}) m FROM {tbl}").fetchone()
        print(f"  {tbl}: age_min={round((now - r['m'])/60, 1)}")
    except Exception as e:
        print(f"  {tbl}: ERR {e}")

print("== sensus status ==")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  {r['status']} = {r['n']}")

cands = ["t_ba9f0bf6", "t_2da2d99f", "t_8998b559", "t_8da71c9f", "t_fb910478"]
print("== profil kandidat longgar detail_v2 ==")
for cid in cands:
    t = con.execute("SELECT id,title,status,tenant,completed_at,created_by,assignee FROM tasks WHERE id=?", (cid,)).fetchone()
    if not t:
        print(f"  {cid}: TIDAK ADA")
        continue
    comps = con.execute("SELECT author, substr(body,1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (cid,)).fetchall()
    lap = [c for c in comps if "LAPOR" in c["b"].upper()]
    ack = [c for c in comps if "RANTAI-ACK" in c["b"].upper()]
    mark = [c for c in comps if "RANTAI-WAKE" in c["b"].upper()]
    print(f"  {cid} [{t['status']}] tenant={t['tenant']} done_age={(now-(t['completed_at'] or now))/60:.0f}m by={t['created_by']} assignee={t['assignee']}")
    print(f"     title={t['title'][:70]}")
    print(f"     LAPOR={[(c['author'], round((now-c['created_at'])/60)) for c in lap]}")
    print(f"     ACK={[(c['author'], round((now-c['created_at'])/60)) for c in ack]}")
    print(f"     MARKER={[(c['author'], c['b'][:40], round((now-c['created_at'])/60)) for c in mark]}")
    if not lap:
        print(f"     komentar terakhir={[(c['author'], c['b'][:50], round((now-c['created_at'])/60)) for c in comps[-2:]]}")
