# Person tracing recipe (given name -> fenced candidate) — measured 09-09

Input shape: user gives only a given name ("Jessie") tied to a company. Goal: candidate
entity-match with PROV + confidence, or a documented NEGATIF-RESULT. Never fabricate.

## Ladder that produced the hit (run in this order)
1. Official company pages first: fetch home/about/team/contact pages of every brand
   (venntel.com, unacast.com incl. redirect sources); grep token 'jess' case-insensitive
   per page; record chars fetched + hits per URL with timestamp (page dump files as evidence).
2. Sitemap sweep: sitemap.xml of each brand (venntel 43 urls, unacast 575 urls at
   measurement), fetch team-ish targets (~75), grep token. Cheap and catches bios pages.
3. Search engine: DDGS backend bing (memory: builtin web_search noisy for niche queries).
   Batched queries: '<name> <company>', '"<name>" "<Company>"', '<name> <company> <event>',
   '"<fullname guess>" "strategic partnerships"' etc. 3 batches / 41 queries / 205 raw hits
   stored as hits_jessie*.jsonl. Filter: rows with name token AND entity token
   (venntel|gravy|unacast) in title/body/href.
4. Event/conference corroboration: company LinkedIn POST announcing a speaker session
   (ISS World Nov 2025) named the person — corporate-channel attribution is the strongest
   public signal; web_extract the post.
5. Aggregators (growjo, zoominfo, leadiq, rocketreach, datanyze): use ONLY for role
   attribution, mark each as secondary; DO NOT copy contact values (emails/phones) into
   corpus; rocketreach 403 = blocked rung, recorded and moved on.
6. Archives: Wayback CDX per-URL for the LinkedIn profile (0 snaps typical for LI) and
   archive.today newest (404 = no snapshot). Nihil per class WITH account (URL+status+ts).
7. Regulator docs: extract text of FTC press-release PDF mirror, grep name tokens ->
   0 hits = valid negative datapoint (person absent from enforcement action).

## Output table per candidate (format that passed verification)
| Field | Nilai | PROV (B-nn ids) | Confidence |
Fields: Nama; Afiliasi tercantum (headline verbatim); Afiliasi historis; Bidang peran
(self-stated About text); Jabatan agregator (label disagreement between aggregators);
Peran publik (who announced them — company account vs self); Lokasi publik; Pendidikan
(self-stated, cross-check status).
Confidence per field, not global: e.g. TINGGI afiliasi / SEDANG jabatan eksak.

## Mandatory fences in report text
- Present as KANDIDAT entity-match; state explicitly that match to the user's intended
  person cannot be confirmed (user gave given name only).
- Rejected candidates section (entity-match FAIL) so downstream cannot reuse them.
- If nothing found: NEGATIF-RESULT block listing every rung + status + timestamps.
- Personal-data hygiene: professional public info only.
