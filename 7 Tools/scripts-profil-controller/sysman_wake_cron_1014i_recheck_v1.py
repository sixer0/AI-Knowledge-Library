import sqlite3, time, collections
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
ids = {
 "t_6a370834":"bab 5 EN","t_ca284fa4":"bab 10 EN","t_fa568361":"bab 2 EN",
 "t_b7d31583":"bab 3 EN","t_aa98df31":"bab 4 EN","t_0ba22121":"bab 9 EN","t_eb458a5e":"bab 11 EN"}
print("== RECHECK 7 KARTU SERAH-TANPA-ACK ==")
for tid, lbl in ids.items():
    t = con.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()
    cs = list(con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    mark = [c for c in cs if "RANTAI-WAKE done-unacked" in (c["body"] or "")]
    la = {c["author"] for c in lapor}
    ao = [c for c in ack if c["author"] not in la]
    print(f"  {tid} ({lbl}) [{t['status']}] lap={len(lapor)} ack_total={len(ack)} ack_lain={len(ao)} marker={len(mark)}")
# siapa penulis RANTAI-ACK di papan belakangan
print("\n== RANTAI-ACK terbaru lintas papan ==")
for r in con.execute("SELECT task_id, author, created_at FROM task_comments WHERE body LIKE '%RANTAI-ACK%' ORDER BY created_at DESC LIMIT 8"):
    print(f"  {r['task_id']} by {r['author']} {int((now-r['created_at'])/60)}m lalu")
con.close()
