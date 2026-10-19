# -*- coding: utf-8 -*-
"""
PERIKSA EKAS — pemeriksa keutuhan sistem.

Menemukan pembusukan diam-diam: baris register menunjuk berkas yang tidak ada,
kartu tanpa berkas vault, manifest laci yang ketinggalan, kutipan halaman melebihi
jumlah halaman berkasnya, jalur yang tidak dapat diselesaikan, dan salinan ganda.

TIDAK mengubah apa pun. Hanya melaporkan.

Jalankan:  python periksa_ekas.py
Opsi   :   --halaman   periksa kutipan "PDF n" terhadap jumlah halaman sebenarnya (lambat)
           --diam      hanya tampilkan GALAT
Keluar dengan kode 1 bila ada GALAT — dapat dipakai sebagai gerbang otomatis.
"""
import io, os, re, sys, csv, glob, hashlib, collections

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

EKAS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAK = os.path.dirname(EKAS)
SKILLS = r"C:\Users\gspen\.claude\skills"
VAULT = os.path.join(EKAS, "03_SOURCE-VAULT")
HALAMAN = "--halaman" in sys.argv
DIAM = "--diam" in sys.argv

temuan = []          # (tingkat, kelompok, pesan)


def lapor(tingkat, kelompok, pesan):
    temuan.append((tingkat, kelompok, pesan))


def isi(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


def hashfile(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ── 1. Register induk ────────────────────────────────────────────────
def periksa_register():
    p = os.path.join(EKAS, "02_REGISTERS", "MASTER-REFERENCE-REGISTER.csv")
    if not os.path.exists(p):
        lapor("GALAT", "register", "MASTER-REFERENCE-REGISTER.csv tidak ada")
        return []
    rows = list(csv.DictReader(io.open(p, encoding="utf-8")))
    ids = collections.Counter(r["reference_id"] for r in rows)
    for rid, n in ids.items():
        if n > 1:
            lapor("GALAT", "register", "reference_id ganda: %s (%d kali)" % (rid, n))
    for r in rows:
        vp = os.path.join(EKAS, r["vault_path"].replace("/", os.sep))
        if not os.path.isdir(vp):
            lapor("GALAT", "register", "%s: laci tidak ada -> %s" % (r["reference_id"], r["vault_path"]))
        elif not [b for b in os.listdir(vp) if b.lower().endswith(".pdf")]:
            lapor("PERINGATAN", "register", "%s: laci kosong -> %s" % (r["reference_id"], r["vault_path"]))
        rp = r.get("resume_path", "")
        if rp:
            if not os.path.exists(os.path.join(EKAS, rp.replace("/", os.sep))):
                lapor("GALAT", "register", "%s: resume tidak ada -> %s" % (r["reference_id"], rp))
        elif r["authority_status"] != "INTAKE_ONLY":
            lapor("GALAT", "register",
                  "%s berstatus %s tetapi TANPA resume" % (r["reference_id"], r["authority_status"]))
        if r["authority_status"] == "INTAKE_ONLY" and r["may_set_acceptance"] not in ("no", "no-unless-contract-adopts"):
            lapor("GALAT", "register",
                  "%s: INTAKE_ONLY tetapi may_set_acceptance=%s" % (r["reference_id"], r["may_set_acceptance"]))
    return rows


# ── 2. Kartu pengetahuan ↔ register ──────────────────────────────────
def periksa_kartu(rows):
    kartu = {os.path.basename(p)[:-3]: p for p in glob.glob(os.path.join(EKAS, "04_KNOWLEDGE-CARDS", "*", "*.md"))}
    reg = {r["reference_id"]: r for r in rows}
    for rid, p in kartu.items():
        if rid not in reg:
            lapor("GALAT", "kartu", "kartu %s tidak ada di register" % rid)
    for rid, r in reg.items():
        if rid not in kartu:
            t = "PERINGATAN" if r["authority_status"] == "INTAKE_ONLY" else "GALAT"
            lapor(t, "kartu", "%s tanpa kartu pengetahuan (%s)" % (rid, r["authority_status"]))
    # domain kartu harus sama dengan register
    for rid, p in kartu.items():
        if rid in reg:
            dom_kartu = os.path.basename(os.path.dirname(p))
            if dom_kartu != reg[rid]["domain"]:
                lapor("GALAT", "kartu", "%s: domain kartu '%s' != register '%s'"
                      % (rid, dom_kartu, reg[rid]["domain"]))


# ── 3. Manifest laci ↔ isi sebenarnya ────────────────────────────────
def periksa_laci():
    for akar, dirs, berkas in os.walk(VAULT):
        if "_ISI.md" not in berkas:
            if [b for b in berkas if b.lower().endswith(".pdf")]:
                lapor("GALAT", "laci", "laci tanpa _ISI.md: %s" % os.path.relpath(akar, EKAS))
            continue
        nyata = sorted(b for b in berkas if b.lower().endswith(".pdf"))
        teks = isi(os.path.join(akar, "_ISI.md"))
        tercatat = set(re.findall(r"^\| `([^`]+\.pdf)`", teks, re.M | re.I))
        rel = os.path.relpath(akar, EKAS)
        for b in nyata:
            if b not in tercatat:
                lapor("GALAT", "laci", "%s: `%s` ada tetapi tidak tercatat di _ISI.md" % (rel, b[:52]))
        for b in tercatat - set(nyata):
            lapor("GALAT", "laci", "%s: _ISI.md mencatat `%s` yang tidak ada" % (rel, b[:52]))
        m = re.search(r"\*\*(\d+) berkas", teks)
        if m and int(m.group(1)) != len(nyata):
            lapor("GALAT", "laci", "%s: _ISI.md menulis %s berkas, sebenarnya %d"
                  % (rel, m.group(1), len(nyata)))


# ── 4. Salinan ganda di dalam vault ──────────────────────────────────
def periksa_ganda():
    sidik = collections.defaultdict(list)
    for akar, dirs, berkas in os.walk(VAULT):
        for b in berkas:
            if b.lower().endswith(".pdf"):
                p = os.path.join(akar, b)
                sidik[hashfile(p)].append(os.path.relpath(p, EKAS))
    for h, ps in sidik.items():
        if len(ps) > 1:
            lapor("PERINGATAN", "ganda", "isi sama di %d tempat: %s" % (len(ps), " | ".join(x[-58:] for x in ps)))
    return sidik


# ── 5. Berkas vault yang tidak terdaftar ─────────────────────────────
def periksa_tak_terdaftar(rows):
    laci_terdaftar = {r["vault_path"] for r in rows}
    for akar, dirs, berkas in os.walk(VAULT):
        pdf = [b for b in berkas if b.lower().endswith(".pdf")]
        if not pdf:
            continue
        rel = os.path.relpath(akar, EKAS).replace(os.sep, "/")
        if rel not in laci_terdaftar:
            lapor("PERINGATAN", "yatim", "%d berkas di laci yang tidak dirujuk register: %s"
                  % (len(pdf), rel))


# ── 6. Jalur yang disebut dokumen tetapi tidak ada ───────────────────
def periksa_jalur():
    pola = re.compile(r"`(0\d_[A-Z][A-Za-z0-9_\-/&\. ]+|R[1-5]/[A-Z][A-Za-z0-9\-]*/?)`")
    ruang = glob.glob(os.path.join(EKAS, "**", "*.md"), recursive=True)
    ruang += glob.glob(os.path.join(SKILLS, "*", "*.md"))
    ruang += glob.glob(os.path.join(SKILLS, "*", "references", "*.md"))
    pendek = {"R1": "R1_NATIONAL-NORMATIVE", "R2": "R2_INTERNATIONAL-STANDARDS",
              "R3": "R3_TEXTBOOK-HANDBOOK", "R4": "R4_OEM-TECHNICAL",
              "R5": "R5_RESEARCH-SECONDARY"}
    rusak = collections.Counter()
    for f in ruang:
        if os.sep + "99_ARCHIVE" + os.sep in f or "CHANGELOG" in f:
            continue
        for m in pola.findall(isi(f)):
            if m.lower().endswith((".pdf", ".epub")):
                continue          # nama berkas, bukan jalur map
            j = m.rstrip("/")
            if re.match(r"^R[1-5]/", j):
                bagian = j.split("/")
                j = os.path.join(VAULT, pendek[bagian[0]], *bagian[1:])
            else:
                j = os.path.join(EKAS, j.replace("/", os.sep))
            if not os.path.exists(j):
                rusak[m] += 1
    for j, n in rusak.most_common():
        lapor("GALAT", "jalur", "jalur tidak dapat diselesaikan (%d kali): `%s`" % (n, j))


# ── 7. Kutipan halaman melebihi jumlah halaman berkas ────────────────
def periksa_halaman():
    try:
        import fitz
    except ImportError:
        lapor("CATATAN", "halaman", "PyMuPDF tidak ada — pemeriksaan halaman dilewati")
        return
    # laci berisi tepat satu PDF -> kutipan di berkas yang menyebut laci itu dapat diuji
    for akar, dirs, berkas in os.walk(VAULT):
        pdf = [b for b in berkas if b.lower().endswith(".pdf")]
        if len(pdf) != 1:
            continue
        try:
            d = fitz.open(os.path.join(akar, pdf[0]))
            n = d.page_count
            d.close()
        except Exception:
            continue
        laci = os.path.basename(akar)
        for f in glob.glob(os.path.join(EKAS, "05_DOMAIN-KNOWLEDGE", "**", "*.md"), recursive=True):
            t = isi(f)
            if laci not in t:
                continue
            for hal in re.findall(r"PDF\s+(\d{1,4})", t):
                if int(hal) > n:
                    lapor("GALAT", "halaman", "%s: menyebut PDF %s, `%s` hanya %d halaman"
                          % (os.path.basename(f)[:44], hal, laci, n))


# ── 8. Sumber kebenaran ganda di luar EKAS ───────────────────────────
def periksa_ganda_akar():
    kembar = []
    for akar, dirs, berkas in os.walk(EKAS):
        for b in berkas:
            if b.endswith(".md"):
                kembar.append((b, os.path.join(akar, b)))
    peta = collections.defaultdict(list)
    for b, p in kembar:
        peta[b].append(p)
    for luar in glob.glob(os.path.join(RAK, "*.md")) + glob.glob(os.path.join(RAK, "_sistem", "**", "*.md"), recursive=True):
        b = os.path.basename(luar)
        if b in peta:
            sama = any(isi(luar) == isi(x) for x in peta[b])
            lapor("GALAT" if not sama else "PERINGATAN", "kembar-akar",
                  "%s ada di luar EKAS %s" % (b, "(ISI BERBEDA)" if not sama else "(isi sama)"))


def main():
    rows = periksa_register()
    periksa_kartu(rows)
    periksa_laci()
    periksa_ganda()
    periksa_tak_terdaftar(rows)
    periksa_jalur()
    if HALAMAN:
        periksa_halaman()
    periksa_ganda_akar()

    urut = {"GALAT": 0, "PERINGATAN": 1, "CATATAN": 2}
    temuan.sort(key=lambda x: (urut[x[0]], x[1]))
    c = collections.Counter(t for t, _, _ in temuan)

    print("=" * 72)
    print("PERIKSA EKAS")
    print("=" * 72)
    kel = None
    for t, k, m in temuan:
        if DIAM and t != "GALAT":
            continue
        if (t, k) != kel:
            kel = (t, k)
            print()
            print("[%s] %s" % (t, k))
        print("   ", m[:150])
    print()
    print("=" * 72)
    print("GALAT %d · PERINGATAN %d · CATATAN %d" % (c["GALAT"], c["PERINGATAN"], c["CATATAN"]))
    print("=" * 72)
    return 1 if c["GALAT"] else 0


if __name__ == "__main__":
    sys.exit(main())
