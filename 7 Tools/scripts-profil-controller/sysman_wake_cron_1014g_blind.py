#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sapuan blind ronde 14-10g (read-only): blocked non-VBCB, aktivitas loop timeout, event hangat."""
import os, sqlite3, time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
NOW = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("=== BLOCKED NON-VBCB (di luar 34 penulis) ===")
rows = con.execute("""SELECT id,title,status,tenant,created_by,assignee FROM tasks
    WHERE status='blocked' AND (tenant IS NULL OR tenant != 'VIBE-BIBLE-1013')""").fetchall()
for r in rows:
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    lc = con.execute("SELECT author, substr(replace(body,char(10),' '),1,120) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
    print("%s | tenant=%s | by=%s | evAge=%dm" % (r["id"], r["tenant"], r["created_by"], int((NOW-ev)/60) if ev else -1))
    print("   T: %s" % (r["title"][:100] if r["title"] else ""))
    if lc:
        print("   LASTCOM [%s %dm]: %s" % (lc["author"], int((NOW-lc["created_at"])/60), lc["b"]))

print("\n=== AKTIVITAS LOOP TIMEOUT VBCB (event < 60m terakhir pada kartu VBCB) ===")
hot = con.execute("""SELECT e.task_id, e.kind, e.created_at FROM task_events e JOIN tasks t ON t.id=e.task_id
    WHERE t.tenant='VIBE-BIBLE-1013' AND e.created_at > ? ORDER BY e.created_at DESC LIMIT 20""", (NOW-3600,)).fetchall()
if not hot:
    print("(tidak ada event VBCB dalam 60 menit terakhir)")
for h in hot:
    print("%s | %s | age%dm" % (h["task_id"], h["kind"], int((NOW-h["created_at"])/60)))

print("\n=== RUN VBCB: jumlah run per outcome + run terbaru ===")
rs = con.execute("""SELECT r.outcome, COUNT(*) c, MAX(COALESCE(r.ended_at,r.started_at)) mx
    FROM task_runs r JOIN tasks t ON t.id=r.task_id WHERE t.tenant='VIBE-BIBLE-1013'
    GROUP BY r.outcome""").fetchall()
for r in rs:
    print("%s = %d (run terakhir umur %dm)" % (r["outcome"], r["c"], int((NOW-r["mx"])/60) if r["mx"] else -1))

print("\n=== EVENT TERAKHIR BOARD (top 10) ===")
for e in con.execute("SELECT task_id,kind,created_at FROM task_events ORDER BY created_at DESC LIMIT 10").fetchall():
    t = con.execute("SELECT title,status,tenant FROM tasks WHERE id=?", (e["task_id"],)).fetchone()
    print("%s | %s | age%dm | %s | %s" % (e["task_id"], e["kind"], int((NOW-e["created_at"])/60), (t["status"] if t else "?"), (t["title"][:70] if t and t["title"] else "")))

print("\n=== DONE VBCB (11 kartu) - ACK check ===")
for d in con.execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchall():
    nack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (d["id"],)).fetchone()["c"]
    nlap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (d["id"],)).fetchone()["c"]
    print("%s | ACK=%d LAPOR=%d | %s" % (d["id"], nack, nlap, d["title"][:70]))
con.close()
