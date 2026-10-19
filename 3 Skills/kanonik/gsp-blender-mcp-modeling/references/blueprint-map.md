# Blueprint Map (report-to-skill conversion contract)

Verbatim copy of Appendix A of `docs/2026-10-16-blender-mcp-skill/output/REPORT.md`
(rev A): every manuscript heading mapped to the skill file that carries its
content. Destination rules follow the report's Chapter 8 contract: thin SKILL.md
body, thresholds in the number register, failures in the failure catalog, recipes
as executable scripts or step templates. The verifier re-runs the heading scan on
the manuscript and diffs this table: 62 mapped rows, zero unmapped headings by
construction of the scan. Two manuscript destinations deliberately ship nowhere
else: the Contents navigation (belongs to the report) and Appendix C's figure plan
(consumed by the DOCX builder, not by agents). One limitation is worth stating
plainly: this map freezes the 2026-10-16 rev A heading set, so an upstream
chapter rename silently invalidates rows here until the map is regenerated
alongside the chapter it mirrors.

| Manuscript section | Skill destination | Content carried |
|---|---|---|
| Front matter: Revision history | (provenance note row in SKILL.md) | framing content |
| Front matter: Contents | (not shipped; navigation belongs to the report) | framing content |
| Front matter: Background, scope, and how to read this report | SKILL.md frontmatter description + intro section | framing content |
| Front matter: Executive summary | SKILL.md opening doctrine section | framing content |
| Chapter 1 (The MCP control architecture) | references/mcp-architecture.md | chapter spine: competency + procedure + limits + thresholds |
| Section 1.1 (Competency) | competency rules -> SKILL.md doctrine bullets + references/mcp-architecture.md | section body distilled |
| Section 1.2 (Working procedure) | procedure -> recipe steps in templates/pin-and-handshake-check.md | section body distilled |
| Section 1.3 (Limitations and typical failures) | failures -> references/failure-catalog.md rows | section body distilled |
| Section 1.4 (Measured thresholds and configuration numbers) | thresholds -> references/number-register.md rows | section body distilled |
| Section 1.5 (References) | pointer -> SKILL.md navigation row for references/mcp-architecture.md | section body distilled |
| Chapter 2 (Modeling theory and topology) | references/modeling-topology.md | chapter spine: competency + procedure + limits + thresholds |
| Section 2.1 (Competency) | competency rules -> SKILL.md doctrine bullets + references/modeling-topology.md | section body distilled |
| Section 2.2 (Working procedure) | procedure -> recipe steps in scripts/topology_checks.py | section body distilled |
| Section 2.3 (Limitations and typical failures) | failures -> references/failure-catalog.md rows | section body distilled |
| Section 2.4 (Measured thresholds) | thresholds -> references/number-register.md rows | section body distilled |
| Section 2.5 (References) | pointer -> SKILL.md navigation row for references/modeling-topology.md | section body distilled |
| Chapter 3 (UV unwrapping, materials, and shading) | references/uv-materials.md | chapter spine: competency + procedure + limits + thresholds |
| Section 3.1 (Competency) | competency rules -> SKILL.md doctrine bullets + references/uv-materials.md | section body distilled |
| Section 3.2 (Working procedure) | procedure -> recipe steps in scripts/uv_density_check.py | section body distilled |
| Section 3.3 (Limitations and typical failures) | failures -> references/failure-catalog.md rows | section body distilled |
| Section 3.4 (Measured thresholds) | thresholds -> references/number-register.md rows | section body distilled |
| Section 3.5 (References) | pointer -> SKILL.md navigation row for references/uv-materials.md | section body distilled |
| Chapter 4 (Lighting and rendering) | references/lighting-render.md | chapter spine: competency + procedure + limits + thresholds |
| Section 4.1 (Competency) | competency rules -> SKILL.md doctrine bullets + references/lighting-render.md | section body distilled |
| Section 4.2 (Working procedure) | procedure -> recipe steps in templates/cycles-headless-render.md | section body distilled |
| Section 4.3 (Limitations and typical failures) | failures -> references/failure-catalog.md rows | section body distilled |
| Section 4.4 (Measured thresholds) | thresholds -> references/number-register.md rows | section body distilled |
| Section 4.5 (References) | pointer -> SKILL.md navigation row for references/lighting-render.md | section body distilled |
| Chapter 5 (Geometry nodes and precision parametric work) | references/gn-precision.md | chapter spine: competency + procedure + limits + thresholds |
| Section 5.1 (Competency) | competency rules -> SKILL.md doctrine bullets + references/gn-precision.md | section body distilled |
| Section 5.2 (Working procedure) | procedure -> recipe steps in templates/gn-parametric-generator.md | section body distilled |
| Section 5.3 (Limitations and typical failures) | failures -> references/failure-catalog.md rows | section body distilled |
| Section 5.4 (Measured thresholds) | thresholds -> references/number-register.md rows | section body distilled |
| Section 5.5 (References) | pointer -> SKILL.md navigation row for references/gn-precision.md | section body distilled |
| Chapter 6 (Optimization and measurable QA standards) | references/optimization-qa.md | chapter spine: competency + procedure + limits + thresholds |
| Section 6.1 (Competency) | competency rules -> SKILL.md doctrine bullets + references/optimization-qa.md | section body distilled |
| Section 6.2 (Working procedure) | procedure -> recipe steps in scripts/qa_gate.py | section body distilled |
| Section 6.3 (Limitations and typical failures) | failures -> references/failure-catalog.md rows | section body distilled |
| Section 6.4 (Measured thresholds) | thresholds -> references/number-register.md rows | section body distilled |
| Section 6.5 (References) | pointer -> SKILL.md navigation row for references/optimization-qa.md | section body distilled |
| Chapter 7 (Grease Pencil 2D and licensed asset libraries) | references/greasepencil-libraries.md | chapter spine: competency + procedure + limits + thresholds |
| Section 7.1 (Competency) | competency rules -> SKILL.md doctrine bullets + references/greasepencil-libraries.md | section body distilled |
| Section 7.2 (Working procedure) | procedure -> recipe steps in templates/gp-workflow.md | section body distilled |
| Section 7.3 (Limitations and typical failures) | failures -> references/failure-catalog.md rows | section body distilled |
| Section 7.4 (Measured thresholds) | thresholds -> references/number-register.md rows | section body distilled |
| Section 7.5 (References) | pointer -> SKILL.md navigation row for references/greasepencil-libraries.md | section body distilled |
| Chapter 8 (Claude tool-use surfaces and what they demand of the skill) | references/claude-tool-use.md | chapter spine: competency + procedure + limits + thresholds |
| Section 8.1 (How Claude calls tools, and what that costs) | competency rules -> SKILL.md doctrine bullets + references/claude-tool-use.md | section body distilled |
| Section 8.2 (Context economics drive skill architecture) | procedure -> recipe steps in (no template; contract feeds SKILL.md body) | section body distilled |
| Section 8.3 (Where skills live and how Hermes fits) | failures -> references/failure-catalog.md rows | section body distilled |
| Section 8.4 (The design contract extracted from this chapter) | thresholds -> references/number-register.md rows | section body distilled |
| Section 8.5 (References) | pointer -> SKILL.md navigation row for references/claude-tool-use.md | section body distilled |
| Chapter 9 (Cross-lane synthesis, open gaps, and next steps) | (merged into SKILL.md doctrine section) | chapter spine: competency + procedure + limits + thresholds |
| Section 9.1 (What the eight lanes say together) | competency rules -> SKILL.md doctrine bullets + (merged into SKILL.md doctrine section) | section body distilled |
| Section 9.2 (Open gaps carried forward) | procedure -> recipe steps in (no separate file) | section body distilled |
| Section 9.3 (Recommendations and next steps) | failures -> references/failure-catalog.md rows | section body distilled |
| Appendix A (SKILL BLUEPRINT (report-to-skill conversion map)) | (this map; maintenance note row in SKILL.md) | whole appendix content |
| Appendix B (Number register (thresholds with sources)) | references/number-register.md | whole appendix content |
| Appendix C (Figure plan (SV allocation per chapter)) | figure plan consumed by the DOCX builder; not shipped in the skill | whole appendix content |
| Appendix D (Referenced sources (link register)) | references/source-links.md | whole appendix content |
| Appendix E (Failure catalog) | references/failure-catalog.md | whole appendix content |
| Appendix F (Coverage cross-check against the denominator) | (gap register; provenance note rows in SKILL.md) | whole appendix content |

Coverage note for this bundle: every row above names a file present in this
folder or names an explicit non-destination (provenance note rows, merged
doctrine rows, or the two report-only sections). When a chapter is revised
upstream, the affected rows change in the same edit as the chapter and the
refresh trigger fires via the SKILL.md maintenance note.
