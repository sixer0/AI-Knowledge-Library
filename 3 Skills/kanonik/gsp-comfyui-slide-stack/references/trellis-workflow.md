# Cara Kerja TRELLIS.2 (image-to-3D) - tervalidasi loop 5 iterasi, 2026-09-01

Kondisi hardware: RTX 5070 Ti 16 GB. Semua langkah di bawah sudah dipukul nyata;
skor juri /30 per iterasi: before 7, v1 6, v4 5, v5b 7, v6 8 (terbaik, input benar).

## Rantai produksi (3 sesi terpisah)

```
Z-Image referensi -> BiRefNet cutout (WAJIB InvertMask) -> TRELLIS.2 GLB
   sesi A                sesi A (model kecil)                sesi B (restart)
```

### Sesi A - referensi + cutout
1. Generate referensi dengan aturan bentuk (lihat "Spesifikasi input" di bawah).
2. Cutout: `LoadImage -> RemoveBackground -> InvertMask -> JoinImageWithAlpha -> SaveImage`.
   RemoveBackground mengembalikan mask = LATAR. Tanpa InvertMask, model 3D dibentuk
   dari sisa latar (inilah akar seluruh hasil jelek sebelum v6).
3. Verifikasi numerik wajib (jangan percaya mata saja):
   - alpha tengah gambar = 254, alpha sudut = 0 (kalau terbalik: tengah 0, sudut 254)
   - bbox objek menyentuh tepi frame kiri+kanan (sayap utuh, tidak terpotong)
   - pigmen warna khas komponen (mis. biru panel surya) hadir dalam mask > 3%
   - komposit di atas magenta untuk cek visual tepi (skrip render helper)

### Sesi B - TRELLIS.2 (restart server dulu)
1. Restart ComfyUI dengan: `--highvram --disable-dynamic-vram --cache-lru 16`
   DAN env `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.
   VRAM baseline wajib < 1 GB. `/free` TIDAK membebaskan bobot yang dipin cache;
   hanya restart yang bersih. Fragmentasi terbukti: reserved 14,3 GB tapi aktif
   8,4 GB saat decode butuh 2,65 GB kontigu -> expandable_segments menyelesaikan.
2. Parameter terkunci (tervalidasi terbaik):
   - conditioning: 1 gambar + mask, threshold 0.5
   - structure: steps 20, cfg 3.0, pm 1.0
   - shape: steps 12, cfg 3.0, res 1024, pm 1.0, algorithm "surface net"
   - upsample: steps 12, cfg 3.0, res 1024, pm 1.0   # RESEP 20x-loop (D14): 1536 justru merusak
   - texture: steps 12, cfg 3.0, coords 16
   - mesh: simplify 500000, remove_internal, weld 0.0002
   - UV: UnwrapMesh (pec, resolution 1024, padding 1, weld_distance 0.0002)
     WAJIB sebelum BakeTextureFromVoxel (bake menolak mesh tanpa UV)
   - bake: texture_size 1024 (2048 mepet OOM di res 1536; 1024 aman berulang)
3. Tandai tahap lambat: "Bake texture" bisa diam 3-5 menit di 40% (rasterize berat).
   Jangan kill; cek `/queue` (running=1) + nvidia-smi util > 0.

## Spesifikasi input yang menentukan hasil (pelajaran v1 vs v4 vs v6)
- SATU objek, latar polos, isi >= 70% frame.
- Layout T atau three-quarter: komponen tidak saling mengoklusi.
  Frontal datar = siluet ambigu = blob (v4 5/30 meski referensi 19/20).
- Komponen khas harus terlihat penuh: dish menghadap kamera, boom + sayap
  horizontal terpisah dari body, modul bawah jelas.
- Skor kandidat referensi dengan vision judge SEBELUM cutout (rubrik a-d /20);
  ambil >= 15/20. 3-4 seed, pilih terbaik.
- Multi-view conditioning TIDAK tersedia di ComfyUI build ini: node
  Trellis2Conditioning hanya menerima 1 input image. Jangan kejar fusi 360
  di jalur ini; tuas realistis = kualitas input + seed.

## Loop perbaikan (skrip di scripts/ folder ini)
1. `trellis_loop.py <variant>` - bangun workflow dari base + varian params,
   submit, tunggu, ambil GLB (kunci output "3d", bukan "gltf").
2. `render_textured.py <glb> <out.png> "<elev,azim list>"` - render 4 sudut
   bertekstur via trimesh (sampling UV per-face).
3. `judge.py <ref.png> <render.png> <konteks>` - delegasi penilaian ke vision
   (rute cepat: gateway kilocode qwen3.8-flash via ask_vision.py, ~40 detik;
   rute hermes chat profil image-analyst terlalu lambat utk 2-3 gambar).
   Rubrik /30: dish, panel, boom, body, detail, clean. Output: score, pass,
   kriteria, critique, fix_hint.
4. Satu perubahan per iterasi (ablation), catat di iter_ledger.json.
   Kalau juri menyalahkan parameter tapi skor tidak naik, curigai INPUT.
5. Plafon jujur: single-image-to-3D kelas ini pada objek kompleks menghasilkan
   bentuk dasar terbaca + detail halus hilang. Target realistis: objek dikenali
   dari 4 sudut, bukan replika CAD.
6. **Konvergensi terbukti (v6 vs v7, 01-09):** threshold 0.50->0.65 dan seed
   diganti TIDAK mengubah skor (keduanya 8/30, kriteria juri identik).
   JANGAN ulangi sweep thr/seed pada objek serupa - plateau ini batas tool,
   bukan knob yang belum ketemu. Sisa perbaikan hanya via custom node
   multi-image pihak ketiga, atau menerima hasil terbaik.
7. **Noise juri TERUKUR (loop-20x, 01-09):** render IDENTIK dinilai 8 lalu 4, lalu
   [6,5,5]. Jangan klaim improvement dari SATU penilaian. Standar: skor = median
   3 run; improvement sah bila median > best DAN >=2 run > best. Baseline v6 pada
   skala median = 5/30 (bukan 8).
8. **Siluet padat (fg > 0,38 dari frame 1024px): turunkan res DAN tex bersamaan.**
   Bukti berantai L02/L02b: thr 0,55 @res1536 OOM di VaeDecodeShape; res1280 +
   tex1024 lolos shape tapi OOM di BakeTexture; baru res1280 + tex512 aman 16 GB.
   Triase satu-per-satu GAGAL untuk objek padat -> lompat dua level sekaligus.
9. **RESEP TERBAIK 20x-loop (D14, 02-09): upsample res 1024 > 1536 untuk KUALITAS.**
   Kontrol identik (input baseline, thr 0,5, seed sama) hanya beda res: median tiga
   run @1024 = [7,6,6] vs band @1536 = 2-5. Res tinggi = voxel berlebih = tepi
   bergerigi + noise yang dihukum juri. Turunkan default resep ke 1024.
10. **Knob sampling TIDAK berpengaruh (20x-loop):** shift 3 (vs 5), rcfg_hi 1,0,
    rcfg_lo 0,7, cfg 5,5 -> semua 3-5/30, setara kontrol tanpa knob. JANGAN habiskan
    iterasi sweep knob sampling; tuas nyata hanya res, input, dan seed (noise).
11. **Seed = sumber noise terbesar:** kontrol res1024 seed 20260901=7, seed lain=3.
    Untuk deliverable: generate 2-3 seed, juri median-3, ambil terbaik (bukan sweep).
12. **Rantai produksi wajib server-per-iterasi** (scripts/chain2.sh): run beruntun
    dalam satu proses menaikkan baseline alokasi -> varian yang sama FAIL di run
    ke-2. Rantai multi-run hanya untuk eksplorasi murah yang siap di-restart.

## OOM triage cepat
| Gejala | Akar | Obat |
|---|---|---|
| Gagal di VaeDecode/Bake padahal aktif << limit | fragmentasi | expandable_segments + restart |
| Gagal dengan aktif mendekati 15,9 GB | beban nyata | tex 2048->1024, upsample 1536->1280 |
| Objek padat (fg>0,38): lolos stage A mati di stage B | volume voxel besar | res DAN tex turun bersamaan (1280+512), jangan satu-satu |
| BakeTexture OOM dengan request KECIL (±149 MiB) | voxel aktif terlalu banyak -> **texture_size TIDAK mengubah puncak bake** (bukti byte-identik 14.62GiB/148.89MiB pada tex1024 vs tex512) | turunkan res atau thr; JANGAN buang siklus GPU menurunkan tex untuk mengatasi bake |
| Stage lain lolos, satu stage mati terus | voxel volume besar (objek padat) | turunkan res upsample, JANGAN sentuh algo |
| Repro varian lama GAGAL padahal dulu lolos | default loop (tex2048) diam-diam beda dari varian asli (tex1024) -> cek `params` mentah variants.json, jangan tulis ulang manual | salin persis params varian asli |
| VaeDecodeShape minta alokasi RAKSASA (>5 GiB) padahal fg mask rendah (<0,3) | **fg mask BUKAN prediktor okupansi voxel.** Bidang solid menghadap kamera (dish/depan penuh) berokupansi jauh lebih tinggi daripada siluet memanjang (T-layout). Bukti: s1 fg 0,271 minta 6,07 GiB; baseline fg 0,332 hanya 1,22 GiB | prediktor aman = luas *bidang proyeksi solid*; desain "depan penuh" wajib res<=1024 sejak awal |
| OOM VaeDecodeTexture padahal statistik mask 2D IDENTIK dengan varian yang lolos | **tidak ada prediktor 2D yang andal** (fg, bbox, extent, komponen semuanya gagal prediksi). Beban ditentukan interpretasi 3D model atas RGB (kondisi DINOv3). Bukti: s1 lolos @1024; s2/s3 mask biner identik (fg & bbox sama) tapi OOM @1024 | jangan habiskan siklus mencari prediktor; tangga res legal hanya **1024-2048 step 128** (min node UpsampleStage=1024; 768 ditolak HTTP 400 SEBELUM eksekusi). Di bawah 1024 satu-satunya tuas = thr/objek |
| Timbul saat ganti sesi | bobot sesi lama tertahan cache | restart, bukan /free |
| `nvidia-smi` ikut hang/timeout setelah OOM berat | driver-level hang: proses python sisa masih memegang GPU | kill via PowerShell `Get-CimInstance Win32_Process` + `Stop-Process -Force` (taskkill dari git-bash tidak andal), tunggu ±90 detik, verifikasi `timeout 20 nvidia-smi` sebelum lanjut |
| gen FAIL "timeout" padahal log server mencatat "Prompt executed" normal | klien mati duluan; server lanjut memproses tanpa konsumen, artefak mungkin tidak tersimpan | cek output dir + queue dulu; bila artefak hilang, jalankan ulang iterasi itu (pola chain2 server-per-iterasi) |
| Varian yang SAMA lolos di run pertama tapi FAIL di run ke-2/3 server yang sama | **VRAM kumulatif antar-run** dalam satu proses server (cache-lru menahan intermediate; baseline alokasi naik pelan). Bukti: L08 lolos @13,1GB lalu L09 (input sama) OOM di shape 13,09+1,30 di server yang sama | rantai produksi = **satu server per iterasi** (chain2.sh: start server -> 1 run -> taskkill). Rantai multi-run hanya untuk eksplorasi murah |

## Bukti keberhasilan (referensi silang)
- SM-09 kamera: GLB 860 KB, pipeline 38 dtk, full load True (log).
- v6 satelit: GLB 1,08 MB, 8/30, pertama dengan geometri satelit terbaca
  (body emas + panel biru), artefak + ledger di docs/2026-09-01-comfyui-slide-stack/smoke/satelit_loop/.
