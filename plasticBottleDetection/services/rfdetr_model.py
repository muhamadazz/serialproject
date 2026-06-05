from rfdetr import RFDETRNano
import uuid
from PIL import Image
import torch
import time
from .inference_logger import InferenceLogger

# =============================================
# CLASS NAMES (sesuaikan dengan dataset kamu)
# =============================================
CLASS_NAMES = {
    1: "BotolPlastik"
}

# Load model sekali saja (global) - mirip YOLO
model = None
logger = InferenceLogger("RF-DETR")

def load_model():
    global model
    if model is None:
        try:
            model = RFDETRNano(
                pretrain_weights="plasticBottleDetection/checkpoint_best_total.pth",  
                device="cuda" if torch.cuda.is_available() else "cpu"
            )
            # Optional: optimasi untuk inference (lebih cepat di CPU)
            model.optimize_for_inference()
            print("✅ RF-DETR Nano model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading RF-DETR model: {e}")
            raise

def get_size(area):
    if area < 60000:
        return "330ml"
    elif area < 100000:
        return "600ml"
    else:
        return "1500ml"


def detect_image(image_path, image_name=None, image_size_kb=None):
    """
    Deteksi botol plastik menggunakan RF-DETR dengan timing measurement
    
    Args:
        image_path: Path ke file gambar
        image_name: Nama file gambar (untuk logging)
        image_size_kb: Ukuran gambar dalam KB (untuk logging)
    
    Returns:
        tuple: (predictions list, inference_metrics dict)
    """
    global model
    if model is None:
        load_model()

    # Buka gambar dengan PIL (RF-DETR lebih suka PIL)
    image = Image.open(image_path).convert("RGB")

    # Mulai timing
    start_time = time.time()
    
    # Inference
    results = model.predict(image, threshold=0.5)   # sesuaikan threshold
    
    # Hitung waktu inference
    inference_time = time.time() - start_time

    predictions = []

    for i in range(len(results.xyxy)):
        x1, y1, x2, y2 = results.xyxy[i].tolist()
        confidence = float(results.confidence[i])
        class_id = int(results.class_id[i])

        width = x2 - x1
        height = y2 - y1
        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2
        area = width * height
        size = get_size(area)

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