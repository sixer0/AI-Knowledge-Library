# Ronde wake 18-10b lanjutan: delta VBCB sejak vonis 17-10 + sensus ACK done + artefak W7.
import sqlite3, time, os, glob
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())

def age(ts):
    return round((now - ts) / 60.0, 1) if ts else None

# 1) event tenant VIBE-BIBLE-1013 sejak vonis 17-10 (epoch kemarin ~ now-86400)
since = now - 86400
n = cur.execute("""SELECT COUNT(*) c FROM task_events e JOIN tasks t ON t.id=e.task_id
                   WHERE t.tenant='VIBE-BIBLE-1013' AND e.created_at >= ?""", (since,)).fetchone()["c"]
ev = cur.execute("""SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id
                    WHERE t.tenant='VIBE-BIBLE-1013'""").fetchone()["m"]
print(f"VBCB events 24j terakhir = {n}; event terakhir tenant umur = {age(ev)}m")

# 2) sensus status tenant VBCB
for r in cur.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    print(f"  VBCB {r['status']} = {r['c']}")

# 3) sensus ACK kartu done VBCB (id-list dulu, hindari nested cursor)
ids = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchall()]
ack0 = 0
marked = 0
for i in ids:
    a = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (i,)).fetchone()["c"]
    if a == 0:
        ack0 += 1
    m = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (i,)).fetchone()["c"]
    if m:
        marked += 1
print(f"VBCB done={len(ids)} ack0={ack0} sudah_ber_marker_RANTAI_WAKE={marked}")

# 4) artefak W7 gate-close: bandingkan docx vs pdf di folder kontrak misi (cari pola)
ws = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace"
cands = []
for pat in ("docs/*vibe*/**/*.docx", "docs/*VIBE*/**/*.docx", "docs/*vibe*/**/*.pdf", "docs/*VIBE*/**/*.pdf"):
    cands += glob.glob(os.path.join(ws, pat), recursive=True)
seen = set()
for f in sorted(cands):
    if f.lower() in seen:
        continue
    seen.add(f.lower())
    st = os.stat(f)
    print(f"  {age(st.st_mtime):>8}m  {os.path.basename(f)[:70]}  ({st.st_size} B)")

# 5) komentar terakhir t_841f18dc (verifikasi isi vonis)
last = cur.execute("SELECT author,substr(body,1,160) b,created_at FROM task_comments WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 1").fetchone()
print(f"komentar terakhir t_841f18dc: author={last['author']} umur={age(last['created_at'])}m | {last['b'][:120]}")
