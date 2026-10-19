# Profile B1 - VENDOR / PRINCIPAL (concrete instantiation of the general standard)

Authority: DD-VENDOR v0.3 / std-source Rev A, ported content-kekal under
blueprint 02b section 2.2 B1. Until DIST-2 the installed dd-vendor skill stays
authoritative for live vendor missions; after DIST-2 this file plus
templates/profiles/vendor/ plus scripts/profiles/vendor.json is the single
source of truth for vendor rules. Nothing here relaxes the general layer;
where this file is silent, references/umum/ applies verbatim.

## B1.1 Trigger
Nominated by the Director naming one potential vendor plus the deadline set at
nomination. Nomination unit: one legal entity (entity-match before anything
else). Tiering: T1 screen always; T2/T3 are the user's choice after reading the
screen report. Machine lines in nomination.md use the legacy `Vendor:` key
(the checker also accepts the general `Object:` key). Folder shape:
`docs/<date>_ddv-<vendor>/`.

## B1.2 Lanes (all at equal full depth)
1. technical - five layers x seven questions grid (02-technical/five-layer.csv).
2. commercial - market, regulation, competition, economy (03-commercial/ +
   economy workbook).
3. prospect - named Indonesian buyers, budgets, procurement routes
   (03-commercial/prospect-map.csv, buyer-map.csv).

## B1.3 Mandatory question bank
Five layers: L1-Source, L2-Processing, L3-Analytics-AI, L4-Delivery,
L5-Operations. Seven questions per layer (fixed set, minimum 35 grid rows):
- Q1 own / license / resell, and from whom;
- Q2 maturity M1..M5 with evidence (self-report alone caps at M2);
- Q3 performance vs physics limits and independent benchmarks;
- Q4 supplier / license / cloud / government dependency and its country;
- Q5 deployment mode incl. air-gap offline on Indonesian government networks;
- Q6 security and sovereignty: data location, who at the counterparty can see
  client tasking, certifications, audit logs;
- Q7 roadmap promises vs delivered, plus accuracy record of past promises.

Category question bank applies per technology category the vendor touches
(geospatial/EO, RF/SIGINT, video analytics/CCTV, platform/C2, cyber forensics,
counter-UAS, telecommunications, AI/ML platforms); a cross-category vendor
gets every matching bank's rows. Cross-cutting measurements: smallest sellable
unit; skills GSP staff must maintain; integration into GSP lines (DEMS, ATLAS,
SENTINEL, warehouse); Indonesian language in interface/reports/support;
export-control status MEASURED per flag class FL-2 (classification, license
route for an Indonesian end-user, precedents and enforcement news; presentation
only). Audit a vendor deliverable sample when one exists: observed vs inferred,
provenance, method, baseline, fusion transparency, reproducibility, language
discipline.

Commercial lane (gate G2-K as hard as G2-T): global market with real segment
definition, size and growth from at least two independent estimates presented
as ranges, demand drivers, buyer types and government share of vendor revenue,
pricing structures and public price points, commoditization direction.
Regulatory routes: remote-sensing data regime, UU 21/2013, UU 16/2012, TKDN
thresholds, UU 27/2022 (PDP), lawful interception, BSSN certification, BIG
standards, the vendor-side export control presented per FL-2, procurement
routes; verify every legal citation is in force on the date of use.
Competition matrix on Indonesian BUYER criteria (not vendor-favorite
features): capability fit, sovereignty, price model, latency, local support,
track record, country-of-origin reception, export friction, language, TKDN
route; sourceless cells stay visibly UNKNOWN; at least one comparable public
price or tender per major competitor; map local representation (each vendor's
and each competitor's Indonesian partners, since when, exclusivity, buyers
served). Economy computed in the excel-master workbook, never estimated in
prose: margin per model across the full chain, volume commitments, FX risk,
certification/stock/demo costs, break-even, pessimistic-base-optimistic
scenarios; every figure citing the workbook file. Use-case per candidate
buyer: the buyer's question in their own words, the answering capability, GSP's
added value, which GSP line grows, size signal, confidence label.

Prospect map rows (one per institution x partnership model): institution, user
unit, decision role if visible, budget source and amount if seen,
budget_visibility (seen or not-found-after-N-searches; missing visibility is a
reported finding, never silence), procurement route (LPSE, INAPROC, e-katalog
LKPP, SiRUP, RENSTRA/LAKIP, direct, unknown) with route history reference,
incumbent supplier and estimated contract expiry, time window from budget
cycles and tender calendars, pipeline_value_estimate printed from the economy
workbook (never typed as a literal), open assumptions, GSP additions and their
cost, source_url + access_date + query_count + saturation_note. Buyer catalog
rows: one per capability x institution pair with demand evidence, evidence
source and date, language requirement, local reception note, and
search_classes_touched recording which of the 8 offensive-search classes were
swept for that row.

## B1.4 Typical flags (above the general baseline four)
- FL-3 ownership acceptability vs buyer stance (who stands behind the company
  and can an Indonesian buyer accept it);
- FL-4 Indonesian rights position (distribution/integration rights, exclusivity,
  duration);
- FL-5 deployment-mode gap (what cannot be deployed where it must be).

## B1.5 Typical artifacts (frozen schemas, headers character-for-character)
templates/profiles/vendor/five-layer.csv, prospect-map.csv, buyer-map.csv;
the frozen vendor variants of screen-report.md and blok-temuan.md keep their
legacy section order and the legacy filename prospect-thesis.md (the checker
accepts both thesis filenames). Master register update targets the vendor
register (DEMS-VSAT class). Economy workbook via excel-master. Term-sheet
points on user command only. Gate manifest: scripts/profiles/vendor.json runs
the legacy G2T/G2K predicate set exactly (regression contract against the
dd-vendor era fixtures).

## B1.6 Presentation focus (prospect-first dossier order)
findings block, vendor one paragraph, PROSPECT MAP and named buyers, market and
competition, regulation and procurement, technical (five layers plus category
banks), entity and ownership, claims ledger summary and consistency flags,
economy, risk register, ask-list, completeness challenge, full data annexes.
Each section closes with two lines: what is still unknown here, and how to
search for it. Focus order never shifts depth (D-15 concrete sits here; the
general equality principle lives in A1/A3).

## Filled examples (fictional, from the V-GATE 1 fixture corpus)
Nomination excerpt:
```
# Nomination record - Example Geospatial Systems Pte Ltd
Nominated by: Director via chat, 2026-10-09
Vendor: Example Geospatial Systems Pte Ltd
Deadline: 2026-10-30
Tier: T1
First real DD: no
```
One five-layer row showing paired UNKNOWN:
```
L4-Delivery,Q6,...,UNKNOWN,n/a,n/a,UNKNOWN,first sweep of official docs,2026-10-09,n/a,official docs + trial report request + support inquiry to sales engineer
```
One prospect-map row (workbook pointer mandatory):
```
Ministry of Example Affairs,Maritime Surveillance Unit,Head of Unit via ULP,DIPA 2027,USD 4.2m,seen,e-katalog LKPP,LKPP tender 2025 ref-0042,IncumbentCo Ltd,2027-Q3,budget cycle Q1 award,reseller + local integration,see ekonomi-workbook-egs.xlsx#Pipeline!D12,volume assumption unconfirmed,integration + certification + ID language + hosting,USD 310k,https://lpse.example-ministry.id/pengadaan/2025/ref-0042,2026-10-09,17,route classes 1-8 swept for this row
```

## Common pitfalls (vendor-specific)
- Publishing a pipeline number typed into the CSV; the checker rejects a bare
  literal.
- Treating "budget not visible" as nothing to report; it is a finding with a
  search count behind it.
- Building the competition matrix on the features the vendor's deck highlights;
  the criteria belong to the Indonesian buyer.
- Starting a lane before entity-match on a name that later turns out to be a
  different company.
