# Round 3: JEDA-GELOMBONG watcher liveness — block/unblock history + queue trend.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def d(sql, args=()):
    cur = con.cursor()
    cur.execute(sql, args)
    return cur.fetchall()

TEN = "VIBE-BIBLE-1013"

# 1. All JEDA-GELOMBONG blocked events across board (any era) + current status of those cards
rows = d("""SELECT e.task_id, e.created_at, t.status FROM task_events e
            JOIN tasks t ON t.id=e.task_id
            WHERE e.kind='blocked' AND e.payload LIKE '%JEDA-GELOMBONG%'
            ORDER BY e.created_at""")
print("JEDA blocks total:", len(rows))
by_status = {}
for r in rows:
    by_status.setdefault(r["status"], []).append(round((now - r["created_at"])/60))
for s, ages in by_status.items():
    print(f"  cards now {s}: {len(ages)} (block-age min: {min(ages)}..{max(ages)})")

# 2. Unblocks in tenant (any reason) — did any JEDA card ever get released?
ub = d("""SELECT e.task_id, e.created_at, t.status FROM task_events e
          JOIN tasks t ON t.id=e.task_id
          WHERE t.tenant=? AND e.kind='unblocked' ORDER BY e.created_at""", (TEN,))
print("\nunblocked events:", [(r["task_id"], round((now-r["created_at"])/60), r["status"]) for r in ub])

# 3. Comments mentioning watcher/jeda across tenant (who operates the watcher)
cm = d("""SELECT c.task_id, c.author, substr(c.body,1,200) b, c.created_at FROM task_comments c
          JOIN tasks t ON t.id=c.task_id
          WHERE t.tenant=? AND (c.body LIKE '%watcher%' OR c.body LIKE '%WATCHER%' OR c.body LIKE '%JEDA%')
          ORDER BY c.created_at DESC LIMIT 12""", (TEN,))
print("\nwatcher/jeda comments:")
for r in cm:
    print(f"  [{round((now-r['created_at'])/60)}m] {r['author']} @{r['task_id']}: {r['b'][:180]}")

# 4. Mission-level: oldest open event age per status group + last activity overall
la = d("""SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=?""", (TEN,))
print("\nlast tenant event min:", round((now-la[0]["m"])/60))

# 5. t_4edfcf3a (penulis bab1) runs detail — 3rd run age vs cap
rr = d("SELECT id, outcome, started_at, ended_at, max_runtime_seconds FROM task_runs WHERE task_id='t_4edfcf3a' ORDER BY started_at")
for r in rr:
    st = round((now-r["started_at"])/60)
    en = round((now-r["ended_at"])/60) if r["ended_at"] else None
    print(f"run#{r['id']} outcome={r['outcome']} started{st}m ago ended={en}m ago cap={r['max_runtime_seconds']}")

# 6. M4 running cards: max_runtime cap + elapsed (risk of another timeout storm)
rr2 = d("""SELECT ru.task_id, ru.max_runtime_seconds mrs, ru.started_at FROM task_runs ru
           JOIN tasks t ON t.id=ru.task_id
           WHERE t.tenant=? AND t.status='running' AND ru.ended_at IS NULL""", (TEN,))
for r in rr2:
    el = round((now-r["started_at"])/60)
    cap = (r["mrs"] or 0)/60
    print(f"live-run {r['task_id']} elapsed {el}m / cap {cap:.0f}m")
