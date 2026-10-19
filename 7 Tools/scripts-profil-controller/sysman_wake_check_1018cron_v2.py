# -*- coding: utf-8 -*-
"""Verifikasi artefak kontrak t_8358d01c di disk + keadaan t_841f18dc (butir ronde sebelumnya)."""
import sqlite3, time, os

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
WS = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace"

print("=== ARTEFAK KONTRAK t_8358d01c ===")
for rel in ("docs/2026-10-18_sys-net-rt-papan-1018/TRACEROOT.md",
            "docs/2026-10-18_sys-net-rt-papan-1018/system_change.md"):
    p = os.path.join(WS, rel.replace("/", os.sep))
    ok = os.path.isfile(p)
    print(f"  {'ADA' if ok else 'HILANG'} size={os.path.getsize(p) if ok else '-'} :: {rel}")

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts):
    return "-" if ts is None else f"{(NOW-int(ts))/60:.0f}m"

print("\n=== t_841f18dc (W7-GATECLOSE, butir ronde 17-10) ===")
r = con.execute("SELECT id,status,completed_at,assignee,tenant FROM tasks WHERE id='t_841f18dc'").fetchone()
if r:
    print(f"  status={r['status']} completed_umur={age(r['completed_at'])} assignee={r['assignee']} tenant={r['tenant']}")
ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id='t_841f18dc'").fetchone()["m"]
ck = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id='t_841f18dc' AND body LIKE '%RANTAI-ACK%'").fetchone()["n"]
last = con.execute("SELECT author,created_at,SUBSTR(body,1,120) b FROM task_comments WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 1").fetchone()
print(f"  event_terakhir umur={age(ev)} | RANTAI-ACK={ck}")
if last:
    print(f"  komentar terakhir [{age(last['created_at'])}] {last['author']}: {last['b']}")

print("\n=== sensus tenant SYNCNAS-1018P (misi kartu wake) ===")
for r in con.execute("SELECT id,title,status FROM tasks WHERE tenant='SYNCNAS-1018P'").fetchall():
    print(f"  {r['id']} {r['status']} :: {(r['title'] or '')[:80]}")
con.close()
