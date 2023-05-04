from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Seguiment
from .serializers import SeguimentSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

class SeguimentView(viewsets.ModelViewSet):
    queryset = Seguiment.objects.all()
    serializer_class = SeguimentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['seguidor', 'seguit']
    ordering_fields = ['seguidor', 'seguit']

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        if self.request.auth is None:
            return Response(status=400, data={'error': 'No authentication token was provided.'})

        user = Token.objects.get(key=self.request.auth.key).user
        seguit = request.GET.get('seguit', None)

        if seguit is not None:
            seguiment = get_object_or_404(self.queryset, seguidor=user.id, seguit=seguit)
            seguiment.delete()
            return Response(status=200, data={'message': f'S\'ha eliminat de forma correcta el seguiment del perfil {user.username} a l\'usuari amb id {seguit}'})
        return Response(status=400, data={'error': 'La Request ha de tenir un paràmetre: seguit (id del perfil que es vol deixar de seguir)'})