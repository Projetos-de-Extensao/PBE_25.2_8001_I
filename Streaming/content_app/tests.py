from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import (
    Candidatura,
    CandidaturaStatus,
    Departamento,
    Disciplina,
    VagaMonitoria,
    VagaMonitoriaStatus,
)
from .serializers import CandidaturaSerializer, VagaMonitoriaSerializer


class WorkflowValidationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_superuser("admin", "admin@example.com", "adminpass")
        self.departamento, _ = Departamento.objects.get_or_create(
            sigla="GER",
            defaults={"nome": "Departamento Geral", "descricao": "Departamento padrão"},
        )
        self.disciplina = Disciplina.objects.create(
            nome="Algoritmos",
            codigo="ALG-101",
            departamento=self.departamento,
            carga_horaria=60,
            periodo="Noturno",
            semestre="2025.1",
            coordenador=self.admin,
        )

    def test_vaga_serializer_prevents_invalid_dates(self):
        payload = {
            "titulo": "Monitoria Algoritmos",
            "disciplina": self.disciplina.id,
            "disciplina_id": self.disciplina.id,
            "prerequisitos": "",
            "responsabilidades": "",
            "periodo_minimo": None,
            "cr_minimo": None,
            "quantidade_vagas": 2,
            "carga_horaria_semanal": 8,
            "bolsa_valor": None,
            "inscricoes_inicio": date.today(),
            "inscricoes_fim": date.today() - timedelta(days=1),
            "monitoria_inicio": date.today(),
            "monitoria_fim": date.today() + timedelta(days=30),
            "status": VagaMonitoriaStatus.PUBLICADA,
            "permitir_edicao_submetida": False,
            "ativo": True,
        }
        serializer = VagaMonitoriaSerializer(
            data=payload,
            context={"request": type("req", (), {"user": self.admin})()},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("inscricoes_fim", serializer.errors)

    def test_candidatura_serializer_blocks_duplicate_and_cr(self):
        vaga = VagaMonitoria.objects.create(
            titulo="Monitoria Algoritmos",
            disciplina=self.disciplina,
            quantidade_vagas=1,
            carga_horaria_semanal=8,
            inscricoes_inicio=date.today(),
            inscricoes_fim=date.today() + timedelta(days=5),
            monitoria_inicio=date.today() + timedelta(days=7),
            monitoria_fim=date.today() + timedelta(days=60),
            status=VagaMonitoriaStatus.PUBLICADA,
            criado_por=self.admin,
        )
        vaga.cr_minimo = 7.0
        vaga.save(update_fields=["cr_minimo"])

        base_payload = {
            "vaga_id": vaga.id,
            "candidato_nome": "João",
            "candidato_email": "joao@example.com",
            "candidato_cr": 5.5,
        }

        serializer = CandidaturaSerializer(data=base_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("candidato_cr", serializer.errors)

        vaga.cr_minimo = 5.0
        vaga.save(update_fields=["cr_minimo"])
        serializer = CandidaturaSerializer(data=base_payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        serializer = CandidaturaSerializer(data=base_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"][0].code, "unique")

        serializer = CandidaturaSerializer(data={**base_payload, "candidato_email": "JOAO@EXAMPLE.COM"})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["non_field_errors"][0].code, "unique")

        candidatura = Candidatura.objects.get()
        candidatura.status = CandidaturaStatus.APROVADA
        candidatura.save(update_fields=["status"])
        serializer = CandidaturaSerializer(
            candidatura,
            data={"status": CandidaturaStatus.CANCELADA},
            partial=True,
        )
        self.assertFalse(serializer.is_valid())
