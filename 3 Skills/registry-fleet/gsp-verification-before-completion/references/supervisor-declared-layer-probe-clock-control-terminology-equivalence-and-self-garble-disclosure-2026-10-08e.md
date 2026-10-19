# Supervisor lessons 2026-10-08e — declared-layer probes, clock control, terminology equivalence, self-garble disclosure

Source: GAYAMANUAL-1007 GM-H15a countersign (t_6eae1f4e, run 5495, 2198s) plus its
follow-up self-correction comment. Four durable techniques, all verified on disk.

## 1. Probe the layer the card DECLARES, not the layer you assume (pelajaran-ke-11, wrong-target variant)

GM-H15a claimed four edits landed "di lapis blok-naskah/mesin-rakit". First probe searched
the source blocks (`gm-blok1/3.md`) for the F1 equivalence entry and F6 L.D items — got
zeros, nearly written up as missing work. The card's own wording said the injection happens
via `gm_l7_merge.py`: the correct probe target is the MERGED MANUSCRIPT
(`work/gm_l7_naskah.md`), where both landed (kesetaraan x3, butir (12)-(16) 1+1+1+1+1).

Rule: when a card names its edit layer (blok / merge / build / gerbang), read that layer's
artifact first. Block-file absence is NOT a finding when merge injects at build time —
the merge output is the ground truth, and the block file legitimately stays "cermin sumber".
This is the same two-layer-one-truth pattern as the GM-08 canon swap (block mirrors source,
merge resolves to canon); the supervisor probe must follow the resolver, not the mirror.

## 2. Clock control (mtime census) as a cheap freeze proof for "untouched" claims

F5 claimed five caption quotes were peeled via an `_unq` plate at BOTH readers (merge and
build) while the five sidecar YAML bytes stayed frozen per ledger pins. Proof without
hashing every file: `os.path.getmtime` census over `output/figura/*.yaml` showed newest
sidecar at 05:49/20:07, strictly older than the run window 11:10–11:46. Combined with the
claim being about *reader-side* transformation, the clock alone validates the freeze.
Use mtime windows whenever the claim is "X was not touched", reserving sha probes for
"X equals pin Y". (Same family as the FG2b/figures-fg1 clock controls.)

## 3. Terminology-equivalence register entry beats editing either side of a canon conflict

F1 was a real conflict: verbatim SG-L6-16 says "tiga dimensi", patched prose says "empat
dimensi" — and the ruling (GM-14/GM-15) forbids touching verbatim SG statements. The
worker's fix: ONE closing entry in register L.C stating the equivalence formula
(three judged dimensions + one guard = four score columns; the four-dimension in-book
procedure is CORRECT). Both texts survive byte-identical; the contradiction is re-read as
terminology mapping. This is the same move as STDM-PV conflict resolution (respect all
precedents, don't weight-pick) and beats both failure modes (silently editing the canon,
or flagging the conflict to the user when a documented equivalence closes it).
Supervisor framing: when a fix claim says "konflik diselesaikan", check WHICH side moved —
if neither moved, demand the equivalence artifact and verify both originals are intact.

## 4. Self-garble disclosure: the supervisor's own comment can carry the defect class it bills

Guard printed CJK=2 on the H15a verdict comment itself ("注入" inside a Latin sentence) —
the exact garble class billed to workers since L12C-D. Handling that kept the ledger clean:
(1) do NOT edit the posted comment; (2) post a SEPARATE self-correction comment naming the
locus, the intended word, and the disposition ("substansi tak terdampak; hilir jangan
mewarisi sebagai kutipan mentah"); (3) add the pre-send CJK/em-dash/middot scan to the
supervisor's OWN send path, not just the worker's — the guard-after-post catches it, but
pre-send scan avoids the errata trail entirely. Pre-send scan snippet (already standard
for drafts): `sum(1 for c in t if '\u4e00' <= c <= '\u9fff')` plus U+2014/U+00B7 counts,
run on the final file AFTER typo fixes, before `hermes kanban comment`.
