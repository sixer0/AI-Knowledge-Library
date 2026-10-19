#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Triase read-only ronde mission-wake 14-10 (sysman cron).
Sensus temuan WAKE per kartu: status, tenant, judul, owner, assignee,
orang tua + statusnya, jumlah komentar controller/penanda, umur event terakhir.
DB dibuka ro; tidak menulis apa pun."""
import os, sqlite3, sys, time, json

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

# 1) parse stdin WAKE lines
findings = {}
for line in sys.stdin:
    parts = line.split()
    if len(parts) == 4 and parts[0] == "WAKE":
        tid, alasan, umur = parts[1], parts[2], int(parts[3])
        findings.setdefault(tid, []).append((alasan, umur))

print("=== SENSUS TEMUAN ===")
print("total_baris=%d total_kartu=%d" % (sum(len(v) for v in findings.values()), len(findings)))
by_class = {}
for tid, lst in findings.items():
    for a, u in lst:
        by_class.setdefault(a.split("-")[0] if a.startswith("run") else a, set()).add(tid)
for k, v in sorted(by_class.items()):
    print("kelas %s: %d kartu" % (k, len(v)))

# 2) per-card detail
print("\n=== DETAIL PER KARTU ===")
rows = []
for tid in sorted(findings):
    t = con.execute("SELECT id,title,status,tenant,created_by,assignee,created_at,completed_at,max_runtime_seconds FROM tasks WHERE id=?", (tid,)).fetchone()
    if t is None:
        rows.append({"id": tid, "missing": True}); continue
    last_ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    parents = con.execute("SELECT l.parent_id AS pid, s.status AS pstatus, s.title AS ptitle FROM task_links l JOIN tasks s ON s.id=l.parent_id WHERE l.child_id=?", (tid,)).fetchall()
    kids_open = con.execute("SELECT COUNT(*) c FROM task_links l JOIN tasks c ON c.id=l.child_id WHERE l.parent_id=? AND c.status NOT IN ('done','archived')", (tid,)).fetchone()["c"]
    n_ctrl = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND author IN ('default','sysmanager-cleaner','mission-wake')", (tid,)).fetchone()["c"]
    n_marker = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["c"]
    n_fase = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%[FASE]%'", (tid,)).fetchone()["c"]
    n_lapor = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (tid,)).fetchone()["c"]
    n_ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    runs_bad = con.execute("SELECT outcome, ended_at, started_at FROM task_runs WHERE task_id=? AND outcome IN ('crashed','timed_out','gave_up') ORDER BY COALESCE(ended_at,started_at) DESC LIMIT 3", (tid,)).fetchall()
    last_cmt = con.execute("SELECT author, substr(body,1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 1", (tid,)).fetchone()
    rows.append({
        "id": tid, "status": t["status"], "tenant": t["tenant"],
        "title": (t["title"] or "")[:70], "created_by": t["created_by"], "assignee": t["assignee"],
        "classes": [a for a, _ in findings[tid]], "age_max": max(u for _, u in findings[tid]),
        "last_ev_min": int((now - last_ev) // 60) if last_ev else None,
        "parents": [(p["pid"], p["pstatus"]) for p in parents],
        "kids_open": kids_open, "n_ctrl": n_ctrl, "n_marker": n_marker,
        "n_fase": n_fase, "n_lapor": n_lapor, "n_ack": n_ack,
        "bad_runs": [(r["outcome"], int((now - (r["ended_at"] or r["started_at"])) // 60)) for r in runs_bad],
        "max_rt": t["max_runtime_seconds"],
        "last_cmt": (last_cmt["author"], last_cmt["b"], int((now - last_cmt["created_at"]) // 60)) if last_cmt else None,
    })

# 3) group by tenant
tenants = {}
for r in rows:
    tenants.setdefault(r.get("tenant") or "(NULL)", []).append(r)
print("\n=== PER TENANT ===")
for tn, rs in sorted(tenants.items()):
    st = {}
    for r in rs:
        st[r["status"]] = st.get(r["status"], 0) + 1
    print("\nTENANT %s : %d kartu %s" % (tn, len(rs), json.dumps(st)))
    titles = {}
    for r in rs:
        titles.setdefault(r["title"][:40], 0)
        titles[r["title"][:40]] += 1
    for tt, c in sorted(titles.items(), key=lambda x: -x[1])[:6]:
        print("   x%d %s" % (c, tt))

with open(os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "scripts", "sysman_wake_triage_1014c.json"), "w") as f:
    json.dump(rows, f, indent=1, default=str)

# 4) print full detail compact
print("\n=== ROW DETAIL ===")
for r in rows:
    print(json.dumps(r, default=str))
