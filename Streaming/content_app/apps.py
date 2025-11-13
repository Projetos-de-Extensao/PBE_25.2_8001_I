from django.apps import AppConfig


class ContentAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content_app'

    def ready(self) -> None:
        # Importa sinais que configuram grupos e perfis padrão.
        from . import signals  # noqa: F401
        return super().ready()
