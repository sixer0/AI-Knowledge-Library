#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ronde cron 11-11 (m): rekonsiliasi kandidat detail_v2 vs scan() kanonis + sapuan buta rute-4b.
import importlib.util
import os
import sqlite3
import time

LOCALAPPDATA = os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local")
DB = os.path.join(LOCALAPPDATA, "hermes", "kanban.db")
SCAN_PATH = os.path.join(LOCALAPPDATA, "hermes", "scripts", "gsp_mission_wake_scan.py")
CANDS = ["t_090415ec", "t_f4de0f1f", "t_5d087ab1", "t_e034cb5e", "t_df6a4a8a", "t_a707d4a3"]

spec = importlib.util.spec_from_file_location("wake_scan", SCAN_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
authors = [a.strip() for a in mod.DEFAULT_AUTHORS.split(",") if a.strip()]
findings = mod.scan(DB, now, authors)
print("== scan() kanonis: %d baris ==" % len(findings))
for f in findings:
    print("   WAKE", *f)

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("== rekonsiliasi kandidat detail_v2 ==")
for tid in CANDS:
    t = con.execute("SELECT id,title,status,tenant,assignee,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    lap = con.execute(
        "SELECT author,created_at,body FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' ORDER BY id DESC LIMIT 1",
        (tid,)).fetchone()
    acks = con.execute(
        "SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY id",
        (tid,)).fetchall()
    marker = con.execute(
        "SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'",
        (tid,)).fetchone()["n"]
    anchor = (lap["created_at"] if lap else t["completed_at"]) or 0
    # gerbang-1: ACK >= anchor
    ack_after = [a for a in acks if a["created_at"] >= anchor]
    lap_author = (lap["author"] if lap else "") or "~"
    lain = [a for a in ack_after if (a["author"] or "") != lap_author]
    reasons = []
    if marker:
        reasons.append("marker=%d" % marker)
    if not t["tenant"]:
        reasons.append("tenant-kosong(gerbang-4b)")
    if (t["assignee"] or "") in authors:
        reasons.append("assignee=controller")
    if not ack_after:
        reasons.append("ACK-nol-setelah-anchor")
    elif not lain:
        reasons.append("ACK-hanya-penulis-LAPOR")
    verdict = "BUTA" if any(r.startswith("tenant") for r in reasons) else ("bebas:" + ("ACK-lain" if lain else "?"))
    print("%s status=%s tenant=%r lap=%s@%s ack_total=%d ack>=anchor=%d ack_lain=%d -> %s | %s" % (
        tid, t["status"], t["tenant"], (lap["author"] if lap else "-"), anchor,
        len(acks), len(ack_after), len(lain), verdict, "; ".join(reasons) or "-"))

print("== sapuan buta rute-4b: event terminal <=6h TANPA syarat tenant ==")
rows = con.execute(
    "SELECT e.task_id AS id, MAX(e.created_at) AS ts, t.status AS st, t.tenant AS tenant, t.assignee AS asg "
    "FROM task_events e JOIN tasks t ON t.id=e.task_id "
    "WHERE e.kind IN ('completed','blocked') AND t.status IN ('done','review','blocked') AND e.created_at >= ? "
    "GROUP BY e.task_id HAVING ts >= ?", (now - 6 * 3600, mod.DONE_UNACKED_CUTOFF)).fetchall()
print("kandidat terminal 6h: %d" % len(rows))
for r in rows:
    lap = con.execute(
        "SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' ORDER BY id DESC LIMIT 1",
        (r["id"],)).fetchone()
    acks = con.execute(
        "SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchall()
    lap_author = (lap["author"] if lap else "") or "~"
    lain = [a["author"] for a in acks if (a["author"] or "") != lap_author]
    self_serve = bool(acks) and not lain
    marker = con.execute(
        "SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%' LIMIT 1",
        (r["id"],)).fetchone()
    age_min = int((now - r["ts"]) // 60)
    flag = "OK" if (lain or marker) else ("SELF-SERVE" if self_serve else "NO-ACK")
    gated = "" if (r["tenant"] and (r["asg"] or "") not in authors) else " [diblok gerbang]"
    print("%s st=%s age=%dm tenant=%r lap=%s ack=%d ack_lain=%d %s%s" % (
        r["id"], r["st"], age_min, r["tenant"], lap_author, len(acks), len(lain), flag, gated))
con.close()
