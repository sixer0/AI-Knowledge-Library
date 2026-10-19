# 01 — Kerangka perancangan perimeter (dari domain terdekat)

## 1. Cakupan yang bisa dipertanggungjawabkan hari ini

| Lapisan/topik | Sumber di korpus | Status |
|---|---|---|
| Kamera, lensa, cakupan, bitrate, rekaman | VIDEO-SURVEILLANCE (Damjanovski/Szeliski) + rantai | ✅ lengkap |
| Termal (kamera) | THERMAL (Vollmer) + NETA Tabel 100.18 | ✅ ambang ΔT R2; NETD/IFOV R4 |
| Jaringan & konfigurasi perangkat | NETWORKING + STORAGE + hw-sw-config-master | ✅ metode |
| Infrastruktur kritis / objek vital | CRITICAL-INFRASTRUCTURE (Johnson) | ✅ kerangka |
| Sensor pagar/radar/fusi sensor | — | ❌ buku khusus tidak ada di rak |
| Standar nasional keamanan fisik | — | ❌ R1 kosong |

## 2. Urutan desain yang benar

1. Ancaman + kinerja (dengan pemilik) → 2. pemilihan teknologi per lapisan → 3. hitung
   kebutuhan (VSS/termal/jaringan) → 4. zona & urutan deteksi → 5. keputusan desain
   tercatat (TPL-01, dengan alternatif ditolak) → 6. uji terima.

## 3. Angka dari domain terdekat yang relevan

- FI/FR 250/125 pix/m (kamera identifikasi vs pengenalan) — cctv-system-designer.
- Ambang ΔT termal: >15 °C antar komponen serupa, >40 °C vs udara [R2 — NETA Tabel 100.18].
- Waktu deteksi hilang sinyal 8/4/2 detik per grade [R2 — BS EN 62676-1-2].
- False alarm rate, jangkauan, konsumsi daya sensor → **R4 pabrikan, jangan dikarang**.

## 4. Klaim yang DILARANG

- "sesuai standar nasional keamanan perimeter" — R1 kosong, tidak ada dasar.
- Jangkauan/keandalan sensor tanpa lembar data (R4).
- Fusi sensor "AI" tanpa spesifikasi unjuk kerja terukur.