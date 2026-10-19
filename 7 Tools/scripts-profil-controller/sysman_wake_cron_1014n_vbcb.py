# Sysman cron: census mendalam tenant VIBE-BIBLE-1013 (misi beku) - ronde siang 14-10.
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
TEN = "VIBE-BIBLE-1013"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def q(sql, *a):
    return con.execute(sql, a).fetchall()

# 1. sensus status penuh tenant (bukan hanya yang WAKE)
print("=== SENSUS STATUS TENANT ===")
for r in q("SELECT status, COUNT(*) n FROM tasks WHERE tenant=? GROUP BY status ORDER BY n DESC", TEN):
    print(f"  {r['status']}: {r['n']}")
tot = q("SELECT COUNT(*) n FROM tasks WHERE tenant=?", TEN)[0]["n"]
print("  total kartu tenant:", tot)

# 2. event kind per kartu blocked (timed_out / gave_up)
print("\n=== EVENT KIND pada kartu tenant (24h terakhir) ===")
for r in q("""SELECT e.kind, COUNT(DISTINCT e.task_id) cards, COUNT(*) evs, MAX(e.created_at) mx
              FROM task_events e JOIN tasks t ON t.id=e.task_id
              WHERE t.tenant=? AND e.created_at > ?
              GROUP BY e.kind ORDER BY evs DESC""", TEN, now-86400):
    print(f"  {r['kind']}: {r['cards']} cards, {r['evs']} evs, terakhir {round((now-r['mx'])/60)} mnt lalu")

# 3. kartu done tenant: ACK + marker
print("\n=== KARTU DONE TENANT: ACK & marker ===")
donen = 0
for r in q("SELECT id, title, completed_at FROM tasks WHERE tenant=? AND status='done' ORDER BY completed_at", TEN):
    donen += 1
    ack = q("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", r["id"])[0]["n"]
    mk  = q("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", r["id"])[0]["n"]
    lap = q("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", r["id"])[0]["n"]
    print(f"  {r['id']} ack={ack} marker={mk} lapor={lap} done {round((now-(r['completed_at'] or now))/60)} mnt lalu | {r['title'][:70]}")
print("  total done:", donen)

# 4. komentar CHECKPOINT dari worker (rem yang ditawarkan)
print("\n=== KOMENTAR CHECKPOINT/CHECKPOINT-RESUME (tenant) ===")
cps = q("""SELECT c.task_id, c.author, substr(c.body,1,300) b, c.created_at
           FROM task_comments c JOIN tasks t ON t.id=c.task_id
           WHERE t.tenant=? AND c.body LIKE '%CHECKPOINT%'
           ORDER BY c.created_at DESC LIMIT 5""", TEN)
for r in cps:
    print(f"  [{round((now-r['created_at'])/60)} mnt] {r['task_id']} by {r['author']}: {r['b'][:220]}")
if not cps: print("  (tidak ada)")

# 5. triase controller terakhir untuk tenant ini (komentar author default/controller > 12h)
print("\n=== TRIASE TERAKHIR (komentar author controller-ish, 48h) ===")
tri = q("""SELECT c.task_id, c.author, substr(c.body,1,200) b, c.created_at
           FROM task_comments c JOIN tasks t ON t.id=c.task_id
           WHERE t.tenant=? AND c.author IN ('default','sysmanager-cleaner','mission-wake','gsp-master','user')
           ORDER BY c.created_at DESC LIMIT 8""", TEN)
for r in tri:
    print(f"  [{round((now-r['created_at'])/60)} mnt] {r['task_id']} by {r['author']}: {r['b'][:160]}")
if not tri: print("  (tidak ada)")

# 6. umur event terakhir per kartu terbuka (flat = beku)
print("\n=== UMUR EVENT TERAKHIR kartu terbuka tenant ===")
ages = []
for r in q("SELECT id FROM tasks WHERE tenant=? AND status IN ('blocked','todo')", TEN):
    mx = q("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", r["id"])[0]["mx"]
    if mx: ages.append((now-mx)/60)
ages.sort()
if ages:
    print(f"  n={len(ages)} min={round(ages[0])} med={round(ages[len(ages)//2])} max={round(ages[-1])} menit")

# 7. aktivitas papan di luar tenant (bukti fleet lain jalan)
print("\n=== AKTIVITAS LUAR-TENAN (event 6h, top tenants) ===")
for r in q("""SELECT COALESCE(NULLIF(t.tenant,''),'(null)') ten, COUNT(*) evs, MAX(e.created_at) mx
              FROM task_events e LEFT JOIN tasks t ON t.id=e.task_id
              WHERE e.created_at > ? AND (t.tenant IS NULL OR t.tenant != ?)
              GROUP BY ten ORDER BY mx DESC LIMIT 8""", now-21600, TEN):
    print(f"  {r['ten']}: {r['evs']} evs, terakhir {round((now-r['mx'])/60)} mnt lalu")
