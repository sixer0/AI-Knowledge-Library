# -*- coding: utf-8 -*-
"""DATA CONTOH SINTETIS BEKU - VCTL-1007 C2.

Semua angka di berkas ini SYNTHETIC (bukan data proyek GSP nyata), konteks
teknis ala dokumen GSP (beban jaringan, arus, harga, jadwal). Seed tunggal
dibekukan: SEED=42. Perubahan apa pun pada berkas ini mengubah keluaran
render dan wajib memicu render ulang penuh + RENDERCHECK baru.
"""
import numpy as np

SEED = 42
RNG = np.random.default_rng(SEED)

# --- pengadaan / harga (juta Rp) ---
PERANGKAT = ["Kamera 4MP", "NVR 24-ch", "Switch PoE+", "Kabel UTP CAT6", "Jasa pasang"]
HARGA = [412.5, 380.0, 255.75, 96.4, 140.0]                 # juta Rp
HARGA_B = [388.0, 402.5, 231.2, 104.9, 155.0]               # penawaran vendor B
VENDOR = ["Vendor Alfa", "Vendor Bravo"]

# --- anggaran komposisi (%) ---
ANGGRAN = [("Hardware", 52), ("Jasa instalasi", 28), ("Lisensi", 14), ("Lainnya", 6)]

# --- deret waktu ---
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
         "Jul", "Aug", "Sep", "Okt", "Nov", "Des"]
TAHUN = ["2022", "2023", "2024", "2025", "2026"]
BITRATE_A = np.round(4.0 + np.cumsum(RNG.normal(0.15, 0.25, 12)), 2).clip(0, 6)
BITRATE_B = np.round(2.5 + np.cumsum(RNG.normal(0.05, 0.20, 12)), 2).clip(0, 6)
BITRATE_C = np.round(3.1 + np.cumsum(RNG.normal(0.02, 0.30, 12)), 2).clip(0, 6)
BITRATE_D = np.round(5.2 - np.cumsum(RNG.normal(0.08, 0.22, 12)), 2).clip(0, 6)
VOLUME_PROYEK = np.round(RNG.uniform(20, 60, 5), 0)          # unit/tahun

# --- beban listrik / arus ---
PANEL = ["Panel L1", "Panel L2", "Panel L3", "Panel genset"]
ARUS_NOMINAL = [63.0, 40.0, 32.0, 80.0]                      # A
ARUS_TERUKUR = [51.2, 36.8, 18.4, 0.0]                       # A
BEBAN_KW = np.round(RNG.uniform(2.0, 14.0, 12), 1)           # kW per bulan

# --- kualitas layanan / distribusi ---
SITE = ["Site A", "Site B", "Site C"]
MTBF = [RNG.normal(m, s, 80) for m, s in [(30, 4), (34, 5), (33, 3)]]   # jam
LATENSI = RNG.lognormal(3.2, 0.45, 500)                      # kbps-ish -> pakai utk hist
PING_MS = RNG.gamma(2.2, 9.0, 400)                           # ms RTT
SLA_PCT = RNG.normal(97.5, 1.4, 300).clip(80, 100)           # % ketersediaan

# --- pareto penyebab gangguan ---
PENYEBAB = ["Fokus lensa", "PoE drop", "Konfigurasi IP", "Kabel rusak", "Lainnya"]
KEJADIAN = [46, 22, 14, 9, 7]

# --- matriks skor (site x faktor uji) ---
FAKTOR = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"]
SKOR_M = np.round(RNG.uniform(0, 1, (6, 8)), 2)
NAMA_SITE6 = ["Site-1", "Site-2", "Site-3", "Site-4", "Site-5", "Site-6"]

# --- dua waktu untuk slope/dumbbell (skor audit H1 vs H2 2026) ---
AUDIT_OBJEK = ["RT-01", "RT-02", "RT-03", "RT-04", "RT-05", "RT-06"]
AUDIT_H1 = [62, 74, 55, 81, 68, 59]
AUDIT_H2 = [71, 69, 66, 88, 64, 77]

# --- survei kepuasan diverging (setuju vs tidak setuju, %) ---
SURVEI_ASP = ["Kehandalan", "Respon tiket", "Dokumentasi", "Harga", "Komunikasi"]
SETUJU = [58, 47, 39, 31, 66]
TIDAK_SETUJU = [-14, -27, -34, -45, -18]

# --- piramida (tenaga kerja per jenjang) ---
JENJANG = ["Teknisi", "Engineer", "Senior", "Spesialis", "Manajer"]
FRONT_END = [42, 28, 17, 9, 4]
BACK_END = [36, 25, 19, 11, 5]

# --- waffle / share 100 titik ---
WAFFLE_PARTS = [("Terpenuhi", 62), ("Susut", 23), ("Belum uji", 15)]

# --- square area / icon proporsional (jumlah titik kamera per site, ratusan) ---
KAMERA_SITE = [("Gedung Pusat", 420), ("Gudang Utara", 180), ("Cabang Timur", 95), ("Depot Selatan", 30)]

# --- marimekko: segmen pasar proyek (lebar=porsi tender, tinggi=mix menang) ---
MARIMEKKO = {  # kategori: (porsi tender %, [(bagian %, warna-indeks)])
    "Surveilans": (38, [("Menang", 55), ("Kalah", 45)]),
    "Fiber":      (27, [("Menang", 40), ("Kalah", 60)]),
    "Daya cadangan": (21, [("Menang", 65), ("Kalah", 35)]),
    "Lainnya":    (14, [("Menang", 30), ("Kalah", 70)]),
}

# --- treemap dua tingkat: biaya per divisi-subpaket (juta Rp) ---
TREEMAP = [
    ("Proyek VSS", [("Kamera", 190.0), ("NVR+Storage", 120.5), ("Instalasi", 88.0)]),
    ("Proyek Fiber", [("ODC+Patchcord", 74.2), ("Penarikan kabel", 96.0), ("Terminasi", 31.5)]),
    ("Proyek Daya", [("UPS 10kVA", 145.0), ("Panel+Kabel", 52.8), ("Genset", 210.0)]),
]

# --- sunburst dua tingkat: status tiket per kanal ---
SUNBURST = [
    ("Tiket selesai", [("Onsite", 120), ("Remote", 210)]),
    ("Tiket berjalan", [("Onsite", 34), ("Remote", 58)]),
    ("Tiket tertunda", [("Onsite", 12), ("Remote", 26)]),
]

# --- funnel proses pengadaan (jumlah dokumen lolos tahap) ---
FUNNEL = [("Dokumen masuk", 120), ("Verifikasi teknis", 86), ("Verifikasi harga", 54),
          ("Evaluasi akhir", 23), ("Kontrak terbit", 9)]

# --- dendrogram: kemiripan profil beban antar gardu (jarak euklidesan beku) ---
DENDRO_LEAF = ["GI-A", "GI-B", "GI-C", "GI-D", "GI-E", "GI-F"]
DENDRO_TREE = [  # (child_i, child_j, jarak) - pohon tetap, bukan hasil solver
    (0, 1, 0.8), (2, 3, 1.1), (5, 6, 1.6), (4, 7, 2.3),
]

# --- org chart (struktur project office) ---
ORG = {
    "root": ("Site Manager", [("Lead Instalasi", ["Teknisi A", "Teknisi B"]),
                              ("Lead Konfigurasi", ["Engineer NOC"]),
                              ("Lead QC", ["Inspektur"])]),
}

# --- network: topologi distro (node tetap, edge tetap) ---
NET_NODES = {  # nama: (x, y)
    "Core": (0.50, 0.78), "DS-1": (0.22, 0.52), "DS-2": (0.50, 0.52), "DS-3": (0.78, 0.52),
    "ACC-1": (0.12, 0.22), "ACC-2": (0.32, 0.22), "ACC-3": (0.42, 0.22),
    "ACC-4": (0.58, 0.22), "ACC-5": (0.68, 0.22), "ACC-6": (0.88, 0.22),
}
NET_EDGES = [("Core", "DS-1"), ("Core", "DS-2"), ("Core", "DS-3"),
             ("DS-1", "ACC-1"), ("DS-1", "ACC-2"), ("DS-2", "ACC-3"),
             ("DS-2", "ACC-4"), ("DS-3", "ACC-5"), ("DS-3", "ACC-6")]
NET_LINK_UTAMA = ("Core", "DS-2")

# --- flowchart alur triase tiket (tetap) ---
FLOW = {
    "steps": [("box", "Tiket masuk"), ("box", "Klasifikasi kelas"),
              ("dia", "P1/P2?"), ("box", "Dispatch teknisi"),
              ("box", "Antre terjadwal"), ("box", "Resolusi + BAP")],
    "edges": [(0, 1), (1, 2), (2, 3, "Ya"), (2, 4, "Tidak"), (3, 5), (4, 5)],
}

# --- tile map: denah gudang 8x6 zona, skor cakupan wifi (%) ---
TILE_ROWS = 6
TILE_COLS = 8
TILE_SCORE = np.round(RNG.uniform(35, 98, (TILE_ROWS, TILE_COLS)), 0)
TILE_LABEL = {  # (baris, kolom): kode zona
    (0, 0): "DOK", (1, 3): "RAK-A", (2, 6): "RAK-B", (4, 1): "BONGKAR",
    (5, 7): "OUT", (3, 4): "OPS",
}

# --- gantt jadwal proyek (minggu ke-) ---
GANTT = [  # (tugas, mulai_minggu, durasi_minggu)
    ("Survey lokasi", 0, 2), ("Desain detail", 1, 3), ("Pengadaan alat", 2, 5),
    ("Instalasi kabel", 5, 4), ("Pasang perangkat", 8, 3), ("Konfigurasi", 10, 2),
    ("Uji terima (FAT/SAT)", 11, 2),
]
GANTT_MILESTONE = (13, "Serah terima")

# --- control chart: % ketersediaan harian, CL/UCL/LCL ---
CTRL = np.round(RNG.normal(97.5, 0.9, 30), 2)
CTRL[22] = 94.1  # pelanggaran bawah
CTRL_CL = 97.5
CTRL_SIGMA = 0.9

# --- waterfall RAB (sama dgn resep r5) ---
WATERFALL = [("Peralatan", 412.5), ("Instalasi", 140.0), ("Konfigurasi", 96.4),
             ("Lisensi", 55.0), ("Diskon", -23.9)]

# --- bullet: SLA vs target ---
BULLET = {"label": "SLA penyelesaian tiket Q3", "value": 72.0, "target": 80.0, "max": 100.0}

# --- scatter: harga vs throughput 24 paket perangkat keras ---
SCAT_X = np.round(RNG.uniform(2, 60, 24), 1)                # harga juta Rp
SCAT_Y = np.round(3.0 + 0.9 * SCAT_X + RNG.normal(0, 6, 24), 1)  # throughput Mbps
SCAT_SIZE = np.round(RNG.uniform(1, 12, 24), 1)             # garansi (tahun) -> bubble
SCAT_ANNOT = {0: "Kit A", 7: "Kit B", 15: "Kit C", 22: "Kit D"}

# --- connected scatter: trajektori latency vs jitter per jam ---
CS_X = np.round(np.linspace(8, 60, 16), 1)                  # latency ms
CS_Y = np.round(2 + 0.35 * CS_X + RNG.normal(0, 2.5, 16), 1)  # jitter ms

# --- categorical scatter: umur baterai UPS per merek (jam backup) ---
CAT_SCAT = {"Merek X": RNG.normal(1.8, 0.25, 22), "Merek Y": RNG.normal(2.3, 0.4, 22),
            "Merek Z": RNG.normal(1.5, 0.3, 22)}

# --- contour: peta kepadagan sinyal dBm area parkir (medan analitik beku) ---
def medan_sinyal(X, Y):
    p1 = np.exp(-((X - 2.5) ** 2 + (Y - 3.0) ** 2) / 2.2)
    p2 = 0.7 * np.exp(-((X - 7.0) ** 2 + (Y - 1.5) ** 2) / 1.6)
    return 100 * (p1 + p2)

# --- fan chart: proyeksi pertumbuhan titik kamera (p10..p90) ---
FAN_TAHUN = np.arange(2026, 2032)
FAN_MED = np.array([420, 470, 528, 590, 655, 720], dtype=float)
FAN_LO1 = FAN_MED * np.array([1, .96, .94, .925, .915, .908])
FAN_HI1 = FAN_MED * np.array([1, 1.05, 1.08, 1.105, 1.122, 1.135])
FAN_LO2 = FAN_MED * np.array([1, .92, .88, .855, .838, .826])
FAN_HI2 = FAN_MED * np.array([1, 1.10, 1.16, 1.205, 1.24, 1.268])

# --- bump chart: peringkat vendor kuartalan (1 = terbaik) ---
BUMP_KV = ["Q1-26", "Q2-26", "Q3-26", "Q4-26"]
BUMP_SERI = {"Alfa": [3, 1, 2, 1], "Bravo": [1, 2, 1, 3], "Cakra": [2, 4, 3, 2],
             "Dharma": [5, 3, 4, 5], "Echo": [4, 5, 5, 4]}

# --- small multiples: tren bitrate 6 site (facet) ---
SM_MULT = {s: np.round(RNG.uniform(1, 6, 12), 2) for s in
           ["Site-1", "Site-2", "Site-3", "Site-4", "Site-5", "Site-6"]}

# --- kalender heatmap: jumlah tiket per hari 2026 ---
CAL_DAYS = 365  # mulai Senin 2026-01-05 dianggap awal grid

# --- sparkline: tren 5 metrik dalam sel tabel ---
SPARK = {
    "Bitrate Site A": BITRATE_A, "Bitrate Site B": BITRATE_B,
    "Beban kW": BEBAN_KW, "Ketersediaan %": np.round(RNG.normal(97, 1, 12), 1),
    "Tiket buka": np.round(RNG.uniform(2, 20, 12), 0),
}

# --- tabel berannotasi: status per site ---
TABLE_ROWS = [
    ["Site-1", 98.2, 412, "Selesai"],
    ["Site-2", 96.7, 233, "Selesai"],
    ["Site-3", 91.4, 187, "Retest"],
    ["Site-4", 99.1, 305, "Selesai"],
    ["Site-5", 88.9, 96,  "Perbaikan"],
]
TABLE_HEAD = ["Site", "Uptime %", "Titik aktif", "Status"]

# --- error bar: rerata latensi per operator (ms) ---
ERR_LABEL = ["Opsel A", "Opsel B", "Opsel C", "Opsel D"]
ERR_MEAN = [38.2, 44.7, 31.5, 52.0]
ERR_SD = [4.1, 7.8, 3.2, 9.5]

# --- pasangan anti-pola (salah vs benar) ---
AP_BAR_KAT = ["Gen-1", "Gen-2", "Gen-3", "Gen-4"]
AP_BAR_VAL = [41.2, 43.8, 45.1, 46.9]           # GWh-ish -> pakai MWh bulanan
AP_PIE_PARTS = [("Hardware", 30), ("Jasa", 22), ("Lisensi", 15), ("Logistik", 11),
                ("Asuransi", 8), ("Uji", 6), ("Dokumentasi", 5), ("Lainnya", 3)]
AP_DUAL_X = np.arange(1, 13)
AP_DUAL_A = np.round(RNG.uniform(10, 14, 12), 2)     # harga indeks
AP_DUAL_B = np.round(RNG.uniform(40, 90, 12), 1)     # unit terjual
AP_LEG_SERI = {"Site A": BITRATE_A, "Site B": BITRATE_B, "Site C": BITRATE_C, "Site D": BITRATE_D}
AP_HEAT_M = SKOR_M  # sama data, beda colormap
