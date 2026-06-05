from ultralytics import YOLO
import uuid
import time
from .inference_logger import InferenceLogger

CLASS_NAMES = {
    1: "BotolPlastik"
}

model = YOLO("plasticBottleDetection/best_plasticbottle_yolov26.pt")
logger = InferenceLogger("YOLO")


def get_size(area):
    if area < 60000:
        return "330ml"
    elif area < 100000:
        return "600ml"
    else:
        return "1500ml"


def detect_image(image_path, image_name=None, image_size_kb=None):
    """
    Deteksi botol plastik menggunakan YOLO dengan timing measurement
    
    Args:
        image_path: Path ke file gambar
        image_name: Nama file gambar (untuk logging)
        image_size_kb: Ukuran gambar dalam KB (untuk logging)
    
    Returns:
        tuple: (predictions list, inference_metrics dict)
    """
    # Mulai timing
    start_time = time.time()
    
    # Inference
    results = model(image_path, conf=0.8)
    
    # Hitung waktu inference
    inference_time = time.time() - start_time

    predictions = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            width = x2 - x1
            height = y2 - y1
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2

            area = width * height
            size = get_size(area)

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            predictions.append({
                "width": width,
                "height": height,
                "x": x_center,
                "y": y_center,
                "confidence": confidence,
                "class_id": class_id,
                "class": CLASS_NAMES.get(class_id, "Unknown"),
                "size": size,
                "area": area,
                "detection_id": str(uuid.uuid4()),
                "parent_id": "image"
            })

    # Log metrics
    metrics = logger.log_inference(
        inference_time=inference_time,
        image_name=image_name or "unknown",
        detection_count=len(predictions),
        image_size_kb=image_size_kb
    )

    return predictions, metrics