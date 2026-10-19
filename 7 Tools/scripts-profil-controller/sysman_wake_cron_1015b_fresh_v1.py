# Read-only: freshness per kartu tenant VIBE-BIBLE-1013, alasan blocked, aktivitas 24 jam terakhir, marker lama.
import sqlite3, time
from collections import Counter

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def mins(ts): return round((now - ts) / 60.0) if ts else None

# 1) umur event terakhir per status dalam tenant (id-list dulu, anti nested-cursor)
rows = con.execute("SELECT id,status,title FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchall()
by_status = {}
for r in rows:
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    by_status.setdefault(r["status"], []).append((r["id"], mins(ev)))
for st, lst in by_status.items():
    ages = [a for _, a in lst if a is not None]
    print(st, "n=", len(lst), "last-event-min min..max:", min(ages), "..", max(ages))

# 2) alasan blocked pada 33 orang tua blocked + cek komentar Digantikan/pengganti
print("\n== ORANG TUA BLOCKED: reason + komentar terakhir ==")
for r in rows:
    if r["status"] != "blocked": continue
    tsk = con.execute("SELECT * FROM tasks WHERE id=?", (r["id"],)).fetchone()
    reason = (tsk["blocked_reason"] or "")[:110] if "blocked_reason" in tsk.keys() else ""
    lc = con.execute("SELECT author, substr(body,1,100) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    print(r["id"], "|", (r["title"] or "")[:45], "|", reason.replace("\n"," "), "|", (lc["author"] + ": " + lc["b"].replace("\n"," ") + f" ({mins(lc['created_at'])}m)") if lc else "tanpa-komentar")

# 3) event tenant 24 jam terakhir per kind (apakah masih ada gerak / unblocked baru)
print("\n== EVENT TENANT 24 JAM TERAKHIR ==")
evs = con.execute("""SELECT e.kind, COUNT(*) c, MAX(e.created_at) mx
                     FROM task_events e JOIN tasks t ON t.id=e.task_id
                     WHERE t.tenant='VIBE-BIBLE-1013' AND e.created_at >= ?
                     GROUP BY e.kind ORDER BY mx DESC""", (now - 24*3600,)).fetchall()
for e in evs:
    print(e["kind"], e["c"], "terakhir", mins(e["mx"]), "mnt lalu")

# 4) unblocked terbaru: kapan pelepasan terakhir terjadi
ub = con.execute("""SELECT e.task_id, e.created_at FROM task_events e JOIN tasks t ON t.id=e.task_id
                    WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='unblocked' ORDER BY e.created_at DESC LIMIT 5""").fetchall()
print("\nunblocked terakhir:", [(u["task_id"], mins(u["created_at"])) for u in ub])

# 5) marker RANTAI-WAKE lama pada kartu done (anti dupel + bukti ronde sebelumnya)
mk = con.execute("""SELECT COUNT(DISTINCT c.task_id) c FROM task_comments c JOIN tasks t ON t.id=c.task_id
                    WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%RANTAI-WAKE done-unacked%'""").fetchone()["c"]
print("kartu done ber-marker RANTAI-WAKE sysman:", mk)

# 6) LAPOR-SELESAI vs ACK pada kartu done: apakah worker lapor & siapa penulisnya
lap = con.execute("""SELECT COUNT(DISTINCT c.task_id) c FROM task_comments c JOIN tasks t ON t.id=c.task_id
                     WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done' AND (c.body LIKE '%LAPOR-SELESAI%' OR c.body LIKE '%LAPOR-SELESEI%')""").fetchone()["c"]
print("kartu done ber-komentar LAPOR:", lap)

# 7) judul jangkar/blueprint tenant yang done tanpa komentar
nores = [r["id"] for r in rows if r["status"]=="done" and con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (r["id"],)).fetchone()["c"]==0]
print("done tanpa komentar sama sekali:", len(nores), nores[:10])
