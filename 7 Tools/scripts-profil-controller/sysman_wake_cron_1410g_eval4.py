# Read-only: why did the 24 M4 resume cards go blocked ~5 min ago?
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

def age(ts):
    return round((NOW - ts) / 60.0, 1) if ts else None

ids = ["t_0913266d","t_0918b6d2","t_0ac8927f","t_0f3e37eb","t_19930381","t_5291d587",
"t_5715d1fc","t_6aa0384c","t_7124c228","t_7707a0cd","t_7f36de9e","t_80a9fb43",
"t_896447e4","t_99bb85a4","t_a148a692","t_a66ce30a","t_ad5d8e6f","t_b2b82e31",
"t_c2180f14","t_ccfca3b8","t_de326482","t_de73c01d","t_deb670d0","t_ed8b0b54"]

# Sample 3 cards: last blocked event payload + all comments
for tid in ids[:3]:
    print("==== ", tid)
    evs = cur.execute("SELECT kind,payload,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)).fetchall()
    for e in evs:
        print("   ev %s age=%s payload=%s" % (e["kind"], age(e["created_at"]), (e["payload"] or "")[:220]))
    cs = cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (tid,)).fetchall()
    for c in cs:
        print("   cm [%s] age=%s: %s" % (c["author"], age(c["created_at"]), c["body"][:220].replace("\n", " | ")))

# Aggregate: who wrote the blocked event (payload actor?) across all 24
from collections import Counter
kinds = Counter(); actors = Counter(); reasons = Counter()
for tid in ids:
    e = cur.execute("SELECT kind,payload,created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    if e:
        kinds[e["kind"]] += 1
        p = e["payload"] or ""
        import json as _j
        try:
            pj = _j.loads(p)
            actors[str(pj.get("actor") or pj.get("by") or pj.get("author") or "?")] += 1
            rsn = str(pj.get("reason") or pj.get("note") or "")[:60]
            reasons[rsn] += 1
        except Exception:
            actors["unparsed"] += 1
print("== blocked-event actors:", dict(actors))
print("== blocked-event reasons:")
for k, v in reasons.most_common(8):
    print("   %3d x %s" % (v, k))

# Comment authors on these cards (any controller assessment after block?)
cm_authors = Counter()
for tid in ids:
    for c in cur.execute("SELECT author FROM task_comments WHERE task_id=?", (tid,)).fetchall():
        cm_authors[c["author"]] += 1
print("== comment authors across 24:", dict(cm_authors))
con.close()
