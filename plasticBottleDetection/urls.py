from django.urls import path
from .views import detect_plastic

urlpatterns = [
    path('detect/', detect_plastic),
]
