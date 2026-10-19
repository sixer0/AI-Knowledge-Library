#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sensus tenant VIBE-BIBLE-1013 + status loop retry + blind spot running (ronde 14-10c)."""
import os, sqlite3, time, json

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("=== A. SENSUS TENAN VIBE-BIBLE-1013 (semua kartu) ===")
tot = {}
for r in con.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    tot[r["status"]] = r["c"]
print(json.dumps(tot))
print("kartu jangkar ber-tenant NULL dgn judul mirip VIBE/VBCB:")
for r in con.execute("SELECT id,status,title,created_by FROM tasks WHERE (tenant IS NULL OR tenant='') AND (title LIKE '%VIBE%' OR title LIKE '%VBCB%')"):
    print("  ", dict(r))

print("\n=== B. LOOP RETRY: run per kartu penulis (blocked) ===")
# ambil semua run 8 jam terakhir utk tenant ini
q = ("SELECT ru.task_id tid, ru.outcome, ru.status rstatus, ru.started_at, ru.ended_at, ru.max_runtime_seconds mx, ru.last_heartbeat_at hb, substr(ru.metadata,1,200) md "
     "FROM task_runs ru JOIN tasks t ON t.id=ru.task_id "
     "WHERE t.tenant='VIBE-BIBLE-1013' AND COALESCE(ru.ended_at,ru.started_at) >= ? "
     "ORDER BY COALESCE(ru.ended_at,ru.started_at) DESC")
runs = con.execute(q, (now - 8*3600,)).fetchall()
print("total_run_8jam=%d" % len(runs))
# run paling baru secara global
for r in runs[:6]:
    print("  terbaru: %s %s/%s umur=%dmn cap=%s hb_umur=%s" % (r["tid"], r["rstatus"], r["outcome"],
          int((now - (r["ended_at"] or r["started_at"])) // 60), r["mx"],
          int((now - r["hb"]) // 60) if r["hb"] else None))
# run yang masih active/running sekarang?
act = [r for r in runs if (r["rstatus"] or "") in ("active", "running", "in_progress") or r["ended_at"] is None]
print("run_aktif_sekarang=%d" % len(act))
for r in act[:10]:
    print("  AKTIF: %s started_umur=%dmn outcome=%s meta=%s" % (r["tid"], int((now - r["started_at"]) // 60), r["outcome"], (r["md"] or "")[:120]))
# distribusi outcome
dist = {}
for r in runs:
    dist[(r["rstatus"], r["outcome"])] = dist.get((r["rstatus"], r["outcome"]), 0) + 1
print("distribusi (rstatus,outcome):", json.dumps({str(k): v for k, v in dist.items()}))
# retry_status kolom?
cols = [c[1] for c in con.execute("PRAGMA table_info(task_runs)")]
print("kolom task_runs:", cols)
if "retry_status" in cols:
    rs = {}
    for r in con.execute("SELECT ru.retry_status x, COUNT(*) c FROM task_runs ru JOIN tasks t ON t.id=ru.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND COALESCE(ru.ended_at,ru.started_at)>=? GROUP BY ru.retry_status", (now - 8*3600,)):
        rs[r["x"]] = r["c"]
    print("retry_status:", json.dumps({str(k): v for k, v in rs.items()}))

print("\n=== C. BLIND SPOT: kartu running di seluruh papan ===")
for r in con.execute("SELECT t.id, t.title, t.tenant, t.assignee, "
                     "COALESCE((SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id),t.created_at) le "
                     "FROM tasks t WHERE t.status='running' ORDER BY le DESC LIMIT 30"):
    lap = con.execute("SELECT COUNT(*) c, MAX(created_at) mx FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()
    hb = con.execute("SELECT COUNT(*) c FROM task_events WHERE task_id=? AND kind='heartbeat'", (r["id"],)).fetchone()
    print("  %s | %s | tenant=%s | ev_umur=%dmn | LAPOR=%d ACK=%d HB=%d | %s" % (
        r["id"], (r["title"] or "")[:45], r["tenant"], int((now - r["le"]) // 60),
        lap["c"], ack["c"], hb["c"], "BLIND?" if lap["c"] and not ack["c"] else ""))

print("\n=== D. SANITAS PAPAN (anti DB basi) ===")
ev = con.execute("SELECT COUNT(*) c, MAX(created_at) m FROM task_events").fetchone()
tk = con.execute("SELECT COUNT(*) c FROM tasks").fetchone()
cm = con.execute("SELECT COUNT(*) c FROM task_comments").fetchone()
print("tasks=%d comments=%d events=%d event_terbaru_umur_menit=%d" % (
    tk["c"], cm["c"], ev["c"], int((now - ev["m"]) // 60)))

print("\n=== E. PROGRES ARTEFAK: komentar worker terbaru per kartu penulis (sample 6) ===")
for r in con.execute("SELECT t.id, t.title FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' ORDER BY t.id LIMIT 6"):
    cmts = con.execute("SELECT author, substr(body,1,160) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 2", (r["id"],)).fetchall()
    print("  %s %s" % (r["id"], (r["title"] or "")[:40]))
    for c in cmts:
        print("     [%s|%dmn] %s" % (c["author"], int((now - c["created_at"]) // 60), c["b"].replace("\n", " ")[:150]))
