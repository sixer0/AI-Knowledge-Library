# Supervisor sensor pitfalls — false-positive registry + countersign discipline

Load before cross-verifying any worker claim with a self-run probe. Every entry is a false-positive
class actually observed this fleet; test your instrument against the real artifact format BEFORE
convicting (or vindicating) an artifact.

## False-positive classes (symptom -> cause -> fixed probe)

1. **Caption/text census misses** — corpus uses NBSP (`Figure\u00a015.1`). Naive `\s` regex reports
   mass desync (observed: 65/23 wrong vs 87/0/1 true). Fix: normalize `\u00a0` -> space before matching.
2. **Path census from evidence tables** — three separate traps: (a) trailing backtick glued to path
   (markdown code spans); (b) spaces inside real filenames ("James F. Kurose...") break `\S+` token
   splitting — capture to end-of-line/pipe then `os.path.exists`; (c) relative paths in the doc will
   never match an absolute-path probe. Observed: "17 paths missing" -> actually 12/12 present.
3. **CSV delimiter** — EKASLAP `UNIT-INVENTORY.csv` is pipe-delimited; `csv.DictReader(p)` without
   `delimiter='|'` yields garbage row counts (observed: "1558 blank rows"). Always print
   `list(reader.fieldnames)` first.
4. **PDF link counting** — URI links usually live in `page.get_links()`, NOT `page.annots()`
   (annots-only probe returned 0 on a doc with 1692 links). Count both surfaces.
5. **"Truncated URL" claims** — substring filters like `'(SICI'` or `'0749-5978(85'` match VALID full
   DOIs (parentheses are legal inside DOI names). Always print the FULL href and compare against the
   expected complete form before declaring truncation. Observed: my filter said "3 truncated"; all 3
   were intact.
6. **Byte-size mismatch vs claim** — check newline convention first: disk bytes with CRLF vs reported
   LF count differ by exactly the number of CR bytes (observed 30.504 vs 30.329 = 175 CRs). Two
   conventions coherent != miscount. Record sha16-of-content and note which convention it pins.
7. **grep status anchors** — sha256 strings can contain "404"/"500"; grep must anchor to the status
   column, not free text.
8. **python-docx `add_*` cost curve** — build time grows quadratically per block (measured 5s->88s per
   1500-line block); a stalled big-docx build is usually this, not a hang. Heavy builders: XML-per-part
   + single insert, or docxcompose split-build (proven on 2 MB master: run-1 died at 68%, run-2 finished).

9. **XML read layer != semantic assert layer (run vs paragraph)** - chip text compared to a
   manifest per `<w:r>` reports false loss after a Word round-trip. Word repaginates runs that
   exceed the frame width when `hAnchor="margin"` is active and splits one chip into two
   `w:r`, while paragraph content stays whole (layout effect, not content loss). Observed on
   real post-embed bytes (kartu t_fcdd32ac, diukur ulang manager t_618c93d4): sensor level-RUN
   hilang=1 JEBOL on attr-margin + attr-minmargin vs level-PARAGRAF hilang=0 OK; kontrol
   `hAnchor="text"` OK on both layers; chip terbelah = "[R -
   ADINT-LIBRARY-INDEX-MASTER-V1.MD BAGIAN 8]" (47 char, dua `w:r`). Fix: bandingkan teks chip
   di LEVEL PARAGRAF - gabung SEMUA `w:t` dalam paragraf ber-`framePr` - sebelum memvonis chip
   hilang; pakai lapis run hanya untuk assert gaya per-run. Jangan ubah semantik gerbang,
   hanya lapis bacanya. Tercatat 2026-10-09 (kartu t_be1b447e, tenant CTXWIN-1009).

10. **Name census di era peran-via-berkas (PMODE-1010)** - menghitung semua token `gsp-*` pada
    blueprint sebagai klaim profil hidup melaporkan belasan hantu positif-palsu, karena tabel
    breakdown kini merujuk BERKAS PERAN arsip (`roles/gsp-document-writer.md`) yang memang bukan
    profil hidup. Probe benar (kartu t_ba326b9e, tenant BMR-1010): buang frontmatter YAML (baris
    `agent:` = identitas penulis, bukan penugasan), lewati token berprefix `roles/` atau berekor
    `.md`, lewati nama skill, baru tagih sisanya ke `fleet/PROFILE-REGISTRY.json`. Lengkapi dengan
    sensus kolom PERAN per kendaraan (worker 12 / fast 6 / thinker 8 / hidup 3 = 29 baris), karena
    hitung-per-baris menangkap salah penugasan yang lolos dari cek himpunan nama.

11. **Lapis angka papan wajib dipin sebelum membandingkan** - satu tenant memberi angka berbeda
    antara lapis `tasks` (completed_at minus started_at) dan `task_runs` (per-run, bisa difilter
    outcome). Terukur pada GAYA-AHLI-1005: median 16,6 vs 15,1 mnt, p90 30,2 vs 27,5 mnt, total
    kerja 20,08 vs 14,92 jam, utilisasi 1,46x vs 0,89x. Keduanya jujur; mencampur tanpa menyebut
    lapisnya tidak. Countersign klaim dinding-waktu atau utilisasi wajib (a) menyebut lapis mana
    yang mereproduksinya dan (b) melaporkan run-per-kartu beserta outcome `timed_out`/`crashed`/
    `blocked`, karena proyeksi dari kerja `completed` saja diam-diam mengasumsikan nol retry.

12. **Objek vonis bermutasi di tengah giliran** - saat artefak yang divonis ditulis ulang penulis
    sementara verifier bekerja (terukur: BANDING.md 3.782 B menjadi 6.835 B pada mtime 1791627580
    di tengah t_ba326b9e), JANGAN memvonis salinan pertama. Baca ulang, pin sha16 + ukuran + mtime
    versi yang benar-benar divonis sebagai CHECK 0 instrumen, lalu diff kedua versi untuk isi yang
    hilang: satu pass naturalisasi bisa menghapus klausul batas jujur tanpa mengubah angka (temuan
    R-1 giliran ini: klausul nol-retry hanya ada di draf yang tersupersede).

13. **Intro-figur / caption census pada docx** - dua jebakan terukur satu run (BUILDR
    t_8f332328, RAFIF-REVB-1010): (a) regex paragraf `<w:p\b.*?(?:</w:p>|/>)` memotong teks
    di TAG MANDIRI-TER-TUTUP pertama di dalam paragraf (bookmarkStart dll) -> hampir semua
    paragraf terpotong buta; pakai `<w:p\b[^>/]*(?:>.*?</w:p>|/>)`. (b) baris INTRO dan baris
    CAPTION sama-sama berawalan label (`Gambar 0.1 ...`), sehingga `t.startswith(label+" ")`
    memilih baris INTRO sebagai anchor -> jendela pra-caption kosong -> intro_pct palsu 37,7%
    vs sejati 91,5%. Fix: cocokkan baris caption dengan TEGAS string caption manifest utuh
    (`t.strip() == cap.strip()`) dan kontrol-silang terhadap angka kanal md hulu (misync
    besar = sensor yang salah, bukan artefaknya). Tercatat 2026-10-10 (kartu t_8f332328;
    dinaikan apa adanya dari salinan fisik profil gsp-worker oleh DUPSKILL-L3, hanya
    indentasi dan penomoran yang diperbaiki: semula tersesat sebagai sub-item di bawah 9).

## Countersign discipline (pengawas)

- **Angka = cetakan alat pada giliran ini.** Never cite board maps, sizes or verdicts from memory or
  from another agent's report; re-census (`awk` over `hermes kanban list`) in the SAME turn, immediately
  before sending, and fill the map into the comment text before the send command runs.
- **Draf vs tayang:** run the glif/CJK sensor over the TEXT THAT ACTUALLY AIRED (`kanban show | grep`),
  not the local draft — pre-send scripts may have silently fixed or missed tokens (lesson-ke-9).
- **Corrections ride as separate comments**, never edits of old comments; prefix "KOREKSI ... (komentar
  terpisah, disiplin jejak)".
- **Redeliver guard:** before commenting on a re-notified card, grep-count your own prior markers
  (both capitalizations! a case-wrong grep returning 0 once nearly caused a duplicate vonis). If the
  result text matches what you already measured, send nothing.
- **Silent closures** (done without notification): still countersign from disk measurement — but state
  in the comment that the verdict came from disk, not from a notification.
- **Self-correction before verdict:** when your probe contradicts the worker, classify each finding
  (meta-block quoting banned phrase, structural table label, mention-use) before accepting either side;
  four boards this session showed both directions of error possible.
- **Vonis menempel byte — termasuk byte alat vonis.** Reports must name scanner pin (16 hex, full);
  pin era-change (e.g. v1.9.0->v1.9.1) requires re-run or explicit non-impact clause. Watch mirror
  drift: profile copies of the scanner can lag the canonical (F-25-7 class) — probe byte-identity
  kanonik-vs-fleet-vs-profil before trusting any scan output.
