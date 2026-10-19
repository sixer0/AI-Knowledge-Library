---
name: gsp-brahma-static-js-gates
description: gsp-brahma static JS edit? Run the skipped eslint gates.
---

# gsp-brahma static JS release gates (Windows)

Two release gates guard runtime-error classes in `static/*.js` beyond `node --check`:

1. `tests/test_static_js_runtime_lint.py` — eslint `no-const-assign` etc over all of `static/` (caught a real TypeError in WLP WP-C 5cf5048 that three impl runs missed because the gate silently skipped).
2. `tests/test_static_js_scope_undef.py` -> `scripts/scope_undef_gate.py` — cross-file `no-undef` over the shared classic-script global scope (#3696 brick class). Proves symbols used cross-file (e.g. outline.js using `_oldestIdx`, `_sameTranscriptMessage` from sessions.js) resolve.

## Pitfalls
- BOTH tests `pytest.skip` when eslint is absent — a green pytest run proves nothing. Install first:
  `npm install --no-save --before=<48h-ago> eslint`  (--no-save keeps package.json untouched)
- The pytest harness itself FAILS on Windows (`subprocess.run` gets a string arg — TypeError 'bytes args is not allowed on Windows'). Run the gates directly instead:
  - `node node_modules/eslint/bin/eslint.js --no-config-lookup -c eslint.runtime-guard.config.mjs static`
  - `PATH="$PWD/node_modules/.bin:$PATH" .venv/Scripts/python.exe scripts/scope_undef_gate.py .`  (exit 0 = clean; needs eslint on PATH)
- Repo venv is `.venv/Scripts/python.exe` (system python has no pytest).
- Targeted source-presence tests: `.venv/Scripts/python.exe -m pytest tests/test_issueNNNN_*.py -q`.

## Verification recipe for any static JS change
1. `node --check` each touched file.
2. eslint runtime-guard over whole `static/` (above) — must be CLEAN.
3. scope_undef_gate (above) — must print CLEAN.
4. Targeted pytest for the issue-numbered tests of touched features.
5. CSS edits: brace balance check (`tr -cd '{' < file | wc -c` vs `}`) + grep expected selector counts.
