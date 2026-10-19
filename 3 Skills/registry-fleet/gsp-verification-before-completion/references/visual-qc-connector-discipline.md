# Disiplin visus konektor figur (preseden RAFIF-MF-1009 09-10, dikukuhkan 10-10)

Sumber preseden terukur: G3.4, G5.3 (dua arah), G11.1 a0a144b8 - tiga kasus 'ilusi perioda dash' menimpa sensor manusia/visus model, dua di antaranya sensor controller. Klaim 'visus CLEAR' worker jatuh 3/3 di uji independen era pra-aturan; pasca-aturan enam-butir, klaim pekerja pertama bertahan (G3.4).

## Aturan wajib (semua kartu render/QC figur)

1. ENAM BUTIR TERTULIS per id, bukan ringkasan 'CLEAR':
   (a) nol segmen/ujung melayang; (b) tiap tepi satu kepala panah tepat di border tujuan, arah tunggal; (c) nol garis menumpang border > 3 mm dan nol dua-rel-sebuas-berimpit; (d) nol garis/border menembus glyph (teks di atas pola wajib plate knockout); (e) label utuh + jumlah label tepi == spek; (f) konten utuh vs spek/sidecar (elipsis sah hanya bila teks penuh di sidecar).
2. SEBELUM memvonis 'ujung melayang' WAJIB adjudikasi mekanis di SVG, bukan piksel saja:
   - ekstrak endpoint tiap path konektor (koordinat akhir 'M ... L ...');
   - uji terhadap border rect/polygon simpul dengan toleransi 0,6 mm;
   - bila celah visual == kelipatan perioda stroke-dasharray (mis. 7.1/1.6/0.2/1.6), itu UNSUR POLA, bukan putus;
   - laporkan koordinat sebagai bukti (contoh kanonis: gerbang teal G11.1 'M 117.33 95.25 ... L 42.67 76.2' - kedua ujung tepat di border Register/Plugin meski piksel tampak putus).
3. SEBELUM mengklaim atau menolak 'panah menempel border': sama, pakai koordinat endpoint vs rect - jangan percaya resolusi tampil.
4. Perbaikan lokal wajib diikuti AUDIT RUTE GLOBAL pada id yang disentuh (preseden G9.1: reparasi lane bus benar tapi membuka persimpangan-T melayang baru).
5. Gerbang mekanik (fontTools/K1-K10) adalah perlu-bukan-cukup: 'cacat 0' tidak memvonis LAYAK; vonis LAYAK hanya dari enam butir + adjudikasi mekanis butir 2-3.
6. Lineage byte pada artefak rakit diverifikasi lewat ZIP media-hash vs figuran/ (byte ber-vonis-merah = TOLAK; jangan percaya atribusi sidecar saja).
7. Koreksi vonis antar-sensor: vonis pengawas (L2) mengikat atas laporan pekerja; koreksi-diri ditulis sebagai jejak TERPISAH, bukan sunting komentar lama.

## Kelas cacat terdaftar (senjata visus enam butir) - per 10-10

K1 stub/konektor melayang; K2 panah orientasi salah/terbalik; K3 garis menumpang border; K4 teks menembus glyph / pita label vs border; K5 self-loop tak sengaja (asal==tujuan); K6 impit dua rel; arsir-latar-vs-teks (preseden G5.1 FG2S: teks di atas hatch wajib plate/halo); tabrakan marker-vs-anotasi chart (preseden G9.3: titik ulangan menimpa label angka - buta GG/GK, tertangkap crop piksel); tepi-kanvas terpotong (preseden G26.5/G27.1/G11.4/G12.1: dark-pixel >50 di baris/kolom tepi kanvas - buta bagi GG/GK/dua-run/cermin manifest; uji margin deterministik, pola sehat >=124 px/sisi); dempet-kolom (G12.2 era FG3B); border-dekoratif-vs-konektor (UJI-6, preseden G8.3 FG2T/FG2U: konektor memotong hairline offset kartu 'shadowed' tanpa knockout/z-order sah - gerbang-8 P1/P2 buta karena rect dekoratif tanpa data-node tak dikenali simpul); korup-sintaksis-marker (Kelas #7, preseden G18.1 FG4C: marker-end="u " - nilai url(#head-x) terpotong oleh transformasi rantai, arah aliran hilang TOTAL padahal GG/GK/UJI-6/dua-run/margin/cermin-semua-hijau; deteksi = regex sapuan SVG: setiap path konektor fill=none wajib marker-end="url(#nama)" yang menunjuk <marker id="nama"> terdefinisi; kalibrasi merah-hijau + kontrol populasi memisahkan satu id rusak dari 50 sehat).

## Kontrol merah-hijau instrumen

Setiap sensor baru (K7 celah<=1mm, K8 knockout-garis-milik-sendiri, K9 asosiasi label-edge, K10 tabrakan label-tepi vs teks-simpul, inset-wrap sisi miring, UJI-6 border-dekoratif z-order+knockout era RAFIF-REVB-1010, GERBANG-MARKER kelas #7) wajib dibuktikan dengan suntikan cacat yang FAIL sebelum dipakai menjatuhkan vonis hijau.

## Hierarki bukti saat sensor bertentangan (preseden FG2U + FG4C 10-10)

Saat visus full-page pengawas dan instrumen deterministik/geometri bertentangan pada kelas cacat geometris halus (persilangan garis-vs-border, knockout, z-order): hierarki = instrumen geometri deterministik + crop resolusi penuh TERARAH (pertanyaan per-titik, bukan per-kesan) MENANG atas kesan visus full-page. Visus tetap pemegang hak vonis LAYAK/TIDAK, tapi TUDUHAN PER-TITIK wajib naik banding ke dua alat itu sebelum ditulis sebagai vonis. Preseden terbalik juga sah: klaim 'visus CLEAR' worker jatuh di kontrol independen (era pra-aturan 3/3), dan visus full-page pengawas MEMBUKTIKAN diri benar pada kelas struktural-halus yang tak terlihat alat (G18.1 panah hilang: scan marker-end + crop sepakat, visus yang pertama kali menemukannya).

Dua arah kalibrasi wajib dicatat: sensor worker bisa lebih presisi dari mata pengawas (FG2U gate-6), dan sebaliknya (FG4C G18.1 - visus jatuh-vonis-pekerja 8/8 LAYAK). Aturan praktis: tiap tuduhan visus dipilah - yang bisa diuji deterministik WAJIB diuji dulu (marker-end regex, endpoint-vs-border, perioda dash); yang murni perseptif (keterbacaan, keseimbangan) cukup crop terarah; tuduhan yang gugur di banding DICORET dari vonis secara eksplisit (preseden stub teal G18.1 = ilusi dash).

## Register pin proteksi (pelajaran LF1 10-10)

Sebelum menuduh 'berkas luar cakupan bergeser' pada kartu sunting: baca pin dari VONIS TERBARU per berkas (kartu FIX/revisi sering menggeser pin pasca-peta awal). Register cetakan pertama = positif-palsu drift (preseden bab-07/08, pin era merah W2 vs byte FIX-W2).

## Determinisme lintas-versi perkakas (pelajaran FG3C 10-10)

Pin byte render TIDAK dijamin reproduktif lintas sesi/versi perkakas (estimator lebar pita knockout vs fontTools - preseden G12.2/G13.4 era FG3B tidak tereproduksi di run FG3C). Yang mengikat: byte yang divisus pada sesi penerbitan + laporan honest 'restage' dengan pin baru; jangan paksa pin lama kembali.

## Mata independen ketiga + gerbang permanen (pelajaran CSIGN v2.1 10-10/11)
Dua kelas cacat lolos DUA mata visus ronde-beruntun (VERIFR + REVERIF/QCV) dan baru tertangkap oleh countersign dengan akun beda dan seed populasi baru (4011): kliping baris kunci TENGAH KATA di tepi kanvas (G1.2) dan marker salah-orientasi di PANGKAL konektor plus gap ujung dashed (G19.2). Aturan:

- (1) populasi visus tiap ronde WAJIB diacak ulang dengan seed baru atas SELURUH raster, bukan hanya id yang dulu merah;
- (2) butir visus eksplisit: kata pada baris kunci utuh di KEDUA tepi kanvas, nol marker/kepala panah di pangkal sumber konektor, ujung tujuan menempel (celah = cacat);
- (3) tuduhan tabrakan label wajib menyebut SISI (border sumber vs tujuan) dengan koordinat - menimpa border tanpa sisi ambigu dan sering salah;
- (4) regresi struktur sajian (penghitung pasangan tabel/blok identik sepopulasi, target kembar=0) menjadi GERBANG PERMANEN tahap rakit, bukan tes sekali pakai - kelas blok-lipat-ganda terbukti warisan lintas-era (v2.0 dan v2.1 identik cacatnya) karena tidak pernah diujikan ulang oleh rantai perbaikan.
