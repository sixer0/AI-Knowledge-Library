# -*- coding: utf-8 -*-
"""
SERAP R4 — memasukkan dokumentasi pabrikan hasil triase ke 03_SOURCE-VAULT/R4_OEM-TECHNICAL/

Membaca INTAKE-QUEUE.csv, mengambil baris R4, mengintip halaman judul untuk
menentukan lacinya, lalu MENYALIN (bukan memindahkan) ke laci yang sesuai.

Menyalin, bukan memindahkan — berkas kerja di Downloads sering masih dipakai.
Duplikat isi dibuang otomatis.

Jalankan:  python serap_r4.py            uji coba
           python serap_r4.py --jalankan  menyalin sungguhan
"""
import io, os, re, sys, csv, shutil, hashlib

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RAK = r"C:\Users\gspen\Videos\Buku"
EKAS = os.path.join(RAK, "GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM")
R4DIR = os.path.join(EKAS, "03_SOURCE-VAULT", "R4_OEM-TECHNICAL")
QUEUE = os.path.join(EKAS, "02_REGISTERS", "INTAKE-QUEUE.csv")
JALANKAN = "--jalankan" in sys.argv

# laci → pola. Diperiksa berurutan; yang pertama cocok menang.
LACI = [
 ("TEST-EQUIPMENT", r"\bOTDR\b|light source|power meter|\bLSPM\b|\bmegger\b|insulation tester|"
  r"earth tester|clamp meter|multimeter|thermal imager|analy[sz]er|calibrator|test set"),
 ("GENSET", r"generator set|\bgenset\b|diesel generator|alternator|engine[\s\-]driven|prime power|"
  r"standby rating"),
 ("UPS", r"\bUPS\b|uninterruptible|\bPDU\b|power distribution unit|power supply unit|\bPSU\b|"
  r"rectifier|\bbatter(y|ies)\b|\bVRLA\b|lithium ?ion|\bATS\b transfer switch"),
 ("VMS-NVR", r"\bNVR\b|\bDVR\b|\bVMS\b|video management|recorder|analysis server|"
  r"intelligent analysis|video server|central management|switcher|video encoder|"
  r"\bdecoder\b|video matrix|streaming (box|encoder)"),
 ("CAMERA", r"\bcamera\b|\bPTZ\b|\bdome\b|bullet camera|thermal imaging camera|dual[\s\-]spectrum|"
  r"image sensor|\blens\b|\bIPC\b|megapixel|face capture|\bANPR\b|\bLPR\b"),
 ("SERVER-STORAGE", r"\bSSD\b|\bNVMe\b|\bHDD\b|\bRAID\b|motherboard|\bGPU\b|graphics card|"
  r"\bCPU\b|edge computer|embedded computer|industrial computer|\bJetson\b|reComputer|"
  r"memory module|\bDIMM\b|workstation|rackmount"),
 ("NETWORK", r"\bswitch\b|\brouter\b|\bPoE\b|\bPBX\b|\bVoIP\b|\bSIP\b|intercom|\bAP\b|access point|"
  r"gateway|ethernet|\bLAN\b|firewall|media converter|transceiver|\bSFP\b"),
]

# yang jelas bukan dokumentasi produk walau tertandai R4
BUKAN_OEM = re.compile(
 r"tutorial|handbook|libgen|deanonymi|autocad|engineering documentation control", re.I)


def hashfile(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for blok in iter(lambda: f.read(1 << 20), b""):
            h.update(blok)
    return h.hexdigest()


def judul(p):
    """Kembalikan (daerah judul, teks penuh). Daerah judul jauh lebih menentukan:
    kata 'battery' di manual telepon adalah aksesori, bukan produknya."""
    try:
        import fitz
        d = fitz.open(p)
        t = "".join(d[i].get_text() for i in range(min(4, d.page_count)))
        d.close()
        return t[:1200], t[:8000]
    except Exception:
        return "", ""


def pilih_laci(kepala, penuh):
    """Skor: kecocokan di daerah judul bernilai 3x kecocokan di badan.
    Ambang 3 -> minimal satu kecocokan di judul, atau tiga di badan."""
    skor = []
    for nama, pola in LACI:
        dk = re.findall(pola, kepala, re.I)
        db = re.findall(pola, penuh, re.I)
        n = len(dk) * 3 + len(db)
        if n:
            contoh = (dk or db)[0]
            skor.append((n, nama, contoh if isinstance(contoh, str) else ""))
    if not skor:
        return None, ""
    skor.sort(key=lambda x: -x[0])
    n, nama, contoh = skor[0]
    if n < 3:
        return None, ""
    return nama, contoh.strip()


def main():
    ada = {}
    for r, d, bs in os.walk(os.path.join(EKAS, "03_SOURCE-VAULT")):
        for b in bs:
            if b.lower().endswith(".pdf"):
                ada[hashfile(os.path.join(r, b))] = b

    rows = [r for r in csv.DictReader(io.open(QUEUE, encoding="utf-8"))
            if r["r_level"] == "R4"]
    print("baris R4 di antrean :", len(rows))

    rencana, tolak, dup, gagal = [], [], [], []
    seen = {}
    for r in rows:
        p, nama = r["jalur"], r["nama"]
        if not os.path.exists(p):
            gagal.append(nama)
            continue
        if BUKAN_OEM.search(nama):
            tolak.append((nama, "bukan dokumen produk"))
            continue
        try:
            hh = hashfile(p)
        except Exception:
            gagal.append(nama)
            continue
        if hh in ada:
            dup.append((nama, "sudah di vault"))
            continue
        if hh in seen:
            dup.append((nama, "kembar dengan " + seen[hh][:40]))
            continue

        kepala, penuh = judul(p)
        nm = nama.replace("_", " ")
        laci, penanda = pilih_laci(nm + " \n" + kepala, nm + " \n" + penuh)
        if not laci:
            # Berkas hasil pindaian tanpa lapis teks tidak dapat dinilai mesin.
            # Ditahan, bukan dibuang — keputusannya milik manusia.
            laci = "_PERLU-DIPERIKSA"
            penanda = "tanpa lapis teks" if not penuh.strip() else "laci tidak jelas"
        seen[hh] = nama
        rencana.append((laci, p, nama, penanda))

    from collections import Counter
    c = Counter(x[0] for x in rencana)
    print("siap diserap        :", len(rencana))
    print("kembar / sudah ada  :", len(dup))
    print("ditolak             :", len(tolak))
    if gagal:
        print("tidak terbaca       :", len(gagal))
    print()
    for k in [x[0] for x in LACI] + ["_PERLU-DIPERIKSA"]:
        if c[k]:
            print("  %-18s %3d" % (k, c[k]))
    print()
    if tolak:
        print("ditolak:")
        for n, a in tolak[:12]:
            print("   %-60s  %s" % (n[:60], a))
    print()

    if not JALANKAN:
        print("=" * 60)
        print("UJI COBA — tidak ada berkas disalin.")
        print("Sungguhan:  python serap_r4.py --jalankan")
        return

    for laci, p, nama, penanda in rencana:
        d = os.path.join(R4DIR, laci)
        os.makedirs(d, exist_ok=True)
        shutil.copy2(p, os.path.join(d, nama))

    # bangun ulang _ISI.md tiap laci R4
    NL = chr(10)
    for k in [x[0] for x in LACI] + ["_PERLU-DIPERIKSA"]:
        d = os.path.join(R4DIR, k)
        if not os.path.isdir(d):
            continue
        bs = sorted(b for b in os.listdir(d) if b.lower().endswith(".pdf"))
        baris = NL.join("| `%s` | %.1f MB |" % (b, os.path.getsize(os.path.join(d, b)) / 1048576.0)
                        for b in bs)
        io.open(os.path.join(d, "_ISI.md"), "w", encoding="utf-8").write(
            u"# Isi laci — `R4_OEM-TECHNICAL/%s`" % k + NL * 2 +
            u"**%d berkas.**" % len(bs) + NL * 2 +
            u"> **R4 melekat pada produk dan versi tertentu.** Sebelum angka dari sini masuk" + NL +
            u"> dokumen serah, pastikan **model dan versi firmware** yang dikutip sama dengan" + NL +
            u"> yang benar-benar terpasang. Lembar data produk lain tidak berlaku." + NL * 2 +
            u"| Berkas | Ukuran |" + NL + u"|---|---|" + NL + baris + NL)

    print("SELESAI. %d berkas diserap ke %d laci." % (len(rencana), len([k for k in c if c[k]])))
    print("Langkah berikutnya: perbarui MASTER-REFERENCE-REGISTER.csv dan kartu yang")
    print("berstatus MENUNGGU R4 pada rantai jaminan.")


if __name__ == "__main__":
    main()
