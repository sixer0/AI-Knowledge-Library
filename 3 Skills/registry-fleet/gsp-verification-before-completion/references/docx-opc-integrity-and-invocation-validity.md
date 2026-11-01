# DOCX OPC integrity + invocation validity (GAYA-AHLI/misi buku 06-10-2026)

Two verification classes that passed every existing gate and still shipped a
broken artifact / vacuous claim. Both generalize beyond the missions found in.

## 1. Invocation validity — a PASS proves nothing about the wrong subject

Case F-25-1 (GAYA-AHLI-1005): release gate claimed "scanner v1.9.1 PASS pada
revD". Actual invocation was `scan_ai_footprint.py --text <path>` — the scanner
measured the two-word PATH STRING, not the 242 KB manual. The printed header
(`berkas | teks-1 [md]`) exposed it; scanning the real body produced >=8 FAILs.
The controller's VONIS-LEPAS rested on this foot among two, and the supervisor's
own earlier countersign had endorsed the claim embedded in an adoption artifact
without testing the invocation.

Rule: before endorsing ANY tool verdict (yours or another agent's), confirm from
the print header / argv WHICH OBJECT was measured. Cheap tells: entry-count of
"1", sizes in bytes matching a path length not a file, header lines echoing the
argument verbatim. Re-run with the file as positional arg before repeating the
claim. "angka = cetakan alat" applies to the tool's SUBJECT too, not just its
numbers.

## 2. OPC integrity — tolerant parsers cannot certify a DOCX opens

Case PDF-55 (book mission): `<book-manuscript>.docx` passed gate54
10/10 (two-build idempotency, tail check, 88 media, 333 links, 144 tables) yet
Word refused it: "The file appears to be corrupted" (wdmain11.chm 25272),
including via OpenAndRepair=True. Roots, both invisible to python-docx /
ElementTree / zipfile readers:

- Duplicate `Id="rId46"` in `word/_rels/document.xml.rels` -> two Targets
  (`media/fig_4-1.png` and `media/rId46.png`); OPC requires unique Ids. Cause:
  a CARRIED image from the previous edition reused an Id that a NEW relation
  also took (carry+new collision).
- 89 `[Content_Types].xml` Overrides pointing at parts absent from the package
  (leftover Ed2-era `/word/media/rIdNN.png` names).

python-docx resolves duplicate Ids silently and never validates Overrides —
so zip-level probes (media count, embed count, caption regex) all stayed green.

Three hard OPC checks for any programmatically built DOCX (stdlib zipfile+re):

```python
import zipfile, re, collections
z = zipfile.ZipFile(p)
rels = z.read('word/_rels/document.xml.rels').decode('utf-8')
ids = re.findall(r'Id="([^"]+)"', rels)
dups = [k for k, v in collections.Counter(ids).items() if v > 1]        # (a) must be []
ct = z.read('[Content_Types].xml').decode('utf-8')
parts = set(z.namelist())
orphan = [o for o in re.findall(r'PartName="/([^"]+)"', ct) if o not in parts]  # (b) must be []
# (c) real open probe: Word COM Documents.Open (or strict OPC validator).
```

Chain-control to localize harness-vs-object: repack a KNOWN-GOOD source
byte-per-byte through the same harness; if that opens OK, the harness is clean
and the defect is in the object. Deduping naively is WRONG — both figures then
render the same image; give carried images fresh unique Ids and drop ghost
Overrides, rebuild idempotent, re-pin.

## 3. python-docx quadratic build = bridge-timeout class

Adding paragraphs/tables one-by-one to one Document is quadratic: measured
5s/7s/13s/23s/52s/88s per successive 1500-line block (~68% done at run kill).
For multi-thousand-line masters use either (A) split-build per section then
merge with docxcompose, or (B) build body XML per part as strings and insert
once into document.xml with styles pre-declared; cache the style dict; build
each table whole (add_table(rows=0) then grow is the most expensive pattern).
A partial artifact must NEVER remain under the final filename — rename
`*.part.docx` so downstream cannot mistake it (observed near-miss).

## 4. Reconstructing a lost verdict byte (revD case)

When the exact bytes a verdict pinned are no longer on disk (only later
revisions archived): reconstruct deterministically from the later revision by
reversing the named ledger edits, ASSERT sha256[:16] == recorded pin, then
archive as `_arsip/<doc>.rev<X>.md`. Verified: revD c317e0fbcafbefb7 rebuilt
byte-exact from revE + reverse-edit; one copy into _arsip restores the
custodian's ability to open the judged byte. If assert fails, record
known-defect in the register instead of promoting.
