from django.db.models import Max
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Xat, Missatge
from .serializers import XatSerializer, MissatgeSerializer


class XatsView(viewsets.ModelViewSet):
    queryset = Xat.objects.all()
    serializer_class = XatSerializer
    model = Xat
    permission_classes = []

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'id': ['exact', 'in'],
        'nom': ['exact', 'in'],
        'participants__username': ['in'],
        'dataCreacio': ['exact', 'range'],
    }
    ordering_fields = ['id', 'nom', 'dataCreacio', 'dataModificacio']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(dataModificacio=Max('missatges__data'))

        return queryset


class MissatgesView(viewsets.ModelViewSet):
    queryset = Missatge.objects.all()
    serializer_class = MissatgeSerializer
    model = Missatge
    permission_classes = []

    def get_queryset(self):
        # Agafem l'id del xat rebut a la URL
        xat_id = self.kwargs['xat_id']
        queryset = super().get_queryset()
        # Filtrem pels missatges que són d'aquell xat
        xat = get_object_or_404(Xat, id=xat_id)
        queryset = queryset.filter(xat=xat)
        return queryset
