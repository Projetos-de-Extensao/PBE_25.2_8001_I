# myapp/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import  VagaMonitoriaViewSet, VagaMonitoriaAPIView

router = DefaultRouter()
router.register(r'vagas',  VagaMonitoriaViewSet, basename='vaga-monitoria')

urlpatterns = [
    path('', include(router.urls)),
    path('produtos/baratos/', VagaMonitoriaAPIView(), name='produtos-baratos'),
]