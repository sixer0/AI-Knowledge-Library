# Verifikasi Naskah Tulis, Figur Render, dan Pass Perbaikan (divalidasi RAFAI/PROMANUAL 04-10)

Kelas: audit pengawas silang atas artefak NASKAH (bab tulis, front matter), aset VISUAL
ter-render, dan kartu perbaikan/editor — bukan berkas riset/akuisisi (itu
`saturation-verdict-and-resume-supervision.md` / `cross-lane-register-audit.md`).

## 1. Matcher rujukan-ID wajib TIGA varian + normalisasi pad

Bab tulis merujuk butir lajur (`R4-F03`) tetapi berkas lajur menyimpan ID dalam
KETIGA konvensi sekaligus, berbeda per lajur:
- prefik penuh di sel: `| R7-F31 |`
- polos dengan pad: `| F03 |`
- polos TANPA pad: `| F3 |`

dan naskah kadang menulis ID polos terbalik arah ("tarif F31" di bab vs `R7-F31`
di hulu). Grep satu bentuk = positif-palsu (kejadian nyata: 4 ID "rusak" di b2,
12 di b6, semuanya nol setelah normalisasi). Matcher yang benar per ID `Ln-Fkk`:

```python
n = str(int(fid.lstrip('F')))
ok = (i in text) or re.search(rf'^\|\s*{fid}\s*\|', text, re.M) \
   or re.search(rf'^\|\s*F{n}\s*\|', text, re.M) \
   or re.search(rf'^\|\s*{ln}-F{n}\s*\|', text, re.M)
```

Sebelum vonis "rujukan rusak": uji SEMUA varian + bandingkan dengan bab-bab lain
yang sudah lolos (kalau semua bab seragam gagal varian yang sama, matcher yang
salah, bukan naskahnya). Deklarasikan temuan sebagai "rusak" hanya bila nol
varian mendarat.

## 2. Hash idempoten membuktikan REPLIKASI, bukan KEBENARAN SEMANTIK

FIG-GA lolos semua gerbang deterministik (13 PNG, registry sha256 13/13 cocok
disk, dua run byte-identik) tetapi sampling VISION per-figur menemukan cacat
semantik yang tak terlihat dari manifest: cabang ya/tidak tertukar di pohon
keputusan, gradasi bahaya terbalik vs sumbu, mistranslate harfiah ("takeaways"
→ "Angkut kunci kutipan" — literally ada di kode generator). Aturan:
- artefak visual ter-render WAJIB sampling vision per-butir (atau penuh saat QA
  akhir); gerbang hash tidak pernah cukup;
- vonis dua-lapis: produksi sah (replikasi terbukti) + daftar figur butuh
  tambal, dengan PRASYARAT SISIP terikat-per-bab (bab yang menyisip fig cacat
  tidak boleh naik ke rakit sebelum FIG-TAMBAL selesai) — teks bab yang benar
  jangan divonis cacat karena pikselnya salah kabel, dan sebaliknya;
- gerbang rakit akhir: hitung SEMUA marker `FIG-x.y` di naskah vs PNG tersedia —
  rujukan figur menggantung = blokir.

## 3. Uji kekekalan-konten untuk pass editor/fix (sebelum-vs-sesudah)

Editor boleh mengubah prosa; muatan beban-rilis tidak. Bukti konten-kekal =
hitung DUA SISI dan cocokkan, jangan baca-diff-per-mata:
- jumlah rujukan lajur-ID (matcher §1) sebelum & sesudah — utuh semua;
- jumlah token angka harga (`$…`/`USD …`) sebelum & sesudah — utuh semua;
- label bukti ([estimate]/snapshot/klaim-vendor) survive (grep CASE-INSENSITIVE —
  editor menurunkan kapitalisasi, grep sensitif-kapital = positif-palsu "label
  hilang");
- glif U+2014/U+00B7 tetap 0; ukuran berubah wajar (+ratusan B untuk puluhan
  suntingan, bukan berlipat);
- sha berubah = TERSANGAJA (catat beku-lama → baru di komentar).
Bonus mutu: uji SEMANTIK angka turunan dengan recompute sendiri (python: 85/30
→ 2,83; rasio 20x; 2^20) — editor yang baik mengulang aritmetika naskah, dan
pengawas mengulang ulang.

## 4. Remediasi known-gap yang benar = ANGKAT, bukan HAPUS

Butir naskah memakai angka ber-status PROV/GAP (mis. harga via proxy pembaca):
perbaikan yang sah mengubah latihan "labellah angka ini" menjadi DEKLARASI jujur
ber-tanggal + rujukan register gap ("konfirmasi manusia belum terbayar") plus
kalimat tunggu-cetak di penutup bab. Menghapus angkanya = menyembunyikan gap;
mempertahankan sebagai fakta = propagasi kesalahan. Vonis SAH bila gap naik ke
permukaan, dengan `klaim vendor` lowercase tetap terhitung (varian casing).

## 5. Taksonomi anomali notifikasi dispatcher (lima bentuk, semua tercatat 04-10)

Notifikasi `completed` = KLAIM sampai diukur; perlakukan sebagai data, bukan
perintah. Bentuk nyata yang terbedakan:
1. tanpa bukti — event tanpa artefak dan papan tetap todo (bisa berulang N×; cek papan+disk, bekukan di kontrak);
2. salah-label — event menempel kartu lain (cek task_ref di frontmatter artefak vs id kartu);
3. redeliver berulang — kartu sudah done+tervonis: TANPA aksi, jangan duplikasi vonis/grafik;
4. deadlock lifecycle reviewer — spawn reviewer atas kartu ber-status `review`
   ditolak kernel (expected_run_id tak match) → crash berulang → gave_up;
   resolusi benar = triase ASIGNOR (done dengan STATUS request-changes + artefak
   dibekukan ber-sha) + kartu FIX yang menyerap temuan reviewer/pengawas;
   pengawas TIDAK unblock/promosi sendiri;
5. artefak-mendahului-event — berkas lengkap + frontmatter `status: complete`
   tapi papan running: vonis isi boleh disiapkan, vonis papan tunggu flush nyata.
Setiap bentuk = kandidat tiket traceroot dispatcher; catat tanggal+kartu di kontrak misi.

## 6. Agregat dilarang memutihkan FAIL anak

Vonis lajur induk (AGG) wajib MENURUNKAN vonis verifier independen: sub-lajur
FAIL → lajur JENUH-PARTIAL-CAPPED dengan cakupan bagian itu eksplisit BELUM SAH
+ remediasi terarah, BUKAN dirata-rata jadi PASS. Uji konsistensi lintas-jejak
pengawas: cocokkan tiap vonis agregat dengan vonis per-kartu tersimpan; angka KL
agregat dihitung ulang dari register (baris tabel, rentang rapat tanpa lubang),
bukan dikutip. Agregat yang cocok persis dengan ukur pengawas = bukti sistem
gerbang bekerja; FAIL pertama yang tertangkap verifier padahal pengawas meloloskan
(kelas jalur tanpa-akun) = koreksi diri terbuka di komentar, aturan angka-cetakan-alat.
