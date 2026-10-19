# -*- coding: utf-8 -*-
# Ronde cron 15-10 lanjutan: pelepasan blok, isi komentar blocked, census ACK done, running blindspot.
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts): return round((NOW - ts) / 60.0) if ts else None

print("== 1. EVENT unblocked VBCB 24 JAM TERAKHIR ==")
rows = con.execute("""SELECT e.task_id, e.created_at FROM task_events e JOIN tasks t ON t.id=e.task_id
  WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='unblocked' AND e.created_at > ? ORDER BY e.created_at DESC""", (NOW-86400,)).fetchall()
print("n_unblocked_24h=", len(rows))
for r in rows[:12]:
    print(" ", r["task_id"], age(r["created_at"]), "mnt lalu")

print("\n== 2. KARTU blocked VBCB: sebaran umur event terakhir ==")
rows = con.execute("""SELECT t.id, t.title, MAX(e.created_at) mx FROM tasks t LEFT JOIN task_events e ON e.task_id=t.id
  WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' GROUP BY t.id""").fetchall()
buckets = {}
for r in rows:
    a = age(r["mx"])
    b = "<30m" if a < 30 else ("30-120m" if a < 120 else (">120m"))
    buckets.setdefault(b, []).append((r["id"], a, (r["title"] or "")[:50]))
for k, v in sorted(buckets.items()):
    print(k, "n=", len(v))

print("\n== 3. KOMENTAR TERAKHIR 3 KARTU blocked M4 (contoh) ==")
for tid in ["t_a66ce30a", "t_ad5d8e6f", "t_b10a1e32"]:
    c = con.execute("SELECT author, created_at, substr(body,1,300) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    print(tid, "|", c["author"], "|", age(c["created_at"]), "mnt |", c["b"].replace("\n", " ") if c else "-")

print("\n== 4. CENSUS DONE VBCB: ack & marker ==")
rows = con.execute("""SELECT t.id, t.title, t.completed_at,
  (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%') ack,
  (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-WAKE done-unacked%') mark,
  (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%LAPOR%') lap
  FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done'""").fetchall()
noack = [(r["id"], age(r["completed_at"]), r["mark"], (r["title"] or "")[:45]) for r in rows if r["ack"] == 0]
print("done_total=", len(rows), " ack=0:", len(noack))
for x in noack: print("  ", x)

print("\n== 5. RUNNING VBCB SEMUA (blindspot): lap/ack/umur lap ==")
rows = con.execute("""SELECT t.id, t.title FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='running'""").fetchall()
for r in rows:
    hb = con.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=? AND kind='heartbeat'", (r["id"],)).fetchone()["mx"]
    lap = con.execute("SELECT author, created_at, substr(body,1,60) b FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%' ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    print(r["id"], "| hb", age(hb), "m | ack", ack, "| lap", (age(lap["created_at"]), lap["author"]) if lap else None, "|", (r["title"] or "")[:40])

print("\n== 6. SYNCNAS-1014M t_1a9ca5ce: komentar terakhir ==")
rows = con.execute("SELECT author, created_at, substr(body,1,200) b FROM task_comments WHERE task_id='t_1a9ca5ce' ORDER BY created_at DESC LIMIT 3").fetchall()
for r in rows: print(" ", r["author"], age(r["created_at"]), "m |", r["b"].replace("\n", " "))
