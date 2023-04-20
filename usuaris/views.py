from rest_framework import viewsets, mixins

from django.contrib.auth.models import User
from rest_framework.decorators import action, api_view

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from social_django.utils import psa

from .models import Perfil, Organitzador, Administrador
from .serializers import PerfilSerializer, PerfilExtendedSerializer, OrganitzadorSerializer, AdministradorSerializer, SignUpPerfilsSerializer, LoginPerfilSerializer, ElMeuPerfilSerializer


class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PerfilExtendedSerializer
        return self.serializer_class

    @action(methods=['GET', 'PUT'], detail=False)
    def jo(self, request):

        if self.request.auth is None:
            return Response(status=400, data={'error': 'No authentication token was provided.'})

        user = Token.objects.get(key=self.request.auth.key).user
        message = 'Els atributs que es poden modificar són: [password, imatge]'

        if request.method == 'PUT':
            newPassword = request.POST.get('password', None)
            newImage = request.POST.get('imatge', None)
            message = 'S\'ha actualitzat els atributs:'
            if newPassword is None and newImage is None:
                message = 'No s\'ha actualitzat cap atribut del perfil.'
            if newPassword is not None:
                user.set_password(newPassword)
                message += ' password'
            if newImage is not None:
                user.perfil.image = newImage
                message += ' ,imatge'
            user.save()
            user.perfil.save()

        serializer = ElMeuPerfilSerializer(user.perfil)
        return Response(status=200, data={**serializer.data, **{'message': message}})


class OrganitzadorView(viewsets.ModelViewSet):
    queryset = Organitzador.objects.all()
    serializer_class = OrganitzadorSerializer

class AdmistradorView(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class LoginPerfilsView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginPerfilSerializer

class SignUpPerfilsView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpPerfilsSerializer

@api_view(['POST'])
@psa()
def GoogleSignIn(request, backend):
    token = request.POST.get('access_token', None)
    if token is None:
        return Response(status=400, data={'error': 'No access_token was provided, you can provide it through an access_token parameter in the body of the request.'})
    user = request.backend.do_auth(token)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        Perfil.objects.create(user=user)
        serializer = ElMeuPerfilSerializer(user.perfil)
        serializer.data['token'] = token
        serializer.data['created'] = created
        return Response(status=200, data=serializer.data)
    else:
        return Response(status=400, data={'errors': {'token': 'Invalid token'}})