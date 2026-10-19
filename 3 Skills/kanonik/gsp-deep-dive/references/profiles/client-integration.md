# Profile B4 - CLIENT-INTEGRATION (thin instantiation of general defaults)

Status: initial instantiation per blueprint 02b section 2.2 (AD-3). Neutral
instantiation of Part A defaults plus precedent provenance; no new substantive
rules. Expansion only through the Decision Log. Precedent: the engineering
mode of past GSP integration work (requirements to acceptance evidence).

## B4.1 Trigger
The Director nominates one client-side integration opportunity (a named
client's system problem plus the candidate solution) plus deadline. Nomination
unit: one client requirement cluster. Tiering as general. Folder shape:
`docs/<date>_dd-<client>-integration/`.

## B4.2 Lanes (all at equal full depth)
1. requirement-fit - what the client actually needs, measured from their own
   documents and statements, not from the sales frame.
2. integration-path - interfaces, data flows, site constraints, phasing.
3. acceptance-evidence - how acceptance will be tested, by whom, against which
   standard; what has already been accepted anywhere comparable.

## B4.3 Mandatory questions
The seven general lane questions applied per lane: 21 grid rows minimum in
02-lanes/lane-grid.csv (manifest
scripts/profiles/client-integration.json). Provenance: the general
five-x-seven bank reduced to its object-neutral core, same as B2.

## B4.4 Typical flags (above the general baseline four)
- requirement drift: stated requirement differs from the signed document
  (misrepresentation class applies to any party, including a client side);
- interface dependency on a third party that has not confirmed cooperation;
- acceptance ambiguity: no named test, threshold, or signer in the evidence.

## B4.5 Typical artifacts
02-lanes/lane-grid.csv, saturation/{requirements,integration,acceptance}.md,
query-log.csv, claims-ledger.csv, interview register (dated contact log rows
in query-log). No maps gate defined. Gate manifest:
scripts/profiles/client-integration.json.

## B4.6 Presentation focus
Requirement statement in the client's own words first, then fit scores, then
integration path with dependencies, then acceptance plan and open items.
Depth identical across lanes regardless of order.
