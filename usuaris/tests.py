from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory

from django.contrib.auth.models import User
from .models import Perfil, Organitzador, Administrador
from . import permissions


class TestPermissions(TestCase):

    def setUp(self) -> None:
        # Usuaris
        self.userPerfil = User.objects.create(
            id=1,
            username='usuariPerfil',
            is_active=True
        )
        self.perfil = Perfil.objects.create(
            user=self.userPerfil,
        )

        self.userOrganitzador = User.objects.create(
            id=2,
            username='userOrganitzador',
            is_active=True
        )
        self.organitzador = Organitzador.objects.create(
            user=self.userOrganitzador
        )

        self.userAdministrador = User.objects.create(
            id=3,
            username='userAdministrador',
            is_active=True
        )
        self.administrador = Administrador.objects.create(
            user=self.userAdministrador
        )

    # Qualsevol usuari, com un organitzador, està autenticat
    def test_authenticated_true(self):
        request = APIRequestFactory().get('')
        request.user = self.userOrganitzador
        permission = permissions.IsAuthenticated()
        self.assertTrue(permission.has_permission(request))

    # Si no hi ha usuari no està autenticat
    def test_authenticated_true(self):
        request = APIRequestFactory().get('')
        request.user = None
        permission = permissions.IsAuthenticated()
        self.assertFalse(permission.has_permission(request))

    # Comprovació de si ets perfil
    def test_perfil_true(self):
        request = APIRequestFactory().get('')
        request.user = self.userPerfil
        permission = permissions.IsPerfil()
        self.assertTrue(permission.has_permission(request))

    # Comprovació de si no ets perfil
    def test_perfil_false(self):
        request = APIRequestFactory().get('')
        request.user = self.userOrganitzador
        permission = permissions.IsPerfil()
        self.assertFalse(permission.has_permission(request))

    # Comprovació de si ets organitzador
    def test_organitzador_true(self):
        request = APIRequestFactory().get('')
        request.user = self.userOrganitzador
        permission = permissions.IsOrganitzador()
        self.assertTrue(permission.has_permission(request))

    # Comprovació de si no ets organitzador
    def test_organitzador_false(self):
        request = APIRequestFactory().get('')
        request.user = self.userPerfil
        permission = permissions.IsOrganitzador()
        self.assertFalse(permission.has_permission(request))

    # Comprovació de si ets administrador
    def test_admin_true(self):
        request = APIRequestFactory().get('')
        request.user = self.userAdministrador
        permission = permissions.IsAdmin()
        self.assertTrue(permission.has_permission(request))

    # Comprovació de si no ets administrador
    def test_admin_false(self):
        request = APIRequestFactory().get('')
        request.user = self.userPerfil
        permission = permissions.IsAdmin()
        self.assertFalse(permission.has_permission(request))

    # Comprovació de si ets perfil pots GET en IsAdminOrOrganitzadorEditPerfilRead
    def test_perfilread_true(self):
        request = APIRequestFactory().get('')
        request.user = self.userPerfil
        permission = permissions.IsAdminOrOrganitzadorEditPerfilRead()
        self.assertTrue(permission.has_permission(request))

    # Comprovació de si ets perfil no pots POST en IsAdminOrOrganitzadorEditPerfilRead
    def test_perfilwrite_false(self):
        request = APIRequestFactory().post('')
        request.user = self.userPerfil
        permission = permissions.IsAdminOrOrganitzadorEditPerfilRead()
        self.assertFalse(permission.has_permission(request))

    # Comprovació de si no estàs autenticat pots GET en IsAdminOrOrganitzadorEditOthersRead
    def test_othersread_true(self):
        request = APIRequestFactory().get('')
        request.user = None
        permission = permissions.IsAdminOrOrganitzadorEditOthersRead()
        self.assertTrue(permission.has_permission(request))

    # Comprovació de si no estàs autenticat no pots POST en IsAdminOrOrganitzadorEditOthersRead
    def test_otherswrite_false(self):
        request = APIRequestFactory().post('')
        request.user = None
        permission = permissions.IsAdminOrOrganitzadorEditOthersRead()
        self.assertFalse(permission.has_permission(request))

