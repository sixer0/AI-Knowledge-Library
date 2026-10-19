# Ronde cron mission-wake 11-10 (sysman): rekonsiliasi kandidat detail WAKE=1
# (buang jendela 6h) + sapuan blind terminal-event <=6h tanpa syarat tenant.
import sqlite3, time, json, os

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
CAND = ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3"]

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

print("== REKONSILIASI KANDIDAT (komentar per kartu) ==")
for cid in CAND:
    row = cur.execute("SELECT id,title,status,tenant,completed_at,created_by,assignee FROM tasks WHERE id LIKE ?", (cid+"%",)).fetchone()
    if not row:
        print(f"[{cid}] TIDAK DITEMUKAN"); continue
    age_h = (now - (row["completed_at"] or 0))/3600.0
    print(f"\n--- {row['id']} | {row['title'][:60]} | status={row['status']} tenant={row['tenant']!r} done_age={age_h:.1f}h creator={row['created_by']} assignee={row['assignee']}")
    coms = cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (row["id"],)).fetchall()
    for c in coms[-8:]:
        print(f"   [{(now-c['created_at'])/60.0:7.1f}m] {c['author']}: {c['body'][:110].replace(chr(10),' / ')}")

print("\n== BLIND SWEEP: event terminal <=6h TANPA syarat tenant ==")
cut = now - 6*3600
evs = cur.execute("""
  SELECT e.task_id, e.kind, e.created_at, t.status, t.tenant, t.title
  FROM task_events e JOIN tasks t ON t.id=e.task_id
  WHERE e.created_at >= ? AND e.kind IN ('completed','parked','blocked')
  ORDER BY e.created_at DESC LIMIT 60
""", (cut,)).fetchall()
seen = set()
for e in evs:
    if e["task_id"] in seen: continue
    seen.add(e["task_id"])
print(f"baris event terminal unik <=6h: {len(seen)}")

# Untuk tiap kartu terminal <=6h yang done/blocked: cek LAPOR vs ACK (author-lain, urutan)
print("\n-- kartu terminal <=6h tanpa ACK author-lain pasca-LAPOR --")
hits = 0
for tid in seen:
    row = cur.execute("SELECT id,status,tenant,title,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not row or row["status"] not in ("done","blocked","parked"): continue
    coms = cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)).fetchall()
    lapor = [c for c in coms if "LAPOR-SELESA" in c["body"].upper() or "LAPOR SELESAI" in c["body"].upper()]
    if not lapor: continue
    anchor = lapor[-1]["created_at"]; lauthor = lapor[-1]["author"]
    acks = [c for c in coms if "RANTAI-ACK" in c["body"].upper() and c["created_at"] >= anchor]
    ack_lain = [c for c in acks if c["author"] != lauthor]
    mark = [c for c in coms if "RANTAI-WAKE" in c["body"].upper()]
    if not ack_lain:
        hits += 1
        print(f"HIT {row['id']} | {row['title'][:55]} | status={row['status']} tenant={row['tenant']!r} lap={lauthor}@{(now-anchor)/60.0:.0f}m ack_total_post={len(acks)} marker={len(mark)}")
if hits == 0:
    print("(kosong — semua kartu ber-LAPOR di jendela ini sudah ter-ACK author-lain)")
con.close()
