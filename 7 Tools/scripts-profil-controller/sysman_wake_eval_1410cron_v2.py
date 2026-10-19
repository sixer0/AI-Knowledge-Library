# Compact round-2: group counts, non-VBCB detail, VBCB gave_up census + CHECKPOINT tokens,
# done-card ACK census per tenant, blind-spot sweep of running cards.
import sqlite3, json, time, collections

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
IDS = """t_002af121 t_0311d1e4 t_050a75ff t_0bf0854c t_0df60358 t_1168e59f t_14e7030f t_153594d4
t_1c98456a t_23f7da05 t_2543fb8f t_2ae211bb t_2d32e7c8 t_2e0e92d4 t_30dd071c t_34bf2edc t_3782b61a
t_397be920 t_46ff8be6 t_483b2d91 t_4d7a1691 t_4edfcf3a t_5831a79d t_60ed37fa t_64328060 t_674377e1
t_68d1d8be t_7391c81b t_760e7792 t_77a9bcd3 t_799a1879 t_8b90e854 t_8d618268 t_93c6bec3 t_95b5b6cb
t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc t_a064e4cc t_a37d190b t_a3e70bf1 t_a48e52d1 t_a4b6791b
t_a783103d t_a931e1b1 t_aaab1be9 t_b422fa6d t_b81fea6a t_b9500192 t_ba72c512 t_be219ab7 t_c1d55eef
t_c792df45 t_c8784acc t_cb601d70 t_d3cc135a t_d4fca8b3 t_d8480778 t_d9f482ab t_e04bca14 t_e4c7440d
t_e5e2e083 t_e8cac74b t_ec2342d5 t_edb280b5 t_efb6071f t_f9ac1ff2""".split()

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("UNIQUE WAKE IDS:", len(set(IDS)))

# 1) per-WAKE-id tenant/status compact
tenants = collections.Counter()
non_vbcb = []
for tid in sorted(set(IDS)):
    row = con.execute("SELECT id,title,status,tenant FROM tasks WHERE id=?", (tid,)).fetchone()
    if not row:
        print("MISSING", tid); continue
    tenants[row["tenant"] or "(no-tenant)"] += 1
    if (row["tenant"] or "") != "VIBE-BIBLE-1013":
        ev = con.execute("SELECT kind, MAX(created_at) m FROM task_events WHERE task_id=? GROUP BY kind ORDER BY m DESC LIMIT 3", (tid,)).fetchall()
        coms = con.execute("SELECT author, substr(body,1,160) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)).fetchall()
        par = [p["parent_id"] for p in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))]
        parst = []
        for p in par:
            pr = con.execute("SELECT status FROM tasks WHERE id=?", (p,)).fetchone()
            parst.append((p, pr["status"] if pr else "?"))
        print("\nNON-VBCB %s | %s | status=%s | tenant=%s" % (row["id"], row["title"][:80], row["status"], row["tenant"]))
        print("  events:", [(e["kind"], round((NOW-e["m"])/60)) for e in ev])
        print("  parents:", parst)
        for c in coms:
            print("  com[%s] %dm: %s" % (c["author"], round((NOW-c["created_at"])/60), c["b"].replace("\n"," ")[:150]))
print("\nTENANT COUNTS over WAKE ids:", dict(tenants))

# 2) VBCB full census by tenant (not just WAKE ids)
vb = con.execute("SELECT id,title,status,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchall()
st = collections.Counter(r["status"] for r in vb)
print("\nVBCB FULL CENSUS:", len(vb), dict(st))
gave = con.execute("SELECT COUNT(DISTINCT task_id) c FROM task_events WHERE kind='gave_up' AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')").fetchone()["c"]
print("VBCB gave_up distinct cards:", gave)
# last event age min/max across tenant
ages = []
for r in vb:
    e = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    if e: ages.append((NOW-e)/60.0)
if ages: print("VBCB last-event age min=%.0f max=%.0f min" % (min(ages), max(ages)))
# CHECKPOINT token census
cp = con.execute("SELECT COUNT(*) c FROM task_comments WHERE body LIKE '%CHECKPOINT%' AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')").fetchone()["c"]
print("VBCB comments w/ CHECKPOINT:", cp)
sample = con.execute("SELECT t.id, c.author, substr(c.body,1,300) b FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%CHECKPOINT%' ORDER BY c.created_at DESC LIMIT 2").fetchall()
for s in sample:
    print("  CP sample", s["id"], s["author"], ":", s["b"].replace("\n"," ")[:280])
# done cards ack census
done = [r["id"] for r in vb if r["status"]=="done"]
ack0 = 0; marked = 0
for did in done:
    a = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (did,)).fetchone()["c"]
    mk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (did,)).fetchone()["c"]
    if a==0: ack0 += 1
    if mk: marked += 1
print("VBCB done=%d ack0=%d marker_present=%d" % (len(done), ack0, marked))

# 3) blind spot: running cards w/ LAPOR & ack=0
run = con.execute("SELECT id,title,assignee,started_at FROM tasks WHERE status='running'").fetchall()
print("\nRUNNING cards:", len(run))
for r in run:
    lap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (r["id"],)).fetchone()["c"]
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    hb = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=? AND kind='heartbeat'", (r["id"],)).fetchone()["m"]
    if lap and not ack:
        print("  BLINDSPOT %s | %s | lap=%d ack=%d hb_age=%s run_min=%s" % (
            r["id"], r["title"][:60], lap, ack,
            round((NOW-hb)/60) if hb else "None",
            round((NOW-(r["started_at"] or NOW))/60)))
