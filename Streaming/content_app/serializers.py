from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (
    AvaliacaoCandidato,
    Candidatura,
    CandidaturaStatus,
    Departamento,
    Disciplina,
    ResultadoSelecaoChoices,
    UserProfile,
    VagaMonitoria,
    VagaMonitoriaStatus,
)


User = get_user_model()


class UsuarioResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")
        read_only_fields = fields


class UserProfileSerializer(serializers.ModelSerializer):
    user = UsuarioResumoSerializer(read_only=True)
    nome = serializers.CharField(source="nome_exibicao", allow_blank=True, required=False)
    curriculo_pdf = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ("id", "user", "nome", "curriculo_pdf", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def validate_curriculo_pdf(self, value):
        if value is None:
            return value
        content_type = getattr(value, "content_type", "").lower()
        if content_type and content_type not in {"application/pdf", "application/x-pdf"}:
            raise serializers.ValidationError("Envie um arquivo PDF válido.")
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("Envie um arquivo PDF válido.")
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("O arquivo deve ter no máximo 5 MB.")
        return value

    def update(self, instance, validated_data):
        nome = validated_data.pop("nome_exibicao", None)
        curriculo = validated_data.get("curriculo_pdf", serializers.empty)

        if nome is not None:
            instance.nome_exibicao = nome
            if instance.user.first_name != nome:
                instance.user.first_name = nome
                instance.user.save(update_fields=["first_name"])

        if curriculo is not serializers.empty:
            if curriculo is None:
                instance.curriculo_pdf = None
            else:
                instance.curriculo_pdf = curriculo

        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name")

    def validate_email(self, value):
        return (value or "").strip().lower()

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UsuarioResumoSerializer(self.user).data
        data["groups"] = list(self.user.groups.values_list("name", flat=True))
        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        data["profile"] = UserProfileSerializer(profile, context=self.context).data
        return data


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ("id", "nome", "sigla", "descricao", "ativo", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")


class DisciplinaSerializer(serializers.ModelSerializer):
    coordenador = UsuarioResumoSerializer(read_only=True)
    coordenador_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="coordenador",
        write_only=True,
    )
    departamento = DepartamentoSerializer(read_only=True)
    departamento_id = serializers.PrimaryKeyRelatedField(
        queryset=Departamento.objects.filter(ativo=True),
        source="departamento",
        write_only=True,
    )
    vagas_ativas = serializers.SerializerMethodField()
    vagas_preview = serializers.SerializerMethodField()

    class Meta:
        model = Disciplina
        fields = (
            "id",
            "nome",
            "codigo",
            "departamento",
            "departamento_id",
            "carga_horaria",
            "periodo",
            "semestre",
            "coordenador",
            "coordenador_id",
            "ativo",
            "vagas_ativas",
            "vagas_preview",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "vagas_ativas", "vagas_preview")

    def get_vagas_ativas(self, obj) -> int:
        return obj.vagas.filter(status=VagaMonitoriaStatus.PUBLICADA, ativo=True).count()

    def get_vagas_preview(self, obj):
        vagas = obj.vagas.select_related("disciplina").order_by("-created_at")[:3]
        return [
            {
                "id": vaga.id,
                "titulo": vaga.titulo,
                "status": vaga.status,
                "status_display": vaga.get_status_display(),
            }
            for vaga in vagas
        ]


class VagaMonitoriaSerializer(serializers.ModelSerializer):
    disciplina = DisciplinaSerializer(read_only=True)
    disciplina_id = serializers.PrimaryKeyRelatedField(
        queryset=Disciplina.objects.filter(ativo=True),
        source="disciplina",
        write_only=True,
    )
    criado_por = UsuarioResumoSerializer(read_only=True)
    atualizado_por = UsuarioResumoSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    inscricoes_abertas = serializers.BooleanField(read_only=True)

    class Meta:
        model = VagaMonitoria
        fields = (
            "id",
            "titulo",
            "disciplina",
            "disciplina_id",
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
            "status_display",
            "publicado_em",
            "criado_por",
            "atualizado_por",
            "permitir_edicao_submetida",
            "ativo",
            "inscricoes_abertas",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "publicado_em",
            "criado_por",
            "atualizado_por",
            "inscricoes_abertas",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        status = attrs.get("status", getattr(self.instance, "status", VagaMonitoriaStatus.RASCUNHO))
        disciplina = attrs.get("disciplina", getattr(self.instance, "disciplina", None))
        if status in {VagaMonitoriaStatus.PUBLICADA, VagaMonitoriaStatus.EM_AVALIACAO} and disciplina and not disciplina.ativo:
            raise serializers.ValidationError({"disciplina_id": "A disciplina precisa estar ativa para publicar a vaga."})

        if status == VagaMonitoriaStatus.PUBLICADA:
            obrigatorios = ("carga_horaria_semanal", "quantidade_vagas", "inscricoes_inicio", "inscricoes_fim")
            for campo in obrigatorios:
                if attrs.get(campo) is None and not getattr(self.instance, campo, None):
                    raise serializers.ValidationError({campo: "Campo obrigatório para vagas publicadas."})

        inicio = attrs.get("inscricoes_inicio", getattr(self.instance, "inscricoes_inicio", None))
        fim = attrs.get("inscricoes_fim", getattr(self.instance, "inscricoes_fim", None))
        if inicio and fim and inicio > fim:
            raise serializers.ValidationError({"inscricoes_fim": "A data final deve ser posterior ao início."})

        monitoria_inicio = attrs.get("monitoria_inicio", getattr(self.instance, "monitoria_inicio", None))
        monitoria_fim = attrs.get("monitoria_fim", getattr(self.instance, "monitoria_fim", None))
        if monitoria_inicio and monitoria_fim and monitoria_inicio > monitoria_fim:
            raise serializers.ValidationError({"monitoria_fim": "O término da monitoria deve ser após o início."})

        if fim and monitoria_inicio and fim > monitoria_inicio:
            raise serializers.ValidationError({"monitoria_inicio": "A monitoria deve iniciar após o fim das inscrições."})

        return attrs


class CandidaturaSerializer(serializers.ModelSerializer):
    vaga = VagaMonitoriaSerializer(read_only=True)
    vaga_id = serializers.PrimaryKeyRelatedField(
        queryset=VagaMonitoria.objects.filter(ativo=True),
        source="vaga",
        write_only=True,
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    avaliacoes = serializers.SerializerMethodField()

    class Meta:
        model = Candidatura
        fields = (
            "id",
            "candidato_nome",
            "candidato_email",
            "candidato_curso",
            "candidato_periodo",
            "candidato_cr",
            "historico_escolar",
            "curriculo",
            "carta_motivacao",
            "vaga",
            "vaga_id",
            "status",
            "status_display",
            "feedback",
            "motivo_cancelamento",
            "avaliacoes",
            "created_at",
            "updated_at",
            "ultima_atualizacao_status",
        )
        read_only_fields = ("created_at", "updated_at", "ultima_atualizacao_status", "avaliacoes")

    def get_avaliacoes(self, obj):
        from .serializers import AvaliacaoCandidatoResumoSerializer
        avaliacoes = obj.avaliacoes.all()
        return AvaliacaoCandidatoResumoSerializer(avaliacoes, many=True).data

    def validate(self, attrs):
        vaga = attrs.get("vaga", getattr(self.instance, "vaga", None))
        status = attrs.get("status", getattr(self.instance, "status", CandidaturaStatus.SUBMETIDA))
        if vaga and vaga.status not in {VagaMonitoriaStatus.PUBLICADA, VagaMonitoriaStatus.EM_AVALIACAO}:
            raise serializers.ValidationError({"vaga_id": "Candidaturas só são permitidas em vagas abertas ou em avaliação."})
        if status == CandidaturaStatus.CANCELADA and not attrs.get("motivo_cancelamento"):
            raise serializers.ValidationError({"motivo_cancelamento": "Informe o motivo do cancelamento."})
        email = attrs.get("candidato_email", getattr(self.instance, "candidato_email", None))
        if not email:
            raise serializers.ValidationError({"candidato_email": "Informe um e-mail válido."})
        email = email.strip().lower()
        attrs["candidato_email"] = email

        candidato_cr = attrs.get("candidato_cr", getattr(self.instance, "candidato_cr", None))
        if vaga and vaga.cr_minimo and candidato_cr is not None and candidato_cr < vaga.cr_minimo:
            raise serializers.ValidationError({"candidato_cr": "CR insuficiente para a vaga."})

        if vaga and email:
            existing = Candidatura.objects.filter(vaga=vaga, candidato_email__iexact=email)
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                error = serializers.ErrorDetail("Já existe uma candidatura para esta vaga.", code="unique")
                raise serializers.ValidationError({"non_field_errors": [error]})
        return attrs

    def update(self, instance, validated_data):
        if not instance.pode_editar:
            raise serializers.ValidationError("A candidatura não pode mais ser editada.")
        return super().update(instance, validated_data)


class AvaliacaoCandidatoSerializer(serializers.ModelSerializer):
    """
    Serializer para avaliações de candidatos
    """
    avaliador = UsuarioResumoSerializer(read_only=True)
    candidatura = CandidaturaSerializer(read_only=True)
    candidatura_id = serializers.PrimaryKeyRelatedField(
        queryset=Candidatura.objects.all(),
        source="candidatura",
        write_only=True,
    )
    resultado_display = serializers.CharField(source="get_resultado_display", read_only=True)

    class Meta:
        model = AvaliacaoCandidato
        fields = (
            "id",
            "candidatura",
            "candidatura_id",
            "avaliador",
            "nota",
            "criterios_avaliacao",
            "comentarios",
            "resultado",
            "resultado_display",
            "mensagem_resultado",
            "resultado_comunicado",
            "data_comunicacao",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("avaliador", "data_comunicacao", "created_at", "updated_at")

    def validate(self, attrs):
        resultado = attrs.get("resultado")
        mensagem = attrs.get("mensagem_resultado", "")
        
        # Se definir resultado, exige mensagem
        if resultado and not mensagem:
            raise serializers.ValidationError({
                "mensagem_resultado": "É obrigatório incluir uma mensagem ao definir o resultado."
            })
        
        # Validar nota se fornecida
        nota = attrs.get("nota")
        if nota is not None and (nota < 0 or nota > 10):
            raise serializers.ValidationError({
                "nota": "A nota deve estar entre 0 e 10."
            })
        
        return attrs

    def create(self, validated_data):
        # Adiciona o avaliador automaticamente
        validated_data["avaliador"] = self.context["request"].user
        return super().create(validated_data)


class AvaliacaoCandidatoResumoSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de avaliações
    """
    avaliador_nome = serializers.CharField(source="avaliador.get_full_name", read_only=True)
    resultado_display = serializers.CharField(source="get_resultado_display", read_only=True)

    class Meta:
        model = AvaliacaoCandidato
        fields = (
            "id",
            "avaliador_nome",
            "nota",
            "resultado",
            "resultado_display",
            "resultado_comunicado",
            "data_comunicacao",
            "created_at",
        )
        read_only_fields = fields