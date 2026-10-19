# Read-only: open-card census per tenant + ACK census for recent done tenants
# (anti tamat-senyap tingkat misi; pola dari skill gsp-system-manager-ops)
import sqlite3, time, os, re

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
cur = con.cursor()
now = time.time()

print("-- open cards (status not done/archived) --")
rows = cur.execute(
    "SELECT id,title,status,tenant,created_by,created_at FROM tasks "
    "WHERE status NOT IN ('done','archived') ORDER BY tenant, created_at"
).fetchall()
for tid, title, status, tenant, cb, ca in rows:
    age_h = (now - ca) / 3600.0
    print(f"{tid} [{status}] tenant={tenant} by={cb} age={age_h:.1f}h | {title[:60]}")
print(f"total_open={len(rows)}")

# tenants of done cards finished in last 24h
print("-- done-in-24h tenants: per-card ACK-lain-author census --")
dones = cur.execute(
    "SELECT id,title,tenant,completed_at FROM tasks "
    "WHERE status='done' AND completed_at >= ? ORDER BY tenant, completed_at",
    (now - 24 * 3600,),
).fetchall()

def lap_author(tid):
    r = cur.execute(
        "SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' "
        "ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    return r[0] if r else None

def ack_lain(tid):
    la = lap_author(tid)
    q = cur.execute(
        "SELECT author, COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' GROUP BY author",
        (tid,)).fetchall()
    return sum(n for a, n in q if a != la), [a for a, n in q]

by_tenant = {}
for tid, title, tenant, cat in dones:
    by_tenant.setdefault(tenant, []).append((tid, title, cat))

for tenant, items in sorted(by_tenant.items(), key=lambda kv: str(kv[0])):
    open_cnt = sum(1 for r in rows if r[3] == tenant)
    print(f"== tenant={tenant} done24h={len(items)} open_now={open_cnt}")
    for tid, title, cat in items:
        n, authors = ack_lain(tid)
        flag = "ZERO-ACK-LAIN" if n == 0 else ""
        age_h = (now - cat) / 3600.0
        print(f"   {tid} ack_lain={n} {authors} done_age={age_h:.1f}h {flag} | {title[:50]}")
con.close()
