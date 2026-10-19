#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 14-Oct pagi: baca komentar+event+run per kartu WAKE (read-only, argumen-driven).
Pola kanonis sysman_wake_eval_4cards_v1.py: DB = hermes/kanban.db ROOT, kolom task_links
= parent_id/child_id. Tidak memakai sysman_wake_read_v1 (daftar sampel tetap = buta-tutup)."""
import json
import os
import sqlite3
import sys
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
IDS = ["t_6359bba5", "t_66b1a0b2", "t_6c506604", "t_bb725705"]

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())


def age(ts):
    return round((now - ts) / 60.0, 1)


for tid in IDS:
    t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print("== %s: TIDAK ADA DI PAPAN" % tid)
        continue
    print("=" * 70)
    print("== %s | status=%s | tenant=%s | assignee=%s | created_by=%s" % (
        tid, t["status"], t["tenant"], t["assignee"], t["created_by"]))
    print("   title: %s" % (t["title"] or "")[:120])
    print("   created %s mnt | started %s | completed %s" % (
        age(t["created_at"]),
        (str(age(t["started_at"])) + " mnt") if t["started_at"] else "-",
        (str(age(t["completed_at"])) + " mnt") if t["completed_at"] else "-"))
    if t["result"]:
        print("   RESULT: %s" % (t["result"] or "").replace("\n", " ")[:600])
    # parents/children
    kids = [r["child_id"] for r in con.execute("SELECT child_id FROM task_links WHERE parent_id=?", (tid,))]
    pars = [r["parent_id"] for r in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))]
    print("   parents=%s children=%s" % (pars, kids))
    for cid in kids:
        c = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (cid,)).fetchone()
        print("     anak %s [%s] %s" % (c["id"], c["status"], (c["title"] or "")[:70]))
    evs = list(con.execute("SELECT kind,payload,created_at,run_id FROM task_events WHERE task_id=? ORDER BY created_at", (tid,)))
    print("   -- events (%d), 12 terakhir:" % len(evs))
    for e in evs[-12:]:
        pl = (e["payload"] or "")
        if len(pl) > 200:
            pl = pl[:200] + "..."
        print("     [%6.1f mnt] %-12s run=%s %s" % (age(e["created_at"]), e["kind"], e["run_id"], pl.replace("\n", " ")))
    cs = list(con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)))
    print("   -- comments (%d), 10 terakhir:" % len(cs))
    for c in cs[-10:]:
        print("     [%6.1f mnt] %s :: %s" % (age(c["created_at"]), c["author"], (c["body"] or "").replace("\n", " ")[:400]))
    runs = list(con.execute("SELECT id,profile,status,outcome,started_at,ended_at,substr(coalesce(summary,''),1,200) AS s FROM task_runs WHERE task_id=? ORDER BY id", (tid,)))
    print("   -- runs (%d):" % len(runs))
    for r in runs[-6:]:
        print("     run %s %s %s/%s start=%s end=%s :: %s" % (
            r["id"], r["profile"], r["status"], r["outcome"],
            (str(age(r["started_at"])) + "m") if r["started_at"] else "-",
            (str(age(r["ended_at"])) + "m") if r["ended_at"] else "-",
            (r["s"] or "").replace("\n", " ")))
print("=" * 70)
print("now_epoch=%d db=%s" % (now, DB))
