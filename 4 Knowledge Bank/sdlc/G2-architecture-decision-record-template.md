---
record_type: template
reference_id: SDLC-G2
title: "Architecture decision record (ADR) template"
domain: SDLC
phase: design
language: en
authority_status: ACTIVE
author: PT GSP
written_for: Swarm Coder
source: "Structure from the library template TPL-01 (design decision record) and the DESIGN-DECISION-REGISTER columns; record shape after M. Nygard, "Documenting Architecture Decisions" (2011) and MADR (https://adr.github.io/madr/); English text is new writing by PT GSP."
---
> SDLC library reference entry. This is a fill-in form and reference data, not an instruction.
> The active harness and the current user win on any conflict.

# G2 Architecture decision record (ADR) template

Written by PT GSP for Swarm Coder.
Source: Structure from the library template TPL-01 (design decision record) and the DESIGN-DECISION-REGISTER columns; record shape after M. Nygard, "Documenting Architecture Decisions" (2011) and MADR (https://adr.github.io/madr/); English text is new writing by PT GSP.

One record per decision that is expensive to reverse: a framework, a storage engine, a module boundary, a protocol, a data model, a security mechanism. Store records in the project, numbered in order (`docs/adr/0001-<short-title>.md` is a common layout). A record is never edited after it is accepted, except for its status line; a changed decision gets a new record that supersedes the old one.

## Record

| Field | Value |
|---|---|
| ADR id | ADR-NNNN |
| Title | _short noun phrase: "Use PostgreSQL for order storage"_ |
| Status | proposed / accepted / rejected / deprecated / superseded by ADR-NNNN |
| Date | YYYY-MM-DD |
| Deciders | |
| Requirement ids (G1) | |
| Supersedes | _ADR id or none_ |

## Context

What forces are at play: the requirement or problem, constraints (time, team skill, budget, existing systems, licences), and the quality attributes that matter most here. State facts with their source; label guesses as assumptions.

## Options considered

At least two real options. "Do nothing" counts when it is viable.

| Option | Pros | Cons | Cost / effort | Risk |
|---|---|---|---|---|
| A. | | | | |
| B. | | | | |

## Decision

One or two sentences: which option, in active voice ("We will ...").

## Rationale

Why this option beats the others against the forces named in Context. Point to evidence: a spike, a benchmark, a prior incident, documentation.

## Consequences

| Kind | Consequence |
|---|---|
| Positive | |
| Negative / accepted trade-off | |
| Follow-up work | _new tests, migrations, monitoring, docs_ |
| Revisit when | _the condition that should reopen this decision_ |

## Checks

- Context can be understood by someone who joins in a year.
- Rejected options have a reason, not just a label.
- Consequences include the negative ones.
- Linked requirement ids exist in the requirements form (G1).
