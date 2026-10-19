# sysman cron 15-10 ronde A: nilai 33 baris WAKE stalled dari kanban.db root (read-only)
import sqlite3, time, json, collections

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = ["t_002af121","t_0311d1e4","t_0bf0854c","t_1168e59f","t_14e7030f","t_153594d4",
"t_1c98456a","t_23f7da05","t_2e0e92d4","t_34bf2edc","t_3782b61a","t_397be920","t_46ff8be6",
"t_5831a79d","t_60ed37fa","t_7391c81b","t_77a9bcd3","t_799a1879","t_95b5b6cb","t_99418ea0",
"t_9bf75422","t_9e457da5","t_9ebc8fbc","t_a064e4cc","t_a37d190b","t_a48e52d1","t_a4b6791b",
"t_c8784acc","t_cb601d70","t_d4fca8b3","t_e04bca14","t_efb6071f","t_f9ac1ff2"]

now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# sanity papan hidup: MAX(created_at) events
r = con.execute("SELECT MAX(created_at) m, COUNT(*) c FROM task_events").fetchone()
print(f"SANITY events: total={r['c']} umur_event_terakhir_menit={(now - r['m'])/60:.1f}")

def cols(table):
    return [x[1] for x in con.execute(f"PRAGMA table_info({table})")]
print("tasks cols:", cols("tasks"))
print("task_links cols:", cols("task_links"))

for tid in IDS:
    t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(f"== {tid} TIDAK DITEMUKAN"); continue
    d = dict(t)
    evs = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)).fetchall()
    last_ev = f"{evs[0]['kind']}@{(now-evs[0]['created_at'])/60:.0f}m" if evs else "tanpa-event"
    par = con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()
    parinfo = []
    for p in par:
        pt = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
        if pt: parinfo.append(f"{pt['id']}:{pt['status']}")
    ncom = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (tid,)).fetchone()["c"]
    lap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (tid,)).fetchone()["c"]
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    mark = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["c"]
    print(f"== {tid} status={d.get('status')} tenant={d.get('tenant')} assignee={d.get('assignee')} author={d.get('created_by')} lastev={last_ev} parents=[{','.join(parinfo)}] com={ncom} lap={lap} ack={ack} mark={mark}")
    print(f"   title: {(d.get('title') or '')[:110]}")
    if d.get('status') == 'blocked':
        print(f"   reason/note: {(str(d.get('blocked_reason') or d.get('note') or ''))[:200]}")

# sensus per tenant yang muncul
tenants = set()
for tid in IDS:
    t = con.execute("SELECT tenant FROM tasks WHERE id=?", (tid,)).fetchone()
    if t and t["tenant"]: tenants.add(t["tenant"])
print("\n=== SENSUS TENANT ===")
for tn in sorted(tenants):
    rows = con.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant=? GROUP BY status", (tn,)).fetchall()
    dist = {r["status"]: r["c"] for r in rows}
    tot = sum(dist.values())
    ev = con.execute("SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=?", (tn,)).fetchone()["m"]
    gave = con.execute("SELECT COUNT(*) c FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind IN ('timed_out','gave_up')", (tn,)).fetchone()["c"]
    print(f"tenant {tn}: total={tot} dist={dist} umur_event_terakhir={(now-ev)/60:.0f}mnt gave_up/timed_out={gave}")

con.close()
