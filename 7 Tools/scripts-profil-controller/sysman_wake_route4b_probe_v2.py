# -*- coding: utf-8 -*-
"""Probe rute-4b per-predikat utk id yang diargumenkan (argv), read-only.
Anti buta-tutup sysman_wake_explain_v1.py (daftar sampel tetap). Menjalankan
PREDIKAT KANONIS rute-4b satu per satu + memanggil scan() modul pemindai asli
 utk rekonsilasi replika-vs-kanonis (preseden 11-10: replika bukan vonis)."""
import importlib.util
import os
import sqlite3
import sys
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")
SCAN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "gsp_mission_wake_scan.py")

ids = sys.argv[1:]
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = time.time()

# baca konstanta kanonis dari sumber skrip
import re
src = open(SCAN, encoding="utf-8").read()
AUTHORS = [a.strip() for a in re.search(r'DEFAULT_AUTHORS\s*=\s*"([^"]+)"', src).group(1).split(",")]
WINDOW = int(re.search(r"DONE_UNACKED_WINDOW\s*=\s*(\d+)\s*\*\s*(\d+)", src).group(1)) * int(re.search(r"DONE_UNACKED_WINDOW\s*=\s*(\d+)\s*\*\s*(\d+)", src).group(2))
CUTOFF = int(re.search(r"DONE_UNACKED_CUTOFF\s*=\s*(\d+)", src).group(1))
MIN_AGE = int(re.search(r"DONE_UNACKED_MIN\s*=\s*(\d+)", src).group(1))
ph = ",".join("?" * len(AUTHORS))

for tid in ids:
    t = con.execute("SELECT id,title,status,tenant,assignee,created_by,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(f"{tid} TIDAK ADA"); continue
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=? AND kind IN ('completed','blocked')", (tid,)).fetchone()["m"]
    title = (t["title"] or "")[:58].replace("\n", " ")
    print(f"\n[{tid}] {title}")
    p = []
    p.append(("status-in", t["status"] in ("done", "review", "blocked"), t["status"]))
    p.append(("tenant-nonkosong", bool(t["tenant"]), repr(t["tenant"])))
    p.append(("assignee-bukan-controller", (t["assignee"] is None) or (t["assignee"] not in AUTHORS), repr(t["assignee"])))
    p.append(("ev-terminal-ada", ev is not None, f"age={(now - ev) / 60:.1f}m" if ev else "-"))
    if ev is not None:
        p.append(("ev>=now-window", ev >= now - WINDOW, f"{int((now - ev) // 60)}m lalu"))
        p.append(("ev>=cutoff", ev >= CUTOFF, str(ev)))
        p.append(("age>=MIN", (now - ev) // 60 >= MIN_AGE, ""))
    anchor = con.execute("SELECT MAX(created_at) a FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (tid,)).fetchone()["a"]
    lap_auth = con.execute("SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' ORDER BY id DESC LIMIT 1", (tid,)).fetchone()
    lap_auth = (lap_auth[0] if lap_auth else "") or "~"
    acks = con.execute("SELECT author,created_at,body FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchall()
    ack_after_anchor = any(a["created_at"] >= (anchor if anchor is not None else (ev or 0)) for a in acks)
    ack_other = any((a["author"] or "") != lap_auth for a in acks)
    p.append(("ack-setelah-anchor-TIDAK-ada", not ack_after_anchor, f"n_ack={len(acks)}"))
    p.append(("ack-author-lain-TIDAK-ada", not ack_other, f"lap_author={lap_auth}"))
    marker = con.execute("SELECT 1 x FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%' LIMIT 1", (tid,)).fetchone()
    p.append(("marker-dedup-TIDAK-ada", marker is None, ""))
    fails = [name for name, ok, _ in p if not ok]
    for name, ok, extra in p:
        print(f"   {'OK ' if ok else 'GATE'} {name} {extra}")
    print(f"   => {'LOLOS SEMUA PREDIKAT (seharusnya WAKE!)' if not fails else 'tergating oleh: ' + ', '.join(fails)}")
    for c in con.execute("SELECT author,created_at,body FROM task_comments WHERE task_id=? ORDER BY rowid DESC LIMIT 3", (tid,)):
        print(f"     c[{c['author']}] {int((now - float(c['created_at'])) / 60)}m: {c['body'][:90]}".replace("\n", " "))

# rekonsilasi kanonis: panggil scan() modul pemindai asli
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
findings = mod.scan(DB, int(now), AUTHORS)
print(f"\n=== KANONIS scan() now={int(now)} : {len(findings)} baris ===")
for f in findings:
    print("WAKE", *f)
con.close()
