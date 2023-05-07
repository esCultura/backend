from django.test import TestCase

from rest_framework import status

from django.contrib.auth.models import User
from usuaris.models import Perfil, Organitzador, Administrador


class TestPermissions(TestCase):

    def setUp(self) -> None:
        self.perfil_token = self.client.post("/usuaris/sign_up/perfils/", {'email': "temp@temp.com", 'username': "temp", 'password': 'admin4321', 'password2': 'admin4321'}).json()['token']

        userPerfil2 = User.objects.create(
            id=2,
            username='usuariPerfil2',
            is_active=True
        )
        userPerfil3 = User.objects.create(
            id=3,
            username='usuariPerfil3',
            is_active=True
        )
        userPerfil4 = User.objects.create(
            id=4,
            username='usuariPerfil4',
            is_active=True
        )

        self.perfil2 = Perfil.objects.create(
            user=userPerfil2,
        )
        self.perfil3 = Perfil.objects.create(
            user=userPerfil3,
        )
        self.perfil4 = Perfil.objects.create(
            user=userPerfil4,
        )

        self.url_seguiments = "/seguiments/"

    # Comprovació de seguiments entre usuaris cas seguiment exitós
    def test_successful_seguiment(self):
        # Seguiment del Perfil 1 al Perfil 2
        response = self.client.post(self.url_seguiments, {'seguidor': 1, 'seguit': 2})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    # Comprovació de seguiments entre usuaris cas seguiment ja existent
    def test_seguiment_already_exists(self):
        # Seguiment del Perfil 1 al Perfil 2
        response = self.client.post(self.url_seguiments, {'seguidor': 1, 'seguit': 2})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Seguiment del Perfil 1 al Perfil 2
        response2 = self.client.post(self.url_seguiments, {'seguidor': 1, 'seguit': 2})
        self.assertEquals(response2.status_code, status.HTTP_400_BAD_REQUEST)

    # Comprovació de seguiments entre usuaris cas eliminar seguiment
    def test_delete_seguiment(self):
        # Seguiment del Perfil 1 al Perfil 2
        response = self.client.post(self.url_seguiments, {'seguidor': 1, 'seguit': 2})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Eliminació Seguiment del Perfil 1 al Perfil 2
        response2 = self.client.delete(self.url_seguiments + "?seguit=2", {'seguidor': 1, 'seguit': 2}, HTTP_AUTHORIZATION=f'Token {self.perfil_token}')
        self.assertEquals(response2.status_code, status.HTTP_200_OK)

    # Comprovació de seguiments entre usuaris cas seguir molts perfils
    def test_seguiment_a_molts(self):
        # Seguiment del Perfil 1 al Perfil 2
        response = self.client.post(self.url_seguiments, {'seguidor': 1, 'seguit': 2})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Seguiment del Perfil 1 al Perfil 3
        response2 = self.client.post(self.url_seguiments, {'seguidor': 1, 'seguit': 3})
        self.assertEquals(response2.status_code, status.HTTP_201_CREATED)

        # Seguiment del Perfil 1 al Perfil 4
        response3 = self.client.post(self.url_seguiments, {'seguidor': 1, 'seguit': 4})
        self.assertEquals(response3.status_code, status.HTTP_201_CREATED)

        # Comprovar que el perfil 1 segueix a tres perfils
        resp = self.client.get("/usuaris/perfils/1/")
        self.assertEquals(resp.json()['estadistiques']['seguits'], 3)

        # Comprovar que el perfil 2 té 1 seguidor
        resp = self.client.get("/usuaris/perfils/2/")
        self.assertEquals(resp.json()['estadistiques']['seguidors'], 1)

        # Comprovar que el perfil 3 té 1 seguidor
        resp = self.client.get("/usuaris/perfils/3/")
        self.assertEquals(resp.json()['estadistiques']['seguidors'], 1)

        # Comprovar que el perfil 4 té 1 seguidor
        resp = self.client.get("/usuaris/perfils/4/")
        self.assertEquals(resp.json()['estadistiques']['seguidors'], 1)