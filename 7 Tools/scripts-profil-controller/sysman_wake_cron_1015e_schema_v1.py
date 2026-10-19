#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cek kolom tasks/task_events kanban.db root (read-only)."""
import os
import sqlite3

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
print("tasks:", [x[1] for x in con.execute("PRAGMA table_info(tasks)")])
print("task_events:", [x[1] for x in con.execute("PRAGMA table_info(task_events)")])
con.close()
