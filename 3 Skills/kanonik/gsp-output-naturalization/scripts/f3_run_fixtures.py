"""GAYA-AHLI-1005 S15 - runner fixture merah-hijau scanner jejak AI.

Menjalankan scan_ai_footprint.py SATU kali per fixture pada kanal yang diminta,
lalu memvonis ekspektasi dari f3_manifest.json:
  * "want"            : status baris check harus persis ini
  * "want_not"        : status baris check TIDAK boleh ini
  * "detail"          : regex yang wajib cocok pada kolom detail
  * "mode": "any"     : cukup satu baris yang cocok memenuhinya (scanner mencetak
                        baris utama + baris 'DIKECUALIKAN blok' untuk kunci sama)
  * check "exit"      : kode keluar scanner yang diharapkan
  * known_defect      : deviasi dilaporkan NEEDS_REVIEW (bukan FAIL) dengan bukti
                        - dipakai untuk temuan yang butuh putusan controller
Vonis deviasi = FAIL; keluaran selalu daftar CHECK + RINGKAS + satu baris VERDICT
dan exit non-zero bila ada deviasi. Deterministik: tanpa waktu, tanpa rawak,
fixture diurut leksikografis sehingga dua run byte-identik.

Pakai:
  python f3_run_fixtures.py --fixtures <dir> [--scanner <path>]
  python f3_run_fixtures.py --fixtures <dir> --expect-lapis merah --scanner <v1.8.1>

Lapis 'merah' menjalankan fixture yang SAMA pada scanner LAMA untuk membuktikan
fixture memang menangkap cacat yang belum ditambal saat itu; fixture di
SKIP_MERAH dilewati karena gerbangnya belum ada pada scanner lama.
"""
import argparse, json, os, re, subprocess, sys

# Fixture di luar skop bukti-merah: pasangan stres M-09 menguji gerbang aktivasi
# >2.000 kalimat yang tidak ada pada scanner lama, jadi vonis di sana tidak
# bermakna sebagai bukti merah.
SKIP_MERAH = {"f3-m09-lowopener-red.md", "f3-m09-diverse-green.md"}


def load_expectations(fixdir):
    mp = os.path.join(fixdir, "f3_manifest.json")
    if not os.path.exists(mp):
        raise SystemExit("manifest hilang: " + mp)
    with open(mp, encoding="utf-8") as fh:
        return json.load(fh)["fixtures"]


def parse_scan(stdout):
    rows = []
    for ln in stdout.splitlines():
        if not ln.startswith("CHECK ") or ": " not in ln or " - " not in ln:
            continue
        body = ln.split(": ", 1)[1]
        status, rest = body.split(" - ", 1)
        name = rest.split(" | ")[0]
        detail = rest.split(" | ", 1)[1] if " | " in rest else ""
        rows.append((status.strip(), name, detail))
    return rows


_CODE_RE = re.compile(r"^(?:[ABC]-?\d+[a-z]?|D-TA-\d+)$")


def match(rows, key):
    """Key berbentuk kode check ('A4','C-26','C-8b','D-TA-09') -> HANYA cocok pada
    kode persis, supaya 'C-1' tidak ikut memvonis baris 'C-13'/'C-14'. Key bebas
    ('perluasan C-13', 'rasio pembuka', 'DIKECUALIKAN blok') -> anak-kunci nama."""
    exact = bool(_CODE_RE.match(key))
    return [(st, nm, dt) for st, nm, dt in rows
            if ((nm.split(" ", 1)[0] == key) if exact else (key in nm))]


def judge(scanner, fixdir, entry, lapis="hijau"):
    path = os.path.join(fixdir, entry["file"])
    out = []
    if lapis == "merah" and entry["file"] in SKIP_MERAH:
        return [("SKIP", entry["file"], "luar skop bukti-merah: gerbang >2.000 kalimat "
                "belum ada pada scanner lama")]
    if not os.path.exists(path):
        return [("FAIL", entry["file"], "berkas fixture hilang: " + path)]
    p = subprocess.run([sys.executable, scanner, path, "--channel", entry["channel"]],
                       capture_output=True, text=True, encoding="utf-8")
    rows = parse_scan(p.stdout)
    defect = entry.get("known_defect")
    for exp in entry["checks"]:
        key = exp.get("check") or ("exit" if "exit" in exp else None)
        if key is None:
            out.append(("FAIL", entry["file"], "ekspektasi tanpa kunci check/exit: %r" % exp))
            continue
        label = "%s [%s]" % (entry["file"], key)
        if key == "exit":
            want = exp.get("want", exp.get("exit"))
            ok = p.returncode == want
            st = "PASS" if ok else ("NEEDS_REVIEW" if defect else "FAIL")
            out.append((st, "%s exit" % entry["file"],
                        "" if ok else "exit aktual %d, harapan %d" % (p.returncode, want)))
            continue
        hits = match(rows, key)
        if not hits:
            # 'want_not' saja = memang mengharapkan baris TIDAK ADA (dua arah).
            if exp.get("want_not") and "want" not in exp and "detail" not in exp:
                out.append(("PASS", label, ""))
            else:
                out.append(("NEEDS_REVIEW" if defect else "FAIL", label,
                            "baris check tidak muncul pada keluaran scanner"))
            continue
        # mode "all" (default): SETIAP baris yang cocok kunci harus memenuhi;
        # mode "any": cukup satu (dipakai utk kunci yang mencetak baris utama +
        # baris 'DIKECUALIKAN blok' sekaligus, mis. A4 pada berkas berpenanda).
        any_mode = exp.get("mode") == "any"
        probs, first_bad = None, None
        for status, name, detail in hits:
            bad = []
            if "want" in exp and status != exp["want"]:
                bad.append("status %s != %s" % (status, exp["want"]))
            if "want_not" in exp and status == exp["want_not"]:
                bad.append("status terlarang %s" % status)
            if "detail" in exp and not re.search(exp["detail"], detail):
                bad.append("detail tidak cocok /%s/" % exp["detail"])
            if not bad:
                if any_mode:
                    probs = []
                    break
                continue
            if first_bad is None:
                first_bad = bad
            if any_mode:
                continue
            probs = bad
            break
        if probs is None:
            # any_mode dan TIDAK ADA satu pun baris yang memenuhi -> tetap FAIL.
            probs = (first_bad or ["tidak ada baris yang memenuhi"]) if any_mode \
                else (first_bad or [])
        if probs:
            st = "NEEDS_REVIEW" if defect else "FAIL"
            ev = "; ".join(probs)
            if defect:
                ev += " || DEFECT: " + defect
            out.append((st, label, ev[:600]))
        else:
            out.append(("PASS", label, ""))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--scanner", default=None, help="jalur scan_ai_footprint.py")
    ap.add_argument("--expect-lapis", default="hijau", choices=("hijau", "merah"),
                    help="hijau = vonis penuh ekspektasi; merah = lapiskan pada scanner "
                         "lama untuk membuktikan fixture menangkap cacat pra-tambal")
    a = ap.parse_args(argv)
    scanner = a.scanner or os.environ.get("F3_SCANNER")
    if not scanner or not os.path.exists(scanner):
        print("CHECK 1: FAIL - jalur scanner tidak valid | %s" % scanner)
        print("VERDICT: FAIL")
        return 1
    entries = sorted(load_expectations(a.fixtures), key=lambda e: e["file"])
    results = []
    for e in entries:
        results.extend(judge(scanner, a.fixtures, e, a.expect_lapis))
    fails = sum(1 for s, _, _ in results if s == "FAIL")
    needs = sum(1 for s, _, _ in results if s == "NEEDS_REVIEW")
    skips = sum(1 for s, _, _ in results if s == "SKIP")
    lines = []
    for i, (status, label, bukti) in enumerate(results, 1):
        line = "CHECK %d: %s - %s" % (i, status, label)
        if bukti:
            line += " | %s" % bukti
        lines.append(line)
    lines.append("RINGKAS: %d check, %d FAIL, %d NEEDS_REVIEW, %d SKIP (lapis=%s)" %
                 (len(results), fails, needs, skips, a.expect_lapis))
    verdict = "FAIL" if fails else ("NEEDS_REVIEW" if needs else "PASS")
    lines.append("VERDICT: %s" % verdict)
    sys.stdout.write("\n".join(lines) + "\n")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
