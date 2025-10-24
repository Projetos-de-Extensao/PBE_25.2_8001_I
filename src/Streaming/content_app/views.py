from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, permissions
from .models import VagaMonitoria
from .serializers import VagaMonitoriaSerializer

class VagaMonitoriaViewSet(viewsets.ModelViewSet):
    queryset = VagaMonitoria.objects.all().order_by('-data_criacao')
    serializer_class = VagaMonitoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # O professor logado é atribuído automaticamente
        serializer.save(professor=self.request.user)