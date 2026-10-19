# Aggregate wake eval JSON into compact per-tenant summary.
import json, collections
data = json.load(open("C:/Users/TRIAL/AppData/Local/hermes/scripts/_wake1410b_eval.json", encoding="utf-8"))
by_tenant = collections.defaultdict(list)
for r in data:
    by_tenant[r.get("tenant") or "(null)"].append(r)
for t, rows in sorted(by_tenant.items()):
    print(f"=== TENANT {t} ({len(rows)} kartu) ===")
    st = collections.Counter(r.get("status") for r in rows)
    print("  status:", dict(st))
    for r in sorted(rows, key=lambda x: x["id"]):
        toks = r.get("tok", {})
        line = (f"  {r['id']} [{r.get('status')}] age={r.get('age_min')}m children={r.get('n_child')} "
                f"ev={r.get('ev_hist','')[:70]} toks={ {k:v for k,v in toks.items() if v} }")
        print(line)
        if r.get("last_com"):
            print(f"     last_com: {r['last_com'][:150]}")
        if r.get("parents"):
            print(f"     parents: {r['parents']}")
    # sample titles
    print("  titles:")
    seen = set()
    for r in rows[:60]:
        ti = r.get("title","")
        if ti[:40] not in seen:
            seen.add(ti[:40])
            print(f"     {r['id']}: {ti}")
