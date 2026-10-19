# Read-only deep-dive VIBE-BIBLE-1013 for cron round 15-10 (sysman)
import sqlite3, time
from collections import Counter

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
TEN = "VIBE-BIBLE-1013"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def age(ts): return "%.0fm" % ((now-ts)/60) if ts else "-"

# 1) blocked cards in tenant: distinct reasons + age of block event
print("=== BLOCKED CARDS (tenant) reasons ===")
rows = con.execute("SELECT id,title FROM tasks WHERE tenant=? AND status='blocked'", (TEN,)).fetchall()
reasons = Counter()
for r in rows:
    ev = con.execute("SELECT json_extract(payload,'$.reason') rs FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    rs = ((ev["rs"] if ev and ev["rs"] else None) or "(no reason)")[:90]
    reasons[rs] += 1
for rs, c in reasons.most_common():
    print(f"  x{c}: {rs}")
bevs = con.execute("SELECT MAX(e.created_at) mc FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind='blocked'", (TEN,)).fetchone()["mc"]
print("newest 'blocked' event:", age(bevs))

# 2) unblocked events (watcher releases)
ub = con.execute("SELECT COUNT(*) c, MAX(e.created_at) mc FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind='unblocked'", (TEN,)).fetchone()
print(f"unblocked events: count={ub['c']} newest={age(ub['mc'])}")

# 3) gave_up / timed_out timeline
print("\n=== TIMEOUT/GAVE_UP timeline (last 12h) ===")
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

# 5) running card t_deb670d0 full comments + events
print("\n=== RUNNING CARD t_deb670d0 ===")
for c in con.execute("SELECT author, created_at, substr(body,1,400) b FROM task_comments WHERE task_id='t_deb670d0' ORDER BY created_at"):
    print(f"  [{age(c['created_at'])} ago] {c['author']}: {c['b'][:350].replace(chr(10),' | ')}")
print("  events:")
for e in con.execute("SELECT kind, created_at FROM task_events WHERE task_id='t_deb670d0' ORDER BY created_at DESC LIMIT 12"):
    print(f"    {e['kind']} @{age(e['created_at'])} ago")

# 6) activity map last 6h by card status
print("\n=== ACTIVITY last 6h (tenant) ===")
act = con.execute("""SELECT t.status, COUNT(DISTINCT t.id) c FROM task_events e JOIN tasks t ON t.id=e.task_id
WHERE t.tenant=? AND e.created_at >= ?-6*3600 GROUP BY t.status""", (TEN, now)).fetchall()
for r in act: print(f"  {r['status']}: {r['c']} cards touched")

# 7) current runs status
print("\n=== task_runs recent (tenant cards) ===")
runs = con.execute("""SELECT tr.task_id, tr.status, tr.outcome, tr.started_at, tr.ended_at
FROM task_runs tr JOIN tasks t ON t.id=tr.task_id
WHERE t.tenant=? ORDER BY tr.started_at DESC LIMIT 8""", (TEN,)).fetchall()
for r in runs:
    print(f"  {r['task_id']} {r['status']}/{r['outcome']} start={age(r['started_at'])} ago fin={age(r['ended_at'])} ago")

# 8) any [FASE] comments in tenant last 24h
print("\n=== [FASE] comments last 24h (tenant) ===")
fsh = con.execute("""SELECT t.id, tc.author, tc.created_at, substr(tc.body,1,120) b FROM task_comments tc
JOIN tasks t ON t.id=tc.task_id
WHERE t.tenant=? AND tc.body LIKE '%[FASE]%' AND tc.created_at >= ?-24*3600 ORDER BY tc.created_at DESC LIMIT 10""", (TEN, now)).fetchall()
print("count shown:", len(fsh))
for r in fsh: print(f"  {r['id']} [{age(r['created_at'])}] {r['author']}: {r['b'][:100]}")
