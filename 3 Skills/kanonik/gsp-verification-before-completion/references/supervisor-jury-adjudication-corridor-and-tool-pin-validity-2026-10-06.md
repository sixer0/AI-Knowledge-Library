# Supervising two-jury + adjudicator corridors & tool-pin validity (GAYA-AHLI S12/S12b/S12c/S12d/S15/S15FIX/S16/S18/S20/S21, 05–06-10-2026)

Recipe for countersigning blind-jury / adjudication / scanner-tool cards. Companion to [`judge-noise-calibration.md`](judge-noise-calibration.md) (that file = calibrating juries; this file = SUPERVISING a multi-jury corridor and the tool bytes underneath it).

## 1. Corridor shape that proved healthy
patch scanner (fixture red-green) → microfix artefact per jury findings → juri-2 independen → adjudikator-3 (only when selisih ≥2 per rubrik) → putusan controller → VONIS-LEPAS atas pin revisi-C. Supervisor's job at each card: verify the PRECEDING pin lineage, not just the current claim.

## 2. Per-card verification checklist (what I actually ran, reuse verbatim)
- **Jury cards (S12c/S21/S12d):** read events for GERBANG SHA behaviour — a run that `dependency_wait`s because disk sha still equals the PREVIOUS revision's pin is the correct behaviour, praise it explicitly (objek-sama-yang-dinilai). Verify: lembar pin == pin countersign kartu revisi (not the pre-revision pin); skor beku written to file BEFORE rival sheets read (Seksi 0 giliran-log); calibrasi anchor executed and selisih ≤1 disclosed; byte-identik vs bergeser zona counts match an independent anchor mapping.
- **Disclosure chain is a quality signal, not a defect:** three consecutive agents (juri-1, juri-2, adjudicator) each self-reported their procedural leak/limit (e.g. grep inventory exposed one summary score before lock; "kesamaan angka bukan bukti independensi"). Countersign should NAME and endorse this; it is the strongest evidence the corridor is honest.
- **Divergence-by-revision-effect class:** when juri-1 (era A bytes) and juri-2 (era B bytes) differ ≥2 on the same cuplikan, the adjudicator must extract BOTH eras with separate scripts and compare via anchor mapping — reconciling across two byte-eras without doing so = invalid. Verify extract scripts per era exist (e.g. f2_adj_extract.py + f2_adj_reva.py).
- **Two-basis aggregate (K koheren vs R harfiah):** both reported with named blockers per basis = acceptable; a single convenient number = flag. Verdict "LEPAS BELUM" because procedural gates sit above both bases is CORRECT, not failure.

## 3. Tool-pin validity rule ("vonis menempel byte, termasuk byte ALAT vonis")
- Every gate report must record the scanner sha16 (full 16 hex — I flagged a 15-hex truncated pin `d61b996931e93dc` in G-NAT-53; harmless but fix downstream).
- A tool change is retroactively SAFE for old verdicts only when its scope provably cannot touch the judged layer (v1.9.1 = EN signature whitelist for letters → book-manuscript verdicts stand). State the scope argument in the countersign.
- After any tool bump, ALL later reruns must re-pin the new tool sha (PROMANUAL rerun-gerbang-kitab, the Unity book G-NAT/F8, GAYA rescan revisi-C). Two pending sensor fixes should land as ONE tool patch, not two pin churns.
- Scanner-gate "PASS" with an allow-list register means "every finding adjudicated", NOT "sensor silent" — say the difference explicitly in vonis (register 12 kelas ber-fixture, G-NAT-53).

## 4. Regression-verdict anatomy (S16, reusable template)
Regression = "lama tidak berubah KECUALI yang diputus berubah", not "semua angka bagus". Required parts, all verified present: (a) delta bernama satu-satunya = kelas putusan dengan label putusan menempel (DIIZINKAN-M-05) + cetakan LAMA/BARU berdampingan; (b) determinisme dua-run byte-identik; (c) kontrol reproduksi vs cetakan era-alat-lama yang disimpan; (d) segitiga bukti selftest+fixtures+korpus; (e) UJI DUA ARAH: check BARU wajib menagih DI ATAS ambang pada korpus BERSALAH (regression must never launder a softening sensor); (f) IDENTIK-TERURUT per korpus (nol vonis lama hilang diam-diam).

## 5. Anti-tambal-gejala contract for fixture-driven patches (S15/S15FIX)
When a card finds a latent sensor defect while building fixtures: leave the penagih fixture FAILING (NEEDS_REVIEW with known_defect), hand controller repro + options, and stipulate that after the patch the runner must reach exit-0 WITHOUT touching fixture content. Verify: sha256 of all fixtures vs manifest (I counted 33/33 beda-0). "Yang berubah sensor, bukan soalnya."

## 6. Supervisor self-instrument discipline (fires again this session)
- Before contradicting a worker's count with your own probe, test YOUR sensor against the real format: my 65/0/23 vs worker 87/0/1 collision resolved when I discovered captions use NBSP (`Figure\u00a015.1`) — worker was right; sixth occurrence of this class.
- Scan your OWN outgoing comments for planted-lesson classes: my draft carried stray CJK (caught pre-send by the same ticket I filed for others).
- Redelivered notifications: grep -c a unique vonis phrase first; corrections go in SEPARATE comments (never edit sent ones); fill map placeholders with final board print immediately before sending.

## 7. Related infra class
Worker crash <65 s on review-claim with `Unknown skill(s)` in kernel log = load `gsp-dispatch-troubleshooting/references/review-claim-skill-crash.md` (preseden S15 double-crash; decide from frozen artifacts, never blind-retry).
