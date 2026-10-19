# Nilai baris WAKE ronde 14-10h: kelompok per tenant, status, gave_up, ACK, marker.
import sqlite3, time, collections, importlib.util

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

# 1) Jalankan scan() kanonis untuk mendapat baris persis
spec = importlib.util.spec_from_file_location(
    "wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
rows = m.scan(DB, now, [a.strip() for a in m.DEFAULT_AUTHORS.split(",")])
print("== SCAN KANONIS ==")
print("total baris:", len(rows))
by_card = collections.defaultdict(list)
for r in rows:
    tid = r[0] if isinstance(r, (tuple, list)) else r.get("id", str(r))
    cls = r[1] if isinstance(r, (tuple, list)) else r.get("cls", "?")
    by_card[tid].append(cls)
print("kartu unik:", len(by_card))

# 2) Profil tiap kartu: tenant, judul, status, assignee, umur event terakhir
print("\n== PROFIL KARTU WAKE ==")
tenants = collections.Counter()
info = {}
for tid in by_card:
    t = con.execute("SELECT id,title,status,assignee,tenant,created_at,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print("  TIDAK ADA:", tid); continue
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    ev_age = int((now - ev) / 60) if ev else -1
    info[tid] = dict(title=t["title"], status=t["status"], tenant=t["tenant"],
                     assignee=t["assignee"], ev_age=ev_age, classes=sorted(set(by_card[tid])))
    tenants[t["tenant"] or "(NULL)"] += 1
for tn, c in tenants.most_common():
    print(f"  tenant {tn}: {c} kartu")

# 3) Per tenant: sensus status seluruh kartu tenant + umur event min/max
print("\n== SENSUS PER TENANT (seluruh kartu, bukan hanya wake) ==")
for tn in tenants:
    if tn == "(NULL)":
        continue
    trows = list(con.execute("SELECT id,status FROM tasks WHERE tenant=?", (tn,)))
    st = collections.Counter(r["status"] for r in trows)
    ids = [r["id"] for r in trows]
    q = ",".join("?" * len(ids))
    ages = [int((now - e) / 60) for (e,) in con.execute(
        f"SELECT MAX(created_at) FROM task_events WHERE task_id IN ({q}) GROUP BY task_id", ids) if e]
    lo, hi = (min(ages), max(ages)) if ages else (-1, -1)
    print(f"  {tn}: total={len(trows)} status={dict(st)} umur_event_mnt min={lo} max={hi}")

# 4) Kartu NULL-tenant dalam wake (jangkar/kartu lain): detail
print("\n== KARTU WAKE TENANT NULL ==")
for tid, d in info.items():
    if not d["tenant"]:
        print(f"  {tid} [{d['status']}] ev={d['ev_age']}m cls={d['classes']} :: {d['title'][:80]}")

# 5) Event gave_up / timed_out agregat per tenant dari kartu wake
print("\n== EVENT RUN/TIMEOUT KARTU WAKE ==")
gv = collections.Counter()
for tid in by_card:
    tn = info.get(tid, {}).get("tenant") or "(NULL)"
    for r in con.execute("SELECT kind, COUNT(*) c FROM task_events WHERE task_id=? AND kind IN ('timed_out','gave_up') GROUP BY kind", (tid,)):
        gv[(tn, r["kind"])] += r["c"]
for (tn, k), c in sorted(gv.items()):
    print(f"  {tn} {k}: {c}")

# 6) Done-unacked: kartu berstatus done/blocked dengan LAPOR tanpa ACK author-lain + marker
print("\n== DONE-UNACKED / ACK STATUS KARTU WAKE ==")
for tid, d in sorted(info.items(), key=lambda kv: (kv[1]["tenant"] or "", kv[0])):
    cs = list(con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "") or "LAPOR SELESAI" in (c["body"] or "")]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    mark = [c for c in cs if "RANTAI-WAKE done-unacked" in (c["body"] or "")]
    lap_authors = {c["author"] for c in lapor}
    ack_others = [c for c in ack if c["author"] not in lap_authors]
    if lapor and not ack_others:
        last = lapor[-1]
        print(f"  UNACKED {tid} [{d['status']}] tenant={d['tenant']} lap={last['author']} umur_lap={int((now-last['created_at'])/60)}m marker={len(mark)} :: {d['title'][:60]}")
con.close()
print("\n== SELESAI ==")
