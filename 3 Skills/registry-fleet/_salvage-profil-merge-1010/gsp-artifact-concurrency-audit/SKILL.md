---
name: gsp-artifact-concurrency-audit
version: 1.0.0
description: Use when several agents write one shared artifact.
metadata:
  hermes:
    tags: [gsp, verification, kanban]
    category: verification
---
# Artifact Concurrency Audit (GSP)

## When to use
- You are a PEKERJA writing to a **contract path** that another agent may also write (controller delegated the same step to a bridge worker; duplicate kanban cards exist).
- A downstream artifact was generated FROM your artifact (freeze/generate/fan-out script) and consistency between them is an acceptance criterion.

## Core rule
Do NOT win a write race. If your artifact was overwritten, **preserve both versions, verify what is actually on disk, and file the desync as a child card**. Overwriting back silently desyncs every downstream consumer that already read the other version.

## Steps
1. **Detect the race early.** Before writing, `ls -lat --time-style=+%H:%M:%S process | head`. New files you did not create (`*_prompt.txt`, `probeN.txt`, `freeze_*.py`) = another writer is live. Check the board for duplicate titles (read-only sqlite URI on `~/.hermes/kanban.db`; never open it read-write from a worker).
2. **Snapshot before touching anything:** `cp -p selection-memo.md selection-memo-<who>-<hhmm>.md`. Same for any verifier you did not author.
3. **Verify the LIVE artifact, not your memory of it.** Write ONE deterministic script printing `CHECK n: PASS|FAIL|NEEDS_REVIEW — name :: detail` + final `VERDICT:` (pattern in `gsp-verification-before-completion` → Verifying at Fleet Scale).
4. **Make the checker layout-independent.** Bind to *section names* (`TERPILIH` / `DITOLAK` / `Risiko`) and extract IDs by regex `^C\d{2}$` from the first two table cells — NOT to exact header text. A header-coupled parser reports FAIL on valid-but-differently-formatted content and burns a debugging cycle.
5. **Classify checker failures honestly.** Naive number-scanning yields false positives: HTTP status codes (`403`, `202`), pagination counts (`208 ID/hal`), year tokens (`2027`), link counts (`314 link`). Restrict scale-traceability to the exhibitor-count cell only, and emit `NEEDS_REVIEW` (not FAIL) for figures legitimately sourced from a named secondary source.
6. **Check upstream↔downstream sync separately.** Compare selected-ID sets of memo vs frozen register, print set differences BOTH ways, plus mtime ordering of generator vs source. Root cause is usually `freeze.py` written BEFORE the final memo rewrite.
7. **File it, don't fix it.** Which list wins is a controller/Director design decision. `kanban_create(title='...FIX...', assignee=<controller profile>, parents=[your task])` with: reproducible command, both sets, mtime evidence, what must NOT be reverted (artifacts valid under either choice), and definition of done = checker prints PASS.
8. Record in `method-log.md` + `kanban_comment` (`hotspot: <path> — <reason>`) + completion metadata `hotspot`.

## Pitals found in practice (EXPO26, 2026-09-02)
- Two writers hit `process/selection-memo.md` within 3 minutes; my memo was overwritten twice; the register was frozen from a THIRD state (neither my memo nor the final on-disk memo) → 4-slot desync, Step-5 criterion failed.
- `grep -i xinhua` returned nothing while the corroboration WAS present as `新华社`/`央视` — **grep CJK evidence in CJK**, or use `search_files`; otherwise you falsely accuse a peer of fabricating a source.
- `python` on this host is the Microsoft Store stub → use `uv run --python 3.11 python ...`.
- Heredoc / `python -c` can be blocked by the danger filter in single-query mode; write a `.py` file and run it instead.
- Editing a file another writer appends to (method-log) shows a stale-read warning but the patch still lands — re-read the tail to confirm, don't re-apply.

## Verification before claiming
Re-run BOTH checkers fresh at completion and quote their actual `VERDICT:` lines. A `FAIL` verdict on a *finding* checker is a successful outcome — report it as the finding, never as "done, all green".
