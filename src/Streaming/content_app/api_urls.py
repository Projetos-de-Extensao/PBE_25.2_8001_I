from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .api import VagaMonitoriaViewSet,VagaMonitoriaAPIView
from rest_framework import serializers

router = DefaultRouter()
router.register(r'vagas', VagaMonitoriaViewSet, basename='vaga-monitoria')

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('vagas', VagaMonitoriaAPIView(), name='vaga-monitoria-api'),
    path('admin/', admin.site.urls),
    path('api/', include('content_app.urls')),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]