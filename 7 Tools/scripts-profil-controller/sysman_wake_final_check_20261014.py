# -*- coding: utf-8 -*-
"""Verifikasi akhir pra-laporan: jumlah baris per kelas, kartu penulis vs verifier, ACK."""
import sqlite3, time
db = sqlite3.connect("C:/Users/TRIAL/AppData/Local/hermes/kanban.db"); db.row_factory = sqlite3.Row
NOW = int(time.time())
ids = [r["id"] for r in db.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013'")]
w = db.execute("SELECT COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' AND assignee='gsp-worker'").fetchone()["c"]
v = db.execute("SELECT COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo' AND assignee='gsp-thinker'").fetchone()["c"]
d = db.execute("SELECT COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchone()["c"]
print(f"tenant VBCB: total={len(ids)} penulis-blocked={w} verif-todo={v} done={d}")
ck = db.execute("""SELECT COUNT(DISTINCT task_id) c FROM task_comments WHERE body LIKE '%CHECKPOINT%'
   AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked')""").fetchone()["c"]
lap = db.execute("""SELECT COUNT(DISTINCT task_id) c FROM task_comments WHERE body LIKE '%LAPOR-SELE%'
   AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked')""").fetchone()["c"]
ack = db.execute("""SELECT COUNT(DISTINCT task_id) c FROM task_comments WHERE body LIKE '%RANTAI-ACK%'
   AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')""").fetchone()["c"]
print(f"komentar CHECKPOINT di kartu terkunci={ck}/34 | LAPOR-SELESAI={lap} | kartu ber-RANTAI-ACK={ack}")
cap = db.execute("SELECT DISTINCT max_runtime_seconds FROM task_runs WHERE task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked')").fetchall()
print("cap runtime kartu penulis:", [c[0] for c in cap])
err = db.execute("SELECT error FROM task_runs WHERE task_id='t_050a75ff' ORDER BY started_at DESC LIMIT 1").fetchone()
print("contoh error run:", err["error"])
age = db.execute("SELECT MIN(created_at) m FROM task_events WHERE kind='gave_up' AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')").fetchone()
print("event gave_up terakhir lama-kartu-menunggu: belum; gave_up TERAKHIR umur(mnt):", None)
last = db.execute("SELECT MAX(created_at) m FROM task_events WHERE kind='gave_up' AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')").fetchone()
print("gave_up terbaru berumur (mnt):", round((NOW-last["m"])/60))
