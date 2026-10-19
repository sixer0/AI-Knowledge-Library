# Cek akhir: komentar terbaru kartu VBCB (sudah ternilai controller?), detail id baru re-scan, kartu t_d3cc135a.
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

print("=== komentar VBCB terbaru (top 8) ===")
q = """SELECT c.task_id, c.author, substr(c.body,1,90) b, c.created_at FROM task_comments c
JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013'
ORDER BY c.created_at DESC LIMIT 8"""
for r in con.execute(q):
    print(f"  {r['task_id']} {r['author']} {(now-r['created_at'])/60:.0f}m {r['b']!r}")

print("\n=== apakah ada RANTAI/VONIS/TRIASE controller di kartu blocked VBCB? ===")
n = con.execute("""SELECT COUNT(*) n FROM task_comments c JOIN tasks t ON t.id=c.task_id
WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked'
AND (c.body LIKE '%RANTAI-ACK%' OR c.body LIKE '%VONIS%' OR c.body LIKE '%TRIASE%')""").fetchone()["n"]
print("  count:", n)

print("\n=== id baru re-scan vs ronde awal ===")
first = set("""t_002af121 t_0311d1e4 t_050a75ff t_0bf0854c t_1168e59f t_14e7030f t_153594d4
t_1c98456a t_23f7da05 t_2543fb8f t_2ae211bb t_2d32e7c8 t_2e0e92d4 t_30dd071c t_34bf2edc
t_3782b61a t_397be920 t_46ff8be6 t_483b2d91 t_4d7a1691 t_4edfcf3a t_5831a79d t_60ed37fa
t_64328060 t_674377e1 t_68d1d8be t_7391c81b t_760e7792 t_77a9bcd3 t_799a1879 t_8b90e854
t_8d618268 t_93c6bec3 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc t_a064e4cc
t_a37d190b t_a3e70bf1 t_a48e52d1 t_a4b6791b t_a783103d t_a931e1b1 t_aaab1be9 t_b422fa6d
t_b81fea6a t_b9500192 t_ba72c512 t_be219ab7 t_c1d55eef t_c792df45 t_c8784acc t_cb601d70
t_d3cc135a t_d4fca8b3 t_d8480778 t_d9f482ab t_e04bca14 t_e4c7440d t_e5e2e083 t_e8cac74b
t_ec2342d5 t_edb280b5 t_efb6071f t_f9ac1ff2""".split())
rescan = set(l.split()[1] for l in open(r"C:/Users/TRIAL/AppData/Local/Temp/rescan_1014z.txt") if l.startswith("WAKE"))
for tid in sorted(rescan - first):
    r = con.execute("SELECT tenant,status,title FROM tasks WHERE id=?", (tid,)).fetchone()
    print("  NEW:", tid, dict(r) if r else "MISSING")
for tid in sorted(first - rescan):
    r = con.execute("SELECT tenant,status,title FROM tasks WHERE id=?", (tid,)).fetchone()
    print("  GONE:", tid, dict(r) if r else "MISSING")

print("\n=== t_d3cc135a komentar terakhir ===")
for r in con.execute("SELECT author, substr(body,1,140) b, created_at FROM task_comments WHERE task_id='t_d3cc135a' ORDER BY created_at DESC LIMIT 3"):
    print(f"  {r['author']} {(now-r['created_at'])/60:.0f}m {r['b']!r}")
