# Blind-spot sweep: 34 running parents (heartbeat age, LAPOR vs ACK), 10 blocked cards, done-unacked candidates.
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = time.time()

def age(ts):
    return int((now - ts) / 60) if ts else None

CHILDREN = """t_002af121 t_0311d1e4 t_0bf0854c t_1168e59f t_14e7030f t_153594d4 t_1c98456a
t_23f7da05 t_2e0e92d4 t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_5831a79d t_60ed37fa
t_7391c81b t_77a9bcd3 t_799a1879 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a48e52d1 t_a4b6791b t_c8784acc t_cb601d70 t_d4fca8b3 t_e04bca14
t_edb280b5 t_efb6071f t_f9ac1ff2""".split()

parents = set()
for c in CHILDREN:
    for p in cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (c,)):
        parents.add(p["parent_id"])
print("PARENT_COUNT", len(parents))

print("---- RUNNING PARENTS ----")
for pid in sorted(parents):
    r = cur.execute("SELECT * FROM tasks WHERE id=?", (pid,)).fetchone()
    if not r:
        print(pid, "NOT-FOUND"); continue
    hb = r["last_heartbeat_at"]
    started = r["started_at"]
    maxrt = r["max_runtime_seconds"]
    nlap = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (pid,)).fetchone()[0]
    nack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (pid,)).fetchone()[0]
    lastev = cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    print(f"{pid} | {r['status']} | assignee={r['assignee']} | started={age(started)}m hb={age(hb)}m "
          f"maxrt={maxrt} | LAPOR={nlap} ACK={nack} | lastev={(lastev['kind'], age(lastev['created_at'])) if lastev else None} "
          f"| {r['title'][:55]}")

# Any running card NOT a parent of our children? (other missions)
other_run = [r for r in cur.execute("SELECT id,title,status,last_heartbeat_at,started_at,assignee FROM tasks WHERE status='running'")]
nonpar = [r for r in other_run if r["id"] not in parents]
print("RUNNING_NOT_IN_PARENT_SET", len(nonpar))
for r in nonpar:
    nlap = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()[0]
    nack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    print(f"  {r['id']} | hb={age(r['last_heartbeat_at'])}m started={age(r['started_at'])}m LAPOR={nlap} ACK={nack} | {r['title'][:60]}")

print("---- BLOCKED CARDS ----")
for r in cur.execute("SELECT id,title,status,tenant,assignee,created_at,block_kind FROM tasks WHERE status='blocked'"):
    lastev = cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    nlap = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()[0]
    nack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    ntri = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%[FASE]%' OR body LIKE '%TRIASE%' OR body LIKE '%DITAHAN%')", (r["id"],)).fetchone()[0]
    print(f"{r['id']} | tenant={r['tenant']} | created={age(r['created_at'])}m lastev={(lastev['kind'], age(lastev['created_at'])) if lastev else None} LAPOR={nlap} ACK={nack} FASE/TRIASE={ntri} | {r['title'][:60]}")

print("---- DONE-LAST-6H WITHOUT ANY ACK (route-4b loose check) ----")
cut = now - 6*3600
for r in cur.execute("SELECT id,title,tenant,completed_at,created_by FROM tasks WHERE status='done' AND completed_at>=? ORDER BY completed_at DESC LIMIT 40", (cut,)):
    nack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    nlap = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()[0]
    nmark = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()[0]
    if nack == 0:
        print(f"{r['id']} | tenant={r['tenant']} | done_age={age(r['completed_at'])}m by={r['created_by']} LAPOR={nlap} MARKER={nmark} | {r['title'][:60]}")

print("---- VIBE-BIBLE-1013 TENANT CENSUS ----")
tot = {}
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    tot[r["status"]] = r["n"]
print("TENANT_STATUS", tot)
