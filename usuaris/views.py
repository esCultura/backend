from rest_framework import viewsets

from django.contrib.auth.models import User

from .models import Perfil, Organitzador, Administrador
from .serializers import PerfilSerializer, OrganitzadorSerializer, AdministradorSerializer, SignUpPerfilsSerializer, LoginPerfilSerializer


class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

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