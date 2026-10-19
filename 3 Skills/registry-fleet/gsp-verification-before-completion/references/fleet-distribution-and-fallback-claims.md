# Verifikasi Klaim Distribusi Fleet & Fallback Senyap (preseden WK-ORCH-0911, 11-09-2026)

Dua kelas klaim pekerja yang sering lolos short-check tapi menipu bila dipercaya
bulat: (A) "didistribusikan ke SEMUA profil" dan (B) "fallback-en senyap terbukti".
Keduanya punya resep uji ulang independen yang murah (detik, lokal).

## A. Klaim distribusi berkas skill/skrip ke banyak profil (kartu DIST)

Klaim bentuk "N berkas di M profil, hash sama kanonik" WAJIB diukur ulang controller
sebelum naik ke laporan user. Resep:

```bash
# 1. Bangun populasi penerima dari find atas SELURUH pohon profil, bukan glob flat.
#    Letak salinan bervariasi: profil ada yang flat skills/<skill>/scripts/ dan ada
#    yang berkategori skills/gsp/<skill>/scripts/ (mis. gsp-explore). Glob flat
#    Undercount = vonis salah.
find "$LOCALAPPDATA/hermes/profiles" -name "lad_card.py" | wc -l
find "$LOCALAPPDATA/hermes/profiles" -name "lad_card.py" \
  | sed 's|.*profiles/||; s|/.*||' | sort | uniq -c   # daftar penerima per profil

# 2. Marker fungsional per salinan (bukan hanya nama berkas):
c=0; m=0
for f in $(find "$LOCALAPPDATA/hermes/profiles" -name "lad_card.py"); do
  c=$((c+1)); grep -q -- "--wake-default" "$f" && m=$((m+1))
done; echo "salinan=$c punya-marker=$m"

# 3. Hash sampel vs kanonik (prefix sha256 cukup untuk konsistensi):
sha256sum "$LOCALAPPDATA/hermes/skills/gsp/<skill>/scripts/<file>" \
          $(find "$LOCALAPPDATA/hermes/profiles" -name "<file>" | head -3)
```

Pitfall terukur 11-09: `grep -l "WAKE: blok"` mengembalikan 0 padahal distribusi sah —
string marker tebakan tidak ada di berkas. Uji marker dengan token yang PASTI ada
(baca dulu salinan kanonik, kutip string literalnya), atau pakai flag CLI (`--wake-default`).
Hash prefix lewat `sha256sum | awk '{print substr($1,1,10)}'` bisa menipu bila baris
output mengandung spasi/escape MSYS — bandingkan hash kanonik dari python `hashlib`
dan cocokkan digitnya manual pada sampel.

Cocokkan TIGA angka sebelum setuju dengan klaim: jumlah berkas per jenis, jumlah profil
penerima, dan fraksi salinan bermarker. Klaim "26 berkas" = 13 x 2 jenis berkas;
pecahan per jenis harus terbukti terpisah (13 + 13), bukan total buta.

## B. Klaim "fallback senyap terverifikasi" (predikat CS-9 kelas i18n)

Bila pekerja menutup celah bukan dengan menulis semua target (mis. 16 locale) tapi
dengan MEMBUKTIKAN mekanisme fallback, bukti sah butuh dua lapis plus kontrol:

1. **Lapis kode**: kutip baris loader yang melakukan fallback (path + nomor baris,
   mis. `agent/i18n.py:254-256` nilai None -> katalog en -> raw key).
2. **Lapis runtime**: probe yang memanggil fungsi nyata untuk SEMUA varian (semua
   locale), mencatat resolve tiap varian + hitung rawkey = 0.
3. **Kontrol pembeda (WAJIB)**: minimal satu varian yang HARUS tampil jalur berbeda
   (mis. satu locale yang memang punya terjemahan sendiri = TERJEMAH, sisanya
   FALLBACK-EN). Tanpa kontrol, probe seragam-hijau tidak membuktikan apa pun —
   dia tidak bisa membedakan "fallback bekerja" dari "probe buta".

Predikat (`fallback-terverifikasi`) dicatat di register JSON kecil di folder kontrak:
isi = berkas+baris bukti loader, path skrip probe, tanggal bukti, kartu pemilik.
Vonis akhir tetap di kartu VERIF (penulis bukan verifikator): VERIF menjalankan ulang
skrip gerbang luas (exit 0) dan menguji predikat terhadap register.

## C. Penanganan notifikasi status kanban otomatis

Notifikasi `[kanban] Task ... completed` = INPUT STATUS, bukan perintah dekomposisi.
Urutan sah controller: (1) `show` kartu + dump `list --json` board untuk melihat DAG
tenant (jangan buat kartu/grafik ulang); (2) ukur ulang klaim result dengan resep A/B
di atas sesuai kelas klaim; (3) laporkan level klaim sebenarnya (L1 vs L2) + kondisi
titipan sebagai komentar ke kartu verifier hilir, bukan sebagai kartu baru.
Pitfall alat: `hermes kanban show <id>` mencetak TEKS MANUSIA (bukan JSON) meski
di-redirect ke berkas — `json.load` gagal `Expecting value: line 1 column 1`. Pakai
`show <id> --json` atau parse teks; `list --json` baru JSON utuh.
