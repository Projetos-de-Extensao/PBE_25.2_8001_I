from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from content_app.api import VagaMonitoriaViewSet, VagaMonitoriaAPIView
from content_app import views


router = DefaultRouter()
router.register(r'vagas', VagaMonitoriaViewSet, basename='vaga-monitoria')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API principal
    path('api/', include(router.urls)),

    # Endpoint alternativo com APIView (se necessário)
    path('api/vagas/custom/', VagaMonitoriaAPIView.as_view(), name='vaga-monitoria-api'),

    # Token de autenticação
    path('api/token/', obtain_auth_token, name='api_token_auth'),

    # URLs adicionais do content_app (se houver)
    path('api/', include('content_app.urls')),
]