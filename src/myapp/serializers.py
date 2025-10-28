# minhaapp/serializers.py
from rest_framework import serializers
from myapp.models import Produto, VagaMonitoria

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'descricao', 'disponivel']
        read_only_fields = ['id']


class VagaMonitoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VagaMonitoria
        fields = '__all__'