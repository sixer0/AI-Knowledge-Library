# Ronde wake 15-10b: detail orang tua blocked, marker pada kartu done, kesegaran tenant
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# 1) seluruh kartu blocked tenant VIBE-BIBLE-1013: reason + umur + komentar terakhir
print("== BLOCKED WRITERS VBCB ==")
rows = con.execute("SELECT id,title,status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' ORDER BY id").fetchall()
cur = con.cursor()
for r in rows:
    tid = r['id']
    evs = cur.execute("SELECT kind, created_at, payload FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)).fetchall()
    lastev = f"{evs[0]['kind']}@{(now-evs[0]['created_at'])/60:.0f}m" if evs else "-"
    blks = cur.execute("SELECT created_at, payload FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    coms = cur.execute("SELECT author, substr(body,1,160) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (tid,)).fetchall()
    print(f"{tid} last={lastev}")
    print(f"   title={r['title'][:80]}")
    if blks is not None:
        print(f"   blocked_payload={(blks['payload'] or '')[:200]} age={(now-blks['created_at'])/60:.0f}m")
    for c in coms:
        print(f"   com[{c['author']}] {(now-c['created_at'])/60:.0f}m: {c['b'][:150]}")

# 2) kartu done tenant: marker RANTAI-WAKE / LAPOR / ACK
print("\n== DONE CARDS MARKER CENSUS ==")
dones = [r['id'] for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchall()]
mk = ck = ak = both0 = 0
cur2 = con.cursor()
for did in dones:
    m = cur2.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (did,)).fetchone()[0]
    l = cur2.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%')", (did,)).fetchone()[0]
    a = cur2.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (did,)).fetchone()[0]
    if m: mk += 1
    if l: ck += 1
    if a: ak += 1
    if not (m or l or a): both0 += 1
print(f"done={len(dones)} marker_wake={mk} lapor={ck} ack={ak} tanpa_komentar_kunci={both0}")

# contoh 5 done tanpa marker: kapan selesai + author
print("\n== SAMPLE DONE tanpa marker ==")
cur3 = con.cursor()
shown = 0
for did in dones:
    m = cur3.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%' OR task_id=? AND body LIKE '%LAPOR-SELESAI%' OR task_id=? AND body LIKE '%LAPOR-SELESEI%' OR task_id=? AND body LIKE '%RANTAI-ACK%'", (did,did,did,did)).fetchone()[0]
    if m: continue
    comp = cur3.execute("SELECT completed_at, assignee, created_at FROM tasks WHERE id=?", (did,)).fetchone()
    age_h = (now - comp[0])/3600 if comp[0] else -1
    print(f"{did} completed_age={age_h:.1f}h assignee={comp[1]}")
    shown += 1
    if shown >= 6: break

# 3) kesegaran tenant: rentang umur event terakhir per kartu tenant
print("\n== KESegARAN TENANT ==")
ages = []
cur4 = con.cursor()
for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchall():
    e = cur4.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r['id'],)).fetchone()
    if e and e['mx']: ages.append((now - e['mx'])/60)
if ages:
    print(f"kartu_ber_event={len(ages)} umur_event_min={min(ages):.0f} max={max(ages):.0f} menit")

# 4) komentar CHECKPOINT / keputusan controller terbaru di tenant (24 jam)
print("\n== KOMENTAR TERAKHIR TENANT (24 jam, semua kartu) ==")
for row in con.execute("""SELECT c.task_id, c.author, substr(c.body,1,200) b, c.created_at
  FROM task_comments c JOIN tasks t ON t.id=c.task_id
  WHERE t.tenant='VIBE-BIBLE-1013' AND c.created_at > ?
  ORDER BY c.created_at DESC LIMIT 15""", (now-86400,)).fetchall():
    print(f"{(now-row['created_at'])/60:.0f}m [{row['author']}] {row['task_id']}: {row['b'][:180]}")

# 5) pembanding: apakah masih ada kartu running di fleet (global) & blocked non-VBCB terkini
print("\n== BLOCKED NON-VBCB (status blocked, event <=6 jam) ==")
cur5 = con.cursor()
for r in con.execute("SELECT id,tenant,title FROM tasks WHERE status='blocked' AND tenant IS NOT NULL AND tenant != 'VIBE-BIBLE-1013'").fetchall():
    e = cur5.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r['id'],)).fetchone()
    age = (now - e['mx'])/60 if e and e['mx'] else 99999
    if age <= 360:
        print(f"{r['id']} tenant={r['tenant']} last_ev={age:.0f}m :: {r['title'][:70]}")
