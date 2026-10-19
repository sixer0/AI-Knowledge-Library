# -*- coding: utf-8 -*-
"""Introspeksi payload komentar + cek checkpoint/LAPOR pada kartu penulis VIBE-BIBLE."""
import sqlite3, json, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
db = sqlite3.connect(DB); db.row_factory = sqlite3.Row

# 1) struktur payload mentah satu event commented
r = db.execute("SELECT * FROM task_events WHERE kind='commented' AND task_id='t_050a75ff' ORDER BY created_at").fetchall()
print("== RAW commented t_050a75ff ==")
for x in r:
    print(x["created_at"], "|", (x["payload"] or "")[:600])
print()

# 2) semua kartu penulis blocked: komentar apa adanya (potong 300 char)
ids = [row["id"] for row in db.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' ORDER BY id")]
print("blocked penulis:", len(ids))
has_ck = has_lap = 0
sample_printed = 0
for tid in ids:
    cs = db.execute("SELECT created_at,payload FROM task_events WHERE task_id=? AND kind='commented' ORDER BY created_at", (tid,)).fetchall()
    txts = []
    for c in cs:
        try: p = json.loads(c["payload"])
        except Exception: p = {}
        body = p.get("body") or p.get("text") or p.get("comment") or ""
        author = p.get("author") or p.get("created_by") or "?"
        txts.append((author, body))
    joined = " ".join(b for _, b in txts).upper()
    if "CHECKPOINT" in joined: has_ck += 1
    if "LAPOR-SELE" in joined: has_lap += 1
    if sample_printed < 3:
        print(f"-- {tid}")
        for a, b in txts:
            print("   ", a, "::", b[:300].replace("\n", " | "))
        sample_printed += 1
print("kartu penulis dgn komentar CHECKPOINT:", has_ck, "| dgn LAPOR-SELESAI:", has_lap)
print()

# 3) kartu jangkar/kontroller tenant ini (status lain, mis. running/done) di luar 68 wake
others = db.execute("""SELECT id,title,status,assignee FROM tasks WHERE tenant='VIBE-BIBLE-1013'
  AND status NOT IN ('todo','blocked')""").fetchall()
print("== kartu non-todo/blocked tenant ini ==")
for o in others:
    print(o["id"], o["status"], o["assignee"], "|", o["title"][:80])

# 4) sensus seluruh tenant VIBE-BIBLE-1013
cnt = db.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status").fetchall()
print("== sensus status tenant ==", {c['status']: c['c'] for c in cnt})
tot = db.execute("SELECT COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchone()["c"]
print("total kartu tenant:", tot)
