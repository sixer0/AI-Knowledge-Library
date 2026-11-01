# Visual-Figure QC & Rerender Chain (misi manual, 09-10)

Condensed controller lessons from running a figure-build -> vision-QC -> rerender chain for a
DATUM book mission. Reusable for any mission whose deliverable contains rendered
diagrams/charts gated by vision review.

## 1. The 7-test per-figure template (what "dibuka mata" means)
Per figure, test explicitly: (1) text clipped/cut at canvas edge; (2) text overflowing its
shape (parallelogram slants especially); (3) text-vs-text overlap (annotation labels over node
titles); (4) connector lines crossing THROUGH edge-labels (YA/TIDAK pierced by spine);
(5) palette consistency (accents not wrecking monochrome scheme); (6) legend/KEY row intact
and SYNCHRONIZED with what is actually drawn; (7) flow readable (no broken/hanging connectors).
Verdict per id: LAYAK / TIDAK-LAYAK + concrete defects WITH LOCATION (which node, which label).

## 2. Connector-continuity tests — the class mechanical gates are BLIND to
A worker rerender published 6 ids with `cacat_gerbang: 0` (fontTools geometric gate) yet
controller pixel-vision found one TIDAK-LAYAK. The gate checked label/border collisions but
NOT connector topology. Three explicit tests a QC card MUST run per diagram and report
pass/fail per id (never folded into a generic "7 tests"):
- T-A: every connector endpoint attaches to a node border OR to a bus that has an outgoing
  path to a node — zero floating stubs / dead segments between labels.
- T-B: every incoming arrow terminates AT the target node's border with an arrowhead marker;
  no arrow arriving from a separate disconnected segment; no wrong-direction arrowheads.
- T-C: no connector runs parallel riding along a node border (anchor must be mid-edge, not
  corner).
Blind-spot classes observed empirically: annotation-vs-node-title overlap; connector
discontinuity (stub/hanging, misroute, detached arrowhead); vertex clipped at canvas.
Corollary: a worker's own sensor passing is NOT evidence of visual release; controller/QC
vision on the PUBLISHED file (not scratch) is the release gate.

## 3. Snapshot-lock pattern (protect active renders from engine edits)
When a library/engine fix card (canonical-only) runs while render workers are active:
- steer each render card: copy the engine to scratch at work start, record its sha16 in the
  result, render ONLY from that snapshot for all ids + two-run determinism;
- forbid reading the live canonical path mid-run (it may be edited by the fix card);
- forbid fleet sync until renders finish (single source of truth per worker, pinned in
  manifest entries: `mesin_sha16`).
This decouples distribution timing from worker determinism entirely.

## 4. Force-done vs red-verdict (assignor closure of QC cards)
A QC card that completes its STEERED scope but withholds the population verdict because
upstream rerenders have not published yet (proven via sidecar attribution + manifest absence)
is a CORRECT closure, not a failure. Assignor closes it `complete --force` with result stating:
scope-tuntas-per-steer + gerbang-naik DITANGGUHKAN + where the gate key moved (successor QC
cards wired as downstream-gate parents). NEVER force-done over a red verdict of the card's own
evidence. Deterministic staleness proof for "not yet rerendered": sidecar `kartu` field still
names the old card + id absent from the rerender manifest.

## 5. Citation-gate parser must be LOOSE
Strict `\[S-\d+\]` misses compound forms `[S-137, S-202]`. Use `S-\d+` over all text, then
validate membership against the register KEEP set. Derived counts must state their basis
(per-file unique vs cross-file union vs token count) — "80 unique" claims that don't
reproduce are SPK-002-6 class defects; reconcile by restating basis, not by re-editing.

## 6. Register/ledger columns: measure POPULATION, not schema
A merged register carried column `bab_rujuk` in 1137/1137 entries as EMPTY — schema presence
proved nothing. Downstream gates must be planned against measured population (per-column
non-empty count), and where a column is empty, the mapping authority shifts to the artifact
text itself (e.g., citations parsed per chapter file).

## 7. Gate-selection by measurement, not card wording
When a card body hypothesizes a layout mode ("Moda A campuran") but the RULE says selection is
mechanical from the manuscript, COUNT first (citations per prose block) and bind the mode to
the count (D-24: 115 blocks, 0 cited -> Moda B obligatory). Card wording = hypothesis; the
controller breaks design deadlocks by measurement, and forbids fabricating provenance to
force a richer mode (content-kekal pin stays).

## 8. Rerender discipline after a failed vision gate
- Freeze LAYAK ids (single-writer per id; verify via sidecar attribution + mtime before and
  after); never re-render what passed.
- Require the rerender card to use the CALIBRATED gate (zero-false-positive on a known-clean
  control) as a PRE-PUBLISH requirement, plus self-vision per id before publish — the
  previous generation's own sensor may be blind to the failing class; name the blind spots
  explicitly in the card body.
- Commit/publish per-id as it passes (anti-loss under 30-min run windows), never batch to end.
- The follow-up QC card carries: per-id comparison vs the old defect column ("old defect gone
  = requirement, not bonus") + regression spot-check of a few newly-passing ids.
