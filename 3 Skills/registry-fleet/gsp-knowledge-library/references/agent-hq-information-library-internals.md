# Agent HQ Information Library — Verified Internals (2026-08-23)

Repo: `~/gsp-agent-headquarter` (Next.js :9011, Postgres `gsp_agent_hq`, hermes-bridge).

## Endpoints
- `GET /api/information-library?q=&scope=all|wiki|workspace&type=&status=active|all`
  → `{ entries, typeCounts, total, lastSync }`, `Cache-Control: no-store`.
  Serves from `src/app/api/information-library/route.ts`; UI polls every 10s.
- `GET /api/information-library/file?root=workspace|wiki&path=<rel>` → raw file, correct MIME
  (md/json/py/csv/txt→octet-stream), `Content-Disposition: inline`, `no-store`. Path-traversal outside root → 403.
- `POST /api/brahma/memory` (the WRITE path, see below).
- `/memory-wiki` → 308 redirect to `/information-library` (next.config.ts); sidebar label "Information Library".

## Wiki scope (DB) — how rows get there
- Source of truth: `.md` files in `~/.hermes/wiki` (`HERMES_WIKI` env). File frontmatter:
  `id, type, title, status, confidence, provenance, tags: [...], links: [...], updated: YYYY-MM-DD` + markdown body.
- `hermes-bridge/bridge.mjs`: `mirrorWiki()` walks `~/.hermes/wiki`, `parseEntry()` → UPSERT into
  `HermesMemory` (id = rel path minus `.md`), then **DELETE rows whose id is not in the vault**.
  → DB is a pure mirror; a row with no vault file vanishes next tick. `writeWikiEntry(e)` writes the file
  (path default `${type}s/${id}.md`); `gitCommitWiki()` runs git init/add/commit in the wiki dir.
- As of 2026-08-23 `~/.hermes/wiki` is empty → wiki scope returns 0 entries.

## Workspace scope (filesystem, read-only)
- Root `SHARED_WORKSPACE` env, default `~/workspace/gsp-hermes/workspace` (AGENTS.md, MEMORY.md, memory/, docs/).
- `walkMd()` recursive scan of `.md|.markdown|.mdx`, SKIP dirs: `node_modules .git .next dist build .cache __pycache__ .venv venv`.
- Title = first `# ` heading, fallback basename. Type inferred from path (`inferType`):
  `refs/lesson`→lesson · `tasks/report`→project · `docs/decision`→decision · `log|memory/`→note · `agents.md|memor*`→fact · else note.
- Body capped 6000 chars + `…(dipotong)`. `docs/[date]_[task]/` folders containing non-md artifacts → one
  `project` entry per folder with `files[]` (rel paths, size KB) + body listing up to 60 files.
- Search `q` matches `path + title + body` (workspace) / `title+body+tags` (wiki, insensitive).
- Entries merged, sorted `updatedAt` desc. Workspace entries are read-only in UI (provenance `shared-workspace`).

## The write path ("injection") that needs a gate
```
UI "New entry"/"Edit" → POST /api/brahma/memory {id,path,type,title,body,tags,status,confidence}
→ prisma.agentRequest.create({ kind:"memory.write", origin:"web", status:"queued", prompt:JSON(entry) })
→ bridge runRequest(): kind==="memory.write" → writeWikiEntry(e) → gitCommitWiki → mirrorWiki() → HermesMemory
```
No curation, no verification, no provenance enforcement, no dedup. Anyone (dev-mode, no auth) can write.
This is exactly the "inject by data" the user wants replaced by a gatekeeper agent (see SKILL.md GSP convention).

## Notes for routing work
- Profile dispatch already exists in the bridge: `AgentRequest.profile` set → `hermes -p <profile> -z <prompt>`,
  records OrchestrationRecord edge `brahma → <profile>` (kind dispatch), creates+closes a real kanban card,
  reads semantic status from agent response (`STATUS: blocked|needs-review|failed|complete`), sets AgentState.
  Per-request timeout `RUN_TIMEOUT_MS` default 1800s (env `BRIDGE_RUN_TIMEOUT_MS`).
- This is the natural mechanism to route library proposals to a `gsp-librarian` profile for attestation.
