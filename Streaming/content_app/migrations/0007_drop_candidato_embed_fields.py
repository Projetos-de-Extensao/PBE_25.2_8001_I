from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


def copy_candidate_data_forward(apps, schema_editor):
    Candidatura = apps.get_model("content_app", "Candidatura")
    try:
        Candidato = apps.get_model("content_app", "Candidato")
    except LookupError:
        Candidato = None
    if Candidato is None or not hasattr(Candidatura, "candidato_id"):
        return

    atualizaveis = [
        "candidato_nome",
        "candidato_email",
        "candidato_curso",
        "candidato_periodo",
        "candidato_cr",
        "historico_escolar",
        "curriculo",
        "carta_motivacao",
    ]

    for candidatura in Candidatura.objects.select_related("candidato"):
        candidato = getattr(candidatura, "candidato", None)
        if not candidato:
            continue
        candidatura.candidato_nome = candidato.nome or ""
        email = getattr(candidato, "email", "") or f"sem-email-{candidato.pk}@local"
        candidatura.candidato_email = email
        candidatura.candidato_curso = getattr(candidato, "curso", "") or ""
        candidatura.candidato_periodo = getattr(candidato, "periodo_atual", "") or ""
        candidatura.candidato_cr = getattr(candidato, "cr_atual", None)
        candidatura.historico_escolar = getattr(candidato, "historico_escolar", None)
        candidatura.curriculo = getattr(candidato, "curriculo", None)
        candidatura.carta_motivacao = getattr(candidato, "carta_motivacao", "") or ""
        candidatura.save(update_fields=atualizaveis)


class Migration(migrations.Migration):

    dependencies = [
        ("content_app", "0006_departamento_alter_candidato_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidatura",
            name="candidato_nome",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddField(
            model_name="candidatura",
            name="candidato_email",
            field=models.EmailField(default="", max_length=254),
        ),
        migrations.AddField(
            model_name="candidatura",
            name="candidato_curso",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddField(
            model_name="candidatura",
            name="candidato_periodo",
            field=models.CharField(blank=True, default="", max_length=30),
        ),
        migrations.AddField(
            model_name="candidatura",
            name="candidato_cr",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("10"))]),
        ),
        migrations.AddField(
            model_name="candidatura",
            name="historico_escolar",
            field=models.FileField(blank=True, default="", upload_to="documentos/"),
        ),
        migrations.AddField(
            model_name="candidatura",
            name="curriculo",
            field=models.FileField(blank=True, default="", upload_to="documentos/"),
        ),
        migrations.AddField(
            model_name="candidatura",
            name="carta_motivacao",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.RunPython(copy_candidate_data_forward, migrations.RunPython.noop),
        migrations.AlterUniqueTogether(
            name="candidatura",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="candidatura",
            name="candidato",
        ),
        migrations.DeleteModel(
            name="Candidato",
        ),
        migrations.AlterField(
            model_name="candidatura",
            name="candidato_nome",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="candidatura",
            name="candidato_email",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="candidatura",
            name="candidato_curso",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="candidatura",
            name="candidato_periodo",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="candidatura",
            name="historico_escolar",
            field=models.FileField(blank=True, upload_to="documentos/"),
        ),
        migrations.AlterField(
            model_name="candidatura",
            name="curriculo",
            field=models.FileField(blank=True, upload_to="documentos/"),
        ),
        migrations.AlterField(
            model_name="candidatura",
            name="carta_motivacao",
            field=models.TextField(blank=True),
        ),
        migrations.AlterUniqueTogether(
            name="candidatura",
            unique_together={("candidato_email", "vaga")},
        ),
    ]
