from django.db import models

# Create your models here.
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    descricao = models.TextField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    

class VagaMonitoria(models.Model):
    disciplina = models.CharField(max_length=100)
    pre_requisitos = models.TextField()
    responsabilidades = models.TextField()
    numero_vagas = models.PositiveIntegerField()
    

    def __str__(self):
        return f"{self.disciplina} ({self.numero_vagas} vagas)"