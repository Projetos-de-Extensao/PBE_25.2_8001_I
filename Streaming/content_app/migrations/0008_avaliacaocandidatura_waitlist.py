from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content_app", "0007_drop_candidato_embed_fields"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AvaliacaoCandidatura",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("resultado", models.CharField(choices=[("approved", "Aprovado"), ("waitlist", "Lista de Espera"), ("reproved", "Reprovado")], max_length=20)),
                ("nota", models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("10"))])),
                ("comentario", models.TextField(blank=True)),
                ("mensagem_personalizada", models.TextField(blank=True)),
                ("avaliador", models.ForeignKey(on_delete=models.PROTECT, related_name="avaliacoes_realizadas", to=settings.AUTH_USER_MODEL)),
                ("candidatura", models.ForeignKey(on_delete=models.CASCADE, related_name="avaliacoes", to="content_app.candidatura")),
            ],
            options={
                "ordering": ["-created_at"],
                "unique_together": {("candidatura", "avaliador")},
            },
        ),
        migrations.AlterField(
            model_name="candidatura",
            name="status",
            field=models.CharField(choices=[("submitted", "Submetida"), ("in_review", "Em Análise"), ("approved", "Aprovada"), ("waitlist", "Lista de Espera"), ("rejected", "Rejeitada"), ("cancelled", "Cancelada")], default="submitted", max_length=20),
        ),
    ]
