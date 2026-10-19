# -*- coding: utf-8 -*-
"""
Membangun kerangka direktori GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM
dan mengisi seluruh lapis dokumen turunan.

TIDAK memindahkan berkas PDF. Pemetaannya ditulis ke manifest;
pemindahan fisik dikerjakan terpisah oleh migrasi_sumber.py.

Jalankan:  python "C:/Users/gspen/Videos/Buku/_tools/bangun_ekas_struktur.py"
"""
import io, os, csv, shutil, re

RAK = r"C:\Users\gspen\Videos\Buku"
EKAS = os.path.join(RAK, "GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM")
SKILLS = r"C:\Users\gspen\.claude\skills"

# ─────────────────────────────────────────────────────────────────────
# KERANGKA
# ─────────────────────────────────────────────────────────────────────
POHON = """
00_START-HERE
01_GOVERNANCE
02_REGISTERS
03_SOURCE-VAULT/R1_NATIONAL-NORMATIVE/SNI
03_SOURCE-VAULT/R1_NATIONAL-NORMATIVE/PUIL
03_SOURCE-VAULT/R1_NATIONAL-NORMATIVE/PERMENAKER
03_SOURCE-VAULT/R1_NATIONAL-NORMATIVE/SKKNI
03_SOURCE-VAULT/R1_NATIONAL-NORMATIVE/OTHER-REGULATION
03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/IEC
03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ISO-IEC
03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/IEEE
03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/TIA
03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ITU-T
03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/EN-BS
03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ANSI-NETA
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/BATTERY
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/CCTV-VSS
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/ELECTRICAL
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/FIBER-OPTIC
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/GENSET
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/GROUNDING
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/LIGHTNING
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/NETWORK
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/RCM
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/STORAGE
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/THERMAL
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/UPS
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/MECHANICAL
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/SECURITY
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/OPERATIONS
03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/CRITICAL-INFRASTRUCTURE
03_SOURCE-VAULT/R4_OEM-TECHNICAL/CAMERA
03_SOURCE-VAULT/R4_OEM-TECHNICAL/VMS-NVR
03_SOURCE-VAULT/R4_OEM-TECHNICAL/NETWORK
03_SOURCE-VAULT/R4_OEM-TECHNICAL/UPS
03_SOURCE-VAULT/R4_OEM-TECHNICAL/GENSET
03_SOURCE-VAULT/R4_OEM-TECHNICAL/SERVER-STORAGE
03_SOURCE-VAULT/R4_OEM-TECHNICAL/TEST-EQUIPMENT
03_SOURCE-VAULT/R5_RESEARCH-SECONDARY/PAPERS
03_SOURCE-VAULT/R5_RESEARCH-SECONDARY/THESIS
03_SOURCE-VAULT/R5_RESEARCH-SECONDARY/TECHNICAL-GUIDES
03_SOURCE-VAULT/R5_RESEARCH-SECONDARY/RESEARCH-INTAKE
06_ENGINEERING/REQUIREMENTS
06_ENGINEERING/DESIGN-DECISIONS
06_ENGINEERING/ASSUMPTIONS
06_ENGINEERING/CALCULATIONS
06_ENGINEERING/DESIGN-REVIEWS
07_VERIFICATION-VALIDATION/ITP
07_VERIFICATION-VALIDATION/FAT
07_VERIFICATION-VALIDATION/SAT
07_VERIFICATION-VALIDATION/TEST-PROCEDURES
07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA
07_VERIFICATION-VALIDATION/NON-CONFORMANCE
08_EVIDENCE/MEASUREMENT
08_EVIDENCE/OTDR
08_EVIDENCE/OLTS
08_EVIDENCE/GROUNDING
08_EVIDENCE/ELECTRICAL
08_EVIDENCE/SCREENSHOTS-LOGS
08_EVIDENCE/PHOTO
08_EVIDENCE/CERTIFICATES
09_HANDOVER/AS-BUILT
09_HANDOVER/ASSET-REGISTER
09_HANDOVER/CONFIGURATION-BACKUP
09_HANDOVER/TEST-RESULT
09_HANDOVER/TRAINING
09_HANDOVER/O&M-MANUAL
09_HANDOVER/BERITA-ACARA
10_TEMPLATES
90_TOOLS
95_IMPORT-SNAPSHOTS/BATCH-01
95_IMPORT-SNAPSHOTS/BATCH-02
99_ARCHIVE/SUPERSEDED
99_ARCHIVE/ORIGINAL-BEFORE-OCR
99_ARCHIVE/LEGACY-EKAS
99_ARCHIVE/OLD-EXPORTS
""".strip().splitlines()

DOMAIN = ["FIBER-OPTIC", "VIDEO-SURVEILLANCE", "POWER-BACKUP", "GROUNDING-LIGHTNING",
          "ELECTRICAL", "THERMAL", "RCM", "NETWORKING", "STORAGE", "CYBERSECURITY",
          "MECHANICAL", "CRITICAL-INFRASTRUCTURE"]

# ─────────────────────────────────────────────────────────────────────
# PEMETAAN SUMBER: folder rak → (R, jalur vault, domain, id)
# ─────────────────────────────────────────────────────────────────────
PETA = [
    # (folder rak, subfolder, R, vault, domain, prefix id)
    ("Battery", "", "R3", "R3_TEXTBOOK-HANDBOOK/BATTERY", "POWER-BACKUP", "BAT"),
    ("Battery", "_standar", "R2", "R2_INTERNATIONAL-STANDARDS/IEEE", "POWER-BACKUP", "BAT"),
    ("CCTV VSS", "", "R3", "R3_TEXTBOOK-HANDBOOK/CCTV-VSS", "VIDEO-SURVEILLANCE", "VSS"),
    ("CCTV VSS", "_standar", "R2", "R2_INTERNATIONAL-STANDARDS/EN-BS", "VIDEO-SURVEILLANCE", "VSS"),
    ("Critical Infrastructure", "", "R3", "R3_TEXTBOOK-HANDBOOK/CRITICAL-INFRASTRUCTURE", "CRITICAL-INFRASTRUCTURE", "CIP"),
    ("Cyber Operations", "", "R3", "R3_TEXTBOOK-HANDBOOK/SECURITY", "CYBERSECURITY", "SEC"),
    ("Cybersecurity", "", "R3", "R3_TEXTBOOK-HANDBOOK/SECURITY", "CYBERSECURITY", "SEC"),
    ("Cybersecurity", "_panduan", "R5", "R5_RESEARCH-SECONDARY/TECHNICAL-GUIDES", "CYBERSECURITY", "SEC"),
    ("Cybersecurity", "_tesis", "R5", "R5_RESEARCH-SECONDARY/THESIS", "CYBERSECURITY", "SEC"),
    ("Electrical Maintenance", "", "R3", "R3_TEXTBOOK-HANDBOOK/ELECTRICAL", "ELECTRICAL", "ELC"),
    ("Electrical Maintenance", "_standar", "R2", "R2_INTERNATIONAL-STANDARDS/ANSI-NETA", "ELECTRICAL", "ELC"),
    ("Fiber Optic Fundamental", "", "R3", "R3_TEXTBOOK-HANDBOOK/FIBER-OPTIC", "FIBER-OPTIC", "FO"),
    ("FO Test Advanced", "", "R3", "R3_TEXTBOOK-HANDBOOK/FIBER-OPTIC", "FIBER-OPTIC", "FO"),
    ("FO Test Advanced", "_standar", "R2", "R2_INTERNATIONAL-STANDARDS/IEC", "FIBER-OPTIC", "FO"),
    ("Genset", "", "R3", "R3_TEXTBOOK-HANDBOOK/GENSET", "POWER-BACKUP", "PWR"),
    ("Grounding & Bonding", "", "R3", "R3_TEXTBOOK-HANDBOOK/GROUNDING", "GROUNDING-LIGHTNING", "GRD"),
    ("Lightning Protection", "", "R3", "R3_TEXTBOOK-HANDBOOK/LIGHTNING", "GROUNDING-LIGHTNING", "LPS"),
    ("Maintenance Management", "", "R3", "R3_TEXTBOOK-HANDBOOK/RCM", "RCM", "RCM"),
    ("Maintenance Planning", "", "R3", "R3_TEXTBOOK-HANDBOOK/RCM", "RCM", "RCM"),
    ("Mechanical Structure", "", "R3", "R3_TEXTBOOK-HANDBOOK/MECHANICAL", "MECHANICAL", "MEC"),
    ("Network Troubleshooting", "", "R3", "R3_TEXTBOOK-HANDBOOK/NETWORK", "NETWORKING", "NET"),
    ("Networking", "", "R3", "R3_TEXTBOOK-HANDBOOK/NETWORK", "NETWORKING", "NET"),
    ("Networking Fundamentals", "", "R3", "R3_TEXTBOOK-HANDBOOK/NETWORK", "NETWORKING", "NET"),
    ("RCM", "", "R3", "R3_TEXTBOOK-HANDBOOK/RCM", "RCM", "RCM"),
    ("Storage RAID NVR", "", "R3", "R3_TEXTBOOK-HANDBOOK/STORAGE", "STORAGE", "STG"),
    ("System Administration", "", "R3", "R3_TEXTBOOK-HANDBOOK/OPERATIONS", "NETWORKING", "OPS"),
    ("TCP IP", "", "R3", "R3_TEXTBOOK-HANDBOOK/NETWORK", "NETWORKING", "NET"),
    ("Thermal Camera", "", "R3", "R3_TEXTBOOK-HANDBOOK/THERMAL", "THERMAL", "THM"),
    ("UPS", "", "R3", "R3_TEXTBOOK-HANDBOOK/UPS", "POWER-BACKUP", "PWR"),
    ("Video Analytics", "", "R3", "R3_TEXTBOOK-HANDBOOK/CCTV-VSS", "VIDEO-SURVEILLANCE", "VAI"),
]

RANTAI_DOMAIN = {
    "A-serat-optik.md": "FIBER-OPTIC",
    "B-video-pengawasan.md": "VIDEO-SURVEILLANCE",
    "C-catu-daya-baterai.md": "POWER-BACKUP",
    "D-pembumian-petir.md": "GROUNDING-LIGHTNING",
    "E-uji-instalasi-listrik.md": "ELECTRICAL",
    "F-termografi.md": "THERMAL",

#> CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24): pemetaan 'F-termografi.md' -> THERMAL di atas menunjuk berkas PHANTOM - `F-termografi.md` tidak pernah ada di disk (find = 0; register K-6 studi NWSKILL-0923, docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md Bagian 5). Sasaran nyata rantai F = `05_DOMAIN-KNOWLEDGE/THERMAL/RANTAI-JAMINAN.md`. Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
    "G-keandalan-pemeliharaan.md": "RCM",
    "H-penyimpanan-jaringan.md": "STORAGE",
}


def tulis(rel, teks):
    p = os.path.join(EKAS, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8").write(teks)


def salin(src, rel):
    p = os.path.join(EKAS, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    shutil.copy2(src, p)


def main():
    # 1 — kerangka
    for d in POHON:
        os.makedirs(os.path.join(EKAS, d.strip()), exist_ok=True)
    for d in DOMAIN:
        os.makedirs(os.path.join(EKAS, "04_KNOWLEDGE-CARDS", d), exist_ok=True)
        os.makedirs(os.path.join(EKAS, "05_DOMAIN-KNOWLEDGE", d), exist_ok=True)

    # 2 — kumpulkan sumber
    sumber = []   # dict per berkas PDF
    resume = []   # dict per resume
    ctr = {}
    for folder, sub, R, vault, dom, pre in PETA:
        d = os.path.join(RAK, folder, sub) if sub else os.path.join(RAK, folder)
        if not os.path.isdir(d):
            continue
        for b in sorted(os.listdir(d)):
            f = os.path.join(d, b)
            if not os.path.isfile(f):
                continue
            relrak = os.path.relpath(f, RAK)
            if b.lower().endswith(".pdf"):
                sumber.append(dict(R=R, vault=vault, domain=dom, nama=b,
                                   asal=relrak, ukuran=os.path.getsize(f)))
            elif b.startswith("RESUME") and b.endswith(".md"):
                ctr[pre] = ctr.get(pre, 0) + 1
                rid = "REF-%s-%03d" % (pre, ctr[pre])
                judul = re.sub(r"^RESUME(\s+(STANDAR|TESIS|PANDUAN))?\s*-\s*", "", b[:-3])
                resume.append(dict(id=rid, R=R, domain=dom, judul=judul,
                                   asal=relrak, sumber_folder=folder + ("/" + sub if sub else ""),
                                   vault=vault))

    # 3 — salin resume ke 05_DOMAIN-KNOWLEDGE
    for r in resume:
        salin(os.path.join(RAK, r["asal"]),
              "05_DOMAIN-KNOWLEDGE/%s/%s - %s.md" % (r["domain"], r["R"], r["judul"]))

    # 4 — rantai jaminan ke domain
    for nama, dom in RANTAI_DOMAIN.items():
        src = os.path.join(RAK, "_sistem", "rantai", nama)
        if os.path.exists(src):
            salin(src, "05_DOMAIN-KNOWLEDGE/%s/RANTAI-JAMINAN.md" % dom)

    # 5 — manifest per laci vault
    laci = {}
    for s in sumber:
        laci.setdefault(s["vault"], []).append(s)
    for v, isi in laci.items():
        baris = "\n".join(
            "| `%s` | %.1f MB | `%s` |" % (x["nama"], x["ukuran"] / 1048576.0, x["asal"])
            for x in sorted(isi, key=lambda y: y["nama"]))
        tulis("03_SOURCE-VAULT/%s/_ISI.md" % v, u"""# Isi laci — `%s`

**%d berkas.** Berkas fisik **masih berada di lokasi rak lama** — laci ini belum diisi.
Pemindahannya dikerjakan `90_TOOLS/migrasi_sumber.py`.

| Berkas | Ukuran | Lokasi sekarang |
|---|---|---|
%s

> Setelah migrasi dijalankan, kolom "lokasi sekarang" tidak berlaku lagi dan manifest ini
> dibangun ulang oleh alatnya.
""" % (v, len(isi), baris))

    # laci kosong
    for d in POHON:
        d = d.strip()
        if not d.startswith("03_SOURCE-VAULT/"):
            continue
        v = d[len("03_SOURCE-VAULT/"):]
        if v in laci or "/" not in v:
            continue
        tulis("03_SOURCE-VAULT/%s/_ISI.md" % v, u"""# Isi laci — `%s`

**Kosong.** Belum ada sumber pada laci ini.

Jangan mengisi laci ini dengan sumber dari tingkat lain hanya karena topiknya cocok —
**tingkat R ditentukan oleh penerbit sumbernya, bukan oleh isinya.**
""" % v)

    # 6 — MASTER-REFERENCE-REGISTER.csv
    p = os.path.join(EKAS, "02_REGISTERS", "MASTER-REFERENCE-REGISTER.csv")
    with io.open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["reference_id", "r_level", "title", "domain", "vault_path",
                    "source_folder", "resume_path", "authority_status",
                    "may_set_acceptance", "notes"])
        for r in sorted(resume, key=lambda x: x["id"]):
            may = {"R2": "yes-if-adopted", "R3": "no-unless-contract-adopts",
                   "R5": "no"}[r["R"]]
            st = "ACTIVE_WITH_SCOPE_LIMITS" if r["R"] == "R2" else (
                "ACTIVE" if r["R"] == "R3" else "POINTER_ONLY")
            w.writerow([r["id"], r["R"], r["judul"], r["domain"],
                        "03_SOURCE-VAULT/" + r["vault"], r["sumber_folder"],
                        "05_DOMAIN-KNOWLEDGE/%s/%s - %s.md" % (r["domain"], r["R"], r["judul"]),
                        st, may, ""])

    # 7 — register kosong berkepala
    KEPALA = {
        "REQUIREMENT-REGISTER.csv": ["req_id", "project", "requirement_text", "source",
                                     "r_level", "owner_decision_ref", "status"],
        "DESIGN-DECISION-REGISTER.csv": ["ddr_id", "project", "decision", "rationale",
                                         "reference_id", "r_level", "rejected_alternative",
                                         "approved_by", "date"],
        "CALCULATION-REGISTER.csv": ["calc_id", "project", "quantity", "formula",
                                     "formula_source", "inputs", "input_tags", "result",
                                     "checked_by", "status"],
        "TEST-REGISTER.csv": ["test_id", "project", "test_type", "method", "method_source",
                              "instrument", "calibration_due", "acceptance_criterion",
                              "criterion_source", "r_level", "result", "witness"],
        "EVIDENCE-REGISTER.csv": ["evidence_id", "project", "test_id", "evidence_type",
                                  "file_path", "ba_number", "date", "status"],
        "ASSET-REFERENCE-REGISTER.csv": ["asset_id", "project", "asset_name", "location",
                                         "reference_id", "oem_doc_ref", "maintenance_task",
                                         "interval", "interval_basis"],
    }
    for nama, kepala in KEPALA.items():
        with io.open(os.path.join(EKAS, "02_REGISTERS", nama), "w",
                     encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerow(kepala)

    # 8 — GAP-REGISTER terisi
    GAP = [
        ["GAP-001", "R1", "PUIL / SNI kelistrikan", "Kepatuhan instalasi listrik Indonesia",
         "ELECTRICAL, GROUNDING-LIGHTNING", "TINGGI", "terbuka",
         "ANSI/NETA menutup ambang uji, BUKAN kepatuhan hukum Indonesia"],
        ["GAP-002", "R1", "UU 11/2008 (ITE) + perubahan", "Dasar hukum bukti elektronik",
         "CYBERSECURITY", "TINGGI", "terbuka",
         "Hanya disebut lewat tesis [R5]; wajib salinan aslinya"],
        ["GAP-003", "R1", "Peraturan BSSN No. 4/2021", "Kriteria audit siber instansi",
         "CYBERSECURITY", "TINGGI", "terbuka", "Hanya disebut lewat tesis [R5]"],
        ["GAP-004", "R1", "SNI proteksi petir", "Kepatuhan proteksi petir",
         "GROUNDING-LIGHTNING", "TINGGI", "terbuka", "Uman mengutip IEC 62305:2006 — usang"],
        ["GAP-005", "R2", "ONVIF", "Interoperabilitas perangkat video",
         "VIDEO-SURVEILLANCE", "TINGGI", "terbuka",
         "BS EN 62676-1-2 mengatur transmisi, BUKAN interoperabilitas"],
        ["GAP-006", "R2", "ISO/IEC 27001 & 27002", "Persyaratan SMKI",
         "CYBERSECURITY", "TINGGI", "terbuka", "Sering jadi syarat tender"],
        ["GAP-007", "R2", "NIST SP 800-86 · ISO/IEC 27037", "Penanganan bukti digital",
         "CYBERSECURITY", "TINGGI", "sebagian",
         "Alsmadi PDF 268 memberi proses 4 tahap + rantai kustodi [R3]"],
        ["GAP-008", "R2", "ANSI/NETA MTS", "Uji PEMELIHARAAN listrik",
         "ELECTRICAL", "MENENGAH", "terbuka", "Yang ada ATS = uji TERIMA"],
        ["GAP-009", "R2", "IEEE 450", "Uji baterai VENTED",
         "POWER-BACKUP", "MENENGAH", "terbuka",
         "IEEE 1188 hanya VRLA. Ada fragmen 5 hal di koleksi lain — bukan standar utuh"],
        ["GAP-010", "R2", "IEC 61280-4-1", "Uji redaman serat MULTIMODE",
         "FIBER-OPTIC", "MENENGAH", "terbuka", "Yang ada 4-2 = singlemode"],
        ["GAP-011", "R2", "TIA-568 / TIA-942", "Perkabelan terstruktur & pusat data",
         "STORAGE, NETWORKING", "MENENGAH", "terbuka", ""],
        ["GAP-012", "R3", "Bab 11 Diesel Generator Handbook", "Emergency & standby genset",
         "POWER-BACKUP", "MENENGAH", "terbuka", "± 55 halaman hilang dari berkas"],
        ["GAP-013", "R3", "Perencanaan kapasitas jaringan", "Rumus kapasitas",
         "NETWORKING", "RENDAH", "terbuka", "Fall & Stevens membahas protokol, bukan perancangan"],
        ["GAP-014", "R4", "Seluruh dokumentasi OEM", "Angka melekat produk",
         "SEMUA", "PER PROYEK", "by-design",
         "Tidak diadakan — diminta ke pabrikan tiap proyek"],
    ]
    with io.open(os.path.join(EKAS, "02_REGISTERS", "GAP-REGISTER.csv"), "w",
                 encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["gap_id", "missing_r_level", "missing_source", "impact",
                    "domain", "priority", "status", "notes"])
        w.writerows(GAP)

    # 9 — salin dokumen tata kelola & rekayasa
    S = os.path.join(RAK, "_sistem")
    salin(os.path.join(S, "01-TINGKAT-KEYAKINAN-RUJUKAN.md"),
          "01_GOVERNANCE/REFERENCE-CONFIDENCE-LEVEL.md")
    salin(os.path.join(S, "03-RANTAI-JAMINAN.md"), "01_GOVERNANCE/ASSURANCE-WORKFLOW.md")
    salin(os.path.join(S, "02-REGISTER-RUJUKAN.md"),
          "02_REGISTERS/MASTER-REFERENCE-REGISTER.md")
    salin(os.path.join(S, "04-KARTU-KENDALI.md"), "10_TEMPLATES/TPL-00-KARTU-KENDALI.md")
    salin(os.path.join(RAK, "PROSEDUR-TAMBAH-BUKU.md"),
          "01_GOVERNANCE/SOURCE-UPDATE-PROCEDURE.md")
    salin(os.path.join(RAK, "ASUMSI-BAKU.md"), "06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md")
    salin(os.path.join(RAK, "KATALOG-RUMUS.md"), "06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md")
    salin(os.path.join(RAK, "TEMPLATE-BERITA-ACARA.md"),
          "07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md")
    salin(os.path.join(RAK, "PETA-CELAH-KOLEKSI.md"), "02_REGISTERS/GAP-REGISTER.md")
    salin(os.path.join(RAK, "DAFTAR-PENGADAAN-BAHAN.md"),
          "02_REGISTERS/GAP-ACQUISITION-PLAN.md")
    salin(os.path.join(RAK, "RENCANA-KERJA.md"), "00_START-HERE/CHANGELOG.md")

    # 10 — perkakas
    for t in ["ocr_book.py", "buat_katalog_docx.py", "buat_paket_markdown.py",
              "buat_paket_batch2.py", "buat_paket_ekas.py", "bangun_ekas_struktur.py",
              "README-ekspor.md"]:
        f = os.path.join(RAK, "_tools", t)
        if os.path.exists(f):
            salin(f, "90_TOOLS/" + t)

    # 11 — arsip & snapshot
    for z, dst in [("Pustaka-Teknis-GSP-Markdown.zip", "95_IMPORT-SNAPSHOTS/BATCH-01/"),
                   ("Pustaka-Teknis-GSP-Batch2.zip", "95_IMPORT-SNAPSHOTS/BATCH-02/"),
                   ("Engineering-Knowledge-Assurance-System.zip", "99_ARCHIVE/OLD-EXPORTS/")]:
        f = os.path.join(RAK, z)
        if os.path.exists(f):
            salin(f, dst + z)

    return sumber, resume, laci


if __name__ == "__main__":
    sumber, resume, laci = main()
    print("EKAS dibangun di:", EKAS)
    print("laci vault terisi manifest :", len(laci))
    print("PDF terpetakan             :", len(sumber),
          "(%.0f MB)" % (sum(x["ukuran"] for x in sumber) / 1048576.0))
    print("resume tersalin            :", len(resume))
    for R in ["R1", "R2", "R3", "R4", "R5"]:
        print("   %s : %2d sumber · %2d resume" % (
            R, sum(1 for x in sumber if x["R"] == R),
            sum(1 for x in resume if x["R"] == R)))
