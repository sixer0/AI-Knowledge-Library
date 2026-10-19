# MCP Control Architecture

Chapter spine distilled from report Chapter 1 (lane 1, register UK, accessed
2026-10-16). Thresholds are NOT restated here: cite the register rows named at
the end of each rule from references/number-register.md (block AN-01-nn).

## What the bridge actually is (competency)

1. Two processes joined by two transports. Addon `blender_mcp.py` runs inside
   Blender and owns a plain TCP socket on localhost port 9876, executing
   received commands serially on Blender's main thread through a timer queue.
   The server package `mcp-for-blender` speaks MCP to the client over stdio and
   translates each tool call into one private JSON command on that socket
   (AN-01-06). Reason: neither half can be collapsed into the other; the addon
   cannot import the MCP library or write to Blender stdout, and the server
   cannot touch the `bpy` runtime without a UI context.
2. The socket side is not a standard MCP transport. It carries undocumented
   payloads of type and params, framed by repeated parse attempts on 8192-byte
   chunks rather than line delimiters; oversized responses surface as
   incomplete-JSON errors after a timeout (AN-01-04, AN-01-07; FC-02).
3. The tool surface is deliberately consolidated. The pinned build registers
   fourteen tools, nine model-facing (`get_addon_status`, `get_scene_info`,
   `execute_blender_code`, `look`, `search_assets`, `import_asset`,
   `generate_3d`, `record_trajectory_feedback`, `disable_telemetry`) and five
   reserved for application clients such as the interactive viewport
   (AN-01-07). Refer to them qualified per server, `ServerName:tool_name`, and
   enumerate the live tool list before assuming names survive an upgrade
   (AN-08-30). Upstream tests lock this set so schema cost stays predictable.
4. Capability grows through instructions and scripts, not through new tools.
   Upstream froze portability rules into the initialize instructions after
   proving model-invoked prompts were never reached (AN-01-07). That channel is
   bounded: the server injects its instructions into every conversation turn
   under a tested ceiling of 2500 characters (register cell
   instructions_ceiling_tested at AN-01-07). Consequence: expertise belongs in
   this skill body, not in tool definitions.
5. Configuration facts a fresh session asks first, all register-backed: the MCP
   SDK dependency floor resolved inside its supported ceiling below major
   version two; the protocol revision negotiated at handshake is the
   date-stamped string current at pin time; telemetry ships minimal-anonymous
   with payload consent behind three kill switches, one of them a model-facing
   tool (AN-01-07, and Ch. 1.4 restatement via UK-16, UK-19, UK-21).

## Working procedure (canonical order lives in templates/pin-and-handshake-check.md)

Read-only scene inspection may be batched when independent; every mutating
command is serial because the transport executes serially and the socket
protocol has no correlation id, so interleaved writes cannot be attributed
after the fact (AN-01-07; contract cross-referenced from AN-08-07 through
AN-08-10). Split anything that could run longer than the socket budget, and
split generation jobs at the tighter internal ceiling using submit-and-poll
cycles instead of one long call (AN-01-07). Use `look` as the visual feedback
channel so generated code gets checked against the viewport. Imported assets
arrive at arbitrary scale: bounding-box measurement precedes any dimensional
claim (FC-36).

## Limitations and typical failures (rows live in the failure catalog)

- Background mode is refused by the addon server start, measured twice on the
  host this cycle (AN-01-06; FC-01). The MCP path exists only while a GUI
  session runs; deterministic work goes headless outside MCP.
- Socket security is honest-defaults, not design: binding localhost removes
  remote exposure by accident, the protocol has no auth or encryption, and the
  safe-mode AST allowlist validator is opt-in via environment variable and was
  measured disabled (AN-01-07). Guardrails against destructive `bpy` live in
  client confirmation and in this skill's rules, not in the transport.
  Yang membedakan these limits from ordinary conservatism is that each one was
  measured on the host this cycle, not inferred from caution.
- Release cadence is a limitation in disguise: any unpinned instruction drifts
  within weeks, and missing git tags force hash pins humans forget to refresh
  (AN-01-01, AN-01-03; FC-32).
- Handshake mismatch (protocol integer, handler-switch count, command-handler
  set divergence) is a versioning incident, not permission to continue; a stale
  host addon reports as unknown or absent commands (AN-01-08, AN-01-09; FC-03).

## Freshness and recheck duty

The pins in this chapter carry a recheck obligation whenever Blender or
mcp-for-blender moves; the report notes the next Blender major already visible
on the download page at access time. Re-measure the surface with the pinned
package before trusting any count above, and if a number moved, fix the
register row at its lane source rather than patching prose.

Threshold anchor block: AN-01-01 (cadence, hash), AN-01-02 (rename shim),
AN-01-03 (repo identity, zero tags), AN-01-04 (tree census, buffer chunk),
AN-01-05 (raw sources, bundled addon digest), AN-01-06 (background refusal
print), AN-01-07 (surface census, schema cost, timeouts, ceilings), AN-01-08
through AN-01-10 (host addon staleness), AN-01-13 (listener absence),
AN-01-14 (link lint result).
