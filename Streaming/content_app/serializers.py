from rest_framework import serializers
from .models import VagaMonitoria

class VagaMonitoriaSerializer(serializers.ModelSerializer):
    professor_nome = serializers.ReadOnlyField(source='professor.username')

    class Meta:
        model = VagaMonitoria
        fields = ['id', 'titulo', 'descricao', 'disciplina', 'professor', 'professor_nome', 'data_criacao', 'disponivel']
        read_only_fields = ['id', 'data_criacao', 'professor_nome']