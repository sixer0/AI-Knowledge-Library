# Sysman cron eval: nilai baris WAKE ronde siang 14-10, kelompok per tenant.
import importlib.util, json, sqlite3, time, sys

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
SCAN = r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py"

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")

now = int(time.time())
findings = mod.scan(DB, now, authors)

# Normalisasi temuan: boleh list of tuples/dicts
rows = []
for f in findings:
    if isinstance(f, dict):
        rows.append(f)
    elif isinstance(f, (tuple, list)):
        d = {"id": f[0], "cls": f[1], "age_min": f[2]}
        if len(f) > 3: d["extra"] = str(f[3])
        rows.append(d)

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def one(cur, q, *a):
    c = cur.cursor()
    c.execute(q, a)
    r = c.fetchone()
    return r[0] if r else None

print("=== FINDINGS:", len(rows))
ids = sorted({r["id"] for r in rows})
print("=== UNIQUE CARDS:", len(ids))

by_class = {}
for r in rows:
    by_class.setdefault(r["cls"], set()).add(r["id"])
for k, v in sorted(by_class.items()):
    print(f"class {k}: {len(v)} cards")

out = []
for cid in ids:
    t = con.execute("SELECT id,title,status,tenant,created_at,completed_at FROM tasks WHERE id=?", (cid,)).fetchone()
    if not t:
        out.append({"id": cid, "err": "not-found"}); continue
    evs = con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (cid,)).fetchall()
    last_ev = dict(evs[0]) if evs else None
    if last_ev: last_ev["age_min"] = round((now - last_ev["created_at"])/60)
    # parents
    par = con.execute("SELECT p.id,p.status,p.title FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?", (cid,)).fetchall()
    nchild_open = one(con, "SELECT COUNT(*) FROM task_links l JOIN tasks c ON c.id=l.child_id WHERE l.parent_id=? AND c.status NOT IN ('done','cancelled')", cid)
    # comments: latest few
    cms = con.execute("SELECT author, substr(body,1,160) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (cid,)).fetchall()
    n_lapor = one(con, "SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%' OR body LIKE '%LAPOR-SELESEI%')", cid)
    n_ack = one(con, "SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", cid)
    n_mark = one(con, "SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", cid)
    has_fase = one(con, "SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%[FASE]%'", cid)
    out.append({
        "id": cid, "title": t["title"][:90], "status": t["status"], "tenant": t["tenant"],
        "age_card_min": round((now - t["created_at"])/60),
        "last_ev": last_ev, "parents": [(p["id"], p["status"], p["title"][:60]) for p in par],
        "open_children": nchild_open, "lapor": n_lapor, "ack": n_ack, "marker": n_mark, "fase": has_fase,
        "comments": [dict(c) for c in cms],
        "classes": sorted({r["cls"] for r in rows if r["id"] == cid}),
    })

with open(r"C:/Users/TRIAL/AppData/Local/hermes/scripts/sysman_wake_cron_1014n_detail.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)

# ringkas per tenant
from collections import defaultdict
g = defaultdict(list)
for o in out:
    g[o.get("tenant") or "(no-tenant)"].append(o)
print("\n=== GROUP BY TENANT ===")
for ten, items in sorted(g.items(), key=lambda kv: -len(kv[1])):
    st = defaultdict(int)
    for i in items: st[i["status"]] += 1
    ages = [i["last_ev"]["age_min"] for i in items if i.get("last_ev")]
    print(f"{ten}: {len(items)} cards | status={dict(st)} | last-ev age min..max = {min(ages) if ages else '-'}..{max(ages) if ages else '-'} min")
    # sample titles
    for i in items[:3]:
        print(f"   e.g. {i['id']} [{i['status']}] {i['title']}")

# sanity papan hidup
print("\n=== SANITY ===")
print("max event age (min):", round((now - one(con, "SELECT MAX(created_at) FROM task_events"))/60))
print("tasks:", one(con, "SELECT COUNT(*) FROM tasks"), "| events:", one(con, "SELECT COUNT(*) FROM task_events"), "| comments:", one(con, "SELECT COUNT(*) FROM task_comments"))
run = con.execute("SELECT COUNT(*) FROM tasks WHERE status='running'").fetchone()[0]
print("running cards:", run)
