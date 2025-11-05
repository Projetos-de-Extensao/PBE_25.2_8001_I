from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from content_app.api import VagaMonitoriaViewSet, VagaMonitoriaAPIView
from content_app import views
from django.contrib.auth import views as auth_views


router = DefaultRouter()
router.register(r'vagas', VagaMonitoriaViewSet, basename='vaga-monitoria')

urlpatterns = [
    path('', views.index, name='index'),
    path('vagas/', views.listar_vagas, name='listar_vagas'),
    path('cadastrar/', views.cadastrar_candidato, name='cadastrar_candidato'),
    path('cadastrar/<int:vaga_id>/', views.cadastrar_candidato, name='cadastrar_candidato_vaga'),
    path('area-candidato/', views.area_candidato, name='area_candidato'),
    path('professor/', views.prof_index, name='prof_index'),

    path('admin/', admin.site.urls),

    # Authentication URLs (login, logout, password reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # API principal
    path('api/', include(router.urls)),

    # Endpoint alternativo com APIView
    path('api/vagas/custom/', VagaMonitoriaAPIView.as_view(), name='vaga-monitoria-api'),

    # Token de autenticação
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]