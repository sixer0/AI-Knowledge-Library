---
name: onvif-interop
description: Use when checking or selecting ONVIF device profiles.
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, onvif, interoperability, vss, profiles, video]
  hermes:
    tags: [gsp, onvif, vss]
    related_skills: [cctv-system-designer, pustaka-teknis]
---

# ONVIF Interop — Profil & Interoperabilitas Perangkat Video

## When to Use

- Menjawab *"apakah kamera A benar-benar bisa dipakai dengan VMS B?"* — pertanyaan yang
  muncul di hampir tiap proyek VSS.
- Menyusun persyaratan profil ONVIF dalam spesifikasi/tender (S/G/T/M).
- Menyiapkan & menilai **uji interoperabilitas**.

## ⚠ Sumber

Bahan utama **TIDAK ada di korpus EKAS** — diambil dari **dokumen publik resmi ONVIF
(onvif.org)**, gratis. Penanda kutip: `[PUB — ONVIF <dokumen> vX.Y, URL]`.
Karena bukan R1/R2/R3 EKAS, perlakukan sebagai **rujukan eksternal yang perlu diverifikasi
ulang pada saat pemakaian untuk persyaratan mengikat** (profil dapat direvisi/didepresiasi).

## Peta profil video (per 24-08-2026)

| Profil | Peruntukan | Fitur inti yang dijamin | Catatan |
|---|---|---|---|
| **S** | Streaming video dasar | Video streaming & konfigurasi (IP/RTSP), PTZ control, audio in, multicast, relay | ⚠ **DEPRECATED** — pengajuan produk baru sampai 31 Mar 2027; proyek baru pindah ke **T** |
| **G** | Edge storage & retrieval | Recording di perangkat/jaringan, playback; audio & metadata stream (bila didukung) | Kombinasi umum dengan T |
| **T** | Advanced streaming | H.264/H.265, imaging settings, motion alarm & tampering events, metadata streaming (wajib), onscreen display (wajib), bi-directional audio; client wajib PTZ; + HTTPS streaming, PTZ config, motion region, digital I/O, relay | **Pilihan utama VSS baru** |
| **M** | Metadata & events untuk analytics | Konfigurasi & streaming metadata; klasifikasi objek (geolocation, vehicle, license plate, face, body); event: object counter, face/LPR; MQTT | Untuk analitik; bisa digabung S/T |
| **D** | Berlaku untuk sistem video & akses | Cek spesifikasi resmi bila dipakai | — (profil akses juga: A, C, D) |

**Hanya produk yang terdaftar di ONVIF Conformant Products dengan conformance profil
tertentu yang boleh disebut "ONVIF conformant".** Klaim vendor tanpa registrasi = tidak sah.

## Alur kerja

1. **Tentukan kebutuhan fungsional**: streaming saja? rekaman? analitik/metadata? akses?
2. **Pilih profil** yang menjamin fitur itu (lihat tabel; VSS baru → **T**, + **G** bila
   edge storage, + **M** bila analitik).
3. **Periksa konformansi**: cek tiap perangkat di halaman ONVIF Conformant Products;
   cocokkan profil yang didukung klien (VMS) maupun perangkat.
4. **Tulis persyaratan spesifikasi**: sebut profil + fitur wajib (bukan sekadar "ONVIF").
5. **Uji interoperabilitas** (proyek): konfigurasikan kamera via VMS, streaming, playback,
   PTZ, event — dengan bukti (screenshot/log). **Klaim vendor bukan bukti.**
6. **Catat batas**: profil yang tidak terpenuhi = keterbatasan nyata, tuliskan.

## Yang DILARANG

- Menulis "sesuai ONVIF" di proposal tanpa verifikasi registrasi konformansi produk.
- Menganggap perangkat yang mendukung satu profil otomatis mendukung yang lain.
- Menggunakan **Profile S** sebagai persyaratan proyek baru (deprecated — pilih T).

## Verifikasi sebelum mengklaim selesai

- Profil yang dipilih sesuai kebutuhan fungsional (streaming/recording/analitik) ✓
- Setiap perangkat tervalidasi di ONVIF Conformant Products (tanggal cek dicatat) ✓
- Spesifikasi menyebut profil + fitur wajib, bukan sekadar kata "ONVIF" ✓
- Uji interoperabilitas dilakukan dengan bukti nyata ✓
- Versi dokumen ONVIF yang dipakai dicatat [PUB — ...] ✓