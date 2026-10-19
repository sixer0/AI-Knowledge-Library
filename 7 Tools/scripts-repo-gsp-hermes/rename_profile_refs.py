#!/usr/bin/env python3
"""Replace gsp-vendor-crawler-orchestrator -> gsp-crawler-orchestrator across
profiles + workspace, skipping binary/log/historical files."""
import os, re

HH = os.path.expandvars(r'%LOCALAPPDATA%\hermes')
ROOTS = [os.path.join(HH, 'profiles'),
         r'C:\Users\TRIAL\workspace\gsp-hermes',
         os.path.join(HH, 'memories'),
         os.path.join(HH, 'skills')]
SKIP_DIR_PARTS = ('logs', '.git', '__pycache__', 'sessions', 'audio_cache')
SKIP_EXT = ('.db', '.sqlite', '.sqlite3', '.jsonl', '.log', '.pid', '.lock', '.pyc', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico')

PAIRS = [
    ('gsp-vendor-crawler-orchestrator', 'gsp-crawler-orchestrator'),   # full name first
    ('vendor-crawler-orchestrator', 'crawler-orchestrator'),           # then short name
    ('Vendor Crawler Orchestrator', 'Crawler Orchestrator'),           # prose title case
]

changed = []
skipped = []
for root in ROOTS:
    if not os.path.isdir(root):
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        if any(s in dirpath.replace('\\', '/').split('/') for s in SKIP_DIR_PARTS):
            continue
        for fn in filenames:
            if fn.endswith(SKIP_EXT):
                continue
            if fn in ('gateway.pid', 'gateway.lock', 'gateway_state.json'):
                skipped.append(os.path.join(dirpath, fn))
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    txt = f.read()
            except Exception:
                continue
            new = txt
            for old, neww in PAIRS:
                new = new.replace(old, neww)
            if new != txt:
                with open(path, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(new)
                changed.append(path)

print(f"changed: {len(changed)} files")
for c in changed:
    print('  ', c.replace(HH, '~HH'))
print(f"\nskipped (runtime artifacts, deleted separately): {len(skipped)}")
