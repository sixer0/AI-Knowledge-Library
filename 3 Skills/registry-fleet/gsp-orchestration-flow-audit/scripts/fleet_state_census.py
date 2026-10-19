#!/usr/bin/env python3
"""Fleet state census - one-shot read-only audit of orchestration flow.

Measures: kanban board (status/assignee/blocked-age/title buckets),
cross-profile cron inventory (jobs.json files, NOT the cronjob tool),
mission docs folders, and fleet scripts dir. Prints JSON to stdout.

Usage: python fleet_state_census.py [--docs PATH] [--scripts PATH]
Read-only: no writes, no board mutations.
"""
import json, os, re, sys, glob, subprocess, collections, datetime

LA = os.environ.get("LOCALAPPDATA") or r"C:\Users\TRIAL\AppData\Local"
DOCS_DEFAULT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs"
SCRIPTS_DEFAULT = r"C:/Users/TRIAL/workspace/gsp-hermes/scripts"

BUCKETS = {
    "RT-like": r"\bRT\b|translate|terjemah|request.?translat",
    "TA-like": r"\bTA\b|blueprint|structured|architect",
    "verifikasi/verdict": r"VER-|\[VER|\bverdict\b|counter.?sign|spot.?audit|juri|jury|verif",
    "fix/rework": r"\bfix\b|perbaikan|tambal|karantina|healing|rework|revise|revisi",
    "audit/sweep": r"audit|scan|sweep|sapuan|inventaris",
    "triase/rekonsiliasi": r"triase|triage|rekonsiliasi|reconcile",
    "watchdog/monitor": r"watchdog|monitor|heartbeat|progress report|cek progres",
    "sync NAS/email": r"sync.?(email|nas)|nas.?(sync|pagi|malam)",
    "gateway/fleet-check": r"gateway|fleet.?check|invarian|INV-",
    "gelombang/dispatch": r"gelombang|wave|dispatch|batch",
    "naturalisasi": r"natural|gate.?nat",
    "restart/deploy": r"restart|deploy|rollout|provisioning",
}

def kanban():
    out = subprocess.run(["hermes", "kanban", "--board", "default", "list", "--json"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    cards = json.loads(out.stdout)
    st = collections.Counter(c.get("status") for c in cards)
    asg = collections.Counter(str(c.get("assignee")) for c in cards)
    profs = set(os.listdir(os.path.join(LA, "hermes", "profiles")))
    dead = {a: n for a, n in asg.items() if a != "None" and a not in profs}
    empty = asg.get("None", 0)
    now = datetime.datetime.now().timestamp()
    blocked = []
    for c in cards:
        if c.get("status") == "blocked":
            t = c.get("completed_at") or c.get("started_at") or c.get("created_at") or 0
            age_d = (now - t) / 86400 if t else -1
            blocked.append([c["id"], round(age_d, 1), (c.get("title") or "")[:70]])
    buckets = collections.Counter()
    for c in cards:
        title = (c.get("title") or "").lower()
        for k, p in BUCKETS.items():
            if re.search(p, title):
                buckets[k] += 1
    return {"total": len(cards), "status": dict(st),
            "assignee_dead_or_missing": {**{("DEAD:" + k): v for k, v in dead.items()},
                                          "EMPTY(None)": empty},
            "blocked_age_days": sorted(blocked, key=lambda x: -x[1]),
            "title_buckets_regex_approx": dict(buckets.most_common())}

def cron():
    paths = [os.path.join(LA, "hermes", "cron", "jobs.json")] + \
            glob.glob(os.path.join(LA, "hermes", "profiles", "*", "cron", "jobs.json"))
    rows = []
    for p in paths:
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        jobs = d if isinstance(d, list) else d.get("jobs", [])
        owner = p.split(os.sep)[-3] if "profiles" in p else "MAIN"
        for j in jobs:
            sch = j.get("schedule") or {}
            rows.append({"owner": owner, "name": j.get("name"),
                         "sched": sch.get("display") if isinstance(sch, dict) else sch,
                         "enabled": j.get("enabled", True), "no_agent": j.get("no_agent"),
                         "script": j.get("script")})
    agent_runs = [r for r in rows if r["enabled"] and not r["no_agent"]]
    return {"total_jobs": len(rows), "agent_run_jobs": len(agent_runs),
            "note": "cronjob tool shows only active profile; jobs.json files are ground truth",
            "jobs": rows}

def docs(path):
    if not os.path.isdir(path):
        return {"error": "docs path missing: " + path}
    entries = os.listdir(path)
    folders = [e for e in entries if os.path.isdir(os.path.join(path, e))]
    pat = {"sync-email-nas": r"sync-email-nas", "gateway": r"gateway",
           "draf-vN": r"draf-v\d", "triase": r"triase|triage",
           "knowledge-register": r"knowledge-register", "watchdog": r"watchdog"}
    counts = {k: sum(1 for d in folders if re.search(p, d)) for k, p in pat.items()}
    return {"entries": len(entries), "folders": len(folders),
            "with_contract_md": sum(1 for d in folders if os.path.isfile(os.path.join(path, d, "contract.md"))),
            "with_identification": sum(1 for d in folders if os.path.isdir(os.path.join(path, d, "identification"))),
            "with_phase_reports": sum(1 for d in folders if os.path.isfile(os.path.join(path, d, "PHASE-REPORTS.md"))),
            "recurring_name_patterns": counts}

def scripts(path):
    if not os.path.isdir(path):
        return {"error": "scripts path missing: " + path}
    names = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    dated = [f for f in names if re.search(r"20\d{4}", f)]
    oneoff = [f for f in names if re.match(r"(install_|rollout_|lean_|fix_fleet|amend_|probe_|cmp_|optwf_)", f)]
    return {"files": len(names), "dated_once_pakai": len(dated), "rollout_class": len(oneoff)}

def main():
    docs_p, scr_p = DOCS_DEFAULT, SCRIPTS_DEFAULT
    args = sys.argv[1:]
    if "--docs" in args:
        docs_p = args[args.index("--docs") + 1]
    if "--scripts" in args:
        scr_p = args[args.index("--scripts") + 1]
    report = {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
              "kanban": kanban(), "cron": cron(), "docs": docs(docs_p),
              "scripts": scripts(scr_p)}
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))

if __name__ == "__main__":
    main()
