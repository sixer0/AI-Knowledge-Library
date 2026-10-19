# Supervisor lessons 08-10: order-by-mtime, rakit-layer patch, pin-era audit, custodian teeth, declarative re-pin

Condensed from VCTL-1007 tail (SB `t_d6715b08`, FIX-3 `t_86670cef`, LIB `t_e396fce0`, LIB2 `t_469ed5fe`) plus GAYAMANUAL L7b cross-checks. All countersigns posted, guards =1.

## 1. Urutan wajib dibuktikan lewat jam berkas, bukan narasi

SB menerima STEER controller @23:00 dengan urutan wajib "sinkron -> gate -> build". Verifikasi pengawas: mtime `catalog.csv` 23:02:03 (sinkron 2 menit setelah steer), DOCX terbit 23:27:06, PDF 23:27:27 — urutan terkunci oleh waktu, dan selisih sinkron-nya dicek langsung di sel target (`VC-68/VC-85`: "bila perlu"=0, ASM-VCTL-03/04=True). Pola: **kalau kartu membawa "urutan wajib", buktikan dengan tiga timestamp + isi sel, jangan dengan klaim result**.

## 2. Tambal di lapis rakit, hulu beku = vonis hilir tidak bergeser

FIX-3 menambal 4 cacat sajian (irisan logo, fragmentasi kolom, caption-yatim, aset VC-32) seluruhnya di builder; `manual.md` (294f9bb6) dan `catalog.csv` (b8601535) kuprobe TIDAK bergeser (mtime < jendela run). Efeknya: semua vonis hulu (C1/C3/V2/V3) tetap sah di eranya, hanya pin sajian yang bergeser. Detektor QA **baru lahir bersama cacatnya** (`qa_d1_img.py`: baseline era-SB 3.267 pt2 FAIL sebagai red-green -> 0,0) — resep fixture merah-hijau kelas R13 VISUAL terulang otomatis di papan keenam. Ukur objek terbit sendiri (pymupdf): halaman==klaim, caption-yatim 0 (69 hal ber-caption SEMUA ber-gambar), lewat-tepi 0 worst 0,0 pt, footer riil 118/120.

**Pitfall penamaan arsip:** byte era-SB utuh di `docx.bak/pdf.bak/xlsx.bak` (sha kucocokkan satu-satu) tapi tanpa label-era — generasi berikutnya bisa salah pilih. Tagihan baku: arsip pra-promosi **bernama-era** (pola `RBUILD2-<sha>` papan kembar), `.bak` polos = utang jejak.

**Audit mata-vs-mesin:** alat independen menandai 8 halaman ekor-bab "mencurigakan", pekerja memverifikasi via vision sebagai akhir-bab wajar dan menyertakan `vision2/` 25 PNG (termasuk nomor halaman literal) untuk mata controller. Pola sah: temuan alat -> adjudikasi vision -> bahan mentah putusan manusia ikut diawetkan, bukan angka telanjang.

## 3. Pin-era audit pada proposa library (pembeda L3-PV vs VCTL-LIB)

L3-PV dulu membasukan pin revC yang sudah tergantikan revD (kutandai sebagai tagihan). VCTL-LIB melakukan sebaliknya dengan benar: katalog `b8601535` == disk terkini, manual DOCX `5a329957` == byte FIX-3 (BUKAN era-SB `43987253` yang sudah tergantikan), manifest `4cf5216f` == generasi pasca-regenerasi aset. **Resep countersign LIB: cocokkan SETIAP pin objek vault terhadap sha16 disk-KINI dan terhadap ledger era pengawas; pin yang benar-umur = indikator librarian mengukur, bukan mengutip.** Dedup juga harus banding-nyata lintas-rak (vs datman-1004/EKAS), bukan sekadar nol-rujukan-silang antar-berkas (uji lemah yang kutandai di L3-PV).

## 4. Jalur deklaratif menghindari re-pin (satu-sumber-kebenaran tanpa memindahkan risiko)

KD-1: pointer katalog benar-isi-salah-alamat (`VC-01` kutip "DAT L135", isi klaim ada di snapshot L93). Dua obat: (a) sunting catalog.csv -> pin b8601535 basi -> SEMUA id vault/proposa yang menyematnya wajib re-pin; (b) sumber TIDAK disentuh, koreksi ditulis di seksi KD-1 objek wiki dengan hasil ukur pembenar + status known-defect menempel -> id tetap valid. LIB2 memilih (b) dan ini sah: **rak membaca koreksi bersama sumbernya**. Tagihan yang wajib ikut tertulis: kalau nanti sumber benar-benar disunting, re-pin id = kewajiban eksplisit (deklarasi tersimpan di objek). Generalisasi: saat artefak sudah disemat-pin oleh id objek hilir, prefer obat deklaratif di lapis konsumen daripada mutasi sumber; kalau mutasi perlu, hitung dulu semua penanam-pin.

## 5. Custodian punya gigi + dispatch env-strip

Rantai promosi LIB2: katalog+manual lolos iterasi-1; objek RESEP **ditolak** perlu_revisi ("60 VC/1 WARISAN/1 LEGACY" vs census seharusnya) -> gatekeeper menambal ber-guard ke 61+12+1=74 (== angka vonis-C2 pengawas) -> iterasi-2 lolos. Bukti pemisah-tangan dua-arah: gatekeeper boleh menulis objek, tapi verdict tetap milik custodian yang berani menolak. Resep teknis: `env -u HERMES_KANBAN_TASK -u HERMES_KANBAN_DB hermes -p gsp-custodian -z "<kontrak verdict-first>"` — env-strip mencegah sesi custodian mewarisi konteks kartu (vonis segar, bukan gema). Post-proof dua-arah 15/15: body vault-disk == wiki-disk byte-identik + sensus mirror own/total.

## 6. Terbit-dengan-known-defect berlapis (KD-2)

Ratifikasi manusia (50+4 butir ASUMSI) diputus SADAR bukan prasyarat rak INTERNAL (butir sudah bertanda per-sel sehingga tidak terbaca kebijakan final), tetapi tetap mengunci kanal EKSTERNAL. Semantik rilis berlapis: internal-shah-dengan-register != eksternal-layak; sebutkan kunci eksternalnya eksplisit supaya tidak terwarisi lupa.

## 6a. Sensor pengawas: baca KONTEKS sebelum membantah (lagi)

Probe-ku atas klaim librarian "L135 = seksi Grouped": satu baris pertama mencetak `###   ` (heading kosong) dan hampir kubacakan sebagai bantahan; kucek baris 135+136 -> judul seksi memang di baris berikutnya (heading markdown terpecah). Klaim librarian BENAR, vonis "PASS d.d. KD-1" survive. Pelajaran-ke-11 diterapkan ke rebuttal sendiri SEBELUM tayang: koreksi teks komentar saat pra-post, bukan komentar-koreksi setelahnya.

## 7. Ledger akhir papan keenam (untuk silang-papan berikutnya)

Katalog enam-era declared: 1faaf613 -> 88ffc2f4 -> 5e21d8c3 -> 3bff9391 -> b8601535; manual-md 294f9bb6; sajian docx 43987253 (era-SB, terarsip .bak) -> 5a329957 / pdf b7966d27 (FINAL 120 hal); xlsx 919cfc1f; manifest 11fb027d -> 4cf5216f; VC-32 aset fda8c03a. Vault 3 objek wiki active. Sisa di luar papan: closeout git standing-rule + ratifikasi eksternal ASUMSI.
