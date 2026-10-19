# -*- coding: utf-8 -*-
"""
Membangun Engineering-Knowledge-Assurance-System.zip

Menyusun ulang seluruh rak (batch 1 + batch 2) menurut RANTAI JAMINAN —
rujukan → keputusan desain → perhitungan → pengujian → bukti serah terima —
dengan setiap sumber bertanda tingkat keyakinan R1–R5.

Jalankan:  python "C:/Users/gspen/Videos/Buku/_tools/buat_paket_ekas.py"
"""
import io, os, re, zipfile, hashlib

RAK = r"C:\Users\gspen\Videos\Buku"
SKILLS = r"C:\Users\gspen\.claude\skills"
OUT = os.path.join(RAK, "Engineering-Knowledge-Assurance-System.zip")

SKILL_LIST = ["pustaka-teknis", "rcm-analysis", "fiber-link-design",
              "power-backup-sizing", "grounding-lightning-design"]

# Buku yang dipakai untuk hitungan (R3-H) vs kerangka berpikir (R3-K)
R3_HITUNG = {
    "CCTV From Light to Pixels", "FOA Reference Guide to Fiber Optics",
    "Reference Guide to Fiber Optic Testing Vol 1", "Grounds for Grounding",
    "The Art and Science of Lightning Protection",
    "Electrical Power Equipment Maintenance and Testing", "RCM II (John Moubray)",
    "Battery Reference Book", "Uninterruptible Power Supplies and Active Filters",
    "Diesel Generator Handbook", "Storage Networks Explained",
    "TCP-IP Illustrated Vol 1", "Infrared Thermal Imaging",
    "Shigley's Mechanical Engineering Design",
}


def tingkat(relpath):
    """Tentukan tingkat R dari lokasi berkas resume."""
    if "_standar" in relpath:
        return "R2"
    if "_tesis" in relpath or "_panduan" in relpath:
        return "R5"
    return "R3"


def kumpulkan_resume():
    hasil = []
    for akar, dirs, berkas in os.walk(RAK):
        dirs[:] = [d for d in dirs if d not in ("_tools", "_sistem", "_koleksi-lain")]
        for b in berkas:
            if not b.startswith("RESUME") or not b.endswith(".md"):
                continue
            penuh = os.path.join(akar, b)
            rel = os.path.relpath(penuh, RAK)
            folder = rel.split(os.sep)[0]
            judul = re.sub(r"^RESUME(\s+(STANDAR|TESIS|PANDUAN))?\s*-\s*", "", b[:-3])
            R = tingkat(rel)
            if R == "R3":
                sub = "R3-hitungan" if judul in R3_HITUNG else "R3-kerangka"
            elif R == "R2":
                sub = "R2-standar"
            else:
                sub = "R5-sekunder"
            hasil.append((penuh, u"02-rujukan/%s/%s - %s.md" % (sub, folder, judul)))
    return sorted(hasil, key=lambda x: x[1])


README = u"""# Engineering Knowledge & Assurance System (EKAS)

**PT Gemilang Satria Perkasa** · Dibangun 20 Agustus 2026
Rak sumber: `C:\\Users\\gspen\\Videos\\Buku` · 24 folder topik · 20.791 halaman

---

## Apa yang berubah dari "perpustakaan teknis"

Perpustakaan menjawab **"di buku mana?"**.
Sistem ini menjawab **"bagaimana angka ini sampai ke berita acara, dan apakah ia bertahan
saat diperiksa?"**

Isinya sebagian besar sama. **Arahnya yang berbeda.** Perpustakaan disusun menurut buku;
sistem ini disusun menurut **rantai jaminan** — dan sebuah rujukan dianggap belum berguna
sampai rantainya sampai ke ujung.

```
①  RUJUKAN  →  ②  KEPUTUSAN  →  ③  HITUNGAN  →  ④  UJI  →  ⑤  BUKTI SERAH
   [R1–R5]      desain           + asumsi        + ambang    berita acara
```

Dua hal ditambahkan yang tidak ada pada perpustakaan:

1. **Tingkat keyakinan rujukan R1–R5** — melekat pada setiap sumber, menentukan **untuk apa
   angka itu boleh dipakai**. Ambang serah terima menuntut R1/R2; angka produk menuntut R4;
   penalaran boleh R3.
2. **Delapan rantai jaminan** — satu per domain, lengkap dari rujukan sampai lampiran
   berita acara, termasuk **rantai yang sengaja diterbitkan dalam keadaan putus**.

---

## Peta isi

| Map | Isi | Mulai dari sini bila… |
|---|---|---|
| `00-sistem/` | Definisi R1–R5, register seluruh sumber, rantai jaminan, kartu kendali | …Anda baru pertama memakai sistem ini |
| `01-rantai-jaminan/` | **8 rantai lengkap** ①→⑤ per domain | …Anda sedang mengerjakan proyek nyata |
| `02-rujukan/` | 30 resume, **terkelompok menurut tingkat R** | …Anda mencari isi sebuah buku |
| `03-hitungan/` | Katalog rumus induk — pertanyaan → rumus → halaman | …Anda butuh rumusnya saja |
| `04-pengujian-bukti/` | Kerangka 8 jenis berita acara + sumber ambang | …Anda sedang menyusun dokumen serah |
| `05-tata-kelola/` | Asumsi baku, peta celah, daftar pengadaan, prosedur, riwayat | …Anda mengelola raknya |
| `06-skill/` | 5 skill operasional beserta berkas rujukannya | …Anda memakai model bahasa |
| `07-koleksi-lain/` | Indeks koleksi non-teknis | …Anda mencari makalah |

---

## Tingkat keyakinan rujukan

| | Jenis | Boleh menjadi ambang serah terima? |
|---|---|---|
| **R1** | Regulasi / SNI / standar normatif nasional | ✅ **ya — mengikat secara hukum** |
| **R2** | Standar internasional (IEC, IEEE, BS EN, ANSI/NETA) | ✅ ya, bila diadopsi kontrak |
| **R3** | Buku teks / handbook rekayasa | ⚠ hanya bila kontrak mengadopsinya tertulis |
| **R4** | Dokumentasi teknis pabrikan (OEM) | ✅ untuk angka yang melekat produk — **wajib** |
| **R5** | Sumber sekunder (tesis, makalah, panduan) | ❌ **tidak pernah** — penunjuk saja |

### Sebaran rak ini

```
R1  ░░░░░░░░░░░░░░░░░░░░  0      ← tidak ada dasar hukum Indonesia
R2  ███░░░░░░░░░░░░░░░░░  5
R3  ████████████████████  24     ← kekuatan rak
R4  ░░░░░░░░░░░░░░░░░░░░  0      ← selalu dari pabrikan, per proyek
R5  ██░░░░░░░░░░░░░░░░░░  3 + 21 makalah
```

**Rak ini kuat pada R3, cukup pada R2, kosong pada R1 dan R4.** Artinya GSP dapat merancang
dan menghitung dengan baik dari sini, dan dapat menetapkan ambang untuk lima jenis
pengujian — **tetapi tidak dapat menyatakan kepatuhan hukum Indonesia** dan **tidak dapat
menyebut angka produk** tanpa bahan dari luar.

Kedua kekosongan itu ditangani berbeda: **R4 tidak perlu diadakan** (diminta per proyek dari
pabrikan), sedangkan **R1 perlu diadakan** dan ada di urutan teratas daftar pengadaan.

---

## Status delapan rantai

| Rantai | Domain | Sumber ambang | Status |
|---|---|---|---|
| **A** | Serat optik | Hitungan rancangan + IEC 61280-4-2 **[R2]** | ✅ utuh |
| **B** | Video pengawasan | Sasaran pemilik + BS EN 62676-1-2 **[R2]** | ✅ utuh / bergantung pemilik |
| **C** | Catu daya & baterai | IEEE 1188 + IEC 62485-2 **[R2]** | ✅ utuh / menunggu **R4** |
| **D** | Pembumian & petir | — | ⚠ **PUTUS di mata ④** |
| **E** | Uji tahanan isolasi | ANSI/NETA ATS-2017 **[R2]** | ✅ **utuh — terkuat** |
| **F** | Termografi | ANSI/NETA Tabel 100.18 **[R2]** | ✅ utuh |
| **G** | Keandalan & pemeliharaan | Hitungan RCM **[R3]** | ⚠ perlu adopsi kontrak |
| **H** | Penyimpanan & jaringan | Hitungan rancangan | ⚠ tanpa sandaran normatif |

**Rantai D diterbitkan dalam keadaan putus dengan sengaja.** Tidak ada sumber sah untuk
ambang resistansi pembumian di rak ini, dan menyamarkannya akan lebih berbahaya daripada
menyatakannya. Berkasnya memuat **tiga jalan sah** untuk menutupnya per proyek.

---

## Cara memakai pada pekerjaan nyata

1. Buka **rantai domainnya** di `01-rantai-jaminan/` — bukan bukunya.
2. Isi **kartu kendali** (`00-sistem/04-KARTU-KENDALI.md`) untuk tiap besaran yang akan
   masuk dokumen serah.
3. Tandai kartu **"menunggu R4"** dan kirim permintaan data ke pabrikan **di awal proyek** —
   ini penghambat paling umum menjelang serah terima.
4. Periksa **mata ④**: apakah ambangnya punya sumber sah? Bila R3, apakah kontrak
   mengadopsinya secara tertulis?
5. Susun berita acara dari `04-pengujian-bukti/`.
6. **Simpan kartu kendali bersama berita acara.** Kartu itu yang menjawab pemeriksa tanpa
   membongkar ulang perhitungan.

---

## Yang membuat sistem ini berguna

Tiga pernyataan berikut hanya mungkin ditulis karena sistem ini ada — dan ketiganya
**memperkuat** dokumen, bukan melemahkannya:

> *"Ambang uji tahanan isolasi pada pekerjaan ini bersandar pada standar internasional
> [R2], bukan pada penilaian pelaksana."*

> *"Faktor derating genset belum dapat ditetapkan sampai surat pabrikan diterima; angka
> sementara dipakai hanya untuk kajian kepekaan, tidak untuk ambang terima."*

> *"Ambang resistansi pembumian belum memiliki sandaran normatif dan harus ditetapkan
> pemilik sistem secara tertulis."*

Dokumen yang menyatakan batasnya lebih sulit dipatahkan daripada dokumen yang
menyamarkannya — karena tidak ada lagi yang tersisa untuk ditemukan pemeriksa.

---

## Batas yang harus diketahui pemakai

- **Seluruh nomor halaman merujuk halaman PDF**, bukan halaman cetak, kecuali dinyatakan
  keduanya. Empat buku punya selisih tetap dan boleh dikutip dua-duanya; selebihnya PDF saja.
- **Diesel Generator Handbook kehilangan ± 55 halaman** (Bab 11 seluruhnya — emergency &
  standby). Materinya tidak tersedia.
- **Tiga buku catu daya terbit 2000–2004.** Kerangka hitungnya sahih; angka produknya tidak.
- Rincian cacat berkas dan selisih halaman: `06-skill/pustaka-teknis/references/03-batas-dan-celah.md`
"""


def main():
    isi = []  # (path sumber, nama dalam zip)

    # 00 — sistem
    for nama in ["01-TINGKAT-KEYAKINAN-RUJUKAN.md", "02-REGISTER-RUJUKAN.md",
                 "03-RANTAI-JAMINAN.md", "04-KARTU-KENDALI.md"]:
        isi.append((os.path.join(RAK, "_sistem", nama), "00-sistem/" + nama))

    # 01 — rantai
    rantai_dir = os.path.join(RAK, "_sistem", "rantai")
    for nama in sorted(os.listdir(rantai_dir)):
        isi.append((os.path.join(rantai_dir, nama), "01-rantai-jaminan/" + nama))

    # 02 — rujukan
    isi.extend(kumpulkan_resume())

    # 03 / 04 / 05
    isi.append((os.path.join(RAK, "KATALOG-RUMUS.md"), "03-hitungan/KATALOG-RUMUS.md"))
    isi.append((os.path.join(RAK, "TEMPLATE-BERITA-ACARA.md"),
                "04-pengujian-bukti/TEMPLATE-BERITA-ACARA.md"))
    for nama in ["ASUMSI-BAKU.md", "PETA-CELAH-KOLEKSI.md", "DAFTAR-PENGADAAN-BAHAN.md",
                 "PROSEDUR-TAMBAH-BUKU.md", "RENCANA-KERJA.md"]:
        isi.append((os.path.join(RAK, nama), "05-tata-kelola/" + nama))

    # 06 — skill
    for s in SKILL_LIST:
        base = os.path.join(SKILLS, s)
        isi.append((os.path.join(base, "SKILL.md"), "06-skill/%s/SKILL.md" % s))
        refdir = os.path.join(base, "references")
        if os.path.isdir(refdir):
            for nama in sorted(os.listdir(refdir)):
                if nama.endswith(".md"):
                    isi.append((os.path.join(refdir, nama),
                                "06-skill/%s/references/%s" % (s, nama)))

    # 07 — koleksi lain
    isi.append((os.path.join(RAK, "_koleksi-lain", "README.md"),
                "07-koleksi-lain/README.md"))
    isi.append((os.path.join(RAK, "_koleksi-lain", "Makalah IEEE", "INDEKS-MAKALAH.md"),
                "07-koleksi-lain/INDEKS-MAKALAH.md"))

    hilang = [s for s, _ in isi if not os.path.exists(s)]
    if hilang:
        for h in hilang:
            print("HILANG:", h)
        raise SystemExit("berhenti — sumber tidak lengkap")

    mentah = len(README.encode("utf-8"))
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("README.md", README)
        for src, dst in isi:
            data = io.open(src, encoding="utf-8").read()
            z.writestr(dst, data)
            mentah += len(data.encode("utf-8"))

    with zipfile.ZipFile(OUT) as z:
        rusak = z.testzip()
        nama = z.namelist()

    from collections import Counter
    c = Counter(n.split("/")[0] if "/" in n else "(akar)" for n in nama)

    print("keluaran   :", OUT)
    print("berkas     :", len(nama))
    print("mentah     : %.1f KB" % (mentah / 1024))
    print("terkompresi: %.1f KB" % (os.path.getsize(OUT) / 1024))
    print("integritas :", "OK" if rusak is None else "RUSAK: " + rusak)
    print("sha256     :", hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:16])
    print()
    for k in sorted(c):
        print("  %-20s %3d berkas" % (k, c[k]))
    print()
    for sub in ["R2-standar", "R3-hitungan", "R3-kerangka", "R5-sekunder"]:
        n = sum(1 for x in nama if "/" + sub + "/" in x)
        print("  rujukan %-14s %3d" % (sub, n))


if __name__ == "__main__":
    main()
