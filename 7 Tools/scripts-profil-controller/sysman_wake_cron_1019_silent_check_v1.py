"""Ronde wake 19-10: rekonsiliasi keadaan buta-titik yang sudah ternilai.

Ukur: (a) komentar papan terbaru (isi ringkas), (b) umur event terakhir per kartu
khususnya t_841f18dc (W7 gate-close beku) + jangkar t_66b1a0b2, (c) sensus ACK
kartu done tenant VIBE-BIBLE-1013 gelombang lama, (d) marker RANTAI-WAKE terbaru.
Read-only terhadap kanban.db root.
"""
import os
import sqlite3
import time

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())


def age(ts):
    return "-" if ts is None else f"{(now - int(ts)) / 60.0:.1f} mnt"


print("== KOMENTAR 8 TERBARU ==")
for r in cur.execute(
    "SELECT task_id, author, substr(replace(body, char(10), ' '),1,90) b, created_at"
    " FROM task_comments ORDER BY created_at DESC LIMIT 8"
):
    print(f"  {age(r['created_at'])} | {r['task_id']} | {r['author']} | {r['b']}")

print("== EVENT 8 TERBARU ==")
for r in cur.execute(
    "SELECT task_id, kind, created_at FROM task_events ORDER BY created_at DESC LIMIT 8"
):
    print(f"  {age(r['created_at'])} | {r['task_id']} | {r['kind']}")

print("== KARTU KUNCI ==")
ids = ["t_841f18dc", "t_66b1a0b2"]
for tid in ids:
    row = cur.execute(
        "SELECT id, status, tenant, created_at, completed_at FROM tasks WHERE id=?", (tid,)
    ).fetchone()
    if not row:
        print(f"  {tid}: TIDAK ADA")
        continue
    ev = cur.execute(
        "SELECT MAX(created_at) m, COUNT(*) c FROM task_events WHERE task_id=?", (tid,)
    ).fetchone()
    cm = cur.execute(
        "SELECT MAX(created_at) m, COUNT(*) c FROM task_comments WHERE task_id=?", (tid,)
    ).fetchone()
    print(
        f"  {tid} | {row['status']} | tenant={row['tenant']} | event_last={age(ev['m'])}"
        f" ev={ev['c']} | comment_last={age(cm['m'])} cm={cm['c']}"
    )

print("== SENSUS ACK DONE VIBE-BIBLE-1013 ==")
ids_done = [r["id"] for r in cur.execute(
    "SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'"
)]
acked = 0
marked = 0
for tid in ids_done:
    a = cur.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
        (tid,),
    ).fetchone()["c"]
    m = cur.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'",
        (tid,),
    ).fetchone()["c"]
    acked += 1 if a else 0
    marked += 1 if m else 0
print(f"  done={len(ids_done)} ber-ACK={acked} tanpa-ACK={len(ids_done)-acked} ber-marker-RANTAI-WAKE={marked}")

print("== MARKER RANTAI-WAKE 5 TERBARU ==")
for r in cur.execute(
    "SELECT task_id, substr(body,1,60) b, created_at FROM task_comments"
    " WHERE body LIKE '%RANTAI-WAKE%' ORDER BY created_at DESC LIMIT 5"
):
    print(f"  {age(r['created_at'])} | {r['task_id']} | {r['b']}")

con.close()
