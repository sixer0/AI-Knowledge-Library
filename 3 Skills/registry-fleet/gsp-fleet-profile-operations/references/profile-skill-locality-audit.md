# Profile Skill-Locality Audit (recipe verified 2026-10-07, kartu t_7b6dcffe)

Question answered: "which skill improvements applied by profile X in the last N days exist ONLY on that profile (not global)?"

## Deterministic procedure (no LLM needed for the comparison itself)
1. Enumerate touched files per profile:
   `find "$LOCALAPPDATA/hermes/profiles/<p>/skills" -type f -mtime -N ! -name '*.lock' -printf '%TY-%Tm-%Td %TH:%TM | %p\n'`
   Exclude machine ledgers from substance counts: `.usage.json`, `.curator_ledger.jsonl`, `.curator*` snapshot dirs (timestamped names like `2026-10-05T08-03-47Z` — these parse as "skill names" if you split paths naively; filter them).
2. Resolve skill dir per file: first path component under [`skills/`](../../../kanonik/) is the skill UNLESS nested category layout exists (`skills/<category>/<skill>/SKILL.md` — real case: gsp-master01 has [`skills/gsp/gsp-doc-layout-gates`](../../gsp-doc-layout-gates/) AND `skills/verification/gsp-doc-layout-verification`). Walk up to the dir containing SKILL.md.
3. For each file compute sha256[:16] and compare against BOTH global sources:
   - registry fleet: `$LOCALAPPDATA/hermes/skills/gsp/<skill>/<relpath>`
   - canonical: `C:/Users/TRIAL/workspace/gsp-hermes/skills/<skill>/<relpath>` (find by dir name — categories differ between roots)
4. Verdict per file: GLOBAL-IDENTIK (sha match either source) / DRIFT (file exists globally, bytes differ) / PROFIL-LOKAL (absent from both).
5. Cross-check before reporting: randomly re-check ~5 PROFIL-LOKAL items with `find <global-root> -name <basename>` — guards against path-resolution false positives from step 2.
6. Whole-skill check: a skill dir present ONLY under a profile's skills/ = skill born locally (never distributed). Also compare the profile's SKILL.md sha vs fleet to separate "body rule deviation" (rare, serious) from "reference appendices lagging behind" (common, benign).

## Interpretation norms (what the user expects in the answer)
- Report per-profile totals + grouped listing of PROFIL-LOKAL items with dates, and explicitly state whether SKILL.md bodies are identical to global (sha values as proof).
- PROFIL-LOKAL items are promotion CANDIDATES, not defects. Correct next step per G-1 gate: one backflow proposal card to gsp-skill-manager (preseden 1.8.4: fleet->canonical flow-back verified byte-level, manager approves as-is). Controller must NOT silently copy them into registry/canonical.
- Pattern seen 07-10: controller-type profiles that run many missions accumulate fresh references in their own profile faster than the fleet absorbs backflow (gsp-master 0 local, gsp-master01 37 local). Two twin profiles can diverge sharply — always audit each profile matching the user's name pattern (`ls profiles | grep -i master` found gsp-master AND gsp-master01).

## Ops notes hit during this audit
- lad_card.py rejects assignee `brahma` (rebrand ghost) — controller-lane infra-ops cards go to `default`; the 'config profil default tidak terbaca -- fallback cap 500' warning is informational.
- A controller-authored card can get claimed by the dispatcher mid-work (claim 15-min window); closing after evidence is collected: `hermes kanban complete <id> --force --result "<bukti>"` is the sanctioned path (non-negotiable 4 / pitfall klaim-0509).
- psql is NOT on PATH on this host; query AgentRequest via HQ internal API instead: header `x-internal-secret: <INTERNAL_API_SECRET from gsp-datacenter/.env>` → `https://127.0.0.1:9011/api/brahma/requests?limit=100` (curl -sk mandatory, TLS self-signed).
- Kanban list JSON fields: timestamps are `started_at`/`created_at`/`completed_at` (no `updated_at`); `started_at` was empty on running cards — card age unmeasurable from board, treat as telemetry gap not failure.
- Bridge health cannot be read from `hermes-bridge/bridge*.out.log` when those files are stale (last write 16-09 despite live bridge.mjs pid) — verify bridge liveness by process + cards actually progressing, not log freshness.
