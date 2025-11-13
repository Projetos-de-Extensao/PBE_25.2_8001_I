"""Expose API viewsets for external imports without duplicating definitions."""

from .views import AvaliacaoCandidatoViewSet, CandidaturaViewSet, DisciplinaViewSet, VagaMonitoriaViewSet

__all__ = [
    "DisciplinaViewSet",
    "VagaMonitoriaViewSet",
    "CandidaturaViewSet",
    "AvaliacaoCandidatoViewSet",
]