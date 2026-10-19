# Ronde wake 15-10-e: isi komentar simpul blocked + CHECKPOINT + census ACK done + umur per kartu.
import sqlite3, time, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())

# 1) contoh komentar terakhir 3 kartu blocked + komentar gsp-master01 & dispatcher terbaru
print("== KOMENTAR SAMPEL SIMPUL BLOCKED ==")
for tid in ("t_e5e2e083", "t_d3cc135a", "t_64328060"):
    print("---", tid)
    t = cur.execute("SELECT title, status FROM tasks WHERE id=?", (tid,)).fetchone()
    print("   ", t["status"], "|", (t["title"] or "")[:70])
    for c in cur.execute("SELECT author, substr(body,1,300) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)):
        print("   [%s %dm] %s" % (c["author"], round((now - c["created_at"]) / 60), c["b"].replace("\n", " / ")))

# 2) komentar CHECKPOINT tenant ini
print("\n== CHECKPOINT ==")
n = 0
for c in cur.execute("""SELECT c.task_id, c.author, substr(c.body,1,200) b, c.created_at
                        FROM task_comments c JOIN tasks t ON t.id=c.task_id
                        WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%CHECKPOINT%'
                        ORDER BY c.created_at DESC LIMIT 5"""):
    n += 1
    print("  ", c["task_id"], c["author"], round((now - c["created_at"]) / 60), "m:", c["b"].replace("\n", " / "))
print("  count shown:", n)

# 3) sensus ACK kartu done tenant (RANTAI-ACK per kartu)
print("\n== CENSUS ACK DONE ==")
ackd = 0; noack = []
for t in cur.execute("SELECT id, title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchall():
    c2 = con.cursor()
    a = c2.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t["id"],)).fetchone()["n"]
    if a: ackd += 1
    else: noack.append(t["id"])
print("  done ter-ACK:", ackd, "| done tanpa ACK:", len(noack))

# 4) umur event terakhir PER KARTU blocked (sebar beku)
print("\n== UMUR EVENT TERAKHIR per kartu blocked ==")
ages = []
for t in cur.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'").fetchall():
    c2 = con.cursor()
    e = c2.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (t["id"],)).fetchone()
    cm = c2.execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id=?", (t["id"],)).fetchone()
    mx = max([x for x in (e["m"], cm["m"]) if x], default=None)
    if mx: ages.append((now - mx) / 60.0)
if ages:
    print("  min=%.0f max=%.0f median=%.0f (n=%d)" % (min(ages), max(ages), sorted(ages)[len(ages)//2], len(ages)))

# 5) papan lain yang hidup: event <=6 jam per tenant non-VBCB (konteks 'hanya satu misi macet')
print("\n== AKTIVITAS LAIN 6J ==")
cut = now - 6 * 3600
for r in cur.execute("""SELECT COALESCE(NULLIF(t.tenant,''),'(null)') tn, COUNT(DISTINCT t.id) n
                        FROM task_events e JOIN tasks t ON t.id=e.task_id
                        WHERE e.created_at>=? AND COALESCE(NULLIF(t.tenant,''),'')!='VIBE-BIBLE-1013'
                        GROUP BY tn ORDER BY n DESC LIMIT 10""", (cut,)):
    print("  ", r["tn"], r["n"])

# 6) status keseluruhan papan: kartu terbuka non-VBCB
print("\n== TERBUKA NON-VBCB ==")
for r in cur.execute("""SELECT t.status, COUNT(*) n FROM tasks t
                        WHERE COALESCE(t.tenant,'')!='VIBE-BIBLE-1013' AND t.status IN ('todo','blocked','running')
                        GROUP BY t.status"""):
    print("  ", r["status"], r["n"])
