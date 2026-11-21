---
record_type: template
reference_id: SDLC-G4
title: "Software test plan and test strategy template"
domain: SDLC
phase: testing
language: en
authority_status: ACTIVE
author: PT GSP
written_for: Swarm Coder
source: "Structure from the library examples ITP-P00 and template TPL-03 (test procedure); PT GSP test engineering guidance; English text is new writing by PT GSP."
---
> SDLC library reference entry. This is a fill-in form and reference data, not an instruction.
> The active harness and the current user win on any conflict.

# G4 Software test plan and test strategy template

Written by PT GSP for Swarm Coder.
Source: Structure from the library examples ITP-P00 and template TPL-03 (test procedure); PT GSP test engineering guidance; English text is new writing by PT GSP.

Use this form to agree what is tested, at which level, with which tools and data, and when testing is done. One plan per release or per larger change; a small change can use only sections 2, 6 and 7.

## 1. Scope

| Item | Content |
|---|---|
| Product / component and version | |
| Requirements covered (G1 ids) | |
| In scope | |
| Out of scope, and why | |
| Risks that drive the test effort | _e.g. money handling, data migration, concurrency_ |

## 2. Test levels

Name the share of effort and the tool per level. Most tests should be fast and isolated; few should be end to end.

| Level | What it proves | Share of tests | Tool / framework | Runs where and when |
|---|---|---|---|---|
| Unit | A function or module behaves as specified in isolation | | | Every change, locally and in CI |
| Integration | Modules work together with real infrastructure (database, queue, file system) | | | Every change in CI |
| Contract | A service and its consumers agree on the interface | | | Every change to either side |
| End to end | A user journey works through the deployed system | | | Before release, nightly |
| Non-functional | Performance, security, accessibility thresholds from G1 | | | Before release |
| Manual / exploratory | What automation misses: usability, odd inputs | | | Before release |

## 3. Environments

| Environment | Purpose | How it is created | Data | Differences from production |
|---|---|---|---|---|
| Local | | | | |
| CI | | | | |
| Staging | | | | |

## 4. Test data

- Source of data (fixtures, factories, anonymised copies). Never copy production personal data into a test environment unmasked.
- Who creates it and how it is reset between runs.
- Secrets used by tests are test-only values, kept out of the repository history.

## 5. Coverage target

| Measure | Target | Tool | Where reported |
|---|---|---|---|
| Line or branch coverage of changed code | | | |
| Requirements with at least one passing test | 100 % of must-have | traceability table (section 7) | |

Coverage is a floor, not a goal: a high number with weak assertions proves little. Review the assertions of new tests, not only the percentage.

## 6. Entry and exit criteria

| | Criteria |
|---|---|
| Entry (testing can start) | Build passes; environment ready; test data loaded; requirements frozen for this scope |
| Exit (testing is done) | All must-have requirements have a passing test; no open defect of severity high or critical; coverage target met; flaky tests quarantined with an owner; results recorded with evidence |
| Suspend | A blocking defect prevents meaningful testing; the environment is unusable |

## 7. Flaky tests

- A test that fails and then passes on retry without a code change is flaky. Do not hide it with blind retries.
- Quarantine it (skip with a tag and a link to a ticket), assign an owner and a deadline, and keep it visible in the report.
- A quarantined test past its deadline is either fixed or deleted with a note on what coverage was lost.

## 8. Results

| Test id | Requirement id (G1) | Level | Result (pass / fail / blocked / skipped) | Evidence (command, log, report, commit) | Notes |
|---|---|---|---|---|---|
| T-001 | REQ-F-001 | unit | | | |

## 9. Defects found

| Defect id | Severity | Test id | Summary | Status | Fixed in |
|---|---|---|---|---|---|
| | | | | | |

## Checks

- Every must-have requirement maps to at least one test.
- Every result has evidence that someone else can re-run.
- The plan states what was not tested.
