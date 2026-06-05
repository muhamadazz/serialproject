#!/usr/bin/env python
"""
Script untuk testing inference logging

Usage:
    python test_inference_logging.py
"""

import os
import sys
import json
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serialproject.settings')

import django
django.setup()

from plasticBottleDetection.services.inference_logger import InferenceLogger
from plasticBottleDetection.services.log_viewer import export_logs_to_csv

def test_logging():
    """Test logging functionality"""
    
    print("\n" + "="*70)
    print("🧪 INFERENCE LOGGING TEST")
    print("="*70 + "\n")
    
    # Test 1: Simulasi YOLO inference
    print("1️⃣  Testing YOLO Logger...")
    logger_yolo = InferenceLogger("YOLO")
    metrics1 = logger_yolo.log_inference(
        inference_time=0.1254,
        image_name="test_bottle_001.jpg",
        detection_count=3,
        image_size_kb=156.23
    )
    print(f"✅ YOLO logging test passed")
    
    # Test 2: Simulasi RF-DETR inference
    print("\n2️⃣  Testing RF-DETR Logger...")
    logger_rfdetr = InferenceLogger("RF-DETR")
    metrics2 = logger_rfdetr.log_inference(
        inference_time=0.0893,
        image_name="test_bottle_002.jpg",
        detection_count=2,
        image_size_kb=145.67
    )
    print(f"✅ RF-DETR logging test passed")
    
    # Test 3: Lihat log files
    print("\n3️⃣  Checking log files...")
    log_dir = Path(__file__).parent / "plasticBottleDetection" / "inference_logs"
    if log_dir.exists():
        log_files = list(log_dir.glob("*_logs.json"))
        print(f"✅ Found {len(log_files)} log file(s):")
        for log_file in log_files:
            with open(log_file, 'r') as f:
                logs = json.load(f)
            print(f"   - {log_file.name}: {len(logs)} entries")
    else:
        print("⚠️  Log directory not found (will be created on first inference)")
    
    # Test 4: Get statistics
    print("\n4️⃣  Testing statistics...")
    stats = InferenceLogger.get_statistics()
    if stats:
        print(f"✅ Statistics retrieved for {len(stats)} model(s)")
        for model_name, model_stats in stats.items():
            if model_stats:
                print(f"   - {model_name}: {model_stats['total_inferences']} inferences")
    else:
        print("⚠️  No statistics available yet")
    
    # Test 5: Print comparison
    print("\n5️⃣  Printing comparison...")
    InferenceLogger.print_comparison()
    
    # Test 6: Export to CSV
    print("\n6️⃣  Testing CSV export...")
    try:
        export_logs_to_csv()
        print("✅ CSV export test passed")
    except Exception as e:
        print(f"⚠️  CSV export: {e}")
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED")
    print("="*70 + "\n")
    
    print("📚 NEXT STEPS:")
    print("1. Run inference via API endpoint (see INFERENCE_LOGGING.md)")
    print("2. Check statistics at /api/statistics/")
    print("3. View logs in plasticBottleDetection/inference_logs/")
    print("\n")

if __name__ == "__main__":
    test_logging()
