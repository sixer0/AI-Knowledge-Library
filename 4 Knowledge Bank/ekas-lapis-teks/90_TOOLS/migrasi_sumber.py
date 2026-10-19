# -*- coding: utf-8 -*-
"""
Memindahkan berkas PDF sumber dari lokasi rak lama ke 03_SOURCE-VAULT/.

BAKU: uji coba (dry run) — tidak mengubah apa pun.
      python migrasi_sumber.py

JALANKAN SUNGGUHAN:
      python migrasi_sumber.py --jalankan

Alat ini memindahkan berkas, membangun ulang _ISI.md tiap laci, dan menulis
daftar berkas .md yang masih memuat jalur lama sehingga perlu disunting.

JALANKAN SAAT TIDAK ADA PEKERJAAN PROYEK BERJALAN.
"""
import io, os, sys, shutil, csv

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

RAK = r"C:\Users\gspen\Videos\Buku"
EKAS = os.path.join(RAK, "GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM")
VAULT = os.path.join(EKAS, "03_SOURCE-VAULT")
SKILLS = r"C:\Users\gspen\.claude\skills"

JALANKAN = "--jalankan" in sys.argv


def baca_manifest():
    """Kumpulkan rencana pindah dari _ISI.md tiap laci."""
    rencana = []
    for akar, dirs, berkas in os.walk(VAULT):
        if "_ISI.md" not in berkas:
            continue
        laci = os.path.relpath(akar, VAULT).replace("\\", "/")
        for baris in io.open(os.path.join(akar, "_ISI.md"), encoding="utf-8"):
            if not baris.startswith("| `"):
                continue
            sel = [s.strip() for s in baris.strip().strip("|").split("|")]
            if len(sel) != 3 or not sel[2].startswith("`"):
                continue
            nama = sel[0].strip("`")
            asal = sel[2].strip("`")
            rencana.append((laci, nama, asal))
    return rencana


def cari_rujukan_jalur(folder_lama):
    """Berkas .md mana saja yang menyebut folder rak lama."""
    kena = {}
    ruang = [RAK, SKILLS]
    for basis in ruang:
        for akar, dirs, berkas in os.walk(basis):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
            for b in berkas:
                if not b.endswith(".md"):
                    continue
                p = os.path.join(akar, b)
                try:
                    t = io.open(p, encoding="utf-8").read()
                except Exception:
                    continue
                hit = [f for f in folder_lama if f in t]
                if hit:
                    kena[p] = sorted(set(hit))
    return kena


def bangun_isi(laci, berkas_baru):
    d = os.path.join(VAULT, laci)
    baris = "\n".join(
        "| `%s` | %.1f MB |" % (n, os.path.getsize(os.path.join(d, n)) / 1048576.0)
        for n in sorted(berkas_baru))
    io.open(os.path.join(d, "_ISI.md"), "w", encoding="utf-8").write(u"""# Isi laci — `%s`

**%d berkas.** Berkas fisik **sudah berada di laci ini**.

| Berkas | Ukuran |
|---|---|
%s
""" % (laci, len(berkas_baru), baris))


def main():
    rencana = baca_manifest()
    if not rencana:
        print("Tidak ada rencana pindah. Jalankan bangun_ekas_struktur.py lebih dulu.")
        return

    folder_lama = sorted(set(a.split(os.sep)[0] for _, _, a in rencana))

    print("=" * 68)
    print("MIGRASI SUMBER  -  %s" % ("SUNGGUHAN" if JALANKAN else "UJI COBA (tidak mengubah apa pun)"))
    print("=" * 68)

    total = 0
    hilang = []
    per_laci = {}
    for laci, nama, asal in rencana:
        src = os.path.join(RAK, asal)
        if not os.path.exists(src):
            hilang.append(asal)
            continue
        total += os.path.getsize(src)
        per_laci.setdefault(laci, []).append((src, nama))

    print("\nBerkas siap pindah : %d  (%.0f MB)" % (
        sum(len(v) for v in per_laci.values()), total / 1048576.0))
    print("Laci tujuan        : %d" % len(per_laci))
    if hilang:
        print("\n⚠ TIDAK DITEMUKAN (%d):" % len(hilang))
        for h in hilang:
            print("   ", h)

    for laci in sorted(per_laci):
        print("\n  %s  (%d berkas)" % (laci, len(per_laci[laci])))
        for _, nama in sorted(per_laci[laci], key=lambda x: x[1]):
            print("      -", nama[:70])

    # rujukan yang akan putus
    kena = cari_rujukan_jalur(folder_lama)
    print("\n" + "-" * 68)
    print("BERKAS .md YANG MENYEBUT JALUR LAMA : %d" % len(kena))
    print("-" * 68)
    for p in sorted(kena):
        print("  %s" % os.path.relpath(p, os.path.dirname(RAK)))
        print("      menyebut:", ", ".join(kena[p])[:100])

    laporan = os.path.join(EKAS, "90_TOOLS", "LAPORAN-MIGRASI.csv")
    with io.open(laporan, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["berkas_md", "folder_lama_disebut"])
        for p in sorted(kena):
            w.writerow([p, " | ".join(kena[p])])
    print("\nDaftar lengkap ditulis ke: %s" % laporan)

    if not JALANKAN:
        print("\n" + "=" * 68)
        print("UJI COBA SELESAI — tidak ada berkas yang dipindahkan.")
        print("Untuk menjalankan sungguhan:  python migrasi_sumber.py --jalankan")
        print("=" * 68)
        return

    print("\nMemindahkan…")
    for laci in sorted(per_laci):
        d = os.path.join(VAULT, laci)
        os.makedirs(d, exist_ok=True)
        nama_baru = []
        for src, nama in per_laci[laci]:
            shutil.move(src, os.path.join(d, nama))
            nama_baru.append(nama)
        bangun_isi(laci, nama_baru)
        print("  %s : %d berkas" % (laci, len(nama_baru)))

    print("\nSELESAI. Berkas dipindahkan, _ISI.md dibangun ulang.")
    print("LANGKAH BERIKUTNYA — belum otomatis:")
    print("  1. Sunting %d berkas .md pada LAPORAN-MIGRASI.csv" % len(kena))
    print("     Ganti jalur lama menjadi 03_SOURCE-VAULT/<laci>/")
    print("  2. Perbarui 02_REGISTERS/MASTER-REFERENCE-REGISTER.csv kolom vault_path")
    print("  3. Catat di 00_START-HERE/CHANGELOG.md")


if __name__ == "__main__":
    main()
