# Pin and Handshake Check (first recipe, always before scene commands)

Purpose: establish supply-chain identity and addon/server protocol agreement
before a single command mutates a scene. A stale handshake or missing listener
later reads as a dead tool (FC-01, FC-03, FC-32). Register anchors: AN-01-01
through AN-01-10 in references/number-register.md. Known limitation of this
recipe: the numbers cited are pins of 2026-10-16 and go stale with the next
release wave (16 releases in 34 days, AN-01-01), so a step that passes today
without re-reading the register is already deprecated by construction.

Dependencies stated, never assumed: Python 3.11+ with `uv` OR pip, network
access to PyPI for the identity check, Blender 5.2.x GUI on the target host.
Steps 5-6 need the MCP client session; steps 1-4 run in any shell.

1. Pin the supply chain as a TRIPLE before anything installs:
   - canonical package name `mcp-for-blender` (the old name `blender-mcp` is a
     rename shim whose installs freeze an obsolete build, AN-01-02);
   - PyPI version checked live against the register pin (AN-01-01);
   - wheel artifact hash recorded at install time (prefix in AN-01-01).
   The repository publishes no releases or tags (AN-01-03), so the triple, not
   a tag, is the identity. Refresh cadence: the measured release rate in
   AN-01-01 means re-check pins at least per mission, not per memory.
   `<example>`
   uv tool install "mcp-for-blender==<version>" --with-no-cache
   then record: sha256sum <site-packages wheel file> | cut -c1-16
   `</example>`
2. Start in the documented ORDER: GUI Blender first; addon panel server start
   second; MCP client launch third.
3. Confirm the listener exists before issuing scene commands (a silent bind
   failure reads as a dead tool, FC-01):
   `<example>`
   # Windows host check; expect a LISTEN entry on port 9876 only while the
   # GUI Blender session with the addon server running exists (AN-01-13).
   netstat -ano | grep ":9876" | grep LISTEN
   `</example>`
4. Read the addon state of the host you are ON, not the state of the last host
   you were on: installed addon file size/line count and switch count against
   the bundled copy of your pinned package (AN-01-09). If they differ, the host
   carries a stale addon.
5. Run the HANDSHAKE first inside the session: compare the addon protocol
   integer reported by the connected addon against the integer the pinned
   server expects (the divergence this cycle measured is AN-01-07 versus
   AN-01-06). Treat any mismatch as a versioning incident: reinstall the
   bundled addon from the pinned package, restart, re-check. Do not continue on
   a mismatched handshake.
6. Verify the two opt-in safety switches before trusting a sandboxed session:
   socket authentication does not exist at all, and the AST safe-mode validator
   activates only through its environment variable (measured disabled by
   default, AN-01-07). Say so explicitly in the session notes if neither is on.
7. Probe the command surface once per new connection: enumerate live tools
   qualified per server (`ServerName:tool_name`) and diff against the set in
   references/mcp-architecture.md before assuming a verb exists; a diverging
   handler set is the stale-addon signature again (AN-01-10; FC-03).
8. Only now issue the first mutating command - one at a time, serial, with the
   split rules from references/mcp-architecture.md.

Abort rule: if any step fails, open references/failure-catalog.md at the named
FC row and apply its remedy; do not improvise around the checklist, because
every step here exists because its absence cost real debugging time on the
measured host (report Chapter 1, lane prints).
