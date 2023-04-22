from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_active


class IsPerfil(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.perfil
        except (ObjectDoesNotExist, AttributeError):
            return False


class IsOrganitzador(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.organitzador
        except (ObjectDoesNotExist, AttributeError):
            return False


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.administrador
        except (ObjectDoesNotExist, AttributeError):
            return False


class IsAdminOrOrganitzadorEditPerfilRead(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and (
                getattr(request.user, 'administrador', False) or
                getattr(request.user, 'organitzador', False) or
                (request.method in permissions.SAFE_METHODS and request.user.perfil)
            )
        except (ObjectDoesNotExist, AttributeError):
            return False
