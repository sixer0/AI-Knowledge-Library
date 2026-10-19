# -*- coding: utf-8 -*-
# Ronde wake 15-10b lanjutan: vonis tingkat-misi VIBE-BIBLE-1013.
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
TEN = "VIBE-BIBLE-1013"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

# 1. orang tua blocked: alasan + komentar CHECKPOINT?
print("=== ORANG TUA BLOCKED (33) ===")
bl = con.execute("SELECT id, title, reason FROM tasks WHERE tenant=? AND status='blocked' ORDER BY title", (TEN,)).fetchall() if "reason" in [c[1] for c in con.execute("PRAGMA table_info(tasks)")] else None
if bl is None:
    bl = con.execute("SELECT id, title FROM tasks WHERE tenant=? AND status='blocked' ORDER BY title", (TEN,)).fetchall()
for x in bl:
    ev = con.execute("SELECT payload, created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (x["id"],)).fetchone()
    reason = (ev["payload"] if ev else "") or ""
    reason = reason.replace("\n", " ")[:110]
    nckpt = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%CHECKPOINT%'", (x["id"],)).fetchone()["c"]
    nlap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (x["id"],)).fetchone()["c"]
    nack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (x["id"],)).fetchone()["c"]
    print("%s | %s | ckpt=%d lap=%d ack=%d | %s" % (x["id"], (x["title"] or "")[:44], nckpt, nlap, nack, reason))

# 2. sensus ACK kartu done
print("\n=== DONE ACK CENSUS ===")
dn = con.execute("SELECT id, title, completed_at FROM tasks WHERE tenant=? AND status='done' ORDER BY completed_at", (TEN,)).fetchall()
noack = []
for x in dn:
    nack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (x["id"],)).fetchone()["c"]
    nmk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (x["id"],)).fetchone()["c"]
    if nack == 0:
        noack.append((x["id"], (x["title"] or "")[:44], nmk, (NOW - x["completed_at"])/60.0 if x["completed_at"] else -1))
print("done=%d tanpa-ACK=%d" % (len(dn), len(noack)))
for i in noack:
    print("  NOACK %s | %s | marker=%d | umur_done=%.0fm" % (i[0], i[1], i[2], i[3]))

# 3. pola pelepasan watcher: umur tiap event unblocked
print("\n=== UNBLOCKED TIMELINE ===")
ub = con.execute("SELECT e.task_id, e.created_at FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind='unblocked' ORDER BY e.created_at", (TEN,)).fetchall()
for u in ub:
    print("  unblock %s @%.0fm lalu" % (u["task_id"], (NOW-u["created_at"])/60.0))

# 4. 12 event terakhir tenant
print("\n=== 12 EVENT TERAKHIR TENANT ===")
ev = con.execute("SELECT e.task_id, e.kind, e.created_at FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? ORDER BY e.created_at DESC LIMIT 12", (TEN,)).fetchall()
for e in ev:
    print("  %s %s @%.0fm" % (e["kind"], e["task_id"], (NOW-e["created_at"])/60.0))

# 5. sampel komentar CHECKPOINT terbaru dari satu orang tua (rem yang ditawarkan worker)
print("\n=== CHECKPOINT TERBARU (sampel) ===")
cc = con.execute("SELECT c.task_id, c.body, c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant=? AND c.body LIKE '%CHECKPOINT%' ORDER BY c.created_at DESC LIMIT 2", (TEN,)).fetchall()
for c in cc:
    print("--- %s @%.0fm ---\n%s" % (c["task_id"], (NOW-c["created_at"])/60.0, c["body"][:900]))
con.close()
