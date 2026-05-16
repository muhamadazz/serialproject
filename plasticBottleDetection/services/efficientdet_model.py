import torch
import uuid
from PIL import Image
from torchvision import transforms
from effdet import create_model

CLASS_NAMES = {
    0: "BotolPlastik"
}

# =========================
# Load Model
# =========================
model = create_model(
    'tf_efficientdet_d2',
    bench_task='predict',
    num_classes=1,
    pretrained=False,
    image_size=(640, 640)
)

checkpoint = torch.load(
    "plasticBottleDetection/best_efficientdet_d2.pt",
    map_location=torch.device("cpu")
)

# Jika checkpoint hasil training berbentuk dictionary
if isinstance(checkpoint, dict):

    # paling umum
    if "state_dict" in checkpoint:
        checkpoint = checkpoint["state_dict"]

    # kadang key model
    elif "model" in checkpoint:
        checkpoint = checkpoint["model"]

# hapus prefix module. jika ada
new_state_dict = {}

for k, v in checkpoint.items():

    if k.startswith("module."):
        k = k[7:]

    new_state_dict[k] = v

model.load_state_dict(new_state_dict, strict=False)

model.eval()


# =========================
# Transform Image
# =========================
transform = transforms.Compose([
    transforms.Resize((640, 640)),
    transforms.ToTensor(),
])


# =========================
# Size Estimation
# =========================
def get_size(area):

    if area < 60000:
        return "330ml"

    elif area < 100000:
        return "600ml"

    else:
        return "1500ml"


# =========================
# Detection Function
# =========================
def detect_image_efficientdet(image_path):

    image = Image.open(image_path).convert("RGB")

    original_width, original_height = image.size

    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():

        results = model(img_tensor)

    predictions = []

    detections = results[0]

    for det in detections:

        score = float(det[4])

        # confidence threshold
        if score < 0.8:
            continue

        x1, y1, x2, y2 = det[:4].tolist()

        # scaling ke ukuran asli gambar
        x_scale = original_width / 512
        y_scale = original_height / 512

        x1 *= x_scale
        x2 *= x_scale
        y1 *= y_scale
        y2 *= y_scale

        width = x2 - x1
        height = y2 - y1

        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2

        area = width * height

        size = get_size(area)

        class_id = 0

        predictions.append({
            "width": width,
            "height": height,
            "x": x_center,
            "y": y_center,
            "confidence": score,
            "class_id": class_id,
            "class": CLASS_NAMES.get(class_id, "Unknown"),
            "size": size,
            "area": area,
            "detection_id": str(uuid.uuid4()),
            "parent_id": "image"
        })

    return predictions