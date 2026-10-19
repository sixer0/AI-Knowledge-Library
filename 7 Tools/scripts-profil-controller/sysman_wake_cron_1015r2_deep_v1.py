# -*- coding: utf-8 -*-
# Ronde 1015r2 gali: orang tua blocked VBCB (reason/checkpoint/ACK), kejadian 44m lalu,
# 10 blocked non-VBCB, census ACK done VBCB, umur gave_up/timed_out terakhir.
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

PARENTS = ["t_64328060","t_30dd071c","t_d8480778","t_8b90e854","t_93c6bec3","t_d9f482ab",
"t_4d7a1691","t_ec2342d5","t_c1d55eef","t_674377e1","t_68d1d8be","t_b422fa6d","t_2d32e7c8",
"t_760e7792","t_ba72c512","t_2ae211bb","t_050a75ff","t_483b2d91","t_e8cac74b","t_e5e2e083",
"t_a783103d","t_d3cc135a","t_8d618268","t_c792df45","t_0df60358","t_a3e70bf1","t_be219ab7",
"t_b9500192","t_a931e1b1","t_2543fb8f","t_b81fea6a","t_aaab1be9","t_e4c7440d"]

print("== 33 ORANG TUA BLOCKED VBCB ==")
for tid in PARENTS:
    t = con.execute("SELECT title,status,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    ev = con.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (tid,)).fetchone()["mx"]
    blk = con.execute("SELECT payload,created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    nck = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%CHECKPOINT%'", (tid,)).fetchone()[0]
    nack = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
    nlap = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (tid,)).fetchone()[0]
    lastc = con.execute("SELECT author,substr(body,1,110) b,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    print(f"{tid} | {(t['title'] or '')[:52]} | ev={age(ev)}m blk={age(blk['created_at']) if blk else '-'}m ck={nck} lap={nlap} ack={nack}")
    if blk: print("    reason:", str(blk["payload"])[:150].replace("\n"," "))
    if lastc: print("    cmt_last:", lastc["author"], age(lastc["created_at"]), "m |", lastc["b"].replace("\n"," ")[:110])

print("\n== KEJADIAN TERAKHIR PAPAN (<=60m) ==")
rows = con.execute("""SELECT e.task_id, e.kind, e.created_at, substr(COALESCE(t.title,''),1,50) ti
 FROM task_events e LEFT JOIN tasks t ON t.id=e.task_id WHERE e.created_at > ? ORDER BY e.created_at DESC LIMIT 15""", (NOW-3600,)).fetchall()
for r in rows: print(" ", age(r["created_at"]), "m |", r["task_id"], r["kind"], "|", r["ti"])

print("\n== UMUR EVENT TIMEOUT/GAVE_UP TERAKHIR VBCB ==")
r = con.execute("""SELECT MAX(e.created_at) FROM task_events e JOIN tasks t ON t.id=e.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind IN ('timed_out','gave_up')""").fetchone()[0]
print("terakhir:", age(r), "mnt")

print("\n== 10 BLOCKED NON-VBCB ==")
rows = con.execute("""SELECT id, COALESCE(tenant,'(null)') tn, substr(title,1,60) ti, assignee FROM tasks
 WHERE status='blocked' AND (tenant IS NULL OR tenant != 'VIBE-BIBLE-1013')""").fetchall()
for r in rows:
    ev = con.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
    blk = con.execute("SELECT payload,created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    nack = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    nmark = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()[0]
    print(f"{r['id']} | {r['tn']} | {r['ti']} | ev={age(ev)}m ack={nack} mark={nmark}")
    if blk: print("    reason:", str(blk["payload"])[:160].replace("\n"," "), "| blk_age:", age(blk["created_at"]), "m")

print("\n== CENSUS ACK 46 DONE VBCB ==")
rows = con.execute("""SELECT id, substr(title,1,44) ti, completed_at FROM tasks
 WHERE tenant='VIBE-BIBLE-1013' AND status='done' ORDER BY completed_at DESC""").fetchall()
noack = []
for r in rows:
    nack = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    nmark = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()[0]
    if nack == 0: noack.append((r["id"], r["ti"], age(r["completed_at"]), nmark))
print("total done:", len(rows), "| tanpa ACK:", len(noack), "| dari itu sudah ber-marker sysman:", sum(1 for x in noack if x[3] > 0))
for x in noack[:15]: print("  ", x[0], "|", x[1], "| selesai", x[2], "m | mark:", x[3])
