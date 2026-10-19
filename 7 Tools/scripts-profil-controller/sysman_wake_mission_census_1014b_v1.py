# Read-only mission-level census for tenant VIBE-BIBLE-1013 + blindspot sweep.
import sqlite3, time, collections, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = int(time.time())

def fmt(ts):
    return time.strftime("%m-%d %H:%M", time.localtime(ts)) if ts else "-"

print("== tenant census VIBE-BIBLE-1013 ==")
rows = con.execute("SELECT id,title,status,assignee,created_at,completed_at,max_runtime_seconds FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchall()
st = collections.Counter(r["status"] for r in rows)
print("total:", len(rows), dict(st))

# ACK count per card
print("\n== done cards: ACK census ==")
done_ids = [r["id"] for r in rows if r["status"] == "done"]
n_ack0 = 0
for i in done_ids:
    nack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (i,)).fetchone()["c"]
    nlap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (i,)).fetchone()["c"]
    if nack == 0:
        n_ack0 += 1
        t = con.execute("SELECT title FROM tasks WHERE id=?", (i,)).fetchone()["title"]
        print(f"  ACK0 {i} lapor={nlap} {t[:60]}")
print("done total:", len(done_ids), "ack0:", n_ack0)

# blocked writer cards: sample comments (last 3 per card, truncated) - look for CHECKPOINT
print("\n== blocked writer cards: comment samples (CHECKPOINT/LAPOR) ==")
blocked = [r for r in rows if r["status"] == "blocked"]
cp_any = 0
for r in blocked[:6]:
    cs = con.execute("SELECT author, substr(body,1,220) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (r["id"],)).fetchall()
    print(f"-- {r['id']} {r['title'][:50]} mrs={r['max_runtime_seconds']}")
    for c in cs:
        print(f"   [{fmt(c['created_at'])}] {c['author']}: {c['b'][:200]}".replace("\n", " | "))
for r in blocked:
    n = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND upper(body) LIKE '%CHECKPOINT%'", (r["id"],)).fetchone()["c"]
    cp_any += n
print("total CHECKPOINT comments across blocked:", cp_any)

# max_runtime distribution among blocked
mrs = collections.Counter(r["max_runtime_seconds"] for r in blocked)
print("max_runtime_seconds dist (blocked):", dict(mrs))

# runs for a couple of blocked cards: elapsed, retry_status
print("\n== task_runs sample (t_050a75ff, t_d3cc135a) ==")
try:
    rc = [c["name"] for c in con.execute("PRAGMA table_info(task_runs)")]
    print("task_runs cols:", rc)
    for cid in ("t_050a75ff", "t_d3cc135a"):
        for run in con.execute("SELECT * FROM task_runs WHERE task_id=? ORDER BY rowid DESC LIMIT 3", (cid,)):
            d = dict(run)
            print(cid, {k: (fmt(v) if "at" in k and isinstance(v, int) else v) for k, v in d.items() if v not in (None, "")})
except Exception as e:
    print("runs err:", e)

# scheduled card
print("\n== scheduled card ==")
for r in con.execute("SELECT id,title,status,tenant,assignee,created_at FROM tasks WHERE status='scheduled'"):
    print(dict(r))

# any open card outside VIBE-BIBLE (blocked/todo not in tenant) -> other missions needing hand?
print("\n== open cards NOT VIBE-BIBLE-1013 ==")
for r in con.execute("SELECT id,title,status,tenant,assignee,created_at FROM tasks WHERE status IN ('todo','blocked','running','scheduled') AND (tenant IS NULL OR tenant!='VIBE-BIBLE-1013') ORDER BY created_at DESC LIMIT 30"):
    age = round((now - r["created_at"]) / 60.0)
    print(f"{r['id']} [{r['status']}] tenant={r['tenant']} age_min={age} {r['title'][:70]}")

# last event age for tenant overall
mx = con.execute("SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013'").fetchone()["m"]
print("\ntenant last event:", fmt(mx), "age_min:", round((now - mx) / 60.0))

# who created the mission / dispatcher card?
print("\n== earliest cards of tenant (origin) ==")
for r in con.execute("SELECT id,title,status,created_by,created_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' ORDER BY created_at LIMIT 5"):
    print(r["id"], r["status"], r["created_by"], fmt(r["created_at"]), r["title"][:60])
