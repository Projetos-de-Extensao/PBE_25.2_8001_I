from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class TempoRegistro(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Departamento(TempoRegistro):
    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=16, unique=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self) -> str:
        return f"{self.sigla} - {self.nome}" if self.sigla else self.nome


class Disciplina(TempoRegistro):
    nome = models.CharField(max_length=150)
    codigo = models.CharField(max_length=20, unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name="disciplinas")
    carga_horaria = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    periodo = models.CharField(max_length=30)
    semestre = models.CharField(max_length=20)
    coordenador = models.ForeignKey(User, on_delete=models.PROTECT, related_name="disciplinas_coordenadas")
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["codigo"]
        unique_together = ("nome", "departamento", "semestre")

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nome}"


class VagaMonitoriaStatus(models.TextChoices):
    RASCUNHO = "draft", _("Rascunho")
    PUBLICADA = "published", _("Publicada")
    EM_AVALIACAO = "under_review", _("Em Avaliação")
    FINALIZADA = "closed", _("Finalizada")


class VagaMonitoria(TempoRegistro):
    titulo = models.CharField(max_length=150)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, related_name="vagas")
    prerequisitos = models.TextField(blank=True)
    responsabilidades = models.TextField(blank=True)
    periodo_minimo = models.PositiveSmallIntegerField(null=True, blank=True)
    cr_minimo = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                    validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("10"))])
    quantidade_vagas = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    carga_horaria_semanal = models.PositiveSmallIntegerField(default=4, validators=[MinValueValidator(1)])
    bolsa_valor = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    inscricoes_inicio = models.DateField(default=timezone.now)
    inscricoes_fim = models.DateField(default=timezone.now)
    monitoria_inicio = models.DateField(default=timezone.now)
    monitoria_fim = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=VagaMonitoriaStatus.choices, default=VagaMonitoriaStatus.RASCUNHO)
    publicado_em = models.DateTimeField(null=True, blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name="vagas_criadas")
    atualizado_por = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name="vagas_atualizadas")
    permitir_edicao_submetida = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Vaga de Monitoria"
        verbose_name_plural = "Vagas de Monitoria"

    def __str__(self) -> str:
        return f"{self.titulo} - {self.disciplina.codigo}"

    @property
    def inscricoes_abertas(self) -> bool:
        hoje = timezone.now().date()
        return self.status == VagaMonitoriaStatus.PUBLICADA and self.inscricoes_inicio <= hoje <= self.inscricoes_fim

    def clean(self):
        super().clean()
        if self.inscricoes_inicio and self.inscricoes_fim and self.inscricoes_inicio > self.inscricoes_fim:
            raise ValidationError({"inscricoes_fim": _("A data final deve ser posterior ao início.")})
        if self.monitoria_inicio and self.monitoria_fim and self.monitoria_inicio > self.monitoria_fim:
            raise ValidationError({"monitoria_fim": _("O término da monitoria deve ser após o início.")})
        if self.inscricoes_fim and self.monitoria_inicio and self.inscricoes_fim > self.monitoria_inicio:
            raise ValidationError({"monitoria_inicio": _("A monitoria deve iniciar após o fim das inscrições.")})

    def save(self, *args, **kwargs):
        if self.status == VagaMonitoriaStatus.PUBLICADA and not self.publicado_em:
            self.publicado_em = timezone.now()
        if self.status != VagaMonitoriaStatus.PUBLICADA:
            self.publicado_em = self.publicado_em if self.status != VagaMonitoriaStatus.RASCUNHO else None
        super().save(*args, **kwargs)


class CandidaturaStatus(models.TextChoices):
    SUBMETIDA = "submitted", _("Submetida")
    EM_ANALISE = "in_review", _("Em Análise")
    APROVADA = "approved", _("Aprovada")
    LISTA_ESPERA = "waitlist", _("Lista de Espera")
    REJEITADA = "rejected", _("Rejeitada")
    CANCELADA = "cancelled", _("Cancelada")


class Candidatura(TempoRegistro):
    candidato_nome = models.CharField(max_length=100)
    candidato_email = models.EmailField()
    candidato_curso = models.CharField(max_length=100, blank=True)
    candidato_periodo = models.CharField(max_length=30, blank=True)
    candidato_cr = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("10"))],
    )
    historico_escolar = models.FileField(upload_to="documentos/", blank=True)
    curriculo = models.FileField(upload_to="documentos/", blank=True)
    carta_motivacao = models.TextField(blank=True)
    vaga = models.ForeignKey(VagaMonitoria, on_delete=models.CASCADE, related_name="candidaturas")
    status = models.CharField(max_length=20, choices=CandidaturaStatus.choices, default=CandidaturaStatus.SUBMETIDA)
    feedback = models.TextField(blank=True)
    motivo_cancelamento = models.TextField(blank=True)
    ultima_atualizacao_status = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("candidato_email", "vaga")

    def __str__(self) -> str:
        return f"{self.candidato_nome} - {self.vaga.titulo}"

    @property
    def pode_editar(self) -> bool:
        if self.status == CandidaturaStatus.SUBMETIDA:
            return True
        if self.status == CandidaturaStatus.EM_ANALISE and self.vaga.permitir_edicao_submetida:
            return True
        return False


class AuditoriaRegistro(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="auditorias")
    acao = models.CharField(max_length=50)
    modelo = models.CharField(max_length=120)
    objeto_id = models.CharField(max_length=50)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self) -> str:
        return f"{self.acao} - {self.modelo} ({self.criado_em:%Y-%m-%d %H:%M})"


class UserProfile(TempoRegistro):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nome_exibicao = models.CharField(max_length=150, blank=True)
    curriculo_pdf = models.FileField(upload_to="curriculos/", blank=True, null=True)

    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis de Usuário"

    def __str__(self) -> str:
        return self.nome_exibicao or self.user.get_username()

    def clean(self):
        super().clean()
        arquivo = self.curriculo_pdf
        if arquivo and not arquivo.name.lower().endswith(".pdf"):
            raise ValidationError({"curriculo_pdf": _("Envie apenas arquivos PDF.")})


class ResultadoSelecaoChoices(models.TextChoices):
    APROVADO = "approved", _("Aprovado")
    LISTA_ESPERA = "waitlist", _("Lista de Espera")
    REPROVADO = "rejected", _("Reprovado")


class AvaliacaoCandidato(TempoRegistro):
    """
    Modelo para registro de avaliações de candidatos por professores
    """
    candidatura = models.ForeignKey(
        Candidatura, 
        on_delete=models.CASCADE, 
        related_name="avaliacoes"
    )
    avaliador = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name="avaliacoes_realizadas"
    )
    nota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("10"))],
        help_text="Nota da avaliação (0 a 10)"
    )
    criterios_avaliacao = models.JSONField(
        default=dict,
        blank=True,
        help_text="Critérios específicos avaliados (ex: conhecimento técnico, motivação, etc)"
    )
    comentarios = models.TextField(
        blank=True,
        help_text="Comentários e observações sobre o candidato"
    )
    resultado = models.CharField(
        max_length=20,
        choices=ResultadoSelecaoChoices.choices,
        null=True,
        blank=True,
        help_text="Resultado final da seleção"
    )
    mensagem_resultado = models.TextField(
        blank=True,
        help_text="Mensagem padronizada a ser enviada ao candidato"
    )
    resultado_comunicado = models.BooleanField(
        default=False,
        help_text="Indica se o resultado já foi comunicado ao candidato"
    )
    data_comunicacao = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Data em que o resultado foi comunicado"
    )
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Avaliação de Candidato"
        verbose_name_plural = "Avaliações de Candidatos"
        unique_together = ("candidatura", "avaliador")

    def __str__(self) -> str:
        return f"Avaliação de {self.candidatura.candidato_nome} por {self.avaliador.get_full_name()}"

    def save(self, *args, **kwargs):
        # Atualiza o status da candidatura baseado no resultado
        if self.resultado and not self.pk:
            if self.resultado == ResultadoSelecaoChoices.APROVADO:
                self.candidatura.status = CandidaturaStatus.APROVADA
            elif self.resultado == ResultadoSelecaoChoices.LISTA_ESPERA:
                self.candidatura.status = CandidaturaStatus.LISTA_ESPERA
            elif self.resultado == ResultadoSelecaoChoices.REPROVADO:
                self.candidatura.status = CandidaturaStatus.REJEITADA
            self.candidatura.save()
        
        # Registra data de comunicação
        if self.resultado_comunicado and not self.data_comunicacao:
            self.data_comunicacao = timezone.now()
        
        super().save(*args, **kwargs)