# Summarize wake eval JSON: group by tenant+class, flag false-positives.
import json, collections

data = json.load(open(r"C:/Users/TRIAL/AppData/Local/hermes/scripts/wake_eval_1014cron.json", encoding="utf-8"))
cards = data["wake_cards"]
print("board_alive_last_event_min:", data["board_alive_last_event_min"], "| total_events:", data["total_events"])

def klass(tid, c):
    if "error" in c: return "not-found"
    if c["status"] == "done":
        return "done-unacked"
    return "stalled-" + (c["status"] or "?")

groups = collections.defaultdict(list)
for tid, c in cards.items():
    groups[(c.get("tenant"), klass(tid, c))].append((tid, c))

for (tenant, k), items in sorted(groups.items(), key=lambda x: (str(x[0][0]), x[0][1])):
    print(f"\n=== tenant={tenant} class={k} n={len(items)} ===")
    for tid, c in sorted(items, key=lambda x: x[1]["title"]):
        par = ",".join(f"{p}:{s}" for p, s in c["parents"]) or "-"
        print(f"{tid} | {c['status']} | {c['last_ev_kind']}@{c['last_ev_age_min']}m | created {c['age_min_created']}m | kids {c['kids_open']}/{c['kids_total']} open | parents[{par}] | lap={c['lap_authors']}{c['lap_age_min']} ack={c['ack_n']}{c['ack_authors']} mk={c['marker_n']} | {c['title']}")
