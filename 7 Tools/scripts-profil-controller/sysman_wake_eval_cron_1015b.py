# sysman cron 15-10 ronde B: vonis tingkat-misi VIBE-BIBLE-1013 (blocked parents, watcher, ACK census)
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
TN = "VIBE-BIBLE-1013"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# 1) kartu blocked per tenant: alasan dari komentar terakhir + kind event terakhir
print("=== KARTU BLOCKED (33) ===")
rows = con.execute("SELECT id,title FROM tasks WHERE tenant=? AND status='blocked' ORDER BY id", (TN,)).fetchall()
reasons = {}
for r in rows:
    lastc = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    snippet = (lastc["body"][:90].replace("\n"," ") if lastc else "TANPA-KOMENTAR")
    key = snippet[:40]
    reasons.setdefault(key, []).append(r["id"])
    if len(reasons) <= 6 and sum(len(v) for v in reasons.values()) <= 12:
        print(f"{r['id']} ev={ev['kind'] if ev else '-'}@{(now-ev['created_at'])/60:.0f}m com[{lastc['author'] if lastc else '-'}]: {snippet}")
print("\n--- pengelompokan alasan (prefix 40 char) ---")
for k, v in sorted(reasons.items(), key=lambda x: -len(x[1])):
    print(f"[{len(v)}x] {k}")

# 2) watcher hidup? event unblocked per tenant + umur
ub = con.execute("SELECT COUNT(*) c, MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind='unblocked'", (TN,)).fetchone()
print(f"\nUNBLOCKED events tenant: count={ub['c']} umur_terakhir={'-' if not ub['m'] else f'{(now-ub[chr(109)])/60:.0f}mnt'}")

# 3) sensus gave_up/timed_out per kartu
gu = con.execute("SELECT e.kind, COUNT(DISTINCT e.task_id) c FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind IN ('timed_out','gave_up') GROUP BY e.kind", (TN,)).fetchall()
print("GAVE_UP/TIMED_OUT per kartu:", {g["kind"]: g["c"] for g in gu})

# 4) census ACK + marker pada kartu done
print("\n=== CENSUS DONE (46): ack & marker ===")
dones = con.execute("SELECT id,title FROM tasks WHERE tenant=? AND status='done' ORDER BY completed_at", (TN,)).fetchall()
noack = []
for d in dones:
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (d["id"],)).fetchone()["c"]
    mk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (d["id"],)).fetchone()["c"]
    if ack == 0:
        noack.append((d["id"], mk, (d["title"] or "")[:60]))
print(f"done={len(dones)} tanpa-ACK={len(noack)}")
for i,(tid,mk,tt) in enumerate(noack):
    print(f"  {tid} marker={mk} {tt}")

# 5) umur event terakhir per status (deteksi beku)
for st in ("blocked","todo","done","running"):
    m = con.execute("SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND t.status=?", (TN, st)).fetchone()["m"]
    print(f"status {st}: umur_event_terakhir={'-' if not m else f'{(now-m)/60:.0f}mnt'}")

# 6) komentar CHECKPOINT/CHECKPOINT-RESUME pada kartu blocked (rem yang ditawarkan worker)
cp = con.execute("SELECT c.task_id, c.author, c.body, c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant=? AND c.body LIKE '%CHECKPOINT%' ORDER BY c.created_at DESC LIMIT 5", (TN,)).fetchall()
print(f"\nKOMENTAR CHECKPOINT: {len(cp)} (terbaru:)")
for c in cp:
    print(f"  {c['task_id']} [{c['author']}] @{(now-c['created_at'])/60:.0f}m: {c['body'][:120].replace(chr(10),' ')}")

# 7) komentar terbaru di seluruh tenant (siapa bicara terakhir)
lc = con.execute("SELECT c.task_id, c.author, c.body, c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant=? ORDER BY c.created_at DESC LIMIT 6", (TN,)).fetchall()
print("\nKOMENTAR TERBARU TENANT:")
for c in lc:
    print(f"  {c['task_id']} [{c['author']}] @{(now-c['created_at'])/60:.0f}m: {c['body'][:140].replace(chr(10),' ')}")
con.close()
