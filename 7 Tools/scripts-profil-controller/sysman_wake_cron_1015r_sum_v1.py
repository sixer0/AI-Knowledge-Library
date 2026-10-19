# -*- coding: utf-8 -*-
# Ringkas hasil evaluasi ronde wake 15-10 sore.
import json, collections
d = json.load(open("C:/Users/TRIAL/AppData/Local/hermes/scripts/sysman_wake_cron_1015r_eval_out.json", encoding="utf-8"))
cards = d["cards"]
print("board_last_event_min_ago:", d["board_last_event_min_ago"])
print("status_census:", d["status_census"])
print("timeout_kinds:", d["timeout_kinds"])
print("n_cards:", len(cards))
st = collections.Counter((c.get("status"), c.get("tenant")) for c in cards)
print("by status/tenant:", dict(st))
# parent pattern check: every card has 1 blocked parent + 1 done [M4] parent?
pat = collections.Counter()
for c in cards:
    ps = sorted(p["status"] for p in c.get("parent_status", []))
    pat[tuple(ps)] += 1
print("parent-status patterns:", dict(pat))
# any card with own comments/flags?
flagged = [c["id"] for c in cards if c.get("n_comments")]
print("cards_with_own_comments:", flagged)
# blocked parents census
blocked_parents = {}
for c in cards:
    for p in c.get("parent_status", []):
        if p["status"] == "blocked":
            blocked_parents[p["id"]] = p["title"]
print("n_blocked_parents:", len(blocked_parents))
print("sample blocked parents:", list(blocked_parents.items())[:3])
# replacements section (Digantikan markers) - on the todo cards themselves none; check separately below
print("replacements_on_todo_cards:", d.get("replacements"))
print("tenant_census:", json.dumps(d.get("tenant_census"), indent=1))
