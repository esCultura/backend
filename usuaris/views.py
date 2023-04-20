from rest_framework import viewsets, mixins

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Perfil, Organitzador, Administrador
from .serializers import PerfilSerializer, PerfilExtendedSerializer, OrganitzadorSerializer, AdministradorSerializer, SignUpPerfilsSerializer, LoginPerfilSerializer
from . import permissions


class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PerfilExtendedSerializer
        return self.serializer_class


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