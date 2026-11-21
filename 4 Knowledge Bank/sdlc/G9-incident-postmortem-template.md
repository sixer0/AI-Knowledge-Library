---
record_type: template
reference_id: SDLC-G9
title: "Incident postmortem template (blameless)"
domain: SDLC
phase: maintenance
language: en
authority_status: ACTIVE
author: PT GSP
written_for: Swarm Coder
source: "Structure after the library template TPL-09 (nonconformance report) and common blameless postmortem practice; English text is new writing by PT GSP."
---
> SDLC library reference entry. This is a fill-in form and reference data, not an instruction.
> The active harness and the current user win on any conflict.

# G9 Incident postmortem template

Written by PT GSP for Swarm Coder.
Source: Structure after the library template TPL-09 (nonconformance report) and common blameless postmortem practice; English text is new writing by PT GSP.

Write a postmortem after any incident that affected users, lost data, or needed an emergency change. Blameless means the write-up explains how the system and the process allowed the failure; it names roles and actions, not people to blame. Draft it within a few days, while logs and memory are fresh.

## 1. Summary

| Field | Value |
|---|---|
| Incident id and title | |
| Severity | |
| Start, detection, mitigation, resolution (with time zone) | |
| Status | draft / reviewed / actions closed |
| Author and reviewers | |

Two or three sentences: what broke, for whom, and how it was fixed.

## 2. Impact

| Question | Answer |
|---|---|
| Who was affected (users, customers, internal teams) | |
| How many, and how was that counted | |
| For how long | |
| What they could not do | |
| Data lost or corrupted, and whether it was recovered | |
| Commitments breached (SLA, SLO, legal) | |

## 3. Timeline

Facts with timestamps and sources (alert, log line, chat message, commit). No interpretation here.

| Time | Event | Source |
|---|---|---|
| | | |

## 4. Root cause and contributing factors

- **Trigger:** the change or event that started it.
- **Root cause:** the underlying condition that let the trigger cause harm. Ask "why" until the answer is a condition you can change, not a person.
- **Contributing factors:** what made it worse or slower to detect (missing alert, unclear runbook, no test for this case, risky deploy timing).

## 5. Detection and response

| Question | Answer |
|---|---|
| How was it detected (alert, user report, by chance) | |
| Time from start to detection, and why | |
| What helped the response | |
| What slowed it down | |

## 6. What went well, what did not, where we were lucky

| Went well | Did not go well | Lucky |
|---|---|---|
| | | |

## 7. Action items

Each action is specific, has one owner and a due date, and is tracked in the normal issue tracker.

| # | Action | Type (prevent / detect / mitigate / process) | Owner | Due | Ticket | Status |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

## Checks

- The timeline is backed by sources.
- No sentence assigns blame to a person.
- Every contributing factor has at least one action, or a note why none is taken.
- Changes shipped as a result are recorded in the changelog (G8).
