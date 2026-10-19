# Failure Catalog (FC-nn)

Verbatim transcription of Appendix E of the mission report
`docs/2026-10-16-blender-mcp-skill/output/REPORT.md` (rev A), plus the
append-only rows FC-33 through FC-36 that this skill revision adds per the
catalog's own rule ("Ids FC-nn are stable; future revisions append rather
than renumber"). Each entry states symptom, cause, and remedy in the form
Claude's retry behavior consumes: error text here is engineered to be
actionable because Claude retries a failing tool call two or three times
from the correction signal before surfacing helplessness (row AN-08-04,
CT-04). No entry adds a fact that is not in the report and its lanes. The
catalog's own limitation travels with it: remedies were validated on the
2026-10-16 host stack (Blender 5.2, server 2.1.9), and an era shift can move
a symptom onto a different row without warning; re-probe before trusting a
remedy against a newer build.

| Id | Area | Symptom | Cause | Remedy | Evidence |
|---|---|---|---|---|---|
| FC-01 | Transport | MCP tools hang or connection refused with no listener | GUI Blender not running or addon server not started; socket lives only in GUI sessions | Start Blender GUI, start addon server, verify port 9876 listener before commands | Ch. 1, rows UK-15, UK-22 |
| FC-02 | Transport | Incomplete JSON response after long wait | Response exceeds the 180 s socket timeout or framing parse gives up mid-object | Split the command; fetch scene data in bounded pages (list clamps at 20..500) | Ch. 1, rows UK-16, UK-19 |
| FC-03 | Transport | Commands unknown or absent on a working connection | Addon older than server: protocol integers differ and handler sets diverge | Run handshake comparison first; reinstall the bundled addon version | Ch. 1, rows UK-18, UK-19 |
| FC-04 | Export | GLB valid but visually empty after geometry-nodes work | Exporter writes base meshes; evaluated geometry needs the apply flag | Always export with export_apply and verify primitive counts post-export | Ch. 5, row AN-L5-19 |
| FC-05 | API drift | TypeError on modifier socket dictionary assignment | Era 5.2 rejects direct mod[Socket_N] writes | Write through mod.properties.inputs[Socket_N]["value"] plus update_tag | Ch. 5, rows AN-L5-07, AN-L5-09 |
| FC-06 | API drift | Edited interface default values never reach the evaluated result in-process | Five forced-update routes fail to propagate interface defaults live | Treat interface defaults as authoring-time; vary at runtime via modifier inputs | Ch. 5, row AN-L5-10 |
| FC-07 | API drift | Operator call fails although hasattr reports true | Stub attribute without registered operator in 5.2 | Never trust hasattr for bpy.ops existence; call inside try and verify effect | Ch. 5, row AN-L5-17 |
| FC-08 | Render | Engine validation rejects Cycles in headless sessions | Enum listing shows only EEVEE even though Cycles assignment succeeds | Validate by assigning then reading back the stored value, not by enum census | Ch. 4, limitation on engine enum |
| FC-09 | Render | AttributeError on film pixel-filter properties in older scripts | Filter settings moved onto engine data-blocks between eras | Read the current RNA path per version; keep a version map in the skill | Ch. 4, drift finding L4-15 |
| FC-10 | Render | Early-denoise request does nothing on final frames | denoising_start_sample applies to viewport only in 5.2 | Drop early-denoise promises for final renders; denoise after sampling | Ch. 4, row AN-L4-12 context |
| FC-11 | Render | EEVEE final render fails headless on Windows | Rasterizer requires a graphics context absent in background mode | Use Cycles for headless; label EEVEE speedups as GUI-session claims | Ch. 4, route table row |
| FC-12 | Render | Silent CPU renders on GPU-equipped hosts | Factory device is CPU; GPU enabling is never automatic | Explicit enable-devices block per backend with CPU fallback | Ch. 4, rows AN-L4-18, AN-L4-23 |
| FC-13 | Units | Imported model appears 1000 times oversized | Millimeter-convention file crossed the glTF meter contract without normalization | Normalize by scale factor at import; assert bounding dimensions | Ch. 5, rows AN-L5-14, AN-L5-20 |
| FC-14 | Drivers | Dependency cycle warning; driver evaluates stale value | Driver reads a property chain that passes through its own object | Break the loop with a helper empty carrying the source transform | Ch. 5, row AN-L5-13 |
| FC-15 | Drivers | Driver creation raises on legacy type name | Enum vocabulary changed; PYTHON no longer accepted | Use SCRIPTED with expression variables from the 5.2 enum set | Ch. 5, row AN-L5-11 |
| FC-16 | Geometry nodes | Modifier evaluates to zero vertices with a depsgraph warning | Node group interface lacks an output socket | Declare OUTPUT socket at tree creation; assert n_verts after evaluation | Ch. 5, row AN-L5-04 |
| FC-17 | Topology | Creased or bubbled shading under subdivision surfaces | Ngons or uncontrolled poles beneath Catmull-Clark | Keep quads under subdiv; move poles; ngons only on flat non-deforming faces | Ch. 2, rows AN-04, AN-05 context |
| FC-18 | Topology | Bevel profile changes produce no visible effect | Segments below 2 disables profile and miter mathematics | Set Segments at least 2 before tuning shape | Ch. 2, row AN-04 |
| FC-19 | UV | Bleeding seams or wasted atlas space | Bake margin too small or islands packed without margin | Use fraction margins (1/1024 default) and two-pixel island separation | Ch. 3, row AN3-01 |
| FC-20 | Material | Exported materials read wrong in target engines | Channel packing violates the metalness-roughness convention | Pack per glTF sections (G rough, B metal, linear data, Non-Color tags) | Ch. 3, row AN3-09 |
| FC-21 | Color management | Visual QA disagrees with render intent | Reviewers read pre-tone-mapped or display-referred images inconsistently | Standardize review on post-AgX display images and say so in reports | Ch. 3, row AN3-06 |
| FC-22 | QA gates | Asset accepted although target engine will reject it | Validator exit treated as advice; warnings ignored | glTF-Validator exit 0 with zero errors is the only pass state | Ch. 6, row AN-L6-05 |
| FC-23 | QA gates | Unexplained triangle explosions after decimate | Decimate triangulates; budgets counted on authoring quads miss runtime truth | Count triangles post-export against budget rows, not pre-export | Ch. 6, rows AN-L6-01 context; Ch. 2 row AN-09 |
| FC-24 | Naming | Marketplace or engine import rejects meshes silently | Identifier charset and prefix discipline violated | Lint names with the charset regex and prefix grammar before delivery | Ch. 6, row AN-L6-20 |
| FC-25 | Licensing | Catalog-size claims wrong by construction | Search endpoint ceiling read as total | Take totals from category census fields; treat search counts as caps | Ch. 7, rows AN-L7-13, AN-L7-14 |
| FC-26 | Licensing | Filter returns whole catalog | Unknown type token silently ignored by provider API | Validate the echoed query token in every filtered response | Ch. 7, parser finding on ambientCG |
| FC-27 | Grease Pencil | Promised VFX effect absent from final render | VFX types are viewport-first and cannot be applied | Rasterize intended look via GP render panels or bake to texture; never promise VFX baking | Ch. 7, VFX limitation entry |
| FC-28 | Tool-use contract | API rejects request that worked on older integrations | Forced tool use returns 400 on newest models | Use strict tool use or structured outputs; remove any assumptions | Ch. 8, row CT-06 |
| FC-29 | Tool-use contract | Parallelism silently lost | Tool results emitted across multiple messages or after text | Batch all tool_result blocks in one user message before any text | Ch. 8, row CT-08 |
| FC-30 | Tool-use contract | Conversation rejected mid-task | Thinking block altered or omitted alongside its tool result | Return thinking blocks byte-intact with matching signature | Ch. 8, row CT-14 |
| FC-31 | Tool-use contract | Wrong tool chosen or none chosen | Too many definitions crowded the decision space | Keep surface under the trigger band; adopt official tool search when above it | Ch. 8, rows CT-16 through CT-18 |
| FC-32 | Supply chain | Pin installs an obsolete build | Old package name resolves to rename shim | Install canonical name with version plus hash triple; refresh on cadence | Ch. 1, rows UK-10 through UK-12 |
Appended by this skill revision (facts restated from report Chapter 8
section 8.3 and Chapter 9 section 9.3, no new measurements):

| Id | Area | Symptom | Cause | Remedy | Evidence |
|---|---|---|---|---|---|
| FC-33 | Tool-use contract | blender-mcp unreachable from a hosted Claude connector surface | Connectors accept public HTTPS servers only and reject local STDIO topology | Use the desktop or Hermes-hosted route for the localhost socket; never promise hosted-connector Blender control | Ch. 8.3, rows AN-08-37, AN-08-38 (CT-37, CT-38) |
| FC-34 | Distribution | Installed skill invisible on another Claude surface | Custom skills do not synchronize across claude.ai, API, and Code surfaces | Distribute the skill folder per surface as an explicit step; do not assume propagation | Ch. 8.3, rows AN-08-34, AN-08-35 (CT-34, CT-35) |
| FC-35 | Number discipline | Published threshold disagrees with the measured host | Value recalled from memory or an older corpus instead of the register | Quote only rows from references/number-register.md; re-measure with a probe when a row looks stale | Ch. 9.3 recommendation 3; Appendix B preamble |
| FC-36 | Transport | Dimensional claim wrong on an imported marketplace asset | Imported assets arrive at arbitrary scale; no measurement step ran before the claim | Measure the bounding box before any dimensional statement, and use `look` to check generated code against the viewport | Ch. 1.2 step 5 (rows UK-15, UK-16 via AN-01-06, AN-01-07) |
