from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Seguiment
from .serializers import SeguimentSerializer

class SeguimentView(viewsets.ModelViewSet):
    queryset = Seguiment.objects.all()
    serializer_class = SeguimentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['seguidor', 'seguit']
    ordering_fields = ['seguidor', 'seguit']