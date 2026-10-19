#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sensus read-only kartu terbuka non-WAKE (blocked/todo/scheduled) ronde 14-10."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")


def connect_ro(db_path):
    uri = "file:" + db_path.replace("\\", "/") + "?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA query_only = ON")
    return con


def main():
    now = int(time.time())
    con = connect_ro(DB)
    try:
        print("== KARTU TERBUKA blocked/todo/scheduled (umur event terakhir) ==")
        for r in con.execute("SELECT id, status, tenant, assignee, created_by, title FROM tasks "
                             "WHERE status IN ('blocked','todo','scheduled') ORDER BY status, created_at"):
            ev = con.execute("SELECT MAX(created_at) AS m FROM task_events WHERE task_id=?",
                             (r["id"],)).fetchone()["m"]
            ev = ev or 0
            ncom = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=?", (r["id"],)).fetchone()["n"]
            kids = con.execute("SELECT COUNT(*) AS n FROM task_links WHERE parent_id=?", (r["id"],)).fetchone()["n"]
            par = [p["parent_id"] for p in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (r["id"],))]
            parstat = []
            for p in par:
                ps = con.execute("SELECT status FROM tasks WHERE id=?", (p,)).fetchone()
                parstat.append("%s:%s" % (p[-6:], ps["status"] if ps else "?"))
            print("%s | %-9s | tenant=%s | assignee=%s | ev_age_min=%d | com=%d | kids=%d | parents=%s | %s" % (
                r["id"], r["status"], r["tenant"], r["assignee"], (now - ev) // 60, ncom, kids,
                ",".join(parstat) or "-", (r["title"] or "")[:64]))

        print("\n== BOBOT TURUNAN TRANSITIF dua kartu WAKE ==")
        for tid in ("t_6359bba5", "t_bb725705"):
            seen, stack = set(), [tid]
            while stack:
                cur = stack.pop()
                for c in con.execute("SELECT child_id FROM task_links WHERE parent_id=?", (cur,)):
                    if c["child_id"] not in seen:
                        seen.add(c["child_id"])
                        stack.append(c["child_id"])
            print("%s descendants=%d" % (tid, len(seen)))

        print("\n== GSF-22 (t_b8f35c42) penutup: ACK + LAPOR ==")
        for c in con.execute("SELECT author, created_at, substr(body,1,120) AS b FROM task_comments WHERE task_id='t_b8f35c42' ORDER BY created_at"):
            print("   [%s] age_h=%.1f :: %s" % (c["author"], (now - c["created_at"]) / 3600.0, c["b"].replace("\n", " ")))
    finally:
        con.close()


if __name__ == "__main__":
    main()
