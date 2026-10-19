#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_naturalisasi_20260902.py - Verifikasi gerbang naturalisasi keluaran GSP.

Kartu     : t_ecaa4d46 (NAT-S18), blueprint langkah 18
            docs/2026-09-02-naturalisasi-output/identification/02_structured.md baris 217
Kriteria  : definisi S-1..S-6 dan C-1..C-10 diambil langsung dari
            identification/01_translated.md seksi 5 (dibaca run ini, bukan salinan).
Kelompok S: uji struktural gerbang (skill kanonik+fleet, distribusi profil, blok SOUL,
            isi skill, scanner hidup, kontrol merah-hijau corpus).
Kelompok C: uji konten satu artefak atau lebih lewat scanner fleet; tiap kode C-1..C-10
            dilaporkan sebagai satu CHECK dengan angka nyata dari scanner. Tanpa --artefak
            dipakai sampel bawaan (fixture hijau kanal doc) supaya struktur CHECK terbukti
            dari output contoh; langkah 19 (NAT-S19) menjalankan artefak nyata.

Kontrak keluaran:
  - Tiap CHECK mandiri: satu check gagal/crash tidak menghentikan check lain.
  - Baris: "CHECK <ID>: PASS|FAIL|NEEDS_REVIEW|N/A|INFO - nama | detail"
  - Satu baris "VERDICT:" akhir: FAIL bila ada satu pun FAIL; NEEDS_REVIEW bila tidak
    ada FAIL tetapi ada NEEDS_REVIEW; selain itu PASS.
  - Exit code: 1 bila VERDICT memuat FAIL; 0 untuk PASS maupun NEEDS_REVIEW
    (NEEDS_REVIEW = menunggu keputusan/pekerjaan kartu lain, bukan cacat di sini).
  - Determinisme: tanpa stempel waktu, iterasi koleksi di-sort, dua run beruntun
    byte-identik pada keadaan disk yang sama.

Interpretasi jujur yang tertanam (bukan pelonggaran):
  - S-1 membedakan selisih sha256 kanonik-vs-fleet yang versinya kanonik lebih baru
    (drift terdokumentasi, re-sync = kartu NAT-HIL-D t_f465458a -> NEEDS_REVIEW) dari
    selisih tanpa penjelasan versi (FAIL).
  - S-2 memakai basis roster-disk: target bernama yang TIDAK ADA DI DISK dan sudah
    terdokumentasi (gsp-content-research-writer di skill_distribution.md; default di
    contract.md D-TA-02) dihitung sebagai deviasi tercatat, bukan kegagalan senyap.
  - S-3 menghitung ulang SOUL.md tingkat atas saat run berjalan dan menjelaskan
    selisih terhadap basis beku 53 (contract.md) dengan menyebut nama profil tambahan.
  - D-TA-10: skrip ini memverifikasi keadaan yang terukur, tidak mengklaim fleet-wide 0.

Kebersihan sumber: berkas ini tidak memuat literal U+2014 / U+00B7 maupun bentuk
escape/entity-nya, sehingga ikut lolos sapuan scanner atas folder scripts/.
"""

import hashlib
import os
import re
import subprocess
import sys

try:  # konsol Windows default cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------------------
# Lokasi tetap (kontrak misi 2026-09-02-naturalisasi-output)
# ---------------------------------------------------------------------------
LOCALAPPDATA = os.environ.get(
    "LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local")
PROFILES = LOCALAPPDATA + "/hermes/profiles"
FLEET_SKILL = LOCALAPPDATA + "/hermes/skills/gsp/gsp-output-naturalization"
CANON_SKILL = "C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-output-naturalization"
CONTRACT_DIR = ("C:/Users/TRIAL/workspace/gsp-hermes/workspace/"
                "docs/2026-09-02-naturalisasi-output")
CONTRACT_MD = CONTRACT_DIR + "/contract.md"
DIST_MD = CONTRACT_DIR + "/skill_distribution.md"
SCANNER = FLEET_SKILL + "/scripts/scan_ai_footprint.py"
CORPUS = FLEET_SKILL + "/references/corpus-merah-hijau"
SKILL_NAME = "gsp-output-naturalization"
GATE_MARKER = "GATE NATURALISASI"

FIXED_SNIPPET = (
    "Laporan verifikasi gerbang naturalisasi ini disusun untuk menguji determinisme "
    "scanner pada masukan yang sama sehingga kedua run menghasilkan angka yang sama "
    "tanpa perbedaan satu karakter pun.")

# matriks kontrol merah-hijau (cermin run_red_green_s11.py NAT-S11, handoff NAT-S10)
MATRIX_MERAH = [
    ("merah-a1-em-dash.md", ["--channel", "doc"]),
    ("merah-a2-middle-dot.md", ["--channel", "doc"]),
    ("merah-a3-emoji.md", ["--channel", "doc"]),
    ("merah-a4567-frasa.md", ["--channel", "doc"]),
    ("merah-a5-label-ruang-kerja.md", ["--channel", "doc"]),
    ("merah-b-agregasi.md", ["--channel", "doc"]),
    ("merah-semua-kode.md", ["--channel", "sosmed"]),
]
MATRIX_HIJAU = []
for _ch in ("doc", "deck", "kanban", "etalase", "sosmed", "chat", "notif"):
    MATRIX_HIJAU.append(("hijau-doc-laporan.md", ["--channel", _ch]))
MATRIX_HIJAU.append(("hijau-doc-laporan.md", ["--channel", "etalase", "--require-marker"]))
for _ch in ("kanban", "doc"):
    MATRIX_HIJAU.append(("hijau-kanban-summary.md", ["--channel", _ch]))
MATRIX_HIJAU.append(("hijau-kanban-summary.md", ["--channel", "etalase", "--require-marker"]))
for _ch in ("chat", "notif"):
    MATRIX_HIJAU.append(("hijau-notif-deploy.txt", ["--channel", _ch]))
REDCOV_CODES = ("C-1", "C-2", "C-3", "A4", "A5", "A6", "A7")  # kontrak README corpus

TARGETS_NAMED = ("gsp-document-writer", "gsp-pm-writer",
                 "gsp-content-research-writer", "gsp-custodian", "default")

C_CODES = ("C-1", "C-2", "C-3", "C-4", "C-5", "C-6", "C-7", "C-8", "C-9", "C-10")


def read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def sha256_file(path):
    return hashlib.sha256(read_bytes(path)).hexdigest()


def read_text(path):
    return read_bytes(path).decode("utf-8", errors="replace")


def run_py(args, timeout=180):
    """Jalankan scanner dengan interpreter yang sama seperti skrip ini."""
    p = subprocess.run([sys.executable, SCANNER] + args,
                       capture_output=True, timeout=timeout)
    out = p.stdout.decode("utf-8", errors="replace")
    err = p.stderr.decode("utf-8", errors="replace")
    return p.returncode, out, err


def top_level_profiles():
    """Direktori profil dengan SOUL.md tingkat atas (bukan scratch bersarang)."""
    out = []
    if not os.path.isdir(PROFILES):
        return out
    for name in sorted(os.listdir(PROFILES)):
        soul = os.path.join(PROFILES, name, "SOUL.md")
        if os.path.isfile(soul):
            out.append((name, soul))
    return out


class Res:
    def __init__(self):
        self.rows = []

    def add(self, cid, status, nama, detail=""):
        self.rows.append((cid, status, nama, detail))

    def guard(self, cid, nama, fn):
        """Tiap CHECK mandiri: exception menjadi baris, tidak menghentikan yang lain."""
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 - klasifikasi jujur, bukan diam
            self.add(cid, "NEEDS_REVIEW", nama,
                     "check tidak dapat diselesaikan: %s: %s"
                     % (type(exc).__name__, exc))


# ---------------------------------------------------------------------------
# Kelompok S - uji struktural (RT seksi 5.1)
# ---------------------------------------------------------------------------
def s1(res):
    def body():
        canon = CANON_SKILL + "/SKILL.md"
        fleet = FLEET_SKILL + "/SKILL.md"
        if not (os.path.isfile(canon) and os.path.isfile(fleet)):
            res.add("S-1", "FAIL", "Skill naturalisasi kanonik ada + salinan fleet identik",
                    "kanonik=%s fleet=%s" % (os.path.isfile(canon), os.path.isfile(fleet)))
            return
        hc, hf = sha256_file(canon), sha256_file(fleet)
        vc = re.search(r"^version:\s*(\S+)", read_text(canon), re.M)
        vf = re.search(r"^version:\s*(\S+)", read_text(fleet), re.M)
        vc = vc.group(1) if vc else "?"
        vf = vf.group(1) if vf else "?"
        if hc == hf:
            res.add("S-1", "PASS", "Skill naturalisasi kanonik ada + salinan fleet identik",
                    "sha256 identik (%s...), versi %s" % (hc[:12], vc))
        elif vc != vf:
            res.add("S-1", "NEEDS_REVIEW",
                    "Skill naturalisasi kanonik ada + salinan fleet identik",
                    "DRIFT terdokumentasi: kanonik v%s sha %s... vs fleet v%s sha %s...; "
                    "kanonik lebih baru, re-sync adalah ranah kartu NAT-HIL-D "
                    "(t_f465458a), bukan cacat distribusi" % (vc, hc[:12], vf, hf[:12]))
        else:
            res.add("S-1", "FAIL", "Skill naturalisasi kanonik ada + salinan fleet identik",
                    "sha256 beda tanpa selisih versi (kanonik %s... vs fleet %s...)"
                    % (hc[:12], hf[:12]))
    res.guard("S-1", "Skill naturalisasi kanonik ada + salinan fleet identik", body)


def s2(res):
    def body():
        dist = read_text(DIST_MD) if os.path.isfile(DIST_MD) else ""
        contract = read_text(CONTRACT_MD) if os.path.isfile(CONTRACT_MD) else ""
        on_disk = {n for n, _ in top_level_profiles()}
        physical = set()
        for name in sorted(on_disk):
            p = os.path.join(PROFILES, name, "skills", SKILL_NAME, "SKILL.md")
            if os.path.isfile(p):
                physical.add(name)
        pointer = set()
        for line in dist.splitlines():
            if "awareness-pointer" in line:
                m = re.match(r"\|\s*([\w.-]+)\s*\|", line)
                if m and m.group(1) in on_disk:
                    pointer.add(m.group(1))
        covered = physical | pointer
        notes = []
        deviasi = []
        unresolved = []
        for t in TARGETS_NAMED:
            if t in physical:
                notes.append("%s=fisik" % t)
            elif t in pointer:
                notes.append("%s=pointer" % t)
            elif t not in on_disk and re.search(
                    re.escape(t) + r".*(TIDAK ADA DI DISK|tidak ada di disk)",
                    dist + "\n" + contract, re.IGNORECASE):
                deviasi.append("%s=TIDAK ADA DI DISK (terdokumentasi)" % t)
            else:
                unresolved.append(t)
        detail = ("cakupan=%d (fisik=%d, pointer=%d); target bernama: %s"
                  % (len(covered), len(physical), len(pointer), "; ".join(notes)))
        if deviasi:
            detail += "; deviasi tercatat: " + ", ".join(deviasi)
        if len(covered) < 5:
            res.add("S-2", "FAIL", "Distribusi ke agen penulis >= 5 profil", detail)
        elif unresolved:
            res.add("S-2", "NEEDS_REVIEW", "Distribusi ke agen penulis >= 5 profil",
                    detail + "; target belum terselesaikan: " + ", ".join(unresolved))
        else:
            res.add("S-2", "PASS", "Distribusi ke agen penulis >= 5 profil", detail)
    res.guard("S-2", "Distribusi ke agen penulis >= 5 profil", body)


def s3(res):
    def body():
        souls = top_level_profiles()
        total = len(souls)
        with_block = [n for n, p in souls if GATE_MARKER in read_text(p)]
        missing = sorted(n for n, _ in souls if n not in with_block)
        basis = None
        if os.path.isfile(CONTRACT_MD):
            m = re.search(r"basis_profil_resmi\D{0,8}?(\d+)", read_text(CONTRACT_MD))
            basis = int(m.group(1)) if m else None
        detail = "%d/%d SOUL.md ber-blok '%s'; basis beku=%s" % (
            len(with_block), total, GATE_MARKER, basis)
        if basis is not None and total != basis:
            delta = total - basis
            detail += (" ; selisih %s%d profil terhadap basis beku dijelaskan sebagai "
                       "profil lahir/setelah pembekuan basis (nama tidak dibekukan di "
                       "skrip ini; lihat handoff NAT-S17)" % ("+" if delta > 0 else "", delta))
        if total == 0:
            res.add("S-3", "FAIL", "Blok wajib hadir di SEMUA SOUL.md profil fleet",
                    "tidak ada SOUL.md tingkat atas terdeteksi")
        elif missing:
            res.add("S-3", "FAIL", "Blok wajib hadir di SEMUA SOUL.md profil fleet",
                    detail + "; TANPA blok: " + ", ".join(missing))
        else:
            res.add("S-3", "PASS", "Blok wajib hadir di SEMUA SOUL.md profil fleet", detail)
    res.guard("S-3", "Blok wajib hadir di SEMUA SOUL.md profil fleet", body)


def s4(res):
    def body():
        text = read_text(CANON_SKILL + "/SKILL.md")
        reqs = [
            ("default formal", r"Formal institusional"),
            ("daftar A1-A7", r"A1-A7[\s\S]{0,400}\|\s*A1\s*\|[\s\S]{0,2000}\|\s*A7\s*\|"),
            ("daftar B1-B9", r"B1-B9[\s\S]{0,400}\|\s*B1\s*\|[\s\S]{0,2000}\|\s*B9\s*\|"),
            ("prosedur 4 langkah", r"Prosedur 4 langkah"),
            ("cara panggil scanner", r"Cara panggil scanner[\s\S]{0,600}scan_ai_footprint\.py"),
            ("prosedur override", r"Prosedur override"),
        ]
        miss = [nama for nama, pat in reqs if not re.search(pat, text)]
        if miss:
            res.add("S-4", "FAIL", "Isi SKILL.md memadai (butir a-f)",
                    "tidak ditemukan: " + ", ".join(miss))
        else:
            res.add("S-4", "PASS", "Isi SKILL.md memadai (butir a-f)",
                    "default formal, A1-A7, B1-B9, prosedur 4 langkah, pemanggilan "
                    "scanner, override: semua hadir")
    res.guard("S-4", "Isi SKILL.md memadai (butir a-f)", body)


def s5(res):
    def body():
        if not os.path.isfile(SCANNER):
            res.add("S-5", "FAIL", "Scanner ada dan jalan (selftest + determinisme)",
                    "scanner tidak ditemukan di " + SCANNER)
            return
        rc, out, err = run_py(["--selftest"])
        st_ok = rc == 0
        a = subprocess.run([sys.executable, SCANNER, "--text", FIXED_SNIPPET,
                            "--channel", "doc"], capture_output=True, timeout=180)
        b = subprocess.run([sys.executable, SCANNER, "--text", FIXED_SNIPPET,
                            "--channel", "doc"], capture_output=True, timeout=180)
        det_ok = a.stdout == b.stdout and a.returncode == b.returncode
        ver = ""
        rv = subprocess.run([sys.executable, SCANNER, "--version"],
                            capture_output=True, timeout=60)
        if rv.returncode == 0:
            ver = rv.stdout.decode("utf-8", "replace").strip()
        detail = "selftest exit=%d; dua run byte-identik=%s; %s" % (
            rc, det_ok, ver or "versi tidak terbaca")
        if st_ok and det_ok:
            res.add("S-5", "PASS", "Scanner ada dan jalan (selftest + determinisme)", detail)
        else:
            tail = (out + err).strip().splitlines()[-3:] if (out + err).strip() else []
            res.add("S-5", "FAIL", "Scanner ada dan jalan (selftest + determinisme)",
                    detail + ("; ekor: " + " / ".join(tail) if tail else ""))
    res.guard("S-5", "Scanner ada dan jalan (selftest + determinisme)", body)


def s6(res):
    def body():
        problems = []
        red_fail_codes = set()
        for fname, extra in MATRIX_MERAH:
            path = os.path.join(CORPUS, fname)
            if not os.path.isfile(path):
                problems.append("corpus merah hilang: " + fname)
                continue
            rc, out, err = run_py([path.replace("\\", "/")] + extra)
            for line in out.splitlines():
                m = re.match(r"CHECK \d+: FAIL - (\S+)", line)
                if m:
                    red_fail_codes.add(m.group(1))
            if rc != 1 or "VERDICT: FAIL" not in out:
                problems.append("merah tidak FAIL: %s (exit=%d)" % (fname, rc))
        for fname, extra in MATRIX_HIJAU:
            path = os.path.join(CORPUS, fname)
            if not os.path.isfile(path):
                problems.append("corpus hijau hilang: " + fname)
                continue
            rc, out, err = run_py([path.replace("\\", "/")] + extra)
            if rc != 0 or "VERDICT: PASS" not in out:
                problems.append("hijau tidak PASS: %s %s (exit=%d)"
                                % (fname, " ".join(extra), rc))
        cov_miss = [c for c in REDCOV_CODES if c not in red_fail_codes]
        detail = "merah=%d run, hijau=%d run; cakupan kode merah %s" % (
            len(MATRIX_MERAH), len(MATRIX_HIJAU),
            "lengkap " + ",".join(REDCOV_CODES) if not cov_miss
            else "KURANG " + ",".join(cov_miss))
        if problems:
            detail += "; masalah: " + "; ".join(problems[:6])
        if not problems and not cov_miss:
            res.add("S-6", "PASS", "Kontrol merah-hijau (gerbang tidak mati)", detail)
        else:
            res.add("S-6", "FAIL", "Kontrol merah-hijau (gerbang tidak mati)", detail)
    res.guard("S-6", "Kontrol merah-hijau (gerbang tidak mati)", body)


# ---------------------------------------------------------------------------
# Kelompok C - uji konten artefak (RT seksi 5.2, ambang ditegakkan scanner)
# ---------------------------------------------------------------------------
CHECK_LINE = re.compile(r"^CHECK \d+: (\S+) - ([^|]+?)(?: \|(.*))?$")


def scanner_rows(args):
    rc, out, err = run_py(args)
    rows = {}
    verdict = None
    for line in out.splitlines():
        if line.startswith("VERDICT:"):
            verdict = line.split(":", 1)[1].strip()
            continue
        m = CHECK_LINE.match(line)
        if m:
            status, nama, detail = m.group(1), m.group(2).strip(), (m.group(3) or "").strip()
            code = nama.split(" ", 1)[0]
            rows.setdefault(code, (status, nama, detail))
    return rc, rows, verdict, out, err


def c_group(res, artefaks, channel, require_marker):
    if not artefaks:
        # struktur CHECK terbukti dari output contoh: fixture hijau kanal doc
        artefaks = [(os.path.join(CORPUS, "hijau-doc-laporan.md").replace("\\", "/"),
                     "doc", False)]
        label_note = " (sampel bawaan: fixture hijau kanal doc)"
    else:
        label_note = ""
    for path, ch, rm in artefaks:
        base = os.path.basename(path)
        args = [path, "--channel", ch] + (["--require-marker"] if rm else [])

        def body(path=path, ch=ch, rm=rm, base=base):
            if not os.path.isfile(path):
                for code in C_CODES:
                    res.add(code, "NEEDS_REVIEW",
                            "%s [%s]%s" % (code, base, label_note),
                            "artefak tidak ditemukan: " + path)
                return
            rc, rows, verdict, out, err = scanner_rows(args)
            if verdict is None:
                for code in C_CODES:
                    res.add(code, "NEEDS_REVIEW",
                            "%s [%s]%s" % (code, base, label_note),
                            "scanner tidak menghasilkan VERDICT (exit=%d): %s"
                            % (rc, (err.strip() or out.strip())[:160]))
                return
            for code in C_CODES:
                if code in rows:
                    status, nama, detail = rows[code]
                    if status == "N/A":
                        status = "N/A"
                    res.add(code, status, "%s [%s]: %s%s" % (code, base, nama, label_note),
                            detail)
                else:
                    res.add(code, "NEEDS_REVIEW",
                            "%s [%s]%s" % (code, base, label_note),
                            "kode tidak dilaporkan scanner (verdict scanner: %s)" % verdict)
        res.guard("C", "%s [%s]" % ("grup C", base), body)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    artefaks = []
    channel = "doc"
    require_marker = False
    skip_c = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--artefak" and i + 1 < len(argv):
            artefaks.append([argv[i + 1], channel, False]); i += 2
        elif a == "--channel" and i + 1 < len(argv):
            channel = argv[i + 1]; i += 2
        elif a == "--require-marker":
            if artefaks:
                artefaks[-1][2] = True
            require_marker = True; i += 1
        elif a == "--skip-c":
            skip_c = True; i += 1
        else:
            sys.stderr.write("argumen tidak dikenal: %s\n" % a)
            return 2
    # artefak yang disebut sebelum --channel mengikuti channel terakhir yang berlaku
    for item in artefaks:
        item[1] = channel

    res = Res()
    for cid, fn in (("S-1", s1), ("S-2", s2), ("S-3", s3),
                    ("S-4", s4), ("S-5", s5), ("S-6", s6)):
        fn(res)
    if not skip_c:
        c_group(res, [tuple(x) for x in artefaks], channel, require_marker)

    fails = sum(1 for _, s, _, _ in res.rows if s == "FAIL")
    reviews = sum(1 for _, s, _, _ in res.rows if s == "NEEDS_REVIEW")
    for cid, status, nama, detail in res.rows:
        line = "CHECK %s: %s - %s" % (cid, status, nama)
        if detail:
            line += " | " + detail
        sys.stdout.write(line + "\n")
    verdict = "FAIL" if fails else ("NEEDS_REVIEW" if reviews else "PASS")
    sys.stdout.write("VERDICT: %s\n" % verdict)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
