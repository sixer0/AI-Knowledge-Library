# Kontrak Desain: anti-drift dari sumber desain (D-INT-11, preseden INT-EXPO-2026 RevC 06-09)

Kelas kegagalan: user meminta keluaran "mengikuti Template X" (mis. Template Hi-Tech
v1.1 untuk Dashboard Utama), tetapi artefak yang terbit menyimpang jauh dari anatomi
template, LOLOS semua gerbang verifikasi, dan baru tertangkap oleh mata user saat
telaah. Vonis user: artefak dicabut ("Hapus RevC dari data - Ini adalah kesalahan").

## Anatomis kegagalan (preseden nyata)
1. Blueprint TA mereduksi spesifikasi template secara diam-diam: DASHBOARD-KISI
   (kios komando 8 seksi bernomor: judul+ID/TIER/STATUS, kalimat situasi, kartu
   sasaran T-00 HARI + REL BUKTI, 6 tile ukuran U1-U6 + batang REPT + rujukan
   lembar/kolom, panel grafik+FILTER+tabel pendamping bers STATUS, panel batang
   top-10, panel status, panel mutu, state kosong, footer ORGANISASI/PROGRAM/SHA
   + jam + kotak cari + pil status) ditulis ulang jadi "daftar KPI + tabel" karangan
   sendiri. Controller mensahkan tanpa mencatatnya sebagai deviasi dari instruksi
   eksplisit user.
2. Sistem bahasa visual diganti lokal: pita peran baris 4 template (glif per gugus
   kolom: IDENTITAS, ■ SUMBER, ◈ TURUNAN, ƒ RUMUS HIDUP, △ INPUT, ✓ STATUS) diganti
   label kosakata baru per kolom. Saat user mengeluh "pita salah", controller
   menambal GEJALA (isi 32/32 kolom) dengan kosakata baru, bukan memulihkan SISTEM
   template. Terukur: 32/32 terisi, 0 mengandung glif peran.
3. Gerbang fidelity menguji hal yang salah: V1-V8 menguji angka/tautan/wrap/determinis
   terhadap SPEKS CONTROLLER, bukan terhadap sumber desain. Lebih fatal, V1 mencantumkan
   baris pita sebagai "delta yang diizinkan" - drift menjadi LULUS BERSERTIFIKAT.
   Ini ulangan penyakit D-INT-10 (gerbang acuan artefak antara) di domain desain.
4. Struktur lembar pendukung ikut hilang tanpa jejak: KARTU kehilangan seksi
   berkepala (RINGKASAN, BUCKET · BENTUK PRODUK, SKOR PRIORITAS · LAJUR, dst),
   breadcrumb, pil status, footer SHA, kotak cari kepala, jam hidup.

## RULE PERMANEN (mengikat semua misi 'mengikuti template/prototipe/exemplar')
R1. SEBELUM blueprint: dump struktur sumber desain (skrip read-only; contoh pola:
    scripts/dump_template.py -> template_dump.json berisi dims/freeze/colwidths/
    merged/isi baris per sheet). Blueprint WAJIB memuat KONTRAK-DESAIN: daftar butir
    anatomi template (lembar, seksi bernomor, token gaya, elemen wajib) dengan status
    per butir: PERSIS / ADAPTASI-alasan / DIBUANG-putusan-user. Tidak ada status
    diam-diam. Deviasi dari kata kerja eksplisit user ('mengikuti X') butuh putusan
    user tercatat di Decision Log, bukan persetujuan controller sendiri.
R2. SELAMA build: elemen kontrak yang berbiaya (batang, jam, pil) boleh diubah
    MEKANIKanya demi anti-lag (statis vs formula) tetapi BUKAN keberadaan dan
    bentuknya. Ganti sistem token (glif peran, palet, separator) = pelanggaran
    kontrak; pulihkan sistem sumber, jangan ciptakan padanan lokal.
R3. SEBELUM serah: verifier menguji KONTRAK-DESAIN BUTIR per BUTIR terhadap artefak
    akhir dengan predikat terukur (mis. 'baris 4 gugus N memuat glif ■/◈/ƒ sesuai
    dump', 'dashboard memuat seksi 01-08 dengan minimal isi X'). Daftar
    delta-terizinkan pada gerbang fidelity TIDAK boleh memuat elemen kontrak desain
    tanpa putusan user. Speks controller BUKAN alat ukur desain; sumber desain-lah
    alat ukurnya.
R4. KELUHAN VISUAL USER = sinyal tingkat vonis: "kok beda dengan template", "pita
    salah", "konteksnya drift" => berhenti menambal gejala; diff artefak vs sumber
    desain dulu, temukan elemen sistem yang hilang, pulihkan sistemnya. Laporan
    ketidakcocokan visual tidak pernah diselesaikan dengan kosakata baru.
R5. Jika user mencabut artefak: hapus dari SEMUA lokasi data (sisa file = 0 diverifikasi
    find), catat hash jejak (reports/...-DIHAPUS-HASH.txt), komentar REVOKE di kartu
    done, rilis resmi sebelumnya dikonfirmasi utuh (sha), pelajaran naik ke Decision
    Log + referensi ini. Jangan pembelaan; eksekusi + akar + tambal gerbang.

## Checklist cepat controller (tempel ke kartu BUILD dan VERIFY)
- [ ] Dump sumber desain ada dan dirujuk blueprint
- [ ] KONTRAK-DESAIN per-butir dengan status PERSIS/ADAPTASI/DIBUANG
- [ ] Tiap ADAPTASI/DIBUANG punya putusan user tercatat
- [ ] Uji verifier membaca artefak vs dump (bukan vs speks)
- [ ] Delta-terizinkan tidak menyentuh elemen kontrak
- [ ] Telaah visual mandiri controller sebelum SERAH (buka sheet kunci, bandingkan
      side-by-side dengan template: siapa yang hilang?)
