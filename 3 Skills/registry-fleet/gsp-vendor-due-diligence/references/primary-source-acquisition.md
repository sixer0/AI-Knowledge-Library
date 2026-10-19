# Primary-source acquisition for US/Nordic vendor DD — patterns measured 09-09

All fetches logged with URL + HTTP status + UTC timestamp into REGISTER-BUKTI; raw
artifacts saved under research/evidence_f1a/ (PDF, docket HTML, probe JSON).

## FTC (enforcement orders — strongest identity+legal evidence)
- Docket page: https://www.ftc.gov/legal-library/browse/cases-proceedings/<212-3035-style-slug>
  yields case status, timeline, Part 2 consents; note face-value quirks (docket printed
  "Case Status Pending" even after final order filed — publish as-is with nuance).
- Documents: download PDFs from the docket page's OWN file links
  (/system/files/ftc_gov/pdf/...complaint.pdf, ...final_consent_package_without_signatures.pdf).
  Guessed direct URLs to press-release PDFs return 404.
- Mirrors: data.aclum.org hosts copies (e.g. FTC action PDF 531.355 B); mark P (mirror) in
  register when the canonical ftc.gov path 404s.
- Extract text layer of order PDF (34 pages) for: Definitions (carve-outs, e.g. National
  Security, geofence radius 1.850 kaki), provisions I-XIX (deletion requests, retention
  schedule, privacy program, compliance reports), effective date + 20-year duration,
  absence of monetary provisions. Vendor's own volume claims inside complaint (e.g.
  "17 miliar sinyal/hari") = respondent claim, label as such.

## SEC EDGAR (corporate identity, US)
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<10-digit> — CIKs found via
search; gave Gravy Analytics CIK 0001526946 (DE, formerly TimeRAZOR, Form D 2016-2022) and
Unacast Inc CIK 0001674974. Registry-grade, entity-match PASS on official registry fields.

## Norway Brreg (Nordic affiliates)
https://data.brreg.no/enhetsregisteret/api/enheter?navn=Unacast — orgnr 913820746,
registration date; official registry API, no key.

## CourtListener API (civil litigation census)
Primary court data without PACER: per-defendant query returned 6 suits with dates;
termination nature (dismissal vs settlement) NOT derivable without PACER -> REGISTER-KOSONG.
Pattern metric that mattered: 5 of 6 suits short-lived, 1 still active (name it).

## Site liveness + structure
HTTP probe venntel.com (200), robots.txt, sitemap.xml lastmod (site maintained Aug 2026);
CMS probe wp-json/wp-login (404/403; Webflow static markers) — record "not WordPress,
no hidden content endpoints" as completed rung 3, not as buntu.
Redirect map post-merger: gravyanalytics.com -> unacast.com (brand consolidation proof).

## Archives
Wayback CDX per-url + per-domain (collapse 2015-2026, limit=-3); archive.ph/newest/<domain>.
Use for history of brand/domain, not for current facts.

## Non-verifiable-by-design items
Internal classification flags (e.g. GSP's own TERBATAS) are not external facts — record as
"BUKAN objek verifikasi eksternal; tidak naik". Legacy fleet scores are never inherited.
