from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory

from django.contrib.auth.models import User

from usuaris.models import Perfil, Organitzador, Administrador
from .models import Esdeveniment
from .serializers import EsdevenimentSerializer

from . import urls


class TestEsdevenimentsViewGet(TestCase):

    # Creem 3 usuaris: perfil, organitzador i admin.
    # Creem 2 esdeveniments: 1 té organitzador l'organitzador anterior, l'altre no en té
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

        # Esdeveniments
        self.esdevenimentAmbOrganitzador = Esdeveniment.objects.create(
            codi=1,
            nom='Tinc organitzador :)',
            organitzador=self.organitzador
        )
        self.esdevenimentSenseOrganitzador = Esdeveniment.objects.create(
            codi=2,
            nom='Jo no en tinc!'
        )

    # Organitzador ha de poder veure els seus esdeveniments
    def test_get_esdevenimentOrganitzador_organitzador(self):
        url = reverse('esdeveniments-detail', kwargs={"pk": 1})

        # Preparem i executem un GET d'un esdeveniment sent l'organitzador
        request = APIRequestFactory().get(url)
        force_authenticate(request, self.userOrganitzador)
        view = resolve(url).func
        response = view(request, pk=1)

        # Comprovem que hem pogut obtenir l'esdeveniment
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Organitzador no ha de poder veure altres esdeveniments
    def test_get_esdevenimentSenseOrganitzador_organitzador(self):
        url = reverse('esdeveniments-detail', kwargs={"pk": 2})

        # Preparem i executem un GET d'un esdeveniment sent l'organitzador
        request = APIRequestFactory().get(url)
        force_authenticate(request, self.userOrganitzador)
        view = resolve(url).func
        response = view(request, pk=2)

        # Comprovem que no hem pogut obtenir l'esdeveniment
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Els perfils han de poder veure tots els esdeveniments
    def test_get_perfil(self):
        url = reverse('esdeveniments-list')

        # Preparem i executem un LIST d'un esdeveniment sent un perfil
        request = APIRequestFactory().get(url)
        force_authenticate(request, self.userPerfil)
        view = resolve(url).func
        response = view(request)

        # Comprovem que tenim els dos esdeveniments
        self.assertIn(EsdevenimentSerializer(self.esdevenimentAmbOrganitzador).data, response.data)
        self.assertIn(EsdevenimentSerializer(self.esdevenimentSenseOrganitzador).data, response.data)

    # Els administradors han de poder veure tots els esdeveniments
    def test_get_administrador(self):
        url = reverse('esdeveniments-list')

        # Preparem i executem un LIST d'un esdeveniment sent un administrador
        request = APIRequestFactory().get(url)
        force_authenticate(request, self.userPerfil)
        view = resolve(url).func
        response = view(request)

        # Comprovem que tenim els dos esdeveniments
        self.assertIn(EsdevenimentSerializer(self.esdevenimentAmbOrganitzador).data, response.data)
        self.assertIn(EsdevenimentSerializer(self.esdevenimentSenseOrganitzador).data, response.data)


class TestEsdevenimentsViewPost(TestCase):

    # Creem 3 usuaris: perfil, organitzador i admin.
    # Creem 1 esdeveniment qualsevol
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

        # Esdeveniments
        self.esdeveniment = Esdeveniment.objects.create(
            codi=1,
            nom='Un esdeveniment qualsevol',
        )

    # Organitzador pot crear esdeveniments
    def test_post_esdeveniment_organitzador(self):
        url = reverse('esdeveniments-list')

        # Preparem i executem una POST per un nou esdeveniment sent organitzador
        request = APIRequestFactory().post(url, {'nom': 'Nou esdeveniment'}, format='json')
        force_authenticate(request, self.userOrganitzador)
        view = resolve(url).func
        response = view(request)

        # Comprovem que s'ha creat l'esdeveniment correctament
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Administrador pot crear esdeveniments
    def test_post_esdeveniment_administrador(self):
        url = reverse('esdeveniments-list')

        # Preparem i executem una POST per un nou esdeveniment sent organitzador
        request = APIRequestFactory().post(url, {'nom': 'Nou esdeveniment 2'}, format='json')
        force_authenticate(request, self.userAdministrador)
        view = resolve(url).func
        response = view(request)

        # Comprovem que s'ha creat l'esdeveniment correctament
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestEsdevenimentsInfo(TestCase):
    # Creem 1 esdeveniment
    def setUp(self) -> None:
        self.esdeveniment = Esdeveniment.objects.create(
            codi=1,
            nom='Un esdeveniment qualsevol',
            imatges='imatge1,https://imatge2,http://imatge3'
        )

    # Get de les imatgess
    def test_get_imatges_iguals(self):
        # imatge2 i imatge3 no haurien de modificar-se
        self.assertEqual(self.esdeveniment.get_imatges()[1], self.esdeveniment.imatges.split(',')[1])
        self.assertEqual(self.esdeveniment.get_imatges()[2], self.esdeveniment.imatges.split(',')[2])

    def test_get_imatges_modificades(self):
        # imatge1 hauria de quedar amb el prefix d'agenda cultural
        self.assertEqual(self.esdeveniment.get_imatges()[0], 'http://agenda.cultura.gencat.cat' + self.esdeveniment.imatges.split(',')[0])
