# Census kartu blocked + cek kontradiksi catatan-vs-papan + blind spot tenant-kosong (read-only)
import sqlite3, os, json, time, re

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = time.time()

def age_min(ts):
    return (now - float(ts)) / 60.0 if ts else None

print("== KARTU BLOCKED ==")
rows = con.execute("SELECT id,title,status,tenant,assignee,created_by,created_at,completed_at,last_heartbeat_at FROM tasks WHERE status='blocked' ORDER BY created_at DESC").fetchall()
for r in rows:
    print(f"- {r['id']} | {r['title'][:70]} | tenant={r['tenant']!r} | assignee={r['assignee']!r} | by={r['created_by']} | umur={age_min(r['created_at']):.0f}m")
    cs = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (r['id'],)).fetchall()
    for c in cs:
        print(f"    [{age_min(c['created_at']):.0f}m] {c['author']}: {c['body'][:160].replace(chr(10),' / ')}")

print()
print("== BLIND SPOT: kartu done/parked 24 jam terakhir ber-tenant KOSONG dengan LAPOR tanpa ACK ==")
cands = con.execute("""
  SELECT id,title,status,tenant,created_by,completed_at FROM tasks
  WHERE status IN ('done','blocked') AND (tenant IS NULL OR tenant='')
    AND completed_at IS NOT NULL AND completed_at > strftime('%s','now','-24 hours')
  ORDER BY completed_at DESC LIMIT 30
""").fetchall()
for r in cands:
    cs = con.execute("SELECT author,body FROM task_comments WHERE task_id=? ORDER BY created_at", (r['id'],)).fetchall()
    lapor = [c for c in cs if 'LAPOR' in c['body'].upper()]
    acks = [c for c in cs if 'RANTAI-ACK' in c['body']]
    if lapor and not acks:
        print(f"- {r['id']} | {r['title'][:60]} | {r['status']} | by={r['created_by']} | LAPOR={len(lapor)} ACK=0")

print()
print("== DONE 6 jam terakhir tanpa komentar sama sekali (hulu tamat-senyap) ==")
recent_done = con.execute("""
  SELECT id,title,tenant,created_by,completed_at FROM tasks
  WHERE status='done' AND completed_at > strftime('%s','now','-6 hours')
  ORDER BY completed_at DESC
""").fetchall()
print(f"total done 6 jam: {len(recent_done)}")
for r in recent_done:
    ncom = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (r['id'],)).fetchone()['c']
    if ncom == 0:
        print(f"- (no-comment) {r['id']} | {r['title'][:60]} | tenant={r['tenant']!r} | by={r['created_by']}")
con.close()
