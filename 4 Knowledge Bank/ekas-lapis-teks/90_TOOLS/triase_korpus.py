# -*- coding: utf-8 -*-
"""
TRIASE KORPUS — menyaring seluruh berkas kandidat di mesin ini menjadi
antrean intake terklasifikasi R1-R5 + kategori teknik.

Menggantikan pemeriksaan satu per satu. Sekali jalan menghasilkan:
  02_REGISTERS/INTAKE-QUEUE.csv   — antrean terurut prioritas
  02_REGISTERS/INTAKE-RINGKAS.md  — ringkasan untuk dibaca manusia

TIDAK memindahkan, menyalin, atau mengubah berkas apa pun.

Jalankan:  python triase_korpus.py
Opsi   :   --dalam   baca halaman judul tiap PDF (lebih tepat, lebih lambat)
"""
import io, os, re, sys, csv, hashlib

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HOME = r"C:\Users\gspen"
RAK = os.path.join(HOME, "Videos", "Buku")
EKAS = os.path.join(RAK, "GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM")
VAULT = os.path.join(EKAS, "03_SOURCE-VAULT")
SUMBER = ["Downloads", "Documents", "Desktop", "OneDrive", "Videos", "Pictures"]
EKST = (".pdf", ".epub", ".djvu", ".chm", ".mobi")
DALAM = "--dalam" in sys.argv
INTIP = [0]

# ── R1: regulasi & standar nasional Indonesia ────────────────────────
R1 = [r"\bSNI[\s\-_]?\d", r"\bPUIL\b", r"\bPERMEN\w*\b", r"\bPERKAP\b", r"\bPERGUB\b",
      r"\bPERBAN\b", r"\bUU[\s\-_]?(No\.?\s*)?\d+[\s\-_]*(TAHUN|/)\s*\d{4}",
      r"\bSKKNI\b", r"\bPERPRES\b", r"\bPERMENAKER\b", r"\bKEPMEN\w*\b",
      r"\bBSSN\b", r"\bPeraturan\s+(Menteri|Pemerintah|Presiden|Badan)\b"]
# ── R2: standar internasional ────────────────────────────────────────
R2 = [r"\bIEC[\s\-_]?\d", r"\bIEEE[\s\-_]?(Std[\s\-_]?)?\d", r"\bISO[\s\-_/]?(IEC[\s\-_])?\d",
      r"\bBS[\s\-_]?EN[\s\-_]?\d", r"\bEN[\s\-_]?\d{4,}", r"\bANSI[\s\-_/]",
      r"\bNETA\b", r"\bNFPA[\s\-_]?\d", r"\bTIA[\s\-_]?\d{3}", r"\bITU[\s\-_]?T\b",
      r"\bASTM\b", r"\bASHRAE\b", r"\bASME\b", r"\bNIST[\s\-_]?SP[\s\-_]?\d",
      r"\bONVIF\b", r"\bETSI\b", r"\bRFC[\s\-_]?\d{3,}"]
# ── R4: dokumentasi pabrikan ─────────────────────────────────────────
R4 = [r"\bdatasheet\b", r"\bdata[\s\-_]sheet\b", r"\bspec[\s\-_]?sheet\b",
      r"\buser[\s\-_]manual\b", r"\binstallation[\s\-_]guide\b", r"\bconfiguration[\s\-_]guide\b",
      r"\bproduct[\s\-_]guide\b", r"\bcatalog(ue)?\b", r"\bbrochure\b",
      r"\bhardware[\s\-_]guide\b", r"\bfirmware\b", r"\brelease[\s\-_]notes\b",
      r"\bspecification\b", r"\bSPEC[\s\-_]?V?\d", r"\bquick[\s\-_]start\b",
      r"\bordering[\s\-_]guide\b", r"\bmodel[\s\-_]?no\b", r"\bP/N\b"]
# ── R5: sekunder ─────────────────────────────────────────────────────
R5 = [r"\btesis\b", r"\bthesis\b", r"\bdisertasi\b", r"\bdissertation\b",
      r"\bskripsi\b", r"\bjurnal\b", r"\bjournal\b", r"\bproceedings?\b",
      r"\bwhite[\s\-_]?paper\b", r"\bsurvey\b", r"\ba[\s\-_]review\b",
      r"^\d{4}\.\d{4,5}", r"\barXiv\b", r"_IEEE_", r"\bconference\b"]

# ── kategori teknik ──────────────────────────────────────────────────
KAT = [
 ("ELECTRICAL-POWER", r"electric|power system|switchgear|transformer|busbar|substation|"
  r"circuit breaker|protection relay|arc flash|short circuit|load flow|kelistrikan|gardu"),
 ("POWER-BACKUP", r"\bUPS\b|\bbatter(y|ies|ai)\b|generator set|genset|diesel gen|rectifier|inverter|"
  r"VRLA|lithium|fuel cell|photovolta|solar"),
 ("GROUNDING-LIGHTNING", r"\bground(ing)?\b|earthing|bonding|lightning|surge protect|\bSPD\b|"
  r"petir|pembumian|\bEMC\b|\bEMI\b|shielding"),
 ("FIBER-OPTIC", r"fib(er|re)[\s\-_]?optic|OTDR|splic|singlemode|multimode|DWDM|CWDM|"
  r"optical (network|transport)|GPON|FTTH|serat optik"),
 ("NETWORKING", r"\bTCP\b|IP network|routing|\bswitching\b|\bBGP\b|\bOSPF\b|\bMPLS\b|\bLAN\b|\bWAN\b|SD-WAN|"
  r"\bCCNA\b|\bCCNP\b|\bJNCIA\b|ethernet|wireless|Wi-?Fi|802\.11|\b5G\b|\bLTE\b|radio link|microwave"),
 ("VIDEO-SURVEILLANCE", r"\bCCTV\b|video surveillance|IP camera|\bVMS\b|\bNVR\b|\bONVIF\b|thermal camera|"
  r"video analytic|face recog|\bANPR\b|\bLPR\b|pengawasan"),
 ("STORAGE-DATACENTER", r"\bRAID\b|\bSAN\b|\bNAS\b|storage|data ?cent(er|re)|"
  r"\bserver\b|virtualiz|VMware|hyper-?v|kubernetes|backup|disaster recovery|TIA-942"),
 ("CYBERSECURITY", r"cyber ?security|information security|infosec|penetration test|"
  r"pentest|\bSIEM\b|\bSOC\b|malware|ransomware|forensic|incident response|ISO ?27|NIST ?CSF|"
  r"zero trust|cryptograph|encryption|keamanan siber"),
 ("RELIABILITY-MAINTENANCE", r"\bRCM\b|reliability|maintenance|FMEA|FMECA|RAMS|availability|"
  r"condition monitoring|predictive maint|vibration analysis|root cause|keandalan|pemeliharaan"),
 ("MECHANICAL", r"mechanical (design|engineering)|machine design|shigley|stress analysis|"
  r"finite element|\bFEA\b|fatigue|bearing|gear|shaft|weld"),
 ("HVAC-THERMAL", r"\bHVAC\b|air condition|cooling|chiller|thermal management|"
  r"heat transfer|thermograph|infrared|refrigerat|ventilat"),
 ("CIVIL-STRUCTURAL", r"civil engineering|structural|concrete|steel structure|foundation|"
  r"geotechni|tower design|mast|struktur|beton|pondasi"),
 ("INSTRUMENTATION-CONTROL", r"instrumentation|control system|\bPLC\b|\bSCADA\b|\bDCS\b|"
  r"sensor|transmitter|calibration|process control|automation|\bPID\b"),
 ("RF-ANTENNA", r"antenna|\bRF\b|radio frequency|propagation|link budget|waveguide|"
  r"microwave|spectrum|\bSDR\b|electromagnetic wave"),
 ("SOFTWARE-DATA", r"software (engineering|architecture)|programming|database|"
  r"machine learning|deep learning|artificial intelligence|data science|python|"
  r"algorithm|distributed system"),
 ("PROJECT-QUALITY", r"project management|\bPMBOK\b|quality (management|assurance|control)|"
  r"ISO ?9001|six sigma|commissioning|inspection and test|\bITP\b|contract management"),
 ("SAFETY-K3", r"\bK3\b|occupational (health|safety)|\bHSE\b|safety engineering|"
  r"hazard|risk assessment|LOTO|arc flash|keselamatan kerja|\bHAZOP\b"),
 ("PHYSICAL-SECURITY", r"perimeter|access control|intrusion detect|fence|barrier|"
  r"\bradar\b|screening|guard force|physical security|keamanan fisik"),
 ("GEOSPATIAL-SURVEY", r"geospatial|\bGIS\b|survey(ing)?|geodes|photogrammetr|\bLiDAR\b|"
  r"\bGNSS\b|\bGPS\b|remote sensing|cartograph|pemetaan"),
 ("DEFENSE-C4ISR", r"\bC4ISR\b|\bISR\b|military|defen[cs]e\b|command and control|battlefield|"
  r"electronic warfare|SIGINT|COMINT|tactical|pertahanan"),
]

# yang jelas BUKAN teknik — dibuang cepat
BUKAN = re.compile(
 r"invoice|kwitansi|struk|receipt|nota|rekening|tagihan|npwp|ktp|paspor|passport|"
 r"quotation|quote|proforma|penawaran|purchase ?order|PO[\s\-_]?\d|price ?list|"
 r"cv[\s\-_]|curriculum vitae|resume[\s\-_]kerja|lamaran|ijazah|sertifikat[\s\-_]pelatihan|"
 r"undangan|brosur[\s\-_]wisata|menu|resep|novel|komik|majalah[\s\-_]hiburan|"
 r"laporan[\s\-_]keuangan|slip[\s\-_]gaji|boarding|tiket|ticket", re.I)


def hashfile(p, n=1 << 20):
    h = hashlib.md5()
    with open(p, "rb") as f:
        h.update(f.read(n))
    return h.hexdigest()


def teks_judul(p):
    """Ambil teks halaman 1-2 bila PyMuPDF ada."""
    try:
        import fitz
        d = fitz.open(p)
        t = "".join(d[i].get_text() for i in range(min(2, d.page_count)))
        d.close()
        return t[:4000]
    except Exception:
        return ""


def cocok(pola_list, teks):
    for pola in pola_list:
        if re.search(pola, teks, re.I):
            return re.search(pola, teks, re.I).group(0).strip()
    return None


def nilai_r(teks):
    # R4 diperiksa SEBELUM R2: lembar data produk hampir selalu menyebut standar
    # yang dipatuhinya ("sesuai IEC 60950") — itu kepatuhan, bukan standarnya.
    for R, pola in (("R1", R1), ("R4", R4), ("R2", R2), ("R5", R5)):
        m = cocok(pola, teks)
        if m:
            return R, m
    return "R3", ""


def kategori(teks):
    hit = [(k, len(re.findall(p, teks, re.I))) for k, p in KAT]
    hit = [(k, n) for k, n in hit if n]
    if not hit:
        return "", 0
    hit.sort(key=lambda x: -x[1])
    return hit[0][0], hit[0][1]


# celah yang sedang dicari — dipakai untuk skor prioritas
CELAH = {
 "PUIL": 10, "SNI": 10, "ONVIF": 10, "ISO 27001": 9, "ISO/IEC 27001": 9,
 "NIST SP 800-86": 9, "ISO/IEC 27037": 9, "TIA-568": 7, "TIA-942": 7,
 "NETA MTS": 7, "IEEE 450": 7, "IEC 61280-4-1": 6, "IEC 62305": 8,
 "NFPA 780": 6, "NFPA 70E": 6, "UU 11/2008": 9, "BSSN": 9, "ISO 9001": 5,
}


def main():
    # sidik jari isi vault, supaya duplikat tidak masuk antrean
    ada = set()
    for r, d, bs in os.walk(EKAS):
        for b in bs:
            if b.lower().endswith(".pdf"):
                ada.add(hashfile(os.path.join(r, b)))
    print("berkas sudah di EKAS :", len(ada))

    kandidat = []
    for s in SUMBER:
        base = os.path.join(HOME, s)
        if not os.path.isdir(base):
            continue
        for r, d, bs in os.walk(base):
            if RAK.lower() in r.lower():
                continue
            for b in bs:
                if b.lower().endswith(EKST):
                    kandidat.append(os.path.join(r, b))
    print("kandidat ditemukan   :", len(kandidat))

    baris = []
    dibuang = dup = 0
    for p in kandidat:
        nama = os.path.basename(p)
        if BUKAN.search(nama):
            dibuang += 1
            continue
        try:
            if p.lower().endswith(".pdf") and hashfile(p) in ada:
                dup += 1
                continue
            ukuran = os.path.getsize(p)
        except Exception:
            continue

        teks = nama.replace("_", " ")
        R, penanda = nilai_r(teks)
        kat, kuat = kategori(teks)

        # Nama berkas sering tidak memberi petunjuk — intip halaman judulnya.
        # Ini yang menemukan standar dengan nama berkas asal-asalan.
        if p.lower().endswith(".pdf") and ukuran > 200_000 and (not kat or R == "R3"):
            dalam = teks_judul(p)
            if dalam:
                INTIP[0] += 1
                gab = teks + " \n" + dalam
                Rd, pend = nilai_r(gab)
                if Rd != "R3":
                    R, penanda = Rd, pend
                kd, ud = kategori(gab)
                if ud > kuat:
                    kat, kuat = kd, ud

        # Sumber R1/R2/R4 TIDAK PERNAH dibuang walau kategorinya belum ketahuan —
        # justru inilah yang paling dicari. Nama standar sering tidak memuat kata
        # teknis apa pun ("SNI 0225-2011", "IEC 62305-3").
        if not kat:
            if R in ("R1", "R2", "R4"):
                kat = "PERLU-DINILAI"
            else:
                dibuang += 1
                continue

        skor = {"R1": 40, "R2": 30, "R4": 10, "R3": 15, "R5": 5}[R] + min(kuat, 8)
        for c, n in CELAH.items():
            if re.search(re.escape(c).replace(r"\ ", r"[\s\-_/]?"), teks, re.I):
                skor += n * 3
                penanda = (penanda + " | CELAH:" + c).strip(" |")
        if ukuran < 300_000:
            skor -= 8          # kemungkinan fragmen
        if ukuran > 5_000_000:
            skor += 4          # kemungkinan buku/standar utuh

        baris.append(dict(skor=skor, r_level=R, kategori=kat, nama=nama,
                          mb=round(ukuran / 1048576.0, 1), penanda=penanda, jalur=p))

    baris.sort(key=lambda x: (-x["skor"], x["kategori"]))

    out = os.path.join(EKAS, "02_REGISTERS", "INTAKE-QUEUE.csv")
    with io.open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["skor", "r_level", "kategori", "nama", "mb",
                                           "penanda", "jalur"])
        w.writeheader()
        w.writerows(baris)

    print("halaman judul diintip :", INTIP[0])
    print("bukan teknik / dibuang:", dibuang)
    print("duplikat vault        :", dup)
    print("masuk antrean         :", len(baris))
    print()
    from collections import Counter
    cr = Counter(b["r_level"] for b in baris)
    ck = Counter(b["kategori"] for b in baris)
    print("menurut tingkat:", "  ".join("%s:%d" % (k, cr[k]) for k in ["R1", "R2", "R3", "R4", "R5"]))
    print()
    print("menurut kategori:")
    for k, n in ck.most_common():
        print("   %-26s %3d" % (k, n))
    print()
    print("20 teratas:")
    for b in baris[:20]:
        print("  %3d  %-3s %-24s %5.1fMB  %s" % (
            b["skor"], b["r_level"], b["kategori"][:24], b["mb"], b["nama"][:60]))
    print()
    # ── ringkasan untuk dibaca manusia ───────────────────────────────
    ring = os.path.join(EKAS, "02_REGISTERS", "INTAKE-RINGKAS.md")
    NL = chr(10)

    def tabel(rows, n=25):
        return NL.join("| %d | %s | %s | %.1f MB | `%s` |" % (
            b["skor"], b["r_level"], b["kategori"], b["mb"], b["nama"][:70]) for b in rows[:n])
    with io.open(ring, "w", encoding="utf-8") as fh:
        fh.write(u"""# Antrean Intake — hasil triase korpus

**Dibangun otomatis oleh** `90_TOOLS/triase_korpus.py` · **Jangan disunting tangan** —
berkas ini ditimpa tiap kali alatnya dijalankan.

Kandidat dipindai: **%d** · masuk antrean: **%d** · dibuang (bukan teknik/duplikat): **%d**
Halaman judul diintip: **%d**

> **Antrean bukan penilaian.** Seluruh baris di sini berstatus `INTAKE_ONLY` sampai
> dibuka, diresume, dan dinilai manusia. Tingkat R di bawah adalah **dugaan mesin**
> dari nama berkas dan halaman judul — bukan penetapan.

## Sebaran menurut tingkat

| Tingkat | Jumlah | Artinya |
|---|---|---|
| **R1** | %d | Regulasi Indonesia — yang paling dicari |
| **R2** | %d | Standar internasional |
| **R3** | %d | Buku teks / handbook |
| **R4** | %d | Dokumentasi produk (OEM) |
| **R5** | %d | Sekunder |

## Sebaran menurut kategori teknik

%s

## 25 teratas menurut skor

| Skor | R | Kategori | Ukuran | Berkas |
|---|---|---|---|---|
%s

## Cara memakai

1. Buka `INTAKE-QUEUE.csv`, saring kolom `r_level` = `R1` atau `R2` lebih dulu.
2. Buka berkasnya, **periksa isi terhadap namanya** — dugaan mesin sering meleset.
3. Yang lolos: ikuti `01_GOVERNANCE/SOURCE-UPDATE-PROCEDURE.md`.
4. Yang tidak relevan: cukup abaikan — antrean dibangun ulang tiap kali alat dijalankan.

## Batas alat ini

- **Tidak mengunduh apa pun.** Hanya memindai berkas yang sudah ada di mesin ini.
- Dugaan R **sering keliru** pada dokumen yang menyebut standar sebagai kepatuhan.
  Lembar data produk yang menulis "sesuai IEC 60950" adalah **R4**, bukan R2.
- Kategori diambil dari kata yang paling sering muncul — dokumen lintas bidang bisa
  masuk kategori yang kurang tepat.
""" % (len(kandidat), len(baris), dibuang + dup, INTIP[0],
       cr["R1"], cr["R2"], cr["R3"], cr["R4"], cr["R5"],
       NL.join("- **%s** — %d" % (k, n) for k, n in ck.most_common()),
       tabel(baris)))
    print("ringkasan     :", ring)
    print("antrean penuh:", out)


if __name__ == "__main__":
    main()
