# Daftar padanan wajib (rujukan data, BUKAN gerbang)

Sumber: GAYA-AHLI-1005 S14, putusan `t_dbb77bfe` butir M-18 (APPROVE sebagai
berkas data referensi). Pemakai: Manual L4 (STD-GAYA-AHLI-001) dan scanner HANYA
bila sebuah check kosakata memang membutuhkannya nanti. Berkas ini TIDAK boleh
dipakai sebagai dasar FAIL sampai ada bukti pakai pada korpus.

Status label per baris: `TERUJI` = muncul di korpus pembanding lajur G3
(`work/g3_kosakata.md` §4.4, R-6 contoh 18); `ASSUMPTION` = usulan penulis lajur
G3 yang belum teruji pakai, dilarang menjadi dasar vonis (syarat putusan M-18).

| Istilah | Padanan ID | Status | Bukti / catatan |
|---|---|---|---|
| monitoring | pemantauan | TERUJI | g3_kosakata.md §4.4 baris "wajib padanan" [R-6 contoh 18] |
| review | reviu / tinjauan | ASSUMPTION | dipakai luas tetapi belum diuji-pakai pada korpus pembanding |
| workshop | pelatihan | TERUJI | g3_kosakata.md §4.4 [R-6 contoh 18] |
| road map | peta jalan | TERUJI | g3_kosakata.md §4.4 [R-6 contoh 18] |
| forum group discussion | diskusi kelompok terpumpun | TERUJI | g3_kosakata.md §4.4 [R-6 contoh 18] |
| backup | cadangan | ASSUMPTION | tiga pasangan terakhir ditandai ASSUMPTION oleh penulis G3 (§6 butir 9) |
| rollback | pemulihan | ASSUMPTION | belum teruji di korpus |
| pipeline | alur kerja | ASSUMPTION | belum teruji di korpus; catatan: 'pipeline' juga nama instrumen teknis GSP - uji kasus diperlukan sebelum gerbang |

Kelas yang BOLEH dipertahankan tanpa padanan (putusan §4.4): token teknis
protokol/antarmuka (`BACnet/IP`, `ONVIF Profile S`, `SNMP`, `SHA-256`) dengan
label manusia saat kemunculan pertama; istilah tanpa padanan mapan di bidang GSP
(`chain of custody`, `hot-swap`, `loss budget`) dengan definisi sekali; idiom
korespondensi bisnis EN (`Kind regards,`) demi konsistensi rumah (D-08).

Aturan pakai: pasangan berlabel ASSUMPTION dilarang memicu FAIL maupun cited
sebagai "standar" sampai putaran kalibrasi korpus mencatat daya pisahnya; jika
scanner kelak menambah check kosakata padanan, check itu mulai diberlakukan sebagai INFO dulu sesuai
disiplin yang sama dengan C-26/C-27/C-28/C-33 (naik predikat hanya setelah nol
positif palsu terdokumentasi).
