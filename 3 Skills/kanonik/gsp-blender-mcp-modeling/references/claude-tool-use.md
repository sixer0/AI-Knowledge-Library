# Claude Tool-Use Surfaces and What They Demand of the Skill

Chapter spine distilled from report Chapter 8 (lane 8, register CT, accessed
2026-10-16). This chapter reads as incoming requirements for the skill rather
than as a Blender domain; SKILL.md carries the surface summary, this file
carries the full evidence spine. Register block AN-08-nn in
references/number-register.md backs every number cited as CT-nn below. The
limitations inherited here are deliberate: two of these findings (the forced
tool-use ban and the open standardization) were four days old at access time,
so this spine is the freshest layer of the bundle and ages fastest.

## 1. How Claude calls tools, and what that costs

- A tool definition travels as `name` (regex-constrained, letters/digits/
  underscore/hyphen up to 128 characters, AN-08-01), `description` (prose: what
  it does, when to use it and when not to, what it returns, caveats; three to
  four sentences minimum; consolidation favored over proliferation, AN-08-02),
  and `input_schema` (JSON Schema). Optional `input_examples` validate against
  the schema (invalid is an HTTP 400) and cost per the token band in AN-08-03;
  they are not supported for server tools or the computer/browser toolsets.
- The roundtrip: Claude answers `stop_reason: "tool_use"` with blocks carrying
  `id`, `name`, `input`; the application executes and returns a user message
  with `tool_result` blocks (`tool_use_id`, `content`, optional `is_error`).
- Failure handling is a design surface: Claude retries a failing call two or
  three times using correction signals from the error text before surfacing
  helplessness (AN-08-04). Consequence for this bundle: FC remedies are written
  as actionable corrections. Invalid tool names or parameters from the model
  side are fixed by improving the description, not by scolding.
- Tool-use system-prompt overhead is measurable per model family (AN-08-05).
  Forced tool use (`any`, `tool`) now returns 400 on the newest models; strict
  tool use or structured outputs is the sanctioned replacement, and forcing
  conflicts with manual extended thinking where both are supported (AN-08-06;
  FC-28). Parallel calling defaults on from Claude 4; all results belong in one
  user message before any text, and the disable switch lives inside
  `tool_choice` (AN-08-07 through AN-08-09; FC-29). Dependent batches run
  serial stop-on-first-failure and still answer unexecuted calls with
  `is_error: true` (AN-08-10).
- Streaming delivers `input_json_delta.partial_json` string fragments; the
  final `input` is an object, the model emits one complete key-value pair at a
  time, and resume logic differs by model era - partial tool_use and thinking
  blocks never resume (AN-08-11, AN-08-12).

## 2. Context economics drive skill architecture

- The flagship window reaches one million tokens including definitions and
  thinking; older models 200k; maximum output 128k; image/PDF-page caps per
  AN-08-13. Overflow prints are registered in AN-08-14.
- Definitions compete for the window measurably: one instrumented five-server
  MCP setup carried roughly 55k tokens of definitions before any work, another
  deployment was seen at 134k, and the official search mitigation cut
  definition load by more than 85 percent while real evaluations improved by
  the margins in AN-08-20 and AN-08-21.
- Selection accuracy degrades starting around the band in AN-08-18; the
  official trigger threshold band for adopting search-based loading is in
  AN-08-19 (FC-31). The Blender surface (nine model-facing tools, schema cost
  in AN-01-07) sits under the band by design, so normal operation never needs
  tool search and the expertise budget goes to document structure instead.
- The Agent Skills disclosure ladder is the structure this bundle implements:
  level one metadata costs roughly the per-skill figure in AN-08-26 and is
  always resident; level two body targets the budget in AN-08-26 when
  triggered; level three resources cost zero until read, and executed scripts
  return only their output (AN-08-27). Unbundled-content practical ceiling:
  none, per the same sources - move instructions into deterministic scripts
  rather than paying for prose. Yang membedakan this ladder from ordinary
  documentation habits is arithmetic: the reading cost is paid per token at
  selection time, so structure, not brevity-by-taste, decides what Claude knows.
- Instruction style that measurably works on Claude: explicit numbered steps
  for order-dependent procedures with the golden rule "show your colleague"
  (AN-08-22); reasons attached to every hard rule, and never request
  chain-of-thought in tool parameters because reasoning-extraction asks risk
  refusal (AN-08-23; CT-22); consistent XML-consistent tags with worked
  examples in `<example>` blocks (AN-08-24); for long documents, quote-first
  grounding with the document above the query (AN-08-25).

## 3. Where skills live and how Hermes fits (failure rows FC-33, FC-34)

- Skills travel as folders following the open Agent Skills standard (AN-08-36);
  the same folder contract feeds Hermes, which loads by frontmatter name and
  description - keep the core fields standard and paths slash-separated with no
  assumed packages, and one authored tree serves both hosts (AN-08-30).
- Surfaces: Claude Code reads personal and project skill directories with a
  documented precedence and live-change detection (AN-08-34); the API consumes
  skills through container plus code execution in a no-network sandbox
  (AN-08-33); claude.ai takes per-user zip uploads; and custom skills do not
  synchronize across surfaces (AN-08-35; FC-34).
- MCP connectors on hosted Claude surfaces accept tool calls only, require
  public HTTPS servers, and reject local STDIO topology (AN-08-37), with a beta
  listing block able to pin server tool lists (AN-08-38). The blender-mcp
  localhost socket therefore reaches desktop and Hermes-hosted routes but not
  hosted connectors (FC-33) - reinforcing the two-route doctrine rather than
  weakening it.
- Trigger mechanics: skill selection is description matching over the whole
  installed list (AN-08-31); the description field carries the entire trigger
  burden within its cap (AN-08-28); Claude Code truncates listings per entry
  at the documented cap, making front-of-description cases load-bearing
  (AN-08-32). Iterate the trigger from observed trajectories, not speculation.

## 4. The ten-point design contract (acceptance criteria for this bundle)

Reproduced from report section 8.4 as a checklist; each point names its
register anchors. This list doubles as rubric material for the independent exam
bank of mission step 17.

1. Description is the trigger: what-plus-when with domain tokens (CT-25,
   CT-28, CT-31). Implemented in the frontmatter above this file's chapter.
2. Body stays thin; numbers, failures, recipes demoted one level to
   references (CT-25, CT-26).
3. Deterministic recipes ship as executable scripts, not pasted code (CT-26).
4. MCP references qualify tool names per server and forbid stale assumptions
   (CT-29).
5. Parallelism contracts separate read-only batching from serial mutation,
   inheriting the socket reality of Chapter 1 (CT-07 through CT-10).
6. Error texts are engineered for the retry behavior (CT-04).
7. Token economy rides official mechanisms only, never invented parsimony
   (CT-16 through CT-20).
8. Portability forbids Windows path styles and undeclared dependencies
   (CT-29, CT-30).
9. Release requires at least three real evaluations across the consuming model
   families (CT-30).
10. Style follows the documented instruction patterns, not local convention
    (CT-21 through CT-24).

Comparators: OpenAI function-calling mechanics differ on the record
(`strict` normalization, top-level parallel toggle; AN-08-40) and were kept as
comparator only; nothing in this bundle depends on non-Claude semantics.

Register anchor block: AN-08-01 through AN-08-40.
