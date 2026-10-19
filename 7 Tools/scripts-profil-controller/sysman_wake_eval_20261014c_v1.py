# Read-only eval of WAKE rows for cron round 2026-10-14c (sysman).
import sqlite3, time, json, os, collections

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = """t_002af121 t_0311d1e4 t_050a75ff t_0bf0854c t_0df60358 t_1168e59f t_14e7030f
t_153594d4 t_1c98456a t_23f7da05 t_2543fb8f t_2ae211bb t_2d32e7c8 t_2e0e92d4 t_30dd071c
t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_483b2d91 t_4d7a1691 t_4edfcf3a t_5831a79d
t_60ed37fa t_64328060 t_674377e1 t_68d1d8be t_7391c81b t_760e7792 t_77a9bcd3 t_799a1879
t_8b90e854 t_8d618268 t_93c6bec3 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a3e70bf1 t_a48e52d1 t_a4b6791b t_a783103d t_a931e1b1 t_aaab1be9
t_b422fa6d t_b81fea6a t_b9500192 t_ba72c512 t_be219ab7 t_c1d55eef t_c792df45 t_c8784acc
t_cb601d70 t_d3cc135a t_d4fca8b3 t_d8480778 t_d9f482ab t_e04bca14 t_e4c7440d t_e5e2e083
t_e8cac74b t_ec2342d5 t_edb280b5 t_efb6071f t_f9ac1ff2""".split()

now = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def tables():
    return [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]

tabs = tables()
# print schema of key tables once
for t in ("tasks", "task_events", "task_comments", "comments", "task_links", "task_runs"):
    if t in tabs:
        cols = [r[1] for r in con.execute(f"PRAGMA table_info({t})")]
        print(f"SCHEMA {t}: {','.join(cols)}")

COM_T = "task_comments" if "task_comments" in tabs else ("comments" if "comments" in tabs else None)

def age(ts):
    return None if ts is None else round((now - ts) / 60)

print("\n=== PER-CARD ===")
rows_by_tenant = collections.defaultdict(list)
for tid in IDS:
    t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(f"{tid} NOT-FOUND")
        continue
    td = dict(t)
    evs = con.execute(
        "SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6",
        (tid,)).fetchall()
    last_ev = f"{evs[0]['kind']}@{age(evs[0]['created_at'])}m" if evs else "none"
    kinds = collections.Counter(e['kind'] for e in con.execute(
        "SELECT kind FROM task_events WHERE task_id=?", (tid,)))
    parents = con.execute(
        "SELECT p.id, p.status, p.title FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?",
        (tid,)).fetchall()
    kids = con.execute(
        "SELECT c.id, c.status FROM task_links l JOIN tasks c ON c.id=l.child_id WHERE l.parent_id=?",
        (tid,)).fetchall()
    ncom = 0
    lastcom = None
    if COM_T:
        ncom = con.execute(f"SELECT COUNT(*) FROM {COM_T} WHERE task_id=?", (tid,)).fetchone()[0]
        lc = con.execute(
            f"SELECT author, substr(body,1,90) b, created_at FROM {COM_T} WHERE task_id=? ORDER BY created_at DESC LIMIT 1",
            (tid,)).fetchone()
        if lc:
            lastcom = f"{lc['author']}@{age(lc['created_at'])}m: {lc['b']!r}"
    ack = lap = mark = 0
    if COM_T:
        ack = con.execute(f"SELECT COUNT(*) FROM {COM_T} WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
        lap = con.execute(f"SELECT COUNT(*) FROM {COM_T} WHERE task_id=? AND body LIKE '%LAPOR%'", (tid,)).fetchone()[0]
        mark = con.execute(f"SELECT COUNT(*) FROM {COM_T} WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()[0]
    line = (f"{tid} | st={td.get('status')} | tenant={td.get('tenant')} | assignee={td.get('assignee')} "
            f"| author={td.get('created_by')} | age_created={age(td.get('created_at'))}m "
            f"| lastev={last_ev} | evkinds={dict(kinds)} | parents={[ (p['id'],p['status']) for p in parents ]} "
            f"| kids={len(kids)}:{collections.Counter(k['status'] for k in kids)} "
            f"| com={ncom} ack={ack} lapor={lap} mark={mark}")
    print(line)
    print(f"    TITLE: {str(td.get('title'))[:110]}")
    if lastcom:
        print(f"    LASTCOM: {lastcom}")
    rows_by_tenant[td.get('tenant')].append((tid, td.get('status')))

print("\n=== TENANT GROUPS ===")
for ten, lst in sorted(rows_by_tenant.items(), key=lambda x: -len(x[1])):
    print(f"{ten}: n={len(lst)} statuses={dict(collections.Counter(s for _, s in lst))}")

print("\n=== BOARD SANITY ===")
mx = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
print(f"max_event_age_min={age(mx)} tasks_total={con.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]}"
      f" events_total={con.execute('SELECT COUNT(*) FROM task_events').fetchone()[0]}"
      + (f" comments_total={con.execute(f'SELECT COUNT(*) FROM {COM_T}').fetchone()[0]}" if COM_T else ""))

print("\n=== GAVE_UP / retry census among IDS ===")
q = ",".join("?" * len(IDS))
gu = con.execute(
    f"SELECT task_id, kind, created_at, substr(COALESCE(detail,''),1,120) d FROM task_events "
    f"WHERE task_id IN ({q}) AND (kind LIKE '%gave%' OR kind LIKE '%retry%' OR kind LIKE '%timed%') "
    f"ORDER BY created_at DESC LIMIT 40", IDS).fetchall() if any(
    r[1] == 'detail' for r in con.execute("PRAGMA table_info(task_events)")) else []
for r in gu:
    print(f"{r['task_id']} {r['kind']} @{age(r['created_at'])}m {r['d']!r}")
if not gu:
    # fallback: kinds only
    gu2 = con.execute(
        f"SELECT task_id, kind, created_at FROM task_events WHERE task_id IN ({q}) "
        f"AND (kind LIKE '%gave%' OR kind LIKE '%retry%' OR kind LIKE '%timed%') ORDER BY created_at DESC LIMIT 40",
        IDS).fetchall()
    for r in gu2:
        print(f"{r['task_id']} {r['kind']} @{age(r['created_at'])}m")
