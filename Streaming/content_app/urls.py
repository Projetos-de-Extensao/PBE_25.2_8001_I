from rest_framework.routers import DefaultRouter

from .api import CandidaturaViewSet, DisciplinaViewSet, VagaMonitoriaViewSet

router = DefaultRouter()
router.register(r"disciplinas", DisciplinaViewSet, basename="disciplina")
router.register(r"vagas", VagaMonitoriaViewSet, basename="vaga")
router.register(r"candidaturas", CandidaturaViewSet, basename="candidatura")

urlpatterns = router.urls