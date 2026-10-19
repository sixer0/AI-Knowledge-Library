# Read-only wake evaluation for cron round 14-10b (late): per-id detail + tenant census.
import sqlite3, time, json, sys

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

IDS = """t_002af121 t_0311d1e4 t_0913266d t_0918b6d2 t_0ac8927f t_0ba22121 t_0bf0854c
t_0f3e37eb t_1168e59f t_14e7030f t_153594d4 t_19930381 t_1c98456a t_23f7da05 t_2e0e92d4
t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_5291d587 t_5715d1fc t_5831a79d t_60ed37fa
t_6aa0384c t_7124c228 t_7391c81b t_7707a0cd t_77a9bcd3 t_799a1879 t_7f36de9e t_80a9fb43
t_896447e4 t_95b5b6cb t_99418ea0 t_99bb85a4 t_9bf75422 t_9e457da5 t_9ebc8fbc t_a064e4cc
t_a148a692 t_a37d190b t_a48e52d1 t_a4b6791b t_a66ce30a t_ad5d8e6f t_b2b82e31 t_c2180f14
t_c8784acc t_cb601d70 t_ccfca3b8 t_d4fca8b3 t_de326482 t_de73c01d t_deb670d0 t_e04bca14
t_ed8b0b54 t_efb6071f t_f9ac1ff2""".split()

def one(cur, q, *a):
    r = cur.execute(q, a).fetchone()
    return r

# board sanity
cur = con.cursor()
r = one(cur, "SELECT COUNT(*) n FROM tasks")
e = one(cur, "SELECT MAX(created_at) m FROM task_events")
print(f"# SANITY tasks={r['n']} last_event_age_min={round((NOW-e['m'])/60)}")

# per-id detail
print("\n# PER-ID DETAIL")
for tid in IDS:
    c = con.cursor()
    t = c.execute("SELECT id,title,status,tenant,created_by,assignee,created_at,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(f"{tid} | NOT-FOUND")
        continue
    le = c.execute("SELECT kind,MAX(created_at) m FROM task_events WHERE task_id=? GROUP BY kind ORDER BY m DESC LIMIT 1", (tid,)).fetchone()
    kinds = [row['kind'] for row in c.execute("SELECT DISTINCT kind FROM task_events WHERE task_id=?", (tid,))]
    par = c.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()
    parents = []
    for p in par:
        pt = c.execute("SELECT id,status,title FROM tasks WHERE id=?", (p['parent_id'],)).fetchone()
        parents.append(f"{pt['id']}:{pt['status']}" if pt else p['parent_id'])
    nlap = c.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (tid,)).fetchone()['n']
    nack = c.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()['n']
    nmark = c.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()['n']
    lastc = c.execute("SELECT author,SUBSTR(body,1,90) b,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    print(f"{tid} | {t['status']} | tenant={t['tenant']} | created_by={t['created_by']} | age_min={round((NOW-t['created_at'])/60)} | lastev={le['kind'] if le else '-'}@{round((NOW-le['m'])/60) if le else '-'}m | evkinds={','.join(kinds)} | parents={parents} | LAPOR={nlap} ACK={nack} MARKER={nmark}")
    if lastc:
        print(f"    last_comment by {lastc['author']} @{round((NOW-lastc['created_at'])/60)}m: {lastc['b'].replace(chr(10),' ')}")

# tenant census for tenants seen
print("\n# TENANT CENSUS")
tenants = set()
c = con.cursor()
for row in c.execute("SELECT DISTINCT tenant FROM tasks WHERE id IN (%s)" % ",".join("?"*len(IDS)), IDS):
    if row['tenant']:
        tenants.add(row['tenant'])
for tn in sorted(tenants):
    c = con.cursor()
    rows = c.execute("SELECT status,COUNT(*) n FROM tasks WHERE tenant=? GROUP BY status", (tn,)).fetchall()
    tot = sum(r['n'] for r in rows)
    print(f"tenant {tn}: total={tot} " + " ".join(f"{r['status']}={r['n']}" for r in rows))
    # done cards ack census
    d = c.execute("SELECT id,(SELECT COUNT(*) FROM task_comments x WHERE x.task_id=t.id AND body LIKE '%RANTAI-ACK%') acks,(SELECT COUNT(*) FROM task_comments x WHERE x.task_id=t.id AND body LIKE '%RANTAI-WAKE done-unacked%') mk FROM tasks t WHERE tenant=? AND status='done'", (tn,)).fetchall()
    noack = [x['id'] for x in d if x['acks']==0]
    print(f"   done={len(d)} done_no_ack={len(noack)} marked={sum(1 for x in d if x['mk']>0)} -> {noack[:12]}")
    # gave_up / timed_out events in tenant
    g = c.execute("SELECT e.kind,COUNT(DISTINCT e.task_id) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind IN ('timed_out','gave_up') GROUP BY e.kind", (tn,)).fetchall()
    print(f"   timeout_events={[(r['kind'],r['n']) for r in g]}")
    # unblocked events after blocking
    ub = c.execute("SELECT COUNT(*) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind='unblocked'", (tn,)).fetchone()['n']
    bl = c.execute("SELECT COUNT(*) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind='blocked'", (tn,)).fetchone()['n']
    print(f"   blocked_events={bl} unblocked_events={ub}")

# running cards blind spot sweep
print("\n# RUNNING CARDS (blind spot)")
c = con.cursor()
for row in c.execute("SELECT id,title,status,tenant,created_by,created_at FROM tasks WHERE status='running'").fetchall():
    c2 = con.cursor()
    hb = c2.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=? AND kind='heartbeat'", (row['id'],)).fetchone()['m']
    lap = c2.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (row['id'],)).fetchone()['n']
    ack = c2.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (row['id'],)).fetchone()['n']
    print(f"{row['id']} | tenant={row['tenant']} | hb_age={round((NOW-hb)/60) if hb else 'none'}m | LAPOR={lap} ACK={ack} | {row['title'][:60]}")
