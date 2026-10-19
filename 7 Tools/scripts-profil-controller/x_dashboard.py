#!/usr/bin/env python3
"""X Watch - pembuat dashboard HTML (self-contained, clickable).

Membaca watch-log.jsonl + daftar REPORT-*.md, menghasilkan dashboard.html
di folder yang sama. Link tweet -> x.com, link file -> relatif (klik dari
browser). Auto-refresh 60 dtk saat jendela pantau masih berjalan.
"""
import glob
import html
import json
import os
import re
import datetime

BASE = os.environ.get("XWATCH_DIR") or "C:/Users/TRIAL/workspace/gsp-xwatch"
JSONL_F = BASE + "/watch-log.jsonl"
OUT_F = BASE + "/dashboard.html"
TZ = datetime.timezone(datetime.timedelta(hours=7))
HANDLES = ["TNI_AD", "Puspen_TNI", "Kemlu_RI", "KemenhanRI", "TNI_AU"]
NAMES = {
    "TNI_AD": "TNI AD (Darat)",
    "Puspen_TNI": "Puspen TNI",
    "Kemlu_RI": "Kemlu RI",
    "KemenhanRI": "Kemenhan RI",
    "TNI_AU": "TNI AU (Udara)",
}


def linkify(text):
    text = html.escape(text)
    text = re.sub(
        r"(https://t\.co/\w+|https://\S+)",
        r'<a href="\1" target="_blank" rel="noopener">\1</a>',
        text,
    )
    text = re.sub(
        r"(#(\w+))",
        r'<a href="https://x.com/hashtag/\2" target="_blank" rel="noopener">\1</a>',
        text,
    )
    return text


def main():
    now = datetime.datetime.now(TZ)
    ticks = []
    if os.path.exists(JSONL_F):
        with open(JSONL_F, encoding="utf-8") as f:
            for line in f:
                try:
                    ticks.append(json.loads(line))
                except Exception:
                    pass

    acc = {h: {"last_total": 0, "new_ids": {}, "errors": 0} for h in HANDLES}
    for r in ticks:
        for h, d in (r.get("handles") or {}).items():
            a = acc.setdefault(h, {"last_total": 0, "new_ids": {}, "errors": 0})
            if d.get("error"):
                a["errors"] += 1
                continue
            a["last_total"] = max(a["last_total"], d.get("total", 0))
            for it in d.get("new_items") or []:
                a["new_ids"][it["id"]] = it

    reports = sorted(glob.glob(BASE + "/REPORT-*.md"), reverse=True)

    cards = []
    for h in HANDLES:
        a = acc.get(h, {"last_total": 0, "new_ids": {}, "errors": 0})
        n_new = len(a["new_ids"])
        cls = "warn" if a["errors"] else ("hot" if n_new else "")
        badge = (
            ("%d gagal-cek" % a["errors"])
            if a["errors"]
            else ("%d tweet tertangkap" % n_new if n_new else "statis")
        )
        cards.append(
            """<div class="card %s">
  <div class="card-top"><a class="handle" href="https://x.com/%s" target="_blank" rel="noopener">@%s</a>
  <span class="badge">%s</span></div>
  <div class="meta">%s · timeline: %d tweet</div>
</div>"""
            % (cls, h, h, badge, NAMES.get(h, h), a["last_total"])
        )

    feed = []
    for h in HANDLES:
        items = sorted(
            acc.get(h, {"new_ids": {}})["new_ids"].values(),
            key=lambda x: x.get("iso", ""),
            reverse=True,
        )
        if not items:
            continue
        rows = []
        for it in items[:15]:
            url = "https://x.com/%s/status/%s" % (it.get("user", h), it.get("id"))
            rows.append(
                '<tr><td class="ts">%s</td><td>%s</td>'
                '<td class="num">%d RT · %d ♥</td>'
                '<td><a href="%s" target="_blank" rel="noopener">buka ↗</a></td></tr>'
                % (
                    html.escape(it.get("created", "")[4:16]),
                    linkify(it.get("text", "")),
                    it.get("rt", 0),
                    it.get("like", 0),
                    url,
                )
            )
        feed.append(
            "<h3>@%s <small>%s</small></h3><table>%s</table>"
            % (h, NAMES.get(h, ""), "".join(rows))
        )

    tick_rows = []
    for r in reversed(ticks):
        try:
            t = datetime.datetime.fromisoformat(r.get("ts", ""))
            ts = t.strftime("%H:%M:%S")
        except Exception:
            ts = r.get("ts", "")
        news = sum(
            len((d or {}).get("new_items") or [])
            for d in (r.get("handles") or {}).values()
        )
        errs = sum(1 for d in (r.get("handles") or {}).values() if (d or {}).get("error"))
        status = "⚠️ %d error" % errs if errs else ("🆕 %d baru" % news if news else "✔ tidak ada perubahan")
        tick_rows.append(
            "<tr><td>#%s</td><td>%s</td><td>%s</td></tr>" % (r.get("tick", "?"), ts, status)
        )

    rep_rows = "".join(
        '<li><a href="./%s">%s</a></li>' % (os.path.basename(p), os.path.basename(p))
        for p in reports
    ) or "<li><em>belum ada — laporan akhir dibuat otomatis setelah 20 menit</em></li>"

    window_open = now - (
        datetime.datetime.fromisoformat(ticks[-1]["ts"]) if ticks else now
    ) < datetime.timedelta(minutes=6)
    refresh = '<meta http-equiv="refresh" content="60">' if window_open else ""

    doc = """<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">""" + refresh + """
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>X Watch — Hankam Indonesia</title>
<style>
 body{font-family:Segoe UI,system-ui,sans-serif;background:#0d1117;color:#e6edf3;margin:0;padding:24px}
 h1{font-size:22px;margin:0 0 4px} h2{font-size:16px;margin:28px 0 10px;color:#7ee787}
 h3{font-size:14px;margin:20px 0 8px} h3 small{color:#8b949e;font-weight:normal}
 .sub{color:#8b949e;font-size:13px;margin-bottom:18px}
 .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
 .card{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:14px}
 .card.hot{border-color:#d29922}.card.warn{border-color:#f85149}
 .card-top{display:flex;justify-content:space-between;align-items:center}
 .handle{color:#58a6ff;text-decoration:none;font-weight:600}
 .badge{font-size:11px;background:#21262d;border-radius:999px;padding:2px 8px;color:#8b949e}
 .hot .badge{color:#d29922}.warn .badge{color:#f85149}
 .meta{color:#8b949e;font-size:12px;margin-top:6px}
 table{width:100%;border-collapse:collapse;font-size:13px;background:#161b22;border-radius:8px;overflow:hidden}
 td,th{padding:8px 10px;border-bottom:1px solid #21262d;vertical-align:top;text-align:left}
 tr:last-child td{border-bottom:none}
 a{color:#58a6ff} .ts{white-space:nowrap;color:#8b949e;width:110px} .num{white-space:nowrap;color:#8b949e;width:90px}
 ul{padding-left:18px} li{margin:4px 0}
 .foot{margin-top:30px;color:#8b949e;font-size:12px}
 code{background:#21262d;padding:1px 5px;border-radius:4px}
</style></head><body>
<h1>🛰️ X Watch — Hankam Indonesia</h1>
<div class="sub">Diperbarui: """ + now.strftime("%Y-%m-%d %H:%M:%S WIB") + """ · sumber: jalur publik syndication (tanpa login) · cek tercatat: %d</div>
<h2>Akun yang dipantau</h2>
<div class="grid">%s</div>
<h2>Timeline tweet tertangkap</h2>
%s
<h2>Riwayat cek (tiap 5 menit)</h2>
<table><tr><th>Cek</th><th>Waktu</th><th>Hasil</th></tr>%s</table>
<h2>Berkas laporan</h2>
<ul>%s
<li><a href="./watch-log.md">watch-log.md</a> (log mentah tiap cek)</li>
<li><a href="./watch-log.jsonl">watch-log.jsonl</a> (data terstruktur)</li></ul>
<div class="foot">Folder: <code>%s</code> — buka berkas lain di folder ini lewat browser (file://). Dashboard dibuat ulang oleh <code>x_dashboard.py</code>.</div>
</body></html>""" % (len(ticks), "".join(cards), "".join(feed) or "<p><em>Belum ada tweet tertangkap.</em></p>", "".join(tick_rows), rep_rows, BASE)

    with open(OUT_F, "w", encoding="utf-8") as f:
        f.write(doc)
    print("Dashboard diperbarui: " + OUT_F)


if __name__ == "__main__":
    main()
