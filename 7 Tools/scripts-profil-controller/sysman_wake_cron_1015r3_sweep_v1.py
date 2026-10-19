# -*- coding: utf-8 -*-
# Ronde 1015r3: sisa blocked non-VBCB (papan 43, tenant 33) + author marker 46 done + umur marker.
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

print("== BLOCKED NON-VBCB ==")
for r in con.execute("SELECT id,status,COALESCE(tenant,'(null)') tn,title,created_at FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant!='VIBE-BIBLE-1013')").fetchall():
    ev = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (r["id"],)).fetchone()[0]
    c = con.execute("SELECT author,body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    print(f"  {r['id']} {r['tn']} ev={age(ev)}m {(r['title'] or '')[:55]}")
    if c: print(f"    last cm [{c['author']}] {c['body'][:110]}")

print("\n== AUTHOR + UMUR MARKER 46 DONE ==")
authors = {}
ages = []
for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchall():
    c = con.execute("SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%' ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    if c:
        authors[c["author"]] = authors.get(c["author"], 0) + 1
        ages.append(age(c["created_at"]))
print("authors:", authors, "| umur marker min..max:", (min(ages), max(ages)) if ages else None)

print("\n== DONE NON-VBCB 24J TANPA ACK & TANPA MARKER (cek lintas papan) ==")
n = 0
for r in con.execute("SELECT id,tenant,title,completed_at FROM tasks WHERE status='done' AND completed_at > ? AND COALESCE(tenant,'')!='VIBE-BIBLE-1013'", (NOW-86400,)).fetchall():
    nack = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    nmark = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()[0]
    nlap = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (r["id"],)).fetchone()[0]
    if nlap and not nack and not nmark:
        n += 1
        print(f"  {r['id']} {r['tenant']} done {age(r['completed_at'])}m lap={nlap} ack=0 mark=0 {(r['title'] or '')[:55]}")
print("total kandidat done-unacked non-VBCB:", n)
