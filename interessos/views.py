from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import InteresEnEsdeveniment, InteresEnTematica
from .serializers import InteresEnEsdevenimentSerializer, InteresEnTematicaSerializer


class InteresEnEsdevenimentView(viewsets.ModelViewSet):
    queryset = InteresEnEsdeveniment.objects.all()
    serializer_class = InteresEnEsdevenimentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['perfil', 'esdeveniment']
    ordering_fields = ['perfil', 'esdeveniment']

    # Redefinició del mètode DELETE per tal de poder-lo realitzar a la ListView i a través de paràmetres, en aquest cas l'username i el codi de l'esdeveniment.
    # (Les ListViews només suporten les operacions GET i POST, les DELETE requests només estan permeses a les DetailViews)
    @action(methods=['delete'], detail=False)
    def delete(self, request):
        perfil = request.GET.get('perfil', None)
        esdeveniment = request.GET.get('esdeveniment', None)
        if(not (perfil is None or esdeveniment is None)):
            interes = get_object_or_404(self.queryset, perfil=perfil, esdeveniment=esdeveniment)
            interes.delete()
            return Response(status=200, data={'message': f'S\'ha eliminat de forma correcta l\'interès del perfil {perfil} en l\'esdeveniment amb codi {esdeveniment}'})
        return Response(status=500, data={'error': 'La Request ha de tenir dos paràmetres: perfil(username del perfil) i esdeveniment(codi de l\'esdeveniment)', 'perfil indicat': perfil, 'esdeveniment indicat': esdeveniment})


class InteresEnTematicaView(viewsets.ModelViewSet):
    queryset = InteresEnTematica.objects.all()
    serializer_class = InteresEnTematicaSerializer
