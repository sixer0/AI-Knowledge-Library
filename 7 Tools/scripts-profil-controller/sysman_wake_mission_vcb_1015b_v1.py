# Ronde 15-10b: vonis tingkat-misi VIBE-BIBLE-1013 (VBCB).
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())
m = lambda s: round((now - s)/60.0, 1) if s else None
TEN = "VIBE-BIBLE-1013%"

print("== SENSUS STATUS TENANT ==")
for r in cur.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant LIKE ? GROUP BY status ORDER BY c DESC", (TEN,)):
    print(f"  {r['status']}: {r['c']}")
print("  total:", cur.execute("SELECT COUNT(*) FROM tasks WHERE tenant LIKE ?", (TEN,)).fetchone()[0])

print("\n== EVENT KINDS LINTAS TENANT (top) ==")
q = """SELECT e.kind, COUNT(*) c, MAX(e.created_at) mx FROM task_events e JOIN tasks t ON t.id=e.task_id
       WHERE t.tenant LIKE ? GROUP BY e.kind ORDER BY c DESC"""
for r in cur.execute(q, (TEN,)):
    print(f"  {r['kind']}: n={r['c']} last_age_min={m(r['mx'])}")

print("\n== UNBLOCKED TERAKHIR (watcher hidup?) ==")
qu = """SELECT e.task_id, e.created_at FROM task_events e JOIN tasks t ON t.id=e.task_id
        WHERE t.tenant LIKE ? AND e.kind='unblocked' ORDER BY e.created_at DESC LIMIT 8"""
rows = list(cur.execute(qu, (TEN,)))
if not rows: print("  TIDAK ADA event unblocked sama sekali")
for r in rows: print(f"  {r['task_id']} age_min={m(r['created_at'])}")

print("\n== GAVE_UP / TIMED_OUT TERAKHIR ==")
qt = """SELECT e.kind, e.task_id, e.created_at FROM task_events e JOIN tasks t ON t.id=e.task_id
        WHERE t.tenant LIKE ? AND e.kind IN ('gave_up','timed_out') ORDER BY e.created_at DESC LIMIT 6"""
for r in cur.execute(qt, (TEN,)):
    print(f"  {r['kind']} {r['task_id']} age_min={m(r['created_at'])}")
print("  counts:", dict((r['kind'], r['c']) for r in cur.execute(
    """SELECT e.kind, COUNT(*) c FROM task_events e JOIN tasks t ON t.id=e.task_id
       WHERE t.tenant LIKE ? AND e.kind IN ('gave_up','timed_out') GROUP BY e.kind""", (TEN,))))

print("\n== ORANG TUA BLOCKED: REASON + UMUR EVENT + KOMENTAR TERAKHIR ==")
pset = set()
for r in cur.execute("SELECT id, title, reason, created_at FROM tasks WHERE tenant LIKE ? AND status='blocked' AND title LIKE '%Penulis%'", (TEN,)):
    pset.add(r["id"])
print("  jumlah orang tua Penulis blocked:", len(pset))
first = True
for pid in sorted(pset):
    t = cur.execute("SELECT * FROM tasks WHERE id=?", (pid,)).fetchone()
    ev = cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    cm = cur.execute("SELECT author, SUBSTR(body,1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    if first:
        print("  SAMPLE reason:", repr((t["reason"] or "")[:200]))
        first = False
    if pid in sorted(pset)[:3]:
        print(f"  {pid} ev={ev['kind'] if ev else None} ev_age={m(ev['created_at']) if ev else None} lastcm={cm['author'] if cm else None}:{(cm['b'] if cm else '')[:60]!r} cm_age={m(cm['created_at']) if cm else None}")
# sebaran umur event terakhir orang tua blocked
ages = []
for pid in pset:
    ev = cur.execute("SELECT created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    if ev: ages.append(m(ev["created_at"]))
if ages: print(f"  rentang umur event terakhir orang tua blocked: min={min(ages)} max={max(ages)} menit")

print("\n== SEMUA BLOCKED TENANT: kelompok reason ==")
groups = {}
for r in cur.execute("SELECT id, COALESCE(reason,'(kosong)') rs FROM tasks WHERE tenant LIKE ? AND status='blocked'", (TEN,)):
    key = r["rs"][:60]
    groups.setdefault(key, []).append(r["id"])
for k, v in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    print(f"  [{len(v)}x] {k!r} contoh={v[:2]}")

print("\n== DONE TANPA ACK (serah-terima senyap) + MARKER ==")
done_ack = {"ack0_marker0": 0, "ack0_marker1": 0, "ack_ge1": 0}
samples = []
for r in cur.execute("SELECT id, title FROM tasks WHERE tenant LIKE ? AND status='done'", (TEN,)):
    ack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    mk = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()[0]
    if ack >= 1: done_ack["ack_ge1"] += 1
    elif mk: done_ack["ack0_marker1"] += 1
    else:
        done_ack["ack0_marker0"] += 1
        samples.append((r["id"], (r["title"] or "")[:55]))
print("  ", done_ack)
print("  kandidat done-unacked TANPA marker:", len(samples))
for s in samples[:15]: print("   ", s)

print("\n== RUNNING TENANT + BLIND SPOT GLOBAL ==")
run = cur.execute("SELECT id,title,tenant,last_heartbeat_at FROM tasks WHERE status='running'").fetchall()
print("  total running global:", len(run))
for r in run:
    lap = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (r["id"],)).fetchone()[0]
    acks = cur.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchall()
    lap_a = {x["author"] for x in cur.execute("SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (r["id"],))}
    other = [a for a in acks if a["author"] not in lap_a]
    ev = cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    print(f"  {r['id']} tenant={r['tenant']} lap={lap} other_ack={len(other)} last_ev={ev['kind'] if ev else None} age={m(ev['created_at']) if ev else None} hb_age={m(r['last_heartbeat_at'])} title={(r['title'] or '')[:50]}")

print("\n== FASE-STALL / KARTU LAIN DI LUAR VBCB pada daftar wake? ==")
# semua baris WAKE sudah diketahui VBCB; cek apakah ada kartu non-VBCB berumur event ~690mnt yang juga perlu
q2 = """SELECT t.id, t.status, t.tenant, SUBSTR(t.title,1,55) ti, MAX(e.created_at) mx
        FROM tasks t JOIN task_events e ON e.task_id=t.id
        WHERE t.status IN ('todo','blocked','running') AND (t.tenant IS NULL OR t.tenant NOT LIKE ?)
        GROUP BY t.id HAVING mx < ? AND mx > ? ORDER BY mx DESC LIMIT 12"""
cut_hi = now - 600*60; cut_lo = now - 1791630000 if False else now - 24*3600*30
for r in cur.execute(q2, (TEN, now-720*60, now-600*60)):
    print(f"  {r['id']} {r['status']} tenant={r['tenant']} ev_age={m(r['mx'])} {r['ti']}")
