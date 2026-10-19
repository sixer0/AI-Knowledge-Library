# Round 15-10 cron step2: VBCB freeze forensics - block reasons, run events, checkpoints, ACK census (read-only)
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def mins(ts):
    return round((now - ts) / 60.0, 1) if ts else None

TEN = "VIBE-BIBLE-1013"

print("== BLOCKED WRITER CARDS: reason + block_kind/recurrences (sample 5 + distinct reasons) ==")
reasons = {}
for r in con.execute("SELECT id, title, status, block_kind, block_recurrences, result FROM tasks WHERE tenant=? AND status='blocked'", (TEN,)).fetchall():
    res = r["result"] or ""
    head = res[:160].replace("\n", " ")
    reasons.setdefault(head, []).append(r["id"])
for h, ids in reasons.items():
    print(f"[{len(ids)}x] {h}")
    print("   sample:", ids[:3])

print("\n== RUN/TIMEOUT/GAVE_UP EVENTS THIS TENANT (last 24h) ==")
ev = {}
for r in con.execute("""
  SELECT e.kind, COUNT(*) n, MAX(e.created_at) mx
  FROM task_events e JOIN tasks t ON t.id=e.task_id
  WHERE t.tenant=? AND e.created_at > ?
  GROUP BY e.kind ORDER BY mx DESC""", (TEN, now - 24*3600)).fetchall():
    ev[r["kind"]] = (r["n"], mins(r["mx"]))
    print(r["kind"], r["n"], "last_min_ago=", mins(r["mx"]))

print("\n== OLDEST/RICHEST COMMENTS per blocked writer (top 6 by comment count) ==")
cnts = con.execute("""SELECT c.task_id, COUNT(*) n FROM task_comments c JOIN tasks t ON t.id=c.task_id
  WHERE t.tenant=? AND t.status='blocked' GROUP BY c.task_id ORDER BY n DESC LIMIT 6""", (TEN,)).fetchall()
for c0 in cnts:
    tid = c0["task_id"]
    print(f"--- {tid} ({c0['n']} comments)")
    for cm in con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)).fetchall():
        print("   ", mins(cm["created_at"]), "min ago |", cm["author"], "|", (cm["body"] or "")[:200].replace("\n", " "))

print("\n== DONE CARDS ACK CENSUS (tenant) ==")
tot_done = 0; acked = 0; markers = 0
for r in con.execute("SELECT id, title FROM tasks WHERE tenant=? AND status='done'", (TEN,)).fetchall():
    tid = r["id"]; tot_done += 1
    a = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
    m = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()[0]
    if a: acked += 1
    if m: markers += 1
print("done_total=", tot_done, "with_ACK=", acked, "with_sysman_marker=", markers)

print("\n== DONE-WITHOUT-ACK list (if any) ==")
for r in con.execute("SELECT id, title, completed_at FROM tasks WHERE tenant=? AND status='done' ORDER BY completed_at", (TEN,)).fetchall():
    tid = r["id"]
    a = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
    if not a:
        print(tid, (r["title"] or "")[:60], "completed_min_ago=", mins(r["completed_at"]))

print("\n== UNBLOCKED EVENTS THIS TENANT (watcher check) ==")
u = con.execute("""SELECT COUNT(*) n, MAX(e.created_at) mx FROM task_events e JOIN tasks t ON t.id=e.task_id
  WHERE t.tenant=? AND e.kind='unblocked'""", (TEN,)).fetchone()
print("unblocked_count=", u["n"], "last=", mins(u["mx"]))

print("\n== LAST COMMENT ANYWHERE IN TENANT (freshness of mission talk) ==")
lc = con.execute("""SELECT c.task_id, c.author, c.body, c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id
  WHERE t.tenant=? ORDER BY c.created_at DESC LIMIT 8""", (TEN,)).fetchall()
for x in lc:
    print(mins(x["created_at"]), "min |", x["task_id"], x["author"], "|", (x["body"] or "")[:180].replace("\n", " "))

print("\n== CONTROLLER/MASTER comments about VBCB outside tenant? (recent RANTAI/KEPUTUSAN) ==")
lc2 = con.execute("""SELECT c.task_id, c.author, c.body, c.created_at FROM task_comments c
  WHERE c.created_at > ? AND (c.body LIKE '%VIBE-BIBLE%' OR c.body LIKE '%VBCB%') ORDER BY c.created_at DESC LIMIT 10""", (now - 72*3600,)).fetchall()
for x in lc2:
    print(mins(x["created_at"]), "min |", x["task_id"], x["author"], "|", (x["body"] or "")[:180].replace("\n", " "))

print("\n== ANCHOR t_66b1a0b2 (AIE26SAT) + recurring billed cards current state ==")
for tid in ("t_66b1a0b2","t_6359bba5","t_bb725705","t_a3378d47"):
    row = con.execute("SELECT id,status,title,tenant FROM tasks WHERE id=?", (tid,)).fetchone()
    ev_last = con.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (tid,)).fetchone()["mx"]
    coms = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (tid,)).fetchall()
    print(tid, row["status"], "| ev_min=", mins(ev_last), "| last_com:", [(c["author"], (c["body"] or "")[:80].replace("\n"," "), mins(c["created_at"])) for c in coms])
