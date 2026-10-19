# Read-only: evaluate each WAKE finding per card + tenant census (round 14-10c fix)
import sqlite3, time, json, collections, importlib.util

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
spec = importlib.util.spec_from_file_location(
    "wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
findings = mod.scan(DB, now, ["default","sysmanager-cleaner","mission-wake"])
print("wake findings:", len(findings), "unique ids:", len(set(f[0] for f in findings)))
by_class = collections.Counter(f[1] for f in findings)
print("classes:", dict(by_class))

cls_map = collections.defaultdict(set)
age_map = {}
for i, c, a in findings:
    cls_map[i].add(c)
    age_map[i] = max(age_map.get(i, 0), a)
ids = sorted(cls_map)

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
cur = con.cursor()

def q1(sql, args=()):
    return cur.execute(sql, args).fetchone()

def qall(sql, args=()):
    return cur.execute(sql, args).fetchall()

print("\n== PER-CARD EVAL ==")
out = []
for tid in ids:
    t = q1("SELECT id,title,status,tenant,created_by,assignee,max_runtime_seconds,last_heartbeat_at FROM tasks WHERE id=?", (tid,))
    if not t:
        print(tid, "NOT FOUND"); continue
    id_, title, status, tenant, cby, asg, mrs, hb = t
    last_ev = q1("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,))[0]
    ev_tail = [r[0] for r in qall("SELECT kind FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (tid,))]
    parents = [p for (p,) in qall("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))]
    par_st = [f"{p[:10]}:{q1('SELECT status FROM tasks WHERE id=?',(p,))[0]}" for p in parents]
    kids_open = dict(qall("SELECT t.status, COUNT(*) FROM task_links l JOIN tasks t ON t.id=l.child_id WHERE l.parent_id=? GROUP BY t.status", (tid,)))
    n_lapor = q1("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (tid,))[0]
    n_ack = q1("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,))[0]
    n_marker = q1("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,))[0]
    last_cm = q1("SELECT author, substr(replace(replace(body,char(10),' '),char(13),' '),1,110), created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,))
    out.append(dict(id=id_, title=(title or "")[:64], status=status, tenant=tenant or "(null)",
                    cby=cby, cls=sorted(cls_map[tid]), age_min=age_map[tid],
                    ev_age_min=round((now-(last_ev or 0))/60,1) if last_ev else None,
                    ev_tail=ev_tail, parents=par_st, kids_open=kids_open,
                    lapor=n_lapor, ack=n_ack, marker=n_marker,
                    last_cm=(f"{last_cm[0]}| {last_cm[1]}" if last_cm else None)))

for o in out:
    print(json.dumps(o, ensure_ascii=False))

print("\n== WAKE IDS BY TENANT ==")
print(dict(collections.Counter(o["tenant"] for o in out)))

for tn in sorted(set(o["tenant"] for o in out)):
    print(f"\n== FULL TENANT {tn} ==")
    for st, c in qall("SELECT status, COUNT(*) FROM tasks WHERE tenant=? GROUP BY status", (tn,)):
        print(f"  {st}: {c}")
    d = qall("""SELECT t.id,
        (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%'),
        (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-WAKE done-unacked%')
        FROM tasks t WHERE t.tenant=? AND t.status='done'""", (tn,))
    noack = [x for x in d if x[1] == 0]
    print(f"  done={len(d)} done_no_ack={len(noack)} marked={sum(1 for x in noack if x[2]>0)}")
con.close()
