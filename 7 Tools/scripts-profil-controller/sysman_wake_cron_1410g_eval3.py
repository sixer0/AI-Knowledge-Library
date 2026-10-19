# Read-only eval of 24 new done-unacked WAKE rows (route-4b replica via canonical scan + per-card facts)
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

def age(ts):
    return round((NOW - ts) / 60.0, 1) if ts else None

ids = ["t_0913266d","t_0918b6d2","t_0ac8927f","t_0f3e37eb","t_19930381","t_5291d587",
"t_5715d1fc","t_6aa0384c","t_7124c228","t_7707a0cd","t_7f36de9e","t_80a9fb43",
"t_896447e4","t_99bb85a4","t_a148a692","t_a66ce30a","t_ad5d8e6f","t_b2b82e31",
"t_c2180f14","t_ccfca3b8","t_de326482","t_de73c01d","t_deb670d0","t_ed8b0b54"]

tenants = {}
for tid in ids:
    t = cur.execute("SELECT id,title,status,tenant,assignee,created_by,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(tid, "MISSING"); continue
    laps = cur.execute("SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' ORDER BY created_at", (tid,)).fetchall()
    acks = cur.execute("SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at", (tid,)).fetchall()
    mk = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["c"]
    lap_authors = sorted({r["author"] for r in laps})
    ack_authors = sorted({r["author"] for r in acks})
    # ACK from author != last LAPOR author?
    last_lap = laps[-1]["author"] if laps else None
    other_ack = [a for a in ack_authors if a != last_lap]
    tenants[t["tenant"]] = tenants.get(t["tenant"], 0) + 1
    print("%s | %s | st=%s tenant=%s | lap=%s(%s) ack=%s otherack=%s marker=%d done_age=%s" % (
        tid, (t["title"] or "")[:48], t["status"], t["tenant"], len(laps), ",".join(lap_authors)[:30],
        len(acks), ",".join(other_ack)[:20], mk, age(t["completed_at"])))

print("== TENANTS:", tenants)

# Parent liveness recheck (max event age)
p = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id='t_4edfcf3a'").fetchone()["m"]
print("== PARENT t_4edfcf3a max-event age:", age(p))
st = cur.execute("SELECT status FROM tasks WHERE id='t_4edfcf3a'").fetchone()["status"]
print("== PARENT status:", st)

# Tenant census of the new-wave tenants
for ten in tenants:
    cen = cur.execute("SELECT status,COUNT(*) n FROM tasks WHERE tenant=? GROUP BY status", (ten,)).fetchall()
    print("== CENSUS %s:" % ten, {r["status"]: r["n"] for r in cen})
con.close()
