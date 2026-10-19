# Ronde wake 14-10c langkah 2: isi komentar CHECKPOINT/LAPOR + event gave_up + marker cek (read-only)
import sqlite3, time, json, collections

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

TEN = "VIBE-BIBLE-1013"
cards = con.execute("SELECT id,title,status,max_runtime_seconds,consecutive_failures,current_run_id FROM tasks WHERE tenant=?", (TEN,)).fetchall()

print("=== max_runtime / failures distribusi (blocked) ===")
dist = collections.Counter()
for c in cards:
    if c["status"] == "blocked":
        dist[(c["max_runtime_seconds"], c["consecutive_failures"])] += 1
for k,v in dist.most_common(): print("  cap=%s fails=%s -> %s kartu" % k if False else f"  cap={k[0]} fails={k[1]} -> {v} kartu")

print("\n=== EVENT gave_up/timed_out/blocked: contoh payload ===")
seen = 0
for c in cards:
    if c["status"] != "blocked": continue
    evs = con.execute("SELECT kind,payload,created_at FROM task_events WHERE task_id=? AND kind IN ('gave_up','timed_out','blocked') ORDER BY created_at", (c["id"],)).fetchall()
    if seen < 3:
        print(f"-- {c['id']}")
        for e in evs:
            print(f"   {e['kind']} @ {(NOW-e['created_at'])/60:.0f}m lalu | {(e['payload'] or '')[:160]}")
    seen += 1

print("\n=== KONSUMEN komentar CHECKPOINT/LAPOR (3 kartu contoh) ===")
sample_ids = ["t_050a75ff","t_d3cc135a","t_674377e1"]
for cid in sample_ids:
    print(f"\n#### {cid}")
    for r in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (cid,)).fetchall():
        b = (r["body"] or "").replace("\r"," ")
        print(f"  [{(NOW-r['created_at'])/60:.0f}m] {r['author']}: {b[:600]}")

print("\n=== MARKER RANTAI-WAKE pada 11 kartu done? ===")
for c in cards:
    if c["status"] != "done": continue
    mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (c["id"],)).fetchone()["n"]
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (c["id"],)).fetchone()["n"]
    cm = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=?", (c["id"],)).fetchone()["n"]
    print(f"  {c['id']} comments={cm} marker={mk} ack={ack} | {(c['title'] or '')[:55]}")

print("\n=== ADA komentar author controller/default di kartu blocked (triase)? ===")
auth = collections.Counter()
for c in cards:
    if c["status"] != "blocked": continue
    for r in con.execute("SELECT author FROM task_comments WHERE task_id=?", (c["id"],)).fetchall():
        auth[r["author"]] += 1
print("  authors komentar kartu blocked:", dict(auth))

# kapan terakhir aktivitas papan utk tenant ini
last = con.execute("""SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=?""", (TEN,)).fetchone()["m"]
lastc = con.execute("""SELECT MAX(c.created_at) m FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant=?""", (TEN,)).fetchone()["m"]
print(f"\nAKTIVITAS TENANT: last_event={(NOW-last)/60:.0f}m last_comment={(NOW-lastc)/60:.0f}m")

# gelombang W0 done: kapan selesai + apakah ada vonis/LAPOR
print("\n=== W0 done: completed_at + komentar terakhir ===")
for c in cards:
    if c["status"] != "done": continue
    ca = c["completed_at"]
    lc = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (c["id"],)).fetchone()
    lcs = f"{lc['author']}: {(lc['body'] or '')[:80].replace(chr(10),' ')} ({(NOW-lc['created_at'])/60:.0f}m)" if lc else "-"
    print(f"  {c['id']} done {(NOW-ca)/60:.0f}m lalu | {lcs}")
con.close()
