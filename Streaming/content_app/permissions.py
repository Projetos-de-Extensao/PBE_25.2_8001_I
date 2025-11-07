from typing import Any

from rest_framework.permissions import BasePermission, SAFE_METHODS

ADMIN_GROUP = "Admin"
COORDENADOR_GROUP = "Coordenador"
ESTUDANTE_GROUP = "Estudante"


def _user_in_group(user, group_name: str) -> bool:
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()


def is_admin(user) -> bool:
    return bool(user and user.is_authenticated and (user.is_superuser or _user_in_group(user, ADMIN_GROUP)))


def is_coordinator(user) -> bool:
    return bool(user and user.is_authenticated and (_user_in_group(user, COORDENADOR_GROUP) or is_admin(user)))


def is_student(user) -> bool:
    return bool(user and user.is_authenticated and (_user_in_group(user, ESTUDANTE_GROUP) and not user.is_staff))


class IsAuthenticatedReadOnlyOrRole(BasePermission):
    """Allow safe methods for authenticated users, otherwise require role check."""

    required_role = None

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        role_checker = getattr(self, "role_checker", None)
        if callable(role_checker):
            return role_checker(request.user)
        if self.required_role is None:
            return False
        return _user_in_group(request.user, self.required_role)


class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view) -> bool:
        return is_admin(request.user)


class IsCoordinator(IsAuthenticatedReadOnlyOrRole):
    role_checker = staticmethod(is_coordinator)


class IsStudent(BasePermission):
    def has_permission(self, request, view) -> bool:
        return is_student(request.user)


class IsOwnerCoordinator(BasePermission):
    """Object-level check ensuring coordinator owns the object."""

    def has_object_permission(self, request, view, obj: Any) -> bool:
        if is_admin(request.user):
            return True
        if not is_coordinator(request.user):
            return False

        candidato_email = getattr(obj, "candidato_email", None)
        user_email = getattr(request.user, "email", "") or ""
        if candidato_email and user_email and candidato_email.lower() == user_email.lower():
            return True

        disciplina = getattr(obj, "disciplina", None)
        if disciplina and disciplina.coordenador_id == request.user.id:
            return True

        coordenador = getattr(obj, "coordenador", None)
        if coordenador:
            coordenador_id = getattr(coordenador, "id", None)
            if coordenador_id == request.user.id:
                return True

        criado_por = getattr(obj, "criado_por", None)
        if criado_por and getattr(criado_por, "id", None) == request.user.id:
            return True
        return False