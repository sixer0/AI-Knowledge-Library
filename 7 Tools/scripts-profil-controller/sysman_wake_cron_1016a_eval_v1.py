# Ronde wake 16-10: evaluasi per-kartu t_5b68a0be (done-unacked) dari kanban.db root (read-only)
import sqlite3, time, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
CARD = "t_5b68a0be"
now = int(time.time())

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts):
    return f"{(now - int(ts)) / 60:.1f}m" if ts else "-"

# 1. Kartu
r = con.execute("SELECT * FROM tasks WHERE id=?", (CARD,)).fetchone()
if not r:
    print("KARTU TIDAK ADA"); raise SystemExit
cols = r.keys()
print("=== KARTU ===")
for k in ("id","title","status","tenant","assignee","created_by","created_at","completed_at"):
    if k in cols:
        v = r[k]
        if k.endswith("_at") and v:
            print(f"{k}: {v} (umur {age(v)})")
        else:
            print(f"{k}: {v}")

# 2. Event terakhir
print("\n=== EVENT (10 terakhir) ===")
for e in con.execute("SELECT kind, created_at, payload FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 10", (CARD,)):
    p = (e["payload"] or "")[:120]
    print(f"- {e['kind']} @ {age(e['created_at'])} lalu | {p}")

# 3. Komentar (semua, ringkas)
print("\n=== KOMENTAR ===")
for c in con.execute("SELECT author, created_at, substr(body,1,300) b FROM task_comments WHERE task_id=? ORDER BY created_at ASC", (CARD,)):
    print(f"- [{c['author']}] @{age(c['created_at'])} lalu: {c['b']!r}")

# 4. Marker anti-ulang done-unacked
mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (CARD,)).fetchone()["n"]
print(f"\nMARKER RANTAI-WAKE done-unacked ada: {mk}")

# 5. Relasi
print("\n=== RELASI ===")
for l in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (CARD,)):
    pr = con.execute("SELECT id,title,status FROM tasks WHERE id=?", (l["parent_id"],)).fetchone()
    print(f"parent: {pr['id']} [{pr['status']}] {pr['title'][:70]}")
kids = [x["parent_id"] for x in con.execute("SELECT child_id AS parent_id FROM task_links WHERE parent_id=?", (CARD,))]
print(f"children: {len(kids)}")

# 6. Sensus tenant bila ada
ten = r["tenant"] if "tenant" in cols else None
if ten:
    print(f"\n=== SENSUS TENANT {ten} ===")
    rows = con.execute("SELECT id,status,title FROM tasks WHERE tenant=?", (ten,)).fetchall()
    by = {}
    for x in rows:
        by.setdefault(x["status"], []).append(x["id"])
    for s, ids in sorted(by.items()):
        print(f"{s}: {len(ids)}")
    # ACK per kartu done (id-list dulu, hindari nested cursor)
    done_ids = [x["id"] for x in rows if x["status"] == "done"]
    acked = 0
    for did in done_ids:
        n = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (did,)).fetchone()["n"]
        if n: acked += 1
    print(f"done ber-ACK: {acked}/{len(done_ids)}")

# 7. Sanity papan hidup
mx = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
print(f"\nSANITY: event papan terakhir umur {age(mx)}")
