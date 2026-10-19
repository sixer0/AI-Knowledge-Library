#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rekonsiliasi ronde cron 11-10 h: kandidat longgar detail_v2 vs vonis scan() kanonis,
plus sapuan buta-tutup terminal-event <=6j TANPA syarat tenant, plus kesegaran papan."""
import importlib.util, os, sqlite3, time, sys

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
NOW = int(time.time())

spec = importlib.util.spec_from_file_location(
    "wake_scan", os.path.join(SCRIPTS, "gsp_mission_wake_scan.py"))
ws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ws)

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("== A. vonis kanonis scan() ==")
findings = ws.scan(DB, NOW, ws.DEFAULT_AUTHORS.split(","))
print("baris WAKE =", len(findings), findings if findings else "")

print("\n== B. rekonsiliasi kandidat longgar (detail_v2 WAKE=1) ==")
cands = ["t_090415ec", "t_f4de0f1f", "t_5d087ab1", "t_e034cb5e", "t_df6a4a8a", "t_a707d4a3"]
for tid in cands:
    t = con.execute("SELECT id,status,tenant,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    ts = con.execute("SELECT MAX(created_at) ts FROM task_events WHERE task_id=? AND kind IN ('completed','blocked')", (tid,)).fetchone()["ts"]
    age_min = int((NOW - ts) // 60) if ts else -1
    in_window = 0 <= age_min <= ws.DONE_UNACKED_WINDOW // 60
    marker = con.execute("SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%' LIMIT 1", (tid,)).fetchone()
    lap = con.execute("SELECT author, MAX(created_at) ts FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (tid,)).fetchone()
    acks = con.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at", (tid,)).fetchall()
    print("%s status=%s tenant=%r assignee=%r done_age=%dm in_window6h=%s marker=%s lap_author=%r ack_authors=%s" % (
        tid, t["status"], t["tenant"], t["assignee"], age_min, in_window, bool(marker),
        lap["author"] if lap else None, [a["author"] for a in acks]))

print("\n== C. buta-tutup: terminal event <=6j TANPA syarat tenant ==")
rows = con.execute(
    "SELECT e.task_id id, MAX(e.created_at) ts, t.status, t.tenant, t.assignee "
    "FROM task_events e JOIN tasks t ON t.id=e.task_id "
    "WHERE e.kind IN ('completed','blocked') AND e.created_at >= ? "
    "GROUP BY e.task_id", (NOW - 6 * 3600,)).fetchall()
print("terminal event <=6j =", len(rows))
for r in rows:
    anchor = con.execute("SELECT MAX(created_at) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()[0]
    anchor = anchor if anchor is not None else r["ts"]
    acks = con.execute("SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' AND created_at >= ?", (r["id"], anchor)).fetchall()
    lap_author = con.execute("SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
    la = (lap_author[0] if lap_author else "") or "~"
    other_ack = any((a["author"] or "") != la for a in acks)
    print("%s status=%s tenant=%r ack_setelah_anchor=%d lain_author=%s" % (
        r["id"], r["status"], r["tenant"], len(acks), other_ack))

print("\n== D. kesegaran papan ==")
for tbl, col in [("task_events", "created_at"), ("task_comments", "created_at"), ("task_runs", "COALESCE(ended_at,started_at)")]:
    v = con.execute("SELECT MAX(%s) m, COUNT(*) n FROM %s" % (col, tbl)).fetchone()
    print("%s: n=%d umur_event_terakhir=%.1f mnt" % (tbl, v["n"], (NOW - v["m"]) / 60.0))
st = con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status").fetchall()
print("status:", {r["status"]: r["n"] for r in st})
con.close()
