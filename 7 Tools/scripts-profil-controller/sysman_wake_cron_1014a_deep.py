# Identify 35th stalled row + which run rows carry LAPOR + retry-run ages + wave census per W-group.
import importlib.util, time, sqlite3

spec = importlib.util.spec_from_file_location("mws", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mws = importlib.util.module_from_spec(spec); spec.loader.exec_module(mws)
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
authors = mws.DEFAULT_AUTHORS
if isinstance(authors, str): authors = authors.split(",")
now = int(time.time())
rows = mws.scan(DB, now, authors)

ORIG34 = set("""t_002af121 t_0311d1e4 t_0bf0854c t_1168e59f t_14e7030f t_153594d4 t_1c98456a
t_23f7da05 t_2e0e92d4 t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_5831a79d t_60ed37fa
t_7391c81b t_77a9bcd3 t_799a1879 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a48e52d1 t_a4b6791b t_c8784acc t_cb601d70 t_d4fca8b3 t_e04bca14
t_edb280b5 t_efb6071f t_f9ac1ff2""".split())

con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
stall_new = [r for r in rows if r[1] == "stalled" and r[0] not in ORIG34]
print("NEW_STALLED_ROWS:")
for tid, kind, age_min in stall_new:
    r = cur.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    par = [p["parent_id"] for p in cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))]
    pst = [(p, cur.execute("SELECT status FROM tasks WHERE id=?", (p,)).fetchone()["status"] if cur.execute("SELECT 1 FROM tasks WHERE id=?", (p,)).fetchone() else "?") for p in par]
    print(f"  {tid} | {r['status']} | tenant={r['tenant']} | age={age_min}m | parents={pst} | {r['title'][:70]}")

run_ids = [r[0] for r in rows if r[1] == "run-timed_out"]
print("RUN ROWS WITH LAPOR:")
for tid in run_ids:
    cs = list(cur.execute("SELECT author, created_at, substr(body,1,90) b FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' ORDER BY created_at", (tid,)))
    if cs:
        st = cur.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()["status"]
        nack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
        print(f"  {tid} status={st} ACK={nack}")
        for c in cs:
            print(f"    [{int((now-c['created_at'])/60)}m] {c['author']}: {c['b']}")

# Second-run progress: current run started_at, elapsed
print("CURRENT RUN ELAPSED (min) distribution:")
el = []
for rr in cur.execute("SELECT task_id, started_at, max_runtime_seconds FROM task_runs WHERE status='running' AND task_id IN (%s)" % ",".join("?"*len(run_ids)), run_ids):
    el.append(int((now - rr["started_at"])/60))
if el:
    print(f"  n={len(el)} min={min(el)} max={max(el)}")

# Wave census: how many writers per W group + chapters covered
import re
groups = {}
for rr in cur.execute("SELECT id,title,status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%Penulis%'"):
    m = re.search(r"\[(W\d)\].*bab (\d+)", rr["title"])
    if m:
        groups.setdefault(m.group(1), []).append((int(m.group(2)), rr["status"]))
for g in sorted(groups):
    sts = {}
    for ch, s in groups[g]: sts[s] = sts.get(s, 0) + 1
    print(f"WAVE {g}: {len(groups[g])} writers {sts}")
# Any VBCB writer done yet?
done_w = cur.execute("SELECT COUNT(*) FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%Penulis%' AND status='done'").fetchone()[0]
tot_w = cur.execute("SELECT COUNT(*) FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%Penulis%'").fetchone()[0]
print("WRITERS_DONE", done_w, "/", tot_w)
# W0 done cards (taste tests etc.)
print("VBCB non-writer statuses:")
for r in cur.execute("SELECT id,status,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title NOT LIKE '%Penulis%' AND title NOT LIKE '%Verifikasi%'"):
    print(f"  {r['id']} [{r['status']}] {r['title'][:70]}")
