from rest_framework import viewsets

from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

from .models import Perfil, Organitzador, Administrador
from .serializers import PerfilSerializer, OrganitzadorSerializer, AdministradorSerializer


class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

class OrganitzadorView(viewsets.ModelViewSet):
    queryset = Organitzador.objects.all()
    serializer_class = OrganitzadorSerializer

class AdmistradorView(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


@api_view(['POST'])
def loginPerfils(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("No existeix un usuari amb aquest username.")
    
    pwd_valid = check_password(password, user.password)

    if not pwd_valid:
        return Response("Contrasenya incorrecta.")
    
    token, created = Token.objects.get_or_create(user=user)

    return Response(token.key)