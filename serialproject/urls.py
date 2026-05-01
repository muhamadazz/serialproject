# serialproject/urls.py

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('plasticBottleDetection.urls')),
    path('', include('serialcomm.urls')),
]

