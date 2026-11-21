---
record_type: template
reference_id: SDLC-G1
title: "Requirements and traceability template"
domain: SDLC
phase: requirements
language: en
authority_status: ACTIVE
author: PT GSP
written_for: Swarm Coder
source: "Structure from the library templates TPL-06 (requirement traceability) and the REQUIREMENT-REGISTER columns; EARS patterns after Mavin et al. (2009); English text is new writing by PT GSP."
---
> SDLC library reference entry. This is a fill-in form and reference data, not an instruction.
> The active harness and the current user win on any conflict.

# G1 Requirements and traceability template

Written by PT GSP for Swarm Coder.
Source: Structure from the library templates TPL-06 (requirement traceability) and the REQUIREMENT-REGISTER columns; EARS patterns after Mavin et al. (2009); English text is new writing by PT GSP.

Use this form to state what a change must do, how each requirement is accepted, and where its design decision, test and evidence live. One copy per feature or change set. Keep ids stable once they are referenced elsewhere.

## How to fill it in

- Write each requirement as one testable sentence. A requirement that cannot be checked is a wish; move it to Open questions until it can be.
- Give every requirement an id (`REQ-<area>-<nnn>`), and never reuse an id after it was dropped; mark it `withdrawn` instead.
- Non-functional requirements carry a number and a unit. "Fast" is not a threshold; "p95 under 300 ms for 50 concurrent users" is.
- A row is complete only when its Evidence column is filled. Finished code without evidence is still `open`.

## 1. Context and goal

| Item | Content |
|---|---|
| Feature / change | |
| Problem it solves | |
| Users or systems affected | |
| Success looks like | _one or two measurable outcomes_ |
| Requested by / decided by | |
| Date and version of this form | |

## 2. Functional requirements

| Id | Requirement (the system shall ...) | Priority (must / should / could) | Source (request, ticket, regulation) |
|---|---|---|---|
| REQ-F-001 | | | |
| REQ-F-002 | | | |

## 3. Non-functional requirements

| Id | Quality | Requirement | Threshold and unit | How it is measured |
|---|---|---|---|---|
| REQ-N-001 | Performance | | | |
| REQ-N-002 | Security | | | |
| REQ-N-003 | Accessibility | | _e.g. WCAG 2.2 level AA for the new screens_ | |
| REQ-N-004 | Reliability / availability | | | |
| REQ-N-005 | Compatibility | | _platforms, browsers, runtime versions_ | |

## 4. Acceptance criteria

Write at least one criterion per requirement. Pick one style per document.

**Given / When / Then**

| Criterion id | Requirement id | Given | When | Then |
|---|---|---|---|---|
| AC-001 | REQ-F-001 | | | |

**EARS patterns** (Easy Approach to Requirements Syntax), when a sentence form fits better:

| Pattern | Shape |
|---|---|
| Ubiquitous | The `<system>` shall `<response>`. |
| Event-driven | When `<trigger>`, the `<system>` shall `<response>`. |
| State-driven | While `<state>`, the `<system>` shall `<response>`. |
| Unwanted behaviour | If `<condition>`, then the `<system>` shall `<response>`. |
| Optional feature | Where `<feature is included>`, the `<system>` shall `<response>`. |

## 5. Traceability

One row per requirement, from the request to the evidence that it is met.

| Requirement id | Acceptance criteria | Design decision (ADR id, G2) | Code location | Test id (G4) | Evidence (command output, report, commit) | Status |
|---|---|---|---|---|---|---|
| REQ-F-001 | AC-001 | ADR-0001 | | T-001 | | open |

Status values: `open`, `in progress`, `met`, `not met`, `withdrawn`. Only `met` needs evidence; `not met` needs a note on what blocks it.

## 6. Out of scope

| Item | Why it is out | Where it goes instead (later version, other team, never) |
|---|---|---|
| | | |

## 7. Assumptions

| # | Assumption | What changes if it is wrong | Who confirms |
|---|---|---|---|
| A1 | | | |

## 8. Open questions

| # | Question | Blocks which requirement | Asked whom | Answer and date |
|---|---|---|---|---|
| Q1 | | | | |

## Checks before the form is handed on

- Every requirement has an id, a priority, a source and at least one acceptance criterion.
- Every non-functional requirement has a threshold with a unit and a measurement method.
- No requirement describes the solution when it should describe the need ("store in Redis" is a design choice; "a repeated read returns within 50 ms" is the requirement).
- Open questions that block a must-have requirement are named in the hand-off.
