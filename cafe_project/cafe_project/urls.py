# cafe_project/cafe_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cafe.urls')),  # Include all URLs from the cafe app
]
