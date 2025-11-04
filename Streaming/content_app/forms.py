from django import forms
from .models import Candidato, VagaMonitoria


class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = '__all__'


class VagaMonitoriaForm(forms.ModelForm):
    class Meta:
        model = VagaMonitoria
        # Exclude professor because we'll set it from request.user in the view
        fields = ['titulo', 'disciplina', 'prerequisitos', 'responsabilidades', 'numero_vagas', 'disponivel']
        widgets = {
            'prerequisitos': forms.Textarea(attrs={'rows': 3}),
            'responsabilidades': forms.Textarea(attrs={'rows': 3}),
        }