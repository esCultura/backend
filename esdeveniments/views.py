from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.utils.translation import gettext_lazy as _

from .models import Esdeveniment
from .serializers import EsdevenimentSerializer
from .mixins import FilterBackend, PaginationClass


class EsdevenimentsView(viewsets.ModelViewSet):
    queryset = Esdeveniment.objects.all().prefetch_related('tematiques')
    pagination_class = PaginationClass
    serializer_class = EsdevenimentSerializer
    models = Esdeveniment
    permission_classes = []

    filter_backends = [FilterBackend, DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
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
        'espai': ['exact', 'isnull'],
        'email': ['isnull'],
        'telefon': ['isnull'],
        'url': ['isnull'],
    }
    search_fields = ['nom', 'descripcio', 'provincia', 'comarca', 'municipi', 'espai']
    ordering_fields = ['codi', 'nom', 'dataIni', 'dataFi', 'provincia', 'comarca', 'municipi', 'latitud', 'lonngitud', 'espai']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                description=_('Màxim nombre de resultats que es volen obtenir (per defecte=1000)'),
            ),
            openapi.Parameter(
                'latitud', openapi.IN_QUERY, type=openapi.TYPE_NUMBER,
                description=_('Latitud propera dels esdeveniments a retornar'),
            ),
            openapi.Parameter(
                'longitud', openapi.IN_QUERY, type=openapi.TYPE_NUMBER,
                description=_('Longitud propera dels esdeveniments a retornar'),
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
