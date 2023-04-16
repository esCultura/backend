from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_active


class IsPerfil(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.perfil
        except ObjectDoesNotExist:
            return False


class IsOrganitzador(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.organitzador
        except ObjectDoesNotExist:
            return False


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.admin
        except ObjectDoesNotExist:
            return False
