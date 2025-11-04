from rest_framework.routers import DefaultRouter
from .views import VagaMonitoriaViewSet
from rest_framework import serializers

router = DefaultRouter()
router.register(r'vagas', VagaMonitoriaViewSet, basename='vaga-monitoria')

urlpatterns = router.urls