from rest_framework import viewsets

from django.contrib.auth.models import User
from rest_framework.decorators import action

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Perfil, Organitzador, Administrador
from .serializers import PerfilSerializer, OrganitzadorSerializer, AdministradorSerializer, SignUpPerfilsSerializer, LoginPerfilSerializer, ElMeuPerfilSerializer


class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    #permission_classes = [IsAuthenticated]

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