# Recheck Probes — working recipes (validated 2026-08-30, Windows host, GSP fleet)

All probes run inside `execute_code` (stdlib only). Print one `CHECK n: PASS|FAIL|INFO — name` line per probe so the report table maps 1:1 to evidence.

## 0. Large-HTML section extractor (multi-MB audit docs)

`read_file` truncates; open directly and slice by heading anchor:

```python
import re, html
text = open(SRC, encoding="utf-8", errors="replace").read()

def section(anchor_id):
    m = re.search(r'<h[234][^>]*id="%s"' % re.escape(anchor_id), text)
    if not m: return ""
    start = m.start()
    m2 = re.search(r'<h[23][^>]*id="', text[start+10:])
    end = start + 10 + (m2.start() if m2 else 20000)
    return text[start:end]

def totext(h):
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', h, flags=re.S)
    h = re.sub(r'</(tr|p|li|h[1-6]|div|table)>', '\n', h)
    h = re.sub(r'</t[dh]>', ' | ', h)          # keep table cells readable
    h = re.sub(r'<[^>]+>', '', h)
    h = html.unescape(h)
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'[ \t]+', ' ', h)).strip()

# First pass: dump the TOC to pick anchors
for tag, hid, inner in re.findall(r'<(h[234])[^>]*id="([^"]*)"[^>]*>(.*?)</\1>', text, re.S):
    print(tag, hid, totext(inner))
```

Typical anchors to pull (GSP-QA-001 naming): summary (`s-7-1`), operational warning (`s-7-2`), unfinished migration (`s-7-3`), remediation waves (`s-7-7`).

## 1. Fleet shape snapshot

```python
import os
LA = os.environ["LOCALAPPDATA"]; home = os.path.join(LA, "hermes")
prof_dir = os.path.join(home, "profiles")
profiles = [d for d in os.listdir(prof_dir) if os.path.isdir(os.path.join(prof_dir, d))]
# gsp-* subset, fleet shared skills tree, per-profile skill dirs — count all three separately
```

## 2. Drift: repo vs live (SHA-256 tree comparison)

```python
import hashlib, os
def sha(p):
    try: return hashlib.sha256(open(p,'rb').read()).hexdigest()
    except Exception: return None
def skill_dirs(root):   # any dir containing SKILL.md
    out = {}
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('.git','__pycache__','.curator_backups','node_modules')]
        if 'SKILL.md' in files:
            out[os.path.relpath(r, root).replace('\\','/')] = r
    return out
def tree_index(root):
    idx = {}
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('.git','__pycache__','.curator_backups','node_modules')]
        for f in files:
            fp = os.path.join(r, f)
            idx[os.path.relpath(fp, root).replace('\\','/')] = sha(fp)
    return idx
# Match by skill BASENAME; classify: identical / modified / deployed-only / repo-only.
# Report all four counts + denominators. deployed-only >> repo-only => repo is not source of truth.
```

Also probe `os.path.isdir(os.path.join(repo, ".git"))` — no-git repo upgrades "seal into version control" to top of work list.

## 3. Skill description length (INV-1 / C-DESC-60)

Folded `>-` blocks MUST be joined before measuring:

```python
import re
def fm_desc(md):
    t = open(md, encoding="utf-8", errors="replace").read()
    m = re.match(r'^---\s*\n(.*?)\n---', t, re.S)
    if not m: return None
    fm = m.group(1)
    dm = re.search(r'^description:\s*(?:>\-?|\|)?\s*\n((?:[ \t]{2,}.*\n?)+)', fm, re.M)
    if dm: return " ".join(l.strip() for l in dm.group(1).splitlines())
    dm = re.search(r'^description:\s*(.+)$', fm, re.M)
    if dm:
        s = dm.group(1).strip()
        if s[:1] in ('"',"'") and s[-1:]==s[:1] and len(s)>1: s = s[1:-1]
        return s
    return ""
# Count instances >60 (index truncation) and >1024 across fleet tree + all profile trees.
```

## 4. Cross-skill citations (C-REF-XSKILL)

```python
pat = r'`?(?:\$HERMES_SKILL_DIR/)?skills/([a-z0-9-]+)/([^`\s)]+\.(?:md|py|json|ya?ml|csv|xlsx))`?'
# count tapak across fleet-tree .md files; sample a few hits — many are doc examples, mark "needs triage"
```

## 5. Cron evidence (disk beats self-report)

```python
import json, os, glob, datetime
jobs = json.load(open(os.path.join(home,"cron","jobs.json"), encoding="utf-8"))
jl = jobs if isinstance(jobs, list) else jobs.get("jobs", jobs)
for j in (jl.values() if isinstance(jl, dict) else jl):
    # print id, name, last_status, failure_streak, enabled
    out = os.path.join(home, "cron", "output", str(j.get("id","")))
    # if dir exists: newest file by mtime, grep tail for "failed"/"RuntimeError"/"execvpe"
```

Known failure signature: `RuntimeError: [drift_skip:silent] ... job is unpinned` → fix with `hermes cron edit <id> --provider <p> --model <m>`. Check EVERY recurring job for pin state when one shows this.

## 6. Leftover migration paths

```python
# grep config.yaml + SOUL.md of every profile for old-host prefixes ("/Users/mbp", legacy usernames)
# read gateway_state.json: hermes_home + argv[0] must point at THIS host
```

## 7. Duplicate asset size (W7-style cost findings)

```python
import glob
hits = glob.glob(os.path.join(home, "**", "<asset-dir-name>"), recursive=True)
# per-hit: sum(os.path.getsize) over walk; report count x MiB vs audit's claim
```

## Reporting skeleton

Markdown table: `| # | Temuan audit | Status sekarang | Bukti (tanggal) |` followed by numbered work list grouped by the audit's wave labels (W0 gate first, actively-broken item at #1 overall), closing with the audit's forbidden-actions reminders. Save under shared-ws `docs/`.
