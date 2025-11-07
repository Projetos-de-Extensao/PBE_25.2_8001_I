from django.db import transaction

from .models import AuditoriaRegistro


def registrar_auditoria(usuario, acao: str, instancia, descricao: str = "") -> None:
    """Persist simple audit logs for key workflow actions."""
    if instancia is None:
        return
    modelo = instancia.__class__.__name__
    objeto_id = getattr(instancia, "pk", None)
    with transaction.atomic():
        AuditoriaRegistro.objects.create(
            usuario=usuario if getattr(usuario, "is_authenticated", False) else None,
            acao=acao,
            modelo=modelo,
            objeto_id=str(objeto_id) if objeto_id is not None else "",
            descricao=descricao or "",
        )
