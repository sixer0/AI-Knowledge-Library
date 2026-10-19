# Aggregate WAKE eval output by tenant + class (read-only)
import json, collections, time

data = json.load(open("C:/Users/TRIAL/AppData/Local/hermes/scripts/sysman_wake_eval_1014b_out.json", encoding="utf-8"))

by_tenant = collections.defaultdict(list)
for cid, d in data.items():
    by_tenant[d.get("tenant") or "(null)"].append((cid, d))

NOW = int(time.time())
summary = {}
for ten, items in sorted(by_tenant.items()):
    st = collections.Counter(d["status"] for _, d in items)
    wakek = collections.Counter(k for _, d in items for k in d["wake_kinds"])
    # parent status census for stalled cards
    parent_running = 0
    parent_other = []
    anchors = []
    for cid, d in items:
        if "stalled" in d["wake_kinds"]:
            if d["body_markers"]["ANCHOR"]:
                anchors.append(cid)
            for p in d["parents"]:
                if p["status"] == "running":
                    parent_running += 1
                else:
                    parent_other.append((cid, p["id"], p["status"]))
    summary[ten] = {
        "n_wake_cards": len(items),
        "status_census": dict(st),
        "wake_kinds": dict(wakek),
        "stalled_with_running_parent": parent_running,
        "stalled_parents_notrunning_sample": parent_other[:6],
        "anchor_cards": anchors,
        "assignees": dict(collections.Counter(d["assignee"] for _, d in items)),
        "created_by": dict(collections.Counter(d["created_by"] for _, d in items)),
        "sample_titles": [d["title"][:70] for _, d in items[:4]],
        "max_age_min": max(d["max_age"] for _, d in items),
    }
print(json.dumps(summary, indent=1))

# per-card condensed table
print("\n=== PER CARD ===")
for cid, d in sorted(data.items(), key=lambda kv: (str(kv[1].get("tenant")), kv[0])):
    lastev = d["last_events"][0] if d["last_events"] else None
    run0 = d["runs"][0] if d["runs"] else None
    print(json.dumps({
        "id": cid, "tenant": d["tenant"], "title": d["title"][:60], "status": d["status"],
        "wake": d["wake_kinds"], "age": d["max_age"],
        "last_ev": (lastev["kind"], lastev["age_min"]) if lastev else None,
        "ncom": d["n_comments"],
        "last_com": [(c["author"], c["age_min"], c["head"][:80]) for c in d["comments"][:2]],
        "parents": d["parents"], "kids": dict(d["kids_status"]),
        "run0": run0,
        "anchor": d["body_markers"]["ANCHOR"],
    }))
