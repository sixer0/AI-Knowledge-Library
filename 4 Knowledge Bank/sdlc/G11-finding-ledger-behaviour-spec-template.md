---
record_type: template
reference_id: SDLC-G11
title: "Finding ledger and behaviour spec template"
domain: SDLC
phase: understand-then-implement
language: en
authority_status: ACTIVE
author: PT GSP
written_for: Swarm Coder
source: "Method of PT GSP study-then-rebuild (reverse engineering) practice; the behaviour spec part is new writing by PT GSP."
---
> SDLC library reference entry. This is a fill-in form and reference data, not an instruction.
> The active harness and the current user win on any conflict.

# G11 Finding ledger and behaviour spec template

Written by PT GSP for Swarm Coder.
Source: Method of PT GSP study-then-rebuild (reverse engineering) practice; the behaviour spec part is new writing by PT GSP.

For work that first studies an existing program, file format or system and then builds something that behaves the same or interoperates with it. The ledger keeps what was seen apart from what was guessed; the spec keeps observed behaviour apart from the choices the new implementation makes for itself. The form works with or without an analysis tool server: an evidence id can be a tool's evidence record, a file and offset, a command and its output, or a captured request.

## 1. Questions

Turn the request into questions before looking at anything. Each question names the evidence that would answer it.

| Q id | Question | Evidence needed | Status (answered / partial / unresolved) |
|---|---|---|---|
| Q1 | | | |

## 2. Finding ledger

One row per finding. Never upgrade an inference to an observation without new evidence.

| F id | Q id | Finding | Evidence id(s) | Kind | Confidence | Search boundary |
|---|---|---|---|---|---|---|
| F1 | Q1 | | | observation / inference / unknown | high / medium / low | _what was searched, and what was not_ |

- **Observation:** directly seen in the evidence (a value in a file, a request on the wire, a function's code).
- **Inference:** concluded from observations; state the reasoning in the Finding cell.
- **Unknown:** looked for and not found within the stated boundary. Static reading never proves runtime behaviour; mark it as inference until observed at runtime.

## 3. Behaviour spec

| B id | Behaviour | Basis | Ledger ids |
|---|---|---|---|
| B1 | | observed | |
| B2 | | inferred | |

**Design choices we make ourselves** (not derived from the studied system; free to differ):

| D id | Choice | Reason | Affects |
|---|---|---|---|
| D1 | | | |

**Unknowns that block** (the build waits for these, or proceeds with a stated assumption):

| U id | Unknown | Blocks which behaviour | Plan (more analysis, ask, assume) |
|---|---|---|---|
| U1 | | | |

## 4. Verification

After building, compare the implementation with the ledger, not with memory.

| B id | Implemented behaviour | Ledger observation | Match (yes / no / partial) | Evidence (test, capture, diff) |
|---|---|---|---|---|
| B1 | | | | |

## Checks

- Every behaviour in the spec cites ledger ids or is listed as a design choice.
- Every unresolved question is visible in section 1, not dropped.
- The verification table covers every observed behaviour.
