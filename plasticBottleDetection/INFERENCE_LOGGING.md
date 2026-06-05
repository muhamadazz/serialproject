# 📊 Inference Timing & FPS Logging

Sistem logging untuk membandingkan performa model YOLO dan RF-DETR dalam deteksi botol plastik.

## 🎯 Fitur

- ⏱️ **Inference Time Measurement** - Mengukur waktu inference dalam ms dan detik
- 🎬 **FPS Calculation** - Menghitung frame per second dari waktu inference
- 💾 **Automatic Logging** - Semua hasil inference otomatis tersimpan ke file JSON
- 📊 **Statistics & Comparison** - API endpoint untuk mendapatkan statistik perbandingan model
- 📈 **CSV Export** - Export logs ke CSV untuk analisis lebih lanjut

## 📁 File Structure

```
plasticBottleDetection/
├── services/
│   ├── inference_logger.py      # 🔧 Utility logging (MAIN)
│   ├── log_viewer.py            # 📊 Utility untuk melihat logs
│   ├── yolo_model.py            # YOLO model (sudah terintegrasi)
│   └── rfdetr_model.py          # RF-DETR model (sudah terintegrasi)
├── inference_logs/              # 📁 Folder untuk menyimpan logs (auto-created)
│   ├── yolo_logs.json          # YOLO inference logs
│   └── rf-detr_logs.json       # RF-DETR inference logs
└── views.py & rfdetr_views.py  # (sudah terintegrasi)
```

## 🚀 Cara Menggunakan

### 1️⃣ Deteksi Gambar (Otomatis Logging)

#### YOLO Model
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

#### RF-DETR Model
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
    "detection_count": 3
  }
}
```

### 2️⃣ Lihat Statistik Perbandingan Model

```bash
# Semua model
curl http://localhost:8000/api/statistics/

# Model tertentu
curl "http://localhost:8000/api/statistics/?model=YOLO"
curl "http://localhost:8000/api/statistics/?model=RF-DETR"
```

**Response:**
```json
{
  "statistics": {
    "YOLO": {
      "total_inferences": 45,
      "inference_time": {
        "avg_ms": 128.50,
        "min_ms": 115.32,
        "max_ms": 156.78,
        "total_ms": 5782.50
      },
      "fps": {
        "avg": 7.78,
        "min": 6.38,
        "max": 8.67
      },
      "detections": {
        "total": 120,
        "avg_per_image": 2.67
      }
    },
    "RF-DETR": {
      "total_inferences": 45,
      "inference_time": {
        "avg_ms": 92.30,
        "min_ms": 85.10,
        "max_ms": 110.45,
        "total_ms": 4153.50
      },
      "fps": {
        "avg": 10.84,
        "min": 9.05,
        "max": 11.75
      },
      "detections": {
        "total": 118,
        "avg_per_image": 2.62
      }
    }
  }
}
```

### 3️⃣ Lihat Logs Dari Django Shell

```bash
python manage.py shell
```

```python
from plasticBottleDetection.services.inference_logger import InferenceLogger

# Print perbandingan semua model
InferenceLogger.print_comparison()

# Dapatkan statistik untuk model tertentu
stats = InferenceLogger.get_statistics("YOLO")
print(stats)

# Dapatkan statistik semua model
all_stats = InferenceLogger.get_statistics()
print(all_stats)
```

### 4️⃣ Export ke CSV

```bash
python manage.py shell
```

```python
from plasticBottleDetection.services.log_viewer import export_logs_to_csv

export_logs_to_csv()
# Output: ✅ Logs exported to plasticBottleDetection/inference_logs/inference_logs_export.csv
```

## 📊 Format Log File

Setiap model memiliki file log JSON terpisah:

**YOLO Logs** (`inference_logs/yolo_logs.json`):
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
  },
  ...
]
```

**RF-DETR Logs** (`inference_logs/rf-detr_logs.json`):
```json
[
  {
    "timestamp": "2024-01-15T10:35:12.789012",
    "model": "RF-DETR",
    "image_name": "bottle_002.jpg",
    "inference_time_ms": 89.32,
    "inference_time_sec": 0.0893,
    "fps": 11.20,
    "detection_count": 2,
    "image_size_kb": 145.67
  },
  ...
]
```

## 🔍 Console Output

Setiap kali inference dilakukan, akan menampilkan output seperti ini:

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

## 📈 Analisis & Interpretasi

### Metrik Kunci

| Metrik | Interpretasi | Lebih Baik |
|--------|--------------|-----------|
| **Inference Time (ms)** | Waktu proses deteksi | Lebih Kecil ✅ |
| **FPS** | Frame per second | Lebih Besar ✅ |
| **Detections** | Jumlah botol terdeteksi | Akurasi tergantung |

### Contoh Analisis

**Scenario: YOLO vs RF-DETR**

```
YOLO:
- Avg Inference Time: 128.50 ms
- Avg FPS: 7.78
- Cocok untuk: Aplikasi yang tidak memerlukan real-time tinggi

RF-DETR:
- Avg Inference Time: 92.30 ms
- Avg FPS: 10.84
- Cocok untuk: Aplikasi yang memerlukan kecepatan lebih tinggi
```

## 🔧 Integrasi Manual (Jika Diperlukan)

Jika ingin menambah logging ke kode lain:

```python
from plasticBottleDetection.services.inference_logger import InferenceLogger

# Buat logger instance
logger = InferenceLogger("YourModel")

# Log hasil inference
metrics = logger.log_inference(
    inference_time=0.125,  # dalam detik
    image_name="image.jpg",
    detection_count=3,
    image_size_kb=156.23
)

print(metrics)
# Output: {
#   'timestamp': '2024-01-15T10:30:45.123456',
#   'model': 'YourModel',
#   'image_name': 'image.jpg',
#   'inference_time_ms': 125.0,
#   'inference_time_sec': 0.125,
#   'fps': 8.0,
#   'detection_count': 3,
#   'image_size_kb': 156.23
# }
```

## 📂 Log Files Location

```
project_root/
└── plasticBottleDetection/
    └── inference_logs/
        ├── yolo_logs.json          # All YOLO inference logs
        ├── rf-detr_logs.json       # All RF-DETR inference logs
        └── inference_logs_export.csv  # CSV export (generated)
```

## 🐛 Troubleshooting

### Logs tidak tersimpan
- Pastikan folder `inference_logs/` dapat ditulis
- Periksa permission folder

### Statistik tidak muncul
- Lakukan minimal 1-2 inference terlebih dahulu
- Periksa file JSON di folder `inference_logs/`

### CSV Export error
- Pastikan sudah ada log data
- Periksa permission folder

## 📝 Catatan

- Logs disimpan secara **otomatis** setiap kali deteksi dilakukan
- Tidak perlu setup tambahan
- Kompatibel dengan YOLO v8 dan RF-DETR Nano
- Data logs dapat dihapus manual dari folder `inference_logs/`

## 🎯 Use Cases

1. **Performance Testing** - Bandingkan kecepatan model sebelum production
2. **Monitoring** - Track performa model dari waktu ke waktu
3. **Optimization** - Identifikasi bottleneck dan optimization opportunities
4. **Reporting** - Buat laporan performa untuk stakeholder
5. **Benchmarking** - Compare dengan model lainnya

---

**Created**: 2024-01-15  
**Version**: 1.0  
**Status**: ✅ Production Ready
