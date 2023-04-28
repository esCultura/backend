from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory

from django.contrib.auth.models import User

from usuaris.models import Perfil, Organitzador
from .models import Xat, Missatge


class TestXatsViewTest(TestCase):

    # Creem 1 perfil i 1 organitzador
    # Creem 2 xats
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

        # Xats
        # Un xat amb el usuari perfil com a participant
        self.xat1 = Xat.objects.create(
            id=1,
        )
        self.xat1.participants.add(self.perfil)
        # Un xat sense cap participant
        self.xat2 = Xat.objects.create(
            id=2
        )

    # Un perfil veu els seus xats
    def test_get_xats_perfil(self):
        url = reverse('xats-detail', kwargs={"pk": 1})

        # Preparem i executem un GET d'un xat teu
        request = APIRequestFactory().get(url)
        force_authenticate(request, self.userPerfil)
        view = resolve(url).func
        response = view(request, pk=1)

        # Comprovem que hem pogut obtenir el xat
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Un perfil no pot veure xats que no són seus
    def test_get_xats_perfil_noparticipant(self):
        url = reverse('xats-detail', kwargs={"pk": 2})

        # Preparem i executem un GET d'un xat teu
        request = APIRequestFactory().get(url)
        force_authenticate(request, self.userPerfil)
        view = resolve(url).func
        response = view(request, pk=2)

        # Comprovem que hem pogut obtenir el xat
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Un organitzador no pot veure xats
    def test_get_xat_organitzador(self):
        url = reverse('xats-detail', kwargs={"pk": 2})

        # Preparem i executem un GET d'un xat que no és teu
        request = APIRequestFactory().get(url)
        force_authenticate(request, self.userPerfil)
        view = resolve(url).func
        response = view(request, pk=2)

        # Comprovem que no hem pogut obtenir el xat
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestMissatgesView(TestXatsViewTest):

    # Aprofitem el setup del TestCase anterior
    # Creem 2 missatges
    def setUp(self) -> None:
        super().setUp()
        # Missatges
        # Un missatge al xat 1
        self.missatge1 = Missatge.objects.create(
            id=1,
            xat=self.xat1,
            creador=self.perfil
        )
        # Un missatge al xat 2
        self.missatge2 = Missatge.objects.create(
            id=2,
            xat=self.xat2,
            creador=self.perfil
        )

    # Un perfil pot veure els missatges d'un xat
    def test_get_missatges(self):
        url = reverse('missatges-detail', kwargs={"xat_id": 1, "pk": 1})

        # Preparem i executem un GET d'un missatge d'un xat teu
        request = APIRequestFactory().get(url)
        force_authenticate(request, self.userPerfil)
        view = resolve(url).func
        response = view(request, xat_id=1, pk=1)

        # Comprovem que hem pogut obtenir el missatge
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Un perfil pot crear missatges
    def test_post_missatges(self):
        url = reverse('missatges-list', kwargs={"xat_id": 1})

        # Preparem i executem una POST per un nou xat
        request = APIRequestFactory().post(url, {'text': 'Hoooola'}, format='json')
        force_authenticate(request, self.userPerfil)
        view = resolve(url).func
        response = view(request, xat_id=1)

        # Comprovem que s'ha creat el xat correctament
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
