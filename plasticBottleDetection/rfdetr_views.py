from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .services.rfdetr_model import detect_image, load_model
from .services.inference_logger import InferenceLogger
from datetime import datetime

# Load model saat Django startup (opsional tapi direkomendasikan)
load_model()   # panggil sekali di awal

@api_view(['POST'])
def detect_plastic(request):
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] API Request - Detect Plastic Bottle (RF-DETR)")
    print(f"{'='*60}")
    
    if 'image' not in request.FILES:
        print("❌ Error: No image provided")
        print(f"{'='*60}\n")
        return Response({"error": "No image provided"}, status=400)

    image = request.FILES['image']
    print(f"📁 Image Name: {image.name}")
    image_size_kb = image.size / 1024
    print(f"📊 Image Size: {image_size_kb:.2f} KB")
    
    file_path = default_storage.save(f"temp/{image.name}", image)
    full_path = default_storage.path(file_path)

    try:
        # Deteksi dengan metrics
        predictions, metrics = detect_image(
            full_path,
            image_name=image.name,
            image_size_kb=image_size_kb
        )

        response_data = {
            "predictions": predictions,
            "model_used": "RF-DETR Nano",
            "metrics": {
                "inference_time_ms": metrics['inference_time_ms'],
                "inference_time_sec": metrics['inference_time_sec'],
                "fps": metrics['fps'],
                "detection_count": metrics['detection_count']
            }
        }
        
        print(f"\n📤 Response Data:")
        print(f"   - Total Detections: {len(predictions)}")
        if predictions:
            for idx, pred in enumerate(predictions, 1):
                print(f"   [{idx}] Class: {pred['class']}, Confidence: {pred['confidence']:.2%}, Size: {pred['size']}")
        else:
            print("   ⚠️  No plastic bottle detected")
            
    finally:
        default_storage.delete(file_path)   # bersihkan file

    print(f"{'='*60}\n")
    return Response(response_data, status=200)


@api_view(['GET'])
def get_inference_statistics(request):
    """
    Endpoint untuk mendapatkan statistik inference dari semua model
    
    Query params:
        - model: YOLO, RF-DETR, atau kosong untuk semua
    """
    model_name = request.query_params.get('model', None)
    
    stats = InferenceLogger.get_statistics(model_name)
    
    if not stats:
        return Response({"message": "No inference logs available yet"}, status=404)
    
    # Print comparison
    InferenceLogger.print_comparison()
    
    return Response({
        "statistics": stats,
        "message": "Fetch statistics successfully"
    }, status=200)