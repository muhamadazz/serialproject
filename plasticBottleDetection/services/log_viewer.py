"""
Utility script untuk melihat dan menganalisis inference logs

Usage:
    python manage.py shell
    >>> from plasticBottleDetection.services.inference_logger import InferenceLogger
    >>> InferenceLogger.print_comparison()
    
    # Atau langsung dari shell:
    >>> from plasticBottleDetection.services.inference_logger import InferenceLogger
    >>> stats = InferenceLogger.get_statistics("YOLO")
    >>> print(stats)
"""

from plasticBottleDetection.services.inference_logger import InferenceLogger
import json
from pathlib import Path

def print_comparison():
    """Print perbandingan performa model"""
    InferenceLogger.print_comparison()

def get_stats(model_name=None):
    """Dapatkan statistik model"""
    return InferenceLogger.get_statistics(model_name)

def export_logs_to_csv():
    """Export logs ke file CSV untuk analisis lebih lanjut"""
    import csv
    from datetime import datetime
    
    LOG_DIR = Path(__file__).parent / "inference_logs"
    
    if not LOG_DIR.exists():
        print("❌ Tidak ada log directory")
        return
    
    csv_file = LOG_DIR / "inference_logs_export.csv"
    
    all_logs = []
    for log_file in LOG_DIR.glob("*_logs.json"):
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
                all_logs.extend(logs)
        except:
            pass
    
    if not all_logs:
        print("❌ Tidak ada log data")
        return
    
    # Sort by timestamp
    all_logs.sort(key=lambda x: x['timestamp'])
    
    # Write to CSV
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'Timestamp',
            'Model',
            'Image Name',
            'Inference Time (ms)',
            'FPS',
            'Detections',
            'Image Size (KB)'
        ])
        
        # Data
        for log in all_logs:
            writer.writerow([
                log['timestamp'],
                log['model'],
                log['image_name'],
                log['inference_time_ms'],
                log['fps'],
                log['detection_count'],
                log['image_size_kb'] or 'N/A'
            ])
    
    print(f"✅ Logs exported to {csv_file}")

if __name__ == "__main__":
    print("🔍 Inference Logger Utility")
    print("\nPerbandingan Performa Model:")
    print_comparison()
    
    print("\n📊 Export ke CSV:")
    export_logs_to_csv()
