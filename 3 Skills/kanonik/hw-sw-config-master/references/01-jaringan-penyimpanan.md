# 01 — Jaringan & penyimpanan: rumus dan praktik

## 1. Kapasitas RAID [R3 — Troppens PDF 46–70]

```
RAID 5  : kapasitas terpakai = (n−1) × C
RAID 6  : kapasitas terpakai = (n−2) × C
```

- `n` = jumlah cakram, `C` = kapasitas per cakram.
- **Unjuk kerja tulis & waktu rekonstruksi = R4** (pengendali tertentu; uji kasus per kasus).
- Risiko kegagalan kedua saat rekonstruksi dinilai dari waktu rekonstruksi (R4).

## 2. BDP & window scaling [R3 — Fall & Stevens PDF 769]

```
BDP = RTT × kapasitas penyempit (bandwidth bottleneck)
```

- BDP > window default → perlu **window scaling**; tanpa itu transfer lambat meski
  bandwidth besar.
- TCP/IP Illustrated (ed. 2, 2012): BDP, window, congestion.

## 3. Praktik operasional (praktik standar industri — Limoncelli [R3])

| Praktik | Alasan |
|---|---|
| Konfigurasi = kode (versi, review, riwayat) | Dapat diaudit, rollback pasti |
| Backup config sebelum perubahan | Pemulihan cepat |
| Least privilege + segmenasi + log aktif | Sekuriti default |
| Perubahan via proses (ticket), dokumentasi alasan | Mencegah perubahan liar |

## 4. Yang TIDAK ada di rak

- TIA-568 (perkabelan terstruktur) · TIA-942 (pusat data) — celah GAP menengah.
- Angka throughput/latency produksi per perangkat = **R4**.
- Manajemen proyek teknis (penjadwalan, risiko) — tidak terwakili di rak.

## 5. Asumsi domain (ASUMSI-BAKU §F)

Aras RAID disepakati pemilik · waktu rekonstruksi dari pabrikan · unjuk kerja tulis
diperiksa kasus per kasus (jangan generalisasi lintas produk).