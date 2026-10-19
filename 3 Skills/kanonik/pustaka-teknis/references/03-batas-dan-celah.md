# 03 — Batas & celah rak EKAS (baca sebelum mengutip)

> Kanonik: `ekas/02_REGISTERS/GAP-REGISTER.md` + `02_REGISTERS/GAP-ACQUISITION-PLAN.md` +
> `00_START-HERE/README.md`. Ringkasan di bawah untuk kecepatan; bila ragu, buka kanoniknya.

## Sebaran rak (per 24-08-2026)

```
R1  ░░░ 0      ← tidak ada dasar hukum Indonesia di rak
R2  ███ 5      ← seluruh ambang uji sah berasal dari sini
R3  ██  24 buku ← kekuatan rak: metode, rumus, penalaran
R4  ░░░ 0 (memang selalu dari pabrikan, per proyek; 97 dokumen OEM terindeks di laci namun belum diresume semua)
R5  ██  3+21 makalah ← penunjuk, bukan sandaran
```

## Tiga rantai PUTUS — perilaku wajib

| Rantai | Domain | Yang tidak ada | Akibat |
|---|---|---|---|
| **D** | GROUNDING-LIGHTNING | Ambang resistansi pembumian | Boleh ukur/desain; **tidak boleh menyatakan lulus** tanpa sumber sah |
| **J** | CYBERSECURITY | Seluruh R1/R2 (UU ITE, Perban BSSN, ISO 27001, NIST 800-86, ISO 27037) | Tidak boleh menulis "sesuai ISO 27001" tanpa salinan standar |
| **K** | CIVIL-STRUCTURAL | Empat SNI struktur (1726/1727/1729/2847) | Menghitung boleh; keselamatan struktur **wajib tanda tangan ahli bersertifikat** |

Tiga jalan sah untuk rantai D: (1) pemilik menetapkan ambang tertulis, (2) kontrak mengadopsi
standar tertentu, (3) lapor hasil ukur **tanpa pernyataan lulus**. Yang tidak sah: mengisi
"< 5 Ω" karena angka itu sering terdengar.

## Batas cakupan standar (sering disalahpahami)

| Standar | **Tidak** mencakup |
|---|---|
| ANSI/NETA **ATS** | Uji pemeliharaan — itu MTS, tidak ada di rak. ATS = uji **terima** |
| **IEEE 1188** | Baterai vented — itu IEEE 450 (tidak ada). 1188 = **VRLA** saja |
| **BS EN 62676-1-2** | Interoperabilitas perangkat — itu ONVIF (tidak ada) |
| **IEC 61280-4-2** | Multimode — itu IEC 61280-4-1 (tidak ada) |
| **ANSI/NETA ATS** | Kepatuhan Indonesia — standar Amerika, bukan pengganti PUIL |

## Perangkap besar: dua besaran yang sering tertukar

Rak **punya** ambang **tahanan isolasi** (MΩ, NETA Tabel 100.1 [R2]) — dan **tidak punya**
ambang **resistansi pembumian** (Ω). Keduanya beda satuan dan beda makna. Jangan saling
menggantikan.

## Cacat & usia berkas yang wajib dibawa

- **Diesel Generator Handbook (Mahon 2004)** kehilangan ±55 hal — **Bab 11 (emergency &
  standby) hilang seluruhnya**. Materi genset darurat tidak tersedia di rak.
- Crompton (2000), Emadi (2004), Mahon (2004), Troppens (2009), Nyman & Levitt (2010):
  > 15 tahun → kerangka hitung sahih; **angka batas wajib diperiksa ulang**, angka produk → R4.
- Uman (2008) mengutip **IEC 62305:2006** — sudah usang; sebutkan edisi berlaku bila mengikat.
- Buku sipil/bangunan/kelistrikan berbasis **ASCE 7, AISC, ACI 318, ASTM, IBC, NEC, NFPA,
  ASHRAE** — metodenya boleh, angkanya tidak otomatis berlaku di Indonesia.
- Tabel profil baja Segui = profil **W/HP/HSS Amerika**, bukan WF/H-beam SNI — tidak dipakai langsung.

## Empat hal yang TIDAK boleh diasumsikan (keputusan pemilik)

1. Sasaran MTBF kegagalan majemuk
2. Sasaran pengamatan video (FI/FR)
3. Ambang resistansi pembumian
4. Resistivitas tanah (harus **diukur** — Wenner, tidak ada penggantinya)

Bila belum ditetapkan → sajikan pilihan + konsekuensi, minta keputusan tertulis. Pekerjaan
perancangan belum dapat diselesaikan tanpa keempatnya.

## Daftar pengadaan (yang membuka celah bila tiba)

ONVIF (gratis) · PUIL/SNI · NIST SP 800-86 + ISO/IEC 27037 · ISO/IEC 27001/27002 ·
TIA-568/942 · ANSI/NETA MTS · IEEE 450 · salinan lengkap Diesel Generator Handbook.