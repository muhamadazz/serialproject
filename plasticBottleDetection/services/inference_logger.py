import json
import os
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "inference_logs"

class InferenceLogger:
    """Utility untuk logging inference time dan FPS"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._ensure_log_dir()
    
    def _ensure_log_dir(self):
        """Pastikan direktori log ada"""
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    def log_inference(self, inference_time: float, image_name: str, 
                     detection_count: int, image_size_kb: float = None):
        """
        Log hasil inference ke file JSON
        
        Args:
            inference_time: Waktu inference dalam detik
            image_name: Nama file gambar
            detection_count: Jumlah deteksi
            image_size_kb: Ukuran gambar dalam KB (optional)
        """
        fps = 1.0 / inference_time if inference_time > 0 else 0
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": self.model_name,
            "image_name": image_name,
            "inference_time_ms": round(inference_time * 1000, 2),
            "inference_time_sec": round(inference_time, 4),
            "fps": round(fps, 2),
            "detection_count": detection_count,
            "image_size_kb": round(image_size_kb, 2) if image_size_kb else None
        }
        
        # Print ke console
        self._print_log(log_entry)
        
        # Simpan ke file JSON
        self._save_log(log_entry)
        
        return log_entry
    
    def _print_log(self, log_entry: dict):
        """Print log ke console dengan format yang rapi"""
        print(f"\n{'='*60}")
        print(f"⏱️  INFERENCE METRICS - {self.model_name}")
        print(f"{'='*60}")
        print(f"  📸 Image: {log_entry['image_name']}")
        print(f"  ⏱️  Inference Time: {log_entry['inference_time_ms']}ms ({log_entry['inference_time_sec']}s)")
        print(f"  🎬 FPS: {log_entry['fps']}")
        print(f"  🎯 Detections: {log_entry['detection_count']}")
        if log_entry['image_size_kb']:
            print(f"  📁 Image Size: {log_entry['image_size_kb']} KB")
        print(f"{'='*60}\n")
    
    def _save_log(self, log_entry: dict):
        """Simpan log entry ke file JSON"""
        log_file = LOG_DIR / f"{self.model_name.lower().replace(' ', '_')}_logs.json"
        
        # Load existing logs
        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        # Append new log
        logs.append(log_entry)
        
        # Save back
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    @staticmethod
    def get_statistics(model_name: str = None):
        """
        Dapatkan statistik dari logs
        
        Args:
            model_name: Nama model (misal 'YOLO' atau 'RF-DETR'). 
                       Jika None, ambil semua model
        
        Returns:
            dict dengan statistik (avg, min, max, total, dll)
        """
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        stats = {}
        
        # Jika spesifik model
        if model_name:
            log_file = LOG_DIR / f"{model_name.lower().replace(' ', '_')}_logs.json"
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
                stats[model_name] = InferenceLogger._calculate_stats(logs)
        else:
            # Ambil semua file log
            for log_file in LOG_DIR.glob("*_logs.json"):
                model_name_from_file = log_file.stem.replace("_logs", "").upper()
                try:
                    with open(log_file, 'r') as f:
                        logs = json.load(f)
                    stats[model_name_from_file] = InferenceLogger._calculate_stats(logs)
                except:
                    pass
        
        return stats
    
    @staticmethod
    def _calculate_stats(logs: list):
        """Hitung statistik dari list logs"""
        if not logs:
            return None
        
        inference_times = [log['inference_time_ms'] for log in logs]
        fps_values = [log['fps'] for log in logs]
        detections = [log['detection_count'] for log in logs]
        
        return {
            "total_inferences": len(logs),
            "inference_time": {
                "avg_ms": round(sum(inference_times) / len(inference_times), 2),
                "min_ms": round(min(inference_times), 2),
                "max_ms": round(max(inference_times), 2),
                "total_ms": round(sum(inference_times), 2)
            },
            "fps": {
                "avg": round(sum(fps_values) / len(fps_values), 2),
                "min": round(min(fps_values), 2),
                "max": round(max(fps_values), 2)
            },
            "detections": {
                "total": sum(detections),
                "avg_per_image": round(sum(detections) / len(detections), 2)
            }
        }
    
    @staticmethod
    def print_comparison():
        """Print perbandingan semua model"""
        stats = InferenceLogger.get_statistics()
        
        if not stats:
            print("❌ Belum ada log data")
            return
        
        print(f"\n{'='*80}")
        print(f"📊 INFERENCE PERFORMANCE COMPARISON")
        print(f"{'='*80}\n")
        
        for model_name, model_stats in stats.items():
            if model_stats:
                print(f"🤖 {model_name}:")
                print(f"   Total Inferences: {model_stats['total_inferences']}")
                print(f"   Inference Time (ms):")
                print(f"      - Average: {model_stats['inference_time']['avg_ms']}ms")
                print(f"      - Min: {model_stats['inference_time']['min_ms']}ms")
                print(f"      - Max: {model_stats['inference_time']['max_ms']}ms")
                print(f"   FPS:")
                print(f"      - Average: {model_stats['fps']['avg']}")
                print(f"      - Min: {model_stats['fps']['min']}")
                print(f"      - Max: {model_stats['fps']['max']}")
                print(f"   Detections:")
                print(f"      - Total: {model_stats['detections']['total']}")
                print(f"      - Avg per image: {model_stats['detections']['avg_per_image']}")
                print()
        
        print(f"{'='*80}\n")
