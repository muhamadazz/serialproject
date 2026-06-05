from django.urls import path
from . import views
from . import rfdetr_views

urlpatterns = [
    # YOLO endpoint
    path('detect/', views.detect_plastic, name='detect_yolo'),
    
    # RF-DETR endpoint
    path('detect-rfdetr/', rfdetr_views.detect_plastic, name='detect_rfdetr'),
    
    # Statistics endpoint (untuk perbandingan model)
    path('statistics/', views.get_inference_statistics, name='get_statistics'),
]