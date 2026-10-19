#!/usr/bin/env python3
"""rafi_1004_watch.py — digest stabil papan RAFAI-1004 untuk monitor cron board-mover.
Output deterministik (tanpa timestamp): hash berubah hanya saat keadaan papan/artefak berubah."""
import json, subprocess, os

DOCS = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-10-04-rafif-ai-manual"

def board():
    r = subprocess.run("hermes kanban --board default list --json", shell=True,
                       capture_output=True, text=True, timeout=120)
    try:
        return json.loads(r.stdout)
    except Exception:
        return []

mine = [t for t in board() if "RAFAI-1004" in (t.get("title") or "")]
lines = []
for t in sorted(mine, key=lambda x: x["id"]):
    lines.append(f"{t['id']}|{t['status']}|{t.get('assignee','')}|{t['title'][:60]}")
for sub in ["identification", "research", "masterplan", "output"]:
    d = os.path.join(DOCS, sub)
    if os.path.isdir(d):
        for root, dirs, files in os.walk(d):
            for f in sorted(files):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, DOCS).replace("\\", "/")
                lines.append(f"A|{rel}|{os.path.getsize(p)}")
print("\n".join(lines) if lines else "NO-CARDS-YET")
