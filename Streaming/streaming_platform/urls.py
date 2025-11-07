from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from content_app import views
from content_app.api import CandidaturaViewSet, DisciplinaViewSet, VagaMonitoriaViewSet


router = DefaultRouter()
router.register(r"disciplinas", DisciplinaViewSet, basename="disciplina")
router.register(r"vagas", VagaMonitoriaViewSet, basename="vaga")
router.register(r"candidaturas", CandidaturaViewSet, basename="candidatura")


urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("index/", views.index, name="index"),
    path("vagas/", views.listar_vagas, name="listar_vagas"),
    path("cadastrar/", views.cadastrar_candidato, name="cadastrar_candidato"),
    path("cadastrar/<int:vaga_id>/", views.cadastrar_candidato, name="cadastrar_candidato_vaga"),
    path("area-candidato/", views.area_candidato, name="area_candidato"),
    path("professor/", views.prof_index, name="prof_index"),

    path("admin/", admin.site.urls),

    path("api/", include(router.urls)),
    path("api/token/", obtain_auth_token, name="api_token_auth"),
    path("api/jwt/", TokenObtainPairView.as_view(), name="jwt_obtain_pair"),
    path("api/jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
]