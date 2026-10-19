# Sensus ronde wake 14-10e: tenant VIBE-BIBLE-1013, status, event run, ACK, jangkar.
import sqlite3, time, json, collections

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# 1) Sensus status seluruh papan
cur = con.cursor()
print("== SENSUS STATUS PAPAN ==")
for r in cur.execute("SELECT status, COUNT(*) c FROM tasks GROUP BY status ORDER BY c DESC"):
    print(f"  {r['status']}: {r['c']}")

# 2) Sensus tenant VIBE-BIBLE-1013
print("\n== TENANT VIBE-BIBLE-1013 ==")
rows = list(con.execute("SELECT id,title,status,assignee,created_at,started_at,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013'"))
print(f"  total kartu: {len(rows)}")
st = collections.Counter(r["status"] for r in rows)
print("  status:", dict(st))

ids = [r["id"] for r in rows]
qmarks = ",".join("?" * len(ids))

# 3) Event run per kartu tenant: kinds + gave_up
print("\n== EVENT RUN TENANT (agregat kind) ==")
ev = collections.Counter()
gaveup = []
tout_last = {}
for r in con.execute(f"SELECT task_id, kind, created_at, payload FROM task_events WHERE task_id IN ({qmarks})", ids):
    ev[r["kind"]] += 1
    if r["kind"] == "timed_out":
        tout_last[r["task_id"]] = max(tout_last.get(r["task_id"], 0), r["created_at"])
    if r["kind"] == "gave_up":
        gaveup.append((r["task_id"], r["created_at"]))
print("  kinds:", dict(ev))
n_tout_cards = len(tout_last)
print(f"  kartu dgn event run timed_out: {n_tout_cards}")
print(f"  event gave_up: {len(gaveup)}")
for tid, ts in gaveup[:40]:
    print(f"    gave_up {tid} umur={(now-ts)//60}m")

# 4) Umur event terakhir papan & tenant
mx = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
mxt = con.execute(f"SELECT MAX(created_at) m FROM task_events WHERE task_id IN ({qmarks})", ids).fetchone()["m"]
print(f"\numur event terakhir papan: {(now-mx)/60:.1f} mnt; tenant: {(now-mxt)/60:.1f} mnt")

# 5) done-unacked: kartu done tenant, LAPOR vs ACK author
print("\n== DONE-UNACKED CHECK (kartu done tenant) ==")
done_rows = [r for r in rows if r["status"] == "done"]
print(f"  kartu done: {len(done_rows)}")
unacked = []
for r in done_rows:
    cs = list(con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (r["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "") or "LAPOR SELESAI" in (c["body"] or "")]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    mark = [c for c in cs if "RANTAI-WAKE done-unacked" in (c["body"] or "")]
    lap_authors = {c["author"] for c in lapor}
    ack_others = [c for c in ack if c["author"] not in lap_authors]
    if lapor and not ack_others:
        unacked.append((r["id"], r["title"][:50], len(lapor), len(ack), len(mark)))
print(f"  done tanpa ACK author-lain: {len(unacked)}")
for u in unacked[:30]:
    print("   ", u)

# 6) running cards dengan LAPOR tanpa ACK (blind spot)
print("\n== BLIND SPOT running ber-LAPOR tanpa ACK ==")
for r in rows:
    if r["status"] != "running":
        continue
    cs = list(con.execute("SELECT author, body FROM task_comments WHERE task_id=? ORDER BY created_at", (r["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESEI" in (c["body"] or "")]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    lap_authors = {c["author"] for c in lapor}
    ack_others = [c for c in ack if c["author"] not in lap_authors]
    hb = [c for c in cs if "heartbeat" in (c["body"] or "").lower()]
    if lapor and not ack_others:
        print(f"  {r['id']} '{r['title'][:40]}' lapor={len(lapor)} ack_lain={len(ack_others)} hb={len(hb)}")

# 7) Kartu blocked: reason ringkas + apakah jangkar kontrak
print("\n== BLOCKED TENANT (sebab) ==")
for r in rows:
    if r["status"] != "blocked":
        continue
    evs = list(con.execute("SELECT kind,payload,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (r["id"],)))
    reason = ""
    for e in evs:
        try:
            p = json.loads(e["payload"] or "{}")
        except Exception:
            p = {}
        if isinstance(p, dict) and p.get("reason"):
            reason = str(p["reason"])[:90]; break
    ncom = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (r["id"],)).fetchone()["c"]
    print(f"  {r['id']} '{r['title'][:44]}' com={ncom} reason={reason}")

# 8) Anak todo: orang tua status apa (turunan positif-palsu)
print("\n== TODO TENANT: status orang tua ==")
parent_status = collections.Counter()
orphan_todo = []
for r in rows:
    if r["status"] != "todo":
        continue
    ps = list(con.execute(f"SELECT t.status FROM task_links l JOIN tasks t ON t.id=l.parent_id WHERE l.child_id=?", (r["id"],)))
    if not ps:
        orphan_todo.append(r["id"]); parent_status["(tanpa-parent)"] += 1
    else:
        for p in ps:
            parent_status[p["status"]] += 1
print("  ", dict(parent_status))
print("  todo tanpa parent:", len(orphan_todo))

# 9) Komentar CHECKPOINT pada kartu timed_out (rem yang ditawarkan worker)
print("\n== CHECKPOINT di kartu timed_out ==")
for tid in sorted(tout_last)[:40]:
    cps = list(con.execute("SELECT author, substr(body,1,160) b, created_at FROM task_comments WHERE task_id=? AND body LIKE '%CHECKPOINT%' ORDER BY created_at DESC LIMIT 1", (tid,)))
    if cps:
        c = cps[0]
        print(f"  {tid}: [{c['author']}] {c['b']}")

con.close()
