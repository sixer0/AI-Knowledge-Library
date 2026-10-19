# -*- coding: utf-8 -*-
# sysman cron 14-10: evaluasi baris WAKE (stalled + run-timed_out), read-only.
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())

STALLED = ["t_002af121","t_0311d1e4","t_0bf0854c","t_1168e59f","t_14e7030f","t_153594d4",
"t_1c98456a","t_23f7da05","t_2e0e92d4","t_34bf2edc","t_3782b61a","t_397be920","t_46ff8be6",
"t_5831a79d","t_60ed37fa","t_7391c81b","t_77a9bcd3","t_799a1879","t_95b5b6cb","t_99418ea0",
"t_9bf75422","t_9e457da5","t_9ebc8fbc","t_a064e4cc","t_a37d190b","t_a48e52d1","t_a4b6791b",
"t_c8784acc","t_cb601d70","t_d4fca8b3","t_e04bca14","t_edb280b5","t_efb6071f","t_f9ac1ff2"]
TIMEDOUT = ["t_050a75ff","t_0df60358","t_2543fb8f","t_2ae211bb","t_2d32e7c8","t_30dd071c",
"t_483b2d91","t_4d7a1691","t_4edfcf3a","t_64328060","t_674377e1","t_760e7792","t_8b90e854",
"t_8d618268","t_93c6bec3","t_a3e70bf1","t_a783103d","t_a931e1b1","t_aaab1be9","t_b422fa6d",
"t_b81fea6a","t_b9500192","t_ba72c512","t_be219ab7","t_c1d55eef","t_c792df45","t_d3cc135a",
"t_d8480778","t_d9f482ab","t_e4c7440d","t_e5e2e083","t_e8cac74b","t_ec2342d5"]

con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row

tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES:", ",".join(tables))
for t in ("tasks", "task_events", "task_links"):
    if t in tables:
        print(t, "COLS:", ",".join(r[1] for r in con.execute("PRAGMA table_info(" + t + ")")))
ctab = next((t for t in tables if "comment" in t.lower()), None)
if ctab:
    print(ctab, "COLS:", ",".join(r[1] for r in con.execute("PRAGMA table_info(" + ctab + ")")))
rtabs = [t for t in tables if "run" in t.lower()]
for t in rtabs:
    print(t, "RUNCOLS:", ",".join(r[1] for r in con.execute("PRAGMA table_info(" + t + ")")))

def age(ts):
    return int((now - ts) / 60) if ts else -1

print("\n== STATUS CENSUS ==")
for r in con.execute("SELECT status, COUNT(*) c FROM tasks GROUP BY status ORDER BY c DESC"):
    print(r["status"], r["c"])
m = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
print("LAST EVENT AGE_MIN:", age(m))

print("\n== OPEN BY TENANT (todo/blocked/running) ==")
for r in con.execute("SELECT COALESCE(NULLIF(tenant,''),'-') tn, status, COUNT(*) c FROM tasks "
                     "WHERE status IN ('todo','blocked','running') GROUP BY tn, status ORDER BY tn"):
    print(r["tn"], r["status"], r["c"])

TOKENS = ("LAPOR-SELESAI", "RANTAI-ACK", "ANCHOR-KONTRAK", "[FASE]", "CHECKPOINT",
          "PARKED", "DITAHAN", "RANTAI-WAKE", "WAKE")

def comment_stats(cid):
    if not ctab:
        return 0, {}, ""
    rows = list(con.execute("SELECT author, body, created_at FROM " + ctab +
                            " WHERE task_id=? ORDER BY created_at", (cid,)))
    toks = {}
    for key in TOKENS:
        c = sum(1 for r in rows if key.lower() in (r["body"] or "").lower())
        if c:
            toks[key] = c
    last = " || ".join((r["author"] or "?") + ": " + (r["body"] or "")[:110].replace("\n", " ")
                       for r in rows[-2:])
    return len(rows), toks, last

def parents(cid):
    out = []
    for r in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (cid,)):
        pr = con.execute("SELECT status FROM tasks WHERE id=?", (r["parent_id"],)).fetchone()
        out.append(r["parent_id"] + ":" + (pr["status"] if pr else "?"))
    return out

def children_open(cid):
    n = 0
    for r in con.execute("SELECT child_id FROM task_links WHERE parent_id=?", (cid,)):
        ch = con.execute("SELECT status FROM tasks WHERE id=?", (r["child_id"],)).fetchone()
        if ch and ch["status"] in ("todo", "blocked", "running"):
            n += 1
    return n

def report(ids, klass):
    print("\n== " + klass + " (" + str(len(ids)) + ") ==")
    for cid in ids:
        t = con.execute("SELECT * FROM tasks WHERE id=?", (cid,)).fetchone()
        if not t:
            print(cid, "NOT FOUND")
            continue
        d = {k: t[k] for k in t.keys()}
        ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? "
                         "ORDER BY created_at DESC LIMIT 1", (cid,)).fetchone()
        n, toks, lastc = comment_stats(cid)
        print("%s | %s | tenant=%s | assignee=%s | creator=%s | born=%dm | lastev=%s@%dm | openchild=%d | par=%s | ncmt=%d | %s" % (
            cid, d.get("status"), d.get("tenant"), d.get("assignee"), d.get("created_by"),
            age(d.get("created_at")),
            (ev["kind"] if ev else "-"), (age(ev["created_at"]) if ev else -1),
            children_open(cid), ",".join(parents(cid)) or "-", n,
            " ".join(k + "=" + str(v) for k, v in toks.items())))
        print("   T:", (d.get("title") or "")[:90].replace("\n", " "))
        for rk in ("reason", "blocked_reason", "note"):
            if d.get(rk):
                print("   R:", str(d[rk])[:100].replace("\n", " "))
                break
        if lastc:
            print("   LASTCMT:", lastc[:220])

report(STALLED, "STALLED")
report(TIMEDOUT, "RUN-TIMED_OUT")

# detail run-timed_out: tabel run untuk satu sampel
if rtabs:
    samp = TIMEDOUT[0]
    for t in rtabs:
        try:
            rows = list(con.execute("SELECT * FROM " + t + " WHERE task_id=? ORDER BY rowid DESC LIMIT 3", (samp,)))
            for r in rows:
                dd = {k: r[k] for k in r.keys()}
                print("RUNSAMPLE", t, {k: v for k, v in dd.items() if v not in (None, "", 0)})
        except Exception as e:
            print("runsamp skip", t, e)

print("\n== BLINDSPOT running+LAPOR tanpa ACK ==")
if ctab:
    q = ("SELECT DISTINCT t.id, t.tenant, t.title FROM tasks t JOIN " + ctab +
         " c ON c.task_id=t.id WHERE t.status='running' AND c.body LIKE '%LAPOR%'")
    for r in con.execute(q):
        acks = con.execute("SELECT COUNT(*) FROM " + ctab +
                           " WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
        hb = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (r["id"],)).fetchone()[0]
        lap = con.execute("SELECT MAX(created_at) FROM " + ctab +
                          " WHERE task_id=? AND body LIKE '%LAPOR%'", (r["id"],)).fetchone()[0]
        print(r["id"], "tenant=" + str(r["tenant"]), "acks=" + str(acks),
              "lapor_age=%dm" % age(lap), "lastev=%dm" % age(hb),
              (r["title"] or "")[:70].replace("\n", " "))
