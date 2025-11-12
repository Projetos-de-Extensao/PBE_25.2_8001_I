from django import forms

from .models import Candidatura, VagaMonitoria, VagaMonitoriaStatus


class CandidaturaPublicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        vaga_queryset = kwargs.pop("vaga_queryset", None)
        super().__init__(*args, **kwargs)
        if vaga_queryset is None:
            vaga_queryset = VagaMonitoria.objects.filter(
                status=VagaMonitoriaStatus.PUBLICADA,
                ativo=True,
            )
        self.fields["vaga"].queryset = vaga_queryset.order_by("disciplina__nome", "titulo")
        for nome, campo in self.fields.items():
            if nome == "vaga":
                campo.widget.attrs.setdefault("class", "form-select")
            elif getattr(campo.widget, "input_type", "") == "file":
                campo.widget.attrs.setdefault("class", "form-control")
            else:
                campo.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = Candidatura
        fields = [
            "vaga",
            "candidato_nome",
            "candidato_email",
            "candidato_curso",
            "candidato_periodo",
            "candidato_cr",
            "historico_escolar",
            "curriculo",
            "carta_motivacao",
        ]
        labels = {
            "vaga": "Vaga",
            "candidato_nome": "Nome do candidato",
            "candidato_email": "E-mail do candidato",
            "candidato_curso": "Curso do candidato",
            "candidato_periodo": "Período do candidato",
            "candidato_cr": "CR do candidato",
            "historico_escolar": "Histórico escolar",
            "curriculo": "Currículo",
            "carta_motivacao": "Carta de motivação",
        }
        widgets = {
            "carta_motivacao": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_candidato_email(self):
        email = self.cleaned_data.get("candidato_email", "")
        return email.strip().lower()


class VagaMonitoriaForm(forms.ModelForm):
    class Meta:
        model = VagaMonitoria
        fields = [
            "titulo",
            "disciplina",
            "prerequisitos",
            "responsabilidades",
            "periodo_minimo",
            "cr_minimo",
            "quantidade_vagas",
            "carga_horaria_semanal",
            "bolsa_valor",
            "inscricoes_inicio",
            "inscricoes_fim",
            "monitoria_inicio",
            "monitoria_fim",
            "status",
            "permitir_edicao_submetida",
        ]
        widgets = {
            "prerequisitos": forms.Textarea(attrs={"rows": 3}),
            "responsabilidades": forms.Textarea(attrs={"rows": 3}),
            "inscricoes_inicio": forms.DateInput(attrs={"type": "date"}),
            "inscricoes_fim": forms.DateInput(attrs={"type": "date"}),
            "monitoria_inicio": forms.DateInput(attrs={"type": "date"}),
            "monitoria_fim": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if status not in dict(VagaMonitoriaStatus.choices):
            raise forms.ValidationError("Status inválido para a vaga.")
        return status