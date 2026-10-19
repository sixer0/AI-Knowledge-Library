# Read-only eval of WAKE t_edb280b5 (stalled) + tenant census VIBE-BIBLE-1013
import sqlite3, time, json, os

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

def age(ts):
    return round((NOW - ts) / 60.0, 1) if ts else None

print("== NOW epoch:", NOW)

# 1) Parent chain of t_edb280b5
pid = "t_4edfcf3a"
row = cur.execute("SELECT id,title,status,assignee,created_at,started_at,completed_at,tenant FROM tasks WHERE id=?", (pid,)).fetchone()
if row:
    d = dict(row)
    d["age_started_min"] = age(d["started_at"])
    d["age_completed_min"] = age(d["completed_at"])
    le = cur.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (pid,)).fetchall()
    d["last_events"] = [(r["kind"], age(r["created_at"])) for r in le]
    cmts = cur.execute("SELECT author,substr(body,1,120) b,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (pid,)).fetchall()
    d["last_comments"] = [(r["author"], r["b"][:100], age(r["created_at"])) for r in cmts]
    print("== PARENT:", json.dumps(d, ensure_ascii=False, indent=1))
else:
    print("== PARENT MISSING:", pid)

# grandparents if any
gp = cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (pid,)).fetchall()
for g in gp:
    gpid = g["parent_id"]
    grow = cur.execute("SELECT id,title,status,assignee FROM tasks WHERE id=?", (gpid,)).fetchone()
    print("== GRANDPARENT:", dict(grow) if grow else gpid)

# 2) Sibling set: children of same parent
sibs = cur.execute("""
  SELECT t.id,t.status,t.title FROM task_links l JOIN tasks t ON t.id=l.child_id
  WHERE l.parent_id=? ORDER BY t.created_at""", (pid,)).fetchall()
print("== SIBLINGS of parent (%d):" % len(sibs))
for s in sibs:
    print("   ", s["id"], s["status"], s["title"][:60])

# 3) Tenant census
ten = "VIBE-BIBLE-1013"
cen = cur.execute("SELECT status,COUNT(*) n FROM tasks WHERE tenant=? GROUP BY status", (ten,)).fetchall()
print("== TENANT CENSUS:", {r["status"]: r["n"] for r in cen})

# 4) Last event age per card (freeze check)
le = cur.execute("""
  SELECT t.id, MAX(e.created_at) mx, t.status FROM tasks t
  JOIN task_events e ON e.task_id=t.id
  WHERE t.tenant=? GROUP BY t.id""", (ten,)).fetchall()
ages = sorted([age(r["mx"]) for r in le])
if ages:
    print("== LAST-EVENT AGE MIN/MAX (min):", ages[0], "..", ages[-1], "n=", len(ages))

# 5) Terminal failure kinds across tenant
kinds = cur.execute("""
  SELECT e.kind, COUNT(*) n, MAX(e.created_at) mx FROM task_events e
  JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind IN ('timed_out','gave_up','run_failed','promoted','claimed','parked')
  GROUP BY e.kind""", (ten,)).fetchall()
print("== EVENT KINDS:", [(r["kind"], r["n"], age(r["mx"])) for r in kinds])

# 6) Running cards blind spot: LAPOR vs ACK
run = cur.execute("SELECT id,title FROM tasks WHERE tenant=? AND status IN ('running','in_progress')", (ten,)).fetchall()
print("== RUNNING CARDS:", len(run))
for r in run:
    lap = cur.execute("SELECT COUNT(*) c, MAX(created_at) mx FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()
    ack = cur.execute("SELECT COUNT(*) c, MAX(created_at) mx FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()
    hb = cur.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()
    print("   ", r["id"], r["title"][:50], "| lapor=", lap["c"], "ack=", ack["c"], "| last_event_age=", age(hb["mx"]))

# 7) Done cards without any ACK (silent handover census)
done = cur.execute("SELECT id,title,completed_at FROM tasks WHERE tenant=? AND status='done'", (ten,)).fetchall()
noack = []
for r in done:
    ack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    mk = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["c"]
    if ack == 0:
        noack.append((r["id"], r["title"][:50], age(r["completed_at"]), mk))
print("== DONE total=%d, done-no-ACK=%d" % (len(done), len(noack)))
for n in noack[:40]:
    print("   ", n)

# 8) Board liveness (MAX not MIN!)
ml = cur.execute("SELECT MAX(created_at) mx FROM task_events").fetchone()["mx"]
print("== BOARD LIVENESS last event age(min):", age(ml))
con.close()
