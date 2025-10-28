from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VagaMonitoriaViewSet

urlpatterns = [
    path('', include(router.urls)),
]
