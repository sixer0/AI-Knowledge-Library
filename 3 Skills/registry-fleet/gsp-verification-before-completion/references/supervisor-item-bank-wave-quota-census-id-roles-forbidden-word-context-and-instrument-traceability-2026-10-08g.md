# Supervisor lessons — item-bank wave: quota census, ID roles, forbidden-word context, instrument traceability (2026-10-08g)

Wave: GAYAMANUAL-1007 H11c..V15 + GM-LIB/GM-G10 countersigns, then PSIKOTES-1008 F2 close (L10..CS-2) and F3 production wave (L12..L20). All numbers are tool prints from the turns they were measured.

## 1. Additive-only forensics by substring-superset (GM-H11c)
Claim "pure additive edits, zero deletions" verified WITHOUT git (target files repo-excluded; a `git diff` probe printed 0/0 — wrong instrument, lesson-ke-11). Working method: diff pre/post line lists; for every non-matching old line test `old_line.strip() in new_line` — all 3 mismatches were strict substrings of longer new lines (328→734 chars), proving append-in-place, zero deletion. Also proves verbatim canons untouched (canon text cannot shrink).

## 2. Read the CONTRACT definition before computing a verdict (V14 self-correction, lesson-ke-12)
Supervisor's earlier hold ("weighted D4 3.96 < 4 blocks LEPAS") was wrong twice: rubrik bar for D4 is >=3 (not >=4), and aggregation is the SIMPLE MEAN of the two per-chair aggregates, not per-item pooling. Arithmetic valid, target wrong. Standing fix: before any scoring verdict, quote bar + aggregation formula FROM the contract text, then compute. Verifier V14 additionally proved its parser by REPRODUCING two prior eras' printed aggregates before judging the final era — adopt "parser sanity vs prior-era prints" as standard adjudication gate.

## 3. Quota census from the blueprint print, row-by-row (PSIKOTES L12..L17)
Never accept a card's restated quota; parse the blueprint table directly (v40 S1/S3/S4 prints: A 6+2 @70dtk 1E/3M/2D; B 5+1 1E/2M/2D; C 5+1 1E/3M/1D; D 4+1 0E/2M/1D/1VD; E 10+2 @30dtk 2E/5M/3D; F-SJT 5+9, F-WS 20+4; total inti 55 + cadangan 20 = 75). Then per-bank parse summary rows id→difficulty. Package-close arithmetic (75 == 55+20) supervisor-measured. Live pitfalls: E has ZERO "60 dtk" tokens because its tempo is 30 dtk (near false accusation — check the RIGHT denominator, lesson-ke-14); one-regex item counts across banks unreliable (A overcounts via cross-references; F returns 0 because IDs are `SJT-01`/`F1-WS-nn`) — census per-section with each bank's own ID scheme.

## 4. Reference-number roles vs real item IDs (L15)
First-pass regex found 7 "D-" IDs; D-08/D-11/D-16 are CROSS-REFERENCES to the source book's numbering (construct provenance), not bank items. Rule: in documents with source-reference numbering, check each token's ROLE in context before counting entities. Same class as GM INDEKS-vs-BADAN and SG-range traps.

## 5. Forbidden-word testing two-layer: raw grep then context adjudication (L17→L20 chain)
Raw grep of work-style block printed 11 diagnostic tokens; context showed most were (a) SJT rationale penalty descriptions or (b) DENIAL sentences ("KATEGORI ... BUKAN diagnosis"). Ruling: a banned word inside a sentence that BANS clinical claims is not a violation (generalizes L7 false-positive-lexikal to diagnostic tests). But two occurrences INSIDE WS statements ("memperbaiki gangguan kecil") are operational usage that collide with a mechanical register downstream — supervisor filed the tagihan to L20 BEFORE L20 ran. L20 executed the textbook resolution: REVISI under the card's literal register with concrete one-line substitutions, PLUS written note that teleological reading would pass both unedited and "that decision belongs to controller/user, not verifier". Standard: verifiers apply the literal gate and hand the definitional choice upward WITH both readings' evidence — never silently pick the convenient reading.

## 6. Instrument traceability census must be multi-pattern (L12 retraction, lesson-ke-12)
Supervisor tagged L12 "instruments not persisted" after globs on `*section-A*` found nothing. Wrong: the QC verifier had archived them as `qc/f3/l12_shortcheck.py` + `l12_solver.py` + `l12_ngram_test.py` + run logs (two runs byte-identical 978/978 == worker claim). Accusation formally RETRACTED via separate comment. Rule: trace census must probe card-ID AND section-name AND other-agent archive patterns (workers may save instruments under `qc/f3/<card>-*`, not beside their artifact). Worker practice stays: copy scratch scripts into `qc/` before closing (scratch workspaces vanish post-run).

## 7. Independent-instrument replication beats trusting worker logs (L12 n-gram)
Worker's originality claim (0 hits vs corpus) verified by supervisor's OWN free-tool n-gram pass (cp1252-aware tokenizer, 3,668 unique bank grams vs 73,883 corpus grams → intersection 0) plus supervisor's red control (60-token corpus sample → 52/52 recognized) and negative control (sample not matched as bank). Two-jobs-one-verdict (J8A/J8B pattern). Strongest countersign form for test-type claims: rerun the CLASS of test with an independent implementation, don't just rerun their script.

## 8. Key-determinism architecture for assessment items (L14, L20)
Durable quality bar for test banks: correct keys COMPUTED from raw stimulus data by a parser, checked two ways (count-vs-expected AND count-vs-printed-option-text) — closes "wrong key consistent with text" defect class. L14 established it; L20's verifier re-derived all 12 E keys independently (rc=0, 12/12 match). Countersign of any future bank RUNS the key-recompute script itself, not reads its log.

## 9. Race-bytes: two prints, two times, one artifact (L13)
First census caught `ca4e5a20`/13.578 B mid-run; worker verify log and later probe show `fad6b293`/15.699 B @15:29. Not contradiction — pin the FINAL sha16 (lesson-ke-13); treat cross-card byte disagreements as possible mid-run captures before suspecting mutation.

## 10. Supervisor self-garble: pre-send sensor; garble vs deliberate-quote (L20, FIX-2, J15A)
CJK sensor fired on supervisor's OWN verdict twice: once genuine typo-garble ("处方") that reached the card (fixed via separate disclosure comment), once a DELIBERATE evidence quote (`预期`) that must NOT be stripped — cleaning evidence = destroying the trail. Sensor rule: strip garble BEFORE posting; preserve foreign tokens only when the sentence names them as quoted evidence. Two-way standard applies to supervisors exactly as to workers.

## 11. Ratchet closure with three-source proof (GM-16/V15 CHECK 6b)
When a threshold was amended by authority, green must be proven PASS-by-decision across three agreeing sources (gate constant == contract decision text == rerun log), with source comment "green because the authority re-decided the threshold, NOT because measurement changed"; the measured number stays raw in check detail. Growth-rate-vs-absolute-band semantics belongs in the NEXT mission's instrument register, never swapped mid-release.

## 12. Authority-tiered closure cycle (GM-H15b block → GM-16 → rerak)
Cleanest observed chain: worker BLOCKS at authority line (refuses to move a gate constant) → controller decides BY MEASURING itself (PDF pages, sha of pre-edit build) → gate re-run over the SAME bytes → green. Byte-identical pin before/after proves closure attached no mutation. Also: controller absorbed supervisor's ratchet warning into a stricter three-evidence rule for future raises (measured source-char growth, non-decreasing density, concentrated in controller-ordered material) — supervisor proposals entering fleet rules is the healthy channel; note when a proposal is adopted in strengthened form and say so.
