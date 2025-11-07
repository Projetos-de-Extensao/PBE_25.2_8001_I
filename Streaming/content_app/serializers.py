from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    AvaliacaoCandidatura,
    Candidatura,
    CandidaturaStatus,
    Departamento,
    Disciplina,
    VagaMonitoria,
    VagaMonitoriaStatus,
)


User = get_user_model()


class UsuarioResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")
        read_only_fields = fields


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


class AvaliacaoCandidaturaSerializer(serializers.ModelSerializer):
    avaliador = UsuarioResumoSerializer(read_only=True)
    resultado_display = serializers.CharField(source="get_resultado_display", read_only=True)
    mensagem_padrao = serializers.SerializerMethodField()
    mensagem_final = serializers.SerializerMethodField()

    class Meta:
        model = AvaliacaoCandidatura
        fields = (
            "id",
            "resultado",
            "resultado_display",
            "nota",
            "comentario",
            "mensagem_personalizada",
            "mensagem_padrao",
            "mensagem_final",
            "avaliador",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "resultado_display",
            "mensagem_padrao",
            "mensagem_final",
            "avaliador",
            "created_at",
            "updated_at",
        )

    def get_mensagem_padrao(self, obj):
        return obj.mensagem_padrao

    def get_mensagem_final(self, obj):
        return obj.mensagem_final

    def create(self, validated_data):
        candidatura = self.context["candidatura"]
        avaliador = self.context["avaliador"]
        avaliacao, created = AvaliacaoCandidatura.objects.update_or_create(
            candidatura=candidatura,
            avaliador=avaliador,
            defaults=validated_data,
        )
        self.context["avaliacao_created"] = created
        return avaliacao

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CandidaturaSerializer(serializers.ModelSerializer):
    vaga = VagaMonitoriaSerializer(read_only=True)
    vaga_id = serializers.PrimaryKeyRelatedField(
        queryset=VagaMonitoria.objects.filter(ativo=True),
        source="vaga",
        write_only=True,
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

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
            "created_at",
            "updated_at",
            "ultima_atualizacao_status",
        )
        read_only_fields = ("created_at", "updated_at", "ultima_atualizacao_status")
        extra_kwargs = {
            "candidato_nome": {"required": False, "allow_blank": True, "default": ""},
            "candidato_email": {
                "required": False,
                "allow_blank": True,
                "allow_null": True,
                "default": None,
            },
        }

    def validate(self, attrs):
        vaga = attrs.get("vaga", getattr(self.instance, "vaga", None))
        status = attrs.get("status", getattr(self.instance, "status", CandidaturaStatus.SUBMETIDA))
        if vaga and vaga.status not in {VagaMonitoriaStatus.PUBLICADA, VagaMonitoriaStatus.EM_AVALIACAO}:
            raise serializers.ValidationError({"vaga_id": "Candidaturas só são permitidas em vagas abertas ou em avaliação."})
        if status == CandidaturaStatus.CANCELADA and not attrs.get("motivo_cancelamento"):
            raise serializers.ValidationError({"motivo_cancelamento": "Informe o motivo do cancelamento."})
        email = attrs.get("candidato_email", getattr(self.instance, "candidato_email", None))
        if email:
            email = email.strip().lower()
            attrs["candidato_email"] = email
        else:
            attrs["candidato_email"] = None
        email = attrs["candidato_email"]

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