from django.test import TestCase
from rest_framework.test import APIRequestFactory

from rest_framework import status

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

        self.url_sign_up_perfils = '/usuaris/sign_up/perfils/'
        self.url_sign_up_organitzadors = '/usuaris/sign_up/organitzadors/'
        self.url_sign_up_admins = '/usuaris/sign_up/admins/'
        self.url_login_perfils = '/usuaris/login/perfils/'
        self.url_login_organitzadors = '/usuaris/login/organitzadors/'
        self.url_login_admins = '/usuaris/login/admins/'
        self.email_perfil = "test@test.com"
        self.email_organitzador = "organitzadorTestComprovaNoActivat@test.com"
        self.email_admin = "admin@admin.com"
        self.username_perfil = "testProfile"
        self.username_organitzador = "testOrganitzador"
        self.username_admin = "admin"
        self.password = "admin4321"

    # Qualsevol usuari, com un organitzador, està autenticat
    def test_authenticated_true(self):
        request = APIRequestFactory().get('')
        request.user = self.userOrganitzador
        permission = permissions.IsAuthenticated()
        self.assertTrue(permission.has_permission(request))

    # Si no hi ha usuari no està autenticat
    def test_authenticated_false(self):
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

    # Comprovació de Sign Up i Login d'un Administrador cas d'éxit
    def test_successful_register_and_login_admin(self):
        # Sign Up Administrador
        response = self.client.post(self.url_sign_up_admins, {"email": self.email_admin, "username": self.username_admin, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Login Perfil
        response2 = self.client.post(self.url_login_admins, {"username": self.username_admin, "password": self.password})
        self.assertEquals(response2.status_code, status.HTTP_201_CREATED)

        self.assertEquals(response.json()['token'], response2.json()['token'])

    # Comprovació de Sign Up i Login d'un Administrador cas Login en l'url dels Perfils
    def test_login_administrador_en_url_perfils(self):
        # Sign Up Administrador
        response = self.client.post(self.url_sign_up_admins, {"email": self.email_admin, "username": self.username_admin, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Login Administrador en url Perfil
        response2 = self.client.post(self.url_login_perfils, {"username": self.username_admin, "password": self.password})
        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)

    # Comprovació de Sign Up i Login d'un Administrador cas Login en l'url dels Organitzadors
    def test_login_administrador_en_url_administradors(self):
        # Sign Up Administrador
        response = self.client.post(self.url_sign_up_organitzadors, {"email": self.email_admin, "username": self.username_admin, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Login Administrador en url Organitzadors
        response2 = self.client.post(self.url_login_organitzadors, {"username": self.username_admin, "password": self.password})
        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)

    # Comprovació de Sign Up i Login d'un Perfil cas d'éxit
    def test_successful_register_and_login_perfil(self):
        # Sign Up Perfil
        response = self.client.post(self.url_sign_up_perfils, {"email": self.email_perfil, "username": self.username_perfil, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Login Perfil
        response2 = self.client.post(self.url_login_perfils, {"username": self.username_perfil, "password": self.password})
        self.assertEquals(response2.status_code, status.HTTP_201_CREATED)

        self.assertEquals(response.json()['token'], response2.json()['token'])

    # Comprovació de Sign Up i Login d'un Perfil cas contrasenya incorrecte
    def test_unsuccessful_register_and_login_perfil(self):
        # Sign Up Perfil
        response = self.client.post(self.url_sign_up_perfils, {"email": self.email_perfil, "username": self.username_perfil, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Login Perfil
        response2 = self.client.post(self.url_login_perfils, {"username": self.username_perfil, "password": self.password + "1"})
        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)

    # Comprovació de Sign Up i Login d'un Perfil cas Login en l'url dels Organitzadors
    def test_login_perfil_en_url_organitzadors(self):
        # Sign Up Perfil
        response = self.client.post(self.url_sign_up_perfils, {"email": self.email_perfil, "username": self.username_perfil, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Login Perfil en url Organitzadors
        response2 = self.client.post(self.url_login_organitzadors, {"username": self.username_perfil, "password": self.password})
        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)

    # Comprovació de Sign Up i Login d'un Perfil cas Login en l'url dels Administradors
    def test_login_perfil_en_url_administradors(self):
        # Sign Up Perfil
        response = self.client.post(self.url_sign_up_perfils, {"email": self.email_perfil, "username": self.username_perfil, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Login Perfil en url Admins
        response2 = self.client.post(self.url_login_admins, {"username": self.username_perfil, "password": self.password})
        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)

    # Comprovació de Sign Up i Login d'un Organitzador cas Login quan l'Organitzador no ha estat acceptat encara per un Administrador
    def test_comprovacio_organitzador_no_activat_on_sign_up(self):
        # Sign Up Organitzador
        response = self.client.post(self.url_sign_up_organitzadors, {"email": self.email_organitzador, "username": self.username_organitzador, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.json()['message'], "El teu compte està pendent d'aprovació, rebràs un correu quan un administrador et verifiqui.")

        # Login Organitzador
        response2 = self.client.post(self.url_login_organitzadors, {"username": self.username_organitzador, "password": self.password})
        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)

    # Comprovació de Sign Up i Login d'un Organitzador cas Login quan l'Organitzador ha estat acceptat per un Administrador
    def test_activacio_organitzadors(self):
        # Sign Up Organitzador
        response = self.client.post(self.url_sign_up_organitzadors, {"email": self.email_organitzador, "username": self.username_organitzador, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.json()['message'], "El teu compte està pendent d'aprovació, rebràs un correu quan un administrador et verifiqui.")

        # Sign Up Administrador
        token_admin = self.client.post(self.url_sign_up_admins, {"email": self.email_admin, "username": self.username_admin, "password": self.password, "password2": self.password}).json()['token']

        # Activació de l'Organitzadors a través de l'Administrador
        response2 = self.client.post(f"/usuaris/organitzadorspendents/{response.json()['user']}/accept/", {'enviar_email': True}, HTTP_AUTHORIZATION=f'Token {token_admin}')
        self.assertEquals(response2.status_code, status.HTTP_200_OK)

        # Login Organitzador
        login_organitzador_response = self.client.post(self.url_login_organitzadors, {"username": self.username_organitzador, "password": self.password})
        self.assertEquals(login_organitzador_response.status_code, status.HTTP_201_CREATED)

    # Comprovació de Sign Up i Login d'un Organitzador cas Login en l'url dels Perfils
    def test_login_organitzador_en_url_perfils(self):
        # Sign Up Organitzador
        response = self.client.post(self.url_sign_up_organitzadors, {"email": self.email_organitzador, "username": self.username_organitzador, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Login Organitzador en url Perfil
        response2 = self.client.post(self.url_login_perfils, {"username": self.username_organitzador, "password": self.password})
        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)

    # Comprovació de Sign Up i Login d'un Organitzador cas Login en l'url dels Administradors
    def test_login_organitzador_en_url_administradors(self):
        # Sign Up Organitzador
        response = self.client.post(self.url_sign_up_organitzadors, {"email": self.email_organitzador, "username": self.username_organitzador, "password": self.password, "password2": self.password})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Login Organitzador en url Admins
        response2 = self.client.post(self.url_login_admins, {"username": self.username_organitzador, "password": self.password})
        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)