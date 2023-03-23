from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import InteresEnEsdeveniment, InteresEnTematica
from .serializers import InteresEnEsdevenimentSerializer, InteresEnTematicaSerializer


class InteresEnEsdevenimentView(viewsets.ModelViewSet):
    queryset = InteresEnEsdeveniment.objects.all()
    serializer_class = InteresEnEsdevenimentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['perfil', 'esdeveniment']
    ordering_fields = ['perfil', 'esdeveniment']


class InteresEnTematicaView(viewsets.ModelViewSet):
    queryset = InteresEnTematica.objects.all()
    serializer_class = InteresEnTematicaSerializer
