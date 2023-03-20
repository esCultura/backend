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
        'codi': ['exact', 'in'],
        'nom': ['exact', 'in'],
        'dataIni': ['exact', 'range'],
        'dataFi': ['exact', 'range'],
        'descripcio': ['contains'],
        'entrades': ['isnull'],
        'horari': ['isnull'],
        'enllacos': ['isnull'],
        'imatges': ['isnull'],
        'provincia': ['exact', 'in'],
        'comarca': ['exact', 'in'],
        'municipi': ['exact', 'in'],
        'latitud': ['exact', 'range'],
        'longitud': ['exact', 'range'],
        'espai': ['exact', 'isnull'],
        'email': ['isnull'],
        'telefon': ['isnull'],
        'url': ['isnull'],
    }
    search_fields = ['nom', 'descripcio', 'provincia', 'comarca', 'municipi', 'espai']
    ordering_fields = ['codi', 'nom', 'dataIni', 'dataFi', 'provincia', 'comarca', 'municipi', 'latitud', 'lonngitud', 'espai']
