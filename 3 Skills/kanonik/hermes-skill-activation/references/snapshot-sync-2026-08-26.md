# Snapshot Sync — 2026-08-26 — gsp-firman-custom (141 skills)

## Session Context

- **Profile**: `gsp-firman-custom` (active WebUI workspace `C:\Users\TRIAL\workspace`)
- **Request**: `aktifkan seluruh skill` (Indonesian: activate all skills)
- **Initial state**:
  - `hermes skills list` → `0 hub-installed, 0 builtin, 0 local — 0 enabled, 0 disabled`
  - `hermes profile show gsp-firman-custom` → `Skills: 0`
  - `profiles/gsp-firman-custom/.skills_prompt_snapshot.json` → `{"version":2,"manifest":{},"skills":[],"category_descriptions":{}}`
  - Global [`C:/Users/TRIAL/AppData/Local/hermes/skills/`](../../../registry-fleet/) → 141 SKILL.md files across 19 top-level categories
  - Global canonical snapshot `C:/Users/TRIAL/AppData/Local/hermes/.skills_prompt_snapshot.json` → `141 skills, 158 manifest entries` (verified via Python json load)

## Diagnosis Steps Taken

1. Checked profile snapshot — empty.
2. Checked global snapshot — healthy (141 skills).
3. Listed global skills by category: `apple 4, autonomous-ai-agents 7, creative 16, database/* 7, devops 2, email 2, github 8, gsp 36, hermes 1, media 4, mlops 5, note-taking 2, orchestration 6, productivity 18, research 7, smart-home 1, social-media 1, software-development 11, data-science 1, yuanbao 1`.
4. Confirmed `hermes skills config --help` gives no actionable bulk-enable; `hermes skills repair-official` operates on hub metadata, not snapshot.
5. `config.yaml` absent for `gsp-firman-custom` — normal (inherits defaults), not the activation file.

## Fix Applied

```bash
cp "C:/Users/TRIAL/AppData/Local/hermes/.skills_prompt_snapshot.json" \
   "C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-firman-custom/.skills_prompt_snapshot.json"
```

Result: `COPIED OK` → profile now reports `141 skills, 158 manifest entries` (same Counter breakdown as above). `gsp` largest with 36 skills: `analytics-and-reporting`, `cctv-system-designer`, `crawl4ai-skill`, `crawler`, `dems-polri-proposal-architect`, etc.

## Verification Output

```
Profile now has 141 skills, 158 manifest entries
apple-notes apple
apple-reminders apple
findmy apple
...
hermes profile show → still Skills:0 (expected — that's hub count, not snapshot)
```

Next agent turn will have all 141 skills prompt-injected.

## Lesson

Bulk activation for isolated profiles is a **file sync**, not a CLI flag. The snapshot file is the source of truth for prompt injection. Always copy verbatim to preserve `manifest` mtime+size tuples. Do not regenerate manifest manually.

## Reproduction Recipe

For any future profile `<new-profile>` showing 0 skills:

```bash
python -c "import json; print(json.load(open('C:/Users/TRIAL/AppData/Local/hermes/.skills_prompt_snapshot.json'))['skills'][:1])"
cp "C:/Users/TRIAL/AppData/Local/hermes/.skills_prompt_snapshot.json" "C:/Users/TRIAL/AppData/Local/hermes/profiles/<new-profile>/.skills_prompt_snapshot.json"
python -c "import json; d=json.load(open('C:/Users/TRIAL/AppData/Local/hermes/profiles/<new-profile>/.skills_prompt_snapshot.json')); print(len(d['skills']))"
```
