#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sanity read-only: umur event papan terbaru vs jam kini (anti DB basi saat stdout kosong)."""
import os, sqlite3, time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())
for tbl, col in (("task_events", "created_at"), ("task_comments", "created_at"), ("tasks", "created_at")):
    row = con.execute(f"SELECT MAX({col}) AS mx, COUNT(*) AS n FROM {tbl}").fetchone()
    mx = row["mx"] or 0
    print(f"{tbl}: rows={row['n']} max={mx} age_min={(now - mx) / 60:.1f}")
row = con.execute("SELECT COUNT(*) AS n FROM tasks WHERE status IN ('todo','blocked','review','running')").fetchone()
print("open_tasks =", row["n"])
print("now_epoch =", now)
