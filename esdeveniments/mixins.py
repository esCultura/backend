from rest_framework import filters, pagination, response
from django.db.models import F, FloatField
from django.db.models.functions import Sqrt


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