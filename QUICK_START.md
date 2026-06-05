# 🚀 Quick Start Guide - Inference Logging

## 📝 Apa yang Sudah Diimplementasikan?

Sistem logging otomatis untuk mencatat **Inference Time** dan **FPS** ketika deteksi menggunakan YOLO atau RF-DETR model.

---

## 🎯 Fitur Utama

✅ **Otomatis mencatat waktu inference** - Tidak perlu konfigurasi tambahan
✅ **Hitung FPS** - Frame per second dari waktu inference
✅ **Simpan ke file JSON** - Untuk analisis berkelanjutan
✅ **API Endpoint Statistik** - Bandingkan performa kedua model
✅ **Export ke CSV** - Untuk analisis lebih lanjut di Excel/Spreadsheet

---

## 📂 File yang Dibuat/Dimodifikasi

### Baru Dibuat ✅
- `plasticBottleDetection/services/inference_logger.py` - Core logging utility
- `plasticBottleDetection/services/log_viewer.py` - Utility untuk melihat logs
- `plasticBottleDetection/INFERENCE_LOGGING.md` - Dokumentasi lengkap
- `test_inference_logging.py` - Test script

### Dimodifikasi ✅
- `plasticBottleDetection/services/yolo_model.py` - Tambah timing
- `plasticBottleDetection/services/rfdetr_model.py` - Tambah timing
- `plasticBottleDetection/views.py` - Tambah metrics di response
- `plasticBottleDetection/rfdetr_views.py` - Tambah metrics di response
- `plasticBottleDetection/urls.py` - Fix URL routing

---

## 🚀 Cara Menggunakan

### 1️⃣ Setup (Jika belum)

```bash
# Masuk ke project folder
cd e:\fahraz\saling-rvm-web\local_rvm\serialproject

# Run Django server
python manage.py runserver
```

### 2️⃣ Test Deteksi YOLO

```bash
curl -X POST http://localhost:8000/api/detect/ \
  -F "image=@path/to/image.jpg"
```

**Response:**
```json
{
  "predictions": [...],
  "model_used": "YOLO v2.6",
  "metrics": {
    "inference_time_ms": 125.45,
    "inference_time_sec": 0.1254,
    "fps": 7.97,
    "detection_count": 3
  }
}
```

### 3️⃣ Test Deteksi RF-DETR

```bash
curl -X POST http://localhost:8000/api/detect-rfdetr/ \
  -F "image=@path/to/image.jpg"
```

**Response:**
```json
{
  "predictions": [...],
  "model_used": "RF-DETR Nano",
  "metrics": {
    "inference_time_ms": 89.32,
    "inference_time_sec": 0.0893,
    "fps": 11.20,
    "detection_count": 2
  }
}
```

### 4️⃣ Lihat Statistik Perbandingan

```bash
curl "http://localhost:8000/api/statistics/"
```

**Response:** (Perbandingan lengkap avg, min, max untuk kedua model)

---

## 📊 Contoh Output

### Console Output (Real-time)

```
============================================================
⏱️  INFERENCE METRICS - YOLO
============================================================
  📸 Image: bottle_001.jpg
  ⏱️  Inference Time: 125.45ms (0.1254s)
  🎬 FPS: 7.97
  🎯 Detections: 3
  📁 Image Size: 156.23 KB
============================================================
```

### Log File (`inference_logs/yolo_logs.json`)

```json
[
  {
    "timestamp": "2024-01-15T10:30:45.123456",
    "model": "YOLO",
    "image_name": "bottle_001.jpg",
    "inference_time_ms": 125.45,
    "inference_time_sec": 0.1254,
    "fps": 7.97,
    "detection_count": 3,
    "image_size_kb": 156.23
  }
]
```

---

## 🔍 Analisis Performa

### Contoh Hasil Perbandingan

```
YOLO:
- Total Inferences: 50
- Avg Inference Time: 128.50 ms
- Avg FPS: 7.78

RF-DETR:
- Total Inferences: 50
- Avg Inference Time: 92.30 ms
- Avg FPS: 10.84

➡️ RF-DETR lebih cepat 28% dibanding YOLO
```

---

## 💾 Log Files Location

```
E:\fahraz\saling-rvm-web\local_rvm\serialproject\
└── plasticBottleDetection\
    └── inference_logs\
        ├── yolo_logs.json          # YOLO logs
        ├── rf-detr_logs.json       # RF-DETR logs
        └── inference_logs_export.csv  # CSV export (generated)
```

---

## 🛠️ Advanced Usage

### Dari Django Shell

```bash
python manage.py shell
```

```python
# Lihat perbandingan
from plasticBottleDetection.services.inference_logger import InferenceLogger
InferenceLogger.print_comparison()

# Export ke CSV
from plasticBottleDetection.services.log_viewer import export_logs_to_csv
export_logs_to_csv()

# Dapatkan statistik JSON
stats = InferenceLogger.get_statistics()
print(stats)
```

### Run Test Script

```bash
python test_inference_logging.py
```

---

## 📈 Metrik yang Dicatat

| Metrik | Contoh Nilai | Keterangan |
|--------|-------------|-----------|
| `inference_time_ms` | 125.45 | Waktu inference dalam milliseconds |
| `inference_time_sec` | 0.1254 | Waktu inference dalam seconds |
| `fps` | 7.97 | Frame per second (1/inference_time) |
| `detection_count` | 3 | Jumlah botol terdeteksi |
| `image_size_kb` | 156.23 | Ukuran file gambar |
| `timestamp` | 2024-01-15T10:30:45 | Kapan inference dilakukan |

---

## ✨ Keuntungan

✅ **Tidak perlu setup manual** - Otomatis berjalan saat inference
✅ **Tidak ada breaking changes** - Kompatibel dengan kode existing
✅ **Mudah dibandingkan** - Endpoint statistik untuk perbandingan
✅ **Persisten** - Logs disimpan untuk analisis jangka panjang
✅ **Export-ready** - Bisa di-export ke CSV untuk analisis lebih lanjut

---

## 🎓 Troubleshooting

### ❌ Logs tidak tersimpan
→ Periksa folder `inference_logs/` punya permission tulis

### ❌ Statistik kosong
→ Lakukan minimal 1-2 inference dulu

### ❌ Import error
→ Pastikan semua file sudah di-place dengan benar

### ❌ API error
→ Lihat dokumentasi lengkap di `INFERENCE_LOGGING.md`

---

## 📖 Dokumentasi Lengkap

Untuk dokumentasi lebih detail, lihat:
- `plasticBottleDetection/INFERENCE_LOGGING.md` - Complete reference
- `INFERENCE_LOGGING_IMPLEMENTATION.md` - Implementation details

---

## 🎯 Next Steps

1. ✅ **Run detection** dengan YOLO atau RF-DETR
2. ✅ **Lihat metrics** di response
3. ✅ **Bandingkan performa** via `/api/statistics/`
4. ✅ **Export data** untuk analisis lebih lanjut
5. ✅ **Buat keputusan** model mana yang lebih cepat

---

**Status**: ✅ Ready to Use
**Version**: 1.0
**Created**: 2024

Silakan coba dan hubungi jika ada pertanyaan! 🚀
