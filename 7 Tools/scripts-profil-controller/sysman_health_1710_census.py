# Read-only census: blocked cards + 24h run outcomes (kanban.db root)
import sqlite3, time, json
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())

print("== SENSUS STATUS (non-archived) ==")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks WHERE status!='archived' GROUP BY status ORDER BY n DESC"):
    print(f"  {r['status']}: {r['n']}")

print("== KARTU BLOCKED: umur event terakhir + rem koreksi ==")
rows = con.execute("""
  SELECT t.id, t.title, t.assignee, t.tenant, t.block_kind, t.created_at,
         (SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id) last_ev,
         (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%[SYSMAN-CLEANER%') fixmark,
         (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%Digantikan%') replmark,
         (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-WAKE%') wakemark
  FROM tasks t WHERE t.status='blocked'
""").fetchall()
tot = len(rows)
withfix = sum(1 for r in rows if r['fixmark'] or r['replmark'])
fresh = [r for r in rows if r['last_ev'] and (now - r['last_ev']) < 6*3600]
print(f"  total blocked={tot} | sudah ber-rem koreksi/pengganti={withfix} | event <=6j terakhir={len(fresh)}")
from collections import Counter
tc = Counter((r['tenant'] or '-') for r in rows)
print("  per tenant:", dict(tc.most_common(10)))
bk = Counter(str(r['block_kind']) for r in rows)
print("  per block_kind:", dict(bk))
ages = sorted(((now - r['last_ev'])//60) for r in rows if r['last_ev'])
if ages:
    print(f"  umur event terakhir (menit): min={ages[0]} med={ages[len(ages)//2]} max={ages[-1]}")
print("  == 8 kartu blocked TANPA rem koreksi, event paling basi ==")
unfixed = [r for r in rows if not r['fixmark'] and not r['replmark']]
unfixed.sort(key=lambda r: r['last_ev'] or 0)
for r in unfixed[:8]:
    ageh = (now - (r['last_ev'] or r['created_at']))/3600
    print(f"  {r['id']} [{r['tenant'] or '-'}] {str(r['title'])[:58]} ev={ageh:.0f}h kind={r['block_kind']} wake={r['wakemark']}")
print(f"  (total tanpa rem: {len(unfixed)})")

print("== RUN 24 JAM: outcome ==")
for r in con.execute("""
  SELECT outcome, COUNT(*) n FROM task_runs
  WHERE started_at >= ? GROUP BY outcome ORDER BY n DESC
""", (now - 86400,)):
    print(f"  {r['outcome']}: {r['n']}")
print("== RUN blocked 24j: kartu mana saja ==")
for r in con.execute("""
  SELECT r.task_id, t.tenant, SUBSTR(t.title,1,50) title, r.started_at
  FROM task_runs r JOIN tasks t ON t.id=r.task_id
  WHERE r.started_at >= ? AND r.outcome='blocked' ORDER BY r.started_at DESC
""", (now - 86400,)):
    print(f"  {r['task_id']} [{r['tenant'] or '-'}] {r['title']} mulai {(now-r['started_at'])/3600:.1f}j lalu")

print("== KARTU RUNNING/TODO (blind-spot check) ==")
for r in con.execute("SELECT id, status, assignee, tenant, SUBSTR(title,1,50) title FROM tasks WHERE status IN ('running','todo','in_progress') AND status!='archived' LIMIT 15"):
    print(f"  {r['id']} {r['status']} [{r['assignee']}] [{r['tenant'] or '-'}] {r['title']}")
n_rt = con.execute("SELECT COUNT(*) FROM tasks WHERE status IN ('running','todo','in_progress')").fetchone()[0]
print(f"  total running/todo/in_progress = {n_rt}")
print("== SANITY papan hidup ==")
mx = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
print(f"  event terbaru berumur {(now-mx)/60:.1f} menit; total tasks={con.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]}")
