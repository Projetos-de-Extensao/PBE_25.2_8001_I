from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from .models import VagaMonitoria
from .serializers import VagaMonitoriaSerializer

def home(request):
    return HttpResponse("Bem-vindo ao meu site!")

class VagaMonitoriaViewSet(viewsets.ModelViewSet):
    queryset = VagaMonitoria.objects.all().order_by('-data_criacao')
    serializer_class = VagaMonitoriaSerializer