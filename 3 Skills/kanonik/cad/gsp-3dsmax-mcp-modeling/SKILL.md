---
name: gsp-3dsmax-mcp-modeling
description: >
  Pola wajib build 3D lewat MCP 3ds Max (MAXScript + Arnold GPU). Muat SEBELUM
  tugas modelling/appliance/product render via 3dsmax-mcp: berisi katalog fungsi
  yang SUDAH terbukti gagal di host ini (dilarang uji ulang — buang waktu), resep
  yang terbukti jalan, dan STANDAR DETAIL MINIMAL objek. GUNAKAN ketika: build
  model produk, exploded/disassembly motion, camera fly, text spec display,
  batch render klip, QC render. Jalur Blender bpy tetap di cad-3d-visualization;
  tangga koneksi bridge di mcp-app-bridge-prep.
version: 1.0.4
metadata:
  origin: distilasi penuh misi DEMS appliance 0930 + Edge Client 0930b (30-09 s.d. 01-10-2026), semua butir terukur di sesi nyata
  gsp-owner-profile: gsp-master
  gsp-relations: [mcp-app-bridge-prep, cad-3d-visualization, gsp-verification-before-completion]
  host: Windows, 3ds Max 2027, Arnold GPU (RTX 5070 Ti), safeMode bridge ON
---

# 3ds Max MCP Modeling — Katalog Fakta & Standar Detail

Aturan main: **jangan menguji ulang apa pun di Katalog Gagal** — semuanya sudah
dibuktikan mati di host ini dengan pesan error spesifik. Pilih langsung resep
pengganti dari Katalog Jalan.

## A. KATALOG GAGAL (jangan diuji ulang; pakai pengganti di §B)

### A1. Sintaks/bahasa MAXScript
1. `local` di top level file `fileIn` → compile error. Bungkus SELURUH isi dalam satu blok `(...)`.
2. Lambda anonim `fn () (...)` → syntax error. MAXScript hanya `fn` bernama; pola materi: `fn findMat nm mk` + fallback buat baru.
3. `case of` dengan lengan ekspresi boolean → syntax error. Pakai rantai `if/else if`.
4. `for o in objects do where cond` invalid; bentuk benar `for o in objects where cond do`.
5. `#{...}` = himpunan integer saja; array titik/tuple pakai `#(...)`.
6. `max`/`min` sebagai fungsi dalam ekspresi sering tertafsir command → pakai `if a < b do b = a` eksplisit.
7. `showProperties` mengembalikan boolean (cetak ke listener), BUKAN daftar; enumerasi properti pakai `getPropNames obj`.
8. `getClassInstances Material` → Type error (butuh kelas konkret); pakai `getClassInstances PhysicalMaterial`.
9. `o.bounds` tak tersedia pada banyak kelas; pakai `o.min` / `o.max`.
10. `.children` pada Point helper kosong; `getChildren` undefined di safeMode; enumerasi anak = `for o in objects where o.parent == g`.
11. `numKeys node idx` tidak andal lintas jenis controller (kembalikan 0 padahal keyframe ada). Verifikasi motion = EVALUASI `pos` pada waktu uji, bukan hitung key.
12. `at time f` statement tunggal tanpa badan = NO-OP (waktu tidak berubah). `at time f ( ... )` MEMULIHKAN waktu lama saat keluar blok → batch beku. Satu-satunya penulis waktu andal: `sliderTime = f`.
13. `.pos` = ruang-PARENT setelah ber-parent (bukan dunia). Dunia = rantai `pos * parent.transform` ke akar.
14. `.parent = x` TIDAK preservasi transform dunia: nilai `.pos` lama diinterpretasi ulang di ruang parent → objek bergeser sebesar offset parent. Dampak terukur: detail port tergeser ganda jadi "kapsul melayang".
15. `.rotation = angleaxis...` pada objek yang sudah diposisikan memutar PIVOT mengelilingi origin dunia → posisi ikut berpindah. Resep: buat di `[0,0,0]`, set rotasi, BARU set `.pos`.
16. `PhysicalMaterial base_color:[0.9,0.9,0.92]` → error konversi Point4. Wajib `base_color:(color 230 230 235)` (0-255).
17. Kata kunci: loop `for i in a to b by s` (bukan step); `off` reserved; `let` tidak ada; ekspresi tak boleh terpotong baris; `(x as integer) as string` wajib kurung.
18. Fungsi yang memanggil fungsi lain terikat saat kompilasi → `fileIn` dependency DAHULU (urutan rantai penting).

### A2. SafeMode bridge menolak (pakai jalur MCP)
19. `convertToType o Editable_Poly` → ditolak; `convertToMesh o` → diterima.
20. `deleteModifier` → ditolak; buang modifier via MCP `remove_modifier`. Efek samping: slot material ikut lepas → pasang ulang materi.
21. `createFile` (IO tulis) → diblokir; kembalikan string hasil via balikan tool.
22. `getModCount` → diblokir; introspeksi via `inspect_object` MCP.
23. Iterasi `layerManager` terbatas; pakai `layerManager.count` + indeks, atau `manage_layers` MCP.
24. Assignment `visibility.controller` → ditolak; lihat A3-31 untuk pola state.
25. Konstruktor lampu `Direct`, `TargetDirect`, `Omni` → ditolak. Yang hidup: `Free_Area`, `Skylight`.
26. Konstruktor `PhysicalCamera`, `TargetCamera` → ditolak. Yang hidup: `freeCamera`. Konsekuensi: TIDAK ada properti DOF (`dofEnabled`/`lensAperture`) di kamera build ini; fokus kamera = `fov` + jarak fisik, bukan aperture.

### A3. Perilaku render/Arnold
27. Inline `render camera:$X outputFile:... vfb:false` → berkas LINEAR kusam (bukti final DILARANG). Yang tajam = jalur VFB tone-mapped.
28. `saveImg` bentuk posisi → berulang gagal + dialog modal `Image I/O Error` menyumbat thread utama. Jangan pernah simpan via saveImg.
29. Render >±2 menit menutup pipa MCP; `Connection closed` BUKAN berarti render berhenti — render lanjut di Max. Pulihkan: hitung berkas di disk, resume dari frame berikutnya (penamaan per-frame idempoten).
30. MCP `render_scene` TIDAK membuat folder induk output → mkdir dulu, selalu.
31. Keyframe `.visibility` TIDAK ditegakkan Arnold pada jalur render inline; `.renderable` tidak bisa di-key (boolean tanpa controller). Solusi resmi: FUNGSI STATE per-frame (lihat B6).
32. Arnold "3ds Max Maps Support" aktif → render dipaksa CPU (20+ menit/frame). Matikan agar OptiX GPU (~1 menit/frame 4K).
33. `max render` bukan aksi valid; `max quick render` valid tapi ikut setting viewport/Time Output (tak cocok kontrol multi-frame).
34. Properti preset output namanya `renderOutputFile` (bukan `renderOutputFilename`).
35. Body area light masuk frustum → tampil sebagai patch gelap di latar. Lampu selalu DI LUAR cone kamera; dinding studio `receive_shadows=false`, lantai tetap `true`.
36. Boolean modifier pada pelat tipis + objek sebidang → artefak Z-fighting pink. Buang pelat duplikat/Boolean (via remove_modifier), pakai panel solid + port menonjol.
37. Teks Shape: `render_thickness` default 0 → tak muncul di render walau viewport terlihat. Set 0.3 DAN `convertToMesh`.
38. Materi emissive yang dibagikan (mis. Text_white) jangan dinaikkan emission-nya untuk kartu spek — menular ke objek lain (LCD jadi blok solid). Buat materi KHUSUS per kelas keluaran.

### A4. Pola panggilan tool
39. Tool yang sudah tampil di daftar langsung (`get_bridge_status`, `get_object_info`, dsb.) dilarang lewat `tool_call`/`tool_describe` → error "not a deferrable tool".
40. `tool_call` `arguments` harus objek JSON valid (bukan string tersalin); `describe_toolset` parameternya `toolset` (bukan `name`).
41. Skema benar `render_scene`: `width`, `height`, `output_path`.
42. `viewport.SetType #view_camera` memicu dialog modal `Select Camera` → blokir bridge. Pakai `viewport.SetCamera camNode`.
43. Kamera freeCamera build ini mengekspos `fov`, BUKAN `focalLength`.
44. Helper aim custom menerima NODE kamera, bukan titik posisi.
45. `key.tangentType` tunggal → Unknown property; yang benar `key.inTangentType`/`key.outTangentType`. `pc.xcontroller` juga tidak ada; akses sub-track `pc[1..3]`.
46. `keyframe_tracks action:style` dengan `tcb.easeIn/easeOut > 100` → ditolak senyap (`styledKeys: 0`, tanpa error). Jangan percaya success tanpa cek counter.
47. `deleteKeys node #all` → Unrecognized flag; MAXScript tidak bisa hapus lintas track. Pakai MCP `keyframe_tracks action:delete_keys` dengan `track_paths: ["[#Transform]"]` + `from_time/to_time` WAJIB (tanpa batas: "refusing an unbounded edit").
48. `normalize_tangents` juga menuntut rentang waktu; hasil default-nya Bezier smooth — TIDAK memberi rasa "tenang" pada shot dwell; solusi = kunci posisi sama berulang + #slow (B10).

## B. KATALOG JALAN (resep terbukti, pakai langsung)

### B1. Build geometri
- Semua geometri lewat berkas `.ms` + `fileIn` (deterministik, bisa di-rerun, hemat token). Simpan tiap skrip misi di `scripts/cad-build/<slug>/`.
- Helper box center: `box ... pos:[x,y,z]` lalu koreksi tinggi bila pivot bottom-center; silinder berorientasi: buat di origin → rotasi → set pos (A1-15).
- Lubang panel: MCP `boolean_operation`; jika hasil berartefak → `remove_modifier` + panel solid + port menempel menonjol.
- Layer: MCP `manage_layers` aksi `add_objects`.

### B2. Kamera & studio
- `freeCamera` + helper `aimNode` (matriks xa/ya/za dari dir-up) + `fov` derajat.
- Hero produk desktop 280×240: jarak ±600 mm, fov 30-32; exploded ±1000 mm, fov 34; macro zona: jarak 400-500 mm dari target, fov 26-30.
- Lampu: `Free_Area` key/fill/top/rim di luar frustum + `Skylight` 0.35; fill khusus zona macro dengan multiplier ter-key (0 → 0.9 hanya jendela macro).

### B3. Teks render-able
`text` → `render_thickness = 0.3` → `rotate (angleaxis 90 [1,0,0])` untuk muka -Y (muka +Y tambah `rotate 180 [0,0,1]` agar tidak mirror) → `convertToMesh` → pasang materi. Orientasi front/rear wajib diuji render, bukan viewport.

### B4. Render tunggal resmi
MCP `render_scene` (width/height/output_path) — tajam, tone-mapped, folder harus ada.

### B5. Batch klip inline (multi-frame, kontrol penuh)
```
rendTimeType = 1
viewport.SetCamera cam ; redrawViews()
sliderTime = f            -- LANGSUNG, tanpa blok at time
EC_STATE_F f              -- saklar renderable per frame (B6)
redrawViews()
render outputWidth:W outputHeight:H vfb:true outputFile:path
```
Batch aman ≤32 frame/panggilan (1280×720 GPU ±50 dtk). Bila pipa putus: cek jumlah berkas di disk, lanjut dari frame hilang.

### B6. State visibilitas per-frame (satu-satunya yang ditegakkan Arnold)
```
fn EC_STATE_F f = (
  local expl = (f >= 100 and f <= 270)        -- jendela exploded
  local macroWin = (f >= 138 and f <= 242)    -- jendela macro
  for o in objects where matchPattern o.name pattern:"WIRE_*" do
    o.renderable = (not expl)
  for o in objects where o.parent != undefined and o.parent.name == "EXP_FRONT" do
    o.renderable = (not macroWin)
)
```
Panggil sebelum render TiAP frame dan sebelum menyimpan state manual.

### B7. Hierarki exploded & motion
- Grup `EXP_*` = `point` helper di `[0,0,0]` TANPA rotasi (identitas). Parent detail baru ke grup ini = nol koreksi transform (A1-14).
- Keyframe: `with animate on ( at time f ( g.pos = v ) )` — satu-satunya penulis kunci andal.
- Siklus penuh: assembled f1 → hold → exploded f130 → hold → assembled f240-290 → final f300. Verifikasi dengan evaluasi posisi per waktu (bukan numKeys).
- Kabel ikut grup statis/power; JANGAN parent ke pelat ber-offset.

### B8. Preset output master
`rendTimeType = 4` (Active Time Segment), `renderResHorizontal/Vertical`, `renderVpAspect=false`, pola sequence PNG, GPU on, fps tercatat.

### B9. Encode klip
`ffmpeg -framerate N -i %04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 out.mp4` (renomorasi rapat dulu bila langkah frame >1).

### B10. Penghalusan motion (resep koreografi v2, terukur 01-10-2026)
- Reset total keyframe lama sebelum koreografi ulang: MCP `keyframe_tracks action:delete_keys` WAJIB disertai `from_time`/`to_time` (edit tanpa batas ditolak). Track path lengkap: `[#Transform]`; track parameter lampu: `[#Object (Free Rectangle)][#Basic Parameters][#Multiplier ]` (perhatikan spasi trailing di nama).
- Akses key Bezier Float: `pc = o.pos.controller; pc[si].keys[i]` (si=1..3). Properti key yang ADA: `inTangentType`, `outTangentType`, `value`, `time` — `tangentType` tunggal TIDAK ada. `pc.xcontroller` juga tidak ada di build ini.
- Pola tangen: `#slow` untuk objek dengan fase hold (EXP_*, kartu spek) — kecepatan nol di kedua ujung, hold benar-benar datar; `#smooth` HANYA untuk lintasan kontinu tanpa hold.
- Dwell kamera yang nyaman = kunci-posisi-SAMA berulang tiap ±20 frame + tangen #slow pada track pos DAN rotation. Kamera `#smooth` murni saat kartu tampil = drift melayang yang terasa "tidak tenang" (temuan user: kurang nyaman dilihat).
- `keyframe_tracks action:style` dengan `tcb easeIn/easeOut > 100` → `styledKeys: 0` senyap (valid hanya ≤100). Jangan andalkan TCB untuk ease kuat; pakai tangen #slow eksplisit.
- Verifikasi easing secara NUMERIK, bukan visual saja: sampel `sliderTime = f; o.pos.z` di beberapa titik (mis. 88,90,95,110,125,145,150) — harus 0 → kecil → besar → kecil → target (bentuk S).
- Stagger disassembly: tiap modul start bergeser 6 frame dan durasi berbeda (60-102 f) sehingga gelombang terbuka; assembly memakai URUTAN TERBALIK (modul dalam menutup dulu, pelat lalu cover) — cover paling akhir duduk.
- Jeda baca (aturan ritme untuk audiens, @30fps): kartu spec dwell ≥105 frame (3.5 dtk) dengan fade-in 12f naik 8mm + fade-out 12f; antar-kartu diberi jarak transisi kamera ≥24f; satu hold komposisi lebar tanpa teks 2 dtk setelah ledakan selesai ("napas") sebelum masuk macro; hero awal/akhir ≥3 dtk. Total film produk ±35 dtk terasa lega; 15 dtk penuh sesak.
- Kartu teks muncul-hilang: animasi `.scale` (0.001↔1) + naik 8mm; tangen scale juga #slow.

### B11. Film produk multi-babak (resep arsitektur film, terukur 01-10-2026)
- SATU CAM_FLY untuk semua babak; koreografi lama didaur ulang via MCP `keyframe_tracks action:move_keys` (`time_offset`, `track_paths: ["[#Transform]"]`, `from_time/to_time` wajib) — JANGAN geser key satu-per-satu (Position_XYZ menolak `k.time =`).
- Track parameter (fov, multiplier lampu): `c.keys[i].time = c.keys[i].time + off` BEKERJA (bedanya dengan sub-track pos yang menolak).
- Arah pandang = kunci `fly.transform = matrix3 xa ya za p` eksplisit per waktu; Euler/quat antar-bantalan panjang MELAYANG (kamera menatap langit = frame hitam). untuk transisi >800mm antar target: kisi kunci tiap 6 frame dari tabel target terinterpolasi.
- `acos(dot(...))` MAXScript SUDAH derajat — jangan kalikan 180/pi (terskala 57×, panic palsu).
- Uji framing NUMERIK sebelum render: proyeksi pusat kartu/perangkat ke basis kamera (fwd/side/vert vs tan(fov/2)*fwd, margin 0.78) + uji oklusi sinar cam→target vs bbox semua perangkat. Render = biaya; angka = murah.
- Kartu teks layar: JANGAN parent grup + scale-key (pivot default bottom-center + key scale = objek meledak ribuan mm). Bangun tanpa-parent di koordinat dunia via matrix3 baris-eksplisit (row1=kanan,row2=atas,row3=normal ke kamera), teks `convertToMesh`, dan jendela tampil via FUNGSI STATE per-frame (`renderable`), bukan key.
- Teks judul besar per-huruf: buat + kunci f1 di POSISI BIDANG DINDING dulu (pivot mesh teks = tepi kiri-bawah, bukan tengah — koreksi geser -w/2 untuk centering; `o.center =` pada mesh TIDAK memindahkannya).
- Merge .max lintas scene: `merge_from_file duplicate_action:rename` memicu dialog "Duplicate Material Name" MENYUMBAT thread — jalankan pengawas dialog (EnumWindows pid 3dsmax + BM_CLICK 'Apply to All Duplicates'+'Use Merged Material' via SendMessageTimeout) SEBELUM merge; timeout pipa BUKAN kegagalan merge — verifikasi dari `objects.count` + `selection` (merge men-seleksi hasil).
- Bangun berkas panggung sumber TERLEBIH DAHULU (buang scene/lampu/kamera/callout lama, bunuh key, simpan sebagai *_Stage.max) lalu merge — bukan merge mentah.
- `.min/.max` objek = SUDAH ruang-dunia; `p * tm` lagi = dobel (bbox fantom 951×1038). Ukur bbox dunia = langsung `.min/.max`.
- Batch render klip panjang: langkah 2 frame, ≤400 frame/panggilan fileIn, vfb:true outputFile:, pantau dari DISK (pipa mati = render lanjut). `getTicks()` TIDAK ADA di MAXScript — skrip batch yang memakainya mati senyap di baris pertama; ukur laju dari mtime disk. Laju terukur 02-10: 1080p GPU ±13 frame/menit (lebih CEPAT per-pixel dari 720p ±6 f/mnt — OptiX efisien; resolusi sedang bukan mahal).
- RESEP KAMERA SENYAP v4 (vonis user 'banyak unnecessary movement', 02-10): kunci kamera lama = 354/track (kisi aim 6f + dwell 24f); v4 = 86/track (−76%) dengan prinsip: komposisi DIAM total selama teks/huruf bekerja (hold kunci sama tiap 20-30f), SATU transit antar-blok, tanpa orbit hero, tanpa creep antar-dwell, tangen #slow semua track (pos+rot+fov). FOV juga WAJIB di-hold dengan kunci bernilai sama — fov #smooth antar dua nilai berbeda = zoom drift sepanjang dwell (terasa bergerak walau posisi diam).
- JANGAN membangun ulang koreografi dari skrip GENERATOR pertama (mis. mastercam awal) — pose final hidup di pass REPAIR terakhir (cards6 dst: kartu v6 + dwell v8 + bias aim 0.30 + fov 42-48). Rekonstruksi dari generator salah = kartu terpotong + label billboard keluar bingkai (label melayak dihitung thd kamera hold; ganti pose kamera ⇒ pasang ulang label SETELAH kamera final, pola floatlabel). Urutan wajib revisi kamera: buang semua key (MCP delete_keys tracks:all) → re-key dari tabel plan pass FINAL → probe numerik nilai aktual di sliderTime uji → render QC per jendela → baru batch.
- delete_keys MCP `tracks:"all"` TIDAK menyentuh track parameter (fov/multiplier) — kunci fov sisa menimpa nilai baru (terukur: APPL fov 48 tertimpa 40 oleh key generator lama). Hapus kunci parameter per-indeks MAXScript: `for idx = c.keys.count to 1 by -1 do if (k.time >= t0 and k.time <= t1) do deleteKey c idx`. Loop `while ... do ( ... )` inline via execute_maxscript: increment HARUS di dalam badan kurung — increment di luar = parse error.
- `deleteKeys coll tsArray` (array waktu) GAGAL SENYAP pada controller Position XYZ/Euler build ini (del=0 tanpa error) — selalu deleteKey per-indeks dari key terakhir. Setelah re-key, SELALU verifikasi membaca nilai aktual di waktu uji (`sliderTime = t; fly.pos`) dan bandingkan target — `with animate on at time` bisa tidak menggigit bila ada kunci lain yang tertinggal di rentang sama.
- LABEL BABAK di dinding panggung sering GAGAL framing (kamera pitch turun + fov sempit + dinding jauh): jangan tambal posisi buta. Solusi terbukti: TITLE-BAR MELAYAK billboard — `p = camPos + fwd*DIST + up*RISE` (DIST≈1500, RISE≈200 untuk pita atas), `o.transform = matrix3 row1 row2 row3 p` paralel bidang gambar kamera hold, materi emissif (M_TITLE), jendela state dipersempit ke masa hold saja. Uji 2-3 kamera jendela @640×360 dulu (murah), baru render ulang frame terdampak @full-res, cek STALE per mtime.

## C. STANDAR DETAIL MINIMAL (FLOOR — rilis di bawah ini = FAIL QC)

Acuan ukur: Edge Client final 610 objek dan appliance 2U 645 objek (vonis PASS user 01-10-2026). Produk sekelas appliances/elektronik konsumen WAJIB ≥ angka lantai; DIANJURKAN melebihi.

| Kelas | Lantai minimal |
|---|---|
| Total objek | ≥ 600 (produk multi-zona); ≥ 400 (produk 1 zona) |
| Chassis | dinding+sekat+tray+standoff+foot+cover lepas-pasang; sekrup individual ≥ 12 dengan kepala (cross/hex); ventilasi louvre/perforasi ≥ 20 |
| Panel depan | tumpukan LCD lengkap: bezel + panel + kaca + teks UI emissive ≥ 6 baris; LED status ≥ 5 (materi emissive warna berbeda + light-pipe); tombol ≥ 4 kepala terpisah; engraving/label merek |
| Port belakang | SETIAP konektor berstruktur internal: RJ45 = shell+tongue+8 pin emas; XLR = 3 pin+cincin+latch; USB = lidah+4 kontak; terminal block per-sekrup; SMA emas; fuse drawer; tombol recessed. Pin emas total ≥ 8 per port jaringan |
| PCB | chip per komponen nyata (RAM 8/modul, IC per fungsi, kapasitor bervariasi ukuran, trafo, relay, DIP switch, LED, coin cell+holder); konektor on-board; label zona |
| Kabel | tersimpan per kelas warna (AC/PoE/DC/SATA/ETH/audio/RF/GPIO), segmen+junction, aturan pisahkan audio dari power; state tersembunyi saat exploded |
| Label | barcode + QR + strip serial pada cover/panel (bar ≥ 20, sel QR ≥ 16) |
| Materi | ≥ 30 PBR unik: powder-coat, alu brushed, emas, nikel, tembaga, PCB hijau/biru, karet, plastik, emissive per warna LED, kaca |
| Kamera | ≥ 9: hero 3/4, front, rear, top, exploded, macro ≥ 3 zona, fly |
| Lampu | ≥ 5: key/fill/top/rim (di luar frustum, cast_shadows off) + skylight + fill zona |
| Motion | siklus disassembly→assembly dua arah dengan STAGGER (start antar-modul geser ≥4f, durasi berbeda; assembly urutan terbalik); grup EXP ≥ 6 ber-keyframe; state kabel per-frame; camera fly ≥ 5 shot; DWELL steady tiap shot macro ≥3.5 dtk (kunci posisi sama berulang + tangen #slow — kamera diam saat kartu terbaca); satu hold komposisi lebar tanpa teks ≥2 dtk setelah ledakan; kartu teks spec per zona + envelope (konten dari dokumen, bukan karangan) dengan fade 12f + jeda antar-kartu ≥24f; hero awal/akhir ≥3 dtk. Total durasi produk ≥30 dtk @30fps |
| Render | QC 960×540 per frame kunci + tinjau vision (cacat=0 sebelum serah); final 4K hero/rear/exploded; klip bukti gerak ter-encode |
| File | checkpoint .max disimpan per fase; QC diukur dari DISK (loadMaxFile), bukan memori sesi |

DIANJURKAN (di atas floor, hasil gap-audit): chamfer/bevel tepi chassis, jejak tembaga+silk PCB, UI LCD bitmap, normal map brushed, guide line exploded, motion blur ringan, annotation dimensi.

## D. ALUR KERJA WAJIB (urut)
1. Muat skill ini + `mcp-app-bridge-prep` (tangga 7 lapis; jangan lewati layer "app process running").
2. Set unit mm SEBELUM build; konfirmasi Z-up + konvensi pivot.
3. Blueprint objek per zona dari dokumen spek (dimensi/nama port/konten label diambil VERBATIM dari dokumen).
4. Build per skrip bertahap (chassis→panel→komponen→detail pass→kabel→scene→motion), tiap tahap `fileIn` + hitung objek.
5. Rantai fix SELALU dari muat ulang disk (`loadMaxFile`) agar deterministik; jangan tambal di sesi terkontaminasi.
6. QC: batch uji 6 frame kunci (hero/mid/macro×3/assembly) → vision → tambal → ulang sampai cacat 0.
7. Produksi: render_scene 4K final + batch klip ≤32 frame + ffmpeg.
8. Simpan .max + laporan QC (angka dari disk) + tutup dengan tabel hasil ukur.
