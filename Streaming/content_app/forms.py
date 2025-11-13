from django import forms

from .models import AvaliacaoCandidato, Candidatura, ResultadoSelecaoChoices, VagaMonitoria, VagaMonitoriaStatus


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


class AvaliacaoCandidatoForm(forms.ModelForm):
    """
    Formulário para professores avaliarem candidatos
    """
    class Meta:
        model = AvaliacaoCandidato
        fields = [
            "candidatura",
            "nota",
            "criterios_avaliacao",
            "comentarios",
            "resultado",
            "mensagem_resultado",
        ]
        widgets = {
            "candidatura": forms.HiddenInput(),
            "comentarios": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "mensagem_resultado": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "nota": forms.NumberInput(attrs={"class": "form-control", "min": "0", "max": "10", "step": "0.01"}),
            "resultado": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "nota": "Nota (0 a 10)",
            "criterios_avaliacao": "Critérios de Avaliação (JSON)",
            "comentarios": "Comentários e Observações",
            "resultado": "Resultado da Seleção",
            "mensagem_resultado": "Mensagem para o Candidato",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes CSS aos campos
        for nome, campo in self.fields.items():
            if nome != "candidatura" and "class" not in campo.widget.attrs:
                if isinstance(campo.widget, forms.Select):
                    campo.widget.attrs["class"] = "form-select"
                else:
                    campo.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        resultado = cleaned_data.get("resultado")
        mensagem = cleaned_data.get("mensagem_resultado")

        # Se definir resultado, exige mensagem
        if resultado and not mensagem:
            raise forms.ValidationError(
                "É obrigatório incluir uma mensagem ao definir o resultado da seleção."
            )

        return cleaned_data