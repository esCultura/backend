from django.db.models import Max
from rest_framework import viewsets, filters, generics, mixins, views
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Xat, Missatge
from .serializers import XatSerializer, MissatgeSerializer
from usuaris import permissions


class XatsView(viewsets.ModelViewSet):
    queryset = Xat.objects.all()
    serializer_class = XatSerializer
    model = Xat
    permission_classes = [permissions.IsPerfil]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'id': ['exact', 'in'],
        'nom': ['exact', 'in'],
        'participants__user__username': ['in'],
        'dataCreacio': ['exact', 'range'],
    }
    ordering_fields = ['id', 'nom', 'dataCreacio', 'dataModificacio']

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('participants')
        queryset = queryset.annotate(dataModificacio=Max('missatges__data'))
        # Retornem només els xats del perfil
        queryset = queryset.filter(participants__user=self.request.user)

        return queryset

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if request.user.perfil not in obj.participants.all():
            raise PermissionDenied("No tens permís per executar aquesta acció.")


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
