---
id: manual-komprehensif-chart-graphs-gsp-000-gsp-std-x-2026-reva-terbatas
type: standar
title: Manual Komprehensif Chart & Graphs GSP 000-GSP-STD-X-2026 RevA (TERBATAS)
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-08
catatan_verifikasi: "Verdict: terverifikasi || Alasan: seluruh pin dan angka permukaan terukur ulang cocok; dedup terhadap wiki terbukti; klasifikasi TERBATAS benar dan jujur; mewarisi KD-1/KD-2 yang sudah direkam akurat di objek induk katalog. || Bukti ukur: docx 5a3299573e481323 (4.799.626 B)==pin; pdf b7966d276136ce74 (5.012.287 B)==pin; pypdf 120 halaman==klaim; pita TERBATAS 4x==ukur; nomor registrasi 4x==ukur; word/media 77==klaim dan 74 di antaranya sha256 identik dengan aset assets/render/manifest.json (bukti langsung 74 figur tertanam; 3 sisanya chrome sampul/kepala/ekor). Wiki: tidak ada entri manual chart (hanya datman-1004 pohon/simbol/registri) -> klaim dedup sah. Batas: publikasi eksternal tetap butuh persetujuan manusia (approval-ref); ratifikasi KD-2 objek induk berlaku atas sel katalog yang tampil di halamannya."
keputusan-promosi: "PUTUSAN LIBRARIAN t_469ed5fe 2026-10-08: terbit ke RAK INTERNAL saja (kanal K2 sajian). Publikasi EKSTERNAL belum disetujui manusia - pita TERBATAS tercetak di permukaan dokumen sumber; butuh approval-ref terpisah. Mewarisi KD-1 (pointer terkoreksi L93) dan KD-2 (50 ASUMSI belum ratifikasi) dari objek katalog induk - keduanya tercatat di body objek induk dan dirujuk seksi 3 objek ini."
sumber: docs/2026-10-07-vctl-chart-catalog/output/Manual Komprehensif Chart & Graphs GSP 000-GSP-STD-X-2026 RevA.docx
halaman: 120 hal; pin sha16 5a3299573e481323 (docx) / b7966d276136ce74 (pdf)
tanggal_akses: 2026-10-08
kelas_bukti: sintesis
sensitif: tidak
perkara: vctl-1007
tags: [vctl-1007, manual-chart, std-x-2026, terbatas-internal, kanal-k2, revA]
links: [docs/2026-10-07-vctl-chart-catalog/CONTRACT.md, docs/2026-10-07-vctl-chart-catalog/PHASE-REPORTS.md, vault/vctl-1007/2026-10-08_katalog-kanonik-chart-graph-gsp-99-entri-vctl-1007-pin-b860153546765629.md]
penulis: gsp-librarian
diajukan: 2026-10-08
catatan_keputusan: "dipromosikan: VCTL-1007 LIB2: verdict custodian d61925 (katalog/manual iter-1; resep iter-2 pasca-tambal) + keputusan sadar KD-2 terbit-dengan-known-defect; TERBATAS internal saja"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-08
dipromosikan-ke: standars/manual-komprehensif-chart-graphs-gsp-000-gsp-std-x-2026-reva-terbatas.md
---

# Manual Komprehensif Chart & Graphs GSP 000-GSP-STD-X-2026 RevA (TERBATAS)

Manual 120 halaman kanal K2 (sajian) atas katalog chart kanonik: setiap jenis chart dengan definisi operasional, prasyarat data, ambang, empat kelompok aturan presisi, padanan mesin fleet, dan figur render contoh (74 figur tertanam). Nomor registrasi placeholder `000-GSP-STD-X-2026` menunggu Register Induk (keputusan controller).

## 1. Pin terukur ulang giliran kurasi ini (08-10-2026, gsp-librarian)

| Field | Nilai |
|---|---|
| Path kanonis | `docs/2026-10-07-vctl-chart-catalog/output/Manual Komprehensif Chart & Graphs GSP 000-GSP-STD-X-2026 RevA.docx` [R-1, ukur] |
| sha256[:16] DOCX | `5a3299573e481323` == pin kartu (4.799.626 B) [R-1] |
| sha256[:16] PDF | `b7966d276136ce74` (5.012.287 B; 120 halaman tercacah pypdf run ini) [R-1] |
| Isi tercacah | 4 kemunculan pita "TERBATAS"; 4 kemunculan nomor registrasi; 77 media tertanam (74 figur + sampul/kepala/ekor) [R-1, unzip word/document.xml] |

## 2. Rantai provenans

- Rakit era-SB (124 hal) -> audit controller qa_final 13/13 + vision pass -> 4 cacat (D1 sampul, D2 wrap, D3 caption yatim, D4 aset VC-32) -> FIX-3 t_86670cef bangun ulang dua-pass -> 120 hal konvergen; gerbang diri qa_final 13/13 PASS + sb_check 10/10; vision2/vision3 bersih; vonis pengawas FIX-3 SAH (CONTRACT.md ledger + PHASE-REPORTS.md fase FIX-3).
- doc_gate_check exit=0 kedua berkas; scanner kanal doc PASS; konten-kekal 99+74; determinisme dua-run byte-identik.

## 3. Klasifikasi dan gerbang

- TERBATAS: dokumen internal GSP (pita tercetak di permukaan). Publikasi eksternal BELUM disetujui manusia - objek ini dipromosikan ke vault/rak internal saja; kanal publik menuntut persetujuan tersurat (approval-ref) dari pemilik.
- Kelas bukti: sintesis (turunan katalog kanonik yang sama; angka per-jenis membawa marker `[DAT L###]`/`[HOL brs NNN]`/`ASUMSI` mengikuti katalog).
- Known-defect ikut-terbaca: KD-1 pointer VC-01/VC-05 dan KD-2 50 ASUMSI menunggu ratifikasi - lihat objek katalog `katalog-kanonik-chart-graph-gsp-99-entri-vctl-1007-pin-b860153546765629`; manual menampilkan sel yang sama sehingga cacat pointer ikut terbit di permukaan halaman.

## 4. Dedup

Tidak ada entri wiki/chart-manual serupa: DATMANUAL-1004 menerbitkan pohon pemilihan + katalog simbol (bukan manual chart); STD-VISUAL-001 adalah pedoman aturan instrumen (bukan katalog jenis). Manual ini pelengkap sajian dari katalog kanonik VCTL-1007.
