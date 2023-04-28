from django.db.models import Max
from rest_framework import viewsets, filters, mixins, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
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
        # Sabem que el user serà perfil (per permission_classes)
        if request.user.perfil not in obj.participants.all():
            raise PermissionDenied("No tens permís per executar aquesta acció.")


class MissatgesView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Missatge.objects.all()
    serializer_class = MissatgeSerializer
    model = Missatge
    permission_classes = [permissions.IsPerfil]

    def get_queryset(self):
        # Agafem l'id del xat rebut a la URL
        xat_id = self.kwargs['xat_id']
        queryset = super().get_queryset()
        # Filtrem pels missatges que són d'aquell xat
        xat = get_object_or_404(Xat, id=xat_id)
        queryset = queryset.filter(xat=xat)
        return queryset

    def create(self, request, xat_id=None, *args, **kwargs):
        data = request.data.copy()
        # Agafem l'id del xat rebut a la URL
        data['xat_id'] = xat_id
        data['creador_id'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
