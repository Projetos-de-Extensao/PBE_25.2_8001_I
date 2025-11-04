from rest_framework import serializers
from .models import VagaMonitoria

class VagaMonitoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VagaMonitoria
        fields = '__all__'