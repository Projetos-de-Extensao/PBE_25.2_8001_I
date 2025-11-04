from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from .views import VagaMonitoriaViewSet

router = DefaultRouter()
router.register(r'vagas', VagaMonitoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]