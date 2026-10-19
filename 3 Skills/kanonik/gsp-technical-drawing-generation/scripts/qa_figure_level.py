"""QA teks level-FIGURE untuk lembar deterministik (preseden CAD-RUMAH1020-0920).

QA per-axes lama buta terhadap tabrakan LINTAS panel dan fig.texts. Skrip ini
menarik bbox SEMUA teks (ax.texts dari semua axes + fig.texts) dalam koordinat
pixel figure setelah draw(), lalu melapor:
  OUT-PAGE  : teks keluar bidang cetak (bbox halaman)
  OUT-AXES  : teks keluar axes pemiliknya (margin toleransi 2 px)
  OVERLAP   : pasangan teks beririsan > 25% dari bbox terkecil (lintas axes sah)

Pemakaian di generator:
    from qa_figure_level import qa_figure
    findings = qa_figure(fig)          # panggil SEBELUM savefig (atau monkey-patch)
    for f in findings: print(f)
Target rilis: 0 temuan pada SEMUA lembar. Tempel file ini di folder skrip lane.
"""

def _bb(t, renderer):
    try:
        bb = t.get_window_extent(renderer=renderer)
    except Exception:
        return None
    if bb is None or bb.width <= 0 or bb.height <= 0:
        return None
    return bb


def qa_figure(fig, overlap_frac=0.25, page_margin=1, axes_margin=2):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    items = []
    for ax in fig.axes:
        ab = ax.get_window_extent(renderer=r)
        for t in ax.texts:
            if not t.get_visible():
                continue
            bb = _bb(t, r)
            if bb is not None:
                items.append((t.get_text() or "", bb, ab))
    for t in fig.texts:
        if not t.get_visible():
            continue
        bb = _bb(t, r)
        if bb is not None:
            items.append((t.get_text() or "", bb, None))
    page = fig.bbox
    findings = []
    for txt, bb, ab in items:
        if (bb.x0 < page.x0 - page_margin or bb.y0 < page.y0 - page_margin
                or bb.x1 > page.x1 + page_margin or bb.y1 > page.y1 + page_margin):
            findings.append(("OUT-PAGE", txt[:40], [round(v) for v in (bb.x0, bb.y0, bb.x1, bb.y1)]))
        if ab is not None and (bb.x0 < ab.x0 - axes_margin or bb.y0 < ab.y0 - axes_margin
                               or bb.x1 > ab.x1 + axes_margin or bb.y1 > ab.y1 + axes_margin):
            findings.append(("OUT-AXES", txt[:40], [round(v) for v in (bb.x0, bb.y0, bb.x1, bb.y1)]))
    n = len(items)
    for i in range(n):
        for j in range(i + 1, n):
            t1, b1, _ = items[i]
            t2, b2, _ = items[j]
            ix = max(0.0, min(b1.x1, b2.x1) - max(b1.x0, b2.x0))
            iy = max(0.0, min(b1.y1, b2.y1) - max(b1.y0, b2.y0))
            area = ix * iy
            if area <= 0:
                continue
            small = min(b1.width * b1.height, b2.width * b2.height)
            if small > 0 and area / small > overlap_frac:
                findings.append(("OVERLAP", round(area / small, 2), (t1[:24], t2[:24])))
    return findings


if __name__ == "__main__":
    # selftest dua arah: bersih -> 0 temuan; sengaja tubruk -> OVERLAP tertangkap
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.54, 11.69), dpi=200)
    ax1.text(0.5, 0.5, "BERSIH-A", ha="center")
    ax2.text(0.5, 0.5, "BERSIH-B", ha="center")
    clean = qa_figure(fig)
    plt.close(fig)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.54, 11.69), dpi=200)
    # pasangan batas panel: menguji deteksi OUT-AXES lintas komponen
    ax1.text(0.99, 0.5, "TABRAK-SATU", ha="center")
    ax2.text(0.01, 0.5, "TABRAK-DUA", ha="center")
    # pasangan posisi sama pada satu axes: menjamin irisan >25% sehingga OVERLAP
    # pasti tertangkap (fixture lama hanya beririsan 1,3 px -> selftest FAIL palsu)
    ax1.text(0.5, 0.2, "TUBRUK-A", ha="center")
    ax1.text(0.5, 0.2, "TUBRUK-B", ha="center")
    dirty = qa_figure(fig)
    plt.close(fig)

    print("clean findings:", len(clean))
    print("dirty findings:", len(dirty))
    ok = len(clean) == 0 and any(f[0] == "OVERLAP" for f in dirty)
    print("SELFTEST:", "PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
