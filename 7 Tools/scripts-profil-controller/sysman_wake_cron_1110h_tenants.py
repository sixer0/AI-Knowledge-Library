#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sensus tamat-senyap tingkat misi: tenant aktif <=24j, status per tenant, kartu done tanpa ACK."""
import os, sqlite3, time
DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
NOW = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
tenants = con.execute(
    "SELECT DISTINCT tenant FROM tasks WHERE tenant IS NOT NULL AND tenant != '' "
    "AND created_at >= ?", (NOW - 24 * 3600,)).fetchall()
print("tenant aktif <=24j =", [r["tenant"] for r in tenants])
for tr in tenants:
    tn = tr["tenant"]
    rows = con.execute("SELECT id,status,title FROM tasks WHERE tenant=?", (tn,)).fetchall()
    open_rows = [r for r in rows if r["status"] not in ("done", "archived")]
    print("\n[%s] total=%d terbuka=%d" % (tn, len(rows), len(open_rows)))
    for r in open_rows:
        print("   TERBUKA %s %s | %s" % (r["id"], r["status"], r["title"][:60]))
    if not open_rows:
        # semua selesai -> sensus ACK per kartu
        zero = []
        for r in rows:
            if r["status"] != "done":
                continue
            n = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
            if n == 0:
                zero.append(r["id"])
        print("   DONE tanpa ACK = %d dari %d: %s" % (len(zero), sum(1 for r in rows if r["status"] == "done"), zero[:12]))
con.close()
