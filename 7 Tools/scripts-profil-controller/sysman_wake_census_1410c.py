# Tenant census + status census for WAKE storm triage (read-only, 14-10 round c).
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
cur = con.cursor()

print("== STATUS CENSUS (all tasks) ==")
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  {r['status']:12} {r['n']}")

print("\n== TENANT CENSUS (non-null tenants) ==")
for r in cur.execute("SELECT tenant, COUNT(*) n, SUM(status IN ('done','cancelled')) dn, MIN(created_at) c0, MAX(created_at) c1 FROM tasks WHERE tenant IS NOT NULL AND tenant != '' GROUP BY tenant ORDER BY n DESC LIMIT 40"):
    print(f"  {r['tenant']:28} n={r['n']:3} done={r['dn']:3} first_h={(now-r['c0'])/3600:.0f} last_h={(now-r['c1'])/3600:.0f}")

print("\n== OPEN TASKS PER TENANT (status not done/cancelled) ==")
for r in cur.execute("SELECT tenant, status, COUNT(*) n FROM tasks WHERE status NOT IN ('done','cancelled') GROUP BY tenant, status ORDER BY tenant"):
    print(f"  {str(r['tenant']):28} {r['status']:10} {r['n']}")

print("\n== WAKE IDS: tenant + title prefix grouping ==")
ids = "t_002af121 t_0311d1e4 t_050a75ff t_0bf0854c t_0df60358 t_1168e59f t_14e7030f t_153594d4 t_1c98456a t_23f7da05 t_2543fb8f t_2ae211bb t_2d32e7c8 t_2e0e92d4 t_30dd071c t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_483b2d91 t_4d7a1691 t_4edfcf3a t_5831a79d t_60ed37fa t_64328060 t_674377e1 t_68d1d8be t_7391c81b t_760e7792 t_77a9bcd3 t_799a1879 t_8b90e854 t_8d618268 t_93c6bec3 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc t_a064e4cc t_a37d190b t_a3e70bf1 t_a48e52d1 t_a4b6791b t_a783103d t_a931e1b1 t_aaab1be9 t_b422fa6d t_b81fea6a t_b9500192 t_ba72c512 t_be219ab7 t_c1d55eef t_c792df45 t_c8784acc t_cb601d70 t_d3cc135a t_d4fca8b3 t_d8480778 t_d9f482ab t_e04bca14 t_e4c7440d t_e5e2e083 t_e8cac74b t_ec2342d5 t_edb280b5 t_efb6071f t_f9ac1ff2".split()
groups = {}
for tid in ids:
    r = cur.execute("SELECT tenant,status,title,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    key = (r["tenant"] if r else None, r["status"] if r else "?")
    groups.setdefault(key, []).append((tid, r["title"][:60] if r else "?", r["assignee"] if r else "?"))
for (ten, st), lst in sorted(groups.items(), key=lambda x: str(x[0])):
    print(f"\nTENANT={ten!r} STATUS={st} count={len(lst)}")
    for tid, ti, asg in lst[:6]:
        print(f"   {tid} [{asg}] {ti}")
    if len(lst) > 6: print(f"   ... +{len(lst)-6} lagi")
