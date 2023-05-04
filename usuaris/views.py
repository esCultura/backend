from rest_framework import viewsets

from django.contrib.auth.models import User
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from requests.exceptions import HTTPError

from social_django.utils import psa

from .models import Perfil, Organitzador, Administrador
from .serializers import PerfilSerializer, OrganitzadorSerializer, AdministradorSerializer, SignUpPerfilsSerializer, SignUpOrganitzadorsSerializer, SignUpAdminSerializer, LoginPerfilSerializer, LoginOrganitzadorSerializer, LoginAdminSerializer


class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

    @action(methods=['GET', 'PUT'], detail=False)
    def jo(self, request):

        if self.request.auth is None:
            return Response(status=400, data={'error': 'No authentication token was provided.'})

        user = Token.objects.get(key=self.request.auth.key).user
        message = 'Els atributs que es poden modificar són: [password, imatge, bio]'

        if request.method == 'PUT':
            newPassword = request.POST.get('password', None)
            newImage = request.data.get('imatge', None)
            newBio = request.POST.get('bio', None)

            elementsModificats = []
            if newPassword is not None:
                user.set_password(newPassword)
                elementsModificats.append("password")
            if newImage is not None:
                user.perfil.imatge = newImage
                elementsModificats.append("imatge")
            if newBio is not None:
                user.perfil.bio = newBio
                elementsModificats.append("bio")
            message = 'S\'ha actualitzat els atributs: [' + ", ".join(elementsModificats) + "]"
            if not elementsModificats:
                message = 'No s\'ha actualitzat cap atribut del perfil.'
            user.save()
            user.perfil.save()

        serializer = PerfilSerializer(user.perfil)
        return Response(status=200, data={**serializer.data, **{'message': message}})


class OrganitzadorView(viewsets.ModelViewSet):
    queryset = Organitzador.objects.all()
    serializer_class = OrganitzadorSerializer

class AdmistradorView(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class LoginPerfilsView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = LoginPerfilSerializer

class LoginOrganitzadorsView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginOrganitzadorSerializer

class LoginAdminView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginAdminSerializer

class SignUpPerfilsView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = SignUpPerfilsSerializer

class SignUpOrganitzadorsView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpOrganitzadorsSerializer

class SignUpAdminsView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpAdminSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def GoogleSignIn(request, backend):
    token = request.POST.get('access_token', None)
    if token is None:
        return Response(status=400, data={'error': 'No access_token was provided, you can provide it through an access_token parameter in the body of the request.'})
    try:
        user = request.backend.do_auth(token)
    except HTTPError as e:
        return Response(status=400, data={'errors': {'token': 'Invalid token', 'detail': str(e)}})


    if user:
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            if user.perfil is None:
                Perfil.objects.create(user=user)
            serializer = PerfilSerializer(user.perfil)
            return Response(status=200, data={**serializer.data, 'token': token.key, 'created': created})
        return Response(status=400, data={'errors': 'User deleted their account or was banned by an administrator.'})

    else:
        return Response(status=400, data={'errors': {'token': 'Invalid token'}})