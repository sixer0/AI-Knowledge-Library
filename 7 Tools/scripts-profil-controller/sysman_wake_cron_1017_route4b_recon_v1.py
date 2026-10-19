#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rekonsiliasi kandidat longgar rute-4b vs gerbang scan() kanonis (ronde 17-10)."""
import os
import sqlite3
import time

HOME = os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local")
DB = os.path.join(HOME, "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())
AUTHORS = ["default", "sysmanager-cleaner", "mission-wake"]

cand = con.execute(
    "SELECT e.task_id id, MAX(e.created_at) ts FROM task_events e JOIN tasks t ON t.id=e.task_id "
    "WHERE e.kind IN ('completed','blocked') AND t.status IN ('done','review','blocked') "
    "AND e.created_at >= ? GROUP BY e.task_id", (now - 6 * 3600,)).fetchall()

for r in cand:
    tid = r["id"]
    t = con.execute("SELECT id,title,status,tenant,assignee,created_by FROM tasks WHERE id=?", (tid,)).fetchone()
    print("CANDIDATE %s status=%s tenant=%r assignee=%r created_by=%r" % (
        tid, t["status"], t["tenant"], t["assignee"], t["created_by"]))
    print("  title:", (t["title"] or "")[:120])
    reasons = []
    if not (t["tenant"] or ""):
        reasons.append("gerbang tenant: tenant kosong -> rute-4b mustahil")
    if (t["assignee"] or "") in AUTHORS:
        reasons.append("assignee di daftar controller -> dikecualikan")
    lap = con.execute(
        "SELECT author, MAX(created_at) ts FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'",
        (tid,)).fetchone()
    anchor = lap["ts"] if lap and lap["ts"] else r["ts"]
    acks = con.execute(
        "SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at",
        (tid,)).fetchall()
    lap_author = (lap["author"] or "~") if lap and lap["ts"] else "~"
    print("  anchor=%s lap_author=%s acks=%s" % (
        time.strftime("%H:%M", time.localtime(anchor)), lap_author,
        [(a["author"], time.strftime("%H:%M", time.localtime(a["created_at"]))) for a in acks]))
    if any((a["author"] or "") != lap_author for a in acks):
        reasons.append("ACK sah dari author lain (exempsi rute-4b)")
    mk = con.execute(
        "SELECT body, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE %' ORDER BY created_at DESC LIMIT 1",
        (tid,)).fetchone()
    if mk:
        reasons.append("marker anti-ulang sudah ada: %r @%s" % (
            mk["body"][:60], time.strftime("%m-%d %H:%M", time.localtime(mk["created_at"]))))
    res = con.execute("SELECT result FROM tasks WHERE id=?", (tid,)).fetchone()
    print("  result:", ((res["result"] or "")[:300]) if res else "")
    cm = con.execute(
        "SELECT author, substr(body,1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 5",
        (tid,)).fetchall()
    for c in cm:
        print("  cmt[%s @%s] %s" % (c["author"], time.strftime("%m-%d %H:%M", time.localtime(c["created_at"])), c["b"].replace("\n", " | ")))
    print("  REKONSILIASI:", "; ".join(reasons) if reasons else ">>> BUTA-TUTUP: lolos semua gerbang tapi scan() nol <<<")
con.close()
