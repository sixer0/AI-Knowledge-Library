#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ambil komentar lengkap kartu sampel + cek run ke-3 + sanity papan (read-only)."""
import os, sqlite3, time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
NOW = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

SAMPLES = ["t_0df60358", "t_674377e1", "t_d3cc135a", "t_050a75ff"]
print("=== FULL COMMENTS SAMPLES ===")
for tid in SAMPLES:
    print("\n#### %s ####" % tid)
    cs = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 2", (tid,)).fetchall()
    for c in cs:
        print("--[%s|%dm]--\n%s" % (c["author"], int((NOW - c["created_at"]) / 60), c["body"][:1400]))
    rs = con.execute("SELECT * FROM task_runs WHERE task_id=? ORDER BY id", (tid,)).fetchall()
    for r in rs:
        ea = r["ended_at"] if "ended_at" in r.keys() else None
        sa = r["started_at"] if "started_at" in r.keys() else None
        print("RUN", {k: (time.strftime("%H:%M", time.localtime(v)) if k.endswith(('_at','_ts')) and v else v) for k, v in dict(r).items()})

print("\n=== BOARD SANITY ===")
le = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
lc = con.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()["m"]
nt = con.execute("SELECT COUNT(*) c FROM tasks").fetchone()["c"]
print("last_event_age=%dm last_comment_age=%dm tasks=%d" % (int((NOW-le)/60), int((NOW-lc)/60), nt))
st = con.execute("SELECT status, COUNT(*) c FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status").fetchall()
print("open_by_status:", {r["status"]: r["c"] for r in st})
# tenants aktif (kartu non-done per tenant, top)
tn = con.execute("SELECT COALESCE(NULLIF(tenant,''),'(no-tenant)') tn, status, COUNT(*) c FROM tasks WHERE status NOT IN ('done','archived') GROUP BY tn, status ORDER BY c DESC LIMIT 15").fetchall()
for r in tn:
    print("TENANT %s | %s = %d" % (r["tn"], r["status"], r["c"]))
# aktivitas VIBE lain: event tenant ini dalam 60 mnt terakhir
v = con.execute("SELECT COUNT(*) c FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.created_at >= ?", (NOW-3600,)).fetchone()["c"]
print("VIBE events last 60m =", v)
# apakah ada run baru (ke-3) berjalan utk kartu writer?
run_open = con.execute("SELECT ru.task_id, ru.id, ru.started_at FROM task_runs ru JOIN tasks t ON t.id=ru.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND ru.outcome IS NULL OR (ru.task_id IN (SELECT task_id FROM task_runs WHERE outcome='timed_out') AND ru.ended_at IS NULL)").fetchall()
print("OPEN_RUNS_VIBE:", [(r["task_id"], r["id"], int((NOW-r["started_at"])/60)) for r in run_open])
con.close()
