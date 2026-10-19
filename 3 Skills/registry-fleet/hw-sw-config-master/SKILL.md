---
name: hw-sw-config-master
description: Use when configuring network, storage, or IT infrastructure.
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, network, storage, config, raid, infrastructure, ops]
  hermes:
    tags: [gsp, it-infrastructure]
    related_skills: [pustaka-teknis]
---

# HW/SW Config Master — Konfigurasi Infrastruktur TI

## When to Use

- Merancang/memeriksa **konfigurasi jaringan, penyimpanan, server**: topologi, VLAN/ruas,
  kapasitas RAID, BDP, praktik operasional.
- Menyusun **dokumentasi konfigurasi** dan prosedur operasi yang dapat diaudit.

Kanonik: [`ekas/05_DOMAIN-KNOWLEDGE/NETWORKING/RANTAI-JAMINAN.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/NETWORKING/RANTAI-JAMINAN.md) + `STORAGE/RANTAI-JAMINAN.md`
+ resume (Fall & Stevens, Kurose/Ross, Odom, Limoncelli, Troppens) di folder terkait.

## Alur wajib

1. **Kebutuhan & lingkup**: perangkat, segmen, kapasitas, ketersediaan (SLA).
2. **Hitung kebutuhan** (lihat [`references/01-jaringan-penyimpanan.md`](references/01-jaringan-penyimpanan.md)):
   - Kapasitas RAID: RAID 5 `(n−1)×C` · RAID 6 `(n−2)×C` [R3 — Troppens PDF 46–70].
   - BDP (mengapa transfer lambat padahal bandwidth besar): `BDP = RTT × kapasitas penyempit`
     [R3 — Fall & Stevens PDF 769]; window scaling [TCP/IP Illustrated].
3. **Rancang konfigurasi**: skema IP/VLAN, routing, QoS, HA, backup & config management.
4. **Dokumentasikan**: konfigurasi final + baseline + prosedur perubahan (change
   management). Konfigurasi tanpa dokumentasi = konfigurasi yang tidak dapat diaudit.
5. **Uji/verifikasi**: perintah verifikasi nyata (ping/traceroute/health), bukti output,
   BUKAN deskripsi.

## Aturan praktik operasional (Limoncelli [R3])

- Konfigurasi = kode: versi, review, perubahan tercatat.
- Backup konfigurasi sebelum perubahan; rollback plan selalu ada.
- Sekuriti default: least privilege, segmenasi, log diaktifkan.
- Jangan merombak diam-diam — ubah via proses, dokumentasikan alasan.

## Batas yang harus dinyatakan

- **Unjuk kerja tulis pengendali (write performance) = R4** — bervariasi antar produk
  meski aras RAID sama; uji kasus per kasus (ASUMSI-BAKU §F).
- **Waktu rekonstruksi RAID = R4** dari pabrikan pengendali; nilailah risiko kegagalan kedua.
- Standar perkabelan terstruktur (TIA-568/942) dan desain pusat data **tidak ada di rak**.
- Angka produk (kapasitas kanal, throughput, latency) = R4 per proyek.

## Verifikasi sebelum mengklaim selesai

- Kapasitas terpakai sesuai aras RAID yang disepakati pemilik ✓
- BDP/window scaling dipertimbangkan untuk jalur WAN ✓
- Konfigurasi terdokumentasi (baseline + perubahan) ✓
- Verifikasi dilakukan dengan perintah nyata, output dilampirkan ✓
- Klaim unjuk kerja produk = dari lembar data (R4), bukan brosur umum ✓