# Profile B3 - MARKET / COMPETITION / EXPO (thin instantiation of general defaults)

Status: initial instantiation per blueprint 02b section 2.2 (AD-3). Neutral
instantiation of Part A defaults plus precedent provenance; no new substantive
rules. Expansion only through the Decision Log. Precedents: EXPO-INTEL sweeps,
DEMS-VSAT registry sweeps (buyer-map and query-log reused as basis).

## B3.1 Trigger
The Director nominates one market segment, competitive field, or expo/event
plus deadline. Nomination unit: one bounded market question ("who buys X in
Indonesia and through what route") or one event scope. Tiering as general.
Folder shape: `docs/<date>_dd-<market>/`.

## B3.2 Lanes (all at equal full depth)
1. demand-evidence - named buyers, budgets, tender history, planning documents.
2. competitor-matrix - incumbents and entrants on Indonesian BUYER criteria.
3. route-history - procurement routes (LPSE, INAPROC, e-katalog LKPP, SiRUP,
   RENSTRA/LAKIP) with dated history per row.

## B3.3 Mandatory questions
The seven general lane questions applied per lane: 21 grid rows minimum in
02-lanes/lane-grid.csv (manifest scripts/profiles/market.json), plus the
frozen buyer-map schema rows for every demand finding (provenance: the vendor
era buyer-map, reused unchanged).

## B3.4 Typical flags (above the general baseline four)
- demand illusion: announced programs without any budget line found after N
  dated searches (recorded as unresolved-after-N-searches, never as absence);
- incumbent lock-in: renewal pattern without open tender in the route history;
- source staleness: demand evidence older than the current budget cycle.

## B3.5 Typical artifacts
02-lanes/lane-grid.csv, 03-commercial/buyer-map.csv (frozen schema),
saturation/{demand,competition,routes}.md, query-log.csv, claims-ledger.csv.
Gate manifest: scripts/profiles/market.json (G2T grid + G2K buyer-map).

## B3.6 Presentation focus
Demand headline first (named buyers with dated evidence), then competitor
matrix on buyer criteria, then route history with windows, then known unknowns
with search counts. Depth identical across lanes regardless of order.
