# Ronde wake 16-10f: nilai 6 baris WAKE + orang tua stalled + kesegaran papan
import sqlite3, time, importlib.util, os

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
for tbl, col in (("task_events", "created_at"), ("task_comments", "created_at")):
    r = con.execute(f"SELECT MAX({col}) m FROM {tbl}").fetchone()
    print(f"  {tbl}: age_min={round((now - r['m'])/60, 1)}")

ids = ["t_09c1c9b3", "t_557d84cc", "t_5b044505", "t_65fb51b1", "t_b97f1bc9", "t_e0090b1a"]
for cid in ids:
    t = con.execute("SELECT id,title,status,tenant,completed_at,created_by,assignee,created_at FROM tasks WHERE id=?", (cid,)).fetchone()
    if not t:
        print(f"\n{cid}: TIDAK ADA")
        continue
    print(f"\n== {cid} [{t['status']}] tenant={t['tenant']} by={t['created_by']} assignee={t['assignee']}")
    print(f"   title={t['title'][:100]}")
    evs = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (cid,)).fetchall()
    print(f"   events={[ (e['kind'], round((now-e['created_at'])/60)) for e in evs ]}")
    parents = con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (cid,)).fetchall()
    kids = con.execute("SELECT child_id FROM task_links WHERE parent_id=?", (cid,)).fetchall()
    for p in parents:
        pt = con.execute("SELECT id,title,status FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
        print(f"   PARENT {p['parent_id']} [{pt['status'] if pt else '?'}] {pt['title'][:60] if pt else ''}")
    if kids:
        kstat = []
        kid_ids = [k["child_id"] for k in kids]
        for k in kid_ids:
            kt = con.execute("SELECT status FROM tasks WHERE id=?", (k,)).fetchone()
            kstat.append((k, kt["status"] if kt else "?"))
        print(f"   KIDS({len(kid_ids)})={kstat}")
    comps = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (cid,)).fetchall()
    for c in comps[-6:]:
        print(f"   CMT [{c['author']} {round((now-c['created_at'])/60)}m] {c['body'][:160].replace(chr(10),' | ')}")
    if not comps:
        print("   CMT: (tidak ada komentar)")
