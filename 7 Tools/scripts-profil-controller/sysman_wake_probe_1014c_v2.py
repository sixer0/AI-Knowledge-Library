#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe lanjutan ronde 14-10 C (read-only):
A. Census penuh tenant VIBE-BIBLE-1013 (bukan hanya kartu WAKE) + riwayat run.
B. Loop masih membakar? umur run terakhir vs kini, jumlah run per kartu.
C. Artefak LOCK yang dilaporkan worker (hitung dari komentar CHECKPOINT/LAPOR).
D. Blind spot: kartu blocked/todo/scheduled DI LUAR tenant itu (kenapa tak WAKE).
"""
import json
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())
TEN = "VIBE-BIBLE-1013"

print("=== A. CENSUS TENANT %s ===" % TEN)
rows = list(con.execute(
    "SELECT id,title,status,assignee,created_at,completed_at,max_runtime_seconds,"
    "block_kind,substr(COALESCE(block_recurrences,'') ,1,40) br "
    "FROM tasks WHERE tenant=? ORDER BY status,id", (TEN,)))
print("total kartu tenant:", len(rows))
import collections
print("status:", dict(collections.Counter(r["status"] for r in rows)))
print("assignee:", dict(collections.Counter(str(r["assignee"]) for r in rows)))

print("\n=== B. RIWAYAT RUN kartu tenant ===")
agg = []
for r in rows:
    rs = list(con.execute(
        "SELECT outcome,status,started_at,ended_at,max_runtime_seconds FROM task_runs "
        "WHERE task_id=? ORDER BY started_at", (r["id"],)))
    if not rs:
        continue
    ends = [x["ended_at"] or x["started_at"] for x in rs if (x["ended_at"] or x["started_at"])]
    agg.append({
        "id": r["id"], "title": r["title"][:44], "status": r["status"],
        "n_runs": len(rs),
        "outcomes": ",".join(str(x["outcome"]) for x in rs),
        "last_run_end_age_min": int((now - max(ends)) // 60) if ends else None,
        "caps": sorted(set(x["max_runtime_seconds"] for x in rs)),
    })
print("kartu ber-run:", len(agg))
for a in sorted(agg, key=lambda x: x["last_run_end_age_min"]):
    print("  %s | %-8s | %-42s | nruns=%d | lastEnd=%dm | caps=%s | out=%s" % (
        a["id"], a["status"], a["title"], a["n_runs"],
        a["last_run_end_age_min"], a["caps"], a["outcomes"]))
print("\ndistribusi jumlah run/kartu:", dict(collections.Counter(a["n_runs"] for a in agg)))
print("distribusi outcome:", dict(collections.Counter(
    o for a in agg for o in a["outcomes"].split(","))))

print("\n=== C. JEJAK ARTEFAK/RESUME di komentar pekerja ===")
for r in rows:
    cs = list(con.execute(
        "SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY id", (r["id"],)))
    tags = []
    for c in cs:
        b = c["body"] or ""
        for tok in ("CHECKPOINT", "LAPOR-BERHALANSG", "LAPOR-SELESAI", "SISA_WOR_KERJA",
                    "LOCK", "TERMINAL GRACE"):
            if tok in b:
                tags.append(tok)
    if tags:
        print("  %s | %-8s | nCmt=%d | tags=%s" % (r["id"], r["status"], len(cs),
                                                  sorted(set(tags))))

print("\n=== D. KARTU TERBUKA DI LUAR TENANT (blind spot) ===")
others = list(con.execute(
    "SELECT id,title,status,tenant,created_by,assignee,block_kind,"
    "COALESCE((SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id),created_at) le "
    "FROM tasks t WHERE t.status IN ('blocked','todo','scheduled','review') "
    "AND (t.tenant IS NULL OR t.tenant != ?) ORDER BY t.status, t.id", (TEN,)))
print("jumlah:", len(others))
for o in others:
    age = int((now - o["le"]) // 60)
    nc = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=?", (o["id"],)).fetchone()["n"]
    lastc = con.execute("SELECT author,substr(body,1,110) b FROM task_comments WHERE task_id=? "
                        "ORDER BY id DESC LIMIT 1", (o["id"],)).fetchone()
    excl = con.execute("SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%PROF-MERGE-1010%' "
                       "LIMIT 1", (o["id"],)).fetchone()
    print("  %s | %-9s | age=%4dm | nCmt=%2d | tenant=%s | by=%s | asm=%s | bk=%s | mergeExempt=%d" % (
        o["id"], o["status"], age, nc, o["tenant"], o["created_by"], o["assignee"],
        o["block_kind"], int(excl is not None)))
    print("       title=%s" % (o["title"] or "")[:80])
    if lastc:
        print("       last[%s]=%s" % (lastc["author"], (lastc["b"] or "").replace("\n", " ")))
