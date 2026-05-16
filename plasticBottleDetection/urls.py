from django.urls import path
from .views import (
    detect_plastic,
    detect_plastic_efficientdet
)

urlpatterns = [
    path('detect/', detect_plastic),
    path('detect-efficientdet/', detect_plastic_efficientdet),
]