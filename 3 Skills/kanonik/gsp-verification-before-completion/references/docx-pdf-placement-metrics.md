# DOCX/PDF placement-layer measurement recipes (verified on STD-VISUAL sajian + Edisi-2 book)

Doctrine (born from the F18 blind spot): image gates MUST measure the PUBLISHED layer -
docx inline extents and pdf image bboxes vs page rect. Source-file extent (manifest) is only
an upstream precondition; dev=0 on the manifest coexisted with 53/53 images overflowing the
page because the builder passed mm into a Cm() helper (10x bug).

## Unit arithmetic (both tripped live probes)
- `wp:extent cx/cy` in document.xml = EMU: mm = value / 360000.
- `w:tblW w:w` and `<w:gridCol w:w>` = dxa/twips: mm = value / 1440 * 25.4.
  Using the wrong divisor yields all-FALSE results (observed: 91/91 tables "out of spec"
  with a wrong factor; correct math gave 90@128.0 + 1@166.0 mm, deviation 0).
- Sanity anchor: A4 pgSz = 11906 x 16838 twips; page width 595.32 pt.

## Probe recipes (all reproduced independently of worker scripts)
- Inline extents: regex `<wp:extent cx="(\d+)"` over word/document.xml read from the ZIP
  directly (no python-docx; avoids quadratic readers). Classify by mm; expect only the
  allowed-width token set (e.g. [128, 166]) plus known-full-page grounds ('Page Ground',
  210x297) which are legitimate - adjudicate, do not count as defects.
- PDF image overflow: `page.get_image_info(xrefs=True)` per page; defect if
  `bbox[2] > page.rect.width + 1`. Unique-xref count vs placement count distinguishes
  re-use from duplication (216 placements / 38 xref unique).
- Caption-below test: span whose text startswith 'GAMBAR' with
  `abs(span.bbox[1] - image.bbox[3]) < 30` pt.
- Body-void on a page: max block bottom excluding footer band (blocks with y0 > H-70);
  void% = (H - ymax)/H. Including the footer undercounts void by a ~60pt constant - two
  definitions coexist; quote the STRICT count for release numbers.
- Structural infeasibility proof (void tails): compare next page's tallest figure unit height
  vs remaining tail space on the void page; if unit > remainder at every site, no
  keepNext/wrap config can fix it - that is a contract decision, not a build lever.
- Footer convergence: last-page text contains 'LEMBAR <N> DARI <N>' == len(pymupdf doc)
  == Word COM ComputeStatistics; TOC convergence = pass_k == pass_{k+1}.
- Identifier census: strip tags from document.xml, regex `KL-R\d+-\d+|NEG-R\d+-\d+`;
  expect +-1 vs the fleet scanner (regex-boundary looseness) - confirm direction+magnitude.
- Em-dash/middot/CJK scan on raw bytes AND decoded text (escapes/entities count too).

## Runtime notes
- pymupdf under uv: `uv run --python 3.11 --with pymupdf python probe.py`.
- Bare `python` on this host may land on the Store alias and silently produce empty output;
  run scanners through `uv run --python 3.11 python <abs-script>` and check output file size.
- `get_image_info()` without `xrefs=True` raises KeyError('xref').
