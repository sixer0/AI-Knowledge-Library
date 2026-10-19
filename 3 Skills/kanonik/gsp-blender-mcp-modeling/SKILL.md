---
name: gsp-blender-mcp-modeling
description: >
  Expert use of Blender 5.2 LTS through MCP and headless bpy for standard,
  high-quality 2D/3D assets. Use when a task mentions Blender, MCP, blender-mcp,
  mcp-for-blender, bpy, geometry nodes, Grease Pencil, UV unwrap, baking, PBR
  materials, Cycles or EEVEE rendering, glTF/FBX export, or asset-library
  sourcing, and whenever an agent must build, measure, or QA a Blender asset.
  Carries the two-route doctrine (GUI MCP versus headless blender -b -P), the
  pin-and-handshake first recipe, measured thresholds as register rows AN-nn,
  the failure catalog FC-nn, and the Claude tool-use surface contract. Not for
  3ds Max (see gsp-3dsmax-mcp-modeling) and not for CAD volume takeoffs.
version: 0.1.0-draft
author: GSP fleet (gsp-skill-creator role, mission BLENDER-MCP-SKILL-1016 step 16)
license: MIT
metadata:
  hermes:
    tags: [gsp, blender, mcp, bpy, 3d, 2d, grease-pencil, rendering, claude-tool-use]
    category: 3d-modeling
  provenance: >
    Drafted 2026-10-16 from Appendix A (SKILL BLUEPRINT) of
    docs/2026-10-16-blender-mcp-skill/output/REPORT.md rev A, whose eight lanes
    were re-executed the same day with fresh access dates. The 2026-10-12 corpus
    served only as a coverage denominator; no prose or number was copied from it.
    Report revision history: Rev A, 2026-10-16, session t_c0cc906e (writer role),
    first synthesis of the eight lanes; appendices A-F generated mechanically from
    the lane registers. This skill is that revision's only downstream consumer.
  measured_host: Blender 5.2.0 LTS (build fbe6228777e7 at pin time, Python 3.13.13), mcp-for-blender 2.1.9
  gsp-relations: [gsp-3dsmax-mcp-modeling, gsp-verification-before-completion, pustaka-teknis]
---

# Blender through MCP and headless bpy - expert utilization

Provenance and open gaps for this bundle are at the bottom of this file. Read
the doctrine first, then take a route from the workflow ladder, then open only
the reference file your task names. Thresholds are never restated here; cite
the register row instead. The bundle states its limitations where they bite,
and one thing yang membedakan this contract from a generic house style guide:
every clause below descends from a measured register row of 2026-10-16, not
from preference, so a rule can be audited back to its instrument.

## Doctrine (what a competent operator holds before touching a tool)

1. Blender-MCP is a two-process bridge, not one tool. An addon owns a plain TCP
   socket on localhost port 9876 and runs commands serially on Blender's main
   thread; a separate server package speaks MCP over stdio. Every operational
   limit follows from that shape (register AN-01-06, AN-01-07). Reason:
   instructions that assume one process mislead the model from the first command.
2. Two doors, routed by intent, not availability. The addon refuses background
   mode, so the MCP door exists only while a GUI session runs; deterministic and
   CI work goes through `blender -b -P script.py --python-exit-code 9`. Only the
   GUI door has eyes (the `look` tool); only the headless door is reproducible
   (AN-01-06, AN-05-20, AN-05-21).
3. Portable `bpy` beats tool-schema memorization. Upstream froze its portability
   rules into the initialize instructions after proving model-invoked prompts
   were never reached, and its regression tests lock a deliberately consolidated
   surface (AN-01-07). Reason: capability grows through instructions and scripts,
   not through more tools.
4. Identity is a pinned triple: canonical package name, PyPI version, artifact
   hash. The repository publishes no tags and the old name is a rename shim
   (AN-01-01, AN-01-02, AN-01-03). Reason: sixteen releases in thirty-four days
   means any unpinned instruction drifts within weeks.
5. Quality splits into two testable halves. Standard means normative conformance
   checked by an instrument (glTF-Validator exit status plus a numeric topology
   battery). High quality means a threshold set selected per asset domain (print
   thickness, XR triangle budgets). A claim without a gate is a preference
   (AN-06-01 through AN-06-19).
6. Numbers come from the register or from a probe run this session. Never from
   recall, because API drift in 5.2 removed and redirected exactly the seams
   scripts rely on (`items_new` gone, socket dictionary writes rejected,
   smoothing-by-angle now a modifier) (AN-05-04 through AN-05-09, FC-05, FC-07).
7. Every hard rule in this bundle carries its reason, because Claude generalizes
   correctly from rules that explain themselves (AN-08-23, CT-22).
8. External assets enter only through a verified license row (Poly Haven and
   ambientCG CC0 floors, Blendkit dual license with resale barred, Fab Standard
   barring standalone resale; Free3D excluded until primary verification)
   (AN-07-05 through AN-07-16).

## Workflow ladder (ordered, numbered because order is load-bearing)

1. Pin and handshake. Follow templates/pin-and-handshake-check.md before any
   scene command. A stale addon reads later as a dead tool (FC-01, FC-03).
2. Choose the door by intent: interactive iteration, viewport feedback, or asset
   browsing takes the MCP door; reproducibility, CI, batch export, or dimensional
   claims take the headless door. See references/mcp-architecture.md.
3. Author geometry per references/modeling-topology.md, then gate it with
   [`scripts/topology_checks.py`](scripts/topology_checks.py) (pole valence, manifoldness, winding, triangle
   count post-triangulation).
4. Unwrap, pack, and shade per references/uv-materials.md; ship your own density
   check with [`scripts/uv_density_check.py`](scripts/uv_density_check.py) because Blender has none natively.
5. Light and render per templates/cycles-headless-render.md; enable GPU devices
   explicitly, since the factory device is CPU (FC-12).
6. Parametric work per references/gn-precision.md and
   templates/gn-parametric-generator.md; drive runtime variation through modifier
   inputs only (FC-05, FC-06).
7. Gate the deliverable with [`scripts/qa_gate.py`](scripts/qa_gate.py) plus the validator battery in
   references/optimization-qa.md before human eyes touch the asset.
8. For 2D or cel-style work use references/greasepencil-libraries.md and
   templates/gp-workflow.md; source assets only from the licensed census there.
9. Report measurements taken from disk (evaluated mesh dimensions, file digests,
   validator exit codes), never from the session's memory of them.

## Claude tool-use surface (what your own mechanics demand of this skill)

This section is the contract from report Chapter 8, restated as behaviour rules
for the agent reading this file. It exists because a technically correct
Blender manual that competes with the conversation for the same context window
is a manual Claude cannot drive efficiently. Yang membedakan reading a Blender
manual from driving one through this contract is that every mechanism below has
a measured cost against the model's own context economics, and the economics
were quantified on 2026-10-16 rather than assumed.

Call patterns:
- Tool definitions arrive as name, description, JSON-schema input. Names match
  `^[a-zA-Z0-9_-]{1,128}$` (AN-08-01, CT-01); descriptions run three to four
  sentences and consolidate rather than proliferate (AN-08-02, CT-02).
- A failing call is retried two or three times using correction signals from the
  error text before helplessness surfaces (AN-08-04, CT-04). Reason: error text
  is a design surface, so FC-nn remedies in references/failure-catalog.md are
  written to be actionable, not merely descriptive.
- Parallel calling defaults on from Claude 4 (AN-08-07, CT-07). Batch only
  operations that are independent of each other; all results must return in one
  user message before any text (AN-08-08, CT-08). Scene mutations over the
  Blender socket are serial by transport, so they are never batched (FC-29).
- Forced tool use (`any`, `tool`) returns 400 on the newest model line; strict
  tool use or structured outputs is the sanctioned replacement (AN-08-06,
  CT-06, FC-28). Do not write instructions that assume forced calling.
- Streaming delivers partial JSON deltas; accumulate rather than parse per
  delta, and never assume an argument is complete before `content_block_stop`
  (AN-08-11, AN-08-12, CT-11, CT-12).
- Never ask for chain-of-thought inside a tool parameter; request a short
  explanation or evidence instead, since reasoning-extraction asks risk refusal
  (AN-08-23, CT-22).

Context limits:
- The flagship window reaches one million tokens including tool definitions and
  thinking, 200k on older models, 128k maximum output, 600 image or PDF pages
  (AN-08-13, CT-13). Definitions and thinking compete inside that space: five
  MCP servers cost roughly 55k tokens of definitions before any work, and one
  instrumented deployment saw 134k (AN-08-17, AN-08-21, CT-16, CT-20).
- Selection accuracy degrades starting around 30 to 50 available tools, with the
  official trigger band at 10 or more tools, definitions above 10k tokens, or
  multi-server aggregation past 200 (AN-08-18, AN-08-19, CT-17, CT-18). The
  Blender surface sits under that band at nine model-facing tools, so normal
  operation needs no tool search; if a host aggregates several servers beyond
  the band, adopt the official tool-search mechanism rather than invented
  parsimony (FC-31).
- Thinking blocks must be returned byte-intact with their signature alongside
  the tool result, or the transcript is rejected (AN-08-15, CT-14, FC-30).

Instruction format (how to read this bundle):
- This body stays under five hundred lines and targets the sub-five-thousand
  token level-two budget; numbers, failures, and recipes live one level down in
  [`references/`](references/), [`templates/`](templates/), and [`scripts/`](scripts/), which cost zero tokens until
  opened (AN-08-26, AN-08-27, CT-25, CT-26).
- Run the scripts rather than reading them into context; only their output is
  meant to enter the conversation (AN-08-27, CT-26).
- Numbered steps signal mandatory order; tagged blocks delimit examples; long
  reference chapters are grounded by quoting the relevant passage before work
  begins (AN-08-22 through AN-08-25, CT-21 through CT-24).
- Refer to MCP tools qualified per server, `ServerName:tool_name`, and enumerate
  the live tool list before assuming names, since the surface changes between
  server versions (AN-08-30, CT-29).
- Paths are forward-slash everywhere and no package is assumed installed; each
  recipe states its dependency check (AN-08-30, AN-08-31, CT-29, CT-30).

## Navigation (one row per bundled file)

| File | Open it when | Register ids it relies on |
|---|---|---|
| references/mcp-architecture.md | setting up, diagnosing, or automating the bridge | AN-01-01 through AN-01-15 |
| references/modeling-topology.md | authoring meshes, retopology, bevel/shading stacks | AN-02-01 through AN-02-14 |
| references/uv-materials.md | unwrapping, packing, PBR authoring, baking, colour management | AN-03-01 through AN-03-10 |
| references/lighting-render.md | lights, HDRI, Cycles or EEVEE setup, output formats | AN-04-01 through AN-04-25 |
| references/gn-precision.md | geometry nodes, drivers, units, dimensional verification | AN-05-01 through AN-05-21 |
| references/optimization-qa.md | budgets, validators, naming, delivery gates | AN-06-01 through AN-06-25 |
| references/greasepencil-libraries.md | 2D work, asset sourcing, licence checks | AN-07-01 through AN-07-16 |
| references/claude-tool-use.md | tuning how this skill is selected, sized, and called | AN-08-01 through AN-08-40 |
| references/number-register.md | quoting any threshold, budget, or default | all |
| references/failure-catalog.md | any error, silent failure, or unexpected result | FC-01 through FC-36 |
| references/source-links.md | citing a primary document | D-001 through D-188 |
| references/blueprint-map.md | revising a chapter upstream, or auditing coverage | Appendix A rows |
| templates/pin-and-handshake-check.md | first contact with a new host | AN-01-01, AN-01-06 to AN-01-09 |
| templates/cycles-headless-render.md | producing frames headless | AN-04-10 to AN-04-25 |
| templates/gn-parametric-generator.md | procedural generators with verified dimensions | AN-05-04 to AN-05-22 |
| templates/gp-workflow.md | Grease Pencil scenes and vector export | AN-07-01 to AN-07-04 |
| scripts/topology_checks.py | gating any authored or imported mesh | AN-02-05, AN-02-09, AN-06-01, AN-06-14 |
| scripts/uv_density_check.py | shipping texture-resolution claims | AN-03-01, AN-03-03, AN-03-04, AN-03-10 |
| scripts/qa_gate.py | final pass/fail on a deliverable | AN-06-01 to AN-06-12, AN-06-20 |

## Maintenance note

This file is generated work product of the section-to-file map in
references/blueprint-map.md (Appendix A of the mission report, 62 mapped
manuscript sections). When any report chapter is revised upstream, the affected
rows in that map change in the same edit and this body, the register, and the
catalog refresh together; a chapter edit that does not touch the map is
incomplete. The skill ships as a folder following the open Agent Skills format,
so the same tree is valid on Hermes, Claude Code, and the API surface provided
the core frontmatter fields stay within their limits (AN-08-30 through
AN-08-33, CT-29, CT-36). Distribution is per surface and never automatic
(AN-08-35, CT-35, FC-34).

## Provenance and open gaps (carried honestly from the report)

Measured host: Blender 5.2.0 LTS build `fbe6228777e7`, Python 3.13.13;
mcp-for-blender 2.1.9 (wheel sha256 prefix a5cbc6cf), MCP SDK resolved 1.30.0,
protocol revision string 2026-07-28. All sources accessed 2026-10-16.
Coverage: all eight lanes met their assigned denominator floors (127 prior
topics plus the ten-section Claude gate), zero unexplained omissions.

| Gap | Status carried into this skill |
|---|---|
| ISO 2768 numeric tolerance tables lack a primary path | Fleet baseline governs: max(0.5 mm, 0.1 percent of dimension) until a primary source exists (AN-05 table, gap G-L5-1) |
| glTF add-on manual page vanished from its historical location | Flag semantics taken from operator RNA instead of the doc page (gap G-L5-2) |
| Fab terms partial; CGTrader wording paraphrase-level; Sketchfab per-asset fields unconfirmed | Licence claims limited to what the verified rows state (AN-07-13 through AN-07-16) |
| Free3D blocked behind antibot on every rung attempted | Excluded from recommended sources until primary verification |
| Sketchfab aggregate inventory unavailable to anonymous queries by design | No catalogue-size claim is made for it |
| Official single engine-comparison table no longer exists | Comparison rebuilt from three engine index pages plus release notes |
