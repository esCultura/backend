from rest_framework import viewsets, filters, mixins
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from usuaris import permissions
from .models import AssistenciaAEsdeveniment
from .serializers import AssistenciaAEsdevenimentSerializer, EntradaSerializer


class AssistenciaAEsdevenimentView(viewsets.ModelViewSet):
    queryset = AssistenciaAEsdeveniment.objects.all()
    serializer_class = AssistenciaAEsdevenimentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['perfil', 'esdeveniment', 'data']
    ordering_fields = ['perfil', 'esdeveniment', 'data']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EntradaSerializer
        return self.serializer_class


    # Redefinició del mètode DELETE per tal de poder-lo realitzar a la ListView i a través de paràmetres, en aquest cas l'username i el codi de l'esdeveniment.
    # (Les ListViews només suporten les operacions GET i POST, les DELETE requests només estan permeses a les DetailViews)
    @action(methods=['delete'], detail=False)
    def delete(self, request):
        perfil = request.GET.get('perfil', None)
        esdeveniment = request.GET.get('esdeveniment', None)
        if(not (perfil is None or esdeveniment is None)):
            interes = get_object_or_404(self.queryset, perfil=perfil, esdeveniment=esdeveniment)
            interes.delete()
            return Response(status=200, data={'message': f'S\'ha eliminat de forma correcta l\'assistència del perfil {perfil} a l\'esdeveniment amb codi {esdeveniment}'})
        return Response(status=500, data={'error': 'La Request ha de tenir dos paràmetres: perfil (username del perfil) i esdeveniment (codi de l\'esdeveniment)', 'perfil indicat': perfil, 'esdeveniment indicat': esdeveniment})


class EntradaView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = AssistenciaAEsdeveniment.objects.all()
    serializer_class = EntradaSerializer
    permission_classes = [permissions.IsPerfil]

    def get_queryset(self):
        return AssistenciaAEsdeveniment.objects.filter(perfil=self.request.user.perfil)
