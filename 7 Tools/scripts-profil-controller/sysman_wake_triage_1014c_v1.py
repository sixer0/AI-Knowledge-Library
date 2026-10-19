#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Triase read-only ronde mission-wake 14-10 (sysman cron).

Menggabungkan baris WAKE per kartu (dedup kelas), lalu memperkaya dengan:
judul, status, tenant, created_by, assignee, umur event, orang tua + statusnya,
bobot turunan terbuka, jumlah LAPOR-SELESEI / RANTAI-ACK / marker RANTAI-WAKE,
cap runtime + outcome run. Output JSON siap agregasi per tenant.
"""
import json
import os
import sqlite3
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "wake_scan", os.path.join(HERE, "gsp_mission_wake_scan.py"))
ws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ws)

DB = ws.DEFAULT_DB
now = int(time.time())
authors = [a.strip() for a in ws.DEFAULT_AUTHORS.split(",") if a.strip()]

rows = ws.scan(DB, now, authors)
by_card = {}
for tid, alasan, umur in rows:
    by_card.setdefault(tid, []).append((alasan, umur))

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

def walk_desc(con, tid, seen=None, depth=0):
    """Turunan transitif (kolom kanonis: parent_id, child_id)."""
    if seen is None:
        seen = set()
    out = []
    for r in con.execute("SELECT child_id AS c FROM task_links WHERE parent_id=?", (tid,)):
        cid = r["c"]
        if cid in seen or depth > 6:
            continue
        seen.add(cid)
        out.append(cid)
        out.extend(walk_desc(con, cid, seen, depth + 1))
    return out

cards = []
for tid, classes in sorted(by_card.items()):
    t = con.execute(
        "SELECT id,title,status,tenant,created_by,assignee,created_at,completed_at,"
        "max_runtime_seconds FROM tasks WHERE id=?", (tid,)).fetchone()
    if t is None:
        continue
    last_ev = con.execute(
        "SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    parents = [r["p"] for r in con.execute(
        "SELECT parent_id AS p FROM task_links WHERE child_id=?", (tid,))]
    parent_info = []
    for p in parents:
        pr = con.execute("SELECT status,title FROM tasks WHERE id=?", (p,)).fetchone()
        parent_info.append({"id": p, "status": pr["status"] if pr else "?",
                            "title": (pr["title"][:70] if pr else "?")})
    desc = walk_desc(con, tid)
    open_desc = []
    for d in desc:
        dr = con.execute("SELECT status FROM tasks WHERE id=?", (d,)).fetchone()
        if dr and dr["status"] not in ("done", "archived"):
            open_desc.append(d)
    n_lap = con.execute(
        "SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'",
        (tid,)).fetchone()["n"]
    n_ack = con.execute(
        "SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
        (tid,)).fetchone()["n"]
    has_marker = con.execute(
        "SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%' LIMIT 1",
        (tid,)).fetchone() is not None
    runs = [dict(r) for r in con.execute(
        "SELECT outcome,started_at,ended_at,max_runtime_seconds,status,"
        "last_heartbeat_at,substr(COALESCE(error,''),1,200) err "
        "FROM task_runs WHERE task_id=? ORDER BY started_at DESC LIMIT 5", (tid,))]
    last_comment = con.execute(
        "SELECT author,substr(body,1,160) b,created_at FROM task_comments "
        "WHERE task_id=? ORDER BY id DESC LIMIT 1", (tid,)).fetchone()
    cards.append({
        "id": tid,
        "title": t["title"],
        "status": t["status"],
        "tenant": t["tenant"],
        "created_by": t["created_by"],
        "assignee": t["assignee"],
        "classes": sorted(set(c for c, _ in classes)),
        "age_min": max(u for _, u in classes),
        "last_ev_age_min": int((now - last_ev) // 60) if last_ev else None,
        "parents": parent_info,
        "open_desc_count": len(open_desc),
        "n_lapor": n_lap,
        "n_ack": n_ack,
        "has_wake_marker": has_marker,
        "cap_s": t["max_runtime_seconds"],
        "runs": runs,
        "last_comment": dict(last_comment) if last_comment else None,
    })

# Sanity papan (anti sehat-palsi DB mati)
sanity = {
    "status_census": {r["status"]: r["n"] for r in con.execute(
        "SELECT status, COUNT(*) n FROM tasks GROUP BY status")},
    "tasks_total": con.execute("SELECT COUNT(*) n FROM tasks").fetchone()["n"],
    "events_total": con.execute("SELECT COUNT(*) n FROM task_events").fetchone()["n"],
    "comments_total": con.execute("SELECT COUNT(*) n FROM task_comments").fetchone()["n"],
    "newest_event_age_min": int((now - con.execute(
        "SELECT MAX(created_at) m FROM task_events").fetchone()["m"]) // 60),
    "wake_lines": len(rows),
    "wake_cards": len(by_card),
}
print(json.dumps({"sanity": sanity, "cards": cards}, ensure_ascii=False, indent=1))
