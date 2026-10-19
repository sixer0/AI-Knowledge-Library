# Ambil SEMUA komentar penuh S13 + komentar terakhir dua kartu running (S14/S15) + payload event completed S13
import sqlite3
con = sqlite3.connect("file:C:/Users/TRIAL/AppData/Local/hermes/kanban.db?mode=ro", uri=True)
con.row_factory = sqlite3.Row

print("########## S13 t_5b68a0be — semua komentar penuh ##########")
for c in con.execute("SELECT author, created_at, body FROM task_comments WHERE task_id='t_5b68a0be' ORDER BY created_at ASC"):
    print(f"\n--- [{c['author']}] ---\n{c['body']}")

print("\n########## S13 payload event completed ##########")
for e in con.execute("SELECT kind, payload FROM task_events WHERE task_id='t_5b68a0be' AND kind='completed'"):
    print(e["payload"])

for cid, label in (("t_1837ce19","S14 counter-sign"), ("t_050e08e8","S15 librarian")):
    print(f"\n########## {label} {cid} — 3 komentar terakhir ##########")
    rows = list(con.execute("SELECT author, body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (cid,)))
    if not rows:
        print("(belum ada komentar)")
    for c in reversed(rows):
        print(f"--- [{c['author']}] ---\n{c['body'][:1200]}\n")
