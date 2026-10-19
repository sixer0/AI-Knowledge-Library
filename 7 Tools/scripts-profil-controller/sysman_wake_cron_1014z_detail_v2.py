# Detil misi VBCB: gave_up per kartu, komentar CHECKPOINT, sensus done+ACK tenant, blocked luar-tenant.
import sqlite3, time
from collections import defaultdict

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

TEN = "VIBE-BIBLE-1013"

print("=== TENANT CENSUS (exact tenant=) ===")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant=? GROUP BY status", (TEN,)):
    print(" ", r["status"], r["n"])
tot = con.execute("SELECT COUNT(*) n FROM tasks WHERE tenant=?", (TEN,)).fetchone()["n"]
print("  TOTAL tenant:", tot)
anch = con.execute("SELECT COUNT(*) n FROM tasks WHERE tenant IS NULL AND title LIKE '%VBCB%'").fetchone()["n"]
print("  anchor/jangkar tenant-NULL judul VBCB:", anch)

print("\n=== BLOCKED CARDS: kind event terakhir + CHECKPOINT comment ===")
cp_total = 0
for r in con.execute("SELECT id, title, block_recurrences FROM tasks WHERE tenant=? AND status='blocked' ORDER BY id", (TEN,)):
    ev = con.execute("SELECT kind, MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()
    kinds = [x["kind"] for x in con.execute("SELECT kind FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (r["id"],))]
    cp = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%CHECKPOINT%'", (r["id"],)).fetchone()["n"]
    cp_total += cp
    gave = con.execute("SELECT COUNT(*) n FROM task_events WHERE task_id=? AND kind='gave_up'", (r["id"],)).fetchone()["n"]
    tout = con.execute("SELECT COUNT(*) n FROM task_events WHERE task_id=? AND kind='timed_out'", (r["id"],)).fetchone()["n"]
    print(f"  {r['id']} rec={r['block_recurrences']} gave_up={gave} timed_out={tout} cp_cmt={cp} recent={kinds} :: {r['title'][:44]}")
print("cards with CHECKPOINT comments:", cp_total)

print("\n=== SAMPLE CHECKPOINT body (first 2 cards) ===")
seen = 0
for r in con.execute("SELECT task_id, author, body, created_at FROM task_comments WHERE body LIKE '%CHECKPOINT%' AND task_id IN (SELECT id FROM tasks WHERE tenant=?) ORDER BY created_at DESC", (TEN,)):
    print(f"--- {r['task_id']} by {r['author']} age={(now-r['created_at'])/60:.0f}m")
    print(r["body"][:600].replace("\r\n", "\n"))
    seen += 1
    if seen >= 2: break

print("\n=== DONE CARDS TENANT: ACK census ===")
done_ids = [x["id"] for x in con.execute("SELECT id FROM tasks WHERE tenant=? AND status='done'", (TEN,))]
no_ack = []
for tid in done_ids:
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    if ack == 0: no_ack.append(tid)
print("done:", len(done_ids), "| ack=0:", len(no_ack))
mk = 0
for tid in no_ack:
    m = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["n"]
    mk += (m > 0)
print("dari yang ack=0, sudah ber-marker sysman:", mk)

print("\n=== BLOCKED LUAR-TENANT (11 kartu) ===")
for r in con.execute("SELECT id, tenant, title, created_at FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant!=?) ORDER BY created_at DESC", (TEN,)):
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    cm = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=?", (r["id"],)).fetchone()["n"]
    lastc = con.execute("SELECT author, substr(body,1,80) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    print(f"  {r['id']} tenant={r['tenant']!r} ev_age={(now-ev)/60:.0f}m cm={cm} last={lastc['author'] if lastc else '-'}:{(lastc['b'] if lastc else '')[:60]!r} :: {r['title'][:44]}")

print("\n=== TODO CHILDREN: parents status ===")
par_stat = defaultdict(int)
for r in con.execute("""SELECT c.id child, p.status pstat FROM task_links l
    JOIN tasks c ON c.id=l.child_id JOIN tasks p ON p.id=l.parent_id
    WHERE c.tenant=? AND c.status='todo'""", (TEN,)):
    par_stat[r["pstat"]] += 1
print(dict(par_stat))

print("\n=== max_runtime & elapsed cap (blocked sample payload) ===")
r = con.execute("SELECT id, max_runtime_seconds FROM tasks WHERE tenant=? AND status='blocked' LIMIT 1", (TEN,)).fetchone()
print("max_runtime_seconds:", r["max_runtime_seconds"])
p = con.execute("SELECT payload FROM task_events WHERE task_id=? AND kind IN ('timed_out','gave_up') ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
if p: print("payload:", (p["payload"] or "")[:400])
