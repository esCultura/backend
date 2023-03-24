from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import AssistenciaAEsdeveniment
from .serializers import AssistenciaAEsdevenimentSerializer


class AssistenciaAEsdevenimentView(viewsets.ModelViewSet):
    queryset = AssistenciaAEsdeveniment.objects.all()
    serializer_class = AssistenciaAEsdevenimentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['perfil', 'esdeveniment']
    ordering_fields = ['perfil', 'esdeveniment']