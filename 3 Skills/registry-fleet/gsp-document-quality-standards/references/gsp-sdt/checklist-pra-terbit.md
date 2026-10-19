# Checklist Pra-Terbit GSP-SDT (23 butir ≤ 25) - Paket GSP-SDT

> Sumber: SPEC-DOC-SYSTEM.md §4 (siap-tempel), gerbang C-23 + delta §2.6. Butir 1–18 universal;
> 19–23 varian rezim. **Satu butir wajib gagal = TAHAN terbit; kegagalan dicatat, bukan
> disembunyikan.** Skill konsumen MERUJUK berkas ini - jangan menyalin isinya ke SKILL.md.

```markdown
GSP-SDT PRE-PUBLICATION CHECKLIST - rezim: [SDT|SDTP|AD|AU|PL|CY|BIZ], kelas: [K1..K8]
- [ ] 1. Blok identitas lengkap sesuai bentuk rezim (6×4 pertahanan / strip profesional) dan konsisten Register Induk
- [ ] 2. Status kepatuhan pada Klausul 1–2 dinyatakan; penyimpangan = pengecualian bernomor di revisi
- [ ] 3. Klasifikasi benar menurut penerima; tercetak di kepala, kaki, dan sampul
- [ ] 4. Bobot kelas (Tabel 4.1 rezim) diketahui; seluruh titik uji terpenuhi sebelum pengesahan
- [ ] 5. Anatomi wajib Tabel 5.1 kelas terpenuhi - tidak ada blok ● yang kosong
- [ ] 6. Acuan normatif berstatus Wajib/Rujukan; rujukan bertanggal = edisi yang disebut
- [ ] 7. RUU/draf belum disahkan tidak dipakai sebagai dasar wajib (ditandai Pending)
- [ ] 8. Klausul bernomor tunggal; subklausul ≤3 tingkat; tidak ada nomor dilewati/dipakai ulang
- [ ] 9. Gambar & tabel bernomor per klausul (k.n) dan SETIAP gambar/tabel punya baris SUMBER
- [ ] 10. Setiap kebutuhan membawa REQ-Kx-nnn unik dan tertaut metode verifikasi
- [ ] 11. Setiap angka teknis membawa provenans ■/◈/◇/△ yang benar (wajib di K1/K4/K5)
- [ ] 12. Penomoran lembar mengikuti pola rezim (n-mm / SHEET nn OF mm / LEMBAR n DARI m / HAL nn/mm / HLM n/mm / n/mm) dan cocok dengan jumlah lembar
- [ ] 13. Tabel/gambar tidak dipenggal antar lembar tanpa penanda lanjutan
- [ ] 14. Dokumen berbukti memuat rantai kustodi SHA-256 sebelum-sesudah
- [ ] 15. Format ≥ minimum rezim (A4, margin, huruf, palet) - tidak lebih longgar
- [ ] 16. Riwayat revisi: huruf berurut, baris terbaru di puncak, baris lama utuh
- [ ] 17. Kegagalan butir dicatat, tidak disembunyikan - satu butir wajib gagal = TAHAN terbit
- [ ] 18. Manifest visual konsisten: setiap kepala 'Gambar k.n' punya objek tertanam (docx/pptx) dan setiap objek punya nomor+SUMBER; ilustrasi utama dibuat via jalur /create-image-gsp, bukan screenshot (Module I.11)
Varian:
- [ ] 19. AD/AU: sertifikat kelaikan (udara) terlampir bila K4/K5; tata naskah dinas matra dipenuhi
- [ ] 20. PL: rantai kustodi & BB-nnn+SHA-256 untuk dokumen bukti; TTE/BSrE pada dokumen yang menuntut keabsahan
- [ ] 21. CY: klasifikasi = dampak terparah bila bocor; daftar distribusi terbatas di sampul (K1/K3/K5); PoC tersanitasi & terpisah
- [ ] 22. CY: tiap temuan FND-Kx-nnn membawa CVSS (pita 7.2) + pemetaan MITRE ATT&CK
- [ ] 23. BIZ: harga&lingkup konsisten proposal↔BOQ↔kontrak; TKDN dideklarasikan; INCOTERMS+SLA jelas; NDA/PDP terpenuhi; status Draf/Final/TTD ditandai
```

## Cara eksekusi oleh generator

1. Jalankan checklist SEBELUM ekspor/serah (gerbang terakhir setelah Module L.6 fleet).
2. Hasil checklist ditempel di lampiran atau dicatat di komentar tugas; nilai kelulusan bobot
   kelas dilaporkan jujur (mis. "K5: 9/10 titik uji - butir T tertunda, TAHAN terbit").
3. Hubungkan dengan Module L.6: L.6 memeriksa FORMAT keluaran fleet; checklist ini memeriksa
   BENTUK/ISI GSP-SDT. Keduanya harus LULUS - tidak saling menggantikan.
4. Rujukan angka internal dokumen memakai `[R-n, sumber, hal]` (L.4); rujukan eksternal ke
   dokumen sistem memakai kode R-1..R-7 SPEC-DOC.
