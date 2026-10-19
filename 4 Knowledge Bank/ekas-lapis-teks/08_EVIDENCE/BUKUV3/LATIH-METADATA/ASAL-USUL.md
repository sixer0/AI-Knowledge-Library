# Asal-usul arsip metadata lapisan latih BUKUV3 (W6)

Sumber: share UGOS `http://192.168.0.90:9999/filemgr/share-download/?id=027381cf5c624fbdb2751c6841b0ff4f` (folder `/volume1/GSP-DATA/BUKUv3`, read-only,
sesuai putusan D-01 kontrak BUKUV3-MAP-1009 dan D-ING-01 terkunci D-08 kontrak BUKUV3-ING-1009).

Putusan D-ING-01: lapisan latih diarsipkan **METADATA-SAJA**. Yang tersimpan di folder ini:
kartu model, daftar isi per berkas (nama + ukuran + SHA-256), dan catatan asal-usul ini.
**BOBOT TIDAK DISALIN** ke korpus teks (P-6 PLAN-INGESTION: lisensi LOKAL-SAJA, bobot bukan
pengetahuan tekstual, 11,55 GB).

Isi lapisan menurut manifest NAS (terverifikasi alat giliran ini):
- CURATION/: 231 berkas, 0.792 GB (korpus latih CPT/SFT + pipeline NeMo Curator; nol berkas bobot)
- TRAINING/: 304 berkas, 11.549 GB, terdiri 97 berkas bobot 11.270 GB (safetensors/gguf/bin/pt/pth) + naskah latih/eval

SHA-256 berkas bobot dihitung dengan men-stream isi dari share NAS dan membuang byte setelah
hash (skrip `scripts/ekas-ingestion/bukuv3-ing-1009/w6_hash_bobot.py`; byte bobot tidak pernah
ditulis ke disk kerja). MODEL-CARD diunduh utuh (3156 B, sha256=bceb6b46f6fcf701419241fb79acaf9319f7f6b5291a5fe4c791d22beee4974e).

Diarsipkan oleh kartu W6 t_cc964b17 (misi BUKUV3-ING-1009) pada 2026-10-09 12:36. NAS sumber tidak ditulis.
Daya-ikat entri ini: metadata/register (R5-artefak, LOKAL-SAJA), bukan R1-R4; dilarang promosi
Information Library (gerbang gsp-librarian + label LOKAL-SAJA D-ING-01).
