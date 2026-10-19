# Read-only: evaluate each WAKE line per card + tenant census (round 14-10c)
import sqlite3, time, re, json, collections

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
cur = con.cursor()
now = int(time.time())

# Parse wake lines from scan output saved by previous run (re-run scan module instead)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sig = str(inspect_sig := getattr(mod.scan, "__doc__", ""))[:200] if hasattr(mod, "scan") else "no scan()"
print("scan() doc snippet:", sig)

lines = mod.scan(DB, now, ["default", "sysmanager-cleaner", "mission-wake"]) \
      if hasattr(mod, "scan") else []
rows = []
for ln in lines:
    parts = ln.split() if isinstance(ln, str) else None
    if parts and parts[0] == "WAKE":
        rows.append((parts[1], parts[2], int(parts[3])))
print("wake lines:", len(rows), "unique ids:", len(set(r[0] for r in rows)))

by_class = collections.Counter(r[1] for r in rows)
print("classes:", dict(by_class))

ids = sorted(set(r[0] for r in rows))
cls_map = collections.defaultdict(set)
age_map = {}
for i, c, a in rows:
    cls_map[i].add(c)
    age_map[i] = max(age_map.get(i, 0), a)

def q1(sql, args=()):
    return cur.execute(sql, args).fetchone()

def qall(sql, args=()):
    return cur.execute(sql, args).fetchall()

print("\n== PER-CARD EVAL ==")
out = []
for tid in ids:
    t = q1("SELECT id,title,status,tenant,created_by,assignee,max_runtime_seconds,last_heartbeat_at,started_at,completed_at,reason IS NOT NULL FROM tasks WHERE id=?", (tid,)) \
        if False else q1("SELECT id,title,status,tenant,created_by,assignee,max_runtime_seconds,last_heartbeat_at,started_at,completed_at FROM tasks WHERE id=?", (tid,))
    if not t:
        print(tid, "NOT FOUND"); continue
    id_, title, status, tenant, cby, asg, mrs, hb, started, completed = t
    last_ev = q1("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,))[0]
    ev_kinds = [k for (k,) in q1("SELECT GROUP_CONCAT(kind) FROM (SELECT kind FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6)" , (tid,))[0].split(",")] if q1("SELECT COUNT(*) FROM task_events WHERE task_id=?", (tid,))[0] else []
    parents = [p for (p,) in qall("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))]
    par_st = []
    for p in parents:
        ps = q1("SELECT status FROM tasks WHERE id=?", (p,))[0]
        par_st.append(f"{p[:8]}:{ps}")
    kids = q1("SELECT COUNT(*) FROM task_links WHERE parent_id=?", (tid,))[0][0]
    kids_open = qall("SELECT t.status, COUNT(*) FROM task_links l JOIN tasks t ON t.id=l.child_id WHERE l.parent_id=? GROUP BY t.status", (tid,))
    n_lapor = q1("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%' OR body LIKE '%LAPOR-SELESEI%')", (tid,))[0][0]
    n_ack = q1("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,))[0][0]
    n_marker = q1("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,))[0][0]
    last_cm = q1("SELECT author, substr(body,1,90), created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,))[0]
    out.append(dict(id=id_, title=(title or "")[:70], status=status, tenant=tenant or "(null)",
                    created_by=cby, assignee=asg, cls=sorted(cls_map[tid]), age_min=age_map[tid],
                    ev_age_min=round((now-(last_ev or 0))/60,1) if last_ev else None,
                    last_evs=ev_kinds, parents=par_st, kids=kids, kids_open=dict(kids_open),
                    lapor=n_lapor, ack=n_ack, marker=n_marker,
                    last_cm=(f"{last_cm[0]}|{last_cm[1]}" if last_cm else None)))

for o in out:
    print(json.dumps(o, ensure_ascii=False))

print("\n== TENANT CENSUS OF WAKE IDS ==")
tc = collections.Counter(o["tenant"] for o in out)
print(dict(tc))

# Tenant census full for tenants seen
for tn in sorted(set(o["tenant"] for o in out)):
    if tn == "(null)": continue
    print(f"\n== FULL TENANT {tn} ==")
    for st, c in qall("SELECT status, COUNT(*) FROM tasks WHERE tenant=? GROUP BY status", (tn,)):
        print(f"  {st}: {c}")
    # done cards without ACK
    d = qall("SELECT t.id, (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%'), (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-WAKE done-unacked%') FROM tasks t WHERE t.tenant=? AND t.status='done'", (tn,))
    noack = [x for x in d if x[1] == 0]
    print(f"  done total={len(d)} done_no_ack={len(noack)} of_which_marked={sum(1 for x in noack if x[2]>0)}")
con.close()
