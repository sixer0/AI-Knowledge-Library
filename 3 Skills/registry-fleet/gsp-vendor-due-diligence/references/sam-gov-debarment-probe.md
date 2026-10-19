# SAM.gov debarment/exclusions probe (keyless, control-positive) — measured 09-09

Purpose: hard-flag check for US vendors (Gravy Analytics / Venntel / Unacast case).
Rule: "NOT FOUND" may only be concluded from a 200 response that was PROCESSED and EMPTY,
with a positive control proving the same index+field is alive. Error responses = TIDAK
TERJANGKAU, never evidence of absence.

## Working endpoint (public UI backend, no key)
GET https://sam.gov/api/prod/sgs/v1/search/
  ?index=ex                 # exclusions index
  &q=%22Exact%20Name%22     # quoted phrase; also try single-token
  &qMode=ALL
  &is_active=true           # and a variant WITHOUT is_active (covers inactive records)
Response JSON: totalElements=0 means processed-empty. Variants to run per name:
phrase active, phrase all-records, token in index ex, and index=_all (note: _all public
mode limits entity registration domain to login; exclusions index is the relevant claim).

## Positive control (mandatory, same call shape)
q=construction -> 253 hits; q=trading -> 823 hits; fetch one full record to show fields
(title, exclusionType, excludingAgency e.g. ICE, activationDate). Proves endpoint, index,
and name-field matching are alive at measurement time. Record control in register as its
own FC row.

## Dead / gated paths (documented, not used for conclusions)
- https://api.sam.gov/entity-information/v4/exclusions — official v4 but requires api_key
  (free key needs account registration at api.sam.gov; using anyone's credentials is
  forbidden by card rules). Without key: HTTP 404 empty body. Predikat: TIDAK TERJANGKAU.
- https://saas-api.sam.gov/... — NXDOMAIN on DoH (dns.google/resolve). The old documented
  hostname is gone; do not retry blindly.
- USAspending mirrors api.usaspending.gov/api/v1/es_debars/ and /v2/ — both 404 at
  measurement time (09-09 04:06 UTC). Availability may return; re-probe in future runs.

## Register format used (worked well for verifier)
FC-nn rows: klaim | URL penuh (with query string) | timestamp UTC | entity-match = "N/A
(sistem ditanya langsung atas nama badan)" | confidence. Close with one-line VONIS:
"TIDAK ADA bendera keras" or list FOUND names -> verdict TIDAK LAYAK otomatis.

## Verdict semantics
Processed-empty for all name variants + alive control = NOT FOUND (no debarment).
Any record found = hard flag; downstream score card must flip verdict to TIDAK LAYAK.
Save raw JSON responses into research/evidence_f1c/ (browser_sgs_*.json pattern) so the
verifier can recompute without re-hitting the network.
