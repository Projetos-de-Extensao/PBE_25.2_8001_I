from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):

    dependencies = [
        ("content_app", "0008_avaliacaocandidatura_waitlist"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidatura",
            name="candidato_nome",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="candidatura",
            name="candidato_email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterUniqueTogether(
            name="candidatura",
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name="candidatura",
            constraint=models.UniqueConstraint(
                fields=("vaga", "candidato_email"),
                condition=Q(candidato_email__isnull=False),
                name="unique_candidatura_vaga_email_not_null",
            ),
        ),
    ]
