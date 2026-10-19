# Read-only eval ronde 15-10a cron: 33 baris stalled VBCB — status, orang tua, pasangan Digantikan, ACK census
import sqlite3, time, os, re

HERMES = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HERMES, "kanban.db")
now = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

ids = ["t_002af121","t_0311d1e4","t_0bf0854c","t_1168e59f","t_14e7030f","t_153594d4","t_1c98456a","t_23f7da05","t_2e0e92d4","t_34bf2edc","t_3782b61a","t_397be920","t_46ff8be6","t_5831a79d","t_60ed37fa","t_7391c81b","t_77a9bcd3","t_799a1879","t_95b5b6cb","t_99418ea0","t_9bf75422","t_9e457da5","t_9ebc8fbc","t_a064e4cc","t_a37d190b","t_a48e52d1","t_a4b6791b","t_c8784acc","t_cb601d70","t_d4fca8b3","t_e04bca14","t_efb6071f","t_f9ac1ff2"]

# 1) Detail per kartu wake (id-list dulu, hindari nested-cursor pitfall)
print("=== DETAIL 33 KARTU WAKE ===")
status_counts = {}
for cid in ids:
    t = con.execute("SELECT id,title,status,tenant,created_at,completed_at FROM tasks WHERE id=?", (cid,)).fetchone()
    lev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()["m"]
    ncom = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=?", (cid,)).fetchone()["n"]
    parents = con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (cid,)).fetchall()
    pinfo = []
    for p in parents:
        pt = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
        dig = con.execute("SELECT body FROM task_comments WHERE task_id=? AND body LIKE '%Digantikan%' LIMIT 1", (p["parent_id"],)).fetchone()
        pinfo.append((p["parent_id"], pt["status"] if pt else "?", (dig["body"][:60] if dig else "")))
    status_counts[t["status"]] = status_counts.get(t["status"], 0) + 1
    print(f"W {cid} st={t['status']} age_ev={round((now-(lev or t['created_at']))/60)}m com={ncom} title={(t['title'] or '')[:60]}")
    for pid, pst, dg in pinfo:
        print(f"   parent {pid} st={pst} dig={dg}")
print("STATUS_COUNTS:", status_counts)

# 2) Sensus tenant VBCB per status
print("\n=== SENSUS TENANT VIBE-BIBLE-1013 ===")
print("BY_STATUS:", con.execute("SELECT status, COUNT(*) FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status").fetchall())
tot = con.execute("SELECT COUNT(*) FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchone()[0]
print("TENANT_TOTAL:", tot)

# 3) ACK census pada kartu done tenant (id-list dulu, lalu loop)
dones = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchall()]
ack_n = 0; unmarked = []
for did in dones:
    a = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (did,)).fetchone()["n"]
    m = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (did,)).fetchone()["n"]
    if a > 0: ack_n += 1
    if m == 0: unmarked.append(did)
print(f"DONE_TOTAL={len(dones)} DONE_WITH_ACK={ack_n} DONE_UNMARKED={len(unmarked)} sample_unmarked={unmarked[:8]}")

# 4) Induk tersingkir: blocked dengan komentar Digantikan -> status pasangan
print("\n=== INDUK TERSINGKIR (blocked + Digantikan) ===")
rows = con.execute("""SELECT t.id, t.title, c.body FROM tasks t JOIN task_comments c ON c.task_id=t.id
                      WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' AND c.body LIKE '%Digantikan%'""").fetchall()
print("DISPLACED_PARENTS:", len(rows))
pair_done = pair_open = pair_unknown = 0
for r in rows[:40]:
    mm = re.search(r"(t_[0-9a-f]{8})", r["body"])
    if mm:
        w = con.execute("SELECT status FROM tasks WHERE id=?", (mm.group(1),)).fetchone()
        if w is None: pair_unknown += 1
        elif w["status"] == "done": pair_done += 1
        else: pair_open += 1
print(f"REPLACEMENT done={pair_done} open={pair_open} unknown={pair_unknown}")

# 5) Event terminal gave_up/timed_out tenant
print("\n=== EVENT TERMINAL ===")
print(con.execute("""SELECT e.kind, COUNT(DISTINCT e.task_id) FROM task_events e JOIN tasks t ON t.id=e.task_id
                    WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind IN ('gave_up','timed_out') GROUP BY e.kind""").fetchall())

# 6) Umur event terakhir per kelompok status (signature beku)
for st in ("blocked","todo"):
    r = con.execute("""SELECT MIN(x), MAX(x) FROM (SELECT (SELECT MAX(created_at) FROM task_events WHERE task_id=t.id) x
                     FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status=?)""", (st,)).fetchone()
    mn = (now - r[0])//60 if r[0] else None; mx = (now - r[1])//60 if r[1] else None
    print(f"GRP {st} lastev_age_min..max = {mn}..{mx} mnt")

# 7) Triase lama: komentar dari author controller di kartu wake (sudah pernah dinilai?)
print("\n=== TRIASE LAMA pada kartu wake ===")
tri = con.execute("""SELECT c.task_id, c.author, substr(c.body,1,70), datetime(c.created_at,'unixepoch','localtime')
                     FROM task_comments c WHERE c.task_id IN (%s) ORDER BY c.created_at DESC LIMIT 15""" % ",".join("?"*len(ids)), ids).fetchall()
for r in tri: print("TRI:", tuple(r))
con.close()
