from rest_framework.routers import DefaultRouter

from .api import AvaliacaoCandidatoViewSet, CandidaturaViewSet, DisciplinaViewSet, VagaMonitoriaViewSet

router = DefaultRouter()
router.register(r"disciplinas", DisciplinaViewSet, basename="disciplina")
router.register(r"vagas", VagaMonitoriaViewSet, basename="vaga")
router.register(r"candidaturas", CandidaturaViewSet, basename="candidatura")
router.register(r"avaliacoes", AvaliacaoCandidatoViewSet, basename="avaliacao")

urlpatterns = router.urls