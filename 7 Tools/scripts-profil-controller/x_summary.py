#!/usr/bin/env python3
"""X Watch - laporan akhir setelah 20 menit pemantauan.

Membaca watch-log.jsonl (hasil x_watch.py), merangkum tweet BARU per akun
selama jendela pantau, menulis REPORT-<tanggal>.md, dan mencetak ringkasannya.
"""
import json
import os
import datetime

BASE = os.environ.get("XWATCH_DIR") or "C:/Users/TRIAL/workspace/gsp-xwatch"
JSONL_F = BASE + "/watch-log.jsonl"
TZ = datetime.timezone(datetime.timedelta(hours=7))


def main():
    now = datetime.datetime.now(TZ)
    cutoff = now - datetime.timedelta(minutes=25)
    ticks, per_handle, errors = [], {}, []
    if os.path.exists(JSONL_F):
        with open(JSONL_F, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                ts = r.get("ts", "")
                try:
                    t = datetime.datetime.fromisoformat(ts)
                except Exception:
                    continue
                if t < cutoff:
                    continue
                ticks.append(r)
                for h, d in (r.get("handles") or {}).items():
                    acc = per_handle.setdefault(
                        h, {"new": [], "errors": 0, "last_total": 0}
                    )
                    if d.get("error"):
                        acc["errors"] += 1
                        continue
                    acc["last_total"] = d.get("total", acc["last_total"])
                    for it in d.get("new_items") or []:
                        acc["new"].append(dict(it, handle=h))

    lines = [
        "# Laporan Pemantauan X — Hankam Indonesia",
        "",
        "**Periode:** %s s.d. %s (4x cek @5 menit)"
        % (cutoff.strftime("%H:%M"), now.strftime("%H:%M WIB")),
        "**Akun:** TNI_AD, Puspen_TNI, Kemlu_RI, KemenhanRI, TNI_AU",
        "**Jumlah cek tercatat:** %d" % len(ticks),
        "",
        "## Tweet baru terdeteksi",
        "",
    ]
    total_new = 0
    for h, d in sorted(per_handle.items()):
        uniq = {it["id"]: it for it in d["new"]}
        items = sorted(uniq.values(), key=lambda x: x["iso"], reverse=True)
        total_new += len(items)
        if d["errors"]:
            lines.append("- **@%s** — %d cek gagal ambil data" % (h, d["errors"]))
        if items:
            lines.append("- **@%s** — %d tweet baru:" % (h, len(items)))
            for it in items[:10]:
                lines.append(
                    "  - [%s] %s (RT %d / ♥ %d)"
                    % (it["created"][4:16], it["text"][:180], it["rt"], it["like"])
                )
        elif not d["errors"]:
            lines.append("- **@%s** — tidak ada tweet baru" % h)
    if total_new == 0:
        lines += [
            "",
            "_Tidak ada tweet baru selama jendela 20 menit (baseline tercatat pada cek pertama; aktivitas akun ini umumnya rendah — terakhir posting bisa dilihat di watch-log.md)._",
        ]
    lines += ["", "Log lengkap: `gsp-xwatch/watch-log.md`", ""]

    rep = BASE + "/REPORT-%s.md" % now.strftime("%Y%m%d_%H%M")
    with open(rep, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
    print("Tersimpan: " + rep)


if __name__ == "__main__":
    main()
