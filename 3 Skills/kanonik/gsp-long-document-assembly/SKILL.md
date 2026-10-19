---
name: gsp-long-document-assembly
version: 1.1.0
description: >-
  Split long documents into independently-written sections, assemble them
  into a coherent whole, and review for continuity. Solves the quality
  degradation problem when generating documents exceeding ~8000 words by
  breaking them into focused, manageable sections written with per-section
  context packages.
license: MIT
metadata:
  hermes:
    tags: [gsp, document]
    category: document
  category: orchestration
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/long-document-assembly
    license_path: LICENSE
---

# Long Document Assembly

Split documents exceeding ~8000 words into sections, write each section
independently with focused context, assemble, then review for continuity,
duplicates, and consistency. Integrates with the `document-quality-standards`
skill for style, formatting, and 5W1H tiered enforcement, and with the
`orchestrator-worker` skill for parallel section execution.

---


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: `skills/gsp/gsp-document-quality-standards/SKILL.md` **Module L**
(ringkasan: `skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`).

1. **Header-metadata** di pembuka dokumen: `title`, `date`, `author_profile`,
   `status` (`complete|blocked|needs-review|failed`), `task_ref`, `source_refs`.
2. **Heading bernomor** (1, 1.1, 1.1.1) tanpa melompati level; nama berkas
   `snake_case` untuk artefak internal; dokumen resmi berformat DATUM kelas
   TERBIT/SERAH ikut penamaan DT-12 (judul + nomor bertanda hubung, tanpa garis
   bawah) - pengecualian sah, putusan 08-10.
3. **Angka dan klaim** wajib bertanda rujukan `[R-n, sumber, hal]`; tanpa sumber → tandai sebagai asumsi.
4. **Bahasa** mengikuti bahasa user (default Indonesia); istilah teknis Inggris apa adanya.
5. **Struktur** dipilih dari tipe dokumen (Module A) dan kedalaman audiens (Module E).
6. **Checklist pra-serah** dijalankan sebelum menyerahkan: Module F.1 (10 butir); dokumen
   eksternal (Tier 2+) juga Module F.2 (6 butir).

Konflik **FORMAT** → Module L menang. Konflik **GAYA presisi** → Module H/K tetap menang.
## Triggers

Use this skill when:
- "write a long document"
- "document is too long for single generation"
- "split document into sections"
- "assemble document from sections"
- "long report production"
- "multi-part document writing"
- "sequential chapter writing"
- "write chapters separately then combine"
- "produce a [N]-word document" (where N > 8000)
- "draft each chapter independently"

Do NOT use for:
- Short documents under 8000 words
- Simple single-topic outputs
- Code generation (not document production)
- Quick summaries, emails, or notes

---

## Process

### Phase 0: Length Assessment & Split Decision

Estimate the target word count from the task description and determine the
split strategy.

**Estimation methods:**
| Method | When to Use |
|--------|-------------|
| **Explicit** | User states "write a 50,000-word document" |
| **Section-based** | User says "write a document with 8 sections" — multiply sections × typical section size (1000-1500 words) |
| **Depth-based** | User says "deep analysis of X with methodology, findings, discussion" — estimate 10,000-20,000 words |
| **Reference-based** | User provides a reference document of known length |

**Split decision table:**

| Estimated Words | Action | Strategy |
|----------------|--------|----------|
| < 6,000 | **Single-pass** — write in one generation | No split needed |
| 6,000 - 8,000 | **Borderline** — split recommended | Split into 2 sections |
| 8,000 - 20,000 | **Mandatory split** | Split into N sections (target 2000-4000 words per section) |
| 20,000+ | **Mandatory split + parallel eligible** | Split into N sections, write independent sections in parallel |

**Output of this phase:** A split plan:

```yaml
split_plan:
  document_title: "<title>"
  estimated_total_words: <N>
  split_decision: "single_pass" | "split_recommended" | "mandatory_split"
  section_count: <N>
  parallel_eligible: true | false
  output_format: "markdown" | "docx" | "both"
```

---

### Phase 1: Section Architecture

Design the section structure. Create a **Document Blueprint** that serves as
the single source of truth for all section writers.

**Activities:**
1. Define the chapter/section outline with titles and topics
2. Assign word targets per section (total must sum to estimated_total_words ±10%)
3. Identify dependencies: which sections need content from prior sections
4. Define shared elements: glossary, abbreviations, style guide, 5W1H tier, audience
5. Identify which sections can be written in parallel (no dependencies) vs. sequential

**Output of this phase:** A completed Document Blueprint (see template below).

---

### Phase 2: Context Package Preparation

For each section, prepare a focused **Section Context Package** that contains
everything the writer needs and nothing more.

**Each context package includes:**
- The Document Blueprint (full outline — so the writer knows their place)
- Section-specific scope (topics to cover, topics to exclude)
- Word target for this section
- Dependencies from prior sections (2-3 paragraph summary, not full text)
- Shared style guide and 5W1H tier
- Key terms and definitions relevant to this section
- Output file path

**Guidelines:**
- Keep context packages focused: the writer reads ~500-1000 words of context, not the full document
- Dependencies from prior sections are **summaries**, not full text — the writer only needs the key findings and conclusions
- If sections are written sequentially, the writer reads the actual prior section output instead of a summary

**Output of this phase:** N context packages (one per section).

---

### Phase 3: Section Writing

Write each section using its context package. Execution strategy depends on
dependencies:

| Dependency Pattern | Strategy | Execution |
|-------------------|----------|-----------|
| All sections independent | **Parallel** | All sections written simultaneously using `orchestrator-worker` Phase 0d (Parallel Output Isolation) |
| Some sections depend on others | **Hybrid** | Independent sections written in parallel first; dependent sections written sequentially after their dependencies complete |
| Strictly sequential (each depends on prior) | **Sequential** | Written one after another in order |

**Per-section writing rules:**
1. Each section MUST be self-contained — it references the blueprint but doesn't depend on other section files at write time
2. Each section writes to its own file: `section_[N]_[slug].md`
3. Each section MUST include a section heading at the correct hierarchy level
4. Each section MUST include a closing transition to the next section (for smooth assembly)
5. 5W1H enforcement is applied per-section based on the tier assigned in the blueprint
6. Style guide rules from `document-quality-standards` Module I apply per-section

**Output of this phase:** N individual section files.

---

### Phase 4: Assembly

Merge all section files into a single coherent document.

**Assembly steps:**
1. Read section files in blueprint order
2. Strip per-section frontmatter (if any)
3. Merge into a single file with consistent heading hierarchy
4. Insert table of contents (for Markdown) or generate via DOCX library (for DOCX)
5. Insert cross-references between sections where applicable
6. Apply consistent numbering to sections, tables, figures
7. Write the assembled document

**Assembly rules:**
- Section headings are promoted/demoted to match the document's hierarchy
- Transition sentences between sections are preserved from the closing of each section
- Table of contents items point to correct section headings
- If a DOCX output is required, use the `docx` skill library for generation

**Output of this phase:** A single assembled document file.

---

### Phase 5: Continuity Review

Review the assembled document for quality issues. Use the Continuity Review
Checklist (see template below).

**Review dimensions:**
| Dimension | What to Check |
|-----------|---------------|
| **Duplicates** | No finding/fact/conclusion repeated across sections |
| **Gaps** | All blueprint topics covered by exactly one section |
| **Consistency** | Terminology, tone, citation format, 5W1H tier consistent |
| **Flow** | Smooth transitions, no abrupt topic jumps |
| **References** | All cross-references resolve to actual sections, all citations present |

**Fix strategy:**
| Issue Severity | Action |
|----------------|--------|
| Critical (gaps, contradictions) | Rewrite affected sections |
| Major (tone shift, missing transition) | Edit transitions or rewrite section opening/closing |
| Minor (formatting inconsistency) | Fix in assembly step |

**Output of this phase:** Final polished document.

---

## Templates

### Template: Document Blueprint

```markdown
# Document Blueprint: [Document Title]

## Metadata
- **Target audience:** [audience]
- **5W1H tier:** [Tier 1 / Tier 2 / Tier 3]
- **Estimated total words:** [N]
- **Section count:** [N]
- **Output format:** [Markdown / DOCX / both]
- **Style guide:** [reference to document-quality-standards Module I]
- **Document type classification:** [Module A type from document-quality-standards]

## Shared Elements
- **Glossary:**
  | Term | Definition |
  |------|------------|
  | [term] | [definition] |
- **Abbreviations:**
  | Abbreviation | Full Form |
  |--------------|-----------|
  | [abbr] | [full] |
- **Citation style:** [APA / IEEE / Chicago / custom]
- **Number format:** [Indonesian (dot thousands, comma decimals) / International (comma thousands, dot decimals)]
- **Classification marking:** [PUBLIC / INTERNAL / CONFIDENTIAL / SECRET] (if applicable)

## Section Outline

| # | Section Title | Topics | Word Target | Depends On | 5W1H Tier | Writer |
|---|---------------|--------|-------------|------------|-----------|--------|
| 1 | [title] | [topic list] | [N] | — | [T1/T2/T3] | [agent type] |
| 2 | [title] | [topic list] | [N] | Section 1 summary | [T1/T2/T3] | [agent type] |
| 3 | [title] | [topic list] | [N] | — | [T1/T2/T3] | [agent type] |
| ... | ... | ... | ... | ... | ... | ... |

## Context Handoff Rules
- Section N receives: 2-3 paragraph summary of Section N-1
- Sections that CAN be parallel: [list section groups that have no dependencies on each other]
- Sections that MUST be sequential: [list section chains where each depends on the prior]

## Execution Strategy
- **Strategy:** [parallel / hybrid / sequential]
- **Total execution waves:** [N] (parallel groups)
- **Wave breakdown:**
  - Wave 1: [section IDs — write in parallel]
  - Wave 2: [section IDs — write after Wave 1]
  - ...
```

### Template: Section Context Package

```markdown
# Section Context Package: Section [N] — [Title]

## Your Assignment
Write Section [N]: "[Title]" — approximately [word_target] words.

## Scope
- **Topics to cover:**
  - [topic 1]
  - [topic 2]
  - [topic 3]
- **Do NOT cover:**
  - [excluded topic 1 — this belongs to Section X]
  - [excluded topic 2 — this belongs to Section Y]

## Document Context
- **Full document outline:** [paste Document Blueprint Section Outline table]
- **Your position:** Section [N] of [total_count] — [brief description of where this section fits in the document flow]
- **After this section:** Section [N+1] covers [brief description of next section]

## Prior Section Summary
[If this section depends on a prior section, paste a 2-3 paragraph summary of the preceding section's key findings, conclusions, and any data the writer needs to reference.]

## Shared Elements
- **Glossary (relevant terms):**
  | Term | Definition |
  |------|------------|
  | [relevant term] | [definition] |
- **Style guide (key rules):**
  - [rule 1 — e.g., use Indonesian number format]
  - [rule 2 — e.g., use "Kami" voice for institutional writing]
  - [rule 3 — citation format]
- **5W1H tier:** [T1 / T2 / T3]
  - [Tier-specific requirements — e.g., T1: include full narrative with Who, What, When, Where, Why, How]
- **Classification marking:** [if applicable]

## Output Requirements
- **Format:** [Markdown / DOCX section]
- **File path:** `/docs/[date]_[task]/implementation/section_[N]_[slug].md`
- **Heading level:** `## [Section N: Title]` (level 2 heading)
- **Must include:** Closing transition sentence to the next section

## Verification (for this section)
- [ ] Word count within ±10% of target ([word_target] words)
- [ ] All topics in scope are covered
- [ ] No topic from "Do NOT cover" appears
- [ ] 5W1H tier requirements met
- [ ] Style guide rules followed
- [ ] Closing transition present
```

### Template: Continuity Review Checklist

```markdown
## Continuity Review Checklist

### Duplicate Detection
- [ ] No section repeats the same finding/fact/conclusion from another section
- [ ] No section re-introduces a topic already covered in a prior section
- [ ] Statistics and numbers are consistent across sections
- [ ] No two sections describe the same concept using different terms

### Gap Detection
- [ ] All topics in the Document Blueprint Section Outline are covered by exactly one section
- [ ] No orphaned references (a section mentions something that isn't covered anywhere)
- [ ] All cross-references resolve to actual sections
- [ ] No promised content from the blueprint is missing

### Consistency Detection
- [ ] Terminology is consistent (same term used throughout, no synonyms for the same concept)
- [ ] 5W1H tier is appropriate per section (Tier 1: full narrative; Tier 2: concise; Tier 3: minimal)
- [ ] Tone and voice are consistent across sections
- [ ] Citation format is consistent across all sections
- [ ] Number format is consistent (all Indonesian or all International)
- [ ] Heading hierarchy is consistent across all sections
- [ ] Glossary terms are used consistently

### Flow Detection
- [ ] Each section has a smooth transition from the previous one
- [ ] The document reads coherently from Section 1 to the last section
- [ ] No abrupt topic jumps between adjacent sections
- [ ] Section pacing is balanced (no section is disproportionately long or short)

### Fix Log
| Issue | Section(s) | Severity | Fix Applied |
|-------|-----------|----------|-------------|
| [description] | [N] | [critical/major/minor] | [fix description] |
```

---

## Integration Points

### document-quality-standards Skill
Load the document-quality-standards skill alongside this skill when writing
sections. Reference the following modules:

| Module | When to Use |
|--------|-------------|
| **Module A** (Document Type Classification) | Phase 1 — determine document type for blueprint metadata |
| **Module D** (Writing Principles & Style) | Phase 2 — include relevant principles in context packages |
| **Module E** (Depth Control & Brevity Rules) | Phase 2 — set appropriate depth per section |
| **Module G** (Reference Handling) | Phase 2 — enforce consistent citation format |
| **Module H** (Anti-AI Writing Standards) | Phase 3 — applies to each section during writing |
| **Module I** (Formatting & Styling Standards) | Phase 4 — applies during assembly |

### 5W1H Tiered Enforcement
- Phase 1 assigns a 5W1H tier per section in the Document Blueprint
- Phase 2 includes tier-specific requirements in each Section Context Package
- Phase 3 enforces the tier during writing
- Phase 5 verifies tier compliance during continuity review

| Tier | Requirement |
|------|-------------|
| **Tier 1 (Mandatory)** | Full narrative — must address Who, What, When, Where, Why, How explicitly. Used for critical sections (executive summary, conclusions, recommendations, methodology, findings). |
| **Tier 2 (Concise)** | Address Who, What, Why at minimum. When and Where included if relevant. Used for supporting sections (background, literature review, detailed analysis subsections). |
| **Tier 3 (Minimal)** | Address What and Why only. Maximum 2-3 sentences per fact. Used for reference sections, appendices, tables, footnotes. |

### orchestrator-worker Skill
- When sections are independent (no Depends On), use `orchestrator-worker` for parallel execution
- Follow the **Parallel Output Isolation** rules (Phase 0d): each section writes to a unique file
- Respect **Concurrency Enforcement** limits: max 5 parallel per mission wave, no per-type cap (norma 03-09B; host cap 20)
- The assembly phase (Phase 4 of this skill) corresponds to the synthesis phase (Phase 4) of orchestrator-worker

### task-architect.md Integration
When `task-architect` plans a long document production task, it uses this skill
to:
1. Split the document into sections in the structured task breakdown
2. Assign each section as an independent subtask
3. Specify the execution strategy (parallel / hybrid / sequential)
4. Reference this skill in the delegation prompt for the executor agent

---

## References & Scripts

| File | When to Use |
|------|-------------|
| `references/late-data-integration.md` | Phase 4–5 — late data inserted after writing waves: chapter renumbering protocol (explicit map, never arithmetic bump), renumbering count drift, count reconciliation |
| `scripts/build_docx_from_sections.py` | Phase 4 assembly to DOCX — merges ordered markdown section files into a styled A4 document (headings, page breaks, tables; proven on a 61-page doc) |
| `scripts/estimate_docx_pages.py` | Verification — estimate printed page count of a DOCX without Word/LibreOffice when a page-count minimum is demanded |

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Writing the entire document in one generation (>8000 words) | Split into sections, write each independently, assemble afterward |
| Skipping the Document Blueprint | Always create a blueprint first — it's the contract between sections |
| Writing sections with no context from prior sections | Provide 2-3 paragraph summary of preceding sections as context |
| Merging sections without continuity review | Always run the continuity review checklist after assembly |
| Parallel writing without checking dependencies | Independent sections can be parallel; dependent sections must be sequential |
| Treating all sections at the same 5W1H tier | Use the tiered model — critical sections get Tier 1, supporting sections get Tier 2/3 |
| Writing sections that exceed their word target by >20% | Enforce word targets per section; split oversized sections further |
| Including the full prior section text as context | Summarize to 2-3 paragraphs — full text wastes context and dilutes focus |
| Assigning overlapping topics to multiple sections | Each topic in the blueprint belongs to exactly one section |
| Forgetting to update the blueprint when scope changes | The blueprint is the source of truth — update it first, then propagate |
| Assembly without table of contents or cross-references | Include TOC and cross-refs in the assembly step for navigability |

---

## Execution Checklist

```
[ ] Phase 0: Word count estimated and split decision made
[ ] Phase 0: If >8000 words → split is mandatory (check decision table)
[ ] Phase 0: If >20000 words → parallel execution is eligible
[ ] Phase 1: Document Blueprint created with section outline
[ ] Phase 1: Section word targets sum to total estimate ±10%
[ ] Phase 1: Dependencies identified (Depends On column)
[ ] Phase 1: 5W1H tier assigned per section
[ ] Phase 1: Shared elements defined (glossary, abbreviations, style guide)
[ ] Phase 2: Context package created for each section
[ ] Phase 2: Each context package includes scope, dependencies, style reference
[ ] Phase 2: Dependencies use 2-3 paragraph summaries, not full text
[ ] Phase 3: Each section written to its own file
[ ] Phase 3: All sections within ±10% of word target
[ ] Phase 3: Each section includes a closing transition
[ ] Phase 3: 5W1H tier enforced per section
[ ] Phase 3: Style guide rules applied per section
[ ] Phase 3: If parallel → orchestrator-worker Phase 0d enforced (output isolation)
[ ] Phase 4: Sections merged in blueprint order
[ ] Phase 4: Table of contents generated
[ ] Phase 4: Cross-references inserted
[ ] Phase 4: Heading hierarchy normalized
[ ] Phase 5: Continuity Review Checklist completed
[ ] Phase 5: Critical issues found → sections rewritten
[ ] Phase 5: Major issues found → transitions edited
[ ] Phase 5: Minor issues found → fixed in assembly
[ ] Final: Total word count within ±10% of estimate
[ ] Final: Continuity review passes with zero critical issues
[ ] Final: No duplicate findings/facts across sections
[ ] Final: All cross-references resolve correctly
[ ] Final: Document reads as a single coherent piece
```

---

## Verification

After assembly and continuity review:

1. **Every section exists** as a separate file matching the Document Blueprint outline
2. **Total word count** across all sections meets the target (within ±10%)
3. **Continuity Review Checklist** passes with zero critical issues
4. **No duplicate findings** — facts and conclusions appear in exactly one section
5. **All cross-references** resolve to actual sections
6. **Assembled document** reads as a single coherent piece, not stitched fragments
7. **5W1H tier compliance** — each section meets its assigned tier requirements
8. **Style guide compliance** — formatting, citations, number format are consistent
9. **Glossary consistency** — terms are used consistently across all sections
10. **Transition quality** — each section boundary has a smooth transition

---

## Examples

### Example 1: 25,000-Word Research Report (Parallel Eligible)

**User request:** "Write a comprehensive 25,000-word research report on renewable energy adoption in Southeast Asia, covering policy landscape, technology assessment, economic analysis, case studies, and recommendations."

**Phase 0 — Length Assessment:**
```yaml
split_plan:
  estimated_total_words: 25000
  split_decision: "mandatory_split"
  section_count: 6
  parallel_eligible: true
  output_format: "markdown"
```

**Phase 1 — Document Blueprint:**

| # | Section Title | Topics | Word Target | Depends On | 5W1H Tier |
|---|---------------|--------|-------------|------------|-----------|
| 1 | Executive Summary | Key findings, recommendations summary | 1500 | — | T1 |
| 2 | Policy Landscape | Regulatory frameworks, targets, incentives | 4500 | — | T1 |
| 3 | Technology Assessment | Solar, wind, hydro, geothermal maturity | 5000 | — | T1 |
| 4 | Economic Analysis | LCOE, investment trends, ROI | 5000 | — | T1 |
| 5 | Case Studies | Indonesia, Vietnam, Thailand, Philippines | 6000 | Section 2, 3, 4 | T1 |
| 6 | Conclusions & Recommendations | Strategic recommendations, roadmap | 3000 | Section 5 | T2 |

**Execution strategy:** Hybrid — Sections 1-4 parallel (Wave 1), Section 5 after 2-4 complete (Wave 2), Section 6 after 5 complete (Wave 3).

### Example 2: 12,000-Word Technical Specification (Sequential)

**User request:** "Write a 12,000-word technical specification for a microservices migration project."

**Phase 0 — Length Assessment:**
```yaml
split_plan:
  estimated_total_words: 12000
  split_decision: "mandatory_split"
  section_count: 4
  parallel_eligible: false  # each section depends on prior
  output_format: "docx"
```

**Phase 1 — Document Blueprint:**

| # | Section Title | Topics | Word Target | Depends On | 5W1H Tier |
|---|---------------|--------|-------------|------------|-----------|
| 1 | Current Architecture | System overview, pain points, constraints | 3000 | — | T1 |
| 2 | Target Architecture | Service boundaries, data flow, tech stack | 4000 | Section 1 | T1 |
| 3 | Migration Strategy | Phases, cutover plan, rollback | 3000 | Section 2 | T1 |
| 4 | Implementation Plan | Timeline, resource allocation, risks | 2000 | Section 3 | T2 |

**Execution strategy:** Sequential — Section 1 → Section 2 → Section 3 → Section 4. Each section receives the full output of the prior section as context (not a summary), because they build on each other.
