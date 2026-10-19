# Sensus read-only baris WAKE ronde 14-10b: kelompok per tenant, status orang tua,
# event terakhir per kartu, hitung LAPOR/ACK/marker, plus sensus gave_up/timed_out.
import importlib.util, json, sqlite3, time, sys, os

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
SCAN = r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py"

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
authors = authors.split(",") if isinstance(authors, str) else list(authors)
rows = mod.scan(DB, now, authors)
print("RE-SCAN rows:", len(rows))
wake_ids = [r[0] if isinstance(r, (list, tuple)) else r for r in rows]

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

def one(sql, args=()):
    c2 = con.cursor()
    c2.execute(sql, args)
    return c2.fetchall()

print("\n=== PER-KARTU WAKE ===")
groups = {}
for tid in wake_ids:
    t = one("SELECT id,title,status,tenant,assignee,created_at,completed_at FROM tasks WHERE id=?", (tid,))
    if not t:
        print(f"{tid} NOT-FOUND")
        continue
    t = t[0]
    tenant = t["tenant"] or "(null)"
    parents = one("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))
    pstat = []
    for p in parents:
        pr = one("SELECT status,title FROM tasks WHERE id=?", (p["parent_id"],))
        if pr:
            pstat.append(pr[0]["status"])
    ev = one("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,))
    evk = ev[0]["kind"] if ev else "-"
    evage = round((now - ev[0]["created_at"]) / 60) if ev else -1
    lapor = one("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (tid,))[0]["c"]
    ack = one("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,))[0]["c"]
    marker = one("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,))[0]["c"]
    groups.setdefault(tenant, []).append({
        "id": tid, "title": (t["title"] or "")[:70], "status": t["status"],
        "assignee": t["assignee"], "parents": pstat, "last_ev": evk, "ev_age_min": evage,
        "lapor": lapor, "ack": ack, "marker": marker,
    })

for tenant, cards in sorted(groups.items()):
    print(f"\n--- TENANT {tenant} ({len(cards)} kartu) ---")
    st = {}
    for c in cards:
        st[c["status"]] = st.get(c["status"], 0) + 1
    print("status:", st)
    par = {}
    for c in cards:
        key = ",".join(sorted(set(c["parents"]))) if c["parents"] else "no-parent"
        par[key] = par.get(key, 0) + 1
    print("parent-status:", par)
    evk = {}
    for c in cards:
        evk[c["last_ev"]] = evk.get(c["last_ev"], 0) + 1
    print("last-event-kind:", evk)
    ages = [c["ev_age_min"] for c in cards if c["ev_age_min"] >= 0]
    if ages:
        print("event-age min..max:", min(ages), "..", max(ages))
    for c in cards[:99]:
        print(f"  {c['id']} [{c['status']}] par={','.join(c['parents']) or '-'} ev={c['last_ev']}@{c['ev_age_min']}m lapor={c['lapor']} ack={c['ack']} mk={c['marker']} :: {c['title']}")

print("\n=== SENSUS GAVE_UP / TIMED_OUT (24 jam) ===")
cut = now - 86400
gu = one("SELECT task_id, kind, created_at FROM task_events WHERE kind IN ('gave_up','timed_out') AND created_at>=? ORDER BY created_at", (cut,))
seen = {}
for r in gu:
    seen[r["task_id"]] = (r["kind"], round((now - r["created_at"]) / 60))
print("kartu dgn gave_up/timed_out <=24h:", len(seen))
byk = {}
for k, v in seen.items():
    byk[v[0]] = byk.get(v[0], 0) + 1
print("per kind:", byk)

print("\n=== BLIND SPOT: running + LAPOR tanpa ACK ===")
run = one("SELECT id,title,tenant FROM tasks WHERE status='running'")
print("total running:", len(run))
for r in run:
    lp = one("SELECT author, created_at, body FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%' ORDER BY created_at DESC LIMIT 1", (r["id"],))
    if lp:
        ak = one("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' AND created_at>=?", (r["id"], lp[0]["created_at"]))[0]["c"]
        hb = one("SELECT created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],))
        hbage = round((now - hb[0]["created_at"]) / 60) if hb else -1
        print(f"  {r['id']} tenant={r['tenant'] or '(null)'} hb@{hbage}m ack_after_lapor={ak} :: {(r['title'] or '')[:60]}")

print("\n=== SANITY PAPAN HIDUP ===")
me = one("SELECT MAX(created_at) m FROM task_events")[0]["m"]
print("event terbaru umur (mnt):", round((now - me) / 60))
print("tasks:", one("SELECT COUNT(*) c FROM tasks")[0]["c"], "| events:", one("SELECT COUNT(*) c FROM task_events")[0]["c"])
st_all = {}
for r in one("SELECT status, COUNT(*) c FROM tasks GROUP BY status"):
    st_all[r["status"]] = r["c"]
print("sensus status seluruh papan:", st_all)
