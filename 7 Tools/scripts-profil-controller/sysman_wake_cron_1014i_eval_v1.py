# Ronde wake 14-10i: evaluasi baris WAKE per tenant + ACK + marker + blind spot running.
import sqlite3, time, collections, importlib.util

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

spec = importlib.util.spec_from_file_location(
    "wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
rows = m.scan(DB, now, [a.strip() for a in m.DEFAULT_AUTHORS.split(",")])
print("== SCAN KANONIS (re-run) ==")
print("total baris:", len(rows))
by_card = collections.defaultdict(list)
for r in rows:
    tid = r[0] if isinstance(r, (tuple, list)) else r.get("id", str(r))
    cls = r[1] if isinstance(r, (tuple, list)) else r.get("cls", "?")
    by_card[tid].append(cls)
print("kartu unik:", len(by_card))

info = {}
tenants = collections.Counter()
for tid in by_card:
    t = con.execute("SELECT id,title,status,assignee,tenant,created_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print("  TIDAK ADA:", tid); continue
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    ev_age = int((now - ev) / 60) if ev else -1
    info[tid] = dict(title=t["title"], status=t["status"], tenant=t["tenant"],
                     assignee=t["assignee"], ev_age=ev_age, classes=sorted(set(by_card[tid])))
    tenants[t["tenant"] or "(NULL)"] += 1

print("\n== TENANT KARTU WAKE ==")
for tn, c in tenants.most_common():
    print(f"  {tn}: {c}")

print("\n== SENSUS PER TENANT ==")
for tn in tenants:
    if tn == "(NULL)":
        continue
    trows = list(con.execute("SELECT id,status FROM tasks WHERE tenant=?", (tn,)))
    st = collections.Counter(r["status"] for r in trows)
    ids = [r["id"] for r in trows]
    ages = []
    for r in ids:
        e = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (r,)).fetchone()[0]
        if e: ages.append(int((now - e) / 60))
    lo, hi = (min(ages), max(ages)) if ages else (-1, -1)
    print(f"  {tn}: total={len(trows)} status={dict(st)} umur_event_mnt min={lo} max={hi}")

print("\n== KARTU WAKE TENANT NULL / ANOMALI ==")
for tid, d in info.items():
    if not d["tenant"]:
        print(f"  {tid} [{d['status']}] ev={d['ev_age']}m cls={d['classes']} :: {d['title'][:90]}")

print("\n== EVENT RUN/TIMEOUT AGREGAT PER TENANT (dari kartu wake) ==")
gv = collections.Counter()
for tid in by_card:
    tn = info.get(tid, {}).get("tenant") or "(NULL)"
    for r in con.execute("SELECT kind, COUNT(*) c FROM task_events WHERE task_id=? AND kind IN ('timed_out','gave_up','run_started') GROUP BY kind", (tid,)):
        gv[(tn, r["kind"])] += r["c"]
for (tn, k), c in sorted(gv.items()):
    print(f"  {tn} {k}: {c}")

print("\n== DONE-UNACKED RINCI (kelas done-unacked di scan) ==")
for tid, d in sorted(info.items(), key=lambda kv: (kv[1]["tenant"] or "", kv[0])):
    if "done-unacked" not in d["classes"]:
        continue
    cs = list(con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "") or "LAPOR SELESAI" in (c["body"] or "")]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    mark = [c for c in cs if "RANTAI-WAKE done-unacked" in (c["body"] or "")]
    lap_authors = {c["author"] for c in lapor}
    ack_others = [c for c in ack if c["author"] not in lap_authors]
    last = lapor[-1] if lapor else None
    print(f"  {tid} [{d['status']}] tenant={d['tenant']} ev={d['ev_age']}m lap={last['author'] if last else '-'} umur_lap={int((now-last['created_at'])/60) if last else -1}m ack_lain={len(ack_others)} marker={len(mark)} :: {d['title'][:70]}")

print("\n== SAMPEL KELAS STALLED/FASE PER TENANT (judul) ==")
seen = set()
for tid, d in sorted(info.items(), key=lambda kv: (kv[1]["tenant"] or "", kv[0])):
    tn = d["tenant"] or "(NULL)"
    if tn in seen: continue
    if any(c in ("stalled", "fase-stalled", "run-timed_out") for c in d["classes"]):
        seen.add(tn)
        print(f"  {tn} contoh {tid} [{d['status']}] cls={d['classes']} :: {d['title'][:80]}")

print("\n== BLIND SPOT: kartu running + LAPOR tanpa ACK author-lain ==")
run = list(con.execute("SELECT id,title,status,tenant,assignee FROM tasks WHERE status='running'"))
print("jumlah running:", len(run))
for t in run:
    cs = list(con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (t["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "") or "LAPOR SELESAI" in (c["body"] or "")]
    hb = [c for c in cs if "HEARTBEAT" in (c["body"] or "").upper()]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    lap_authors = {c["author"] for c in lapor}
    ack_others = [c for c in ack if c["author"] not in lap_authors]
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (t["id"],)).fetchone()["m"]
    ev_age = int((now - ev) / 60) if ev else -1
    if lapor and not ack_others:
        print(f"  LAPOR-TANPA-ACK {t['id']} tenant={t['tenant']} ev={ev_age}m lap={lapor[-1]['author']} umur_lap={int((now-lapor[-1]['created_at'])/60)}m :: {t['title'][:70]}")
    elif hb:
        print(f"  heartbeat {t['id']} tenant={t['tenant']} ev={ev_age}m hb_umur={int((now-hb[-1]['created_at'])/60)}m :: {t['title'][:60]}")

con.close()
print("\n== SELESAI ==")
