---
name: gsp-deep-dive
description: "GSP Deep-Dive Standard (GSP-DD-001): when the user nominates an object of ANY class (vendor/principal, technology/product, market/competition/expo, client-integration, or a newly accepted class) and sets a deadline, measure it deeply and equally across the profile lanes to saturation-with-numbers, then present the record; the fleet never decides."
version: 0.1.0
metadata:
  hermes:
    tags: [gsp, due-diligence, deep-dive, dossier, standard]
    category: gsp
---

# GSP DEEP-DIVE - General Standard for All Deep Dives (GSP-DD-001)

Status: APPROVED and installed by card t_cac44e70 (DIST-2, mission
DDV-STD-1009) into the canonical workspace skills folder and the fleet registry,
after V-GATE2 verdict PASS 9/9 (verification/VERDICT2.md, pin gen-source
sha256[:16] c50e2b4d2011de46). Built under card t_e58b6970 per blueprint
identification/02b_general-structure.md section 4. Name remains
DEFAULT-REVERSIBEL DR-1 (open veto). Source of authority: the GSP Deep-Dive
Standard (gen-source.md, provisional number DD/GSP/STD/X/2026). As of DIST-2
this skill is the single source of truth for all deep-dive classes including
vendor: the former dd-vendor package is now a compatibility shim pointing here,
and its rules live in references/profiles/vendor.md (profile B1) with the
regression contract proven identical (V-GATE2 CHECK 5).

## Trigger (manual only)
This skill activates ONLY when the user (the Director) nominates one object and
sets the mission deadline at nomination time. The nomination MUST state the
object CLASS (vendor, technology, market, client-integration, or a class
accepted through the profile contract procedure); if the class is unclear the
fleet asks once before starting. There is no automatic intake: an inbound
email or deck is reported as presence and never processed until nominated.

## Controlling mandate: MEASURE AND PRESENT, NEVER DECIDE
The fleet measures, fills, searches, and presents. Business outcomes belong to
the Director alone. The only decision surface in any deliverable is the empty
slot `Director decision: ______`, which the fleet never fills. Two brakes stop
a lane: a saturation statement with numbers, or the user deadline. All lanes
run at equal full depth; depth equality is a user decision, never a workload
preference.

## Stage sequence S0-S6 (general skeleton; profiles fill the slots)
| Stage | Work | General reference | Gate |
|---|---|---|---|
| S0 | Nomination, entity disambiguation, document register, thesis, seed flag register, tier + deadline recorded | references/umum/s0-nomination-registration.md | G0 |
| S1 | Screen report (T1): material claims into the ledger, first-pass flag register, top five asks, prospect sketch | references/umum/s1-screen-report.md | G1 |
| S2-S3 | Lane dissection: lanes are DEFINED BY THE PROFILE, all at equal full depth | references/umum/s2-lane-dissection.md | G2 per profile manifest |
| S4 | Presentation package: findings block, nine dimension cards, blind completeness challenge | references/umum/s3-presentation-package.md | G3 |
| S5 | Director cycle: answer cycle without billing clocks | references/umum/s4-director-cycle.md | none (human stage) |
| S6 | Close-out and knowledge promotion: IL promotion, register update, refresh triggers | references/umum/s5-closeout-promotion.md | G4 |

Read first, before any lane starts: references/umum/cross-stage-rules.md
(lane law, offensive search, SPK-002, output shape) and
references/umum/gates.md (gate predicates, folder layout, how to run
gate_check --profile).

## Profiles (pick one at nomination; new classes via the profile contract)
| Profile | Reference | Manifest | Lanes |
|---|---|---|---|
| B1 VENDOR / PRINCIPAL | references/profiles/vendor.md | scripts/profiles/vendor.json | technical, commercial, prospect |
| B2 TECHNOLOGY / PRODUCT | references/profiles/technology.md | scripts/profiles/technology.json | capability-vs-physics, maturity-evidence, integration-fit |
| B3 MARKET / COMPETITION / EXPO | references/profiles/market.md | scripts/profiles/market.json | demand-evidence, competitor-matrix, route-history |
| B4 CLIENT-INTEGRATION | references/profiles/client-integration.md | scripts/profiles/client-integration.json | requirement-fit, integration-path, acceptance-evidence |

A fifth class enters through templates/profiles/_template/ plus the acceptance
procedure in references/umum/gates.md section 6 (six blocks, provenance per
question, fixture pair, manifest json, zero edits to the general layer).

## Executable instruments (scripts/)
- `gate_check.py <record-dir> [--profile <name>] [--gate G0|G1|G2T|G2K|G3|G4|all] [--json] [--master-register <csv>]`:
  deterministic completeness check. Without --profile only the general gates
  run (lane gates are reported skipped, never silently passed). With
  --profile the manifest scripts/profiles/<name>.json adds the profile lane
  gates. Exit 0 = all selected gates pass; 1 = at least one FAIL (names
  printed); 2 = misuse (bad profile, unreadable folder or register).
- `recompute-checks.py <claims-ledger.csv> [--tolerance 2.0] [--json]`:
  unchanged from the dd-vendor era (the ledger schema is frozen). Writes
  `<ledger>.checked.csv` beside the input; input never modified. Exit 0 = all
  consistent; 1 = mismatch beyond tolerance or load-bearing numeric claim
  without test_method; 2 = misuse or header mismatch.
- `fixtures/`: complete and broken miniature records for ALL FOUR profiles
  (`{complete,broken}/<profile>-record/`). Per profile the pair proves both
  directions: complete exits 0, broken exits 1 with named FAILs. Run the pair
  before trusting any edit to either script. `fixtures/make_fixtures.py`
  regenerates the three non-vendor pairs; the vendor pair is a frozen
  content-kekal port of the V-GATE 1 fixtures and must stay byte-identical
  (regression contract).
Both scripts are stdlib-only Python >= 3.10, no network, no LLM, no eval().
Fleet execution pattern: `uv run --python 3.11 python <script> ...`

## Templates (templates/)
General: record-layout.md, screen-report.md, blok-temuan.md, claims-ledger.csv,
risk-register.csv, ask-list.csv, document-register.csv, query-log.csv,
validation-first-arrival.md. Profile-specific: templates/profiles/vendor/
(five-layer.csv, prospect-map.csv, buyer-map.csv plus the frozen vendor
variants of screen-report and blok-temuan; headers are fixed schemas,
character-for-character). New classes start from templates/profiles/_template/.
CSV headers are frozen: never rename, reorder or add columns. Empty cells are
forbidden: write UNKNOWN plus the search route, or N/A plus the reason.
