from rest_framework import viewsets

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