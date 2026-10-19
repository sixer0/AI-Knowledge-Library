# Evaluasi baris WAKE ronde cron 14-10 (read-only, kanban.db root)
import sqlite3, time, collections, sys

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = """t_002af121 t_0311d1e4 t_0913266d t_0918b6d2 t_0ac8927f t_0bf0854c t_0f3e37eb
t_1168e59f t_14e7030f t_153594d4 t_19930381 t_1c98456a t_23f7da05 t_2e0e92d4 t_34bf2edc
t_3782b61a t_397be920 t_46ff8be6 t_5291d587 t_5715d1fc t_5831a79d t_60ed37fa t_6aa0384c
t_7124c228 t_7391c81b t_7707a0cd t_77a9bcd3 t_799a1879 t_7f36de9e t_80a9fb43 t_896447e4
t_95b5b6cb t_99418ea0 t_99bb85a4 t_9bf75422 t_9e457da5 t_9ebc8fbc t_a064e4cc t_a148a692
t_a37d190b t_a48e52d1 t_a4b6791b t_a66ce30a t_ad5d8e6f t_b2b82e31 t_c2180f14 t_c8784acc
t_cb601d70 t_ccfca3b8 t_d4fca8b3 t_de326482 t_de73c01d t_deb670d0 t_e04bca14 t_ed8b0b54
t_ed9976be t_efb6071f t_f9ac1ff2""".split()

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = int(time.time())

def cols(table):
    return [r["name"] for r in con.execute(f"PRAGMA table_info({table})")]

tcols = cols("tasks")
ecols = cols("task_events")
ccols = cols("task_comments")
print("SCHEMA tasks:", ",".join(tcols))
print("SCHEMA events:", ",".join(ecols))
print("SCHEMA comments:", ",".join(ccols))

# sanity papan hidup
last_ev = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
n_tasks = con.execute("SELECT COUNT(*) c FROM tasks").fetchone()["c"]
print(f"SANITY last_event_age_min={int((now-last_ev)/60)} tasks={n_tasks}")

# sensus event kinds 6 jam terakhir
print("\n== EVENT KINDS <=6h ==")
for r in con.execute("SELECT kind, COUNT(*) c, MAX(created_at) mx FROM task_events WHERE created_at >= ? GROUP BY kind ORDER BY c DESC", (now-6*3600,)):
    print(f"{r['kind']}: {r['c']} last={int((now-r['mx'])/60)}m")

# per kartu WAKE
print("\n== PER-KARTU ==")
by_tenant = collections.defaultdict(list)
for tid in IDS:
    t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(f"{tid} MISSING"); continue
    td = dict(t)
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    evk = ev["kind"] if ev else "-"; evage = int((now-ev["created_at"])/60) if ev else -1
    # parents
    pars = [p["parent_id"] for p in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))]
    parstat = []
    for p in pars:
        pr = con.execute("SELECT status FROM tasks WHERE id=?", (p,)).fetchone()
        parstat.append(f"{p}:{pr['status'] if pr else '?'}")
    # children statuses
    chs = [c["status"] for c in con.execute("SELECT t.status FROM task_links l JOIN tasks t ON t.id=l.child_id WHERE l.parent_id=?", (tid,))]
    chc = collections.Counter(chs)
    # comments: LAPOR / ACK(author lain) / marker
    cm = [dict(r) for r in con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,))]
    lapor = [c for c in cm if ("LAPOR-SELESEI" in c["body"]) or ("LAPOR-SELESAI" in c["body"]) or ("LAPOR SELESAI" in c["body"].upper())]
    acks = [c for c in cm if "RANTAI-ACK" in c["body"]]
    marker = any("RANTAI-WAKE done-unacked" in c["body"] for c in cm)
    fase = any("[FASE]" in c["body"] for c in cm)
    lastlap = max([c["created_at"] for c in lapor], default=0)
    ack_other = [c for c in acks if lastlap==0 or c["created_at"]>=lastlap]
    authors = collections.Counter(c["author"] for c in cm)
    tenant = td.get("tenant") or "-"
    title = (td.get("title") or "")[:70]
    status = td.get("status")
    assignee = td.get("assignee") or "-"
    reason = (td.get("blocked_reason") or td.get("reason") or "")[:90] if ("blocked_reason" in tcols or "reason" in tcols) else ""
    print(f"{tid} | {status} | tenant={tenant} | asg={assignee} | ev={evk}@{evage}m | par=[{';'.join(parstat)}] | kids={dict(chc)} | lapor={len(lapor)} ack_after={len(ack_other)} marker={int(marker)} fase={int(fase)} | cauthors={dict(authors)}")
    print(f"   title: {title}")
    if reason: print(f"   reason: {reason}")
    by_tenant[tenant].append(tid)

print("\n== GROUP BY TENANT (kartu WAKE) ==")
for k, v in sorted(by_tenant.items(), key=lambda x:-len(x[1])):
    print(f"{k}: {len(v)}")

# sensus penuh per tenant dominan
print("\n== CENSUS TENANT ==")
for ten in [k for k in by_tenant if k != "-"]:
    rows = list(con.execute("SELECT id,status FROM tasks WHERE tenant=?", (ten,)))
    st = collections.Counter(r["status"] for r in rows)
    ids_all = [r["id"] for r in rows]
    q = ",".join("?"*len(ids_all))
    ev6 = con.execute(f"SELECT kind, COUNT(*) c FROM task_events WHERE task_id IN ({q}) AND created_at >= ? GROUP BY kind", (*ids_all, now-6*3600)).fetchall()
    lastev = con.execute(f"SELECT MAX(created_at) m FROM task_events WHERE task_id IN ({q})", (*ids_all,)).fetchone()["m"]
    acked_done = 0; done_n = 0
    for r in rows:
        if r["status"] == "done":
            done_n += 1
            a = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
            mk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["c"]
            if a: acked_done += 1
    print(f"{ten}: total={len(rows)} status={dict(st)} lastev_age={int((now-lastev)/60) if lastev else -1}m ev6h={ {r['kind']:r['c'] for r in ev6} } done={done_n} done_acked={acked_done}")

# blind spot: kartu running dengan LAPOR tanpa ACK
print("\n== BLINDSPOT running ber-LAPOR ==")
run_rows = list(con.execute("SELECT id,title,tenant,assignee FROM tasks WHERE status='running'"))
print(f"total running={len(run_rows)}")
for r in run_rows:
    hb = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    cm = list(con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (r["id"],)))
    lapor = [c for c in cm if "LAPOR-SELESE" in c["body"]]
    acks = [c for c in cm if "RANTAI-ACK" in c["body"]]
    lastlap = max([c["created_at"] for c in lapor], default=0)
    acko = [c for c in acks if lastlap and c["created_at"] >= lastlap]
    if lapor:
        print(f"{r['id']} | {r['tenant'] or '-'} | hb_age={int((now-hb)/60) if hb else -1}m | lapor={len(lapor)} lap_age={int((now-lastlap)/60)}m ack_after={len(acko)} | {(r['title'] or '')[:60]}")
