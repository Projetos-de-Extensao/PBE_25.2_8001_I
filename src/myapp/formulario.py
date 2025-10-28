from django import forms
from .models import VagaMonitoria

class Formulario(forms.ModelForm):
    class Meta:
        model = VagaMonitoria
        fields = ['disciplina', 'pre_requisitos', 'responsabilidades', 'numero_vagas']
