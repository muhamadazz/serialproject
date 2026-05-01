from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .services.yolo_model import detect_image
from datetime import datetime

@api_view(['POST'])
def detect_plastic(request):
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] API Request - Detect Plastic Bottle")
    print(f"{'='*60}")
    
    if 'image' not in request.FILES:
        print("❌ Error: No image provided")
        print(f"{'='*60}\n")
        return Response({"error": "No image provided"}, status=400)

    image = request.FILES['image']
    print(f"📁 Image Name: {image.name}")
    print(f"📊 Image Size: {image.size / 1024:.2f} KB")
    
    file_path = default_storage.save(f"temp/{image.name}", image)
    print(f"💾 File Path: {file_path}")

    predictions = detect_image(default_storage.path(file_path))

    default_storage.delete(file_path)

    response_data = {
        "predictions": predictions
    }
    
    print(f"\n📤 Response Data:")
    print(f"   - Total Detections: {len(predictions)}")
    if predictions:
        for idx, pred in enumerate(predictions, 1):
            print(f"   [{idx}] Class: {pred['class']}, Confidence: {pred['confidence']:.2%}, Size: {pred['size']}")
    else:
        print("   ⚠️  No plastic bottle detected")
    
    print(f"{'='*60}\n")
    
    return Response(response_data, status=200)