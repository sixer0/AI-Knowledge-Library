---
name: hermes-skill-activation
description: Activate all Hermes skills for a profile via snapshot sync.
version: 1.0.0
author: Hermes Agent (curator-managed)
license: MIT
metadata:
  hermes:
    tags: [hermes, skills, profile, snapshot, activation]
    related_skills: [hermes-agent, gsp-agent-hq-ops]
---

# Hermes Skill Activation

Class-level skill for diagnosing and bulk-activating the full Hermes skill library for a specific profile.

## When to Use

- User says `aktifkan seluruh skill`, `enable all skills`, `activate all skills`
- `hermes skills list` reports `0 enabled, 0 disabled` despite global install
- `hermes profile show <profile>` reports `Skills: 0`
- `.skills_prompt_snapshot.json` contains `{"skills": [], "manifest": {}}`

## Core Concepts

Hermes stores installed skills globally at `C:/Users/TRIAL/AppData/Local/hermes/skills/` (141+ skills, category-organized) but **activates** them per-profile via a prompt snapshot file:

- **Global source**: `C:/Users/TRIAL/AppData/Local/hermes/.skills_prompt_snapshot.json` — canonical 141-skill snapshot (version 2, `manifest` + `skills` array, ~158 manifest entries)
- **Per-profile target**: `C:/Users/TRIAL/AppData/Local/hermes/profiles/<profile>/.skills_prompt_snapshot.json`
- `hermes skills list` and `hermes profile show` count hub-installed skills, NOT snapshot-injected skills — they can show 0 even when snapshot is the real activation mechanism.

## Workflow

### 1. Diagnose

```bash
# Check per-profile snapshot
cat "C:/Users/TRIAL/AppData/Local/hermes/profiles/<profile>/.skills_prompt_snapshot.json"
# Check global snapshot health
python -c "import json; d=json.load(open('C:/Users/TRIAL/AppData/Local/hermes/.skills_prompt_snapshot.json')); print(len(d['skills']), len(d['manifest']))"
# Check profile status
hermes profile show <profile>
hermes skills list
# Count actual installed skills on disk
find "C:/Users/TRIAL/AppData/Local/hermes/skills" -name "SKILL.md" | wc -l
```

If target snapshot has `skills: []` and global has ~141 skills → proceed to sync.

### 2. Bulk-Activate (Snapshot Sync)

```bash
cp "C:/Users/TRIAL/AppData/Local/hermes/.skills_prompt_snapshot.json" \
   "C:/Users/TRIAL/AppData/Local/hermes/profiles/<profile>/.skills_prompt_snapshot.json"
```

This is the reliable workaround when `hermes skills config` / `hermes skills repair-official` do not populate the snapshot. Verified: copy yields immediate activation for next agent turn — no gateway restart required.

### 3. Verify

```bash
python -c "
import json
from collections import Counter
d=json.load(open('C:/Users/TRIAL/AppData/Local/hermes/profiles/<profile>/.skills_prompt_snapshot.json'))
print(f\"skills={len(d['skills'])} manifest={len(d['manifest'])}\")
print(Counter(s['category'] for s in d['skills']))
"
hermes profile show <profile>  # note: may still show Skills:0 — that's hub count, not snapshot
```

Expected after 2026-08-26 sync: `141 skills, 158 manifest entries` across ~23 category prefixes (gsp:36 is largest).

### 4. Explain to User

Report total and per-category breakdown. Offer to smoke-test a representative GSP skill via `skill_view`.

## Pitfalls

- **Do not rely on `hermes skills list` alone** — it reports hub-installed count, not snapshot-injected skills. Empty there does not mean activation failed.
- **Do not use `hermes skills repair-official all --restore` as first fix** — it backfills hub metadata, not the per-profile snapshot.
- **Do not create config.yaml manually** — profile may legitimately have no `config.yaml` (inherits defaults); snapshot is the activation file.
- **Preserve manifest timestamps** — copy file verbatim; do not regenerate manifest by hand (contains per-file mtime + size tuples).
- **Profile isolation matters** — source is always `C:/Users/TRIAL/AppData/Local/hermes/.skills_prompt_snapshot.json`, not `profiles/default/...`.

## References

- `references/snapshot-sync-2026-08-26.md` — session transcript and verification output for the 141-skill activation on `gsp-firman-custom`.
