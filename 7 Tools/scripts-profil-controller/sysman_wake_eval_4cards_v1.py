#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only: nilai butir done-unacked spesifik (ACK, turunan terbuka, keadaan misi)."""
import os
import sqlite3
import sys
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
IDS = ["t_6537fbe6", "t_885a4eb8", "t_91f3d6df", "t_bd122a56"]


def ro(path):
    con = sqlite3.connect("file:" + path.replace("\\", "/") + "?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA query_only = ON")
    return con


def mins(ts, now):
    return int((now - ts) // 60) if ts else -1


def main():
    now = int(time.time())
    con = ro(DB)
    print("DB=%s size=%d now=%d" % (DB, os.path.getsize(DB), now))
    print("schema tables:", [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")])
    for tid in IDS:
        t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        if t is None:
            print("\n### %s TIDAK ADA DI DB" % tid)
            continue
        keys = t.keys()
        print("\n" + "=" * 70)
        print("### %s | status=%s assignee=%s tenant=%s" % (
            tid, t["status"], t["assignee"], t["tenant"]))
        print("title: %s" % (t["title"][:110]))
        comp = t["completed_at"] if "completed_at" in keys else None
        print("completed_at=%s umur=%dm started=%s" % (comp, mins(comp, now), t["started_at"]))
        res = (t["result"] or "")
        print("result[0:300]: %s" % res[:300].replace("\n", " / "))
        # terminal events
        evs = con.execute(
            "SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY id", (tid,)).fetchall()
        print("events(%d): %s" % (len(evs), ", ".join("%s@%dm" % (e["kind"], mins(e["created_at"], now)) for e in evs[-8:])))
        # comments summary
        cs = con.execute(
            "SELECT id, author, created_at, body FROM task_comments WHERE task_id=? ORDER BY id", (tid,)).fetchall()
        lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
        acks = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
        wake = [c for c in cs if "RANTAI-WAKE" in (c["body"] or "")]
        print("comments=%d LAPOR=%s ACK=%s WAKE-marker=%s" % (
            len(cs),
            [(c["author"], mins(c["created_at"], now)) for c in lapor],
            [(c["author"], mins(c["created_at"], now)) for c in acks],
            [(c["author"], mins(c["created_at"], now)) for c in wake]))
        for c in cs[-4:]:
            print("  cmt[%s|%dm] %s" % (c["author"], mins(c["created_at"], now),
                                        (c["body"] or "").replace("\n", " ")[:220]))
        # links table discovery
        link_tbl = None
        for cand in ("task_links", "task_deps", "task_dependencies"):
            row = con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (cand,)).fetchone()
            if row:
                link_tbl = cand
                break
        if link_tbl:
            cols = [r[1] for r in con.execute("PRAGMA table_info(%s)" % link_tbl)]
            kids = con.execute(
                "SELECT * FROM %s WHERE %s=?" % (link_tbl, "parent_task_id" if "parent_task_id" in cols else cols[2]),
                (tid,)).fetchall() if len(cols) > 2 else []
            kid_ids = []
            for k in kids:
                kd = dict(k)
                kid_ids.append(kd.get("child_task_id") or kd.get("task_id"))
            print("link_tbl=%s child_ids=%s" % (link_tbl, kid_ids))
            open_kids = []
            for kid in [i for i in kid_ids if i]:
                kt = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (kid,)).fetchone()
                if kt and kt["status"] not in ("done", "archived"):
                    open_kids.append((kt["id"], kt["status"], kt["title"][:60]))
            print("TURUNAN LANGSUNG TERBUKA (%d): %s" % (len(open_kids), open_kids))
        # mission census
        cen = con.execute(
            "SELECT status, COUNT(*) n FROM tasks WHERE tenant=? GROUP BY status", (t["tenant"],)).fetchall()
        print("SENSUS TENANT %s: %s" % (t["tenant"], {r["status"]: r["n"] for r in cen}))
        lastev = con.execute(
            "SELECT MAX(e.created_at) ts FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=?",
            (t["tenant"],)).fetchone()[0]
        print("event terakhir misi: umur %dm" % mins(lastev, now))
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
