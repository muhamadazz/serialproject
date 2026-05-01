from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .services.yolo_model import detect_image

@api_view(['POST'])
def detect_plastic(request):
    if 'image' not in request.FILES:
        return Response({"error": "No image provided"}, status=400)

    image = request.FILES['image']
    file_path = default_storage.save(f"temp/{image.name}", image)

    predictions = detect_image(default_storage.path(file_path))

    default_storage.delete(file_path)

    return Response({
        "predictions": predictions
    }, status=200)