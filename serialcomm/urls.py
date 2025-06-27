# serialcomm/urls.py

from django.urls import path
from .views import send_to_serial

urlpatterns = [
    path('api/send-serial', send_to_serial, name='send_to_serial'),
]
