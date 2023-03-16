from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Esdeveniment
from .serializers import EsdevenimentSerializer


# Create your views here.
class EsdevenimentsView(viewsets.ModelViewSet):
    queryset = Esdeveniment.objects.all()
    serializer_class = EsdevenimentSerializer
    models = Esdeveniment
    permission_classes = []

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'codi': ['in', 'exact'],
        'nom': ['in', 'exact'],
        'dataIni': ['exact'],
        'dataFi': ['exact'],
        'descripcio': ['contains']
    }
    search_fields = ['nom', 'descripcio']
    ordering_fields = ['codi', 'nom', 'dataIni', 'dataFi']
