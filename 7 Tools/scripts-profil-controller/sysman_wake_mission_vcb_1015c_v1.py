# Ronde 15-10c: sisa vonis VBCB (reason via payload event, census ACK, blind spot).
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())
m = lambda s: round((now - s)/60.0, 1) if s else None
TEN = "VIBE-BIBLE-1013%"

print("== ORANG TUA BLOCKED (Penulis): umur event + komentar terakhir + reason payload ==")
pset = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE tenant LIKE ? AND status='blocked' AND title LIKE '%Penulis%'", (TEN,))]
print("  jumlah Penulis blocked:", len(pset))
ages = []
for pid in pset:
    ev = cur.execute("SELECT kind, payload, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    if ev: ages.append(m(ev["created_at"]))
if ages: print(f"  rentang umur event terakhir: min={min(ages)} max={max(ages)} menit")
for pid in pset[:4]:
    t = cur.execute("SELECT id,title,last_failure_error FROM tasks WHERE id=?", (pid,)).fetchone()
    ev = cur.execute("SELECT kind, payload, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    cm = cur.execute("SELECT author, SUBSTR(body,1,120) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    print(f"  {pid} ev={ev['kind']} age={m(ev['created_at'])} payload={(ev['payload'] or '')[:150]}")
    print(f"     lfe={(t['last_failure_error'] or '')[:120]}")
    print(f"     cm={cm['author'] if cm else None} age={m(cm['created_at']) if cm else None} body={(cm['b'] if cm else '')!r}")

print("\n== KELOMPOK BLOCKED via payload reason ==")
groups = {}
for r in cur.execute("SELECT id FROM tasks WHERE tenant LIKE ? AND status='blocked'", (TEN,)):
    ev = cur.execute("SELECT payload FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    key = ((ev["payload"] if ev else None) or "(tanpa event blocked)")[:70]
    groups.setdefault(key, []).append(r["id"])
for k, v in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    print(f"  [{len(v)}x] {k!r}")

print("\n== CENSUS DONE x ACK x MARKER ==")
a0m0 = []; a0m1 = 0; ack = 0
for r in cur.execute("SELECT id, title FROM tasks WHERE tenant LIKE ? AND status='done'", (TEN,)):
    ac = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    mk = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()[0]
    if ac: ack += 1
    elif mk: a0m1 += 1
    else: a0m0.append((r["id"], (r["title"] or "")[:55]))
print(f"  done=46 -> ber-ACK={ack} | tanpa-ACK+bermarker={a0m1} | tanpa-ACK+tanpa-marker={len(a0m0)}")
for s in a0m0: print("   kandidat:", s)

print("\n== BLIND SPOT: running global ==")
run = cur.execute("SELECT id,title,tenant,last_heartbeat_at FROM tasks WHERE status='running'").fetchall()
print("  total running:", len(run))
for r in run:
    lap_a = {x["author"] for x in cur.execute("SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (r["id"],))}
    acks = cur.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchall()
    other = [a for a in acks if a["author"] not in lap_a]
    ev = cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    print(f"  {r['id']} tenant={r['tenant']} lap_authors={lap_a} other_ack={len(other)} last_ev={ev['kind'] if ev else None} age={m(ev['created_at']) if ev else None} hb_age={m(r['last_heartbeat_at'])} {(r['title'] or '')[:55]}")

print("\n== NON-VBCB: kartu terbuka ber-event terakhir 600-720 mnt (bandingkan jendela wake) ==")
q2 = """SELECT t.id, t.status, t.tenant, SUBSTR(t.title,1,55) ti, MAX(e.created_at) mx
        FROM tasks t JOIN task_events e ON e.task_id=t.id
        WHERE t.status IN ('todo','blocked','running') AND (t.tenant IS NULL OR t.tenant NOT LIKE ?)
        GROUP BY t.id HAVING mx < ? AND mx > ? ORDER BY mx DESC LIMIT 15"""
n = 0
for r in cur.execute(q2, (TEN, now-720*60, now-600*60)):
    n += 1
    print(f"  {r['id']} {r['status']} tenant={r['tenant']} ev_age={m(r['mx'])} {r['ti']}")
if n == 0: print("  (kosong)")

print("\n== KARTU EKOR VBCB: done terbaru + komentar CHECKPOINT/PARKED tanpa ACK ==")
q3 = """SELECT t.id, SUBSTR(t.title,1,55) ti, t.completed_at FROM tasks t
        WHERE t.tenant LIKE ? AND t.status='done' ORDER BY t.completed_at DESC LIMIT 5"""
for r in cur.execute(q3, (TEN,)):
    acks = cur.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchall()
    print(f"  {r['id']} done_age={m(r['completed_at'])} ack={[ (a['author'], m(a['created_at'])) for a in acks]} {r['ti']}")
