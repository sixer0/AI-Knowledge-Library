#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 14-10c final: komentar sysman sebelumnya + event global terbaru + konfirmasi re-scan."""
import os, sqlite3, time, importlib.util, sys

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("=== M. 12 KOMENTAR gsp-system-manager di tenant (ronde wake sebelumnya?) ===")
for r in con.execute("SELECT c.task_id tid, substr(c.body,1,140) b, c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND c.author='gsp-system-manager' ORDER BY c.id DESC LIMIT 12"):
    print("  [%dmn] %s | %s" % (int((now - r["created_at"]) // 60), r["tid"], r["b"].replace("\n", " ")[:130]))

print("\n=== N. EVENT GLOBAL TERBARU (di luar tenant VIBE) ===")
for r in con.execute("SELECT e.task_id tid, e.kind, e.created_at, t.tenant, t.status, substr(t.title,1,40) ti FROM task_events e JOIN tasks t ON t.id=e.task_id ORDER BY e.id DESC LIMIT 8"):
    print("  [%dmn] %s %s | tenant=%s status=%s | %s" % (int((now - r["created_at"]) // 60), r["tid"], r["kind"], r["tenant"], r["status"], r["ti"]))

print("\n=== O. RE-SCAN KANONIS scan() (vonis akhir) ===")
spec = importlib.util.spec_from_file_location("ws", os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "scripts", "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = mod.DEFAULT_AUTHORS.split(",")
f = mod.scan(DB, int(time.time()), authors)
from collections import Counter
cc = Counter(a for _, a, _ in f)
print("re-scan baris=%d kelas=%s" % (len(f), dict(cc)))
ids_run = sorted({tid for tid, a, _ in f if a.startswith("run")})
print("kartu run=%d ; kartu stalled saja=%d" % (len(ids_run), len({tid for tid, a, _ in f if a == 'stalled'}) - len(ids_run)))
