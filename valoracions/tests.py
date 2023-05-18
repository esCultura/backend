from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory
from django.contrib.auth.models import User
from usuaris.models import Perfil
from esdeveniments.models import Esdeveniment


class TestValoracionsPost(TestCase):

    # Creem un usuari perfil i un esdeveniment
    def setUp(self) -> None:
        self.userPerfil = User.objects.create(
            id=1,
            username='usuariPerfil',
            is_active=True
        )
        self.perfil = Perfil.objects.create(
            user=self.userPerfil,
        )
        self.esdeveniment = Esdeveniment.objects.create(
            codi=1,
        )

    def test_post_valoracions(self):
        url = reverse('valoracions-list')

        # Preparem i executem una POST per una nova valoració
        data = {
            'text': 'Nova valoració',
            'puntuacio': 3,
            'esdeveniment': 1
        }
        request = APIRequestFactory().post(url, data, format='json')
        force_authenticate(request, self.userPerfil)
        view = resolve(url).func
        response = view(request)

        # Comprovem que s'ha creat la valoració correctament
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
