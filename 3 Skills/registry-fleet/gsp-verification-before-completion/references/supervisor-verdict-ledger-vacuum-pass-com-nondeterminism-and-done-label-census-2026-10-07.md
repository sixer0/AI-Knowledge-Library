# Supervisor discipline: verdict-ledger vs tool-print, vacuum-PASS, COM byte-nondeterminism, done-label census (07-10 era, papan PROMANUAL-V2 / INDUK-1006 / RAFIFFINAL-1007)

Condensed from countersign waves 06-10 s/d 07-10. Each rule below fired in a real card this session.

## 1. Cumulative counts are LEDGER, never fresh tool output
When writing "pin X identik untuk ke-N kalinya", the ordinal N is your own tally across turns, not a measurement any single probe printed. Anti-hallucination rule (SPK-002 angka=cetakan-alat) applies to YOUR prose too. Fix pattern used at G8SYNC: rewrite to what one probe actually shows ("sha+mtime tidak bergeser sejak <ts> terukur ulang giliran ini; cacah kumulatif = ledger pengawas"). Draft the sentence, then ask: which single command printed this number? If none, relabel it as ledger.

## 2. Your own countersign is a summary too — artifacts beat it
L12B (worker) caught a contradiction INSIDE the supervisor lane: my FIX-SA3C countersign read void=5 from the six-field comment, but the card result line said "void=2" and I had not grepped it; the audit JSON (`fixsa3c_audit_pass7.json` measured void_pages=[30,37,55,69,74]) was canonical. Rule extension of "artefak menang atas ringkasan": apply the reconciliation to supervisor verdicts and worker results alike — when posting a countersign that cites an artifact field, probe the artifact JSON directly, not the prose around it. Corrections go in a SEPARATE trace comment + CONTRACT line (never edit the old comment).

## 3. Vacuum-PASS: green with zero test population is not evidence
DATUM-30 history: lint PASS in FIX-SA2/EKASLAP eras was later proven to be "0 figur ditanam" (pre-figure artifacts). A gate that passes because its subject population is empty must be recorded as VAKUM, not hijau. When countersigning any PASS, check the denominator printed next to it (figur=0, kalimat=0, baris=0 => the check never ran on real content). Corollary adopted as doctrine by controller in VERDIKT-C18-FINAL: sensors themselves must pass unit tests (a sensor once mislabeled cm as mm).

## 4. Instrument-defect verdicts: don't patch the document to satisfy the lint
Worker ruling PUTUSAN(b): DATUM-30 FAIL on every real-figure artifact, root cause found at `datum_lint.py` line 486 (regex lacks full-caps `GAMBAR` variant). Correct chain: verify root cause yourself by reading the exact line, pin the instrument file sha16+mtime for the fix card (Skill Manager lane), and state explicitly that the document must NOT be edited to please a broken matcher. Supervisor cross-check = open the cited line and reproduce the regex gap in one probe.

## 5. Word COM render is byte-nondeterministic across runs
Same docx rendered twice: pdf sizes identical (2.252.229 B) but sha differs (`5a7ae0c7` era-L12B vs `de748f1d` era-L13). Downstream (promotion, jury, closeout) must name ONE canonical pdf — prefer the one from the same generation as the printed gate verdict — and record the superseded hash in the ledger so no two-way "official pdf" claim survives. Do not treat size-equality as proof of identity; always sha.

## 6. `done` is a kernel label, not a completeness verdict
RAFIFFINAL-1007 census: cards marked done whose results were partial-handoff with placeholder bodies (bab-6..10 = 5 files of 177 B "(menyusul)", bab-11..14 absent, bab-22 absent). Before any assembly/rakit card is allowed to reach promotion, glob the parts directory and print size+mtime per file; classify anything below a real-content threshold (e.g. <1 KB with '(menyusul)' marker) as LUBANG and report count to controller. Assembly over holes is legitimate only as a REPORT (register koreksi), never as release material.

## 7. Two-definition reconciliation beats agreement demand
Void-percentage probes: worker 247/207/184 pt vs supervisor 307/267/244 pt on the same pages — constant ~60 pt offset = footer-band boundary differs between definitions. Correct verdict: "arah dan besaran sama menurut KEDUA alat; selisih = definisi batas" and require downstream to cite the STRICT threshold number. Never force both tools to one definition; state both and pick the binding one.

## 8. Long terminal commands can fail at submission ("expected string, got NoneType")
Symptom: the command never reaches the shell; short commands keep working. This is a submission-size quirk, not a tool outage. Working paths: (a) write the Python probe to a temp file via write_file, then run it with a SHORT invocation (`uv run --python 3.11 python C:/.../rm_x.py`), avoiding long inline chains joined by `;`+quotes; (b) or run the probe body via execute_code directly. Retry the same long form at most once; then switch form. Do NOT record "terminal broken" — the fix is command shape.

## 9. Promotion-with-decision pattern (E-11) worth reusing
Long mechanical chain (FIX-SA3→3B→3C→3D) ended correctly: worker exhausted sanctioned levers with mathematical proof (next-page figure height > remaining tail at every void page — reproducible by probing image bbox heights vs page void on the PDF scratch artifact), refused to shift thresholds or self-accept known-defect, escalated A/B/C options; controller decided with a printed VERDIKT naming the artifact hashes, kept the gate output FAIL in the record, archived the prior generation as `.cacat-N`, and moved bytes into release location with hash verification. Supervisor countersign checks for this class: (a) active artifact hash == the one the blocked-era countersign probed, (b) full `.cacat-*` ledger intact on disk, (c) gate verdict still printed red somewhere, acceptance is a separate named document, (d) decision-maker != worker.
