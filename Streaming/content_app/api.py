# minhaapp/api.py
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import VagaMonitoria
from .serializers import VagaMonitoriaSerializer

class VagaMonitoriaViewSet(viewsets.ModelViewSet):
    queryset = VagaMonitoria.objects.all()
    serializer_class = VagaMonitoriaSerializer

    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        vagas = VagaMonitoria.objects.filter(disponivel=True)
        serializer = self.get_serializer(vagas, many=True)
        return Response(serializer.data)

class VagaMonitoriaAPIView(generics.ListAPIView):
    serializer_class = VagaMonitoriaSerializer

    def get_queryset(self):
        return VagaMonitoria.objects.filter(preco__lt=1000)