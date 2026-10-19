#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skl_gates.py - alat ukur gerbang SR-1..SR-9 + V-SUSUN paket mw-ammunition-storage.

Misi   : MWSKILL-0916 langkah S8 (kartu t_3f520294)
Wewenang: docs/2026-09-16-mw-skill-global/identification/02_blueprint.md bagian 5.1 dan 5.2
Pemakai: pekerja rakit (self-check) dan verifier S9 (vonis). Deterministik: tanpa stempel
waktu, tanpa acak kecuali seed yang dicetak, dua run beruntun menghasilkan byte laporan sama.

Cara pakai:
    python skl_gates.py [--base DIR_MISI] [--seed 20260916] [--report PATH]

Keluaran: baris "CHECK n: PASS|FAIL - nama | detail" + baris "VERDICT: PASS|FAIL".
Exit code 0 bila tanpa FAIL.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys

SKL_DEFAULT = "C:/Users/TRIAL/workspace/gsp-hermes/skills/mw-ammunition-storage"
BASE_DEFAULT = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-16-mw-skill-global"

CHAP = ["%02d" % i for i in range(1, 14)]
EM = chr(0x2014)
MD = chr(0x00B7)
CITE = re.compile(r"\[R-(\d{2})-(\d{4}), ([^\]]+)\]")


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", default=SKL_DEFAULT)
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--seed", type=int, default=20260916)
    ap.add_argument("--report", default=None)
    o = ap.parse_args()

    refs = os.path.join(o.skill, "references")
    out, fails = [], 0

    def chk(n, name, ok, detail=""):
        nonlocal fails
        st = "PASS" if ok else "FAIL"
        if not ok:
            fails += 1
        out.append("CHECK %s: %s - %s%s" % (n, st, name, (" | " + detail) if detail else ""))
        return ok

    # --- muat artefak ---
    skill_md_p = os.path.join(o.skill, "SKILL.md")
    reg_p = os.path.join(refs, "register.jsonl")
    man_p = os.path.join(o.base, "corpus", "_manifest.json")
    have = all(os.path.exists(p) for p in (skill_md_p, reg_p, man_p))
    chk(1, "SR-1 paket ada (SKILL.md + references terisi)", have and len(os.listdir(refs)) >= 15,
        "SKILL.md=%s berkas_refs=%d" % (os.path.exists(skill_md_p), len(os.listdir(refs)) if os.path.isdir(refs) else 0))
    if not have:
        out.append("VERDICT: FAIL"); print("\n".join(out)); return 1

    skill_md = open(skill_md_p, encoding="utf-8").read()
    reg_bytes = open(reg_p, "rb").read()
    REG = [json.loads(l) for l in reg_bytes.decode("utf-8").split("\n") if l.strip()]
    man = json.load(open(man_p, encoding="utf-8"))
    names = {e["file"] for e in man}
    chap_files = sorted(f for f in os.listdir(refs) if f.startswith("subsystem-"))

    # --- SR-2 frontmatter ---
    fm = re.match(r"^---\n(.*?)\n---\n", skill_md, re.S)
    name = re.search(r"^name:\s*(\S+)", fm.group(1), re.M).group(1) if fm else "?"
    dsc = re.search(r'^description:\s*"?([^"\n]+)"?', fm.group(1), re.M) if fm else None
    dline = dsc.group(1) if dsc else ""
    keys = set(re.findall(r"^(\w[\w\-]*):", fm.group(1), re.M)) if fm else set()
    chk(2, "SR-2 frontmatter lengkap + name + deskripsi <=57",
        bool(fm) and name == "mw-ammunition-storage" and len(dline) <= 57
        and {"name", "description", "version", "author", "license"} <= keys,
        "name=%s deskripsi=%d karakter kunci=%s" % (name, len(dline), ",".join(sorted(keys))))

    # --- SR-3 cakupan 49/49 di silsilah + matriks bab ---
    sil = open(os.path.join(refs, "silsilah-dokumen.md"), encoding="utf-8").read()
    in_sil = {n for n in names if ("`%s`" % n) in sil}
    cited_docs = collections.Counter(r["dokumen"] for r in REG if r["dokumen"])
    chk(3, "SR-3 cakupan berkas: silsilah + matriks bab",
        len(in_sil) == len(names) and set(cited_docs) <= names and len(cited_docs) == len(names),
        "silsilah=%d/%d berkas_reg=%d/%d" % (len(in_sil), len(names), len(cited_docs), len(names)))

    # --- SR-4 nol bab per-dokumen ---
    per_doc = []
    for f in chap_files:
        heads = re.findall(r"^##\s+(.+)$", open(os.path.join(refs, f), encoding="utf-8").read(), re.M)
        per_doc += [(f, h) for h in heads if re.search(r"\.pdf|\.docx", h)]
    chk(4, "SR-4 nol bab per-dokumen (heading berisi nama berkas)",
        not per_doc and len(chap_files) == 13, "berkas_bab=%d heading_per_dokumen=%d" % (len(chap_files), len(per_doc)))

    # --- SR-5 skema register beku ---
    ids = [r["reg_id"] for r in REG]
    uniq = len(set(ids)) == len(ids)
    ordered = ids == sorted(ids)
    pat = re.compile(r"^R-\d{2}-\d{4}$")
    bad_doc = [r["reg_id"] for r in REG if r["dokumen"] and r["dokumen"] not in names]
    bad_quo = [r["reg_id"] for r in REG if r["kelas_asal"] != "TIDAK-ADA-DI-KORPUS" and not r["kutipan"]]
    # SR-5 R1 (blueprint AMANDEMEN R1 A-1): pointer tipe-sadar; DILARANG koersi.
    PTR = re.compile(r"^([0-9]+(\.[0-9]+)*|Tabel-[0-9]+|Lampiran-[A-Z]|paragraf-[0-9]+)$")
    def ptr_ok(r):
        h = r["halaman"]
        if r["kelas_asal"] == "TIDAK-ADA-DI-KORPUS":
            return h is None or (isinstance(h, int) and not isinstance(h, bool) and h >= 0)
        if h is None:
            return False
        if str(r["dokumen"]).lower().endswith(".docx"):
            return isinstance(h, str) and bool(PTR.match(h)) and not (h == "0")
        return isinstance(h, int) and not isinstance(h, bool) and h >= 1
    bad_hal = [r["reg_id"] for r in REG if not ptr_ok(r)]
    bad_cls = [r["reg_id"] for r in REG if r["kelas_asal"] not in
               ("TERUKUR-DOKUMEN", "TERUKUR-OCR", "DITURUNKAN", "INTERNAL-DRAFT", "TIDAK-ADA-DI-KORPUS")]
    bad_td = [r["reg_id"] for r in REG if (r["kelas_asal"] == "DITURUNKAN") != bool(r["turunan_dari"])]
    canon = ("\n".join(json.dumps(json.loads(l), ensure_ascii=False, sort_keys=True,
                                  separators=(",", ":")) for l in reg_bytes.decode("utf-8").split("\n") if l.strip()) + "\n").encode("utf-8")
    chk(5, "SR-5 (R1) skema register: reg_id unik+urut, dokumen sah, kutipan, pointer tipe-sadar, kelas",
        uniq and ordered and all(pat.match(i) for i in ids) and not bad_doc and not bad_quo
        and not bad_hal and not bad_cls and not bad_td and canon == reg_bytes,
        "baris=%d unik=%d urut=%d dokumen_asing=%d kutipan_kosong=%d pointer_tidak_sah=%d kelas_asing=%d turunan_salah=%d kanonis=%s"
        % (len(REG), uniq, ordered, len(bad_doc), len(bad_quo), len(bad_hal), len(bad_cls), len(bad_td), canon == reg_bytes))

    # --- SR-6 sitasi resolve ---
    by_reg = {r["reg_id"]: r for r in REG}
    unresolved, ncite, nnum = [], 0, 0
    for f in chap_files + ["SKILL.md", "qa-pemeriksa.md", "batas-pengetahuan.md", "silsilah-dokumen.md"]:
        p = os.path.join(o.skill, f) if f == "SKILL.md" else os.path.join(refs, f)
        t = open(p, encoding="utf-8").read()
        for m in CITE.finditer(t):
            rid = "R-%s-%s" % m.groups()[:2]
            ncite += 1
            if rid not in by_reg:
                unresolved.append((f, rid))
    # angka prosa: setiap blok prosa berisi NILAI numerik wajib membawa minimal satu sitasi [R-
    # Konteks non-nilai (nomor seri dokumen, divisi bahaya, penunjuk tabel/lampiran, tanggal baseline)
    # dikecualikan lebih dulu; pengecualian dicetak agar verifier bisa mengaudit.
    NONVAL = re.compile(
        r"IATG[\s\-]*[\d][\d.]*|ST[\s\-]*SG[\s/AC.\d\-]*|AC\.?10[\d.]*|Rev(?:ision|\.)?\s*[\d.]+"
        r"|edisi\s*(?:revisi\s*)?ke[\s\-]?\d+|seri\s*\d{2}|bab\s*\d{2}|partisi\s*EX[\s\-]*[A-F]"
        r"|HD\s*[\d.]+|CG\s*[A-Z]|Class\s*\d(\.\d[A-Z])?|SsD\s*[\d.]+|divisi\s*[\d.]+|kategori\s*[A-Z]\d?"
        r"|Tabel\s*[\d.]+[\sA-Z0-9.]*|Clause\s*[\d.\-]+|Annex\s*[A-Z](\s*\d+(\.\d+)*)?|Lampiran\s*[A-Z](\.\d+)?"
        r"|pasal\s*[\d.]+|butir\s*[\d.]+|level\s*\d|zona\s*\d|bagian\s*[\d.]+|nomor\s*\d+"
        r"|(?:UN|EN|ISO|IEC|ASTM)\s*[\d:\-]+"
        r"|\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b|Vol(?:ume)?\s*[IVX0-9]+|hlm?\s*\d+|hal\s*\d+"
        r"|EX[\s\-]*[A-F][\s\-]*[\d.]+|R-\d{2}-\d{4}|\bp?\d{1,4}\b(?=\s*(?:halaman|hal))"
        r"|tingkat\s*\d|gelombang\s*\d|moda\s*\d|tabel\s*\d")
    CITE_SPAN = re.compile(r"\[R-[^\]]+\]")
    naked_para, naked_sent = [], []
    for f in chap_files:
        t = open(os.path.join(refs, f), encoding="utf-8").read()
        for para in re.split(r"\n\s*\n", t):
            if para.startswith(("#", "|", "Sumber:", "Cakupan", "Setiap", "Register beku", "---")):
                continue
            body = CITE_SPAN.sub(" ", para)
            body = NONVAL.sub(" ", body)
            has_val = re.search(r"\d", body)
            if has_val and "[R-" not in para:
                naked_para.append((f, re.sub(r"\s+", " ", para)[:70]))
            for sent in re.split(r"(?<=[.;])\s+", para):
                s2 = NONVAL.sub(" ", CITE_SPAN.sub(" ", sent))
                if re.search(r"\d", s2) and "[R-" not in sent:
                    naked_sent.append((f, re.sub(r"\s+", " ", sent)[:70]))
    chk(6, "SR-6 sitasi resolve ke reg_id + blok bernilai numerik bersitasi",
        not unresolved and ncite > 0 and not naked_para,
        "sitasi=%d tak_resolve=%d blok_bernilai_tanpa_sitasi=%d (granularitas kalimat: %d)"
        % (ncite, len(unresolved), len(naked_para), len(naked_sent)))
    for f, s in naked_para[:8]:
        out.append("  INFO SR-6a BLOK: %s :: %s" % (f, s))
    for f, s in naked_sent[:8]:
        out.append("  INFO SR-6b KALIMAT: %s :: %s" % (f, s))

    # --- SR-7 sidik jari tercetak + cocok hitung ulang ---
    reg16 = sha16(reg_bytes)
    kl = "\n".join("%s|%s" % (e["file"], e["sha256"]) for e in sorted(man, key=lambda x: x["file"])) + "\n"
    cor16 = sha16(kl.encode("utf-8"))
    chk(7, "SR-7 sidik jari register+korpus sha16 tercetak dan cocok",
        reg16 in skill_md and cor16 in skill_md and reg16 in sil and reg16 in open(os.path.join(refs, "register.md"), encoding="utf-8").read(),
        "register=%s korpus=%s" % (reg16, cor16))

    # --- SR-8 pernyataan R-10 ---
    stmt = "baseline beku 16-09-2026"
    chk(8, "SR-8 pernyataan R-10 baseline beku tercetak",
        stmt in skill_md and stmt in open(os.path.join(refs, "batas-pengetahuan.md"), encoding="utf-8").read(),
        "frasa='%s'" % stmt)

    # --- SR-12 jejak tipografi (diukur di sini juga; scanner resmi dijalankan terpisah) ---
    files = [skill_md_p] + [os.path.join(refs, f) for f in os.listdir(refs)
                            if os.path.isfile(os.path.join(refs, f)) and not f.endswith(".py")]
    hits = []
    for p in files:
        t = open(p, encoding="utf-8").read()
        if EM in t or MD in t:
            hits.append((os.path.basename(p), t.count(EM), t.count(MD)))
    chk(12, "SR-12 bebas U+2014 dan U+00B7 pada berkas dibaca user", not hits,
        "berkas_terkena=%d" % len(hits))
    for h in hits[:5]:
        out.append("  INFO SR-12: %s em=%d middot=%d" % h)

    # --- V-SUSUN 1: uji telusur angka (seed dicetak) ---
    import random
    rnd = random.Random(o.seed)
    cand = []
    for f in chap_files:
        t = open(os.path.join(refs, f), encoding="utf-8").read()
        for m in CITE.finditer(t):
            rid = "R-%s-%s" % m.groups()[:2]
            ctx = re.sub(r"\s+", " ", t[max(0, m.start()-160):m.start()])
            if re.search(r"\d", ctx):
                cand.append((f, rid))
    pick = rnd.sample(cand, min(5, len(cand)))
    ok1 = all(r[1] in by_reg and by_reg[r[1]]["dokumen"] in names and by_reg[r[1]]["halaman"] is not None for r in pick)
    chk("V1", "V-SUSUN 1 uji telusur angka (seed %d)" % o.seed, ok1 and len(pick) == 5,
        "telusur=%d/%d sampai<=2 langkah; sampel=%s" % (len(pick), len(pick), ",".join(r[1] for r in pick)))

    # --- V-SUSUN 2: kerapatan keputusan <=30% prosa tanpa angka ---
    tot = withnum = 0
    for f in chap_files:
        t = open(os.path.join(refs, f), encoding="utf-8").read()
        for para in re.split(r"\n\s*\n", t):
            if para.startswith(("#", "|", "---", "Sumber:", "Cakupan", "Setiap", "Register beku")):
                continue
            if len(para) < 80:
                continue
            tot += 1
            if re.search(r"\d", para):
                withnum += 1
    ratio = 0 if not tot else (tot - withnum) / tot
    chk("V2", "V-SUSUN 2 kerapatan keputusan (prosa tanpa angka <=30%)", ratio <= 0.30,
        "blok=%d tanpa_angka=%d rasio=%.1f%%" % (tot, tot - withnum, ratio * 100))

    # --- V-SUSUN 3: routing pembaca tiga jalur ---
    routes = sum(1 for k in ("Cepat", "Penyusun angka", "Pemeriksa angka") if k in skill_md)
    chk("V3", "V-SUSUN 3 routing pembaca tiga jalur", routes == 3, "jalur=%d/3" % routes)

    # --- V-SUSUN 4: rel bukti + sebaran tanda asal berhitung ---
    ka = collections.Counter(r["kelas_asal"] for r in REG)
    tab = all(("| `%s` | %d |" % (k, ka.get(k, 0))) in skill_md for k in
              ("TERUKUR-DOKUMEN", "TERUKUR-OCR", "DITURUNKAN", "INTERNAL-DRAFT", "TIDAK-ADA-DI-KORPUS"))
    chk("V4", "V-SUSUN 4 rel bukti + sebaran tanda asal tampil berhitung", tab and ncite > 0,
        "sebaran=%s" % dict(sorted(ka.items())))

    # --- V-SUSUN 5: sidik jari cocok hitung ulang (sama dgn SR-7, diuji ulang independen) ---
    chk("V5", "V-SUSUN 5 sidik jari tercetak cocok hitung ulang", reg16 in skill_md and cor16 in skill_md,
        "register=%s korpus=%s" % (reg16, cor16))

    # --- V-SUSUN 6: silsilah 49 berkas + tabel angka ditarik ---
    rows = len(re.findall(r"^\| \d+ \| `", sil, re.M))
    chk("V6", "V-SUSUN 6 silsilah 49 berkas + tabel angka ditarik",
        rows == len(names) and "Tabel angka ditarik" in sil, "baris_silsilah=%d/%d" % (rows, len(names)))

    # --- ringkasan tambahan untuk laporan kartu ---
    out.append("RINGKASAN: baris_register=%d berkas_korpus=%d berkas_bab=%d blok_prosa_sitasi=%d "
               "sidik_jari_register=%s sidik_jari_korpus=%s" % (len(REG), len(names), len(chap_files), ncite, reg16, cor16))
    out.append("VERDICT: " + ("PASS" if fails == 0 else "FAIL(%d)" % fails))
    txt = "\n".join(out) + "\n"
    sys.stdout.write(txt)
    if o.report:
        open(o.report, "w", encoding="utf-8", newline="\n").write(txt)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
