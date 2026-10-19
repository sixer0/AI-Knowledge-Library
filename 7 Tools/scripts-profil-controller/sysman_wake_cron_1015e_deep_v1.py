# Ronde wake 15-10-e: gali simpul orang-tua blocked VIBE-BIBLE-1013 + sensus tenant + blind spot.
import sqlite3, time, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())

# 1) sensus status tenant VIBE-BIBLE-1013
print("== SENSUS TENANT ==")
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status ORDER BY n DESC"):
    print(" ", r["status"], r["n"])
tot = cur.execute("SELECT COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchone()["n"]
print("  TOTAL:", tot)

# umur event terakhir per kartu tenant (deteksi beku)
r = cur.execute("""SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id
                   WHERE t.tenant='VIBE-BIBLE-1013'""").fetchone()
print("TENANT last event age_min:", round((now - r["m"]) / 60.0, 1) if r["m"] else None)

# 2) kartu blocked: alasan dari event 'blocked' payload + umur + komentar
print("\n== BLOCKED REASONS (gugus) ==")
groups = {}
for t in cur.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'").fetchall():
    c2 = con.cursor()
    ev = c2.execute("SELECT payload, created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (t["id"],)).fetchone()
    rs = ""
    if ev and ev["payload"]:
        try:
            p = json.loads(ev["payload"])
            rs = str(p.get("reason") or p.get("note") or ev["payload"])[:90]
        except Exception:
            rs = str(ev["payload"])[:90]
    groups.setdefault(rs.replace("\n", " | "), []).append(t["id"])
for rs, ids in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    print(" [%d] %s" % (len(ids), rs))
    print("     contoh:", ",".join(ids[:3]))

# umur event terakhir kartu blocked
r = cur.execute("""SELECT MIN(e.created_at) mn, MAX(e.created_at) mx FROM task_events e
                   JOIN tasks t ON t.id=e.task_id
                   WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked'""").fetchone()
if r["mn"]:
    print("blocked event age_min: min=%.0f max=%.0f" % ((now - r["mx"]) / 60.0, (now - r["mn"]) / 60.0))

# 3) gave_up / timed_out events tenant ini
print("\n== RUN EVENTS TENANT ==")
for r in cur.execute("""SELECT e.kind, COUNT(*) n, MAX(e.created_at) mx FROM task_events e
                        JOIN tasks t ON t.id=e.task_id
                        WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind IN ('timed_out','gave_up','unblocked','blocked','promoted','claimed')
                        GROUP BY e.kind"""):
    print(" ", r["kind"], r["n"], "last_age_min=", round((now - r["mx"]) / 60.0))

# 4) komentar controller pada kartu blocked (triase?) - hitung kartu blocked dgn >=1 komentar
r = cur.execute("""SELECT COUNT(DISTINCT c.task_id) n FROM task_comments c
                   JOIN tasks t ON t.id=c.task_id
                   WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked'""").fetchone()
print("\nblocked cards with >=1 comment:", r["n"])
for r in cur.execute("""SELECT c.author, COUNT(*) n FROM task_comments c
                        JOIN tasks t ON t.id=c.task_id
                        WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked'
                        GROUP BY c.author"""):
    print("  author:", r["author"], r["n"])

# 5) BLIND SPOT: kartu running di seluruh papan + LAPOR tanpa ACK
print("\n== BLIND SPOT running+LAPOR ==")
n_run = 0
for t in cur.execute("SELECT id, tenant, title, last_heartbeat_at, current_run_id FROM tasks WHERE status='running'").fetchall():
    n_run += 1
    c2 = con.cursor()
    lap = c2.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (t["id"],)).fetchone()["n"]
    c3 = con.cursor()
    ack = c3.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t["id"],)).fetchone()["n"]
    hb = round((now - (t["last_heartbeat_at"] or 0)) / 60.0) if t["last_heartbeat_at"] else None
    print(" ", t["id"], t["tenant"], "|", (t["title"] or "")[:60], "| hb_min=", hb, "lapor=", lap, "ack=", ack)
print("total running:", n_run)

# 6) done-unacked longgar (rekon rute-4b): done <=6 jam, LAPOR oleh penulis, tanpa RANTAI-ACK dari author lain, tanpa marker
print("\n== DONE-UNACKED longgar (6h) ==")
cut = now - 6 * 3600
for t in cur.execute("""SELECT id, tenant, title, completed_at, created_by FROM tasks
                        WHERE status='done' AND completed_at>=? ORDER BY completed_at DESC LIMIT 40""", (cut,)).fetchall():
    c2 = con.cursor()
    lap = c2.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%' ORDER BY created_at DESC LIMIT 1", (t["id"],)).fetchone()
    if not lap:
        continue
    c3 = con.cursor()
    acks = c3.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at", (t["id"],)).fetchall()
    other_ack = [a for a in acks if a["author"] != lap["author"]]
    c4 = con.cursor()
    mark = c4.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (t["id"],)).fetchone()["n"]
    if not other_ack:
        print("  CAND", t["id"], t["tenant"], "|", (t["title"] or "")[:50], "| lap_author=", lap["author"], "| ack_total=", len(acks), "| marker=", mark, "| done_age_min=", round((now - t["completed_at"]) / 60.0))
print("(selesai daftar kandidat)")
