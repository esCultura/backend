from rest_framework import viewsets

from .models import InteresEnEsdeveniment, InteresEnTematica
from .serializers import InteresEnEsdevenimentSerializer, InteresEnTematicaSerializer


class InteresEnEsdevenimentView(viewsets.ModelViewSet):
    queryset = InteresEnEsdeveniment.objects.all()
    serializer_class = InteresEnEsdevenimentSerializer


class InteresEnTematicaView(viewsets.ModelViewSet):
    queryset = InteresEnTematica.objects.all()
    serializer_class = InteresEnTematicaSerializer
