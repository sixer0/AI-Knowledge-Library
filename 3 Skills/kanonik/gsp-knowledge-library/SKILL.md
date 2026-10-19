---
name: gsp-knowledge-library
description: "GSP knowledge library: HQ Information Library + IL project."
version: 1.0.0
author: GSP
license: MIT
platforms: [macos, linux]
metadata:
  gsp:
    category: knowledge
    tags: [gsp, library, wiki, information-library, curation, gatekeeper, agent-headquarter]
---

# GSP Knowledge Library

## When to Use

Work on the GSP knowledge library: the Agent HQ **Information Library** page (wiki + workspace), the `information-library` project (F9 of SOP 011/GSP/KT/VIII/2026 Rev A), deciding how knowledge enters the library, or building curation/gatekeeping for it. Also load before proposing any change to how wiki/library writes happen.

## Core facts (verified 2026-08-23)

### Agent HQ Information Library — one page, two sources
- Page `/information-library` (old `/memory-wiki` → 308 redirect). Main API `GET /api/information-library` in `~/gsp-agent-headquarter/src/app/api/information-library/route.ts`. UI: `src/app/information-library/page.tsx`.
- **Wiki scope** = `HermesMemory` table in Postgres `gsp_agent_hq`, mirrored by `hermes-bridge` from `~/.hermes/wiki` (`.md` files; frontmatter `id/type/title/status/confidence/provenance/tags/links/updated`). The DB is DERIVED: `mirrorWiki()` UPSERTs and **DELETEs** rows whose id is no longer in the vault — hand-written rows with no vault file vanish on next mirror.
- **Workspace scope** = read-only scan of `~/workspace/gsp-hermes/workspace` (AGENTS.md, MEMORY.md, memory/, docs/) on every request; title from first `#` heading, type inferred from path, body capped 6000 chars with `…(dipotong)` marker, `docs/[date]_[task]/` folders with non-md artifacts become `project` entries with `files[]`. Skips `node_modules/.git/.next/dist/build/.cache/.venv`.
- File endpoint `/api/information-library/file?root=workspace|wiki&path=` serves raw files with proper MIME; path-traversal outside root → 403.
- **INJECTION PATH (the thing to gate):** UI "New entry" → `POST /api/brahma/memory` → creates `AgentRequest kind=memory.write, status=queued` → bridge `writeWikiEntry()` writes `.md` to wiki + git commit + `mirrorWiki()` → DB. **No curation/verification step.** Anyone (dev mode) can write.
- Full internals: `references/agent-hq-information-library-internals.md`.

### The IL project (F9) — principles to carry into HQ
`/Users/mbp/Documents/Project/information-library` — classified knowledge substrate for GSP (Obsidian vault + SQLite + Python; CLI, FastAPI, HTMX UI, MCP). Milestones M1–M8; M4 (API) + M5 (7 UI surfaces) done. Five non-negotiable principles:
1. **Vault is source of truth** — DB always rebuildable from vault; only non-rebuildable facts (tokens, attestation chain, issued numbers) live in a separate registry DB.
2. **Isolation is files, not WHERE clauses** — one file per tenant, per case.
3. **Numbers without page citation = nonexistent** — provenance (source, page, access date, evidence class) is the only rigidity on data.
4. **Verification not by the author** — attestation gate (single door into corpus), review band, curator + independent reviewers.
5. **Schema observed, not declared** — system infers the catalog from what is actually written.

Derived operational principles worth reusing: honesty panel ("Yang tidak Anda lihat" — drawn/alias/evidence-gap counts), gates validate input shape *before* comparing (`cap ≤ 500` was bypassed with negative `-2`), end-to-end assertions with credentials per pipeline arm (module passing own tests while uncalled = hidden failure), spec-first (code deviating from spec is a defect; schema generated from spec), performance measured at two scales demanding a ratio not a constant, classification filters rather than rejects (rejecting leaks existence). Full deep-dive: `references/information-library-project.md`.

## GSP convention — knowledge enters via a gatekeeper, not injection

The user was explicit (2026-08-23): integration into the library/wiki must **NOT** be manual or data-injection. It must be **processed by a dedicated gatekeeper agent profile** — a `gsp-librarian` (design under discussion) that curates, verifies, attests, and decides before anything lands in the library. Do **not** propose direct UI/API writes to the wiki as the solution. Vault (`.md` files) stays the source of truth; DB stays a derived mirror. Proposed shape: `POST /api/brahma/memory` → dispatch `oneshot` with `profile=gsp-librarian` → librarian writes the curated `.md` → bridge mirrors → DB. Status: **design only, NOT yet implemented** as of 2026-08-23.

## Pitfalls

- **Never propose data-injection integration** for the library (e.g. UI writing straight to HermesMemory/wiki) — the user explicitly rejected that direction and redirected to an agent gatekeeper.
- **Wiki DB is a pure mirror:** `mirrorWiki()` DELETEs `HermesMemory` rows whose id is not in `~/.hermes/wiki`. Writing rows with no vault file = they disappear on next mirror tick.
- **Don't claim a design works until verified end-to-end** (profile created via generator, dispatch ran, entry attested). The librarian design was under discussion, not implemented — do not present it as a working workflow.
- **Fleet profile/skill changes go through the official path** (see `gsp-profile-management`): manifest → `generate_profiles.py` → validator → `add_hq_roster.py` → watchdog. Never edit profile SOUL/skills directly.

## References

- `references/information-library-project.md` — IL project deep-dive: architecture, module map, milestone docs, decision patterns.
- `references/agent-hq-information-library-internals.md` — verified HQ internals: endpoints, mirror flow, wiki file format, workspace scan rules.
