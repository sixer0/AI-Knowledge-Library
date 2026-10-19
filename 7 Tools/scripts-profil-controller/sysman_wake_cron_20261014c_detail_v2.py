# Detail bukti untuk butir tingkat-misi VIBE-BIBLE-1013 - cron 2026-10-14c.
import sqlite3, time, collections, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts):
    return None if ts is None else round((now - ts) / 60)

print("=== WRITER CARD FIELDS (blocked, tenant VBCB) ===")
w = con.execute("""SELECT id,title,status,block_kind,block_recurrences,consecutive_failures,
 max_runtime_seconds,max_retries,last_heartbeat_at,started_at,completed_at,current_run_id,worker_pid,last_failure_error
 FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' ORDER BY title""").fetchall()
print(f"n_blocked_writers={len(w)}")
print("max_runtime set:", dict(collections.Counter(r['max_runtime_seconds'] for r in w)))
print("max_retries set:", dict(collections.Counter(r['max_retries'] for r in w)))
print("block_kind:", dict(collections.Counter(r['block_kind'] for r in w)))
print("consec_fail:", dict(collections.Counter(r['consecutive_failures'] for r in w)))
hb = [age(r['last_heartbeat_at']) for r in w if r['last_heartbeat_at']]
print(f"heartbeat age min..max = {min(hb)}..{max(hb)}")
lf = collections.Counter((r['last_failure_error'] or '')[:60] for r in w)
for k, v in lf.items():
    print(f"  last_failure_error x{v}: {k!r}")

print("\n=== RUN HISTORY sample (3 cards) ===")
for tid in ('t_050a75ff', 't_a783103d', 't_d3cc135a'):
    rs = con.execute("""SELECT id,profile,status,started_at,ended_at,outcome,max_runtime_seconds,
     substr(COALESCE(summary,''),1,100) s, substr(COALESCE(error,''),1,100) e FROM task_runs WHERE task_id=? ORDER BY started_at""", (tid,)).fetchall()
    print(f"-- {tid}: runs={len(rs)}")
    for r in rs:
        print(f"   run {r['id']} {r['profile']} {r['status']} out={r['outcome']} cap={r['max_runtime_seconds']} "
              f"start={age(r['started_at'])}m end={age(r['ended_at'])}m sum={r['s']!r} err={r['e']!r}")

print("\n=== FULL TEXT: latest CHECKPOINT/LAPOR per writer offering remedy (top 6 by length) ===")
cs = con.execute("""SELECT c.task_id, c.author, c.body, c.created_at, t.title FROM task_comments c
 JOIN tasks t ON t.id=c.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND (c.body LIKE '%CHECKPOINT%' OR c.body LIKE '%LAPOR%')
 ORDER BY c.created_at DESC""").fetchall()
seen = set()
shown = 0
for c in cs:
    if c['task_id'] in seen:
        continue
    seen.add(c['task_id'])
    if shown >= 4:
        break
    print(f"--- {c['task_id']} ({c['title'][:40]}) {c['author']} @{age(c['created_at'])}m")
    print(c['body'][:1400])
    print()
    shown += 1

print("\n=== WAVE census (title prefix) among open cards ===")
op = con.execute("SELECT id,title,status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status IN ('todo','blocked')").fetchall()
cnt = collections.Counter()
for r in op:
    wave = r['title'].split(']')[0].replace('[', '') if '[' in r['title'] else '?'
    kind = 'Penulis' if 'Penulis' in r['title'] else ('Verifikasi' if 'Verifikasi' in r['title'] else 'lain')
    cnt[(wave, kind, r['status'])] += 1
for k, v in sorted(cnt.items()):
    print(f"  {k} -> {v}")
print(f"open_total={len(op)}")

print("\n=== Any controller-ish author comment anywhere in tenant? ===")
ca = con.execute("""SELECT c.author, COUNT(*) n FROM task_comments c JOIN tasks t ON t.id=c.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' GROUP BY c.author""").fetchall()
for r in ca:
    print(f"  {r['author']} x{r['n']}")

print("\n=== Anchor/blueprint cards (tenant NULL) referencing VIBE/VBCB ===")
an = con.execute("""SELECT id,title,status,tenant,created_at FROM tasks
 WHERE (title LIKE '%VIBE%' OR title LIKE '%VBCB%' OR body LIKE '%VIBE-BIBLE-1013%')
   AND (tenant IS NULL OR tenant='') ORDER BY created_at DESC LIMIT 12""").fetchall()
for r in an:
    print(f"  {r['id']} st={r['status']} @{age(r['created_at'])}m :: {r['title'][:80]}")
