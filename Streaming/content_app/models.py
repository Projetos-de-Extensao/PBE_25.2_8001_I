from django.db import models
from django.contrib.auth.models import User  # se for usar o usuário padrão do Django

class VagaMonitoria(models.Model):
    titulo = models.CharField(max_length=30)
    disciplina = models.CharField(max_length=100)
    prerequisitos = models.TextField()
    responsabilidades = models.TextField()
    numero_vagas = models.PositiveIntegerField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    disponivel = models.BooleanField(default=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vagas_monitoria')


    def __str__(self):
        return f"{self.titulo} - {self.disciplina} " #({self.numero_vagas} vaga(s))
    

class Candidato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    curso = models.CharField(max_length=100)
    historico_escolar = models.FileField(upload_to='documentos/')
    curriculo = models.FileField(upload_to='documentos/')
    carta_motivacao = models.TextField()

    def __str__(self):
        return self.nome


class Candidatura(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    vaga = models.ForeignKey(VagaMonitoria, on_delete=models.CASCADE)
    data_candidatura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidato.nome} - {self.vaga.disciplina}"