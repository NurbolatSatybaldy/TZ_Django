"""Главный файл URL конфигурации Django проекта."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls")),
]




