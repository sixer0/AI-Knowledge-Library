# Round 2 (read-only): reconcile parents of 33 WAKE stalled cards + context.
import sqlite3, time, collections, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
WAKE = """t_002af121 t_0311d1e4 t_0bf0854c t_1168e59f t_14e7030f t_153594d4 t_1c98456a
t_23f7da05 t_2e0e92d4 t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_5831a79d t_60ed37fa
t_7391c81b t_77a9bcd3 t_799a1879 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a48e52d1 t_a4b6791b t_c8784acc t_cb601d70 t_d4fca8b3 t_e04bca14
t_efb6071f t_f9ac1ff2""".split()

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

# 1. collect all parents first (id-list then per-id queries; no nested cursors)
parents = set()
for tid in WAKE:
    for r in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)):
        parents.add(r[0])
print("distinct_parents=", len(parents))
pstat = collections.Counter()
pdetail = {}
for p in sorted(parents):
    t = con.execute("SELECT id,status,title,tenant FROM tasks WHERE id=?", (p,)).fetchone()
    if not t:
        pdetail[p] = "MISSING"; pstat["MISSING"] += 1; continue
    pstat[t["status"]] += 1
    pdetail[p] = (t["status"], (t["title"] or "")[:75])
print("parent_status_census:", dict(pstat))
blocked_parents = [p for p,v in pdetail.items() if isinstance(v,tuple) and v[0]=="blocked"]
print("blocked_parents sample:", blocked_parents[:5])
for p in blocked_parents[:3]:
    print(" ", p, pdetail[p])

# 2. the 33 blocked VBCB cards: are they the writers? do they carry Digantikan / CHECKPOINT?
print("\n=== BLOCKED VBCB CARDS ===")
blk = [dict(r) for r in con.execute("SELECT id,title,status,created_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'")]
print("count=", len(blk))
ids = [b["id"] for b in blk]
for cid in ids[:6]:
    cs = [dict(r) for r in con.execute("SELECT author, substr(body,1,160) body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4",(cid,))]
    ev = [dict(r) for r in con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5",(cid,))]
    print(cid, "|", next(b["title"] for b in blk if b["id"]==cid))
    for e in ev: print("   ev:", e["kind"], round((NOW-e["created_at"])/60),"min")
    for c in cs: print("   cm:", c["author"], "|", (c["body"] or "").replace("\n"," ")[:140])
dig = 0; chk = 0
for cid in ids:
    n = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%Digantikan%'",(cid,)).fetchone()[0]
    m = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%CHECKPOINT%'",(cid,)).fetchone()[0]
    dig += 1 if n else 0; chk += 1 if m else 0
print("blocked_with_Digantikan_comment=", dig, "blocked_with_CHECKPOINT=", chk)

# 3. done VBCB cards: markers from previous sysman rounds? M4 replacements?
print("\n=== DONE VBCB MARKERS ===")
done_ids = [r[0] for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'")]
mk = 0
for cid in done_ids:
    n = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'",(cid,)).fetchone()[0]
    mk += 1 if n else 0
print("done=", len(done_ids), "with_sysman_marker=", mk)
m4 = [dict(r) for r in con.execute("SELECT id,status,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%M4%'")]
print("M4_cards=", len(m4), collections.Counter(x['status'] for x in m4))

# 4. age spread of last events per VBCB card (freeze check)
ages = []
for cid in [r[0] for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013'")]:
    m = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()[0]
    if m: ages.append((NOW-m)/60)
if ages:
    print("VBCB last-event age min/median/max:", round(min(ages)), round(sorted(ages)[len(ages)//2]), round(max(ages)))

# 5. blocked cards OUTSIDE VBCB (other tenants / null) - open board debt
print("\n=== BLOCKED NON-VBCB ===")
oth = [dict(r) for r in con.execute("SELECT id,title,status,tenant,updated_at FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant!='VIBE-BIBLE-1013') ORDER BY created_at DESC LIMIT 20").description and con.execute("SELECT id,title,status,tenant FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant!='VIBE-BIBLE-1013') ORDER BY created_at DESC")]
for c in oth:
    le = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (c["id"],)).fetchone()[0]
    nc = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=?", (c["id"],)).fetchone()[0]
    la = con.execute("SELECT author, substr(body,1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",(c["id"],)).fetchone()
    print(c["id"], "|", (c["title"] or "")[:60], "| tenant=", c["tenant"], "| lastev_min=", round((NOW-le)/60) if le else None, "| ncm=", nc,
          "| last:", (la["author"]+":"+(la["b"] or "").replace(chr(10)," ")) if la else "-")

# 6. todo cards outside VBCB
print("\n=== TODO NON-VBCB ===")
td = [dict(r) for r in con.execute("SELECT id,title,tenant FROM tasks WHERE status='todo' AND (tenant IS NULL OR tenant!='VIBE-BIBLE-1013')")]
print("count=", len(td))
for c in td[:10]: print(c["id"], (c["title"] or "")[:60], c["tenant"])
