---
id: inventaris-12-identitas-skill-ekas-peta-lintas-versi
type: fakta
title: "Inventaris 12 identitas skill EKAS — peta lintas versi"
status: active
sumber: docs/2026_08_24_inventaris_skill_ekas/INVENTARIS-SKILL-PANDUAN-EKAS.md
halaman: Bagian A (A1-A5)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: ekas-skill-inventaris
domain: library
writer: gsp-librarian
tags: [ekas, skill, inventaris, knowledge-system]
penulis: dashboard
diajukan: 2026-08-25
catatan_keputusan: "Konkurensi orkestrasi 2026-08-25: unit sama juga diproposa paralel lebih atomik — vault/inventaris-skill-ekas/2026-08-25_ekas-registri-12-skill.md (+ ekas-skill-angka-a1-t11-t12, ekas-skill-perancang-a2-pre-existing, ekas-excel-master-workbook-hitungan). Konservatif: TIDAK dihapus; Wave B custodian verifikasi silang kedua set & pilih/merge."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/ekas-skill-inventaris/2026-08-25_inventaris-12-identitas-skill-ekas-peta-lintas-versi.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Inventaris 12 identitas skill EKAS — peta lintas versi

Peta menyeluruh identitas skill yang terdeteksi di korpus EKAS (scan 270 file, terutama CHANGELOG.md T1–T21, GAP-ACQUISITION-PLAN.md, SOURCE-UPDATE-PROCEDURE.md, TEMPLATE-BERITA-ACARA.md, README-ekspor.md, knowledge cards) [R1 — INVENTARIS-SKILL-PANDUAN-EKAS.md, Bagian A].

## Kelompok A1 — dibangun dari rak (T11–T12, 19 Agustus 2026), SKILL.md asli TIDAK ikut paket
1. **pustaka-teknis** — lapisan sumber; memanggil angka + rujukan untuk semua skill perancang; SKILL.md + 3 referensi (01-indeks-rumus, 02-rantai-hitung-proyek, 03-batas-dan-celah) + `04-daftar-rujukan-lengkap.md` (dibangkitkan) [R1, Tabel A1 #1].
2. **rcm-analysis** — keandalan: FMEA, konsekuensi, P-F interval, FFI, interval pemeliharaan [R1, Tabel A1 #2].
3. **fiber-link-design** — serat optik: loss budget, metode uji, OTDR; SKILL.md + 3 referensi (377 baris) [R1, Tabel A1 #3].
4. **power-backup-sizing** — UPS/baterai/genset: kapasitas, derating, ventilasi, interval uji fungsi; SKILL.md + 4 referensi (465 baris) [R1, Tabel A1 #4].
5. **grounding-lightning-design** — pembumian & proteksi petir: Wenner, fall-of-potential, rolling sphere; rantaian RANTAI-JAMINAN PUTUS di ambang [R1, Tabel A1 #5].

## Kelompok A2 — pre-existing di Mac, dirujuk korpus
6. **cctv-system-designer** — perancang VSS ("tetap memegang perancangannya" per CHANGELOG T12) [R1, Tabel A2 #6].
7. **perimeter-security-designer** — perancang keamanan perimeter [R1, Tabel A2 #7].
8. **hw-sw-config-master** — konfigurasi hardware/software [R1, Tabel A2 #8].

## Kelompok A3 — terpasang di mesin asal tanpa rujukan pustaka
9. **digital-forensics-evidence-system** — sistem manajemen bukti digital (lini DEMS); menunggu NIST SP 800-86 / ISO/IEC 27037 [R1, Tabel A3 #9].
10. **dems-polri-proposal-architect** — arsitek proposal DEMS kepolisian; menunggu bahan yang sama [R1, Tabel A3 #10].

## Kelompok A4 — dicanangkan (belum dibangun)
11. **onvif-interop** — interoperabilitas VSS (profil ONVIF S/G/T/M); bahan ONVIF belum diadakan (gratis di onvif.org) [R1, Tabel A4 #11].

## Kelompok A5 — lainnya
12. **excel-master** — workbook hitungan; asumsi pada sheet terpisah, rumus hidup; dirujuk ASUMSI-BAKU.md [R1, Tabel A5 #12].

Catatan: `document-control` (8 file) adalah berkas `DOCUMENT-CONTROL.md`, bukan skill [R1, Bagian A catatan].

## Catatan status saat ini (konteks, bukan klaim sumber A)
Per AGENTS.md workspace GSP (24-08-2026), ke-12 skill di atas sudah dibangun ulang di Windows dan terpasang: kanonik [`gsp-hermes/skills/`](../../../3%20Skills/kanonik/) + registry default [`~/.hermes/skills/gsp/`](../../../3%20Skills/registry-fleet/) [R2 — AGENTS.md, seksi "Skill rekayasa EKAS" & "Skill pelengkap EKAS"]. Diverifikasi 2026-08-25: 12 direktori skill terkonfirmasi ada di kedua lokasi.
