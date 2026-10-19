# Supervisor: riset-lane verdicts — pin re-hash, live counter-probe, cross-lane binding, full-population index gates (2026-10-09, misi EOSRAY-1009 + BUKUV3-ING-1009 W4)

Four verdict techniques proven in one afternoon of controller L2 supervision. All are measurement recipes, not narratives.

## 1. Re-hash every source pin a register claims (fondasi terkunci)

When a research lane publishes a source register with `sha256[:16]` pins (files, email traces), the controller re-hashes the ACTUAL files before trusting any downstream citation:

```python
import hashlib, pypdf
d=open(path,'rb').read()
h=hashlib.sha256(d).hexdigest()[:16]   # compare == pin in register row
len(pypdf.PdfReader(path).pages)        # also verify claimed page counts
```

EOSRAY L1: 5/5 pins matched exactly (3 PDFs + email-trace temp file), page counts 14/17/1 confirmed. Verdict language: "fondasi provenans terkunci" — later lanes cite through these pins, so validating them once at L1 protects the whole chain. Also check entry-ID completeness mechanically: `sorted(set(int(x) for x in re.findall(r'RF-(\d+)', t)))` then report gaps (71 unique, gap [] — structural proof, not narrative claim).

## 2. Counter-probe load-bearing external claims yourself (curl + entity-match + token counts)

Pick the 2–3 claims that carry the report's verdict (budget anchors, prices, constellation status) and fetch the primary source from the controller's own network path:

```bash
curl -sL --compressed -m 45 -o out.html -w "HTTP %{http_code} size %{size_download}\n" <url>
```
then count the claimed tokens in tag-stripped text (`re.sub(r'<[^>]+>',' ',t)`). Umbra/SkyWatch price tables: every figure matched PERSIS. Blog eos.com Apr-2026 still "about to enter the satellite manufacturing industry" independently confirmed a worker's stalled-constellation claim.

Pitfall found: worker ladder cited a spacenews slug that 404s while the NUMBER was true across 5 sources. Separate the verdicts — angka PASS, URL FAIL — and hand the corrected URL to the next gate as a bekal comment; do not void the finding, do not silently bless the link.

Pitfall: some "200 OK" pages are SPA shells (doc.eos.com) — body tokens live behind JS. Presence of host proves liveness only; numeric claims from SPAs need a render rung before rising. Symptom: HTTP 200 but token counts 0 for strings the worker quoted.

## 3. Cross-lane contradiction: the lane with direct evidence binds

Two lanes reported conflicting states of the same source (L4: "planet.com/pricing live terverifikasi" via aggregator PROV; L3: direct fetch FAILED antibot twice, register left empty). Ruling: the lane holding the direct-access account binds; the other claim downgrades to PROV-with-aggregator-label or empty. Post a sinkron comment on the verification-gate card naming the binding lane, so the synthesis stage never arbitrates it again. Generalize: whenever two worker artifacts disagree about the WORLD (not about style), reconcile at verdict time and write the ruling into the contract Decision Log, not just a card comment.

## 4. Full-population index gates beat sampled query gates

W4 card demanded "10 sample queries return real paths". Controller instead validated ALL 372 index rows: every digest file exists on disk (0 missing) and every `#ANCHOR` string is present inside its target file (0 broken), plus byte-identical canonical-vs-fleet mirror hash, unit_id regex census, duplicate count, and per-row binding-stay columns (R/authority/signoff non-empty). Cost was one script pass; it caught nothing here but makes "path nyata" a population theorem, not a sample. When the artifact is a register/index, default the controller gate to full-population; keep sampling only for prose quality.

Ledger arithmetic closure (same pass): per-class state counts must sum to total rows AND cross-check against prior waves (101 buku = 40 resumed + 61 excluded + 0 registered; resumed 40 = 14+16+10). Three-way closure catches silent row loss that per-file checks miss.

## 5. Parser pitfalls when measuring fleet registers

- Delimiter varies per register: KEMAMPUAN-REGISTER.csv is comma, INDEKS-KEMAMPUAN.csv is pipe `|`, INGEST-LEDGER.csv is semicolon `;`. Read the header line FIRST and pass the right `delimiter=` to csv.DictReader, else every column parses as one None-key string and counts silently mislead.
- Legacy-era files pollute domain-folder censuses: separate mission-era artifacts by mtime (hours-old vs 358–1102h) and by presence of the era marker (`[R3` count > 0); report both populations, count only the new one.

## 6. Exempt-channel glyph findings forward as no-inherit tags

Research/identification artifacts carrying U+2014/U+00B7 are gate-exempt (kebijakan 03-09) and must NOT fail the lane verdict — but the count belongs in the verdict comment as an explicit "dilarang mewaris ke objek rilis" tag aimed at NARASI/BUILD, so the exemption does not leak into the release object. (EOSRAY: L1 31 em, L2 44 em + 2 middot in header line; L5 was clean and cited as the model.)
