# Round 14-10c: classify last worker checkpoint per blocked writer card (artifact present vs zero).
import sqlite3, time, re

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

blocked = cur.execute("SELECT id, title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' ORDER BY title").fetchall()
print(f"blocked writers: {len(blocked)}")
zero, some, unknown = [], [], []
for b in blocked:
    cmts = cur.execute("SELECT author, body FROM task_comments WHERE task_id=? ORDER BY created_at DESC", (b["id"],)).fetchall()
    worker_cmt = next((c["body"] or "" for c in cmts if c["author"] == "gsp-worker"), None)
    if worker_cmt is None:
        unknown.append(b["id"]); continue
    head = worker_cmt[:600]
    if re.search(r"NOL (berkas|artefak)|BELUM ada|belum ada artefak|nol pekerjaan|masih kosong", head, re.I):
        # may still list real artifacts later in body; check for byte-size pattern
        if re.search(r"\(\d[\d.,]*\s*(?:B|KB)\)", worker_cmt):
            some.append(b["id"])
        else:
            zero.append(b["id"])
    else:
        some.append(b["id"])
print(f"zero-artifact checkpoints: {len(zero)} -> {zero}")
print(f"partial-artifact checkpoints: {len(some)} -> {some}")
print(f"no-worker-comment: {len(unknown)} -> {unknown}")

# total runs burned this tenant
n = cur.execute("SELECT COUNT(*) c, SUM(tr.ended_at - tr.started_at) s FROM task_runs tr JOIN tasks t ON t.id=tr.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND tr.outcome='timed_out'").fetchone()
print(f"timed_out runs in tenant: {n['c']} total_elapsed_hours={round((n['s'] or 0)/3600,1)}")
n2 = cur.execute("SELECT COUNT(*) c FROM task_runs tr JOIN tasks t ON t.id=tr.task_id WHERE t.tenant='VIBE-BIBLE-1013'").fetchone()
print(f"all runs in tenant: {n2['c']}")

# done cards in tenant - what are they?
print("\ndone cards:")
for d in cur.execute("SELECT id, title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done' ORDER BY title"):
    ack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (d["id"],)).fetchone()["c"]
    print(f"  {d['id']} ack={ack} {(d['title'] or '')[:70]}")
