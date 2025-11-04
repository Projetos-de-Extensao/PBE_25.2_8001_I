from django.db import models
from django.contrib.auth.models import User  # se for usar o usuário padrão do Django

class VagaMonitoria(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    disciplina = models.CharField(max_length=100)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vagas_monitoria')
    data_criacao = models.DateTimeField(auto_now_add=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.disciplina}"
    