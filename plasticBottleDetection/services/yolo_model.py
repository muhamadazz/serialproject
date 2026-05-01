from ultralytics import YOLO
import uuid

CLASS_NAMES = {
    0: "BotolPlastik"
}

model = YOLO("plasticBottleDetection/best_plasticbottle_yolov26.pt")


def get_size(area):
    if area < 60000:
        return "330ml"
    elif area < 100000:
        return "600ml"
    else:
        return "1500ml"


def detect_image(image_path):
    results = model(image_path)

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
                "size": size,                      # ✅ tambahan
                "area": area,                      # (optional tapi bagus untuk debug)
                "detection_id": str(uuid.uuid4()),
                "parent_id": "image"
            })

    return predictions