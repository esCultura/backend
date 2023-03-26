from rest_framework import viewsets, filters, pagination, response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, FloatField
from django.db.models.functions import Sqrt

from .models import Esdeveniment
from .serializers import EsdevenimentSerializer


class FilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        lat = request.query_params.get('latitud')
        long = request.query_params.get('longitud')
        if lat and long:
            # Convert latitudes and longitudes to radians
            lat_aux, long_aux = map(float, [lat, long])
            # Calculate distance between two points using Haversine formula
            queryset = queryset.annotate(
                lat_diff=F('latitud') - lat_aux,
                long_diff=F('longitud') - long_aux,
                distancia=Sqrt((F('lat_diff') ** 2) + (F('long_diff') ** 2), output_field=FloatField()),
            ).order_by('distancia')
        return queryset


class PaginationClass(pagination.LimitOffsetPagination):
    max_limit = 1000  # default max limit

    def get_limit(self, request):
        if 'limit' in request.query_params:
            try:
                return int(request.query_params['limit'])
            except ValueError:
                pass
        return self.max_limit

    def get_paginated_response(self, data):
        return response.Response(data)


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
