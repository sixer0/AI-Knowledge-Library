#!/usr/bin/env python3
"""Monitor misi JIRA-CLONE-0908: cetak tabel status kartu misi (stabil byte utk hash-monitor cron)."""
import json, subprocess, sys

try:
    out = subprocess.run(["hermes", "kanban", "--board", "default", "list", "--json"],
                         capture_output=True, text=True, timeout=60).stdout
    d = json.loads(out)
    arr = d if isinstance(d, list) else d.get("tasks", [])
except Exception as e:
    print("MONITOR-ERROR %s" % e)
    sys.exit(0)

mine = [t for t in arr if "JIRA-CLONE-0908" in (t.get("title") or "")]
rows = []
for t in mine:
    rows.append("%s | %-22s | %-8s | %s" % (
        t.get("id"), (t.get("assignee") or "-")[:22], t.get("status"),
        (t.get("title") or "")[:78]))
print("JIRA-CLONE-0908 STATUS (%d kartu)" % len(mine))
for r in sorted(rows):
    print(r)
