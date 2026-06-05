from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .services.yolo_model import detect_image
from .services.inference_logger import InferenceLogger
from datetime import datetime
# from .services.efficientdet_model import detect_image

# import os
# from .efficientdet.infer import predict_image

@api_view(['POST'])
def detect_plastic(request):
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] API Request - Detect Plastic Bottle (YOLO)")
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
    print(f"💾 File Path: {file_path}")

    # Deteksi dengan metrics
    predictions, metrics = detect_image(
        default_storage.path(file_path),
        image_name=image.name,
        image_size_kb=image_size_kb
    )

    default_storage.delete(file_path)

    response_data = {
        "predictions": predictions,
        "model_used": "YOLO v2.6",
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


# @api_view(['POST'])
# def detect_plastic_efficientdet(request):

#     print(f"\n{'='*60}")
#     print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] API Request - EfficientDet")
#     print(f"{'='*60}")

#     if 'image' not in request.FILES:
#         print("❌ Error: No image provided")
#         print(f"{'='*60}\n")

#         return Response(
#             {"error": "No image provided"},
#             status=400
#         )

#     image = request.FILES['image']

#     print(f"📁 Image Name: {image.name}")
#     print(f"📊 Image Size: {image.size / 1024:.2f} KB")

#     file_path = default_storage.save(
#         f"temp/{image.name}",
#         image
#     )

#     print(f"💾 File Path: {file_path}")

#     predictions = detect_image_efficientdet(
#         default_storage.path(file_path)
#     )

#     default_storage.delete(file_path)

#     response_data = {
#         "predictions": predictions
#     }

#     print(f"\n📤 Response Data:")
#     print(f"   - Total Detections: {len(predictions)}")

#     if predictions:
#         for idx, pred in enumerate(predictions, 1):
#             print(
#                 f"   [{idx}] "
#                 f"Class: {pred['class']}, "
#                 f"Confidence: {pred['confidence']:.2%}, "
#                 f"Size: {pred['size']}"
#             )
#     else:
#         print("   ⚠️ No plastic bottle detected")

#     print(f"{'='*60}\n")

#     return Response(response_data, status=200)


# ==========================================
# API
# ==========================================
# @api_view(['POST'])
# def detect_bottle(request):

#     image = request.FILES.get('image')

#     if not image:

#         return Response({
#             'status': False,
#             'message': 'Image is required'
#         }, status=400)

#     # ==========================================
#     # SAVE TEMP IMAGE
#     # ==========================================
#     temp_path = default_storage.save(
#         f'tmp/{image.name}',
#         image
#     )

#     full_path = default_storage.path(temp_path)

#     # ==========================================
#     # PREDICT
#     # ==========================================
#     predictions = predict_image(full_path)

#     # ==========================================
#     # DELETE TEMP FILE
#     # ==========================================
#     os.remove(full_path)

#     return Response({

#         'status': True,

#         'total_detection': len(predictions),

#         'predictions': predictions

#     })