# Bab 08 - Bahaya radiasi elektromagnetik (EMR)

| Aspek | Isi |
|---|---|
| Sumber berkas | `IATG-05.60-Hazards-electromagnetic-radiation-IATG-V.3.pdf`, `V3_IATG-05.60_en.pdf` |
| Cakupan | 5 blok prosa dari partisi EX-C; 25 baris register (TERUKUR-DOKUMEN=24; TIDAK-ADA-DI-KORPUS=1). |
| Cara menelusur | Setiap angka membawa tanda `[R-n, dokumen, hal]` yang resolve ke `reg_id` pada `references/register.jsonl`. Penanda `DRAF INTERNAL GSP` berarti angka berasal dari draf internal dan bukan norma IATG/NATO. Penanda `nilai turunan` berarti angka dihitung dari baris register lain. Bab ini ikut batas kesegaran baseline yang dicatat di `references/batas-pengetahuan.md`. |


## Dasar kerentanan EID (IATG 05.60)

Bahaya EM muncul ketika kawat dalam medan RF membentuk bagian sirkuit EID dan level RF menginduksi daya/melebihi no-fire threshold (NFT). NFT didefinisikan sebagai daya yang menghasilkan probabilitas api 0,1 persen pada batas keyakinan satu sisi 95 persen, diterapkan lebih lama dari 10 konstanta waktu termal perangkat [R-08-0003, V3_IATG-05.60_en.pdf, hal 7]. Perangkat LV konstanta waktu panjang (10-50 ms, mis. bridge kawat gulung) sensitif terhadap rata-rata daya; perangkat film bridge dsb dengan konstanta waktu 1-100 mikrodetik sensitif pulsa tunggal [R-08-0022, V3_IATG-05.60_en.pdf, hal 15][R-08-0023, V3_IATG-05.60_en.pdf, hal 15]. Bahan bangunan umumnya tidak melindungi: tidak ada transmission loss di bawah 1 MHz, dan perlindungan refleksi jangan diasumsikan, sehingga kuat medan dalam bangunan dianggap sama dengan luar [R-08-0004, V3_IATG-05.60_en.pdf, hal 9].

## Batas jarak pemancar dan penyimpanan (IATG 05.60)

Hanya pemancar esensial yang boleh terpasang dalam ASA. Pemancar <=1 W dengan gain antena <=6 dB aman pada jarak >=10 m dari luar bangunan; <=10 W gain <=6 dB frekuensi >300 MHz aman pada >=5 m [R-08-0005, V3_IATG-05.60_en.pdf, hal 10][R-08-0006, V3_IATG-05.60_en.pdf, hal 10]. Dalam ASA, pemancar esensial <=25 W gain <=6 dB boleh pada jarak 3 m dengan kontrol kuat terjamin seumur transmitter [R-08-0007, V3_IATG-05.60_en.pdf, hal 10]. Penggunaan pemancar di dalam bangunan proses pada umumnya dilarang [R-08-0008, V3_IATG-05.60_en.pdf, hal 10]. Di luar perimeter, radio <=50 W tanpa gain berarti aman pada >=100 m dari bangunan proses; untuk radar atau pemancar daya sangat tinggi asesmen bisa menuntut pengetahuan lokasi hingga 3 km [R-08-0009, V3_IATG-05.60_en.pdf, hal 10][R-08-0010, V3_IATG-05.60_en.pdf, hal 10].

## Batas jarak pemancar dan penyimpanan (IATG 05.60)

Telepon genggam dan pager dilarang di ESH/PES/magazine/area stowage/bangunan proses dan dekat amunisi persiapan, serta di hadapan uap berbahaya [R-08-0011, V3_IATG-05.60_en.pdf, hal 10]. Di area lain hanya ponsel handheld standar dengan jarak pisah hasil Annex C atau minimum 4 m mana yang lebih besar [R-08-0012, V3_IATG-05.60_en.pdf, hal 11]. Talkback pager memancar pada 146-174 MHz dengan ERP maksimum 50 mW [R-08-0013, V3_IATG-05.60_en.pdf, hal 11]. RFID aktif dan battery-assisted dilarang masuk area eksplosif tanpa persetujuan kepala instansi dengan saran teknis amunisi; pembaca tag pasif diperlakukan sama [R-08-0014, V3_IATG-05.60_en.pdf, hal 11].

## Transportasi dan darurat (IATG 05.60) serta Perhitungan jarak aman (Annex C IATG 05.60)

Karena jarak aman hitungan tidak praktis selama transportasi, seluruh EID yang diangkut jalan harus tahan kuat medan minimal 200 V/m (100 W/m2) pada semua frekuensi [R-08-0015, V3_IATG-05.60_en.pdf, hal 11]. Item yang belum cleared ke lingkungan 100 W/m2 diangkut dalam kotak logam atau bahan terlindungi dengan screening memadai [R-08-0016, V3_IATG-05.60_en.pdf, hal 11]. Jarak default ke transmitter tetap kendaraan 3 m dan dapat turun sampai 0.5 m hanya atas kemasan tersetujui plus pengujian spesialis [R-08-0017, V3_IATG-05.60_en.pdf, hal 12].

Semua kendaraan yang masuk ASA diasumsikan memakai pelacak anti-maling: jaga jarak 5 m antara kendaraan dan dinding luar bangunan berisi eksplosif [R-08-0018, V3_IATG-05.60_en.pdf, hal 12]. Saat kecelakaan/darurat: tidak ada pancaran RF dalam radius 10 m dari EID, dan layanan darurat dengan set kendaraan ERP >5 W jangan menancar dalam 50 m dari peralatan rusak [R-08-0019, V3_IATG-05.60_en.pdf, hal 12][R-08-0020, V3_IATG-05.60_en.pdf, hal 12]. Safety statement: emitter RF sekecil apa pun dilarang menyentuh amunisi dan bahan peledak [R-08-0021, V3_IATG-05.60_en.pdf, hal 12].

Data minimum pemancar untuk hitungan kuat medan: tipe antena, daya rata-rata ke antena (W), frekuensi/pita, dan gain antena; untuk bentuk pulsa ditambah PRF dan pulse width. Angka kerentanan contoh 0.003 W/m2 untuk F53 EBW dengan lead 2 m dipakai menghitung jarak aman hingga 1 GHz, tetapi wajib diuji ulang terhadap data EID spesifik [R-08-0024, V3_IATG-05.60_en.pdf, hal 16]. Tabel C.3 worst case (frekuensi s.d. 1 GHz): gain unity 5.0 m (1 W) sampai 36.5 m (50 W); special 6.5-46.0 m; standard 7.5-51.5 m; high gain 10.0-65.0 m [R-08-0025, V3_IATG-05.60_en.pdf, hal 17].

Uraian pada bab ini tunduk pada keterbatasan baseline beku yang dirinci pada `references/batas-pengetahuan.md`, sehingga angka di luar daftar bab ini berstatus belum terverifikasi dan bukan dinyatakan tidak ada.


| Register beku bab ini | `R-08-0001..R-08-0025` (25 baris); tabel manusia pada `references/register.md` bagian bab 08 |
