# Verifikasi: author+umur marker RANTAI-WAKE pada 11 kartu done; pemetaan baris WAKE ke tenant/status.
import sqlite3, time, collections
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

done_ids = ['t_87b1a40e','t_4330b479','t_5957156d','t_b378d64e','t_68f547bd','t_87aa2f1f','t_ff19af14','t_2de376b5','t_be215530','t_c6512519','t_009f2fdc']
print("== MARKER pada kartu done VBCB ==")
for tid in done_ids:
    ms = list(con.execute("SELECT author, created_at, substr(body,1,60) b FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%' ORDER BY created_at", (tid,)))
    acks = list(con.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)))
    for m in ms:
        print(f"  {tid}: marker[{m['author']}] umur={(now-m['created_at'])//60}m | ack={len(acks)}")

# Baris WAKE dari scan: petakan id -> tenant,status
wake_ids = set("""t_002af121 t_0311d1e4 t_050a75ff t_0bf0854c t_0df60358 t_1168e59f t_14e7030f t_153594d4 t_1c98456a t_23f7da05 t_2543fb8f t_2ae211bb t_2d32e7c8 t_2e0e92d4 t_30dd071c t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_483b2d91 t_4d7a1691 t_4edfcf3a t_5831a79d t_60ed37fa t_64328060 t_674377e1 t_68d1d8be t_7391c81b t_760e7792 t_77a9bcd3 t_799a1879 t_8b90e854 t_8d618268 t_93c6bec3 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc t_a064e4cc t_a37d190b t_a3e70bf1 t_a48e52d1 t_a4b6791b t_a783103d t_a931e1b1 t_aaab1be9 t_b422fa6d t_b81fea6a t_b9500192 t_ba72c512 t_be219ab7 t_c1d55eef t_c792df45 t_c8784acc t_cb601d70 t_d3cc135a t_d4fca8b3 t_d8480778 t_d9f482ab t_e04bca14 t_e4c7440d t_e5e2e083 t_e8cac74b t_ec2342d5 t_edb280b5 t_efb6071f t_f9ac1ff2""".split())
print(f"\n== PETAKAN {len(wake_ids)} id unik baris WAKE ==")
cnt = collections.Counter()
other = []
for tid in sorted(wake_ids):
    r = con.execute("SELECT tenant,status,title,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    if r is None:
        cnt[("(hilang)")] += 1; continue
    cnt[(r["tenant"] or "(null)", r["status"])] += 1
    if (r["tenant"] or "") != "VIBE-BIBLE-1013":
        other.append((tid, r["tenant"], r["status"], r["title"][:60], r["assignee"]))
for k, v in sorted(cnt.items(), key=lambda x: str(x[0])):
    print(f"  {k}: {v}")
if other:
    print("\n  LUAR VBCB:")
    for o in other:
        print("   ", o)

# Kartu blocked non-VBCB papan (44 total vs 34 VBCB) - siapa sisanya?
print("\n== BLOCKED NON-VBCB ==")
for r in con.execute("SELECT id,tenant,status,title,assignee FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant!='VIBE-BIBLE-1013') ORDER BY created_at DESC LIMIT 15"):
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    age = (now-(ev or 0))//60
    print(f"  {r['id']} tenant={r['tenant']} '{r['title'][:50]}' umur_event={age}m")

# Umur last event tiap kartu blocked VBCB (apakah flat semua ~212m?)
print("\n== UMUR EVENT TERAKHIR kartu blocked VBCB (min/max) ==")
ages = []
for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'"):
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    ages.append((now-ev)//60)
print(f"  n={len(ages)} min={min(ages)}m max={max(ages)}m")

# Cek apakah ada komentar [FASE] / triase controller di kartu blocked VBCB setelah promoted
print("\n== KOMENTAR TERAKHIR per kartu blocked VBCB (author, 70 char) ==")
seen = collections.Counter()
for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'"):
    c = con.execute("SELECT author, substr(body,1,70) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    if c:
        seen[c["author"]] += 1
print("  author komentar terakhir:", dict(seen))
con.close()
