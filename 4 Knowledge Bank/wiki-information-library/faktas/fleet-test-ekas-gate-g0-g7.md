---
id: fleet-test-ekas-gate-g0-g7
type: fakta
title: "Gate jaminan EKAS G0-G7 dan aturan rantai (2026-08-24)"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-data-analyst/synthesis.md
halaman: hal. 1 (Gate G0-G7; kanonik ASSURANCE-GATES.md)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: engineering
writer: gsp-librarian
tags: [ekas, gate, jaminan, assurance, engineering]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-ekas-gate-g0-g7.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Gate jaminan EKAS G0-G7 dan aturan rantai (2026-08-24)


Rantai jaminan EKAS lima mata: Rujukan -> Keputusan -> Hitungan -> Uji -> Bukti serah [sumber — synthesis.md hal. 1].

Gate G0-G7 [sumber — synthesis.md hal. 1; kanonik ekas/01_GOVERNANCE/ASSURANCE-GATES.md]:
G0 sumber tervalidasi (edisi/halaman/tingkat R); G1 kebutuhan dibekukan (keputusan pemilik tertulis); G2 desain disetujui (catatan + alternatif ditolak); G3 hitungan diverifikasi (masukan bertanda, pemeriksaan kedua); G4 metode uji + ambang beserta sumbernya; G5 uji lulus dengan bukti mentah (kalibrasi berlaku); G6 bukti serah lengkap (asumsi terbuka, data OEM menunggu); G7 diterima pemberi kerja secara tertulis.

Aturan inti: gate tidak boleh dilompati; G4 tidak dapat ditutup selama G3 terbuka bila ambang dihitung sendiri; mundurnya satu gate menarik mundur seluruh gate sesudahnya; "menunggu" boleh asal tertulis.

Kelas bukti: sekunder (ringkasan gsp-data-analyst dari sumber primer EKAS).
