---
id: harga-dems-0927-register-terverifikasi
type: fakta
title: Register harga terverifikasi HARGA-DEMS-0927 (objek library)
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-27
catatan_verifikasi: "Verdict: terverifikasi. || Alasan: re-verifikasi iterasi-2 empat butir fokus, seluruhnya cocok dengan parser sendiri. (1) Bagian 2 benar: TSV v2 terukur 243 baris data, 243/243 ber-harga non-kosong, nol sel literal None, sha256 369205d6f89f2596...c499208 cocok penuh dengan pin objek; ke-13 baris identitas bernama di bagian 2 ditemukan SATU PER SATU di JSONL lajur sebagai entity-match/CER-R0 tanpa harga (L04x4, L06x1, L07x6, L08x1, L09x1; total tanpa-harga tepat 13). (2) Nol angka berubah: multiset SELURUH 243 baris TSV v2 identik dengan bak-v1 ternormalisasi None->kosong (diff dua arah kosong; sel None tervalidasi 147 pada v1, 0 pada v2); beda mentah hanya kelas serialisasi None vs kosong. (3) P-5 cocok: lima baris putusan manusia VS-REPORT seksi KEPUTUSAN MANUSIA hadir persis satu per baris di TSV (BRK-PTZ Uniview alibaba, PST-PDU KEAN gys.cn, KBL-AUD szlcsc, KBL-DAYA jinlongyu szlcsc, KBL-UTP AMPCOM szlcsc). (4) Basis kolom harga terendah dinyatakan di bawah tabel dan teruji 66/66 entri mata-uang pada basis price_list-bila-terisi-selainnya-price_sale dengan batas bulat tampil +0.51 (jauh di atas syarat >=8 sampel; termasuk 8 sel yang gagal pada parser naif iterasi-1: KBL-AUD/DAYA/UTP, KIT-TAS, PST-HDD20, PST-LTO9W, SW-8, UPS-3K). Penguat: census tier TSV nol kebocoran PROV/KLAIM-VENDOR; riwayat iterasi-1 utuh. || Rekomendasi: lanjut promosi oleh gsp-librarian; ingat batas terpasang - P-5 menunggu putusan controller, angka terikat tanggal akses 2026-09-27/2026-09-23."
riwayat-catatan-verifikasi-1: "Verdict: perlu_revisi. || Alasan: enam dari tujuh dimensi lolos ukur ulang independen; dua cacat ditemukan pada klaim isi berkas timbangan dan serialisasinya. Provenans SAH: 10 pin sha256/16 lajur cocok semua saat diukur ulang, pin TSV 40e6cf7e5b617e70...cocok penuh (sha256 lengkap), ladder.md hadir 10/10 lajur, kartu VS t_9bcf08e0 dan V t_9b9c18de cocok dengan laporan. Pembilang COCOK PERSIS dengan parser sendiri atas 713 baris JSONL: PROV terbuang 447, KLAIM-VENDOR terbuang 10, bertahan 256 = 243 ber-harga + 13 identitas-tanpa-harga, 53 kode, tanggal akses 712 @ 2026-09-27 + 1 @ 2026-09-23; tabel bagian 4 cocok per-kode (n) dan jumlah 243; 65 dari 66 sel harga terendah cocok numerik persis pada basis price_list-bila-terisi-selainnya-price_sale, 1 sel (UPS-L IDR 750.000) sama di bawah konvensi titik pemisah ribuan. Anti-karangan SAH di level makna: sampel berseed 20260927 (12 baris) dan perbandingan multiset SELURUH 243 baris TSV vs JSONL menunjukkan 0 beda field setelah normalisasi null; nol baris PROV/KLAIM-VENDOR lolos ke TSV (census tier TSV hanya entity-match varian + CER-R0). Metadata SAH: yaml.safe_load lolos, title==H1, satu baris status, tanpa kunci duplikat, tanpa nilai terpotong kelas-2. Dedup SAH: nol entri wiki dan nol objek vault lain atas korpus ini. Gerbang sensitif/dosir: tidak berlaku (sensitif=tidak; dua kandidat nomor telepon di TSV terukur substring slug URL tokopedia, bukan data kontak). Penanda P-1..P-4 konsisten VS-REPORT: butir FIX-2 terukur benar tereksklusi (IBM TS4300 brnetwork KLAIM-VENDOR L08:23, BRANKAS CNY 66.00 PROV L06:25, KIT-TRIPOD CNY 1.00 PROV L06:112), S-2/S-8 butir FIX-4 ber-tier PROV sehingga tidak menuntut penanda, baris D-1 (jd.com NVR-64) ber-tier PROV sesuai klaim bagian 2. CACAT 1: bagian 2 menyebut 13 baris identitas 'ikut di TSV' dan bagian 5 menyebut keduanya ada di berkas timbangan, padahal TSV terukur berisi 243 baris saja dan 0 dari 13 baris identitas ada di dalamnya (ke-13nya hanya hidup di JSONL lajur). CACAT 2: berkas timbangan membawa 147 sel literal 'None' pada 57 baris (moq 47, pack_size 49, price_sale 36, price_list 15) akibat serialisasi str(None) - setara kosong secara makna, tapi 4 dari 12 baris sampel gagal identik mentah karenanya. || Rekomendasi: (a) koreksi bagian 2 dan bagian 5 menjadi TSV = 243 baris ber-harga saja, atau lampirkan 13 baris identitas sebagai berkas terpisah lalu rujuk; (b) regenerasi TSV dengan null menjadi sel kosong, bukan 'None', lalu pin sha256 baru di objek; (c) tambahkan penanda P-5 untuk lima baris warisan putusan manusia VS (BRK-PTZ Uniview alibaba, PST-PDU KEAN gys.cn, KBL-AUD, KBL-DAYA, KBL-UTP szlcsc) yang ikut substrat tanpa disclosure; (d) nyatakan basis kolom harga terendah (price_list bila terisi, selainnya price_sale) di catatan tabel. Nol angka pembilang berubah; koreksi bersifat klaim alamat isi dan serialisasi."
revisi-oleh: gsp-librarian
revisi-pada: 2026-09-27
revisi-iterasi: 1
catatan_revisi: "Revisi iterasi-1 gatekeeper 2026-09-27 menindaklanjuti perlu_revisi custodian; tiap butir diuji ulang gatekeeper ke sumber pada giliran yang sama: (a) klaim cakupan TSV dikoreksi - TSV memang 243 baris ber-harga saja (ukur wc/grep giliran ini), 13 baris identitas kini terdaftar bernama di bagian 2; (b) TSV diregenerasi dengan sel null kosong menggantikan literal None (147 sel pada 57 baris terukur; multiset nilai diverifikasi identik dengan v1, nol angka berubah), pin sha256 baru dipasang; (c) P-5 lima baris putusan manusia VS ditambah (verbatim VS-REPORT seksi KEPUTUSAN MANUSIA); (d) basis kolom harga terendah dinyatakan. Nol angka pembilang dan nol nilai harga berubah."
sumber: docs/2026-09-27-harga-dems-saturasi/lanes/L01..L10/findings.jsonl
halaman: register 243 baris ber-harga (13 identitas tanpa-harga dirujuk ke JSONL lajur), berkas timbangan library/verified-register-rows.tsv sha256 369205d6f89f2596...; ladder per lajur lanes/*/ladder.md
tanggal_akses: 2026-09-27
kelas_bukti: primer
sensitif: tidak
perkara: harga-dems-0927
tags: [harga, dems, register-brand-model-price, cctv, networking, server, lisensi, harga-dems-0927]
links: [docs/2026-09-27-harga-dems-saturasi/verification/VS-REPORT.md, docs/2026-09-27-harga-dems-saturasi/verification/V-REPORT.md]
penulis: gsp-librarian
diajukan: 2026-09-27
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-27
dipromosikan-ke: faktas/harga-dems-0927-register-terverifikasi.md
catatan_keputusan: "dipromosikan: HARGA-DEMS-0927 KB: register brand-model-price terverifikasi (entity-match/CER-R0 only; PROV/KLAIM-VENDOR tereksklusi); lolos custodian + gerbang gatekeeper; publik non-sensitif"
---

# Register harga terverifikasi HARGA-DEMS-0927 (objek library)

Ringkasan eksekutif: register brand-model-price hasil misi saturasi harga DEMS 27-09-2026, TERBATAS baris ber-evidence_tier entity-match / CER-R0..R4. Baris PROV (447) dan KLAIM-VENDOR (10) DIBUANG dari substrat ini dan tidak boleh disimpulkan ada. Kelas bukti objek = primer (harga tampil di halaman sumber pada tanggal akses), dengan sintesis kurasi gatekeeper.

## 1 Provenans (AM-G4)
- Sumber RAW: docs/2026-09-27-harga-dems-saturasi/lanes/L01..L10/findings.jsonl (10 berkas lajur; total 713 baris).
  - L01/findings.jsonl sha256/16 = 42474a6c36bebf78
  - L02/findings.jsonl sha256/16 = c0cc728fda539938
  - L03/findings.jsonl sha256/16 = bc7cdca6f07719d3
  - L04/findings.jsonl sha256/16 = 95aa9a0ecb23f2ef
  - L05/findings.jsonl sha256/16 = 8e7f72f6735401ba
  - L06/findings.jsonl sha256/16 = e1325e99f0e15fc0
  - L07/findings.jsonl sha256/16 = 20da5ca9ae14ae10
  - L08/findings.jsonl sha256/16 = d9d23bbd2544dbd5
  - L09/findings.jsonl sha256/16 = 8d87e31c2ba87044
  - L10/findings.jsonl sha256/16 = 02d295f59de1b600
- Pin beku pembilang: berkas timbangan objek ini = docs/2026-09-27-harga-dems-saturasi/library/verified-register-rows.tsv (243 baris ber-harga; revisi-1 menormalkan sel null menjadi kosong tanpa mengubah satu pun nilai - multiset nilai diverifikasi identik dengan v1), sha256 = 369205d6f89f25969beef5ae5f93a9850d0eb180eb280e41c9f4cff62c499208.
- Kartu sumber: L01 t_73857fc1 + t_380d8ab0; L02 t_0f5a6e83 + t_e16806c2; L03 t_570cbff5 + t_68ae492e; L04 t_2d0f81c7 + t_1cb6a509; L05 t_88a6e3a7 + t_fcd05988; L06 t_231330e8 + t_a285f27d; L07 t_678ea559 + t_e90019aa; L08 t_89f4ef37 + t_e76ecaf3; L09 t_79a9e19a + t_a5dbabca; L10 t_d2394bd6 + t_03647743; merger MRG t_8fe938db; audit V t_9b9c18de; verifikasi independen VS t_9bcf08e0 (VERDICT PASS lingkup VS, seed 2026092707).
- Tanggal akses: 2026-09-27 (712 baris) dan 2026-09-23 (1 baris). Harga pasar berubah - nilai wajib dianggap terikat tanggal akses, bukan permanen.
- Ladder per lajur (rung | URL/aksi | status HTTP + ts | hasil): docs/2026-09-27-harga-dems-saturasi/lanes/L01..L10/ladder.md; rekap verifikasi: verification/V-REPORT.md dan verification/VS-REPORT.md.
- Workbook turunan (bukan objek ini): output/HARGA-DEMS-0927_Price-Saturation_EN.xlsx sha256 = 16e7724f3dcc40e7f61f891190626e3ef87790bf1645ea2286715f658f91e43a; kurs Rp 20.443,09 per USD (README workbook).

## 2 Metode kurasi
- Gerbang masuk baris: kolom evidence_tier bernilai entity-match (termasuk varian beralasan dalam tanda kurung) atau CER-R0; prov dan klaim-vendor dieksklusi (hitung riil di atas). Tidak ada baris yang diedit isinya; filter murni per-baris utuh dari JSONL lajur.
- 13 baris entity-match/CER-R0 TANPA angka harga (halaman identitas resmi yang tidak menampilkan harga pada tanggal akses) tidak dihitung sebagai baris ber-harga dan TIDAK ditulis ke berkas timbangan - TSV berisi 243 baris ber-harga saja. Ketiga belas baris identitas itu terdaftar bernama: UPS-R SANTAK TG-BOX (santak.com.cn); UPS-R APC SMT1000I (se.com/id); PST-UPS Vertiv GXT5-10KIRT2UXLN (vertiv.com); UPS-L APC BVX700LUI-MS (apc-indonesia.com wp-json); BRANKAS AIPU (aipusafe.com/pro.html); KIT-MIK UGREEN CM727 (lulian.cn); KONSOL Beelink SER5/SER10 (bee-link.com); KONSOL Minisforum UM-series (store.minisforum.com); KIT-TAB HIGOLE F9A (jd.com phb); KIT-KAM Logitech C925e (logitech.com/id-id); PST-KVM MT-VIKI (mt-viki.com); PST-STOR Inspur SA5212H5 (serverbasket.com); PST-FW TOPSEC NGFW4000-UF (price.zol.com.cn). Ketigabelasnya tetap hidup di JSONL lajur sebagai rujukan.
- Vonis rilis workbook (defect D-1 label kanal jd.com NVR-64, milik V) TIDAK diubah objek ini: baris D-1 ber-tier PROV sehingga sudah ter eksklusi dari substrat; attest librarian = gerbang promosi pengetahuan, bukan gerbang rilis workbook.

## 3 Penanda kualitas (known-defect parsial, wajib dibaca sebelum pakai angka)
- P-1 bait/placeholder (preseden VS FIX-2): pembanding US$2.150 IBM TS4300 (brnetwork) dan CNY 66 BRANKAS serta CNY 1,00 KIT-TRIPOD TIDAK masuk substrat ini karena tier-nya KLAIM-VENDOR/PROV (terukur: grep giliran ini). Yang tetap perlu perhatian: PST-TAPE ltoworld US$3.699-5.199 = harga basis-library per-chassis (bukan konfigurasi 2-drive >=40-slot penuh) dan LIS-BAK NAKIVO US$1,00-3,05 = tarif per-user/per-VM pada halaman tarif resmi (bukan lisensi site). Jangan pakai sebagai best-price item utuh tanpa rekonsiliasi.
- P-2 rentang harga: kolom price_list dapat berisi rentang "min-max"; angka terbaik di bawah dihitung dari batas BAWAH.
- P-3 satuan: unit/moq ikut terbawa (kolom unit, moq, pack_size) - pemakai wajib cek basis satuan sebelum membandingkan lintas baris (preseden delta KBL-UTP +45724% akibat beda basis).
- P-5 putusan manusia tertunda (VS-REPORT seksi KEPUTUSAN MANUSIA): lima baris entity-match lolos provinance harvest byte-exact TANPA token identitas di live+CDX (BRK-PTZ Uniview alibaba, PST-PDU KEAN gys.cn, KBL-AUD szlcsc, KBL-DAYA jinlongyu szlcsc, KBL-UTP AMPCOM szlcsc) ikut substrat ini atas keputusan manusia/V yang terus berlaku - status VERIFIED mereka menunggu putusan controller, bukan vonis SALAH-TARGET (spot hidup VS: 0 salah-target).
- P-4 checkpoint controller: kedalaman per kode tidak seragam; 5 kode tanpa baris sama sekali (PKI-ROOT, PST-CORE, PST-MGMT, PST-NTP, PST-HSM) = vonis nol-angka-ber-akun lajur L09, bukan kehilangan data objek ini.

## 4 Tabel ringkasan per kode (baris ber-harga)
| Kode | n | merk terwakili | harga terendah per mata uang (domain sumber) |
|---|---|---|---|
| ARS-HDD | 5 | Seagate, Toshiba, WD | IDR 7,519,900 (tokopedia.com) |
| ARS-SRV | 1 | Dell | USD 2,365 (serverbasket.net) |
| AUD-DSP | 3 | DSPPA, FHB | USD 385 (alibaba.com) |
| BRK-PTZ | 8 | ACTi, Bosch, Hikvision, Uniview, Vivotek | USD 4.2 (alibaba.com) |
| HDD-4 | 4 | Seagate, Toshiba, WD | IDR 3,943,000 (tokopedia.com) |
| HDD-8 | 6 | Seagate, Toshiba, WD | IDR 7,520,000 (tokopedia.com) |
| HDD-EXT | 6 | ADATA, Seagate, WD | IDR 1,800,000 (tokopedia.com) |
| HSM | 1 | Nitrokey | EUR 109 (shop.nitrokey.com) |
| KAM-1 | 8 | Axis, Bosch, Dahua, Forchar, Hanwha Wisenet, Hikvision | USD 71 (veacam.en.made-in-china.com) |
| KAM-2 | 12 | ACTi, Axis, Bosch, G.Craftsman, Hanwha, Hikvision | USD 31 (alibaba.com) |
| KBL-AUD | 1 | 也仁 RVVP | CNY 435 (item.szlcsc.com) |
| KBL-DAYA | 1 | 金龙羽 | CNY 217 (item.szlcsc.com) |
| KBL-UTP | 1 | AMPCOM 安普康 | CNY 1,323 (item.szlcsc.com) |
| KIT-KAM | 3 | Lenovo, NexiGo | CNY 279 (m.lenovo.com.cn); USD 44.99 (nexigo.com) |
| KIT-MIK | 3 | BOYA (博雅), Maono, NexiGo | USD 62.99 (store.boyamic.com) |
| KIT-TAB | 6 | HIGOLE (嗨高乐), Oukitel | USD 159 (higole.en.made-in-china.com) |
| KIT-TAS | 2 | Pelican | USD 270 (pelican.com) |
| KONSOL | 4 | Axioo, Minisforum | IDR 18,770,100 (mbizmarket.co.id); USD 367 (store.minisforum.com) |
| LIS-BAK | 4 | NAKIVO | USD 1 (nakivo.com) |
| LIS-OS | 8 | Canonical, Red Hat, UnionTech (统信 UOS) | CNY 234 (market.aliyun.com); USD 25 (ubuntu.com) |
| LIS-SDS | 2 | Canonical | USD 5,000 (ubuntu.com) |
| LIS-SIEM | 6 | Graylog, Splunk, Wazuh | USD 15 (splunk.com) |
| MDM-LIS | 5 | Jamf, JumpCloud, Scalefusion | USD 5.75 (jamf.com) |
| MIK | 3 | MiCWL, SINGDEN, Takstar | USD 10 (alibaba.com) |
| NVR-16 | 12 | Hikvision, TP-Link, Uniview | IDR 1,695,750 (tokopedia.com) |
| NVR-32 | 12 | Dahua, Hikvision, Uniview | IDR 6,366,000 (distributor-cctv.com) |
| NVR-4 | 6 | EZVIZ, Hikvision, Nextcam, TP-Link, Uniview | IDR 1,210,000 (distributor-cctv.com) |
| NVR-64 | 7 | Dahua, Hikvision | IDR 22,999,000 (tokopedia.com) |
| NVR-8 | 6 | Dahua, Hikvision, Uniview | IDR 1,663,000 (distributor-cctv.com) |
| PST-BAKSRV | 1 | Dell | USD 4,129 (serverbasket.net) |
| PST-FW | 2 | HUAWEI (华为), SANGFOR (深信服) | CNY 10,499 (m.zol.com.cn) |
| PST-HDD20 | 1 | Seagate | USD 1,236 (newegg.com) |
| PST-HOST | 3 | Dell | USD 7,349 (serverbasket.net) |
| PST-KBL | 3 | ROBOfiber (dist. Datainterfaces.com) | USD 27 (datainterfaces.com) |
| PST-KVM | 4 | Eaton (Tripp Lite NetDirector), Raritan (Legrand), Vertiv (Avocent) | USD 1,475 (lttpartners.com) |
| PST-LTO9 | 1 | Fujifilm | USD 225 (backupworks.com) |
| PST-LTO9W | 1 | HPE | USD 246 (tapeandmedia.com) |
| PST-PDU | 7 | AMPCOM (安普康), APC (Schneider Electric), Eaton, generic (深圳厂商 listing), 百能 (Baineng), 科安技术 (KEAN) | CNY 85 (m.1688.com); IDR 6,625,000 (tokopedia.com) |
| PST-RAK | 2 | APC/Schneider, Vertiv | USD 3,505 (server-rack-online.com) |
| PST-STOR | 3 | Dell | USD 3,379 (serverbasket.net) |
| PST-TAPE | 4 | HPE, IBM, MagStor, Quantum | USD 3,699 (ltoworld.com) |
| PST-UPS | 6 | APC (Schneider Electric), EAST 易事特, ITeaQ 艾特网能, JINWUSHI (金武士), KSTAR (科士达) | CNY 6,000 (product.pconline.com.cn); IDR 87,349,904 (tokopedia.com) |
| PSU-12 | 4 | SPC (lokal), generic (import) | IDR 34,400 (cncstorebandung.com) |
| RTR-B | 5 | Fortinet, MikroTik, TP-Link, Ubiquiti | CNY 415 (tp-linkshop.com.cn); USD 129 (store.ui.com) |
| SW-16 | 4 | MikroTik, TP-Link, Ubiquiti | CNY 739 (tp-linkshop.com.cn); USD 199 (store.ui.com) |
| SW-24 | 11 | Marstars (Shenzhen Longxing Industrial), MikroTik, Netgear, TP-Link, Ubiquiti | CNY 979 (tp-linkshop.com.cn); USD 190 (szmarstars.en.made-in-china.com) |
| SW-48 | 4 | Lanwee, MikroTik, Netgear, Ubiquiti | USD 315 (lanweetech.en.made-in-china.com) |
| SW-8 | 6 | MikroTik, Netgear, TP-Link | IDR 450,955 (tokopedia.com); USD 130 (netgear.com) |
| SW-POE | 6 | Marstars (Shenzhen Longxing Industrial), TP-Link, Ubiquiti | CNY 487 (tp-linkshop.com.cn); USD 75 (szmarstars.en.made-in-china.com) |
| TAB-BAG | 3 | Advan, Lenovo, Xiaomi | CNY 1,399 (lenovo.com.cn); IDR 2,599,000 (advandigital.com) |
| UPS-3K | 9 | APC (Schneider Electric), Eaton, HUAWEI (华为), ITeaQ 艾特网能, KEHUA (科华数据), Vertiv (Liebert) | CNY 1,290 (m.gys.cn); IDR 19,800,000 (klikglodok.com) |
| UPS-L | 2 | APC (Schneider) | IDR 750,000 (plazait.co.id) |
| UPS-R | 5 | APC (Schneider Electric), EAST 易事特, ICA | CNY 530 (ymgk.com); IDR 1,251,000 (harrisma.id) |

(Basis angka: price_list bila terisi, selainnya price_sale; nilai IDR ditafsirkan pemisah ribuan titik. Kolom terendah = harga terendah PER MATA UANG dalam baretang kode yang sama; tidak dikonversi lintas mata uang - konversi + PPN/faktor ada di workbook MRG.)

## 5 Register lengkap
Seluruh 243 baris terverifikasi ber-harga ada di berkas timbangan (13 baris identitas tanpa harga dirujuk ke JSONL lajur, lihat bagian 2): docs/2026-09-27-harga-dems-saturasi/library/verified-register-rows.tsv - kolom: lane, code, item_en, origin, brand, model, channel_type, price_list, price_sale, currency, unit, moq, pack_size, source_name, source_url, date_accessed, evidence_tier, spec_match_notes, round. Setiap baris membawa URL sumber + tanggal akses sendiri (provenans per-nilai).

## 6 BATAS
- Bukan daftar harga siap-beli: tidak memuat PPN/faktor impor/kurs per baris (ada di workbook MRG untuk 243 baris yang sama).
- Kelas bukti per kelompok: entity-match = nama entitas muncul di host/judul/isi halaman sumber; CER-R0 = endpoint/API situs resmi pabrikan. Keduanya primer terhadap halaman yang diakses, BUKAN jaminan harga hari ini.
- Sensitif: tidak. Seluruh baris dari halaman publik; tidak ada kredensial, dosir, atau data pribadi.
