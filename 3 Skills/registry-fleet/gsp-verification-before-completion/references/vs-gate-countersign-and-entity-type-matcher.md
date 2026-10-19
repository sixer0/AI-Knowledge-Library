# VS-Gate + Countersign Audit + Entity-Type Matcher (2026-10-04, DEMS-VSAT F2-F4/VS/CSX)

Lanjutan `merge-layer-audit-and-compressed-matcher.md` (§6-7 di sana). File ini
menambah teknik terukur dari giliran audit lajur F2-F4, MRG-F2/F3, DELTA-MRG,
MRG-ALL, VS, dan CSX.

## 8. Entity-match level TUBUH halaman menipu; uji TIPE-ENTITAS di judul/OG
Kasus nyata dua arah:
- Positif-palsu tokenizer pengawas: nama pendek (TOA, LS, Sil) atau umlaut
  (Brähler) tak kena regex `[A-Za-z]{4,}` -> kandidat palsu; cek kolom `brand`
  dan path URL dulu sebelum menuduh.
- NEGATIF-PALSU yang mahal: `eschenbach-group.com` memuat 286 token
  "eschenbach" -> lolos grep-token pengawas, padahal judul halaman
  "Zelthersteller & Zeltbau" = PABRIKAN TENDA Eschenbach, beda entitas dengan
  ESCHENBACK electronic (alat ukur). Tabrakan nama BEDA-INDUSTRI (bukan cuma
  lintas-negara seperti BDCOM). Penangkapnya: VS yang membandingkan JUDUL-vs-
  entitas-klaim, lalu CSX konfirmasi via fetch hidup.
RESEP audit baris ber-URL: jangan berhenti di `grep -c token page.html`; tarik
`<title>`/og_title dan cocokkan DESKRIPSI USAHA-nya vs item_code baris.
Kandidat sah pola induk-merek (Ubiquiti@ui.com, Harman@dbxpro, Octave@qognify,
d&b@dbaudio, Schneider@se.com, AVM@fritz.com) punya merek di judul; tabrakan
nama punya judul dengan TIPE USAHA beda. Rename korporat juga sah dan
terbukti via judul (AnyVision->Oosto: judul "| Oosto" + 382 token).

## 9. Deteksi BARIS KONSOLIDAT (multi-entitas dalam satu sel) sebelum merge
Sel vendor_name berisi >=3 nama dipisah ' / ' ("Redington / Innova / ... /
Compuage") merusak kunci dedup merge DAN audit entity-match per-baris. Probe:
`[r for r in rows if r['vendor_name'].count(' / ') >= 2]`. Vonis pengawas:
merge DITAHAN sampai dipecah. Preseden eksekusi benar: MRG-ALL `split_log`
(L16-F4-089 -> S01..S09 satu baris per entitas, terverifikasi grep per-id).
Beda dengan baris konsolidat: catatan "distributor tier-1" satu entitas = ok.

## 10. Kalibrasi TIER lintas-lajur = prasyarat bandingkan angka di hilir
Satu fokus, anggaran sama: L17-F4 TRUSTED=0 vs L16-F4 TRUSTED=51. Sebabnya
campuran urutan kerja (UPS/switch punya situs korporat mapan; kabel RoW =
etalase dagang) + gerbang TRUSTED tiap lajur tidak identik. Konsekuensi untuk
VS/MRG-ALL: angka tier mentah antar fokus TIDAK sebanding; wajib satu kriteria
kanonis + rekalkulasi, bukan terima vonis lajur. Naikkan jadi SYARAT EKSPLISIT
gerbang fix bila countersign mengulang temuan (kasus: CSX menuntut controller
menetapkan SATU kriteria TRUSTED sebelum kartu fix, karena daftar 13+3+60 tak
bisa ditambal seragam tanpa aturan tunggal).

## 11. Audit gerbang VS (verifikasi rilis 100% populasi) - ukur instrumen, bukan vonis
Artefak wajib ada + terukur: (a) DUA RUN identik-byte (sha256 run1==run2,
ukur sendiri); (b) SEED-LOG append-only dengan seed tercatat + grep-silang
anti-tabrakan vs seed misi lain; (c) fase fetch->cache beku->check TANPA
jaringan (cache_*.jsonl berukuran nyata); (d) cakupan = SELURUH populasi untuk
entity-match, seeded-sample untuk liveness (persentase tercetak); (e) override
mekanik harus NAMED + deterministik di instrumen (bukan penghapusan temuan);
(f) tabel VERIFIKASI-AKURASI menempel. VERDICT FAIL = gerbang BEKERJA - jangan
dibaca sebagai kegagalan verifier. XLS/DGB ditahan sampai run hijau.

## 12. Audit CSX (countersign) - uji INDEPENDENSI, bukan setuju/tidak
Checklist ukur: (1) seed countersign BEDA dari VS (20261005 vs 20261004);
(2) sampel KOMPLEMEN (URL di luar cache VS); (3) rekalkulasi PIVOT dengan kode
ditulis dari nol (bukan import instrumen VS); (4) regenerasi VONIS == resmi
BYTE-EXACT setelah normalisasi CRLF->LF - satu-satunya beda boleh baris
`written <path>` dan itu harus dibukukan jujur; (5) PIN SHA: sha256 VONIS/objek
diukur ulang pengawas sendiri vs yang dikutip laporan = bukti objek tidak
bermutasi; (6) countersigner menemukan bug ALATNYA SENDIRI lalu menulis skrip
koreksi terpisah TANPA menyentuh artefak objek = patuh kontrak NO-fixes, bukan
cacat. AGREE tanpa salah satu bukti ini = stempel, tagih.

## 13. Pertahanan aritmetika pengawas sendiri (anti-halusinasi dua arah)
"Selisih dedup 76 vs klaim 74" di MRG-ALL ternyata SALAH HITUNG pengawas
(lupa split +14 dan basis baca-MERGE-bukan-register-mentah). Sebelum menulis
tuduhan selisih: baca stats.json/laporan penuh (inputs_per_file, split_log,
collapse) dan cocokkan rantai aritmetika. Bila khilaf, koreksi TERBUKA di
kartu + kontrak. Aturan sama berlaku bolak-balik: vonis lajur harus = cetakan
register (episode TRUSTED 9-vs-8 L02-F1), dan klaim pekerja ("27 terpenuhi")
ditagih jejak berkasnya sebelum dipercaya maupun dituduh.

## 14. Tagihan pengawas butuh REGISTER, bukan memori giliran
Tiga tagihan (resolusi kmhq via render, audit origin asing per-baris, jejak
angka "27") lolos dari instrumen VS DAN CSX (grep = 0 di semua artefaknya).
Pola gagal: tagihan hidup di komentar kartu + kontrak, tapi hilir hanya
menjalankan CHECK yang terkodifikasi di instrumennya sendiri. Perbaikan untuk
misi berikutnya: salin SEMUA tagihan lintas-fase ke SATU berkas register
(tagihan.md / baris kontrak ber-id) dan wajibkan gerbang hilir mencentang
per-id ATAU mencatat putusan BUANG resmi - tagihan tidak boleh mati diam.

## 15. Delta pass = satu-satunya tambalan murah yang terus ditunda
Sepanjang malam gerbang basi (MERGE-F1 22:35 vs L06 59/L07 73) ditagih belasan
kali sebelum kartu DELTA lahir; begitu lahir, loop tertutup dalam satu giliran
dan MRG-ALL membacanya benar. Preseden urutan sehat: DELTA-<lajur> -> MRG-ALL
-> VS. Pengawas: ukur mtime merge vs mtime register tiap lajur sumber di SETIAP
giliran audit merge; `grep <ID-LAJUR> merge.tsv` = 0 berarti basi. Setelah
delta, verifikasi serapan per-lajur (L06=59/59, L07=73/73) bukan hanya total.

## 16. Deteksi delimiter per lajur + pitfall hitung papan
Register lajur boleh ber-delimiter PIPA walau berekstensi .tsv (kasus L01-F1,
L11-F3, L15-F4) - parser wajib deteksi dari baris header, bukan hardcode TAB.
Merge sehat menormalkan ke TAB (terverifikasi di MRG-F1/F3/ALL). Hitung papan
per-misi: `workspace_path` di `kanban list --json` = worktree per-kartu,
filter path misi menghasilkan 0 palsu; yang benar grep teks output `kanban
list` atas tag [TENANT] kartu.
