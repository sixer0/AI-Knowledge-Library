# Read-only deep-dive VIBE-BIBLE-1013 v2 (sysman cron 15-10)
import sqlite3, time, json
from collections import Counter

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
TEN = "VIBE-BIBLE-1013"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def age(ts): return "%.0fm" % ((now-ts)/60) if ts else "-"

# 1) blocked cards: reason from latest 'blocked' event payload + last comment
print("=== BLOCKED CARDS reasons ===")
rows = con.execute("SELECT id,title FROM tasks WHERE tenant=? AND status='blocked' ORDER BY id", (TEN,)).fetchall()
reasons = Counter()
for r in rows:
    ev = con.execute("SELECT payload, created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    rs = "(no blocked event)"
    when = "-"
    if ev:
        when = age(ev["created_at"])
        try:
            p = json.loads(ev["payload"] or "{}")
            rs = str(p.get("reason") or p.get("message") or ev["payload"])[:110]
        except Exception:
            rs = str(ev["payload"])[:110]
    reasons[rs] += 1
    print(f"  {r['id']} blocked@{when} ago :: {rs} :: {str(r['title'])[:45]}")
for rs, c in reasons.most_common(5):
    print(f"  REASON x{c}: {rs}")

# 2) unblocked events (watcher releases)?
ub = con.execute("SELECT COUNT(*) c, MAX(e.created_at) mc FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind='unblocked'", (TEN,)).fetchone()
print(f"\nunblocked events: count={ub['c']} newest={age(ub['mc'])}")

# 3) gave_up / timed_out timeline
print("\n=== TIMEOUT/GAVE_UP timeline ===")
tl = con.execute("""SELECT e.kind, COUNT(*) c, MIN(e.created_at) first, MAX(e.created_at) last
FROM task_events e JOIN tasks t ON t.id=e.task_id
WHERE t.tenant=? AND e.kind IN ('timed_out','gave_up') GROUP BY e.kind""", (TEN,)).fetchall()
for r in tl:
    print(f"  {r['kind']}: n={r['c']} first={age(r['first'])} ago, last={age(r['last'])} ago")

# 4) done cards ACK census + markers
print("\n=== DONE CARDS ACK CENSUS ===")
dones = con.execute("SELECT id,title,completed_at FROM tasks WHERE tenant=? AND status='done'", (TEN,)).fetchall()
noack = []
for d in dones:
    nack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (d["id"],)).fetchone()["c"]
    nmark = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (d["id"],)).fetchone()["c"]
    if nack == 0:
        noack.append((d["id"], nmark, str(d["title"])[:55], age(d["completed_at"])))
print(f"done total={len(dones)} ack0={len(noack)}")
for x in noack:
    print(f"  {x[0]} mark={x[1]} done@{x[3]} ago :: {x[2]}")

# 5) running card t_deb670d0 comments + events + run info
print("\n=== RUNNING CARD t_deb670d0 ===")
t = con.execute("SELECT * FROM tasks WHERE id='t_deb670d0'").fetchone()
print(f"  status={t['status']} hb={age(t['last_heartbeat_at'])} maxrun={t['max_runtime_seconds']} started={age(t['started_at'])} consec_fail={t['consecutive_failures']}")
for c in con.execute("SELECT author, created_at, substr(body,1,400) b FROM task_comments WHERE task_id='t_deb670d0' ORDER BY created_at"):
    print(f"  [{age(c['created_at'])} ago] {c['author']}: {c['b'][:350].replace(chr(10),' | ')}")
for e in con.execute("SELECT kind, created_at FROM task_events WHERE task_id='t_deb670d0' ORDER BY created_at DESC LIMIT 12"):
    print(f"    ev {e['kind']} @{age(e['created_at'])} ago")
for r in con.execute("SELECT id,status,outcome,started_at,ended_at,max_runtime_seconds,last_heartbeat_at FROM task_runs WHERE task_id='t_deb670d0' ORDER BY started_at DESC LIMIT 5"):
    print(f"    run {r['id']} {r['status']}/{r['outcome']} start={age(r['started_at'])} end={age(r['ended_at'])} cap={r['max_runtime_seconds']} hb={age(r['last_heartbeat_at'])}")

# 6) activity map last 6h by card status
print("\n=== ACTIVITY last 6h (tenant cards touched) ===")
act = con.execute("""SELECT t.status, COUNT(DISTINCT t.id) c FROM task_events e JOIN tasks t ON t.id=e.task_id
WHERE t.tenant=? AND e.created_at >= ?-6*3600 GROUP BY t.status""", (TEN, now)).fetchall()
for r in act: print(f"  {r['status']}: {r['c']} cards touched")

# 7) [FASE] comments in tenant last 24h
print("\n=== [FASE] comments last 24h ===")
fsh = con.execute("""SELECT t.id, tc.author, tc.created_at, substr(tc.body,1,110) b FROM task_comments tc
JOIN tasks t ON t.id=tc.task_id
WHERE t.tenant=? AND tc.body LIKE '%[FASE]%' AND tc.created_at >= ?-24*3600 ORDER BY tc.created_at DESC LIMIT 8""", (TEN, now)).fetchall()
print("shown:", len(fsh))
for r in fsh: print(f"  {r['id']} [{age(r['created_at'])}] {r['author']}: {r['b'][:95]}")

# 8) checkpoint comments from workers (remedy candidates)
print("\n=== CHECKPOINT comments (tenant, recent) ===")
cps = con.execute("""SELECT t.id, tc.author, tc.created_at, substr(tc.body,1,160) b FROM task_comments tc
JOIN tasks t ON t.id=tc.task_id
WHERE t.tenant=? AND tc.body LIKE '%CHECKPOINT%' ORDER BY tc.created_at DESC LIMIT 6""", (TEN,)).fetchall()
for r in cps: print(f"  {r['id']} [{age(r['created_at'])}] {r['author']}: {r['b'][:140]}")
